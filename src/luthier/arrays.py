"""Array primitives for Luthier: vectors and matrices as numpy arrays.

`Vec` and `Mat` are opaque types (`extern "python:numpy.ndarray"`); the operations here are
the primitives `lib/array.lut` declares, and that file states the algebraic laws they are
certified by. Nothing in Luthier takes an array apart element by element; `toList` is the
one bridge back, for small values and for laws about lists.

Generators take the run's `random.Random` and the current size, like every Python generator.
"""
import random

import numpy as np


# ------------------------------------------------------------------ construction and reading

def from_list(xs):
    return np.asarray(xs, dtype=float)


def to_list(v):
    return [float(x) for x in np.asarray(v).ravel()]


def length(v):
    return int(np.asarray(v).shape[0])


def rows(a):
    return int(np.asarray(a).shape[0])


def cols(a):
    return int(np.asarray(a).shape[1])


def at(v, i):
    return float(np.asarray(v)[i])


def entry(a, i, j):
    return float(np.asarray(a)[i, j])


def zeros(n):
    return np.zeros(int(n))


def identity(n):
    return np.eye(int(n))


def from_rows(rs):
    """A matrix from a list of equal-length vectors, one per row."""
    return np.vstack([np.asarray(r, dtype=float) for r in rs])


# ------------------------------------------------------------------ vector algebra

def add(a, b):
    return np.asarray(a) + np.asarray(b)


def sub(a, b):
    return np.asarray(a) - np.asarray(b)


def scale(c, a):
    return float(c) * np.asarray(a)


def dot(a, b):
    return float(np.dot(np.asarray(a), np.asarray(b)))


def norm(a):
    return float(np.linalg.norm(np.asarray(a)))


def total(a):
    return float(np.sum(np.asarray(a)))


def minimum(a):
    return float(np.min(np.asarray(a)))


def maximum(a):
    return float(np.max(np.asarray(a)))


# ------------------------------------------------------------------ matrix algebra

def outer(a, b):
    return np.outer(np.asarray(a), np.asarray(b))


def mat_vec(a, x):
    return np.asarray(a) @ np.asarray(x)


def mat_mul(a, b):
    return np.asarray(a) @ np.asarray(b)


def transpose(a):
    return np.asarray(a).T.copy()


def trace(a):
    return float(np.trace(np.asarray(a)))


def det(a):
    return float(np.linalg.det(np.asarray(a)))


def solve(a, b):
    """x with A x = b, for a square A."""
    return np.linalg.solve(np.asarray(a), np.asarray(b))


# ------------------------------------------------------------------ comparison

def approx(tol, a, b):
    """Every entry of a and b within tol, measured against the size of the entries:
    |a - b| <= tol * (1 + |a| + |b|)."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != b.shape:
        return False
    return bool(np.all(np.abs(a - b) <= float(tol) * (1.0 + np.abs(a) + np.abs(b))))


# ------------------------------------------------------------------ generators

def _dim(rng: random.Random, size: int) -> int:
    return rng.randint(1, max(1, min(size, 8)))


def _vec(rng: random.Random, n: int, size: int):
    return np.array([rng.uniform(-size, size) for _ in range(n)])


def _mat(rng: random.Random, m: int, n: int, size: int):
    return np.array([[rng.uniform(-size, size) for _ in range(n)] for _ in range(m)])




def cond(a):
    """Condition number in the 2-norm: how much solve amplifies rounding."""
    return float(np.linalg.cond(np.asarray(a)))


def frob(a):
    """Frobenius norm of a matrix."""
    return float(np.linalg.norm(np.asarray(a)))


# ------------------------------------------------------------------ construction by index
# The dual of the accessors: Python walks the indices and calls a Luthier function for each
# entry, so a program can build an array without ever holding it as a list.

def tabulate(n, f):
    return np.array([float(f(k)) for k in range(int(n))])


def tabulate_mat(m, n, f):
    return np.array([[float(f(i, j)) for j in range(int(n))] for i in range(int(m))])


# ------------------------------------------------------------------ rows, pieces, stacking

def row(a, i):
    return np.asarray(a)[int(i)].copy()


def stack(n, f):
    """A matrix whose row i is the vector f(i), for i below n."""
    return np.vstack([np.asarray(f(i), dtype=float) for i in range(int(n))])


def ones(n):
    return np.ones(int(n))


def head(v, n):
    """The first n entries."""
    return np.asarray(v)[: int(n)].copy()


def last(v):
    return float(np.asarray(v)[-1])


def append(v, x):
    return np.append(np.asarray(v, dtype=float), float(x))


def concat(a, b):
    return np.concatenate([np.asarray(a, dtype=float), np.asarray(b, dtype=float)])


# ------------------------------------------------------------------ spectral (leaves with laws)

def eigvals_sym(a):
    """Eigenvalues of a symmetric matrix, ascending."""
    return np.linalg.eigvalsh(np.asarray(a))


def inv_sqrt_sym(a):
    """The symmetric M with M A M = I, for A symmetric positive definite."""
    w, V = np.linalg.eigh(np.asarray(a))
    return (V / np.sqrt(w)) @ V.T


def product(v):
    return float(np.prod(np.asarray(v)))


# ------------------------------------------------------------------ randomness threaded by seed

def normal_vec(n, seed):
    """n standard normals from a seed, and the next seed."""
    rng = np.random.default_rng(int(seed) % (2 ** 63))
    return (rng.standard_normal(int(n)), int(rng.integers(0, 2 ** 62)))





# ------------------------------------------------------------------ matrix arithmetic, entrywise

def madd(a, b):
    return np.asarray(a) + np.asarray(b)


def msub(a, b):
    return np.asarray(a) - np.asarray(b)


def mscale(c, a):
    return float(c) * np.asarray(a)


def hadamard(a, b):
    """Entrywise product."""
    return np.asarray(a) * np.asarray(b)


def max_abs(a):
    return float(np.max(np.abs(np.asarray(a))))


def index(v, k):
    """Entry k of a vector of whole numbers, as an Int."""
    return int(round(float(np.asarray(v)[int(k)])))


# ------------------------------------------------------------------ the retained subspace
# The eigenvalues of a symmetric matrix kept are those above n * eps * max |eigenvalue|: below
# that they are indistinguishable from rounding, and directions with them (a gauge) are dropped.

def _retained(w):
    return w > w.size * np.finfo(float).eps * np.max(np.abs(w))


def retained_rank(a):
    return int(np.sum(_retained(np.linalg.eigvalsh(np.asarray(a)))))


def pinv_sym(a):
    """The pseudo-inverse of a symmetric matrix on its retained subspace."""
    w, V = np.linalg.eigh(np.asarray(a))
    keep = _retained(w)
    return (V[:, keep] / w[keep]) @ V[:, keep].T


def pinv_sqrt_sym(a):
    """M with M A M the projector on the retained subspace of A."""
    w, V = np.linalg.eigh(np.asarray(a))
    keep = _retained(w)
    return (V[:, keep] / np.sqrt(w[keep])) @ V[:, keep].T



# ------------------------------------------------------------------ generators by dimension
# The shapes are in the types (VecOf n, MatOf m n); each generator receives the dimensions.

def gen_dim(rng: random.Random, size: int):
    return rng.randint(1, max(1, min(size, 8)))


def gen_dim2(rng: random.Random, size: int):
    return rng.randint(2, max(2, min(size, 8)))


def gen_vec_of(rng: random.Random, size: int, n):
    return _vec(rng, int(n), size)


def gen_mat_of(rng: random.Random, size: int, m, n):
    return _mat(rng, int(m), int(n), size)


def gen_spd_of(rng: random.Random, size: int, n):
    """B^T B + I: symmetric, eigenvalues at least one."""
    B = _mat(rng, int(n), int(n), size)
    return B.T @ B + np.eye(int(n))


def gen_deficient_of(rng: random.Random, size: int, n):
    """The Gram matrix of fewer vectors than the dimension: positive semidefinite, rank below n."""
    n = int(n)
    r = rng.randint(1, n - 1)
    B = _mat(rng, r, n, size)
    return B.T @ B
