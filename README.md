<!-- -*- coding: utf-8 -*- -->
============================
SpendRight companies scraper
============================

The goal of this project is to generate information about companies mentioned
in buyer's guides (e.g. http://www.hrc.org/apps/buyersguide/index.php),
including complete, correct lists of brands. These can be used to power
brand screens, browser extensions, barcode-scanning apps, etc.

This is a project of [SpendRight](http://spendright.org). You can contact
the author (David Marin) at dave@spendright.org.

Using the Data
--------------

You are welcome to use this data as-is. It's meant to contain only factual
data, so there shouldn't be an issue of copyright (e.g. the list of brands
belonging to a company isn't copyrightable).

You might find it more useful to use data from
[here](https://morph.io/spendright-scrapers/everything), which also includes
ratings and other data from several consumer campaigns.

Writing a Scraper
-----------------

The simplest way to write a scraper is to add a module to scrapers/ which
defines `COMPANY` (the company name) and `scrape_brands()`, a function which
yields brand names. `scraper.py` automatically strips whitespace and (tm), etc.
and performs de-duplication. As an example, here is the scraper for
Kraft Foods in its entirety (`scrapers/kraft.py`):


    from bs4 import BeautifulSoup
    import scraperwiki


    COMPANY = 'Kraft Foods'
    URL = 'http://www.kraftfoodsgroup.com/brands/index.aspx'
    EXTRA_BRANDS = ['Kraft']


    def scrape_brands():
        for b in EXTRA_BRANDS:
            yield b

        soup = BeautifulSoup(scraperwiki.scrape(URL))

        for h1 in soup.select('.brand h1'):
            yield h1.text

You don't need to worry about stripping strings; the scraper harness is
smart enough to do that. In addition, it knows that brand names stop at
a ™/®; a string like `" Consort® for Men "` would be auto-converted to
`"Consort"`, with the `®` stored in a separate `tm` field.

To test a particular scraper rather than running all of them, just specify
its module name on the command line: `python scraper.py kraft`.

To include additional information about a brand, yield a dict with the
`brand` field set to the brand name, and additional fields. For example,
here's a snippet from `scraper/astrazeneca.py` that tags prescription brands:

    if brand.strip().lower() in OTC_BRANDS:
        yield brand
    else:
        yield dict(brand=brand, is_prescription=True)

You can also assign one or more free-form categories to a brand by setting
the 'categories' field to a list of strings.

If you wish to scrape information about the company as well (e.g.
`twitter_handle`), you may instead define a function `scrape_companies()`
and which yields tuples of (table_name, row); use a table_name of `company`
for the company, and `brand` for brands.

The names and fields of `brand`, `company` and other tables are described in this [README](https://github.com/spendright-scrapers/everything/blob/master/README.md).

