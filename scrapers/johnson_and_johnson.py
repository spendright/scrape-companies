from bs4 import BeautifulSoup
import scraperwiki


COMPANY = u'Johnson & Johnson'

URL = 'http://www.jnj.com/healthcare-products/consumer'

# TODO: could easily get prescription products here:
# http://www.jnj.com/healthcare-products/prescription

# TODO: could get subsidiaries (from tooltips links) here:
# http://www.jnj.com/healthcare-products/medical-technologies


def scrape_brands():
    yield COMPANY

    soup = BeautifulSoup(scraperwiki.scrape(URL))

    for div in soup.select('div.gray-container'):
        category = div.h2.text

        for a in div.select('.views-field-title a'):
            yield {'brand': a.text, 'category': category}
