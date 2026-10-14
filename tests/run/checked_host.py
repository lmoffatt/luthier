"""Host side of `run --checked` (record/IA/run-2026-10-13/prompt-12.md item 3; 12.S18, 4.R5,
10.S11): honest and dishonest values at declared subtypes (`Positive`, `VecOf 3`, `PsdAt`).
Imported by tests/run/checked.lut as `python:run.checked_host.*` (tests/ on the path)."""
import numpy as np


def two(u):
    return 2.0


def minus_one(u):
    """A negative where `Positive` is declared."""
    return -1.0


def three_entries(u):
    return np.array([1.0, 2.0, 3.0])


def two_entries(u):
    """Two entries where `VecOf 3` is declared."""
    return np.array([1.0, 2.0])


def identity(u):
    return np.eye(2)


def indefinite(u):
    """A symmetric matrix with a negative eigenvalue where `PsdAt numpy 0.1` is declared."""
    return np.diag([1.0, -1.0])
