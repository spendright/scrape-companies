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
import re

from srs.scrape import scrape_soup



COMPANY = u'AstraZeneca'

URL = 'http://www.astrazeneca.com/Medicines/Products-A-Z'

SEPARATOR_RE = re.compile('[,/]')

# almost all AstraZeneca stuff requires a prescription.
#
# Nexium is approved for OTC, but will be sold by Pfizer. See:
# http://www.fiercepharma.com/story/pfizer-gets-fda-green-light-nexium-otc-launch-az-braces-competition/2014-03-31
OTC_BRANDS = ['emla']  # Lidocaine Cream


def scrape_brands():
    soup = scrape_soup(URL)

    yield COMPANY

    for tr in soup.select('#primary table tbody tr'):
        td = tr.td  # pick first td
        if td:
            td_brands = SEPARATOR_RE.split(td.text)
            for brand in td_brands:
                if ' (' in brand:
                    brand = brand[:brand.index(' (')]

                if brand.strip().lower() in OTC_BRANDS:
                    yield brand
                else:
                    yield dict(brand=brand, is_prescription=True)
