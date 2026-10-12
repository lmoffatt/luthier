# Common part of every wave 1 brief

Read `record/spec-brief-template.md` first: it gives the shape of a chapter, the statuses, the
citation forms, what not to touch, the check and the report. This file adds what every chapter of
wave 1 shares; your chapter's own brief, `record/spec-briefs/NN-<name>.md`, adds the rest. All
three together are your whole task. You work at commit d12b554 of the repository, in your own
worktree; you write exactly one file under `docs/spec/`.

## Reading order

1. `record/spec-brief-template.md`.
2. `docs/spec/00-index.md` (the twelve chapters, the status legend, the citation form).
3. `docs/principles.md`: Terms, G0 to G2, and the entries your brief names. It is the authority;
   where a source disagrees with it, the principles win and you report the disagreement.
4. Your sources, named in your brief with their paths; they are at commit d12b554 in the worktree.
5. `tests/spec/` for the names of the programs a rule may cite (read `tests/spec/README.md` if
   present). You may read `src/luthier/*.py` to decide whether a rule is `[implemented]`; never
   edit it.

## Decisions in force for every chapter

Cite them by id where a rule rests on them.

- D-2026-10-12-y: the specification is a directory of chapters with a status per rule; its Terms
  are the principles'; the grades are the five of Terms (proved, exhaustive, cases, sampled,
  assumed), with the domain and the evidence cost carrying what the older grades said (point is
  cases with one case; census of k is cases; bounded is exhaustive on the box the domain names;
  witnessed is cases with a witness); the rounding correction stays reversible and proposed; `run`
  is strict from the start, no opt-out, a cone with an uncertified or provisional name is refused;
  the content of the libraries is the manual's, not the spec's.
- D-2026-10-12-x: principle L14, what can be written in Luthier is written in Luthier; `Program`
  and `Term` as data enter version 0. Where a chapter's rules can be stated as a theory in Luthier,
  name the `.lut` file that states or would state them, and mark `[proposed]` what is not written.
- D-2026-10-12-z: the term *object* is anything a name defines (a theory, a function, a datum);
  a *theory* is the object several names define together, a cycle of the dependency graph, the
  one-symbol function type included. Where a source says "object" for the cycle, write "theory".
- D-2026-10-12-l: vocabulary: *structure* for a kernel type, *theory* for a Luthier type, *cost*
  for the value of a law and *resources* for time and memory, *model* for what a type names and
  *specimen* for the planner's candidates (an implementation among several).
- D-2026-10-12-r: a sample's statistics convert to an evidence cost by a function declared per
  theory; the first instance is −log(1 − ε̂(n, δ)) in nats, with ε̂ the bound on the failure
  fraction from n samples at confidence 1 − δ, and δ the demand's parameter.
- D-2026-10-12-h: the cutoff (tolerance) is a parameter of the demand, not of a constructor or a
  law.
- D-2026-10-12-t: an `assumed` certificate carries what is asserted, a Boolean law asserted true
  or a cost law asserted with a formula of the inputs; its evidence cost is the demand's parameter.
- D-2026-10-11-n: certification is the default (every certificate of the dependency cone is
  demanded when a value is); its opt-out part is reversed by D-2026-10-12-y.

## What goes where (so that chapters do not overlap)

Chapter 1 notation; 2 grammar and the translation of sugar; 3 the kernel (formers, terms,
reduction, the bridge with the host, `Term` and `Program` as data); 4 the checker's rules; 5 laws
(predicate and cost, how they combine, `Cost`); 6 certification (what a certificate records, its
identity, transport, certification by default); 7 tests and generators; 8 the demand and the plan
(evaluation strategy, memo, identity of a result, the session); 9 specimens and the planner; 10
actions and the world (blocks' actions, externs' validation, worlds); 11 numbers; 12 files and
tools (what a file is, import, what travels, the commands). Chapters 5, 6, 8, 9, 10 are not
written yet: cite them as `spec 6` and so on where your text needs them; the check reports such a
citation as information, not as a finding.

## The check

`scripts/check_spec.py` is being written in parallel and may not exist in your worktree. If it
exists, run it on your file and make it pass. If it does not, apply its rules by hand (every item
has a status; implemented rules name existing accept and reject files; every citation resolves;
no run of eight words copied from another document; `## Open` last) and say in your report that
the check did not run.

## Status statuses, when in doubt

A rule the interpreter enforces today and that has its two programs: `[implemented]`. A rule a
source says is decided but whose decision id you cannot find in `record/decisions.md`:
`[proposed]`, and list it in your report under "decided without an id" with the source's date, so
that the integrator assigns the id. Anything you add: `[proposed]`.
