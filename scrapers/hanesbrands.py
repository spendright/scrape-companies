
from srs.scrape import scrape_soup

COMPANY = 'Hanesbrands Inc.'

CATEGORY = 'Apparel'

URL = 'http://www.hanes.com/corporate'

def scrape_company():
    yield 'company', {'company': COMPANY, 'category': CATEGORY}

    soup = scrape_soup(URL)
    for i in soup.select('#CompanyTxt i'):
        for brand in i.text.split(', '):
            yield 'brand', {'company': COMPANY, 'brand': brand}
