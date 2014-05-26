from ..common import get_soup

NAME = 'Steelcase'

_PRODUCTS_URL = 'http://www.steelcase.com/en/pages/homepage.aspx'


def scrape_brands():
    yield NAME

    soup = get_soup(_PRODUCTS_URL)

    for a in soup.select('.ourBrands li a'):
        yield a.text
