from bs4 import BeautifulSoup
import scraperwiki


COMPANY = u'PepsiCo'

URL = 'http://www.pepsico.com/Brands/BrandExplorer'

JOINT_VENTURES_TEXT = [
    ' joint'
]


def scrape_brands():
    yield COMPANY

    soup = BeautifulSoup(scraperwiki.scrape(URL))

    for div in soup.select('div.brand'):
        yield {
            'brand': div.img['alt'],
            # "joint venture" brands don't belong to PepsiCo (e.g. Starbucks)
            'is_licensed': any(
                jv_text in div.p.text for jv_text in JOINT_VENTURES_TEXT)
        }
