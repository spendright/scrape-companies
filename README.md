# -*- coding: utf-8 -*-
========================
SpendRight brand scraper
========================

The goal of this project is to generate complete, correct lists of brands
owned by major companies mentioned in buyer's guides (e.g.
http://www.hrc.org/apps/buyersguide/index.php). These can be used to power
brand screens, browser extensions, barcode-scanning apps, etc.

The scraper is meant to run in morph.io, a service which auto-runs scrapers.
You can see the scraper running and download its output (a SQLite database) at
https://morph.io/spendright-scrapers/brands. More info about the schema
below. The entry point is `scraper.py`

The simplest way to write a scraper is to add a module to scrapers/ which
defines COMPANY (the company name) and scrape(), a function which yields
brand names. `scraper.py` automatically strips whitespace and (tm), etc.
and performs de-duplication. As an example, here is the scraper for
Kraft Foods in its entirety (`scrapers/kraft.py`)

```python
from bs4 import BeautifulSoup
import scraperwiki


COMPANY = 'Kraft Foods'
URL = 'http://www.kraftfoodsgroup.com/brands/index.aspx'
EXTRA_BRANDS = ['Kraft']


def scrape():
    for b in EXTRA_BRANDS:
        yield b

    soup = BeautifulSoup(scraperwiki.scrape(URL))

    for h1 in soup.select('.brand h1'):
        yield h1.text
```

To test a particular scraper rather than running all of them, just specify
its module name on the command line: `python scraper.py kraft`.

The main use case for this is to match consumer products, so it's helpful
to know if a brand applies to a service, prescription only, or only marketed
to other businesses. It's also helpful to have category information (to
distinguish it from brands with the same name owned by other companies).

To include additional information about a brand, yield a dict with the
`brand` field set to the brand name, and additional fields. For example,
here's a snippet from `scraper/astrazeneca.py` that tags prescription brands

```python
if brand.strip().lower() in OTC_BRANDS:
    yield brand
else:
    yield dict(brand=brand, is_prescription=True)
```

Currently the scraper only outputs a single table, `brand`. You can add
any fields you like, but these are the ones we're aiming for:

 * `company`: name of the company, minus ", Inc." etc.
 * `brand`: brand name, minus "TM", etc.
 * `is_service`: set to 1 if a service, not a product (e.g. Airlines)
 * `is_prescription`: set to 1 if prescription-only
 * `is_b2b`: set to 1 if primarly marketed to other businesses (e.g. pesticide)
 * `category`: Free-form category description (e.g. `Steak Sauce`). For now, if
               you need to include multiple categories, just comma-separate
               them (we can eventually create a brand_category table)
 * `countries`: Countries where the brand is marketed. Use
              ISO 3166-1 country codes, separated by commas (e.g. `US,CA,GB`).
              You can also use `!` to specify that a product is marketed in a
              particular country, e.g. `!US`. (Will probably add utilities
              that can convert country names to country codes for you.)
