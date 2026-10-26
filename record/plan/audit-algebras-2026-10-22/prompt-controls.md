# Brief: a refuted model for every uncontrolled conjunct (L9.14, D-2026-10-25-a q4)

Bite D1 (report-b1-b3-d1.md) made the unit of control the conjunct. Read over every store, 162
conjuncts across 56 laws have no refuted model; the list, with the reason per conjunct, is
`uncontrolled-2026-10-26.tsv` beside this file (file, law, conjunct, reason). L9.14: a law is
evidence of nothing until a wrong model refutes it; a theory is done when each conjunct has one.

Three agents, split by test program so they don't collide:
- Agent K (core): tests/tester/core_laws.test.lut's 98 conjuncts; controls in core_controls.test.lut.
- Agent M (machinery): bases (35), transformer (3), settling (4), lists (4); controls in their
  `*_controls.test.lut` files.
- Agent E (examples and arrays): arrays (7), docs/concepts/tape (4), tables (2),
  sonolocalizacion (2), numbers (2); controls in their controls files and tape.test.lut. Also:
  docs/concepts.md §6.3's printed certify output and §7.1's count of the tape's uncontrolled
  conjuncts, now stale (report-b1-b3-d1.md, "The tape example"); docs/spec/07-tests.md line 67,
  which still names `luthier test` options that don't exist (`--n`, `--exhaustive`, `--size`;
  12.S15 says what exists since a55ae64).

For each conjunct, by its reason: "held on every broken model": write a broken model that breaks
that conjunct and only it if you can (so the refutation says which property fails); "census
outside the domain": give the control a census inside the conjunct's domain (a related pair, a
chain); "no control line": add one; "vacuous": draw cases where the premise holds (generators.lth's
`equalOr`, report-wave-a-3b.md); "stuck match": find why and fix the model or the census. A
conjunct that no total broken model can refute (an axiom, an empty type's vacuous law) is listed
with its reason, not forced. Then run `luthier test` on your controls programs (not certify):
every new control refuted at the conjunct it targets. `luthier check -v` on your laws programs
shows the remaining uncontrolled conjuncts; list them in your report with why.

Read `CLAUDE.md`, report-b1-b3-d1.md, the tsv, and the theories the conjuncts belong to. Run with
`/home/lmoffatt/miniconda3/bin/python` and `/home/lmoffatt/miniconda3/bin/luthier`; scratch under
~/.cache/luthier-controls/<agent>/. Don't re-certify: the coordinator runs one wave after the three.
Touch only your programs (and, for E, the two docs); never git stash, checkout or reset other files.
Small commits staged by path: subject, blank line, one body line, ending with "Co-Authored-By:
Claude <model> <noreply@anthropic.com>". Report: `report-controls-<agent>.md` beside this file,
committed (if your Write is refused, give its full text in your final message): per law the
controls added, the conjuncts still uncontrolled with why, decisions taken on your own.
