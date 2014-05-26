# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import scraperwiki


COMPANY = 'Clorox'

URL = 'http://www.thecloroxcompany.com/products/our-brands/'


def scrape_brands():

    soup = BeautifulSoup(scraperwiki.scrape(URL))

    for img in soup.select('div.mainCol img'):
        yield img['alt']

    for p in soup.select('div.mainCol p'):
        for text in p.children:
            if not isinstance(text, unicode):
                continue

            brand = ''
            # brands are neatly separated by ® symbols
            if 'include: ' in text:
                brand = text[text.index('include: ') + 9:]
            elif text.startswith(', '):
                brand = text[2:]
            elif text.startswith(' and '):
                brand = text[5:]

            brand = brand.strip()
            if brand:
                yield brand
