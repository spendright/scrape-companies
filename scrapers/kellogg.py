# -*- coding: utf-8 -*-
from srs.scrape import scrape_soup



COMPANY = 'Kellogg'

URL = 'http://www.kelloggs.com/en_US/product-search.pt-*.html'
EXTRA_BRANDS = ["Kellogg's"]


def scrape_brands():
    for b in EXTRA_BRANDS:
        yield b

    soup = scrape_soup(URL)

    for a in soup.select('#navleft-brand a'):
        yield a.text
