from bs4 import BeautifulSoup
import scraperwiki


COMPANY = u'PepsiCo'

ALL_BRANDS_URL = 'http://www.pepsico.com/Brands/BrandExplorer'

JOINT_VENTURES_TEXT = [
    ' joint'
]


def scrape_brands():
    yield COMPANY

    soup = BeautifulSoup(scraperwiki.scrape(ALL_BRANDS_URL))

    for div in soup.select('div.brand'):
        # exclude joint ventures (e.g. Starbucks)
        if any(jv_text in div.p.text for jv_text in JOINT_VENTURES_TEXT):
            continue

        yield div.img['alt']
