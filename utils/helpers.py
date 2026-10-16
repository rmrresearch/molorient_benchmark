from decimal import Decimal, getcontext


def round_coord(coord):
    """
    Rounds a coordinate to the current Decimal precision (from molorient's sort_atoms).
    If it has more decimal places than significant digits, quantize to 10**-prec decimal
    places; otherwise keep prec + 2 significant figures.
    """
    t = coord.as_tuple()
    if len(t.digits) < max(0, -t.exponent):
        return coord.quantize(Decimal(10) ** -getcontext().prec)
    getcontext().prec += 2
    rounded = round(coord, getcontext().prec - coord.adjusted() - 1)
    getcontext().prec -= 2
    return Decimal(str(rounded))
