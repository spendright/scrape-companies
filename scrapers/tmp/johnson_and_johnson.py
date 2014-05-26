from bs4 import BeautifulSoup
import scraperwiki


COMPANY = u'Johnson & Johnson'

URL = 'http://www.jnj.com/healthcare-products/consumer'


def scrape_brands():
    yield COMPANY

    soup = BeautifulSoup(scraperwiki.scrape(URL))

    for a in soup.select('.item-list .views-field-title a'):
        yield list(a.stripped_strings)[0]
