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



COMPANY = u'Hasbro'

# TODO: this page no longer exists. Try:
# http://www.hasbro.com/en-us/brands
#
# look in each ul.brand-list li
# the img alt has the brand name, and the href has a hint as to
# whether it's licensed (e.g.
# http://www.hasbro.com/en-us/toys-games/disney:frozen)

URL = 'http://www.hasbro.com/shop/brandlist.cfm'


# these are licensed by multiple companies
LICENSED_BRANDS = [
    'Angry Birds',
    'Captain America',
    'Disney',
    'Disney Princesses',
    'Elmo',
    'Incredible Hulk',
    'Iron Man',
    'Marvel',
    'Marvel Universe',
    'Sesame Street',
    'Star Trek',
    'Star Wars',  # Star Wars Jedi Force seems to be exclusively Hasbro
    'The Avengers',
    'Thor',
    'Wolverine',
    'Zynga',
]


def scrape_brands():
    yield COMPANY

    soup = scrape_soup(URL)

    for a in soup.select('#hsb_shop_bl_container li ul li a'):
        brand = a.text
        if brand in LICENSED_BRANDS:
            yield dict(brand=brand, is_licensed=True)
        else:
            yield brand
