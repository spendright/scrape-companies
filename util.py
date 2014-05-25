# -*- coding: utf-8 -*-
TM_SYMBOLS = u'®\u2120™'  # 2120 is SM symbol


def clean_string(s):
    """Convert to unicode, remove extra whitespace, and
    convert fancy apostrophes."""
    s = unicode(s)
    s = s.strip()
    s = s.replace(u'\u2019', "'")
    return s


def clean_brand(brand):
    """clean_string(), plus strip trailing ® or ™"""
    brand = clean_string(brand)
    for c in TM_SYMBOLS:
        if brand.endswith(c):
            brand = brand[:-1]
    return brand


def clean_dict(dict):
    """Clean all string values in a dict."""
    result = {}

    for k, v in dict.iteritems():
        if k == 'brand':
            result[k] = clean_brand(v)
        elif isinstance(v, basestring):
            result[k] = clean_string(v)
        else:
            result[k] = v

    return result


def wrap_scraper(items):
    """Use this to wrap a scraper. This allows you to write a scraper that
    just emits strings (brand names) or dictionaries with at least the key
    "brand", cleans them up for you, and compiles them into a map from
    brand name to a dict containing other entries to insert into the
    table.
    """
    results = {}

    for item in items:
        if not item:
            continue
        if isinstance(item, dict):

            brand = item.pop('brand')  # modifies dict. that's okay
            brand = clean_brand(brand)
            results[brand] = item
        else:
            brand = clean_brand(item)
            if brand:
                results[brand] = {}

    return results
