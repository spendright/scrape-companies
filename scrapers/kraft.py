from bs4 import BeautifulSoup
import scraperwiki
from util import wrap_scraper


COMPANY = 'Kraft Foods'
URL = 'http://www.kraftfoodsgroup.com/brands/index.aspx'
EXTRA_BRANDS = ['Kraft']


def scrape():
    return {COMPANY: wrap_scraper(_scrape())}


def _scrape():
    for b in EXTRA_BRANDS:
        yield b

    soup = BeautifulSoup(scraperwiki.scrape(URL))

    for h1 in soup.select('.brand h1'):
        yield h1.text
