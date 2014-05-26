from urlparse import urljoin

from ..common import get_soup


NAME = u'GlaxoSmithKline'

_START_URL = 'http://www.gsk.com/products/our-consumer-healthcare-products.html'

_SHORTEN_BRANDS = ['Beechams']


def scrape_brands():
    yield NAME

    start_soup = get_soup(_START_URL)

    urls = [urljoin(_START_URL, a['href'])
            for a in start_soup.select('#alphaPaginationContent a')]

    for url in urls:
        if url == _START_URL + '#':
            soup = start_soup
        else:
            soup = get_soup(url)

        for a in soup.select('td.tableItalic a'):
            brand = a.text.strip()
            for prefix in _SHORTEN_BRANDS:
                if brand.startswith(prefix):
                    brand = prefix

            if '/' in brand:
                for part in brand.split('/'):
                    yield part
            else:
                yield brand
