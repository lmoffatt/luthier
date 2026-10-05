"""Python values for tests/test_bridge.py: each returns something the bridge must accept, convert
or reject by the declared type of the extern that calls it."""
import numpy as np


def hello(s):
    return "hello"


def as_int(x):
    return int(x)


def three_float():
    return 3.0


def true_value():
    return True


def numpy_int():
    return np.int64(7)


def int_array():
    return np.array([1, 2, 3])


def float_array():
    return np.array([1.0, 2.0])


def matrix():
    return np.zeros((2, 2))


def nan_list():
    return [1.0, float("nan")]


def scalar():
    return 3.0


def not_none():
    return 3


def negative(x):
    return -2.0


def indices_out_of_range():
    return np.array([0, 1, 5])


def indices_in_range():
    return np.array([0, 1, 2])


def pair_of_vector(x):
    return np.array([x, x])


def gen_unit_point(rng, size):
    """Points of the unit circle: a distribution the law below can tell from the default one."""
    a = rng.uniform(0.0, 6.283185307179586)
    return (float(np.cos(a)), float(np.sin(a)))


def gen_positive_wrongly(rng, size):
    """A generator that claims positive numbers and gives a negative one."""
    return -1.0
