from bs4 import BeautifulSoup
import scraperwiki


COMPANY = 'AB Electrolux'

ALL_BRANDS_URL = 'http://brandlicensing.electrolux.com/node658.aspx?id=53'
NON_BRANDS = ['Close Window']


def scrape_brands():
    soup = BeautifulSoup(scraperwiki.scrape(ALL_BRANDS_URL))

    brands = set()

    for img in soup.select('.area-wide img'):
        brand = img['alt']
        if brand not in NON_BRANDS:
            brands.add(brand)

    return sorted(brands)
