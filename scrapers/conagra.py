from bs4 import BeautifulSoup
import scraperwiki


COMPANY = 'ConAgra Foods'

URL = 'http://www.conagrafoods.com/our-food/brands'


def scrape_brands():
    soup = BeautifulSoup(scraperwiki.scrape(URL))

    for div in soup.select('#listView div.brandInfo'):
        yield div.a['data-brandname']   # best-annotated brand list ever!