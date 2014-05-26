from bs4 import BeautifulSoup
import scraperwiki

COMPANY = 'Steelcase'

PRODUCTS_URL = 'http://www.steelcase.com/en/pages/homepage.aspx'


def scrape_brands():
    yield COMPANY

    soup = BeautifulSoup(scraperwiki.scrape(PRODUCTS_URL))

    for a in soup.select('.ourBrands li a'):
        yield a.text
