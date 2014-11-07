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
from urllib2 import urlopen
import json

from bs4 import BeautifulSoup

COMPANY = 'Coca-Cola Company'

# Coca-Cola brands are a major source of false positives and not that
# important to searching on Amazon, so sticking to US brands for now.
#
# TODO: query each country and keep track of which countries brands are in.
#
# This returns JSON for an AJAX script.
# The corresponding page is http://www.coca-colacompany.com/brands/all/
US_BRANDS_URL = 'http://www.coca-colacompany.com/api/getAllBrands?country=united-states'


def scrape_brands():

    brand_json = json.load(urlopen(US_BRANDS_URL))

    for brand in brand_json['brands']:
        name_html = brand['name']['desktop']
        name = BeautifulSoup(name_html).text.strip()  # resolve HTML entities
        if name.endswith('*'):
            yield dict(brand=name[:-1], is_licensed=True)
        else:
            yield name
