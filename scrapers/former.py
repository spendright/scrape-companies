"""Mark companies' former brands as is_former, so we don't try to match them.

If a company has its own scraper, put this information there.
"""
FORMER_BRANDS = [
    ('Groupe Danone', 'LU'),  # sold
    ('LG', 'GoldStar'),  # discontinued
    ('Mattel', 'SoftKey'),  # sold
    ('Microsoft', 'GIANT'),  # stopped selling in 2006
    ('VF', 'John Varvatos'),  # sold to Lion Capital in 2012
]


def scrape_company():
    for company, brand in FORMER_BRANDS:
        yield 'brand', {'company': company,
                        'brand': brand,
                        'is_former': True}
