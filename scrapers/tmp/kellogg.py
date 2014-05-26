# -*- coding: utf-8 -*-
from ..common import get_soup


R_AND_TM = u'®™'

COMPANY = 'Kellogg'

ALL_BRANDS_URL = 'http://www.kelloggs.com/en_US/product-search.pt-*.html'
EXTRA_BRANDS = ["Kellogg's"]


def scrape_brands():
    for b in EXTRA_BRANDS:
        yield b

    soup = get_soup(ALL_BRANDS_URL)

    for a in soup.select('#navleft-brand a'):
        brand = a.text
        for c in R_AND_TM:
            if c in brand:
                brand = brand[:brand.index(c)].strip()
        yield brand
