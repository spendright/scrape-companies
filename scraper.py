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
"""
import logging
from argparse import ArgumentParser
from os import environ

from srs.db import use_decimal_type_in_sqlite
from srs.harness import run_scrapers
from srs.log import log_to_stderr

log = logging.getLogger('scraper')

# scrapers that used to work but whose start page disappeared
DISABLED_SCRAPERS = {
    'abbott',
    'gsk',
    'reckitt_benckiser',
}


def main():
    opts = parse_args()

    log_to_stderr(verbose=opts.verbose, quiet=opts.quiet)

    scraper_ids = opts.scraper_ids
    if not scraper_ids and environ.get('MORPH_COMPANY_SCRAPERS'):
        scraper_ids = environ['MORPH_COMPANY_SCRAPERS'].split(',')

    skip_scraper_ids = DISABLED_SCRAPERS
    if environ.get('MORPH_SKIP_COMPANY_SCRAPERS'):
        skip_scraper_ids.update(
            environ['MORPH_SKIP_COMPANY_SCRAPERS'].split(','))

    use_decimal_type_in_sqlite()

    run_scrapers(get_records_from_company_scraper,
                 scraper_ids=scraper_ids,
                 skip_scraper_ids=skip_scraper_ids)


def parse_args(args=None):
    parser = ArgumentParser()
    parser.add_argument('scraper_ids', metavar='N', nargs='*',
                        help='whitelist of scrapers to run')
    parser.add_argument(
        '-v', '--verbose', dest='verbose', default=False, action='store_true',
        help='Enable debug logging')
    parser.add_argument(
        '-q', '--quiet', dest='quiet', default=False, action='store_true',
        help='Log warnings only')

    return parser.parse_args(args)


def get_records_from_company_scraper(scraper):
    if hasattr(scraper, 'scrape_company'):
        return scraper.scrape_company()

    if hasattr(scraper, 'scrape_brands'):
        return wrap_brand_scraper(scraper.COMPANY, scraper.scrape_brands())

    raise AttributeError(
        'does not define scrape_company() or scrape_brands()')


def wrap_brand_scraper(company, brands):
    """Use this to wrap a brand scraper that only outputs brand
    dictionaries."""
    for brand in brands:
        if isinstance(brand, dict):
            yield 'brand', dict(company=company, **brand)
        else:
            yield 'brand', dict(company=company, brand=brand)


if __name__ == '__main__':
    main()
