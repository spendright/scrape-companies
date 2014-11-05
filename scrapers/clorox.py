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
# -*- coding: utf-8 -*-
from srs.scrape import scrape_soup



COMPANY = 'Clorox'

URL = 'http://www.thecloroxcompany.com/products/our-brands/'


def scrape_brands():

    soup = scrape_soup(URL)

    for img in soup.select('div.mainCol img'):
        yield img['alt']

    for p in soup.select('div.mainCol p'):
        for text in p.children:
            if not isinstance(text, unicode):
                continue

            brand = ''
            # brands are neatly separated by ® symbols
            if 'include: ' in text:
                brand = text[text.index('include: ') + 9:]
            elif text.startswith(', '):
                brand = text[2:]
            elif text.startswith(' and '):
                brand = text[5:]

            brand = brand.strip()
            if brand:
                yield brand
