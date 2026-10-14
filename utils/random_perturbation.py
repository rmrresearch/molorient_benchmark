import random
from decimal import Decimal

from utils.helpers import pi_as_decimal, sin_series, cos_series


def random_translation(coords, max_distance=Decimal(100)):
    """
    Translates every [x, y, z] in coords by the same random vector: a random
    unit direction scaled by a random distance in [0, max_distance] Angstroms.
    Returns (new_coords, translation).
    """
    direction = [Decimal(random.gauss(0, 1)) for _ in range(3)]
    norm = sum(d * d for d in direction).sqrt()
    distance = Decimal(random.random()) * max_distance
    translation = [d / norm * distance for d in direction]
    new_coords = [[c[i] + translation[i] for i in range(3)] for c in coords]
    return new_coords, translation


def random_rotation(coords):
    """
    Rotates every [x, y, z] in coords about the origin by random Tait-Bryan
    angles: yaw (z) and roll (x) in [-pi, pi], pitch (y) in [-pi/2, pi/2],
    with R = Rz(yaw) Ry(pitch) Rx(roll). Returns (new_coords, [yaw, pitch, roll]).
    """
    pi = pi_as_decimal()
    yaw = (2 * Decimal(random.random()) - 1) * pi
    pitch = (Decimal(random.random()) - Decimal("0.5")) * pi
    roll = (2 * Decimal(random.random()) - 1) * pi
    cy, sy = cos_series(yaw), sin_series(yaw)
    cp, sp = cos_series(pitch), sin_series(pitch)
    cr, sr = cos_series(roll), sin_series(roll)
    R = [
        [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
        [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
        [-sp, cp * sr, cp * cr],
    ]
    new_coords = [[sum(R[i][j] * c[j] for j in range(3)) for i in range(3)] for c in coords]
    return new_coords, [yaw, pitch, roll]
