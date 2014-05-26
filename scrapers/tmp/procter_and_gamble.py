from urlparse import urljoin

from ..common import get_soup

COMPANY = 'Procter & Gamble'

START_URL = 'http://www.pg.com/en_US/brands/index.shtml?document'

EXTRA_BRANDS = ['James Bond 007']  # fragrance

LICENSED_BRANDS = ['Dolce & Gabbana']

def scrape_brands():
    yield COMPANY
    for brand in EXTRA_BRANDS:
        yield brand

    start_soup = get_soup(START_URL)

    urls = [urljoin(START_URL, a['href'])
            for a in start_soup.select('#category-navigation a')
            if a.text.strip().startswith('Global')]

    for url in urls:
        soup = get_soup(url)

        for div in soup.select('.list-prods div.product'):
            brand = div.text
            if brand not in LICENSED_BRANDS:
                yield brand
