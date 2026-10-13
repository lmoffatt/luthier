# term_model.lut, constructors of a data: brief for Codex

Written 2026-10-13 by Claude Opus 5.5, run from the session.

## The prompt

Read `CLAUDE.md` first: its working rules bind you too. `src/luthier/lib/term.lth` gained the law
`IotaConstructors` at 66d5cae (`git show 66d5cae -- src/luthier/lib/term.lth`): a match on a
constructor of a `data` the program defines (a `Define t ty (Data t cs)`, its constructors the
keys of `cs`), alone or applied, takes that constructor's arm and passes over the arms of the
data's other constructors. Your report (record/IA/term-2026-10-13/codex.md) says the model treats
an unresolved bare `Var` as never a nullary constructor; with this law, a name that is a
constructor of a `data` of the program is a constructor, nullary or applied, and two distinct
constructors of one `data` do not match.

Update `src/luthier/lib/term_model.lut` so that `stepper` meets `IotaConstructors` and every other
law of term.lth §5 as now stated (a name the program declares or defines as an act stays what it
was: a hole, or unfolded by `Delta`). Check by hand, parse with
`PYTHONPATH=src python3 -m luthier.cli parse src/luthier/lib/term_model.lut`. Touch nothing but
term_model.lut and your report; another Codex works in this tree. Do not commit. Append a section
"Constructors" to the report.
