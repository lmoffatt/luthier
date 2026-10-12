# Brief: chapter 10, Actions and the world

Read `record/spec-brief-template.md`, then `record/spec-briefs/common-wave-3.md`. All three are
your whole task.

## Goal

Write `docs/spec/10-world.md`, chapter 10 of the specification: what an action is, the world it
acts on, externs as routes into the host and their validation, and what an action may change. It
realizes L4 (the part on actions) and L11.

## Sources

- `docs/principles.md`: L4 whole (definitions without effects; actions), L11 whole (an extern is a
  specimen certified by its laws; validated the first time an action asks), L10.6, O3.
- `record/decisions.md`: D-2026-10-10-c (no effects in definitions), D-2026-10-11-i (an action in
  a block with its result bound), D-2026-10-12-m (actions on Luthier's own state are idempotent and
  memoizable; on the world never), D-2026-10-12-ab (`extern` is an action since it opens a file),
  D-2026-10-12-ac (an extern is a route, read when a demand reaches it), D-2026-10-12-al.
- `docs/rationale/09-extern-and-the-world.md` (the rationale of externs and worlds; take what the
  principles and decisions confirm, mark the rest `[proposed]`).
- `git show bd4537e:docs/spec/05-static-semantics.md` R5 and R12, and `git show
  bd4537e:docs/spec/02-grammar.md` §9 (blocks). They now live in `docs/spec/04-static-semantics.md`
  (4.R5, 4.R12, 4.S24) and `docs/spec/02-grammar.md` §8: cite those, do not restate them.
- `docs/spec/03-kernel.md` 3.S13, 3.S18, 3.S22 to 3.S28, 3.S40 (extern, the bridge), and
  `docs/spec/12-files-and-tools.md` 12.S18 (`run --checked`): cite.
- `src/luthier/` (read only): which actions exist today (printing, writing `.run.json`, writing a
  certificate), how an extern is resolved and when (today at check time, against D-2026-10-12-ac).

## What the chapter states

- An action: what it is, where it may occur (blocks, `main`, the session), why a definition cannot
  hold one (D-2026-10-10-c), its result bound in a block (D-2026-10-11-i).
- The world: the token or value an action takes and gives. Its form is a library's
  (D-2026-10-12-al): state the interface the core asks of a world, in a table like spec 6.S5,
  `[proposed]`.
- Two kinds of action (D-2026-10-12-m): on Luthier's own state, idempotent and memoizable; on the
  world, never memoized.
- An extern as a route (D-2026-10-12-ac): declared type and route, read when a demand reaches it,
  its file's hash in the identity of what it produces; validated against its type's laws the first
  time an action asks, refused if it fails (L11.2); its certificate by hash; `provisional` (spec
  4.R5). What runs today `[implemented]`, including that the checker imports the module at check
  time, which D-2026-10-12-ac changes.
- `lib/world.lut` or the file that would state the theory of actions in Luthier (L14),
  `[proposed]`.

## Length

About 1200 words. `## Open`: O3 and any other O id the chapter rests on.
