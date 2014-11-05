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


COMPANY = 'Kimberly-Clark'

START_URL = 'http://www.kimberly-clark.com/ourbrands.aspx'

# for now, only saving US brands
COUNTRY = 'United States'

SKIP_SECTIONS = [
    'Kimberly-Clark Health Care',
    'Kimberly-Clark Professional',
]

# grabbed by hand from http://www.kchealthcare.com/products.aspx
HEALTH_CARE_BRANDS = [
    'KIMVENT',
    'MIC',
    'MIC-KEY',
]

# grabbed by hand from
# http://www.kimberly-clark.com/brands/kc_professional.aspx
PROFESSIONAL_BRANDS = [
    'Wypall',
    'Kimtech',
    'Kleenguard',
    'Jackson Safety',
]

def scrape_brands():
    yield COMPANY
    for brand in HEALTH_CARE_BRANDS + PROFESSIONAL_BRANDS:
        yield brand

    start_soup = scrape_soup(START_URL)

    urls = [a['href'] for a in start_soup.select('#nav li a')
            if a.text.strip() not in SKIP_SECTIONS]

    for url in urls:
        soup = scrape_soup(url)
        for h3 in soup.select('.accordion h3'):
            brand = h3.text
            if any(a.text.strip() == COUNTRY
                   for a in h3.findNext('div').select('a')):
                yield brand
