# Brief: chapter 3, The kernel

Read `record/spec-briefs/common.md` and `record/spec-brief-template.md` first.

## Goal

Write `docs/spec/03-kernel.md`, chapter 3 of the specification: the constructs every program
reduces to, how each computes, the bridge with the host, and `Term` and `Program` as data. The
old file `docs/spec/04-kernel.md` is your main source and stays in place; the integrator deletes
it.

## Sources

- `docs/spec/04-kernel.md` at d12b554: §0 (cite `spec 1` instead of restating), §1 acts, §2 type
  formers, §3 terms, §4 reduction, §6 primitive versus derived and the four bridge rules. §5 (the
  translations) goes to chapter 2: cite `spec 2` for it and do not copy the table. §7 (status of
  the interpreter) is not part of a chapter: drop it and say so in your report; the statuses on
  each item carry that information now.
- `docs/principles.md`: L7 (the core is minimal, executable by hand, programs are data), L14
  (what can be written in Luthier is written in Luthier), L2 (holes), L3 (equality has levels).
- `src/luthier/syntax.py`, `evaluator.py`, `machine.py` (read only) to decide what is
  `[implemented]`; `src/luthier/lib/kernel_laws.lut` and `src/luthier/core.lut` for what the
  kernel already states in Luthier.
- The chat decision of 2026-10-12 (D-2026-10-12-x): `Program` and `Term` as data enter version
  0. Four choices were proposed by the model and are not decided; write each `[proposed]`:
  1. `Term` is the kernel term after elaboration (the sugar of `spec 2` translated away), not the
     surface term; the certificates' hashes are computed over it.
  2. Names are strings, with α-equivalence as a law (two terms equal up to the renaming of bound
     variables), not de Bruijn indices.
  3. `quote { t }` gives the `Term` of a term with no obligation; `eval A t : Maybe A` checks the
     term against `A` at evaluation time and gives nothing when it does not check.
  4. The reduction rules (beta, delta, iota, prim, extern) are stated as a function
     `reduce : Term -> Term` in `lib/term.lut`, the interpreter written in Luthier, certified
     against the host's evaluator as two specimens of one theory (L14.3); it is not written yet.

## What the chapter contains

- §1 Acts (from 04 §1, with `primitive` and `axiom` bodies cited from `spec 11`; directives listed
  with the chapter that specifies each: `import` `spec 12`, `test` `spec 7`, `operator` `spec 4`,
  `cite` `spec 6`, `profile` `spec 7`).
- §2 Type formers: the table and its notes, as statements with status; the kernel named as a
  bicartesian closed category with dependent product and exponential, recursive types and
  subtypes. Use "structure" for a kernel type where the source says "type" in that sense
  (D-2026-10-12-l) and keep "type" where it means any type.
- §3 Terms: names, `match`, recursion and the recursor, laws (cite `spec 5` for what a law is;
  keep here only that a law is a term of type `Bool`, `Cost` or `Law`), extern (cite `spec 10`
  for its validation).
- §4 Reduction: the five rules as statements, each with the kernel's existing tests
  (`k_*.accept.lut` files in `tests/spec/`: name the ones that exercise each rule; do not invent).
- §5 Primitive versus derived, native versus extern: the two senses, the four bridge rules
  (statements, `[implemented]`), the order of a sum as part of its rounding, the `Agrees` laws
  with the pointer to `spec 9` (two specimens of one theory) and `spec 4` R10.
- §6 Programs as data: `Term`, `Pattern`, `Act`, `Program` as `data` in `core.lut` with the
  constructors of §2 and §3 (list them: Var, Lit, U, Lam, App, Pi, Sigma, Pair, Match, Inj, Sum,
  Data, Subtype, Extern, Primitive, Axiom, Hole; and for Program the acts), `[decided
  D-2026-10-12-x]`; the four proposed choices above; the canonical form (bound variables renamed
  canonically, module prefix removed) as the form the hashes of `spec 6` are computed over; no
  self-hacking: a `Program` value is data, defining is an action (cite L7.4 and `spec 10`).
- §7 The kernel's theory in Luthier: `lib/kernel_laws.lut` as the theory the host is certified
  against today (what it states, what it cannot: eta, cite O11), and `lib/term.lut` as the one to
  write (`[proposed]`).
- `## Open`: O11; and the four proposed choices named by their statement numbers.

## Length

About 3000 words. Tables are welcome for §2 and §6.
