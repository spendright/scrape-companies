# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import scraperwiki


# TODO: Get around 403 Forbidden. Send more browser-like headers?
# TODO: scrape all countries, not just U.S.

COMPANY = 'Unilever'

# this page says Unilever has "more than 1000 brands" (!)
TOP_BRANDS_URL = 'http://www.unileverusa.com/brands-in-action/view-brands.aspx?view=AtoZ'

# Best Foods is an alternate name for Hellmann's (mayo)
# Marmite and PG Tips are UK brands available in the U.S.
EXTRA_BRANDS = ['Best Foods', 'Marmite', 'PG Tips']


def scrape_brands():
    yield COMPANY
    for brand in EXTRA_BRANDS:
        yield brand

    soup = BeautifulSoup(scraperwiki.scrape(TOP_BRANDS_URL))

    for span in soup.select('.zlist span.title'):
        yield span.text
