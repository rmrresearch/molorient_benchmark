import random
import pytest
from decimal import Decimal, getcontext
from molorient.helpers.trig_helpers import pi_as_decimal
from utils.random_perturbation import random_translation, random_rotation


@pytest.fixture(autouse=True)
def decimal_precision():
    """Every test in this file runs at molorient's default precision of 6; restore whatever came before."""
    orig_prec = getcontext().prec
    getcontext().prec = 6
    yield
    getcontext().prec = orig_prec


@pytest.fixture
def coords():
    return [
        [Decimal('0.0000'), Decimal('0.0000'), Decimal('0.1173')],
        [Decimal('0.0000'), Decimal('0.7572'), Decimal('-0.4692')],
        [Decimal('0.0000'), Decimal('-0.7572'), Decimal('-0.4692')],
    ]


def distances(coords):
    return [
        sum((coords[i][k] - coords[j][k]) ** 2 for k in range(3)).sqrt()
        for i in range(len(coords))
        for j in range(i)
    ]


def test_translation_known_vector(coords, monkeypatch):
    gauss_values = iter([1, 0, 0])
    monkeypatch.setattr(random, "gauss", lambda mu, sigma: next(gauss_values))
    monkeypatch.setattr(random, "random", lambda: 0.5)

    new_coords, translation = random_translation(coords)

    assert translation == [Decimal('50'), Decimal('0'), Decimal('0')]
    for new, old in zip(new_coords, coords):
        assert abs(new[0] - old[0] - Decimal('50')) < Decimal('1e-2')
        assert new[1] == old[1]
        assert new[2] == old[2]


def test_translation_zero_distance(coords):
    new_coords, translation = random_translation(coords, max_distance=Decimal('0'))

    assert new_coords == coords
    assert translation == [Decimal('0')] * 3


def test_rotation_identity(coords, monkeypatch):
    monkeypatch.setattr(random, "random", lambda: 0.5)

    new_coords, angles = random_rotation(coords)

    assert angles == [Decimal('0')] * 3
    for new, old in zip(new_coords, coords):
        for k in range(3):
            assert abs(new[k] - old[k]) < Decimal('1e-5')


def test_rotation_quarter_turn_yaw(monkeypatch):
    draws = iter([0.75, 0.5, 0.5])
    monkeypatch.setattr(random, "random", lambda: next(draws))

    new_coords, angles = random_rotation([[Decimal('1'), Decimal('0'), Decimal('0')]])

    assert abs(angles[0] - pi_as_decimal() / 2) < Decimal('1e-5')
    expected = [Decimal('0'), Decimal('1'), Decimal('0')]
    for k in range(3):
        assert abs(new_coords[0][k] - expected[k]) < Decimal('1e-5')


def test_random_translation(coords):
    random.seed(0)
    for _ in range(10):
        new_coords, translation = random_translation(coords)

        assert sum(t * t for t in translation).sqrt() <= Decimal('100.001')
        for new, old in zip(new_coords, coords):
            for k in range(3):
                assert abs(new[k] - old[k] - translation[k]) < Decimal('1e-2')


def test_random_rotation(coords):
    random.seed(0)
    half_pi = pi_as_decimal() / 2
    for _ in range(10):
        new_coords, (yaw, pitch, roll) = random_rotation(coords)

        assert abs(yaw) <= 2 * half_pi and abs(roll) <= 2 * half_pi
        assert abs(pitch) <= half_pi
        for before, after in zip(distances(coords), distances(new_coords)):
            assert abs(before - after) < Decimal('1e-4')

        origin_after, _ = random_rotation([[Decimal('0')] * 3])
        assert origin_after == [[Decimal('0')] * 3]
