# Prior art: languages and DSLs with Luthier's features

Draft 0, 2026-10-09. Status: for Luciano to read and annotate. Written for Luciano.

Luciano asked for an extensive search for a programming language or domain-specific language
(DSL) that has some or all of Luthier's features. The model (Claude Opus 5.5) wrote the list of
features below from `00`, `04`, `06`, `08`, `09` and `record/objectives.md` at commit 7eb7ecd, and
ran seven searches with web access, one per family of languages. The prompts are in
`record/prior-art-2026-10-09/prompts.md` (commits 1cc8d62 and 523df87), and the seven reports,
unedited, in `record/prior-art-2026-10-09/reports/` (commit 997059b; their SHA-256 hashes are
listed at the end of `prompts.md`). Every claim about a language here comes from those reports,
which cite a primary source for it; the source is repeated where the claim matters. What the
model proposes for Luthier is marked *Proposed*. `02-que-robar.md` (2026-09-29) did a narrower
search on the certificate alone; what it found is not repeated.

## 0. Notation

The features, as the searches used them. Each later mention repeats a short form of the statement.

- F1 Type = theory: a named type is a subtype of a base cut out by executable laws; a value of it
  is a model.
- F2 Laws are executable Bool predicates that the language itself runs as tests on generated
  cases; defining a function defines its test.
- F3 Certificates: persistent, attached to definitions, keyed by content hash, with a grade of
  evidence (point, sampled, bounded, exhaustive, witnessed, proved, assumed); a program's
  certificate is the chain of its parts', graded by the weakest link, and every chain ends in
  assumptions.
- F4 Holes: a declaration without body, filled by another file.
- F5 One concept, several implementations (native and foreign), tested equivalent against the same
  laws, costs measured, the fastest chosen and the choice recorded.
- F6 Extern at a defined type: the type's claims are checked when a value crosses; an undescribed
  extern is debt.
- F7 `Real` is the ideal, `Float64` refines its values with the machine's operations; laws over
  the reals are checked on doubles within a tolerance.
- F8 Generators are values derived from the type; statistical laws declare level and power;
  evidence is read in a Bayesian way with the prior as a parameter.
- F9 Plan and execution: a timeless plan, actions with laws, a trace with costs, the world reached
  through pointers pinned by hash.
- F10 Provenance: everything derived records its inputs by hash, the script version, every
  parameter and the seed.
- F11 A minimal kernel, executable by hand, with the interpreter stated in the language.
- F12 Dependent types, a universe, structural and nominal types, `data` as initial algebras.
- F13 Every criterion is a parameter.
- F14 Built so that models write the code and a human scientist reads it.
- F15 Laws valued in a cost or a discrepancy instead of Bool (the subobject classifier taken as
  [0,∞], Lawvere 1973), with a prior and a cost of failure on a use.
- F16 Aimed at scientific data analysis, interoperating with Python.

Other abbreviations: PBT is property-based testing (laws run on generated inputs); SMT is a
satisfiability-modulo-theories solver, an automatic prover for first-order formulas with
arithmetic; TCC is a type-correctness condition, the proof obligation PVS generates when a value
is used at a predicate subtype; STL is signal temporal logic.

## 1. The answer

No language or DSL found has all of Luthier's features, and none has its core: F1 (a type is a
theory), F2 (the language runs the laws as tests) and F3 (graded certificates keyed by hash)
together. Each feature exists somewhere, most in several places. The closest systems cover five
to seven of the sixteen, each from a different angle.

| system | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 | F10 | F11 | F12 | F13 | F14 | F15 | F16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ACL2 / ACL2s | | ◐ | ◐ | ● | ◐ | | ● | ◐ | | | | | | | | |
| PVS | ● | ◐ | ◐ | ● | | ◐ | | ◐ | | | | | | | | |
| VDM + QuickCheck (Overture) | ◐ | ◐ | ◐ | ● | | ◐ | | ◐ | | | | | | | | |
| Ciao Prolog assertions | ◐ | ● | ◐ | ◐ | | ◐ | | | | | ◐ | | | | | |
| Lean 4 | ● | | ◐ | | ◐ | ◐ | ◐ | | | | ◐ | ● | | | | |
| Sage (hybrid type checking) | ● | | ◐ | | | ◐ | | | | | | ◐ | | | | |
| Unison | | ◐ | ◐ | | | | | | ◐ | ◐ | | ◐ | | | | |
| Aver (2025-26) | | ● | ◐ | | | | | | ◐ | | | | ◐ | ● | | |
| SageMath categories | ◐ | ◐ | | | | | ◐ | | | | | | ◐ | | | ● |
| GAP / CAP | ◐ | | ◐ | ◐ | ◐ | ◐ | | | | | | | | | | |
| Vehicle | | | ◐ | | | ◐ | | | | | | ◐ | ◐ | | ● | ◐ |
| Biocham 4 | | | | | | | | | | | | | ◐ | | ● | ● |
| PetaBricks | | | | | ● | | | | | | | | ◐ | | ◐ | |
| Rosa / Daisy | | | | | | | ● | | | | | | ◐ | | | |

● has it; ◐ has part of it. Sources for each mark are in the reports (A for ACL2, PVS, VDM,
Lean; B for Ciao, Sage; D and F for Unison, Aver; E for SageMath, GAP, Biocham; G for Vehicle;
C for PetaBricks, Rosa).

Four of Luthier's features have no full match anywhere in the seven searches:

- F3 as a whole. The grade ladder exists in pieces: PVS marks theorems that rest on undischarged
  TCCs as incomplete; VDM's QuickCheck answers FAILED, MAYBE or PROVABLE, and its "finite"
  strategy is exhaustive; Alive2's verdict is "bounded"; Ciao has the statuses check, trust, true,
  checked, false; ACL2 marks a book built with skipped proofs as less trustworthy. Hash keys exist
  in Unison, Bazel and Vehicle, with pass or fail and no grade. Nobody combines grade, hash and
  chain.
- F5 with laws. PetaBricks measures alternatives, checks them against each other on one input and
  writes the choice to a file; Kernel Tuner checks variants against a reference with a tolerance.
  Neither checks laws on generated cases, and nobody mixes native and foreign implementations.
- F8's Bayesian reading. Bayesian statistical model checking (Zuliani, Platzer, Clarke) has the
  prior as a parameter, outside any language. No PBT tool reads its evidence that way.
- F14 with F16. There are now dozens of languages for model authors (a catalogue at
  agentlanguages.dev lists 42, most of 2025-26). None is aimed at science, none has laws as types.

So the combination is what Luthier would add, as `02` §1 already said for the certificate alone;
the search widens that to the whole list.

## 2. What to take, feature by feature

Each item names the system, the mechanism, and its source; the line after "*Proposed*" is the
model's reading for Luthier.

**F1, type = theory.** PVS predicate subtypes are `{ x : T | p }` almost literally, and each use
at a subtype generates an obligation (Rushby, Owre, Shankar, TSE 1998,
https://www.csl.sri.com/papers/tse98/tse98.pdf). GATlab (AlgebraicJulia) has the same object, a
theory as signature plus axioms and a model as a value, plus theory morphisms that carry models
from one theory to another; it does not check the axioms, and lists sampling them as future work
(https://arxiv.org/abs/2404.04837). SageMath runs the axioms of every category a structure belongs
to, inherited down the hierarchy, on elements the structure itself supplies (`TestSuite`,
`some_elements()`). *Proposed*: let a model offer its own witnesses beside the generator derived
from the type; and keep GATlab's morphisms in view for F5, a declared map between two models.

**F2, laws run by the language.** Ciao uses an assertion's precondition as a generator, and what
static analysis cannot prove becomes run-time checks and tests over the same assertion
(https://arxiv.org/abs/1102.5497, sec. 4). Clojure spec's `instrument` with `:stub` replaces a
function by one that checks its arguments and draws a result from its return spec. *Proposed*: a
hole (F4) gets a runnable stand-in drawn from its type, so what depends on it can be tested before
it is filled. PVS does the same by naming a temporary instance in `random-test :instance`.

**F3, certificates.** Four mechanisms, from four places.
- Canonical form before hashing. Sage stores refuted and proved subtyping judgments in a database,
  after dropping unused bindings and renaming variables to de Bruijn indices, so equivalent
  judgments hit the same entry (https://www.cs.williams.edu/~freund/papers/sage-tr.pdf).
  Unison's identity is the hash of the syntax tree with each dependency replaced by its hash.
  *Proposed*: hash a certificate's statement in that canonical form, or renaming a variable
  invalidates the evidence.
- Early cutoff. In *Build Systems à la Carte* (Mokhov, Mitchell, Peyton Jones, ICFP 2018), a
  verifying trace keys on the hash of each dependency's value, so a change that leaves a value
  unchanged invalidates nothing downstream. *Proposed*: specify Luthier's certificate store as
  such a trace.
- Obsolete instead of discarded. Why3 keeps old proof attempts and marks those whose goal changed
  as obsolete; its manual warns it does not track realizations against theories, which is the gap
  a content hash closes (https://github.com/AdaCore/why3/blob/master/doc/itp.rst).
- The base of trust, listed. Lean's `#print axioms` gives the assumptions under each theorem, and
  `native_decide` adds one axiom per call so each can be audited. Aver's certificate lists its
  trusted base and, when it declines, names the gate that failed (https://averlang.dev/certificate.html).
  Caesar's slicing removes statements while verification still succeeds and reports which
  assumptions were unnecessary (https://arxiv.org/abs/2512.20214). *Proposed*: this is the
  computable form of "every chain ends in assumptions".

The IEEE 1788 decorations of interval arithmetic are the cleanest working instance of the weakest
link: each interval carries a grade, a result's grade is the minimum of its inputs', and since
IntervalArithmetic.jl 0.23 (July 2025) a flag marks results contaminated by plain numbers, which
is F6's debt carried by the value. *Proposed*: carry the grade on the value and combine by a
lattice meet, so the rule costs nothing per operation.

**F4, holes.** ACL2's `encapsulate` introduces a function with constraints and no body, and
`defattach` attaches an executable one without changing the logic
(https://cs.utexas.edu/~moore/acl2/manuals/current/manual/index-seo.php/ACL2____DEFATTACH). Hazel
evaluates around holes and resumes when one is filled (https://arxiv.org/abs/1805.00155).

**F5, several implementations.** PetaBricks: "include a slow reference implementation as a choice
so that faster choices can be checked against it", and the checks ride on the tuner's own search,
so testing concentrates on what gets chosen
(https://commit.csail.mit.edu/papers/2009/ansel-pldi09.pdf, §3.5). Lean has two grades of "this
implementation is the concept": `@[csimp]` needs a proof of equality, `@[implemented_by]` is
unchecked. Urbit marks each native jet as verified or to be checked against the reference at run
time. CAP computes the cost of a derived operation from the costs of what it uses and settles on
the cheapest. *Proposed*: the equivalence of two models is itself a certificate with a grade;
CAP's static weights become measured costs, recorded with the choice.

**F6, extern.** Typed Racket turns the declared type of an untyped import into a contract at the
boundary, with `unsafe-require/typed` as the explicit unchecked route. Exo declares a foreign
instruction with a native body that is its specification, next to the call that is its cost.
shen-backpressure (2026) compiles a human-reviewed Shen spec into checked constructors in Python,
so model-written code can only build values through them (https://github.com/pyrex41/shen-backpressure).
*Proposed*: an extern with a native reference body is the natural F5 pair.

**F7, the ideal and its realization.** Rosa and Daisy call `Real` "a non-executable specification
language" and put the error bound in the contract, `ensuring(res => res +/- 1.001e-11)`; the
compiler picks the finite type that meets it (https://arxiv.org/abs/1410.0198). ACL2 and Why3
define each float operation as the real one followed by a rounding; in ACL2 the rounding is itself
a constrained function, a hole (Kaufmann and Moore,
https://cs.utexas.edu/~moore/publications/double-float.pdf). Pyret makes `==` on approximate
numbers an error, so a test must name its tolerance. NumFuzz bounds the error between the real and
the float semantics in the type (https://arxiv.org/abs/2405.04612). *Proposed*: state `Float64`'s
operations as `round ∘ op` over `Real`, with `round` declared and not defined; and forbid `==` on
`Float64` inside laws, which `05` R8 nearly does already.

**F8, generators and statistics.** ACL2s `defdata` derives an enumerator from every type, range
types included. VDM's QuickCheck makes the strategy a plug-in that returns values or a verdict
with a witness, so the grade belongs to the strategy (https://arxiv.org/abs/2410.02046). Bayesian
statistical model checking samples until the Bayes factor of P(φ) ≥ θ under a Beta(α, β) prior
passes a threshold T or 1/T (https://logic.kastel.kit.edu/ap/pub/bayesmcest-FMSD.pdf); probabilistic
assertions put probability and confidence in the assertion (`passert e, p, c`). *Proposed*: the
Beta-Bernoulli sequential test as the default engine for a sampled law, α, β and T declared by the
law, and the posterior recorded in the certificate.

**F9, F10, plan, execution, provenance.** Effects with equations exist only in proof systems
(Kidney, Yang, Wu, POPL 2024). Lukšič and Pretnar track which equations of an effect hold in which
part of a program, since most handlers break the global ones (https://arxiv.org/abs/2005.13654).
*Proposed*: a law of an action is certified per context, and the certificate says which. For
provenance, Nextflow, targets (R) and AiiDA already do F10 for scientific pipelines; AiiDA records
a cache hit as a cloned node, so the provenance graph is the same with caching on or off.

**F11, the kernel.** Lean4Lean and MetaCoq state a kernel in its own language against a formal
type theory; MetaCoq calls the shift one from a trusted code base to a trusted theory base. Both are
far too large to run by hand. Ciao's "checkification" turns its analyzer's outputs into run-time
checks to find bugs in the analyzer itself (https://arxiv.org/abs/2501.12093).

**F14.** Aver is the nearest in purpose: laws `verify ... law` beside each function, `decision`
blocks in the syntax, effects recorded and replayable. Its laws run over hand-listed finite
domains, its certificate is all or nothing, and a type is not a theory. Quint positions its
readable spec as what humans validate while models write code (https://quint.sh/posts/llm_era).
L4, a language for law, aims to be written by machine and read by lawyers (the sentence is from a
page that did not load: unverified).

## 3. Laws valued in [0,∞]

Luciano, 2026-10-08 (voice note 18.10.00, [14:35]-[17:34]): laws could go "no a un boolean sino a
un costo", "una especie de likelihood ... no normalizada"; and [03:37]-[08:30]: a prior over the
parameters and a cost of failure, the function judged by an expectation. On 2026-10-09, in chat:
use the positive reals as the subobject classifier, a cost function. What the search found
(report G unless marked):

- The logic exists. Lawvere logics (Bacci, Mardare, Panangaden, Plotkin) take truth values in
  [0,∞] with 0 true and ∞ false; the propositional ones have complete, decidable deduction systems,
  and Rational Lawvere Logic (CSL 2026) adds product and quotient
  (https://entics.episciences.org/12292, https://arxiv.org/abs/2402.03543). Quantitative equational
  logic writes laws as `s =ε t` over metric algebras (https://lmcs.episciences.org/14636). Neither
  has an implementation.
- Bool is the limit case in several working systems. Caesar/HeyVL values assertions in the
  extended non-negative reals, and a Boolean condition is the function that is ∞ where it holds and
  0 elsewhere (https://www.caesarverifier.org/docs/heyvl/statements); its orientation is the
  opposite of Lawvere's. In Probabilistic Soft Logic a hard rule is a rule of infinite weight
  (https://www.jmlr.org/papers/v18/15-631.html).
- One law, two readings. Vehicle compiles one specification to a Boolean query for a verifier and
  to a loss for training, with the differentiable logic as a parameter, and caches verification
  results by the hashes of the spec, the networks and the data
  (https://vehicle-lang.readthedocs.io/en/latest/exporting.html).
- In biology. Biocham 4 gives a temporal specification of behaviour a continuous satisfaction
  degree and uses it as the objective when fitting parameters of a reaction network
  (https://lifeware.inria.fr/biocham4/; report E).
- A caution. The Logic of Differentiable Logics shows that most fuzzy logics used this way are
  sound and incomplete with respect to first-order logic once quantifiers enter
  (https://arxiv.org/abs/2303.10650): the Bool limit is not automatic for quantified laws.
- Not found: a system that records the measured cost in a certificate, or that tests by a prior
  over inputs times a cost of failure. Risk-based testing is process guidance; conservative
  Bayesian inference gives the mathematics of a failure probability updated by failure-free tests
  (https://arxiv.org/abs/2208.07935) and is tied to no language.

*Proposed*, for when the idea is taken up: the certificate of a cost-valued law records the worst
cost seen and the input that reached it, beside the seed and the number of cases (Hypothesis's
`target()` prints this and throws it away); the expectation of the cost under the prior of a use is
the use's value; Lawvere's orientation, 0 true, since it makes the cost a distance and Bool laws
the case {0, ∞}. That last choice is Luciano's.

## 4. Limits of this search

- Search A ran out of its search budget before reaching F*, Event-B, Alloy, Z, TLA+/Apalache,
  OBJ/CafeOBJ, Agda and Twelf. From memory, unverified: Alloy's bounded scope matches the grade
  "bounded", and F* has `assume val` and erased reals.
- The searches were run by the same model that wrote the list of features, so a feature it framed
  narrowly may have hidden a match framed differently.
- Several 2025-26 languages for model authors (Vow, NanoLang, Prove, AILANG) were seen only through
  the catalogue page, not their repositories.
- Claims marked unverified in the reports are not used above except where said.
