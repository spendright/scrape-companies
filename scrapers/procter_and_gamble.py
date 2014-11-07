# -*- coding: utf-8 -*-

#   Copyright 2014 SpendRight, Inc.
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
from urlparse import urljoin

from srs.scrape import scrape_soup


COMPANY = 'Procter & Gamble'

START_URL = 'http://www.pg.com/en_US/brands/index.shtml?document'

EXTRA_BRANDS = ['James Bond 007']  # fragrance

LICENSED_BRANDS = ['Dolce & Gabbana']

def scrape_brands():
    yield COMPANY
    for brand in EXTRA_BRANDS:
        yield brand

    start_soup = scrape_soup(START_URL)

    urls = [urljoin(START_URL, a['href'])
            for a in start_soup.select('#category-navigation a')
            if a.text.strip().startswith('Global')]

    for url in urls:
        soup = scrape_soup(url)

        for div in soup.select('.list-prods div.product'):
            brand = div.text
            if brand not in LICENSED_BRANDS:
                yield brand
