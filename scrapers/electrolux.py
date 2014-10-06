from srs.scrape import scrape_soup



COMPANY = 'Electrolux'  # full name is AB Electrolux, but "AB" is like "Inc."

URL = 'http://brandlicensing.electrolux.com/en/our-brands/all/'

# TODO: scrape all regions/countries
COUNTRY = 'USA'

def scrape_brands():
    soup = scrape_soup(URL)

    for div in soup.select('div.Brands-panel'):
        if div.h3.text == COUNTRY:
            for a in div.select('a.Brands-text'):
                yield a.text
