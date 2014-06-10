from bs4 import BeautifulSoup
import scraperwiki


# TODO: might be able to get useful category information from
# http://www.kraftfoodservice.com/ProductsandBrands/ProductMain.aspx
# and scraping each category from the nav bar at the top.

# TODO: Kraft Foods only operates in the US and Canada. Capri Sun is licensed.

COMPANY = 'Kraft Foods'
URL = 'http://www.kraftfoodsgroup.com/brands/index.aspx'
EXTRA_BRANDS = ['Kraft']


def scrape_brands():
    for b in EXTRA_BRANDS:
        yield b

    soup = BeautifulSoup(scraperwiki.scrape(URL))

    for h1 in soup.select('.brand h1'):
        yield h1.text
