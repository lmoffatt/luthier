# Brief: chapter 9, Specimens and the planner

Read `record/spec-brief-template.md`, then `record/spec-briefs/common-wave-3.md`. All three are
your whole task.

## Goal

Write `docs/spec/09-planner.md`, chapter 9 of the specification: one function with several
implementations (specimens), which of them may replace which, and how the planner chooses among
them for a demand. It realizes L6.

## Sources

- `docs/principles.md`: L6 whole (one function, many specimens), L9.8 and L9.9 (identity and its
  certificate), L10.7 and L10.8 (transport along identity, paths), L11.1 to L11.3 (an extern is a
  specimen), L14.3 (the host as a specimen of what Luthier states), O1, O4.
- `record/decisions.md`: D-2026-10-11-m (substitution only along a certified equivalence),
  D-2026-10-12-u (what is ranked), D-2026-10-12-q (paths), D-2026-10-10-e (in-place mutation as a
  choice of the plan), D-2026-10-12-al, -am.
- `git show bd4537e:docs/spec/04-kernel.md` §6 (primitive versus derived, native versus extern) and
  `git show bd4537e:docs/spec/05-static-semantics.md` R10 (a law characterizes; agreement of two
  implementations is a corollary). Both now live in `docs/spec/03-kernel.md` (3.S21 to 3.S28) and
  `docs/spec/04-static-semantics.md` (4.R10): cite those, do not restate them.
- `docs/spec/06-certification.md` §6 (transport along an identity and along a path): the planner's
  substitution is that transport; cite it.
- `src/luthier/` (read only): whether anything chooses between implementations today (a native
  definition and an extern of one name, `array_python.lut` against `array.lut`). Most of the
  chapter will be `[decided]` or `[proposed]`.

## What the chapter states

- A specimen: an implementation of a function, native or extern or another library's, each a
  model certified against the function's laws (L9.2, spec 4.R10).
- The class of a function: the specimens connected by certified identities (D-2026-10-11-m); a
  specimen alone is never replaced.
- Substitution: the planner replaces A by B only along a certified path, and what A's result
  then carries is spec 6.S11 and 6.S12; whether the demand accepts it is its cutoff.
- What the planner ranks is a library's (D-2026-10-12-al): state the interface the core asks of a
  ranking, in a table like spec 6.S5, `[proposed]`, with D-2026-10-12-u's formula as the first
  candidate model, not as the rule. The resources measured (time, memory) and where they are
  recorded.
- `lib/planner.lut` or the file that would state the planner's theory in Luthier (L14),
  `[proposed]`.

## Length

About 1200 words. `## Open`: O1, O4 and any other O id the chapter rests on.
