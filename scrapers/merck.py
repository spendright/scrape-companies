from srs.scrape import scrape_soup

COMPANY = 'Merck & Co.'

URL = 'https://www.merck.com/product/home.html'

MORE_BRANDS = [u'Merck', u'Schering-Plough']

# From https://www.merck.com/product/consumer-products/home.html
# TODO: scrape this page and match against the image names
# (e.g. consumer_drscholls.jpg)
OTC_BRANDS = ['claritin', 'coppertone', "dr. scholl's", 'miralax', 'oxytrol']


def scrape_brands():

    for brand in MORE_BRANDS:
        yield brand

    soup = scrape_soup(URL)

    for h5 in soup.select('ul.alphabetic-content h5'):
        if h5.sup:
            # yield the part before the (R)/TM
            brand = h5.sup.previous_element

            if brand.strip().lower() in OTC_BRANDS:
                yield brand
            else:
                yield dict(brand=brand, is_prescription=True)
