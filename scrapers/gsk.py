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



COMPANY = u'GlaxoSmithKline'

START_URL = 'http://www.gsk.com/products/our-consumer-healthcare-products.html'

SHORTEN_BRANDS = ['Beechams']


def scrape_brands():
    yield COMPANY

    start_soup = scrape_soup(START_URL)

    urls = [urljoin(START_URL, a['href'])
            for a in start_soup.select('#alphaPaginationContent a')]

    for url in urls:
        if url == START_URL + '#':
            soup = start_soup
        else:
            soup = scrape_soup(url)

        for a in soup.select('td.tableItalic a'):
            brand = a.text.strip()
            for prefix in SHORTEN_BRANDS:
                if brand.startswith(prefix):
                    brand = prefix

            if '/' in brand:
                for part in brand.split('/'):
                    yield part
            else:
                yield brand
