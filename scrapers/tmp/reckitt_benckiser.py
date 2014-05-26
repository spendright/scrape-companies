from ..common import get_soup


COMPANY = u'Reckitt-Benckiser'


_START_URL = 'http://www.rb.com/ourbrands/search-rb-brands-a-z/a-f'

_MORE_BRANDS = [
    COMPANY,
    u'Reckitt',
    #u'Reckitt & Benckiser',  # appears on amazon, but not really legit
]


def scrape_brands():

    for brand in _MORE_BRANDS:
        yield brand

    start_soup = get_soup(
        'http://www.rb.com/ourbrands/search-rb-brands-a-z/a-f')

    urls = [a['href'] for a in start_soup.select('li.active_ancestor_2 li a')]

    for url in urls:
        if url == _START_URL:
            soup = start_soup
        else:
            soup = get_soup(url)

        for fp in soup.select('div.featuredproduct'):
            h2 = fp.h2
            if h2 and h2.text:
                # TODO: for now, just getting US brands
                if 'USA' in fp.text:
                    brand = h2.text.strip()
                    if '/' in brand:  # Lysol/Lizol
                        # TODO: This doesn't handle Glen 10/20 (AU) right
                        # (should be "Glen 10", "Glen 20")
                        for part in brand.split('/'):
                                yield part
                    else:
                        yield brand
