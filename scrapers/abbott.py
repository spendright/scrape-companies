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

from srs.scrape import scrape_soup



# TODO: add in prescription and non-consumer brands
COMPANY = u'Abbott Laboratories'

# TODO: this page no longer exists.
# start here:
START_URL = ('http://www.abbott.com/global/url/content/en_US/20.20:20/product'
             '/Products_By_Category.htm')

SKIP_CATEGORIES = [
    'overview',
    'diagnostics',
    'diabetes',
    'vascular',
    'pharmaceuticals',
]

# AMO is a subsidiary. the page lists AMO products but not "AMO" itself
# AMO's product page is http://www.abbottmedicaloptics.com/products
# but it looks like these products are included in the master list
# except for some lasers.
EXTRA_BRANDS = [
    'Abbott Medical Optics',
    'AMO',
    # Diabetes consumer brands
    # could scrape these, but they're mixed with lots of non-consumer brands
    'FreeStyle',
    'Precision Xtra'
]

NON_BRANDS = [
    'catheters'
]


def scrape_brands():
    yield COMPANY
    for brand in EXTRA_BRANDS:
        yield brand

    start_soup = scrape_soup(START_URL)
    urls = [urljoin(START_URL, a['href'])
            for a in start_soup.select('#nav_secondary a')
            if a.text.strip().lower() not in SKIP_CATEGORIES]

    for url in urls:
        soup = scrape_soup(url)

        for item in soup.select('.product-list-item'):
            brand = item.text
            # leave out generic names of drugs
            if ' (' in brand:
                brand = brand[:brand.index(' (')]

            if brand.strip().lower() in NON_BRANDS:
                continue

            yield brand
