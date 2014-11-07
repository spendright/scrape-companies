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



# TODO: might be able to get useful category information from
# http://www.kraftfoodservice.com/ProductsandBrands/ProductMain.aspx
# and scraping each category from the nav bar at the top.

# TODO: Kraft Foods only operates in the US and Canada. Capri Sun is licensed.

COMPANY = 'Kraft Foods'
URL = 'http://www.kraftfoodsgroup.com/brands/index.aspx'
EXTRA_BRANDS = ['Kraft']


def scrape_brands():
    for b in EXTRA_BRANDS:
        yield b

    soup = scrape_soup(URL)

    for h1 in soup.select('.brand h1'):
        yield h1.text
