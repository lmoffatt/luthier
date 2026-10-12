# Common part of every wave 3 brief

Written 2026-10-13 for chapters 8, 9 and 10. Read `record/spec-brief-template.md` first: it gives
the shape of a chapter, the statuses, the citation forms, what not to touch, the check and the
report. This file replaces `common.md` (wave 1) for wave 3; your chapter's own brief,
`record/spec-briefs/NN-<name>.md`, adds the rest. You work in your own worktree at the commit that
holds this file; you write exactly one file under `docs/spec/`.

## Reading order

1. `record/spec-brief-template.md`.
2. `docs/spec/00-index.md`.
3. `docs/principles.md`: Terms, G0 to G2, and the entries your brief names. It is the authority;
   where a source disagrees with it, the principles win and you report the disagreement.
4. `docs/spec/06-certification.md` whole: it is the model of a wave 3 chapter. It states what the
   core asks of a library and leaves the rest to the library (its 6.S4 and 6.S5).
5. Your sources, named in your brief. Old files are read with `git show bd4537e:<path>`.
6. `tests/spec/` for the names of programs a rule may cite. You may read `src/luthier/*.py` to
   decide whether something is `[implemented]`; never edit it.

## The rule of wave 3 (D-2026-10-12-al)

`Cost` is a library, and so are the open questions of wave 3: the form of the demand, the world's
token, what the planner ranks, the trace. Their invariants are found when the libraries are
implemented. A wave 3 chapter therefore does two things: it states what is decided or implemented,
with its status, and, for each such question, it states the *interface the core asks of the
library*: the fewest operations and laws the core uses, in a table like 6.S5, marked `[proposed]`.
It does not choose the library's algebra, names or representation. Ask for less rather than more:
an interface is what a library can never change later (P16: between designs that satisfy what is
required today, the one cheaper to revise tomorrow).

## Decisions in force

Cite them by id where a statement rests on them. Read the entries in `record/decisions.md` when you
need more than this line.

- D-2026-10-12-y: chapters with a status per rule; grades are the five of Terms; `run` strict, no
  opt-out; the libraries' content is the manual's.
- D-2026-10-12-x: L14, what can be written in Luthier is written in Luthier; `Program` and `Term`
  are data. Name the `.lut` file that would state a chapter's theory, `[proposed]` if not written.
- D-2026-10-12-aj: a *theory* is a type with its law, in one name or several; the number of names
  is its presentation. D-2026-10-12-ak: an *object* is a type with its equality (the base theory, a
  setoid); a kernel type with no equality is a *structure*.
- D-2026-10-12-l: *specimen* for the planner's candidates, *model* for what a type names,
  *resources* for time and memory, *cost* for the value of a law.
- D-2026-10-12-al and -am: `Cost` is a library; certification asks of it `≤`, `0`, `⊤`, `⊕`,
  `lift` (spec 6.S5). Use the same `C` and the same five when your chapter needs costs; ask for
  more only if your chapter cannot do without it, and say so in the report.
- D-2026-10-12-h: the cutoff is a parameter of the demand. D-2026-10-12-r: δ, the confidence, is
  the demand's parameter too.
- D-2026-10-11-n with D-2026-10-12-y: demanding a value demands every certificate in its cone; no
  opt-out at the start (O3).
- D-2026-10-10-c: a definition has no effects; effects live only in actions.
- D-2026-10-10-d: forward on demand; the evaluation strategy is a parameter separate from the
  program.
- D-2026-10-10-e: a mutable parameter is two variables, before and after; in-place mutation is an
  optimization when the before has no other consumer.
- D-2026-10-11-i: blocks; `:=` once, `<-` bind or rebind, an action with its result bound.
- D-2026-10-11-m: the planner substitutes one implementation for another only along a certified
  equivalence (spec 6.S11).
- D-2026-10-12-u: what the planner ranks, a candidate: cost + w·log resources, minimized.
- D-2026-10-12-m: actions on Luthier's own state (a certificate, a test) are idempotent and
  memoizable; actions on the world never are.
- D-2026-10-12-ab: keywords are `data`, `match`, `if`, `then`, `else`, `U` (maybe `operator`); the
  rest are names of core or of a library; `extern` is an action since it opens a file.
- D-2026-10-12-ac and -ad: a file is read when a demand needs it; an extern is a route, read when a
  demand reaches it; import is lazy; `test` of a module is the total demand.

## What goes where

1 notation; 2 grammar; 3 kernel (formers, reduction, the bridge with the host, terms as data); 4
the checker's rules; 5 laws (predicate and cost, how they combine), being written now by the
integrating session; 6 certification, written; 7 tests and generators; 8 the demand and the plan
(what a demand is, the evaluation strategy, the plan, the memo and the identity of a result, the
session's semantics); 9 specimens and the planner (several implementations of one function, the
class connected by certified equivalences, substitution, what is ranked); 10 actions and the world
(actions in blocks, the world, externs as routes and their validation, what an action may change,
idempotence); 11 numbers; 12 files and tools (files, import, the commands). Cite another chapter
rather than restating it; the check rejects any run of eight words shared with another chapter or
with `docs/principles.md`. Chapters 8, 9 and 10 are written at the same time by three agents: cite
each other as `spec 8`, `spec 9`, `spec 10` without section numbers.
