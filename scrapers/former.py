"""Mark companies' former brands as is_former, so we don't try to match them.

If a company has its own scraper, put this information there.
"""
COMPANY_TO_FORMER_BRANDS = {
    'Groupe Danone': {
        'LU',
    },
    'LG': {
        'GoldStar',
    },
    'Mattel': {
        'SoftKey',
    }
}


def scrape_company():
    for company, former_brands in COMPANY_TO_FORMER_BRANDS.iteritems():
        for fb in former_brands:
            yield 'brand', {'company': company,
                            'brand': fb,
                            'is_former': True}
