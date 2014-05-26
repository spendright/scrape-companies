from ..common import get_soup


COMPANY = 'ConAgra Foods'

_ALL_BRANDS_URL = 'http://www.conagrafoods.com/our-food/brands'


def scrape_brands():
    soup = get_soup(_ALL_BRANDS_URL)

    for div in soup.select('#listView div.brandInfo'):
        yield div.a['data-brandname']   # best-annotated brand list ever!
