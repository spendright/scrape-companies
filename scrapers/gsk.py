from urlparse import urljoin

from bs4 import BeautifulSoup
import scraperwiki


COMPANY = u'GlaxoSmithKline'

START_URL = 'http://www.gsk.com/products/our-consumer-healthcare-products.html'

SHORTEN_BRANDS = ['Beechams']


def scrape_brands():
    yield COMPANY

    start_soup = BeautifulSoup(scraperwiki.scrape(START_URL))

    urls = [urljoin(START_URL, a['href'])
            for a in start_soup.select('#alphaPaginationContent a')]

    for url in urls:
        if url == START_URL + '#':
            soup = start_soup
        else:
            soup = BeautifulSoup(scraperwiki.scrape(url))

        for a in soup.select('td.tableItalic a'):
            brand = a.text.strip()
            for prefix in SHORTEN_BRANDS:
                if brand.startswith(prefix):
                    brand = prefix

            if '/' in brand:
                for part in brand.split('/'):
                    yield part
            else:
                yield brand
