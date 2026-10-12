# Brief: chapter 1, Terms and notation

Read `record/spec-briefs/common.md` and `record/spec-brief-template.md` first.

## Goal

Write `docs/spec/01-terms.md`, chapter 1 of the specification: the formal notation the other
chapters use, each symbol defined once, and the words of the language cited from the Terms of
`docs/principles.md`, defined nowhere here.

## Sources

The §0 "Notation" sections of `docs/spec/04-kernel.md`, `docs/spec/05-static-semantics.md`,
`docs/spec/06-numbers.md`, `docs/spec/08-tests.md` and `docs/rationale/09-extern-and-the-world.md`
(all at d12b554). They repeat each other; merge them so that each symbol appears once, with the
chapter that uses it most named beside it. `docs/principles.md` Terms for the words (structure,
predicate, cost, law, theory, model, function, dependences, certificate, grade, evaluation,
execution, demand, planner, declarative and executive face, object): cite, do not restate.

## What the chapter contains

- §1 The judgment and the acts: `x : T` (x refines T; for a value, x is a T), `x : T := t`,
  `x : T` alone (a hole), `x = t` (an alias), `U`.
- §2 Terms: `≡` (definitional equality), `t[a/x]`, `\ x { t }`, `(x : A) -> B`, `(x : A) * B`,
  the letters conventions (`A`, `B`, `T` types; `a`, `b`, `t`, `f`, `p` terms; `x`, `y`, `l`
  names), structural against nominal.
- §3 The dependency graph: `D(n)`, `B(n)`, occurrence in type position and in term position, the
  graph, a theory as a strongly connected component (write "theory", not "object", for the cycle,
  D-2026-10-12-z), a branch.
- §4 Numbers and measures used across chapters: `ℤ`, `ℚ`, `ℝ`, `u = 2^-53`, `x ⊕ y`, `A <: B`, `ε`,
  `κ`, `d`, `L`, `p`, `n`, `α`, `β`, `δ`, `ε̂`, `Φ`; the grades (cite Terms); `Cost` as the
  non-negative reals with infinity (cite `spec 5` for its algebra).
- §5 Tests and certificates: `Gen T`, size, seed, support, measure, binding, profile, census,
  reach (from 08 §0), each in one line, with `spec 7` as the chapter that defines their use.
- §6 Accept and reject programs: what `tests/spec/<name>.accept.lut` and `.reject.lut` are, the
  `-- expect:` comment of a reject (see `tests/test_spec.py`), and how a rule names them.
- `## Open`: cite O2 (the equality a type comes with) as the one open point that touches the
  notation; nothing else.

Every convention is a statement `**1.Sk. Title.** [implemented]` when the interpreter uses the
notation as described, `[proposed]` when it is new here (the merged conventions are not new;
marking them `[implemented]` is right when the sources were the specification of the running
interpreter). No rules (no `1.Rk`): nothing in this chapter is decided by a program.

## Length

About 900 to 1200 words. A table for §4 is fine.
