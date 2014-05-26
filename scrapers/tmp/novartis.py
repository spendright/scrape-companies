# -*- coding: utf-8 -*-
from urlparse import urljoin

from ..common import get_soup


COMPANY = u'Novartis'


NOVARTIS_OTC_START_URL = 'http://www.novartis.com/products/over-the-counter.shtml'
ALCON_PRODUCTS_URL = 'http://www.alcon.com/eye-care-products/'

R_AND_TM = u'®™'


EXTRA_BRANDS = [COMPANY, 'Alcon']


def scrape_brands():
    for brand in EXTRA_BRANDS:
        yield brand

    start_soup = get_soup(NOVARTIS_OTC_START_URL)
    urls = [urljoin(NOVARTIS_OTC_START_URL, a['href'])
            for a in start_soup.select('.tabs.statictabs a')]

    for url in urls:
        if url == NOVARTIS_OTC_START_URL:
            soup = start_soup
        else:
            soup = get_soup(url)

        for i in soup.select('.panes .text-container i'):
            yield i.text

    alcon_soup = get_soup(ALCON_PRODUCTS_URL)

    start_div = [div for div in alcon_soup.select('div.accordionButton')
                 if div.text.lower() == 'over-the-counter'][0]
    otc_div = start_div.findNextSibling(
        'div', attrs={'class':'accordionContent'})

    for h4 in otc_div.select('h4'):
        brand = h4.text.strip()
        for c in R_AND_TM:
            if c in brand:
                brand = brand[:brand.index(c)].strip()
        if brand:
            yield brand
