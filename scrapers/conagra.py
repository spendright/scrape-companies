from srs.scrape import scrape_soup



COMPANY = 'ConAgra Foods'

URL = 'http://www.conagrafoods.com/our-food/brands'


def scrape_brands():
    soup = scrape_soup(URL)

    for div in soup.select('#listView div.brandInfo'):
        yield div.a['data-brandname']   # best-annotated brand list ever!
