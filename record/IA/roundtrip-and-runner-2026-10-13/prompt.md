# Random trees for RoundTrip, and the runner of tests/spec: brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 for Luciano, who gives it
to Codex in this repository. Two bites; do the first, run the tests, then the second.

## The prompt

Read `CLAUDE.md` first: its working rules bind you too. Another session is writing
`src/luthier/lib/term.lth` and may commit while you work: do not touch `src/luthier/lib/`,
`docs/`, `record/` (except your report), `tests/spec/*.lut`, or `src/luthier/parse.py`.

**Bite 1, `tests/test_roundtrip_trees.py`: `RoundTrip` on random trees.** The law `RoundTrip` in
`src/luthier/lib/grammar.lth` says that for every tree a text can give (`WrittenProgram`, the
subtype of `wfProgram (isName d g)`), `parse (print p) == parsed p`. Today it is tested on parsed
texts only. Write a generator of random `SurfaceProgram`s (the classes of `src/luthier/surface.py`)
that satisfy `wf`, `wfAct`, `wfProgram` exactly as `grammar.lth` defines them, with names drawn
from a fixed list that `luthier.parse.lex` reads as names, and a size `s` that bounds depth: at
size 0 only constructors with no recursive argument, otherwise the size less one split among the
recursive arguments (the rule proposed in spec 7.S3). Seeded (`random.Random(seed)`), with the
seed and size printed on failure, and the failing tree shrunk to a smaller one that still fails
if that is cheap. Test: for seeds 0 to 999 at sizes 0 to 6, `parse(print_program(p)) ==
Parsed(p)`; and `Canonical` on the printed text. If a case fails, do not fix `parse.py`: record the
smallest failing tree, the printed text, and the parse result in your report; mark the test
`xfail(strict=True)` with that reason so the suite stays green.

**Bite 2, `tests/test_spec.py`: the runner of `tests/spec/`, syntax only.** For each
`tests/spec/*.lut`: read its header (`-- expect: ...`, `-- expect (v0.1): ...`, `-- expect
(proposed): ...`, `-- verdict: ...`, read `tests/spec/README.md` for their meaning), and check what
can be checked without a checker: an `.accept.lut` parses; a `.reject.lut` either parses (its
rejection is the checker's, reported as pending) or is a syntax rejection, which counts as its
reject only if it is listed in a set in the test with its reason (today `r12_toplevel_arrow`).
Also check that every program named on a `Files:` line of `docs/spec/*.md` exists in
`tests/spec/` or `tests/spec/v0.1/`. Leave a clearly named hook where the checker's verdict and
message will be compared once `luthier check` exists.

Check: `python3 -m pytest tests/ -q` passes whole; `python3 scripts/check_spec.py` passes. Do not
commit. Report in a few lines to `record/IA/roundtrip-and-runner-2026-10-13/codex.md`: what you
wrote, the test counts, and every failing tree of bite 1 with its text.
