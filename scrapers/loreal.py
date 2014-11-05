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


COMPANY = u"L'Oréal"

CATEGORY = 'Cosmetics'

URL = 'http://www.lorealusa.com/brands/brands-homepage.aspx'


def scrape_company():
    yield 'company', {'company': COMPANY, 'category': CATEGORY}

    soup = scrape_soup(URL)

    # left hand nav
    section = soup.find('section', id='Section_CorpTopic_Brand')

    for li in section.select('div > ul > li'):
        header_a = li.a

        # L'Oreal Luxe is all licensed brands
        is_licensed = 'Luxe' in header_a.text

        for a in li.select('ul li a'):
            yield 'brand', {'company': COMPANY,
                            # fix bad HTML for VIKTOR&ROLF
                            'brand': a.text.strip().rstrip(';'),
                            'url': a['href'],
                            'is_licensed': is_licensed}
