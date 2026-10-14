# demand.lth and plan.lth: the demand and the plan as values, brief for a Fable agent

Written 2026-10-15 by the coordinating session (luthier-3e). Step 6.1 of
`record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md`: the theories of layer 3
that remain, demand.lth (8.S1, 8.S2) and plan.lth (8.S4, 8.S8, 8.S11), then the external review
of layer 3 (not this bite). D-2026-10-14-c: every law Boolean, the cutoffs as parameters the
demand supplies: the demand is where those parameters live.

## The prompt

Read `CLAUDE.md` first, then `docs/principles.md` (L5 whole, L12.3, P11), `docs/spec/08-demand.md`
whole (8.S1 to 8.S11 and its table; what is `[decided]` you state, what is `[proposed]`, the
decorated demand's generic form, you leave as a hole with the item cited), `docs/spec/06-
certification.md` 6.S14, 6.S15, `12-files-and-tools.md` 12.S18, 12.S17, and the theories this one
builds on: `src/luthier/lib/certification.lth` §3 (`Demand` as it stands there: the law, the
hash, the values per parameter, `accepts`; `Certified`, `refuse`), `test.lth` §1 (`TestSpec` and
its budgets), `generators.lth` at `Budgets`, `Level`, `world.lth` §2 (`Described`, `own`), and
what the specimen does today: `src/luthier/run.py` at `run`, `holes`, `fill`, `certification`,
`record` (`record/IA/run-2026-10-13/report-7.md`, `report-11.md`,
`record/IA/certification-2026-10-14/report-run.md`): the demand as `run` builds it (the entry,
the `--set` values, `--accept`, `--fuel`, `--checked`, the lock). Pattern: the theories named,
each law citing its item above it. Nobody else edits now: write `src/luthier/lib/demand.lth`,
`demand_model.lut`, `plan.lth`, `plan_model.lut`, one commit each (`git add` its path; never `-A`
or `.`; no `git stash` or `git checkout`), messages naming the items, ending with
"Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"; certification.lth §3's `Demand`
you may move into demand.lth and import back (one commit of certification.lth, saying so).

1. demand.lth: the demand as a value (8.S1): the entry, the type demanded (the identity for
   now, the decorated form `P T` a hole with 8.S1's `[proposed]` cited), the cutoff (the
   weakest grade accepted, 6.S15), the bound and the evidence cost as holes `C`
   (D-2026-10-13-m), the confidence for sampled evidence, the evidence cost of assumptions
   (no default, 6.S10), the resource limits (the fuel, as `run --fuel`), the values of the
   program's holes (`--set`, 12.S18), `--checked`, the lock; the first demand of all with its
   declared defaults recorded (L5.19); a demand inside another passed down, not recomputed
   (L12.3). Laws: what a demand determines (the same demand on the same cone gives the same
   result: the identity of 8.S3, 12.S18's record), what it records (every cutoff it carries,
   L5.18), that a demand with no cutoff for assumptions refuses every assumed value (6.S10),
   that lowering the cutoff loses nothing accepted (certification.lth's `ServesIsMonotoneInTheCutoff`,
   imported, not restated). The model: `theDemand` built from the arguments `run` takes, with
   the defaults of 8.S1's table as a record of parameters.
2. plan.lth: the plan as a value (8.S4, 8.S8, 8.S11, D-2026-10-13-g): the dataflow of a cone (the
   names, what each reads), a schedule (a linearization), the memo key (what the cone reads: the
   hash of the cone and the demand's values, 8.S3, 8.S8), the law `Confluent` (any two
   linearizations of one dataflow give the same result, D-2026-10-13-g), what a plan computes
   against the run (the live subgraph the entry reaches, 8.S4's call by need as the default
   strategy, a parameter), and the backward pass as a hole with the item cited. The model: the
   default plan (call by need, as run.py does) stated over a small dataflow; the memo across
   runs (8.S10 says it does not exist: state its key, no model).
3. Both must parse (`PYTHONPATH=src python3 -m luthier.cli parse`) and `luthier check` clean
   (report what it refuses if not yours). Mark `[proposed]` every reading the spec leaves open,
   with the item above it. Report to `record/IA/demand-2026-10-15/report.md` (commit it): what is
   stated, every `[proposed]`, and what run.py must change to build its demand as the theory
   says (one line per law).
