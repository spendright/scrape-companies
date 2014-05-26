from ..common import get_soup


COMPANY = 'AB Electrolux'

_ALL_BRANDS_URL = 'http://brandlicensing.electrolux.com/node658.aspx?id=53'
_NON_BRANDS = ['Close Window']


def scrape_brands():
    soup = get_soup(_ALL_BRANDS_URL)

    brands = set()

    for img in soup.select('.area-wide img'):
        brand = img['alt']
        if brand not in _NON_BRANDS:
            brands.add(brand)

    return sorted(brands)
