from ..common import get_soup


NAME = u'Johnson & Johnson'

_ALL_BRANDS_URL = 'http://www.jnj.com/healthcare-products/consumer'


def scrape_brands():
    yield NAME

    soup = get_soup(_ALL_BRANDS_URL)

    for a in soup.select('.item-list .views-field-title a'):
        yield list(a.stripped_strings)[0]