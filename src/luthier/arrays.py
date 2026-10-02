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


def gen_vec(rng: random.Random, size: int):
    return _vec(rng, _dim(rng, size), size)


def gen_mat(rng: random.Random, size: int):
    return _mat(rng, _dim(rng, size), _dim(rng, size), size)


def gen_frame(rng: random.Random, size: int):
    """Compatible shapes for the laws: A is m x n, S is n x n symmetric positive definite,
    x and z have length n, y has length m. Returned in the order the record declares."""
    m, n = _dim(rng, size), _dim(rng, size)
    A = _mat(rng, m, n, size)
    B = _mat(rng, n, n, size)
    S = B.T @ B + np.eye(n)
    return (A, S, _vec(rng, n, size), _vec(rng, n, size), _vec(rng, m, size))


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
