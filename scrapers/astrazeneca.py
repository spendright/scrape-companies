import re

from bs4 import BeautifulSoup
import scraperwiki


COMPANY = u'AstraZeneca'

URL = 'http://www.astrazeneca.com/Medicines/Products-A-Z'

SEPARATOR_RE = re.compile('[,/]')

# almost all AstraZeneca stuff requires a prescription.
#
# Nexium is approved for OTC, but will be sold by Pfizer. See:
# http://www.fiercepharma.com/story/pfizer-gets-fda-green-light-nexium-otc-launch-az-braces-competition/2014-03-31
OTC_BRANDS = ['emla']  # Lidocaine Cream


def scrape():
    soup = BeautifulSoup(scraperwiki.scrape(URL))

    yield COMPANY

    for tr in soup.select('#primary table tbody tr'):
        td = tr.td  # pick first td
        if td:
            td_brands = SEPARATOR_RE.split(td.text)
            for brand in td_brands:
                if ' (' in brand:
                    brand = brand[:brand.index(' (')]

                if brand.strip().lower() in OTC_BRANDS:
                    yield brand
                else:
                    yield dict(brand=brand, is_prescription=True)
