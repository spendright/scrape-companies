from ..common import get_soup


COMPANY = u'PepsiCo'

_ALL_BRANDS_URL = 'http://www.pepsico.com/Brands/BrandExplorer'

_JOINT_VENTURES_TEXT = [
    ' joint'
]


def scrape_brands():
    yield COMPANY

    soup = get_soup(_ALL_BRANDS_URL)

    for div in soup.select('div.brand'):
        # exclude joint ventures (e.g. Starbucks)
        if any(jv_text in div.p.text for jv_text in _JOINT_VENTURES_TEXT):
            continue

        yield div.img['alt']
