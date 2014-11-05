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



COMPANY = 'Electrolux'  # full name is AB Electrolux, but "AB" is like "Inc."

URL = 'http://brandlicensing.electrolux.com/en/our-brands/all/'

# TODO: scrape all regions/countries
COUNTRY = 'USA'

def scrape_brands():
    soup = scrape_soup(URL)

    for div in soup.select('div.Brands-panel'):
        if div.h3.text == COUNTRY:
            for a in div.select('a.Brands-text'):
                yield a.text
