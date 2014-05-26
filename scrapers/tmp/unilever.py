# -*- coding: utf-8 -*-
from ..common import get_soup


COMPANY = 'Unilever'

# this page says Unilever has "more than 1000 brands" (!)
TOP_BRANDS_URL = 'http://www.unileverusa.com/brands-in-action/view-brands.aspx?view=AtoZ'

# Best Foods is an alternate name for Hellmann's (mayo)
# Marmite and PG Tips are UK brands available in the US
EXTRA_BRANDS = ['Best Foods', 'Marmite', 'PG Tips']

R_AND_TM = u'®™'


def scrape_brands():
    yield COMPANY
    for brand in EXTRA_BRANDS:
        yield brand

    soup = get_soup(TOP_BRANDS_URL)

    for span in soup.select('.zlist span.title'):
        brand = span.text

        for c in R_AND_TM:
            if c in brand:
                # cut off everything after the ®/™
                # e.g. Consort® For Men becomes simply "Consort"
                brand = brand[:brand.index(c)]

        yield brand
