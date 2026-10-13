# Reply to the review of layers 0 and 1

2026-10-13, by Claude Opus 5.5, after summary.md and Luciano's answers to its seven questions
(D-2026-10-13-aa). Each finding marked "mine to fix" in summary.md, and each answered question, with
the commit that addresses it. Every library file parses at ba322cd.

## The kernel (A)

| finding | commit |
|---|---|
| Alpha not pinned down (Fable): `AlphaPartsAgree`, `RenameBound` for every binder | cc2542d |
| A `data`'s name compared as a binder; pattern variables renamed at once (kernel Codex) | 23d23f4 |
| Fuel read as agreement (GPT, DeepSeek, Fable): an exact `step`, `reduce` its iteration | 2409c59 |
| No strategy (Fable): `HeadFirst`; holes and stuck matches; iota on constants, variables, both orders of a pair; prim on `Primitive` bodies over `Int`, `Float64`, `String`; `Datum` inert | 2409c59 |
| `Delta` on a bare name, found wherever defined; always in head position (Q7) | 2409c59, fe3bdab |
| Substitution for every constructor, and the capture case | fe3bdab |
| `Let`, a local definition (Q1): data, alpha, substitution, `Zeta`; blocks elaborate to it; typed transparently | fe3bdab, b9c9e08 |
| `Axiom` carries its string (3.S2) | 048cd55 |
| Structural equality over `Concrete` types, each object law apart; `Lists` (nil neutral, cons the injection combined) in place of `ListAlgebra`; `TheBooleans` (true where `if` takes its first branch); names of products and coproducts tied to their arrows | 2beeb05 |
| `unqualify` removes a prefix; `eval` computes on quantified terms | 1c521a7 |
| Chapter 3 up to the files (Q2): 3.R1, 3.S29, 3.S33, 3.S36, 3.S38 | ae796ab |
| The model: `stepper`, holes not read as misses or constructors, linear patterns, `Let`, `Axiom`, every law of §2 to §5 checked by hand (Codex) | 04c9269, b1582ca |

Not done, by design: an applied extern's call to the host (3.S18) stays the specimen's and spec
10's; `canonical`'s string functions stay holes until spec 11 names them.

## The checker (B)

| finding | commit |
|---|---|
| Name resolution: dotted names by their prefix, constructors known, binders, parameters and fields in scope after them, `rebind` binds, `sigmaNamed`'s second name a label | e664bae |
| 4.R4 a whitelist through a separate declaration; 4.R5 with the type defined; 4.R6 under the theory's parameters; 4.R8 constructor arguments and declared bases; 4.R9 on bases (refinements are obligations); `bodyApplications` binds its alpha | b793113 |
| `ReportsExactly` vacuous: two laws per rule over violating and clean programs, the sound direction only where a predicate is partial; 4.S14 a report | e52b295 |
| `Typing`: terms that type by construction, global names, untypable applications, introductions and formers, `Let`, `same` and `refines` non-trivial, 4.R11 on any condition | 3520298 |
| 4.R3: laws as what a theory's conjunction claims, fields of a theory declared apart, lambda predicates, patterns that bind nothing (rejects, Q3); 4.R12 inside blocks | ba322cd |
| Translation: qualified names, `-x` on `Float64`, clauses over two parameters, an action in a block, an alias with binders, declared contexts, constructor types as arrows | 5d7963b |

Open: the generators of programs per rule (well-formed programs from a small pool of names,
mutated by one edit aimed at the rule, with tests/spec/ as a census) belong to the certifier (step 5)
and are named in program.lth as the domains' generators.

## Laws, checks, the library (C)

| finding | commit |
|---|---|
| Theories with one model become definitions with characterizing laws (Q5): `checks.lth` (`Check`, with `BothIsAnd`, `EitherIsOr`, `ChainStopsAtFirst`, `BoolIsACheck`), `laws.lth` verdicts with `VerdictsAreExact`; `checks_model.lut` removed | c495404 |
| `Settling` compositional: a forall refuted exactly by a counterexample, points with their coverage, an exists confirmed by a witness, evidence that cannot lie, `Not` and `Then` material, the combination of verdicts the demand's under commutative and absorbing laws | ef38a8b |
| The loader: exact visibility and reads, the theory's fields only, checking against running, the model verified on first demand, kinds on several paths, a theory file rejects an extern | cba732a |

Kept as decided: `Law` Boolean until the cost library (Q6); `U : U` in version 0 (Q4, 3.S8).
