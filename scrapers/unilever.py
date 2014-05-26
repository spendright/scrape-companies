# -*- coding: utf-8 -*-
from urllib2 import Request
from urllib2 import urlopen

from bs4 import BeautifulSoup

from scraper import TM_SYMBOLS


# TODO: scrape all countries, not just U.S.

COMPANY = 'Unilever'

# this page says Unilever has "more than 1000 brands" (!)
URL = 'http://www.unileverusa.com/brands-in-action/view-brands.aspx?view=AtoZ'

# 403s without Accept and User-Agent header
HTTP_HEADERS = {
    'Accept': 'text/html',
    'User-Agent': 'Mozilla/5.0',
}


# Best Foods is an alternate name for Hellmann's (mayo)
# Marmite and PG Tips are UK brands available in the U.S.
EXTRA_BRANDS = ['Best Foods', 'Marmite', 'PG Tips']


def scrape_brands():
    yield COMPANY
    for brand in EXTRA_BRANDS:
        yield brand

    html = urlopen(Request(URL, headers=HTTP_HEADERS)).read()
    soup = BeautifulSoup(html)

    for span in soup.select('.zlist span.title'):
        yield span.text
