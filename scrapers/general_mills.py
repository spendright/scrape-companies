from urlparse import urljoin

from bs4 import BeautifulSoup
import scraperwiki


COMPANY = 'General Mills'

START_URL = 'http://www.generalmills.com/Brands.aspx'
SKIP_SECTIONS = ['Brands', 'General Mills Shop']


DESCRIPTION_TO_BRANDS = {
    'Latina': [
        'Latina Fresh',
    ],
    'Monsters': [
        'Count Chocula',
        'Franken Berry',
        'Boo Berry',
    ],
}

def scrape_brands():
    start_soup = BeautifulSoup(scraperwiki.scrape(START_URL))

    urls = [urljoin(START_URL, section_a['href'])
            for section_a in start_soup.select('#subnav a')
            if section_a.text.strip() not in SKIP_SECTIONS]

    for url in urls:
        soup = BeautifulSoup(scraperwiki.scrape(url))
        for a in soup.select('.productrow h4 a'):
            brand = a.text.strip()
            if '/' in brand:
                for part in brand.split('/'):
                    yield part.strip()
            elif brand in DESCRIPTION_TO_BRANDS:
                # "Monsters" is a family of brands
                for real_brand in DESCRIPTION_TO_BRANDS[brand]:
                    yield real_brand
            else:
                yield brand
