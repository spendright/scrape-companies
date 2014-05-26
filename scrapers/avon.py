from bs4 import BeautifulSoup
import scraperwiki

COMPANY = 'Avon'

# going to scrape brands off their online store
START_URL = 'http://shop.avon.com/product_list.aspx'

# You'd think more of these would need to have "Avon" prepended, but
# "Naturals" (not "Avon Naturals") is actually a brand you can
# filter on on Amazon!

# skip the hair care category; these are all just types of
# Avon Advance Techniques
SKIP_CATEGORIES = ['hair care']
MORE_BRANDS = ['Advance Techniques']


def scrape_brands():
    yield COMPANY
    for brand in MORE_BRANDS:
        yield brand

    start_soup = BeautifulSoup(scraperwiki.scrape(START_URL))

    urls = [a['href'] for a in start_soup.select('div.topmenu a')
            if a['title'].lower() not in SKIP_CATEGORIES]

    for url in urls:
        soup = BeautifulSoup(scraperwiki.scrape(url))

        for a in soup.select('div#shopByBrand a'):
            yield a.text
