# -*- coding: utf-8 -*-

#   Copyright 2014 SpendRight, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from srs.norm import smunch

from srs.scrape import scrape_soup


COMPANY = u'Reckitt-Benckiser'

COMPANY_URL = 'http://www.rb.com/'

BRANDS_URL = 'http://www.rb.com/our-brands'

CATEGORY_URL = 'http://www.rb.com/investors-media/category-performance'


MORE_BRANDS = [
    COMPANY,
    u'Reckitt',
    #u'Reckitt & Benckiser',  # appears on amazon, but not really legit
]

BRAND_CORRECTIONS = {
    "Cillet Bang": "Cillit Bang",
}

SMUNCHED_BRAND_CORRECTIONS = dict(
    (smunch(bad), smunch(good))
    for bad, good in BRAND_CORRECTIONS.iteritems())

# site has an entry for each product in this line; treat them
# as categories instead
KNOWN_BRANDS = [
    "French's",
]



def scrape_company():

    yield 'company', dict(company=COMPANY, url=COMPANY_URL)

    for brand in MORE_BRANDS:
        yield 'brand', dict(company=COMPANY, brand=brand)

    # get logo for brands
    brands_soup = scrape_soup(BRANDS_URL)

    sb_to_logo_url = {}  # map smunch(brand) to logo_url

    for img in brands_soup.select('#scroller img'):
        sb = smunch(img['alt'])
        sb = SMUNCHED_BRAND_CORRECTIONS.get(sb, sb)
        logo_url = img['src']

        sb_to_logo_url[sb] = logo_url

    cat_soup = scrape_soup(CATEGORY_URL)

    for a in cat_soup.select('li.active ul li a'):
        cat = a.text
        url = a['href']

        # TODO: match brands with logos
        # treat "French's" as single brand
        # correct "Cillet Bang" -> "Cillit Bang"

        soup = scrape_soup(url)
        for h2 in soup.select('h2'):
            brand = h2.text.strip()

            if brand:
                # special case for French's
                for kb in KNOWN_BRANDS:
                    if brand.startswith(kb + ' '):
                        sub_cat = brand[len(kb) + 1:]
                        yield 'category', dict(category=sub_cat,
                                               parent_category=cat)
                        brand = kb
                        cat = sub_cat
                        break

                # brand dict
                yield 'brand', dict(
                    company=COMPANY,
                    brand=brand,
                    category=cat,
                    logo_url = sb_to_logo_url.get(smunch(brand)))
