from urllib2 import urlopen
import json

from bs4 import BeautifulSoup

COMPANY = 'Coca-Cola Company'

# Coca-Cola brands are a major source of false positives and not that
# important to searching on Amazon, so sticking to US brands for now.
#
# TODO: query each country and keep track of which countries brands are in.
#
# This returns JSON for an AJAX script.
# The corresponding page is http://www.coca-colacompany.com/brands/all/
US_BRANDS_URL = 'http://www.coca-colacompany.com/api/getAllBrands?country=united-states'


def scrape_brands():

    brand_json = json.load(urlopen(US_BRANDS_URL))

    for brand in brand_json['brands']:
        name_html = brand['name']['desktop']
        name = BeautifulSoup(name_html).text.strip()  # resolve HTML entities
        if name.endswith('*'):
            yield dict(brand=name[:-1], is_licensed=True)
        else:
            yield name
