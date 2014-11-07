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
from srs.scrape import scrape_soup



COMPANY = u'PepsiCo'

URL = 'http://www.pepsico.com/Brands/BrandExplorer'

JOINT_VENTURES_TEXT = [
    ' joint'
]


def scrape_brands():
    yield COMPANY

    soup = scrape_soup(URL)

    for div in soup.select('div.brand'):
        yield {
            'brand': div.img['alt'],
            # "joint venture" brands don't belong to PepsiCo (e.g. Starbucks)
            'is_licensed': any(
                jv_text in div.p.text for jv_text in JOINT_VENTURES_TEXT)
        }
