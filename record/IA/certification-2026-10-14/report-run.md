# run refuses a cone that is not certified: report

2026-10-15, Claude Opus 5.5, an agent of luthier-3e, on prompt-run.md; saved by the coordinator.
Files: `src/luthier/certify.py` (readers: `contains`, `covers_all`, `serves`, `state_of`,
`refuse`, `show_refusal`, `GRADES`), `src/luthier/run.py` (`certification()` before evaluation:
the stores of every file the loader visits, one demand per law the theory head of each cone
name states, the law's hash from a slice with the laws as roots; `refuse_provisional()` before
elaboration; `Refused` lists each law with its state, exit 1, nothing evaluated, no record;
`record` adds `certification` to `x.run.json`: the cone hash, the interpreter revision, the grade
accepted, the counts of states, `not certified`), `src/luthier/cli.py` (`run --accept GRADE`),
`tests/test_run.py` (7 tests; the refused existing tests marked strict xfail), programs under
`tests/run/certified/`. Checks: test_run and test_certify 93 passed, 7 xfailed; the suite 592
passed, 14 xfailed, one failure in test_lm (marked strict xfail by the coordinator at the
commit); under LUTHIER_SLOW=1 the numbers laws pass, validate_graph is refused (xfail).

## What runs and what is refused

Runs: every program whose types state no law (hello.lut, the host, callbacks, holes, scope,
observe, ...). Refused, every law "uncertified (no entry)": vector_norm, matrix_product (`numpy :
Arrays`, 35 laws); maximize_quadratic, maximize_shared, test_lm (`lm : Maximizer` 4, numpy);
table_cell (`built : Table` 4, `csv : Codec` 4); host_cell_under_operator, label_and_definition
(csv); validate_graph (csv, `doubles` 21, `elementary` 14, numpy); experiment_zero (those,
`numpySort : Kolmogorov` 5, lm; refused in 5 s).

Why still refused after certifying: `luthier certify tests/tester/*_laws.lut --jobs 4` (26 min)
graded every law but `FullAgrees`, `ProfileAgrees`, `ProfileIsFullAtItsSigma` (fuel spent); but
the entries sit in `tests/tester/*.cert.json`, and per 12.S11 a run reads only the stores of the
files it imports (`.gitignore` keeps `!src/luthier/lib/*.cert.json`: lib is the intended home).
A scratch check reading the tester stores served numpy, lm, doubles, elementary, numpySort.
Laws no entry serves in the slice's cone: `csv : Codec`'s four and `built : Table`'s four (no
tables laws file; `Table`, `Perturbed`, `BrokenText` have no generator, 7.R4): listed case
entries would certify them.

## Decisions for Luciano

1. Where the library's entries go: the test lines into the model files, or `certify` writing
   each entry into the store of the file that defines the model named in the binding.
2. The interpreter revision: committing changes it, so every store goes stale; rerun certify
   (26 min) after each commit to `src/luthier/*.py`.

## Choices of the agent (each undone by one commit)

`--accept` defaults to `sampled` [proposed]; only theory heads state laws, a refinement none, a
lawless type certified vacuously; what the run gives a law: the name itself to the parameter
typed by the theory, each `--set` hole to the parameter of its name; an entry is "at" the
current hash when the law's cone matches and the binding's fingerprint equals the model's
current cone hash, else stale; a passed entry that does not serve is listed with the reason;
provisional names checked before elaboration; stores merged latest first by date; refused
tests marked strict xfail.
