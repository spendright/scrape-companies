from bs4 import BeautifulSoup
import scraperwiki


COMPANY = 'Electrolux'  # full name is AB Electrolux, but "AB" is like "Inc."

URL = 'http://brandlicensing.electrolux.com/node658.aspx?id=53'
NON_BRANDS = ['Close Window']


def scrape_brands():
    soup = BeautifulSoup(scraperwiki.scrape(URL))

    brands = set()

    for img in soup.select('.area-wide img'):
        brand = img['alt']
        if brand not in NON_BRANDS:
            brands.add(brand)

    return sorted(brands)
