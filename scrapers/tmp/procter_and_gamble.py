from urlparse import urljoin

from ..common import get_soup

COMPANY = 'Procter & Gamble'

_START_URL = 'http://www.pg.com/en_US/brands/index.shtml?document'

_EXTRA_BRANDS = ['James Bond 007']  # fragrance

_LICENSED_BRANDS = ['Dolce & Gabbana']

def scrape_brands():
    yield COMPANY
    for brand in _EXTRA_BRANDS:
        yield brand

    start_soup = get_soup(_START_URL)

    urls = [urljoin(_START_URL, a['href'])
            for a in start_soup.select('#category-navigation a')
            if a.text.strip().startswith('Global')]

    for url in urls:
        soup = get_soup(url)

        for div in soup.select('.list-prods div.product'):
            brand = div.text
            if brand not in _LICENSED_BRANDS:
                yield brand
