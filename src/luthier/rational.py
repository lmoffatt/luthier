"""The Python behind lib/rational.lut: the rationals as fractions.Fraction, the rounding of a fraction
to the nearest double, and a generator of normal doubles over the whole range of exponents, so the
rounding law of the doubles is tested at every scale and not in a box around zero."""
from __future__ import annotations

import math
import random
from fractions import Fraction


def ratio(a: int, b: int) -> Fraction:
    """a / b exactly."""
    return Fraction(a, b)


def nearest(q: Fraction) -> float:
    """The double nearest to q (ties to even), as Python's float() of a Fraction computes it: the
    rounding of the exact quotient of its numerator and denominator."""
    return float(q)


# Doubles with exponents in [-EXP, EXP), so magnitudes between 1e-150 and 1e150, the bounds of
# NormalDouble in rational.lut: a product or a quotient of two stays normal and finite (|e| < 1022), and
# a sum of a few has no subnormal result, so the relative rounding law holds for every operation of two.
EXP = 498


def gen_normal_double(rng: random.Random, size: int) -> float:
    """A normal double, sign and exponent uniform, mantissa uniform in [1, 2); zero now and then."""
    if rng.random() < 0.02:
        return 0.0
    m = 1.0 + rng.random()
    e = rng.randint(-EXP, EXP - 1)
    return math.copysign(math.ldexp(m, e), rng.choice((-1.0, 1.0)))
