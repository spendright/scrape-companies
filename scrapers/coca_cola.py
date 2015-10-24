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
from urlparse import urljoin
from urllib2 import urlopen
import json

from bs4 import BeautifulSoup

COMPANY = 'Coca-Cola Company'

COMPANY_URL = 'http://www.coca-colacompany.com/'

# Coca-Cola brands are a major source of false positives and not that
# important to searching on Amazon, so sticking to US brands for now.
#
# TODO: query each country and keep track of which countries brands are in.
#
# This returns JSON for an AJAX script.

ALL_BRANDS_URL = 'http://www.coca-colacompany.com/brands/all/'

# TODO: fetch brands for each country
US_BRANDS_JSON_URL = 'http://www.coca-colacompany.com/brands/all/_jcr_content/pageContent/allbrandslist.Ajax.json/us.json'


def scrape_company():

    yield 'company', {'company': COMPANY, 'url': COMPANY_URL}

    brand_json = json.load(urlopen(US_BRANDS_JSON_URL))

    for brand_dict in brand_json['brands']:
        brand = dict(company=COMPANY)

        name_html = brand_dict['name']['desktop']
        name = BeautifulSoup(name_html).text.strip()  # resolve HTML entities
        if name.endswith('*'):
            brand['brand'] = name[:-1]
            brand['is_licensed'] = True
        else:
            brand['brand'] = name

        if brand_dict['brand_url']:
            brand['url'] = urljoin(ALL_BRANDS_URL, brand_dict['brand_url'])

        yield 'brand', brand
