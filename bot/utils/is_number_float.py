def is_number_float(el):
    """ Returns True if string is a number. """
    try:
        if "," in el:
            el = el.replace(",", ".")
        float(el)
        return float(el)
    except ValueError:
        return False
