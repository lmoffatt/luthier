"""Host side of the bridge tests of run.py bite 8 (record/IA/run-2026-10-13/prompt-8.md,
D-2026-10-14-a): host functions that call Luthier functions back, read a record of them by
attribute, give a host function to Luthier, and receive a partial application of an extern.
Imported by the programs under tests/run/ as `python:run.bridge_host.*` (tests/ on the path)."""
import functools

GRID = [k / 10 for k in range(10)]


def maximize(f):
    """Calls `f` at the ten points of GRID and gives the point where it is least (as lm.maximize
    gives the best point of a loss)."""
    values = [f(x) for x in GRID]
    assert all(type(v) is float for v in values)
    return GRID[values.index(min(values))]


def descend(objective):
    """Reads `objective.value` and `objective.grad` as attributes: three calls of `value`, two of
    `grad`; gives value(1) + grad(1)."""
    assert objective.value(0.0) == objective.value(0.0)
    return objective.value(1.0) + objective.grad(1.0) + 0 * objective.grad(2.0)


def adder(k):
    """A host function given back to Luthier: x -> k + x."""
    def add(x):
        return k + x
    return add


def twice_at(x):
    """A host function given back to Luthier that calls the Luthier function it receives twice."""
    def at(f):
        return f(x) + f(x)
    return at


def add(x, y):
    return x + y


def describe(f):
    """What the host received for a partial application of an extern."""
    if isinstance(f, functools.partial):
        return f"partial {f.func.__name__} {f.args!r} {f(2.0)!r}"
    return f"{type(f).__name__} {f(1.0, 2.0)!r}"
