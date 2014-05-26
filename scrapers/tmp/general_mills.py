from urlparse import urljoin

from ..common import get_soup


NAME = 'General Mills'

_START_URL = 'http://www.generalmills.com/Brands.aspx'
_SKIP_SECTIONS = ['Brands', 'General Mills Shop']


_DESCRIPTION_TO_BRANDS = {
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
    start_soup = get_soup(_START_URL)

    urls = [urljoin(_START_URL, section_a['href'])
            for section_a in start_soup.select('#subnav a')
            if section_a.text.strip() not in _SKIP_SECTIONS]

    for url in urls:
        soup = get_soup(url)
        for a in soup.select('.productrow h4 a'):
            brand = a.text.strip()
            if '/' in brand:
                for part in brand.split('/'):
                    yield part.strip()
            elif brand in _DESCRIPTION_TO_BRANDS:
                # "Monsters" is a family of brands
                for real_brand in _DESCRIPTION_TO_BRANDS[brand]:
                    yield real_brand
            else:
                yield brand
