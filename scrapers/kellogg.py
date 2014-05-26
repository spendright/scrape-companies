# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import scraperwiki


COMPANY = 'Kellogg'

URL = 'http://www.kelloggs.com/en_US/product-search.pt-*.html'
EXTRA_BRANDS = ["Kellogg's"]


def scrape_brands():
    for b in EXTRA_BRANDS:
        yield b

    soup = BeautifulSoup(scraperwiki.scrape(URL))

    for a in soup.select('#navleft-brand a'):
        yield a.text
