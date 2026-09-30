"""Python-side generators for opaque types (`T : U := extern "..."`), whose values cannot be
built in Luthier. Register one with `gen T := extern "python:luthier.pygen.name"`; each takes
the run's `random.Random` and the current size, so results follow the run seed."""
import random


def _np():
    import numpy
    return numpy


def uniform_signal(rng: random.Random, size: int):
    """Length 8*size, values uniform in [-1, 1]."""
    return _np().array([rng.uniform(-1.0, 1.0) for _ in range(8 * max(size, 1))])


def normal_signal(rng: random.Random, size: int):
    """Length 8*size, standard normal samples."""
    return _np().array([rng.gauss(0.0, 1.0) for _ in range(8 * max(size, 1))])


def sine_signal(rng: random.Random, size: int):
    """Length 8*size: a sine of random frequency and phase plus small noise."""
    np = _np()
    n = 8 * max(size, 1)
    f = rng.uniform(0.5, 4.0)
    phase = rng.uniform(0.0, 6.283185307)
    t = np.arange(n) / n
    return np.sin(6.283185307 * f * t + phase) + 0.01 * np.array([rng.gauss(0.0, 1.0) for _ in range(n)])


def big_normal_signal(rng: random.Random, size: int):
    """2**20 standard normal samples, drawn with numpy from a seed taken from the run's stream."""
    np = _np()
    return np.random.default_rng(rng.randrange(2 ** 31)).standard_normal(2 ** 20)
