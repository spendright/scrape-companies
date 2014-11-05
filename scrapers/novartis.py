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
from urlparse import urljoin

from srs.scrape import scrape_soup



COMPANY = u'Novartis'


NOVARTIS_OTC_START_URL = 'http://www.novartis.com/products/over-the-counter.shtml'
ALCON_PRODUCTS_URL = 'http://www.alcon.com/eye-care-products/'


EXTRA_BRANDS = [COMPANY, 'Alcon']


def scrape_brands():
    for brand in EXTRA_BRANDS:
        yield brand

    start_soup = scrape_soup(NOVARTIS_OTC_START_URL)
    urls = [urljoin(NOVARTIS_OTC_START_URL, a['href'])
            for a in start_soup.select('.tabs.statictabs a')]

    for url in urls:
        if url == NOVARTIS_OTC_START_URL:
            soup = start_soup
        else:
            soup = scrape_soup(url)

        for i in soup.select('.panes .text-container i'):
            yield i.text

    alcon_soup = scrape_soup(ALCON_PRODUCTS_URL)

    start_div = [div for div in alcon_soup.select('div.accordionButton')
                 if div.text.lower() == 'over-the-counter'][0]
    otc_div = start_div.findNextSibling(
        'div', attrs={'class':'accordionContent'})

    for h4 in otc_div.select('h4'):
        yield h4.text
