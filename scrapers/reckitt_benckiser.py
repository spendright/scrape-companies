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


def scrape_company():

    yield 'company', dict(company=COMPANY, url=COMPANY_URL)

    for brand in MORE_BRANDS:
        yield 'brand', dict(company=COMPANY, brand=brand)

    brands_soup = scrape_soup(BRANDS_URL)

    for img in brands_soup.select('#scroller img'):
        yield 'brand', dict(company=COMPANY,
                            brand=img['alt'],
                            logo_url=img['src'])

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
                yield 'brand', dict(company=COMPANY,
                                    brand=h2.text,
                                    category=cat)
