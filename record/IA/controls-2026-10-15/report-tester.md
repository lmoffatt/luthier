# Report: the tester knows controls (L9.14, D-2026-10-15-a)

Brief: record/IA/controls-2026-10-15/prompt-tester.md. By Claude Opus 5.5, a subagent of the
coordinating session, 2026-10-15. Committed: src/luthier/lib/test.lth alone (a92db27). Uncommitted,
as the brief asks: src/luthier/tester.py, certify.py, cli.py, tests/test_tester.py,
tests/test_certify.py, tests/tester/tables_controls.lut. The stores (*.cert.json) are untouched.

Principles touched: L9.14 (every law carries a model it refutes) and 7.S19, applied; P11 (every
criterion a parameter): `control` is a named argument of `test` with a default; P3 (keep the
evidence): no store was rewritten. Assumes the law's cone hash names the law across importers
(checked: tables_laws and tables_controls give CellsOfTheirKind the same hash, 7bdd74d3).

## What changed

1. test.lth (a92db27) [proposed]: `TestSpec` gains `control : Bool`, `test` the named argument
   `(control <- false)`, and §2 `controlPasses v` (true on `Refuted`), cited to 7.S19, L9.14,
   D-2026-10-15-a. A field with a default is the least change; a form `control law ...` would need
   the parser. `luthier check` passes on it.
2. tester.py: `Spec.control` read from the line; a control's entry is its own kind,
   `"kind": "Control"`, with outcome `ControlRefuted` (the case: the control passed),
   `ControlConfirmed` (the grade it would have had: the control failed) or `NotRunFor`, and never a
   grade. Lines print as `control of LAW: ..., refuted at ...: the control passed` or
   `CONTROL FAILED: the law held on the model broken on purpose, too weak to see the break (7.S19)`.
   `luthier test` exits 0 when every law line has a grade and every control is refuted.
3. certify.py: the kind is part of the identity and of the prune group; the grade, the state,
   `state_of`, `serves` and `refuse` read the law's own entries only, so a control's refutation
   never refutes the law nor blocks a run. New: `control_status` (controlled / CONTROL FAILED /
   uncontrolled: untested against any wrong model (7.S19)), `control_standing`, `controls_in`.
   `certify` collects every file's results first, then prints per law `grade; control status`
   and per control line `control of LAW on BINDING: outcome`; it exits 1 when a control failed.
   The grade itself is unchanged.
4. cli.py: `certify --no-cert` (read and write no store); `check -v` prints the control status
   per law, reading the controls from the stores of every file the command is given, and the
   standing of each control line.
5. tables_controls.lut: its line is `(control <- true)`; header comment rewritten.
6. Tests: three in test_tester.py (a control refuted passes, a law line is no control, a control
   the law holds on fails), four in test_certify.py (a control entry is no evidence of the law,
   the status of a law, the tables acceptance with `--no-cert` leaving the stores byte-identical,
   controls through the stores in `certify` and `check -v` with a failing control), and one
   updated (`test_certify_several_files`: the status now follows each grade).

Suite: 703 passed, 5 skipped, 9 xfailed (`python -m pytest -q`, 4m17s).

## Acceptance

`luthier certify tests/tester/tables_laws.lut tests/tester/tables_controls.lut --no-cert`, exit 0:

    tests/tester/tables_laws.lut: 8 laws, 8 lines ran, 0 known
      RoundTrip: cases; uncontrolled: untested against any wrong model (7.S19)
      Canonical: cases; uncontrolled: untested against any wrong model (7.S19)
      Tolerant: cases; uncontrolled: untested against any wrong model (7.S19)
      Rejects: cases; uncontrolled: untested against any wrong model (7.S19)
      SchemaWellFormed: cases; uncontrolled: untested against any wrong model (7.S19)
      KindsKnown: cases; uncontrolled: untested against any wrong model (7.S19)
      CellsOfTheirKind: cases; controlled (refuted on its control at t = holeT)
      NoCellsOffSchema: cases; uncontrolled: untested against any wrong model (7.S19)
    tests/tester/tables_controls.lut: 0 laws, 1 controls, 1 lines ran, 0 known
      control of CellsOfTheirKind on holes (Listed): refuted at t = holeT: the control passed

## Findings

- The stores of the tables files predate the control kind. tables_laws.cert.json still holds the
  `Failed: t = holeT` entry of CellsOfTheirKind from when the control lived in that file; prune
  never drops it (its binding is another group), so with stores `check -v` reports the law
  "refuted at t = holeT" though no line of the file asks for it. tables_controls.cert.json holds
  the same refutation as an old-form `Failed` entry, which reads as no control ("no entry").
  Refreshing them means removing that entry and running `luthier certify` with stores; I left
  both, since rewriting evidence is not mine to decide.
- An entry whose line is no longer in its file keeps counting toward the certificate. That's the
  general form of the item above, and not in this brief.
- certification.lth's `Entry` and `Store` do not know the control kind; the Python is ahead of
  the theory there.

## Decisions taken on my own (each undone by one commit)

- `control` as a field with a default, not a form (test.lth, a92db27).
- The entry kind `"kind": "Control"` with outcomes `ControlRefuted` / `ControlConfirmed`; the kind
  is part of the identity and of the prune group.
- A control's entry goes only to the test file's store, never to a model's home.
- A law and its control are matched by the law's cone hash. Controls are read from the files
  given to `certify` or `check -v`, so a law certified without its control file reads
  uncontrolled.
- Any failed control at the current hash makes the status "CONTROL FAILED", even beside a refuted
  one; `certify` and `test` exit 1 on it.
- `certify --no-cert` added.
