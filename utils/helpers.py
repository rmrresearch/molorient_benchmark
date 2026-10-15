from decimal import Decimal, getcontext


def pi_as_decimal():
    """Pi to the current Decimal precision (from molorient's trig_helpers)."""
    getcontext().prec += 2
    lasts, t, s, n, na, d, da = 0, Decimal(3), 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s
        n, na = n + na, na + 8
        d, da = d + da, da + 32
        t = (t * n) / d
        s += t
    getcontext().prec -= 2
    return +s


def sin_series(x):
    """Maclaurin series of sin."""
    getcontext().prec += 2
    i, lasts, s, fact, num, sign = 1, 0, x, 1, x, 1
    while s != lasts:
        lasts = s
        i += 2
        fact *= i * (i - 1)
        num *= x * x
        sign *= -1
        s += num / fact * sign
    getcontext().prec -= 2
    return +s


def cos_series(x):
    """Maclaurin series of cos."""
    getcontext().prec += 2
    i, lasts, s, fact, num, sign = 0, 0, Decimal(1), 1, Decimal(1), 1
    while s != lasts:
        lasts = s
        i += 2
        fact *= i * (i - 1)
        num *= x * x
        sign *= -1
        s += num / fact * sign
    getcontext().prec -= 2
    return +s


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
