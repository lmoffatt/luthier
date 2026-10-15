# Two findings of criterion e: model homes, and a tester entry serving a first-action check

Read `CLAUDE.md`, `report-e.md` in this folder ("Findings" 1 and 2), then `src/luthier/tester.py`
(`model_homes`, `new_entry`), `src/luthier/run.py` (`FirstActions`, how a first-action demand is
served from a store), `src/luthier/certify.py` (`serves`, `covers_all`), and 10.S10.
1. `model_homes` takes a type alias (`State`, `Record`) or a constructor (`Sampled`) for a
   model and writes stray stores beside theory files: a home is a file defining a value whose
   type is a theory head bound in the line, never an alias or a constructor; a test with the
   two cases of the report.
2. A tester entry of listed cases bound to `host` would serve a run's first-action check of a
   `Host` law, so the run would skip gathering its own case (10.S10: the action is validated at
   its first application in the run). A first-action demand is served only by an entry written
   by a first-action validation (its kind, as controls have theirs), never by a tester's listed
   cases; a test where the tester's entry for `host` exists and the run still gathers its case.
3. The checker's 4.R9 refusal of a string literal at an imported alias `Hash` (accepted inside
   `List Hash`): fix if it is plainly the checker's, with a test, else say why.
Change tester.py, run.py, certify.py, check.py and their tests; the Python uncommitted. Report
with a shell heredoc to `report-findings-e.md` here, committed alone. Accepted when: the suite
passes; `luthier certify tests/tester/demand_laws.lut --no-cert` writes no store beside a theory.
