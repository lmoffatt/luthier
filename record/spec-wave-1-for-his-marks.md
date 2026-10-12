# Wave 1 of the specification: what waits for your marks

Draft 0, 2026-10-12, at c3ab37f. Step 2 of `record/plan-spec-2026-10-12-execution.md`. The seven
chapters of wave 1 are in `docs/spec/` (1, 2, 3, 4, 7, 11, 12). Every item still marked `[proposed]`
is here, one line each, with the questions the agents who wrote the chapters left
(`record/spec-drafts.md`). One section per chapter, each meant to fit a screen.

How to mark: write under a line, as in your feedback files. "ok" moves the item to `[decided]` with
a new entry in `record/decisions.md`; "no" or a comment sends it back; a line you leave unmarked stays
`[proposed]`, which costs nothing until a chapter of wave 2 or 3 needs it. Where I have a reading I
say so after "Mine:"; it's a proposal like the rest.

Done before this document, without you, so that you mark less. Six decisions of 2026-10-05 and
2026-10-06 that the agents found without an id now have one, with their quotes:
D-2026-10-05-a (a law characterizes; a second implementation is not a law), -b (`check -v` reports
"consistent, not characterized"), -c (`toFloat64` stays `Int -> Float64`), D-2026-10-06-aa (a
condition refines its variable inside its branch), -ab (your answers on generators and
certificates) and -ac (the test grammar written for them, its syntax since replaced by
D-2026-10-12-ab, `test` a function with named arguments). The items that rest on them are now
`[decided]`: 2.S19, 4.R10, 4.R11, 4.S20 and sixteen of chapter 7. Chapter 7 also marks as
`[implemented]` what already runs (`with n`, `exhaustive`, `size`, the filter of a subtype, the
order of dependent components, the reuse of a passed certificate), checked against the code.

## Chapter 1. Terms and notation

- 1.S11, the table of symbols shared by all chapters: ε the demand's cutoff, d a distance, κ a
  condition number, L a Lipschitz constant, p a predicate (or, in a statistical law, a
  probability), n the cases or samples, α the level, β the power, δ the confidence parameter,
  ε̂ the bound on the failure fraction, Φ the normal distribution function. The meanings of L and
  p are the agent's guesses.
- A collision the table brings out: 11.S16 uses δ(x) for the additive defect of rounding, while
  1.S11 and 7.S11 use δ for the confidence parameter. Mine: rename the defect η(x) in 11.S16.
- Question of the agent: 1.S12 reads the old grades (point, census of k, bounded, witnessed and the
  rest) through the five of the Terms (proved, exhaustive, cases, sampled, assumed). Is that
  correspondence chapter 1's or chapter 6's (certification, wave 2)? Mine: chapter 6's once it is
  written; it stays in 1 until then.

this question will be solved when we determine the laws of the certification in luthier terms. 
When these laws are formulated, then we will backdetermine the principles. 


## Chapter 2. Grammar

- 2.S20, quote and unquote, one candidate syntax: `quote { t }` gives the term `t` as a value of
  `Term`, and `eval A t` its value at type `A`. The syntax only; what they mean is 3.S32.
- The two questions of the agent are answered by D-2026-10-12-ab (`test` a function with named
  arguments; `primitive` and `axiom` names of core): the metric after `sampled` becomes the value of
  a named argument, and the primitive and axiom bodies of 2.S5 are applications of core's names.
  Nothing to mark.
ok


## Chapter 3. Kernel

The four choices on terms as data (D-2026-10-12-x made `Term` and `Program` data; these say which
data):

- 3.S30, `Term` is the kernel term after elaboration, with the sugar of chapter 2 gone; the hashes
  of certificates are computed over it.
- 3.S31, names are strings, and alpha-equivalence (equal up to renaming bound variables) is a law
  of the theory of `Term`, not a property of de Bruijn indices.
- 3.S32, `quote { t }` gives the `Term` of `t` with no obligation; `eval A t : Maybe A` checks `t`
  against `A` when it is evaluated and gives `nothing` when it does not check.
- 3.S33, the reduction rules (beta, delta, iota, prim, extern) as a function `reduce : Term -> Term`
  in `lib/term.lut`: the interpreter written in Luthier, certified against the host's evaluator as
  two specimens of one theory.
- 3.S34, a canonical form that renames bound variables and drops module prefixes, so that moving a
  definition to another module keeps its hash.
- 3.S38, `lib/term.lut` holds that theory: the data, alpha-equivalence, the canonical form,
  substitution and `reduce`.
- 3.S29, the constructors of `Pattern` and the fields of `Act`, which D-2026-10-12-x left open.
- 3.S11, version 0 has general recursion under a step budget, and no proof layer with a primitive
  recursor.
- Question of the agent: the rules of evaluation (beta, delta, iota, prim) are marked
  `[implemented]`, yet the programs of `tests/spec/` are only checked, never evaluated. Should an
  evaluation rule need a program whose value is compared before it counts as implemented? Mine:
  yes, one program per rule with its expected value; it is the first real case for that check.
- Wave 2, not now: whether a law may be a term of `Cost` (3.S12) and whether `Failures E` stays a
  law type are chapter 5's. Whether the kernel is described as a theory is O11 (the kernel's
  theory stated in Luthier), open as before.
ok

## Chapter 4. Static semantics

- 4.S16, the semantic criterion of dependence as laws a test can check: `f` depends on `y` when some
  `x, y, y'` give different results; a law connects `x` and `y` when it is not a conjunction of a
  law on each. Both are existential, so a test looks for a witness and certifies with the grade
  cases.
- 4.S21, rules 4.R1 to 4.R13 as the laws of a theory `WellFormed : Program -> Failures E` in
  `lib/program.lut`, each rule a law and its accept and reject programs its cases. Until then the
  checker is the specimen and the suite its certificate.
- Question of the agent: 4.S9 tells two kinds of definition by their form, a concrete type (built
  by constructors, observed by eliminators) and a theory (a subtype of a labeled base whose values
  are its models). D-2026-10-12-z defines a theory as a cycle of the dependency graph instead. Do
  the two kinds stay, or does 4.S9 restate them in the terms of -z? Mine: restate; the cycle is the
  criterion you chose, and form becomes how the checker finds it.

  my proposal: 
  Object is one of concrete type, subtype (law involving a single name)  o theory type (law involving more than a name)


## Chapter 7. Tests and generators

Your decisions of 2026-10-06 cover the chapter's frame; what follows are the model's parts.

- 7.S2, sampling inverts a cumulative weight: one rule draws from a list and from an interval. It
  is your idea (cumsum of a cost), which you left as "estoy evaluando". Decide it, or keep it open?
- 7.S3, the table of how `exhaustive` and `sampled` follow each form of type (finite types, numbers
  with and without bounds, products, sums, lists, functions, theories, subtypes, `U`).
- 7.S1, a generator that claims a distribution states it as a law, certified with its own count of
  draws.
- 7.R3, when the product of finite parameters exceeds a budget, `exhaustive` takes a covering array
  of pairs (every pair of values of any two parameters) and the grade says so.
- 7.S4, `linear` for quantities whose meaning survives a shift (coordinates, residuals), `log` for
  those that survive a scaling (standard deviations, distances, tolerances); 0 as an atom of `log`
  with a probability that is an argument; special values (bounds, 0, ±1, the program's literals)
  added to every numeric generator.
- 7.R4, a census may hold families (`from f`, its arguments drawn), it is always explicit (an
  implicit census would change a certificate's meaning when an unrelated definition is added), and
  random functions come later.
- 7.S6, an interval predicate gives bounds and no rejection; any other predicate is a filter whose
  acceptance rate is recorded; a subtype a filter rarely reaches is defined constructively.
- 7.S12, `n` counts cases evaluated to a verdict; draws that failed, cases that raised and false
  premises are counted apart, and a vacuous pass is reported as such.
- 7.S14, labels and coverage: a law labels its cases (`classify`) and can require a share
  (`cover`), checked with a sequential Wilson bound, as QuickCheck's `checkCoverage`.
- Question of the agent: the source's "cost" of sampling is renamed "weight", because the Terms
  keep cost for the value of a law. Mine: ok.
- Question of the agent: grades (7.S10) and the evidence cost (7.S11) as two items. Mine: keep two;
  both are decided and chapter 6 will hold them.

ok

## Chapter 11. Numbers

- 11.S3, a definition meant for every realization is generic in its number type, through a hole
  `num : NumberModel` that the importing file fills (`num := float64`); `lib/number_model.lut`, not
  written.
- 11.S5, the rounding of a `Real` into `Float64` waits for a `Real` that computes; until then no
  law over `Real` is tested.
- 11.S10, intervals and balls, which enclose the true real: an approximation certified by "the
  double lies in the interval", comparisons answered with a probability. Waits on O1 (the algebra
  of costs) and O5 (the decorated output).
- 11.S11, what randomness is, as laws on the distribution of a generator's output, moves to
  chapter 7.
- 11.S13, the range of the rounding law (1e-150 to 1e150) moves from the library to the demand's
  parameters (D-2026-10-12-h, the cutoff is a parameter of the demand).
- 11.S16 and 11.S17 follow L13.3 (rounding is non-expansive up to an additive defect of about ε|x|)
  and L13.4 (the cost algebra needs a multiplicative part and an additive one), both still "mark
  pending" in the principles: your mark there decides these two.
- 11.S18, the `...Agrees` laws and `roundingSlack` return the measured cost and the certificate
  records it; the cutoff is the demand's. The change to the libraries is not done.
- 11.S19, which of these theories exist in Luthier: `lib/rational.lut` yes; `number_model.lut` and
  the theory of 11.S16, no.

ok

## Chapter 12. Files and tools

- 12.S1, a file denotes a value of a dependent record type: its fields are its definitions, the
  laws refine the fields, a library with holes is a function of its holes, `lib/library.lut`. The
  record part is decided since (D-2026-10-12-ad: a module is a value, a record of its definitions);
  the laws as refinements and the holes as parameters remain.
- 12.S9, the pattern of a library as a rule: a pure file with native definitions, holes and laws,
  and a `_python` file that fills the holes with externs certified against them.
- Explicit functors, a private part of a module, and a declared dependency on a Python package:
  three items carried from the old 03 §6, all proposed and none urgent.
- Question of the agent: does `eval` refuse an uncertified cone, as `run` does since
  D-2026-10-12-y (`run` strict from the start, no opt-out)? It records nothing and is a probe. Mine:
  `eval` stays exempt and prints the states of the cone, so what it shows is never mistaken for a
  certified result.
- Question of the agent: do `run --checked` (every value an extern returns tested against its type
  as it crosses) and `run --no-record` stay? Mine: `--checked` stays, it is the bridge check of
  L11.2 (an extern is validated against the laws of its type before it is applied); `--no-record` goes, since a run of a program writes its record (P2, everything derived
  carries how it was derived) and `eval` is the probe that records nothing.

ok