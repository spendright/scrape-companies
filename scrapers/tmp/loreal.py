from ..common import get_soup

NAME = "L'Oreal"

_ALL_BRANDS_URL = 'http://www.lorealusa.com/brands/consumer-products-division/softsheen-carson.aspx'


# fragances, mostly
_LICENSED_BRANDS = [
    'Cacharel',
    'Diesel',
    'Giorgio Armani',
    'Maison Martin Margiela',
    'Ralph Lauren',
    'Viktor&Rolf',
]


def scrape_brands():
    yield NAME

    soup = get_soup(_ALL_BRANDS_URL)

    # this gets the same brands several times, but that's okay
    for strong in soup.select('.slides strong'):
        brand = strong.text.strip()
        if brand.endswith(';'):
            brand = brand[:-1]

        if brand not in _LICENSED_BRANDS:
            yield brand
