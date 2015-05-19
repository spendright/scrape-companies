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


COMPANY = 'Avon'

# online store is blocked by robots.txt; try
# https://www.avon.com/category/allbrands instead

# going to scrape brands off their online store
START_URL = 'http://shop.avon.com/product_list.aspx'

# You'd think more of these would need to have "Avon" prepended, but
# "Naturals" (not "Avon Naturals") is actually a brand you can
# filter on on Amazon!

# skip the hair care category; these are all just types of
# Avon Advance Techniques
SKIP_CATEGORIES = ['hair care']
MORE_BRANDS = ['Advance Techniques']


def scrape_brands():
    yield COMPANY
    for brand in MORE_BRANDS:
        yield brand

    start_soup = scrape_soup(START_URL)

    urls = [a['href'] for a in start_soup.select('div.topmenu a')
            if a['title'].lower() not in SKIP_CATEGORIES]

    for url in urls:
        soup = scrape_soup(url)

        for a in soup.select('div#shopByBrand a'):
            yield a.text
