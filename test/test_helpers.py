import numpy as np
import pytest
from decimal import Decimal, getcontext

from utils.helpers import pi_as_decimal, sin_series, cos_series, round_coord


@pytest.fixture(autouse=True)
def decimal_precision():
    """Every test in this file runs at molorient's default precision of 6; restore whatever came before."""
    orig_prec = getcontext().prec
    getcontext().prec = 6
    yield
    getcontext().prec = orig_prec


tol = Decimal('1e-5')


def test_pi_as_decimal():
    assert abs(pi_as_decimal() - Decimal(np.pi)) < tol


def test_sin():
    assert abs(sin_series(Decimal('0'))) < tol
    assert abs(sin_series(pi_as_decimal() / 2) - Decimal('1')) < tol
    assert abs(sin_series(pi_as_decimal())) < tol


def test_cos():
    assert abs(cos_series(Decimal('0')) - Decimal('1')) < tol
    assert abs(cos_series(pi_as_decimal() / 2)) < tol
    assert abs(cos_series(pi_as_decimal()) + Decimal('1')) < tol


def test_sin_cos_identity():
    for angle in ['-3', '0.7', '2.5']:
        x = Decimal(angle)
        assert abs(sin_series(x) ** 2 + cos_series(x) ** 2 - Decimal('1')) < tol


def test_round_coord_large_keeps_extra_sig_figs():
    assert round_coord(Decimal('123.456789123')) == Decimal('123.45679')


def test_round_coord_small_quantizes_to_precision():
    assert round_coord(Decimal('0.000123456789')) == Decimal('0.000123')


def test_round_coord_in_between():
    assert round_coord(Decimal('1.23456789123')) == Decimal('1.2345679')
