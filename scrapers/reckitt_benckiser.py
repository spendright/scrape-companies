from urlparse import urljoin

from srs.scrape import scrape_soup



COMPANY = u'Reckitt-Benckiser'


# TODO: this no longer exists. Use #scroller from
BRANDS_URL = 'http://www.rb.com/our-brands'

MORE_BRANDS = [
    COMPANY,
    u'Reckitt',
    #u'Reckitt & Benckiser',  # appears on amazon, but not really legit
]


def scrape_brands():

    for brand in MORE_BRANDS:
        yield brand

    brands_soup = scrape_soup(BRANDS_URL)

    for img in brands_soup.select('#scroller img'):
        yield dict(brand=img['alt'],
                   logo_url=urljoin(BRANDS_URL, img['src']))

        # TODO: use http://www.rb.com/media-investors/category-performance
        # to get brand categories
