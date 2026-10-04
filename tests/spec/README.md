# Specification suite

One pair of programs per rule of `docs/semantica/05-static-semantics.md` (files `r*`), and
programs for the type formers of `docs/semantica/04-kernel.md` (files `k*`): a file the checker
must accept and a file it must reject. A rejected file carries the fragment of the error message
it must produce in a comment `-- expect: ...`. Files not ending in `.accept.lut` or `.reject.lut`
are imported by others and not run on their own.

`tests/test_spec.py` runs the suite.
