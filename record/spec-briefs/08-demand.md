# Brief: chapter 8, The demand and the plan

Read `record/spec-brief-template.md`, then `record/spec-briefs/common-wave-3.md`. All three are
your whole task.

## Goal

Write `docs/spec/08-demand.md`, chapter 8 of the specification: what a demand is, how the demand
determines what is computed, the plan, the memo and the identity of a result, and the session. It
realizes L5. There is no old spec file for it: its sources are the principles, the decisions and
what the interpreter does.

## Sources

- `docs/principles.md`: L5 whole (the demand), L4 (a program is a DAG of definitions; actions),
  L10.5 and L10.6 (a certificate serves a demand; certification by default), L12.3 (the cutoff is
  the demand's), O5, O8, O12.
- `record/decisions.md`: D-2026-10-10-c, -d, -e; D-2026-10-11-i, -n; D-2026-10-12-h, -m, -r, -ac,
  -ad, -al.
- `docs/spec/02-grammar.md` §8 (blocks and the session, as grammar), `docs/spec/12-files-and-tools.md`
  (12.S17 to 12.S21: `run`, `eval`, `session`, when a file is read), `docs/spec/06-certification.md`
  §7. Cite them; do not restate them.
- `src/luthier/` (read only): how `run`, `eval` and `session` evaluate today (`cli.py`,
  `evaluator.py` or the machine it uses, `session.py` if present), whether there is a memo, and
  what `.run.json` records. Mark what runs `[implemented]` and say "today" for the rest.

## What the chapter states

- What a demand is, as a value: its entry (a name or a term), its cutoff (a bound and an evidence
  cost, spec 6), its δ, its cost of assumptions (spec 6.S10, no default), its resources if any.
  The *form* of the demand is a library's (D-2026-10-12-al): state the interface the core asks of
  a demand, in a table like spec 6.S5, `[proposed]`.
- Forward on demand (D-2026-10-10-d): the plan backward from the demand over names, nothing
  evaluated before it is needed; the strategy a parameter separate from the program (P11). What
  the interpreter does today (it evaluates `main` eagerly, or as it does) `[implemented]`.
- No effects in definitions (D-2026-10-10-c); mutation as before and after, in place only as an
  optimization of the plan (D-2026-10-10-e).
- Files read on demand (cite spec 12 for the rule; state here that the checker is a demand for
  names and types and `run`/`test` demands for values, D-2026-10-12-ac, -ad).
- The memo and the identity of a result (O12): a result identified by the hash of its cone and its
  inputs; a memo hit serves a demand only if it meets that demand's cutoff (L10.5). `plan.lut` as
  the carrier of the plan in Luthier (L14), `[proposed]` if not written.
- The session (O8): a block over the dataflow, `<-` to explore and `:=` to lock; what a line
  re-evaluates; the memo between items. Cite spec 2 for its grammar.
- The trace, if L5 names one: an interface for a library, `[proposed]`.

## Length

About 1500 words. `## Open`: O5, O8, O12 and any other O id the chapter rests on.
