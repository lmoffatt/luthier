"""Host generators of spec 7.S1: a size and a seed give a value and the next seed.

Sources: spec 7.S1 (`Gen T = Nat -> Seed -> T * Seed`), 7.S5 (the families of matrices: symmetric,
orthogonal by the QR of a Gaussian with the signs of the diagonal of R, Mezzadri 2007), 7.S4 (the
log metric, the atom at 0), 7.S17 (a calibrated sample); arrays.py's `gen_symmetric` and `_mat`,
kept from v0.1. Derivation: record/IA/tester-2026-10-14/prompt-3.md, by a Claude agent of the
coordinating session, 2026-10-15. Each function is the route of a value of generators_model.lut.

How the seed crosses (7.S1): the seed is an `Int` in [0, 2^31) and crosses as a Python int; the
generator seeds a `random.Random` with it, draws everything from that one source, and gives back,
with the value, the next seed, drawn from the same source last. So the value and the next seed are
functions of the size and the seed alone, and a test that threads the seed through its draws is
deterministic given its first seed. The criteria of a family (the probability of an atom, the
bounds of a magnitude) are arguments, never constants here (P11); generators_model.lut sets them.
"""
import math
import random

import numpy as np

from . import arrays

SEEDS = 2 ** 31


def _source(seed):
    return random.Random(int(seed))


def _next(rng):
    return rng.randrange(SEEDS)


def _length(rng, size, low=0):
    return rng.randint(low, max(low, int(size)))


def symmetric(size, seed):
    """v0.1's `gen_symmetric`: B + B^T, B of a size between 1 and the size, entries uniform in
    [-size, size]; symmetric exactly, any spectrum."""
    rng = _source(seed)
    a = arrays.gen_symmetric(rng, int(size))
    return a, _next(rng)


def symmetric_of(k, size, seed):
    """B + B^T of k rows, entries uniform in [-size, size]."""
    rng = _source(seed)
    b = arrays._mat(rng, int(k), int(k), int(size))
    return b + b.T, _next(rng)


def gram(size, seed):
    """B^T B, B of r rows and n columns, n between 1 and the size and r between 0 and n: symmetric
    positive semidefinite, of rank r at most (a rank below n in most draws)."""
    rng = _source(seed)
    n = _length(rng, size, 1)
    b = arrays._mat(rng, rng.randint(0, n), n, int(size))
    a = b.T @ b
    return (a + a.T) / 2.0, _next(rng)


def orthogonal(k, size, seed):
    """Haar-distributed orthogonal matrix of k rows (7.S5): Q of the QR factorization of a matrix of
    standard Gaussian entries, each column multiplied by the sign of R's diagonal entry (Mezzadri
    2007: without it the distribution is not Haar). The size is not read: the family has none."""
    rng = _source(seed)
    k = int(k)
    z = np.array([[rng.gauss(0.0, 1.0) for _ in range(k)] for _ in range(k)], dtype=float).reshape(k, k)
    if k == 0:
        return z, _next(rng)
    q, r = np.linalg.qr(z)
    signs = np.sign(np.diag(r))
    signs[signs == 0] = 1.0
    return q * signs, _next(rng)


def unit_list(atoms, size, seed):
    """A list of between 0 and `size` vectors, each of between 0 and `size` entries in [0, 1]: each
    entry is, with probability `atoms`, one of 0, 1 or an entry already drawn (a tie), and otherwise
    uniform in [0, 1)."""
    rng = _source(seed)
    drawn, out = [], []
    for _ in range(_length(rng, size)):
        entries = []
        for _ in range(_length(rng, size)):
            if rng.random() < float(atoms):
                choice = rng.randrange(3)
                x = 0.0 if choice == 0 else 1.0 if choice == 1 or not drawn else rng.choice(drawn)
            else:
                x = rng.random()
            entries.append(x)
            drawn.append(x)
        out.append(np.array(entries, dtype=float))
    return out, _next(rng)


def uniform_sample(size, seed):
    """A calibrated sample (7.S17): a list of between 1 and `size` vectors, each of between 1 and
    `size` entries, every entry independent and uniform in [0, 1)."""
    rng = _source(seed)
    out = [np.array([rng.random() for _ in range(_length(rng, size, 1))], dtype=float)
           for _ in range(_length(rng, size, 1))]
    return out, _next(rng)


def clear_diagonal(atom, lo, hi, size, seed):
    """A vector of between 1 and `size` entries, each 0 with probability `atom` (7.S4's atom at 0),
    otherwise a sign and a magnitude log-uniform in [lo, hi] (the log metric, 7.S4), kept within
    the bounds against the rounding of exp."""
    rng = _source(seed)
    lo, hi = float(lo), float(hi)
    entries = []
    for _ in range(_length(rng, size, 1)):
        if rng.random() < float(atom):
            entries.append(0.0)
        else:
            x = min(hi, max(lo, math.exp(rng.uniform(math.log(lo), math.log(hi)))))
            entries.append(x if rng.random() < 0.5 else -x)
    return np.array(entries, dtype=float), _next(rng)
