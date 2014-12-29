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

from bs4 import BeautifulSoup

from srs.scrape import scrape


COMPANY = 'Newell Rubbermaid'
START_URL = 'http://www.newellrubbermaid.com/OurBrands/Pages/AllBrands.aspx'


def scrape_soup_from_bad_html(url):
    """Discard a bad comment that's frustrating BeautifulSoup"""
    return BeautifulSoup(scrape(url)[3:])


def scrape_brands():
    start_soup = scrape_soup_from_bad_html(START_URL)

    # TODO: there isn't a left nav anymore. The individual brand pages
    # still exist (e.g.
    # http://newellrubbermaid.com/OurBrands/Tools/Pages/Irwin.aspx)
    # but it's not clear how to navigate to them.
    nav = start_soup.find('div', class_='switchNav1')

    for a in nav.select('a'):
        url = urljoin(START_URL, a['href'])
        if url == START_URL:
            continue

        category = a.text
        soup = scrape_soup_from_bad_html(url)

        for brand_a in soup.select('.switchNav1 ul li ul li a'):
            yield {'brand': brand_a.text, 'category': category}
