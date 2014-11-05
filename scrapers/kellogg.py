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



COMPANY = 'Kellogg'

URL = 'http://www.kelloggs.com/en_US/product-search.pt-*.html'
EXTRA_BRANDS = ["Kellogg's"]


def scrape_brands():
    for b in EXTRA_BRANDS:
        yield b

    soup = scrape_soup(URL)

    for a in soup.select('#navleft-brand a'):
        yield a.text
