# -*- coding: utf-8 -*-

#   Copyright 2014 David Marin
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""Main loop for all company scrapers.

If you want to run particular scrapers (for testing), you can put
their names on the command line (e.g. python scraper.py avon kraft).

It's fine to import from this module inside a scraper
(e.g. from scraper import TM_SYMBOLS)
"""
import dumptruck
import logging
import re
import sqlite3
import sys
from argparse import ArgumentParser
from collections import defaultdict
from decimal import Decimal
from datetime import datetime
from os.path import dirname
from os import environ
from os import listdir
from traceback import print_exc
from urlparse import urlparse

import scraperwiki

import scrapers

log = logging.getLogger('scraper')

TM_SYMBOLS = u'®\u2120™'  # 2120 is SM symbol

DISABLED_SCRAPERS = [
    'abbott',  # start page gone
    'gsk',  # start page gone
]


# support decimal type
dumptruck.PYTHON_SQLITE_TYPE_MAP.setdefault(Decimal, 'real')
sqlite3.register_adapter(Decimal, str)


ISO_8601_FMT = '%Y-%m-%dT%H:%M:%S.%fZ'

def main():
    opts = parse_args()

    level = logging.DEBUG if opts.verbose else logging.INFO
    logging.basicConfig(format='%(name)s: %(message)s', level=level)

    scraper_ids = opts.scraper_ids
    if not scraper_ids and environ.get('MORPH_COMPANY_SCRAPERS'):
        scraper_ids = environ['MORPH_COMPANY_SCRAPERS'].split(',')

    skip_scraper_ids = []
    if environ.get('MORPH_SKIP_COMPANY_SCRAPERS'):
        skip_scraper_ids = environ['MORPH_SKIP_COMPANY_SCRAPERS'].split(',')

    init_tables()

    failed = []

    for scraper_id in get_scraper_ids():
        if scraper_ids:
            if scraper_id not in scraper_ids:
                continue
        elif scraper_id in skip_scraper_ids or scraper_id in DISABLED_SCRAPERS:
            log.info('Skipping scraper: {}'.format(scraper_id))
            continue

        log.info('Launching scraper: {}'.format(scraper_id))
        try:
            scraper = load_scraper(scraper_id)
            if hasattr(scraper, 'scrape_company'):
                save_records(scraper_id, scraper.scrape_company())
            elif hasattr(scraper, 'scrape_brands'):
                save_records(scraper_id, wrap_brand_scraper(
                    scraper.COMPANY, scraper.scrape_brands()))
            else:
                raise AttributeError(
                    'does not define scrape_company() or scrape_brands()')
        except:
            failed.append(scraper_id)
            print_exc()

    # just calling exit(1) didn't register on morph.io
    if failed:
        raise Exception(
            'failed to scrape campaigns: {}'.format(', '.join(failed)))


def parse_args(args=None):
    parser = ArgumentParser()
    parser.add_argument('scraper_ids', metavar='N', nargs='*',
                        help='whitelist of scrapers to run')
    parser.add_argument(
        '-v', '--verbose', dest='verbose', default=False, action='store_true',
        help='Enable debug logging')

    return parser.parse_args(args)


# map from table name to fields used for the primary key (not including
# scraper_id). All key fields are currently TEXT
TABLE_TO_KEY_FIELDS = {
    # factual information about a brand (e.g. company, url, etc.)
    'brand': ['company', 'brand'],
    # factual information about which categories a brand belongs to
    'brand_category': ['company', 'brand', 'category'],
    # category hierarchy information
    'category': ['category'],
    # factual information about a company (e.g. url, email, etc.)
    'company': ['company'],
    # factual information about which categories a company belongs to
    'company_category': ['company', 'category'],
    # used to track when a scraper last ran
    'company_scraper': [],
}

TABLE_TO_EXTRA_FIELDS = {
    'company_scraper': [('last_scraped', 'TEXT')],
}


def merge(src, dst):
    """Merge src dictionary into dst. Only overwrite blank values."""
    for k, v in src.iteritems():
        if v is not None and (v != '' or not dst.get(k)):
            dst[k] = v


def init_tables():
    for table, key_fields in sorted(TABLE_TO_KEY_FIELDS.items()):
        key_fields = ['scraper_id'] + key_fields

        sql = 'CREATE TABLE IF NOT EXISTS `{}` ('.format(table)
        for k in key_fields:
            sql += '`{}` TEXT, '.format(k)
        for k, field_type in TABLE_TO_EXTRA_FIELDS.get(table) or ():
            sql += '`{}` {}, '.format(k, field_type)
        sql += 'PRIMARY KEY ({}))'.format(', '.join(key_fields))

        scraperwiki.sql.execute(sql)



def delete_records_from_scraper(scraper_id):
    for table in sorted(TABLE_TO_KEY_FIELDS):
        scraperwiki.sql.execute(
            'DELETE FROM {} WHERE scraper_id = ?'.format(table),
            [scraper_id])


def save_records(scraper_id, records):
    table_to_key_to_row = defaultdict(dict)

    def handle(table, record):
        """handle a record from a scraper, which main contain/imply
        other records"""
        record = record.copy()

        # allow company to be a dict with company info
        if 'company' in record and isinstance(record['company'], dict):
            handle('company', record['company'])
            record['company'] = record['company']['company']

        # allow company to be a dict with company info
        if 'brand' in record and isinstance(record['brand'], dict):
            handle('brand', record['brand'])
            record['company'] = record['brand'].get('company', '')
            record['brand'] = record['brand']['brand']

        company = record.get('company', '')

        # allow list of brands, which can be dicts
        if 'brands' in record:
            for brand in record.pop('brands'):
                company = record['company']
                if isinstance(brand, dict):
                    handle('brand', dict(company=company, **brand))
                else:
                    handle('brand', dict(company=company, brand=brand))

        # strip tm etc. off end of brand
        if record.get('brand'):
            for c in TM_SYMBOLS:
                idx = record['brand'].find(c)
                if idx != -1:
                    record['brand'] = record['brand'][:idx]
                    record['tm'] = c

        # note that brand is also used in the loop above
        brand = record.get('brand', '')

        # allow single category
        if 'category' in record and not (
                table == 'category' or table.endswith('category')):
            record['categories'] = [record.pop('category')]

        # allow list of categories (strings only)
        if 'categories' in record:
            if brand:
                for c in record.pop('categories'):
                    handle('brand_category', dict(
                        company=company, brand=brand, category=c))
            else:
                for category in record.pop('categories'):
                    handle('company_category', dict(
                        company=company, category=category))

        # automatic brand entries
        if 'brand' in record and table != 'brand':
            handle('brand', dict(company=company, brand=brand))

        # automatic category entries
        if 'category' in record and table != 'category':
            handle('category', dict(category=record['category']))
        if 'parent_category' in record:
            handle('category', dict(category=record['parent_category']))

        # automatic company entries
        if 'company' in record and table != 'company':
            handle('company', dict(company=company))

        store(table, record)


    def store(table, record):
        """store an upacked record in table_to_key_to_row, possibly
        merging it with a previous record."""
        key_fields = TABLE_TO_KEY_FIELDS[table]

        # clean strings before storing them
        for k in record:
            if k is None:
                del record[k]
            elif isinstance(record[k], basestring):
                record[k] = clean_string(record[k])

        # verify that URLs are absolute
        for k in record:
            if k.split('_')[-1] == 'url':
                if record[k] and not urlparse(record[k]).scheme:
                    raise ValueError('{} has no scheme: {}'.format(
                        k, repr(record)))

        for k in key_fields:
            if record.get(k) is None:
                record[k] = ''

        # disallow empty company. Easy to forget this when converting
        # from scrape_brands() to scrape_company().
        if 'company' in record and not record['company']:
            raise ValueError('empty company: {}'.format(repr(record)))

        key = tuple(record[k] for k in key_fields)

        log.debug('`{}` {}: {}'.format(table, repr(key), repr(record)))

        if key in table_to_key_to_row[table]:
            merge(record, table_to_key_to_row[table][key])
        else:
            table_to_key_to_row[table][key] = record

    for record_type, record in records:
        handle(record_type, record)

    # add the time this campaign was scraped
    handle('company_scraper', {
        'last_scraped': datetime.utcnow().strftime(ISO_8601_FMT)})


    delete_records_from_scraper(scraper_id)

    for table in table_to_key_to_row:
        key_fields = TABLE_TO_KEY_FIELDS[table]

        for key, row in table_to_key_to_row[table].iteritems():
            scraperwiki.sql.save(
                ['scraper_id'] + key_fields,
                dict(scraper_id=scraper_id, **row),
                table_name=table)


def get_scraper_ids():
    for filename in sorted(listdir(dirname(scrapers.__file__))):
        if filename.endswith('.py') and not filename.startswith('_'):
            yield filename[:-3]


def load_scraper(name):
    module_name = 'scrapers.' + name
    __import__(module_name)
    return sys.modules[module_name]


def clean_string(s):
    """Convert to unicode, remove extra whitespace, and
    convert fancy apostrophes."""
    s = unicode(s)
    s = s.strip()
    s = s.replace(u'\u2019', "'")
    s = s.replace(u'\xa0', ' ')
    return s


def wrap_brand_scraper(company, brands):
    """Use this to wrap a brand scraper that only outputs brand
    dictionaries."""
    for brand in brands:
        if isinstance(brand, dict):
            yield 'brand', dict(company=company, **brand)
        else:
            yield 'brand', dict(company=company, brand=brand)


# UTILITY CODE FOR SCRAPERS

def scrape_copyright(soup, required=True):
    """Quick and dirty copyright notice scraper."""
    for s in soup.stripped_strings:
        if s.startswith(u'©'):
            return s

    if required:
        raise ValueError('Copyright notice not found!')


TWITTER_URL_RE = re.compile(r'^https?://(www\.)?twitter\.com/(\w+)/?$', re.I)


def scrape_twitter_handle(soup, required=True):
    """Find twitter handle on page."""
    for a in soup.findAll('a'):
        m = TWITTER_URL_RE.match(a.get('href', ''))
        if m:
            # "share" isn't a twitter handle
            if m.group(2) == 'share':
                continue

            handle = '@' + m.group(2)
            # use capitalization of handle in text, if aviailable
            if a.text and a.text.strip().lower() == handle.lower():
                handle = a.text.strip()
            # TODO: scrape twitter page to get capitalization there
            return handle

    if required:
        raise ValueError('Twitter handle not found!')


FACEBOOK_URL_RE = re.compile(
    r'^https?://(www\.)facebook\.com/(([\w-]+)|pages/[\w-]+/\d+)/?$', re.I)

def scrape_facebook_url(soup, required=True):
    """Find twitter handle on page."""
    for a in soup.findAll('a'):
        url = a.get('href')
        if url and FACEBOOK_URL_RE.match(url):
            # normalize url scheme; Facebook now uses HTTPS
            if url.startswith('http://'):
                url = 'https://' + url[7:]
            return url

    if required:
        raise ValueError('Facebook URL not found!')



if __name__ == '__main__':
    main()
