from bs4 import BeautifulSoup
import scraperwiki


COMPANY = 'Electrolux'  # full name is AB Electrolux, but "AB" is like "Inc."

URL = 'http://brandlicensing.electrolux.com/en/our-brands/all/'

# TODO: scrape all regions/countries
COUNTRY = 'USA'

def scrape_brands():
    soup = BeautifulSoup(scraperwiki.scrape(URL))

    for div in soup.select('div.Brands-panel'):
        if div.h3.text == COUNTRY:
            for a in div.select('a.Brands-text'):
                yield a.text
