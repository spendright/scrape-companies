# -*- coding: utf-8 -*-
from os.path import dirname
from os import listdir
from traceback import print_exc
import sys

import scraperwiki

import scrapers

TM_SYMBOLS = u'®\u2120™'  # 2120 is SM symbol


def main():
    failed = False

    for scraper in scraper_modules():
        sys.stderr.write(scraper.__name__ + '\n')
        try:
            records = scraper.scrape()
            if not isinstance(records, dict):
                company = scraper.COMPANY
                records = {company: clean_scraper_output(records)}
        except:
            failed = True
            print_exc()

        save_records(records)

    sys.exit(int(failed))


def save_records(records):
    scraperwiki.sql.execute(
        'CREATE TABLE IF NOT EXISTS brand (company TEXT)')

    for company, brand_to_row in records.iteritems():
        scraperwiki.sql.execute(
            'DELETE FROM brand WHERE COMPANY = ?', [company])
        scraperwiki.sql.commit()
        for brand, row in brand_to_row.iteritems():
            row = dict(brand=brand, company=company, **row)
            scraperwiki.sql.save(
                ['company', 'brand'], row, table_name = 'brand')


def scraper_modules():
    for filename in sorted(listdir(dirname(scrapers.__file__))):
        if filename.endswith('.py') and not filename.startswith('_'):
            module_name = 'scrapers.' + filename[:-3]
            __import__(module_name)
            yield sys.modules[module_name]


def clean_string(s):
    """Convert to unicode, remove extra whitespace, and
    convert fancy apostrophes."""
    s = unicode(s)
    s = s.strip()
    s = s.replace(u'\u2019', "'")
    return s


def clean_brand(brand):
    """clean_string(), plus strip trailing ® or ™"""
    brand = clean_string(brand)
    for c in TM_SYMBOLS:
        if brand.endswith(c):
            brand = brand[:-1]
    return brand


def clean_dict(dict):
    """Clean all string values in a dict."""
    result = {}

    for k, v in dict.iteritems():
        if k == 'brand':
            result[k] = clean_brand(v)
        elif isinstance(v, basestring):
            result[k] = clean_string(v)
        else:
            result[k] = v

    return result


def clean_scraper_output(items):
    """Use this to wrap a scraper. This allows you to write a scraper that
    just emits strings (brand names) or dictionaries with at least the key
    "brand", cleans them up for you, and compiles them into a map from
    brand name to a dict containing other entries to insert into the
    table.
    """
    results = {}

    for item in items:
        if not item:
            continue
        if isinstance(item, dict):

            brand = item.pop('brand')  # modifies dict. that's okay
            brand = clean_brand(brand)
            results[brand] = item
        else:
            brand = clean_brand(item)
            if brand:
                results[brand] = {}

    return results


if __name__ == '__main__':
    main()
