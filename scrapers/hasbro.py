from srs.scrape import scrape_soup



COMPANY = u'Hasbro'

URL = 'http://www.hasbro.com/shop/brandlist.cfm'


# these are licensed by multiple companies
LICENSED_BRANDS = [
    'Angry Birds',
    'Captain America',
    'Disney',
    'Disney Princesses',
    'Elmo',
    'Incredible Hulk',
    'Iron Man',
    'Marvel',
    'Marvel Universe',
    'Sesame Street',
    'Star Trek',
    'Star Wars',  # Star Wars Jedi Force seems to be exclusively Hasbro
    'The Avengers',
    'Thor',
    'Wolverine',
    'Zynga',
]


def scrape_brands():
    yield COMPANY

    soup = scrape_soup(URL)

    for a in soup.select('#hsb_shop_bl_container li ul li a'):
        brand = a.text
        if brand in LICENSED_BRANDS:
            yield dict(brand=brand, is_licensed=True)
        else:
            yield brand
