import scraperwiki
from bs4 import BeautifulSoup

COMPANY = 'Hanesbrands Inc.'

CATEGORY = 'Apparel'

URL = 'http://www.hanes.com/corporate'

def scrape_company():
    yield 'company', {'company': COMPANY, 'category': CATEGORY}

    soup = BeautifulSoup(scraperwiki.scrape(URL))
    for i in soup.select('#CompanyTxt i'):
        for brand in i.text.split(', '):
            yield 'brand', {'company': COMPANY, 'brand': brand}
