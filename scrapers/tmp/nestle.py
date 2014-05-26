# -*- coding: utf-8 -*-
from urlparse import urljoin

from ..common import get_soup

# using unaccented version for consistency with ClimateCounts
COMPANY = 'Nestle' #u'Nestlé'

R_AND_TM = u'®™'

START_URL = 'http://www.nestleusa.com/brands'

SKIP_LINKS = ['websites']


def scrape_brands():
    yield COMPANY

    start_soup = get_soup(START_URL)

    urls = [urljoin(START_URL, a['href'])
            for a in start_soup.select('#sNavigation a')
            if a.text.strip().lower() not in SKIP_LINKS]

    for url in urls:
        soup = get_soup(url)

        for a in soup.select('.brandCarousel a'):
            href = a['href']
            # weirdly, brand is only available in the URL fragment
            if href.startswith('#'):
                href = href[1:]
            if '|' in href:
                href = href[:href.index('|')]

            # stop at the (r)/(tm)
            for c in R_AND_TM:
                if c in href:
                    href = href[:href.index(c)]

            yield href
