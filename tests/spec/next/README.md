# Specification suite, next

Programs for what `docs/semantica/06-numbers.md` decides and the interpreter does not implement
yet: the primitive bodies, the numbers, axioms, the variance of function types, arrays over any
type, the bridge's checks. `tests/test_spec_next.py` runs them marked xfail; when a case passes, it
moves to `tests/spec/` and its mark goes.
