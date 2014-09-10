# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import scraperwiki

COMPANY = u"L'Oréal"

CATEGORY = 'Cosmetics'

URL = 'http://www.lorealusa.com/brands/brands-homepage.aspx'


def scrape_company():
    yield 'company', {'company': COMPANY, 'category': CATEGORY}

    soup = BeautifulSoup(scraperwiki.scrape(URL))

    # left hand nav
    section = soup.find('section', id='Section_CorpTopic_Brand')

    for li in section.select('div > ul > li'):
        header_a = li.a

        # L'Oreal Luxe is all licensed brands
        is_licensed = 'Luxe' in header_a.text

        for a in li.select('ul li a'):
            yield 'brand', {'company': COMPANY,
                            'brand': a.text,
                            'url': a['href'],
                            'is_licensed': is_licensed}
