# Report: the tail of the controls (PinvScales, UniformSampleIsUniform, conftest, the stores)

Brief: record/IA/controls-2026-10-15/prompt-tail.md. By Claude Opus 5.5, a subagent of the
coordinating session, 2026-10-15. Each change is its own commit; the ones marked [proposed] are
undone by that commit.

Principles touched: L9.14 (a law is evidence of nothing until a wrong model refutes it), applied to
PinvScales and UniformSampleIsUniform; P2 (everything derived carries how it was derived) for the
two model stores; P6 (every change can be undone) for the suite, which no longer rewrites the
library's stores. Assumes, as before, that a control matches its law by the law's cone hash.

## 1. PinvScales

PinvScales had RankScales's weakness (report-weak-laws.md): `c : Positive` is drawn within the
size, so it only scaled s by (0, 10] and never pushed an eigenvalue of order one below an absolute
floor. Before touching the law I ran it on a broken model, `pinvAbs`, whose pinvSym drops the
eigenvalues below an absolute 1e-3 (read through the relative leaf as `rankAbs` is: floor
1e-3 / frobDef a, zero matrix when the norm is at most 1e-3), on drawn symmetric matrices
(`symmetric`, seed 20261015, 100 cases), from a scratch file outside the repo with `--no-cert`:
CONTROL FAILED, the old law held on it.

- df74a74 arrays.lth [proposed]: the law also compares P at the scale `c * fl / frobDef s` (a
  Frobenius norm of c times the floor, where every eigenvalue is below any absolute floor above
  c fl) with P over that scale, at the same tolerance as the c clause; a zero floor or a zero
  matrix skips the clause, as in RankScales. On the same scratch run numpy held (seed 20261014,
  100 cases) and pinvAbs was refuted (c = 9.14, s 4 x 4).
- 8f4a02c arrays_controls.lut: PinvScales's control is now pinvAbs on drawn symmetric matrices.
  Before it was `ridge` on the default draw (0 x 0 and 1 x 1 matrices only), a break the size of the
  matrix that the old law already saw.

## 2. UniformSampleIsUniform

- d55ef9c generators_model.lut [proposed]: `UniformSampleIsUniform (source : Gen UnitList)
  (c : Sequential) : Law := SourceIsUniform numpySort source c`. `SkewedSampleIsUniform` is gone.
- dc357c5 generators_laws.lut: the line binds `source` to `uniformSample` (a census of one; on a
  statistical line a `Gen` binding is the stream itself).
- 9da69d7 generators_controls.lut: two control lines of the law itself, `source <- skewedSample`
  and `source <- lump` (probability_model.lut's source, every value 0.9).

The duplicate: yes, they computed the same thing. generators_laws.lut's UniformSampleIsUniform
line and probability_laws.lut's SourceIsUniform line ran SourceIsUniform with the same distance
(numpySort), the same source (uniformSample), the same seed (20261014) and the same cutoffs
(`wald`), so the same sequential test, about 35 s each. Since the brief wants UniformSampleIsUniform
controlled, I dropped the probability one (38356fa). Its control `lump` would have been left with
no law line, so I moved it to generators_controls.lut as UniformSampleIsUniform's second control
(733d537 removes it from probability_controls.lut). b32b433 test_tester.py: the test that a type in a
census is no model home used the SourceIsUniform line as its positive contrast; KolmogorovOfOne
now plays that role (it binds the same `d`, home probability_model.lut).

## 3. The suite and certify

conftest.py put every library store back after each test, from a snapshot taken at the test's
start, so any certify write during a test was reverted. You can't tell from the bytes whether the
test or another process made a change, and tests that call `main(["certify", ...])` spawn
processes an in-process patch would not reach. So I took the brief's second route: tests write
to a temporary copy.

- d5c712d certify.py [proposed]: `store_path` sends the store of a file in src/luthier/lib to the
  directory named by `LUTHIER_LIBRARY_STORES` when that is set. Nothing else reads it. certify.py's
  bytes enter only the cones that reach `python:luthier.certify`, i.e. certification_model.lut,
  which no test file certifies.
- 03f03f9 conftest.py: each test copies the library's stores (556 KB) into a temporary directory,
  sets the variable (spawned processes inherit it), and removes the copy afterwards. The library's
  stores are never written by the suite.
- 7c70b4f test_certify.py: inside the context, a test's own write lands in the copy, and a store
  in the library rewritten by another process (a subprocess without the variable) still holds that
  process's entry after the context exits. Under the old snapshot-and-restore it would have been
  reverted.

## 4. The run

Deleted the stray untracked src/luthier/lib/probability.cert.json. `luthier certify --jobs 2
--fuel 100000000`, with stores, on arrays, generators and probability `_laws.lut` and
`_controls.lut` at 7c70b4f, no suite running: exit 0, 2 min 19 s. CONTROL FAILED appears 0 times.
All 60 laws of the three files read controlled. The two of this brief:

    arrays_laws.lut      PinvScales: sampled; controlled (m = pinvAbs, c = 9.14, s 4 x 4)
    generators_laws.lut  UniformSampleIsUniform: supported, sampled: held at 144 samples of 50
                         (alpha 0.01, beta 0.01, delta 0.5, budget 400); controlled (both controls
                         refuted at 12 samples of 50)

Committed as derived: c805124 arrays_model.cert.json (PinvScales's entries at its new cone) and
007c686 probability_model.cert.json. Nothing in that second store was written by this run (the
probability files ran 0 lines, all 36 + 18 known); its diff holds what the earlier agents' runs
wrote and left uncommitted, read here as current. generators_model.cert.json did not change:
UniformSampleIsUniform's line names no model of another file (uniformSample is a generator, which
is no home), so its entry is only in the test file's store.

`python -m pytest -q`, run alone after certify: 710 passed, 5 skipped, 9 xfailed (4 min 25 s).
The model stores were unchanged afterwards.

## Findings

- The SourceIsUniform law of probability.lth now runs only through generators_model.lut's
  UniformSampleIsUniform. The law is the same and the cone differs, so a demand on SourceIsUniform
  itself would find no entry. If that matters, the reverse choice (keep probability's line, give
  UniformSampleIsUniform's line a different source) is one revert of 38356fa, 733d537 and b32b433.
- Like rankAbs, pinvAbs's "absolute" floor is 1e-3 times largest / Frobenius, so it lies between
  1e-3 / sqrt(n) and 1e-3 in absolute terms. It is absolute in the sense that matters: it doesn't
  scale with s.
- certify writes the tests/tester stores too, and the suite still writes those (ignored by git)
  when a test runs a tests/tester file with stores. The brief covered only the library's.

## Decisions taken on my own (each undone by one commit)

- PinvScales's second scale `c * fl / frobDef s`, the same as RankScales's (df74a74).
- Replaced ridge by pinvAbs as PinvScales's only control instead of adding a second line (8f4a02c).
- Dropped probability_laws.lut's SourceIsUniform line and kept generators_laws.lut's (38356fa).
- Moved the lump control to generators_controls.lut as a second control of UniformSampleIsUniform
  (9da69d7, 733d537); the test_tester.py contrast moved to KolmogorovOfOne (b32b433).
- The suite works on a copy of the library's stores through an environment variable read by
  certify.store_path, a change to production code (d5c712d, 03f03f9).
- Committed probability_model.cert.json with the earlier agents' entries in it (007c686).
