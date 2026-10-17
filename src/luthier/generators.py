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

The special values and the degenerate families (record/IA/regions-2026-10-17/prompt-code.md, items 1
and 2 of report-theory.md section 5; D-2026-10-16-i, D-2026-10-16-j, L9.16): sampling bounds the
fraction of failures under its distribution and says nothing of its null sets, so the cases a law
turns on are given mass. `special` gives a number the tester draws (tester.py's `Values`) the mass
of 7.S4: an atom at 0 and, with a total probability, one of the special values (the bounds and
their neighbours, 0, 1 and -1 when in the support, and the literals given, each with its
neighbours); the two masses are the budgets' `atomAtZero` and `specialMass` (generators.lth §6),
passed in. The matrix families draw their dimension from `DIMENSIONS` (7.S5) and give the zero
matrix and a rank-deficient one each a share, arguments with defaults [proposed: the shares
generators_model.lut does not pass yet, so their defaults are the budgets' `specialMass`].
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


# 7.S5's census of dimensions (LAPACK's tests at these), the default of every family that draws one
# [decided D-2026-10-06-ab]; a family draws those not above its size [proposed: the size stays the
# largest, test.lth's `size`]
DIMENSIONS = (0, 1, 2, 3, 5, 10)
# [proposed] the share of the zero matrix and of a rank-deficient one in a family that draws a
# matrix: the default of the budgets' `specialMass` (test.lth's `defaultBudgets`)
FAMILY_SHARE = 0.05


def dimension(rng, size, dims=DIMENSIONS, low=0):
    """A dimension from the census `dims` (7.S5), among those between `low` and the size (`low` when
    none is)."""
    allowed = [d for d in dims if low <= d <= max(low, int(size))]
    return rng.choice(allowed) if allowed else low


def neighbours(x, integer):
    """x and the numbers next to it: x - 1 and x + 1 for an integer, the doubles next to x
    otherwise (7.S4's "the bounds and their neighbours")."""
    if integer:
        return [x - 1, x, x + 1]
    return [math.nextafter(x, -math.inf), x, math.nextafter(x, math.inf)]


def specials(lo, hi, integer, literals=()):
    """7.S4's special values of a number in [lo, hi]: the bounds and their neighbours, 0, 1 and -1,
    and each literal given with its neighbours, those in the support, each once, in that order.
    [proposed] For a literal that is a cutoff (a tolerance, a floor: D-2026-10-16-j's two sides of
    a cutoff) its double and its half too, the values just above and just below it at the scale of
    the neighbourhood `regions_of` reads (tester.py)."""
    out = []
    for b in (lo, hi):
        out += neighbours(b, integer)
    out += [0, 1, -1]
    for c in literals:
        out += neighbours(c, integer)
        if not integer and c != 0:
            out += [2.0 * c, c / 2.0]
    kept = []
    for v in out:
        v = int(v) if integer else float(v)
        if lo <= v <= hi and v not in kept:
            kept.append(v)
    return kept


def special(rng, lo, hi, integer, special_mass, atom_at_zero, literals=()):
    """7.S4's mass on a number drawn in [lo, hi]: 0 with probability `atom_at_zero` (when 0 is in
    the support), else one of `specials` with probability `special_mass`; None otherwise, and the
    caller draws from its metric. One uniform is drawn from `rng` whatever comes out, so that the
    rest of the stream does not depend on which branch was taken."""
    u = rng.random()
    if u < float(atom_at_zero) and lo <= 0 <= hi:
        return 0 if integer else 0.0
    if u < float(atom_at_zero) + float(special_mass):
        values = specials(lo, hi, integer, literals)
        if values:
            return values[rng.randrange(len(values))]
    return None


def degenerate(rng, a, zero=FAMILY_SHARE, deficient=FAMILY_SHARE):
    """A square matrix replaced, with probability `zero`, by the zero matrix of its size, and with
    probability `deficient` (two rows or more) made rank deficient by a row and a column of zeros
    (symmetric stays symmetric, and a zero row is arrays.lth's `rowsRepeatOrVanish`): the zero and
    rank-deficient families of 7.S5 given their share (`matDegeneracies`, `symmetricDegeneracies`)."""
    u = rng.random()
    if u < float(zero):
        return np.zeros_like(a)
    if u < float(zero) + float(deficient) and a.shape[0] >= 2:
        k = rng.randrange(a.shape[0])
        a = a.copy()
        a[k, :] = 0.0
        a[:, k] = 0.0
    return a


def symmetric(size, seed, dims=DIMENSIONS, zero=FAMILY_SHARE, deficient=FAMILY_SHARE):
    """v0.1's `gen_symmetric`: B + B^T, entries of B uniform in [-size, size]; symmetric exactly, any
    spectrum. Its dimension from the census `dims` (7.S5; v0.1 drew it between 1 and the size), and
    the zero and rank-deficient families with their shares (`degenerate`). Built here and not in
    arrays.py, whose bytes are the host hash of every numpy entry (certify.host_hash): editing it
    makes the model's entries stale."""
    rng = _source(seed)
    n = dimension(rng, size, dims)
    b = arrays._mat(rng, n, n, int(size))
    a = b + b.T
    return degenerate(rng, a, zero, deficient), _next(rng)


def symmetric_of(k, size, seed, zero=FAMILY_SHARE, deficient=FAMILY_SHARE):
    """B + B^T of k rows, entries uniform in [-size, size], the zero and rank-deficient families
    with their shares (`degenerate`)."""
    rng = _source(seed)
    b = arrays._mat(rng, int(k), int(k), int(size))
    return degenerate(rng, b + b.T, zero, deficient), _next(rng)


def gram(size, seed, dims=DIMENSIONS):
    """B^T B, B of r rows and n columns, n from the census `dims` (7.S5; v0.1 drew it between 1 and
    the size) and r between 0 and n: symmetric positive semidefinite, of rank r at most (a rank
    below n in most draws, the zero matrix when r is 0)."""
    rng = _source(seed)
    n = dimension(rng, size, dims)
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
