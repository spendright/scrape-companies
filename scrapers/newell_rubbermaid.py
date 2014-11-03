from urlparse import urljoin

from bs4 import BeautifulSoup

from srs.scrape import scrape


COMPANY = 'Newell Rubbermaid'
START_URL = 'http://www.newellrubbermaid.com/OurBrands/Pages/AllBrands.aspx'


def scrape_soup_from_bad_html(url):
    """Discard a bad comment that's frustrating BeautifulSoup"""
    return BeautifulSoup(scrape(url)[3:])


def scrape_brands():
    start_soup = scrape_soup_from_bad_html(START_URL)

    # if page structure changes, we'll get errors
    nav = start_soup.find('div', class_='switchNav1')

    for a in nav.select('a'):
        url = urljoin(START_URL, a['href'])
        if url == START_URL:
            continue

        category = a.text
        soup = scrape_soup_from_bad_html(url)

        for brand_a in soup.select('.switchNav1 ul li ul li a'):
            yield {'brand': brand_a.text, 'category': category}
