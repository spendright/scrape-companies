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
"""Mark companies' former brands as is_former, so we don't try to match them.

If a company has its own scraper, put this information there.
"""
FORMER_BRANDS = [
    ('Groupe Danone', 'LU'),  # sold
    ('LG', 'GoldStar'),  # discontinued
    ('Mattel', 'SoftKey'),  # sold
    ('Microsoft', 'GIANT'),  # stopped selling in 2006
    (u'Microsoft', u'Calista'),  # acquired in 2008, didn't use brand
    ('VF', 'John Varvatos'),  # sold to Lion Capital in 2012
]


def scrape_company():
    for company, brand in FORMER_BRANDS:
        yield 'brand', {'company': company,
                        'brand': brand,
                        'is_former': True}
