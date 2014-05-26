from ..common import get_soup

COMPANY = "L'Oreal"

ALL_BRANDS_URL = 'http://www.lorealusa.com/brands/consumer-products-division/softsheen-carson.aspx'


# fragances, mostly
LICENSED_BRANDS = [
    'Cacharel',
    'Diesel',
    'Giorgio Armani',
    'Maison Martin Margiela',
    'Ralph Lauren',
    'Viktor&Rolf',
]


def scrape_brands():
    yield COMPANY

    soup = get_soup(ALL_BRANDS_URL)

    # this gets the same brands several times, but that's okay
    for strong in soup.select('.slides strong'):
        brand = strong.text.strip()
        if brand.endswith(';'):
            brand = brand[:-1]

        if brand not in LICENSED_BRANDS:
            yield brand
