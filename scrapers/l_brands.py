
from srs.scrape import scrape_soup

from srs.norm import clean_string

COMPANY = 'L Brands'

URL = 'http://www.lb.com/our_brands/BrandOverview.aspx'

# Licensed and former brands, from
# http://en.wikipedia.org/wiki/L_Brands
LICENSED_BRANDS = {
    'C. O. Bigelow',
    'The White Barn Candle Company',
}

FORMER_BRANDS = {
    'Lane Bryant',  # sold in 2002 to Charming Shoppes.
    'Abercrombie & Fitch',  # acquired by The Limited in 1988
    'Lerner New York',  # sold and became New York and Company.
    'The Limited Too',  # Tween Brands, Inc., spun off in 1999.
    "Galyan's",  # old in 2004, merged with Dick's Sporting Goods
    'Structure',  # converted to Express Men, brand name later sold to Sears.
    'Aura Science',  # merged with Victoria's Secret Beauty.
    'Express',  # 2007, sold a 75% stake to Golden Gate Capital Partners.
    'The Limited',  # In 2010, sold to Sun Capital Partners.
}

CATEGORY_SELECTORS = [
    '#nav-primary ul.menu.primary > li > a',  # Victoria's Secret
    '#nav-primary ul.menu.primary > li > span > a',  # PINK
    'a.nav1-link',  # Bath & Body Works
    '.categorymenu > ul > li > a',  # Henri Bendel
    '.tab-title',  # La Senza
]

BAD_CATEGORY_WORDS = {
    'blog',
    'gifts',
    'new',
    'online',
    'pink',
    'sale',
    'shops',
    'special',
    'specials',
    'vs',
}

CATEGORY_CORRECTIONS = {
    'college & pro': 'College & Pro Apparel',
    'fragrances a-z': 'Fragrances',
    'sleep': 'Sleep Apparel',
    'sport': 'Sport Apparel',
    'swim': 'Swim Apparel',
    'travel': 'Luggage',
}


def scrape_brands():
    for lb in LICENSED_BRANDS:
        yield {'brand': lb, 'is_licensed': True}

    for fb in FORMER_BRANDS:
        yield {'brand': fb, 'is_former': True}

    soup = scrape_soup(URL)

    for a in soup.select('#contentTwo a'):
        yield {'brand': a.text,
               'url': a['href'],
               'categories': list(scrape_categories(a['href']))}



def scrape_categories(url):
    """Actually go to the home page for the brand and scrape top nav."""
    soup = scrape_soup(url)

    for selector in CATEGORY_SELECTORS:
        elts = soup.select(selector)
        if elts:
            for elt in elts:
                category = clean_string(elt.text)
                words = set(w.lower() for w in category.split())
                if words & BAD_CATEGORY_WORDS:
                    continue

                yield CATEGORY_CORRECTIONS.get(category.lower(), category)
            return
    else:
        raise ValueError("Couldn't find top nav on {}".format(url))
