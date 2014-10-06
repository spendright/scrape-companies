from srs.scrape import scrape_soup


COMPANY = 'Steelcase'

PRODUCTS_URL = 'http://www.steelcase.com/en/pages/homepage.aspx'


def scrape_brands():
    yield COMPANY

    soup = scrape_soup(PRODUCTS_URL)

    for a in soup.select('.ourBrands li a'):
        yield a.text
