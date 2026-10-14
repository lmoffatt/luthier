# Review of layer 3 of Luthier, the numerical theories (probability, belief, optimization) (round 1, bundle D)

You are reviewing theory files written in Luthier, a language whose interpreter is being rebuilt from its own theories: a type is a theory (a structure with laws), a value of it is a model, and the language certifies models against their theories by testing. A theory file (`.lth`) declares a record type of operations, states its laws as Bool-valued definitions over a model (`(m : T)`), and defines the theory as their conjunction (`T := Law1 & Law2`); a model file (`.lut`) holds values of theories. Every constructor of a `data` must have a law stating its role (principle L2.7: a definition is a concept; distinct constructors and accessors state no role). A law quantifies over the subtype it means rather than over an implication whose premise random cases rarely meet. The files parse with the project's parser; nothing yet type-checks or certifies them, so you are the first check of their meaning. Grammar, kernel and earlier layers were reviewed in earlier rounds and are not in scope. Do not reopen a decision listed under "Decisions the files cite" unless a file contradicts it; where you disagree with the specification itself, say so as a separate item.

This prompt covers the numerical theories the slice of the first experiment needs (layer 3, bundle D of its external review; the other bundles are reviewed apart and not included). `probability.lth` states a likelihood over the vectors of a dimension, the mean model and the Gaussian construction on it, their derivatives, and the uniform values of a calibrated model with Kolmogorov's distance. `belief.lth` states a Gaussian belief in information form, the maximizer Laplace's update needs (a theory the host's `lm : Maximizer` is validated against), and the update. `optimization.lth` states Levenberg-Marquardt as types with laws over array leaves. Each has a model file (`*_model.lut`). `arrays.lth` is the array leaves they import (given whole). `experiment_zero.lut` is the program that uses these theories; read it as the use the theories must serve, not as a file under review for style. As context only, not under review: section 2 of `docs/spec/11-numbers.md` (the primitive types) and item 6.S16 of `docs/spec/06-certification.md` (the host's code is a specimen certified against the theory). The material below, in this order: terms and principles L2.7, L9.6, L10, L11 and P11; the decisions the files cite; then the files, then the two context excerpts. Frozen at commit 2710cfc.

Cutoffs: D-2026-10-14-c says every law is a Boolean predicate and every cutoff it needs (a tolerance, a resolution, a rank floor, a convergence threshold, a level) is a parameter of the law that the demand supplies (P11), never a constant in a file.

Answer per file, numbered, quoting the line you mean, as briefly as each allows:
1. **Laws that are wrong**: false of the intended model, or unsatisfiable together.
2. **Laws that do not determine what they claim**: where a wrong model passes every law; give it.
3. **Roles (L2.7)**: a constructor of a `data` with no law of its role, or a role law that only lists constructors.
4. **The models against their theories**: a law a `*_model.lut` breaks, with the case.
5. **Against the specification**: where a file says other than its chapter or a cited decision.
6. **Implication over a type**: laws stated over a type with an implication a random case rarely meets, where the subtype should be the quantified domain.
7. **What you would change first**, one thing, with the reason.
8. **Cutoffs**: a cutoff written as a constant where it should be a parameter the demand supplies (D-2026-10-14-c, above).
9. **Certifying the maximizer**: what law is missing for the host's maximizer (`lm : Maximizer`, `belief.lth`) to be certified beyond the quadratic family: which property of a maximizer on a non-quadratic objective a test could check, and over which generator.

Put anything you cannot verify from the files in a final "not sure" list instead of asserting it. Do not rewrite the files.


---

## Material

Frozen at commit 2710cfc.

### Principles (excerpt of `docs/principles.md`)

## Terms

Each term has one category and is defined here and nowhere else; the principles cite Terms.

- A *structure* is a type in the kernel's language (spec 3), built from four forms: a product, a
  value made of several named fields (a record, a tuple); a sum, a value that is one of several
  cases, each tagged (a variant, an enumeration, `Maybe`); a function type `A -> B`; and a
  recursive type, one defined in terms of itself (a list, a tree). Each form may hold the others.
  An *alias* names a structure: a shape used before what it is for is known (D-2026-10-13-p).
- A *predicate* is a function into `Bool`. A *cost* is a function into `Cost`, the non-negative
  reals with infinity, 0 true and ∞ false.
- A *law* is a predicate or a cost, or a combination of laws that is again a predicate or a cost;
  how laws combine is L12.
- A *theory* is a structure with its law.
- A *model* is an inhabitant of a theory: a value of its structure whose law is certified.
- A *function* is a value of a function type `A -> B`, in the standard sense. A function type with
  its law is a theory, and a function that satisfies it is a model of that theory.
- The *dependences* of a theory are the theories whose models its structure and law use
  (`Monoid A` depends on `Setoid A`; `VectorSpace K V` on `Field K`). A carrier is assumed to come
  with the models it names, `A` with its setoid, `K` with its field, so a theory reads them from
  the type (O2 for the syntax). Every theory has dependences; a function type has at least the
  setoids of its carriers, since its law uses their equality.
- A *certificate* is the record that a law was checked, with its *grade*: *proved*, by a theorem
  cited or by delegation to a library's guarantee; *exhaustive*, over every case; *cases*, over
  chosen cases; *sampled at a level*, over a sample drawn from a stated distribution; *assumed*,
  not checked. A proof is a certificate of grade proved. To *certify* is to produce one.
- *Evaluation* computes a function, and has no effect (L4). *Execution* is an action on the world
  (print, save). Writing a certificate into the store Luthier owns is an action on Luthier's own
  state, verified by reading the store back (L4); `test` is that action (L5).
- The *demand* is a request for a value from outside the program, an action, carrying the type and
  the tolerance it wants, the type possibly decorated: the value with its error, its derivative,
  its certificate. The *planner* is what chooses, among the models certified equivalent, the one
  that runs, and plans the decorated type the demand asks for.
- The *declarative face* of a program is what it states: its types, laws and definitions. The
  *executive face* is what the demands ask of it.
- The two faces live apart. The declarative face has no time: its definitions live in the
  universe `U`, and are copied, compared and memoized. The executive face acts on the world `W`,
  one world, each value of it used once, never memoized (D-2026-10-13-b). (A metaphor, not a term:
  mind and world, as in McDowell's *Mind and World*, 1994.)
- Three things make the language: what is said (the definitions, `U`), what is done (the actions,
  `W`), and what is certified. Every reading of the world changes Luthier's representation of it; a
  *certifier* changes something else, the belief that a value belongs to a type, and its result
  comes back to the declarative face as that belief with its evidence: the passage from
  acquaintance to description (G1). It is not a keyword; its five kernel forms are names of core
  (D-2026-10-13-d, D-2026-10-13-e).

- An *object* is a type with its equality, the word for what C++ calls a regular type: the base
  theory (a setoid, O2), whose laws the kernel guarantees for a structural `==` and the author
  states for an observational one; a kernel type with no equality is a *structure*
  (D-2026-10-12-ak). A *theory* is an object with its further laws, written in one name or in
  several (then a cycle of the dependency graph); the number of names is its presentation
  (D-2026-10-12-aj).


- L2.7 (His words) A definition is a concept, and a collection of types is not. An alias names a
  structure we use before we know what it is for; a definition promotes it to a theory, and what makes
  it one is a law it must follow, stating the role of each part. Distinct constructors are free and
  state no role; an observer that only lists them is an automatic accessor, not a law; a `data` with
  no law of its constructors' roles is a collection and is written as an alias (D-2026-10-13-p,
  D-2026-10-07-e). It costs thought, and that is its purpose. Everything has laws; it is a matter of
  finding them, usually in the place the thing holds in a known structure (`Unit` terminal, `List` the
  free monoid, D-2026-10-13-t). [settled]

- L9.6 The grade of a sampled certificate depends on the distribution sampled, not only on the
  number of samples, because errors concentrate at the edges. [settled]

**L10. A certificate records what is known of a law, its domain, its bound and its evidence; it is

- L10.1 A certificate (Terms) names the law it records as checked, the domain the check covered (a
  subtype, the cases listed, or the distribution sampled), the bound observed (for a law into `Cost`,
  the distance its `forall` gives over the costs seen, D-2026-10-13-m), and the evidence: its grade
  and, for a sampled check, the sample's statistics converted to an evidence cost (D-2026-10-12-r).
  [proposed]
- L10.2 The grade is derived from the domain and the evidence cost: proved and exhaustive have
  evidence cost 0 on their domain; cases, 0 on the cases listed and ∞ outside; sampled, the finite
  cost of its statistics on the distribution sampled. An `assumed` certificate carries what is
  asserted and no check: a Boolean law asserted true, with bound 0, or a cost law asserted with a
  formula of the inputs, a library's documented bound such as p(n)·ε·κ(A), with the formula evaluated
  at the input as its bound; its evidence cost is the demand's parameter for assumptions, with no
  default, so that a demand that names none refuses assumed values (D-2026-10-11-n, D-2026-10-12-t).
  When the formula is a cited guarantee with its hypotheses, the certificate is proved by delegation
  (L9.7), not assumed. The five names stay in the certificate for the reader; the planner reads the
  costs. [proposed]
- L10.3 The conversion from statistics to an evidence cost is a function with a declared shape, the
  sample's statistics and the demand's level in, a cost out, filled per theory (D-2026-10-12-r); the
  first instance is −log(1 − ε̂(n, δ)) in nats, with ε̂ the bound on the fraction of the distribution
  where the law's bound fails, from n samples at confidence 1 − δ, and δ the demand's parameter.
  [settled]
- L10.4 A certificate is identified by a hash over its dependency cone (code, cases, seed, the
  distribution and level sampled); it is a frozen snapshot, and a later check does not change it but
  issues a new one that supersedes it, both kept, the latest in front (P3), so progress is the chain
  of certificates. [settled]
- L10.5 A certificate serves every demand whose cutoff it meets, on the bound and on the evidence
  cost alike (D-2026-10-12-h); the demand states what it requires (P11), and a memo hit serves a
  demand only if the cached cone meets it, checked at the hit and not only when the certificate was
  issued. [settled]
- L10.6 Certification is the default: demanding a value demands every certificate in its dependency
  cone, paid once through the memo, with no opt-out at the start (D-2026-10-12-y: a cone with an
  uncertified or provisional name is refused); an exception, if a real case asks for one, is O3 and
  would leave a certificate of grade `assumed` (D-2026-10-11-n); what never reaches an output needs no
  certificate, and what reaches one carries its cone's; `test` is the action that demands certificates
  without values (L5). [settled]
- L10.7 Certification transports along identity: if B is certified on inputs X with bound b and
  evidence cost e, and the identity A ≡ B is certified on inputs Y with distance d and evidence cost
  e′, then A is certified on X ∩ Y with bound b + d and evidence cost e + e′, and by nothing else; a
  path of identities composes the same way, link by link, the distances summed and the evidence summed
  (D-2026-10-12-q). (His correction, in grades) A is certified at the weaker of the two grades on X ∩
  Y. [proposed]
- L10.8 Links sampled over different distributions do not compose without a law relating the
  distributions; links sampled over the same distribution compose by the union bound, the failure
  fractions summed, which is the probabilistic bound the planner waited for (D-2026-10-12-q). The
  composition algebra belongs to the theory's cost type, the sum its first instance; whether a demand
  accepts a sampled path is its evidence cutoff, a parameter (P11). [proposed]
- L10.9 No operation on certificates raises a grade, lowers an evidence cost or widens a domain
  without new evidence. [settled]
- L10.10 Only a certifier builds a certificate: the constructor of `Certificate` is in no interface
  outside the theory of certification (L6.12), so clause 9 is enforced by the language and not left to
  good conduct (D-2026-10-13-c); the precedent is the abstract type `thm` of the LCF provers, which

**L11. Luthier orchestrates other languages: an extern is a specimen certified by its laws, and what

- L11.1 Types and laws are native; values may come through `extern` from Python or any host,
  declared over what they really receive and return, with description and verification kept on
  Luthier's side. [settled]

- L11.2 (His words, "si el tipo no sigue la ley no se aplica el calculo") An extern is declared over
  a type, a type carries its laws (L8), and the extern is validated against them, like any other
  function, the first time an action asks for it, before it is applied, and refused if it fails; its
  certificate stays by hash; without a type with a law to validate against it is not applied; the
  agreement test with the native is in addition (W5), and the planner's substitution is
  D-2026-10-11-m. [settled]

- P11 Every criterion is a parameter, never a constant in the code.

### Decisions the files cite (from `record/decisions.md`)

D-2026-10-05-c  `toFloat64` stays `Int -> Float64`, the nearest double to an integer, where its 37
                uses are; the specification follows the code, and the rounding of a `Real` waits
                for a `Real` that computes.
Author:     the model, departing from item 3.4 of record/plan-2026-10-05.md (which renamed it),
            accepted by Luciano with the rest of phase 3
Quote:      "arranca la Fase 3 como recomendaste"
Source:     chat:aa680014:1057
Kind:       language (spec 11.S5). For P16 (cheaper to revise: no rename of 37 uses for a
            conversion with no use yet)
Status:     current; implemented in luthier@aee30cc. The departure is stated at
            chat:aa680014:1048. Entered 2026-10-12 by the same session

D-2026-10-12-ag Where the correspondence of the old grades to the five of the Terms lives (spec
                1.S12) is settled when the laws of certification are written in Luthier's terms;
                the principles are then determined back from those laws.
Author:     Luciano
Quote:      "this question will be solved when we determine the laws of the certification in luthier
            terms."
            "When these laws are formulated, then we will backdetermine the principles."
Source:     luthier@e31780f:record/spec-wave-1-for-his-marks.md:38
            luthier@e31780f:record/spec-wave-1-for-his-marks.md:39
Kind:       method (spec 1.S12, spec 6; L14). For L14, P13
Status:     current; open until chapter 6 (wave 2) states the laws of certification

D-2026-10-12-ah His marks on wave 1 of the specification: ok on the sections of chapters 2, 3, 7, 11
                and 12 of record/spec-wave-1-for-his-marks.md, the model's readings included. So:
                2.S20 (quote and eval, candidate syntax); 3.S11, 3.S29 (fields), 3.S30 to 3.S34,
                3.S38, and a rule of evaluation counts as implemented only with a program whose
                value is compared; the model's parts of chapter 7, 7.S2 included (read: decided,
                since the idea is his and the section is ok); 11.S3, 11.S5, 11.S10, 11.S11 (to
                spec 7), 11.S13 (the range to the demand), 11.S18, 11.S19; 12.S1, 12.S9, `eval`
                exempt from certification and printing the states of the cone, `run --checked`
                kept, `run --no-record` retired. Left as they were: 11.S16 and 11.S17, which wait
                for his mark on L13.3 and L13.4; the three items carried into chapter 12 from the
                old 03 §6.
Author:     Luciano; the items the model's (the agents' and the integrating session's)
Quote:      "ok"
            "ok"
            "ok"
            "ok"
            "ok"
Source:     luthier@e31780f:record/spec-wave-1-for-his-marks.md:50
            luthier@e31780f:record/spec-wave-1-for-his-marks.md:81
            luthier@e31780f:record/spec-wave-1-for-his-marks.md:132
            luthier@e31780f:record/spec-wave-1-for-his-marks.md:156
            luthier@e31780f:record/spec-wave-1-for-his-marks.md:177
Kind:       language and tool (spec 2, 3, 7, 11, 12). For L14, P2, L11.2
Status:     current; chapter 1 and chapter 4 had no ok and keep their proposed items (1.S11, the
            rename of the rounding defect to η, 4.S16, 4.S21)

D-2026-10-12-h  The cutoff is a parameter of the demand: the minimal cutoff for an implementation
                to be considered. It is not a parameter of the certified-subtype constructor.
Author:     Luciano
Quote:      "I know a place for the cutoff, a minimal cutoff to consider an implementation, it is a
            parameter at the demand level."
Source:     record/recommendations-ia-principles-2026-10-12.md (e8d7db1), §4.3
Kind:       principles (L3, L6, L13). For P11 (every criterion is a parameter), G3 (the demand)
Status:     current; to apply in draft 11

D-2026-10-13-g  His mark on waves 2 and 3 of the specification: ok on every item of
                record/spec-wave-2-3-for-his-marks.md, the model's readings of the agents' questions
                included. So: the interfaces asked of libraries (5.S3, 8.S2, 9.S14, 10.S5) and the
                sixth law of 6.S5, `⊤ ≤ 0` false; checks to a library (5.S10); 5.S12, 5.S13; the
                fields of a certificate, the kept chain, delegation, no free evidence and
                `lib/certification.lut` with the grade correspondence (6.S6 to 6.S16, which settles
                D-2026-10-12-ag); 8.S11, 8.S15, equal keys for results (8.S9), L5.6 as extending
                D-2026-10-10-d; 9.S3 to 9.S17; 10.S3 to 10.S14; L11.7 settled; the validation of an
                extern left under D-2026-10-11-n; and a chapter may cite a settled clause as its
                status, `[decided L6.4]`, checked by `check_spec.py`. With it, on his "Si,
                agregalo": the key of a result holds only the parameters of the demand its cone
                reads.
Author:     Luciano; the items the model's and the agents'
Quote:      "OK"
            "Si, agregalo."
Source:     luthier@582e4bd:record/spec-wave-2-3-for-his-marks.md:98
            chat:f15ae1b6:1793
Kind:       language and tool (spec 1, 5, 6, 8, 9, 10; principles L11.7; scripts/check_spec.py).
            For P13, P8
Status:     current; left proposed because the document did not show them: the method of 8.S1
            (by hand or derived), 8.S13 (a session line re-evaluates only what changed)

D-2026-10-13-x  Answers on layers 0 and 1 (record/questions-for-luciano-2026-10-13-layers-0-1.md).
                Q1: a record is a product whose projections are named, `.x` and `.y` the arrows
                `first` and `second` of the categorical product, so they are part of the product;
                a labeled sum likewise, its labels the injections. The kernel gains a record former
                whose names are part of the term, with the laws of the product on named projections
                (as `PairFst`, `PairSnd`, `Pairing`), and the sum its named injections. Q3: helper
                functions in theory files keep being reported, not rejected, since everything is to
                have an underlying law. Q4: `Nat`'s laws accepted as written (0381962). Q2 (blocks
                and the notation of lambdas) is under discussion.
Author:     Luciano (Q1 his framing; the record former the sessions' recommendation)
Quote:      "en teoria de categorias un producto tiene las flechas first y second, aqui las flechas
            serian   .x  y .y  o sea forman parte del product."
            "yes because we want that everything has an underlying law."
            "Ok"
Source:     luthier@39b0fa5:record/questions-for-luciano-2026-10-13-layers-0-1.md:20
            luthier@39b0fa5:record/questions-for-luciano-2026-10-13-layers-0-1.md:51
            luthier@39b0fa5:record/questions-for-luciano-2026-10-13-layers-0-1.md:67
Kind:       spec (3.S3, 2.S12) and the theories term.lth, kernel_laws.lth, program.lth
Status:     current; Q2 open

D-2026-10-14-a  Functions cross the bridge in three more forms than 3.S23 states: a Luthier
                lambda passed to a host function and called back from the host, its calls
                counted and recorded in the run's record (P2, 12.S18); a record whose fields are
                functions, crossing as the record with each function a callback; a host function
                crossing in as an opaque value, applicable only through the bridge and never
                reduced by the kernel; and a partial application of an extern, with the arity
                from its declared type. Needed by the fit of sonolocalización (lm.maximize,
                Objective, sampleFull; record/IA/sonolocalizacion-inventory-2026-10-13/
                answers-2-2026-10-14.md). Changes 3.S23 (or a new 3.S41), a law for the callback
                in world.lth or term.lth, run.py.
Author:     Luciano, on the model's recommendation (record/plan/questions-2026-10-14.md, Q1)
Quote:      "1--> admitir (suena caro pero necesario de ultima como control)"
Source:     luthier@c707f7c:record/plan/questions-2026-10-14.md:31
Kind:       spec (3.S23) and world.lth or term.lth, run.py
Status:     current

D-2026-10-14-c  First everything Boolean: every law is a Boolean predicate, and every cutoff it
                needs (a tolerance, a resolution, a rank floor, a convergence threshold, a level)
                is a parameter of the law that the demand supplies (P11, 8.S1, L5.18), never a
                constant in a file. The cost types of D-2026-10-13-m (`Distance`, `Evidence`,
                certification.lth) come later, on the slice's failures, and may then relate
                those cutoffs to the cost. Exception kept as stated: a law with a quantifier
                that has no finite Boolean form (`SupIsLeast`, algebra.lth) stays a `Law`,
                stated and not tested.
Author:     Luciano
Quote:      "hagamos primero todo booleano, pero expongamos los parametros de tolerancia de corte
            como variables que luego pide la demanda. La idea es que quizas luego esos parametros
            de corte esten relacionados con el costo. Pero primero hagamos todo booleano"
Source:     chat:a5ea3059:0 (this session, 2026-10-14 evening; the line is unknown until the
            export)
Kind:       theories (the laws of numbers.lth, arrays.lth, probability.lth, belief.lth,
            optimization.lth as written), step 5.1 of the plan
Status:     current


### `probability.lth`

````
-- probability.lth: a likelihood over the vectors of a dimension, the mean model and the Gaussian
-- construction on it, the derivatives their laws need, and the uniform values of a calibrated
-- model with Kolmogorov's distance and tail.
--
-- Draft 0, 2026-10-14, by Claude Fable 5.1, an agent of the coordinating session, on the brief
-- record/IA/slice-theories-2-2026-10-14/prompt.md (item 1; inventory §6 item 7, rows 21 and 24).
-- Sources: spec 7.R2 (the libraries quantify over `VecOf n`, never over `(Theta : U)`), 11.S18
-- (a tolerance is the demand's, D-2026-10-12-h), 7.S17 (a statistical law declares its level),
-- 4.R10 (a law characterizes; agreement with a native definition is a corollary), 12.S9 (the
-- pattern of a library), P11 (every criterion is a parameter: the step and the tolerance of a
-- central difference, v0.1's `fdStep`, `fdTol`). The v0.1 file is `probability.lut` at the tag
-- v0.1-final (lines 36, 57-86, 114-120, 275-313 are what the slice uses); the names below are
-- its, so that the port of experiment_zero.lut, positions.lut and distances.lut is a rename at
-- most. What is not here: the sampler, the probability integral transform and the Bartlett
-- identities of v0.1 (`IsDensityOf`, `Kernel`), which need a generator of standard normals;
-- generators.lth has `Random.uniform` only, and `normalVec` was an extern with no theory.
--
-- What this file states. The parameter space is `VecOf n` and moving along a direction is
-- `add` (7.R2; v0.1's `dim` and `shift` fields are gone). A mean model gives the predicted
-- observations and their Jacobian; a likelihood reports its log-likelihood, its score and its
-- information on data `y`, a vector of `k` observations. The laws: the Jacobian is the derivative
-- of the mean and the score the gradient of the log-likelihood, each by a central difference
-- along a drawn direction at the demand's resolution (step and tolerance, P11); the information is
-- symmetric and non-negative. Of the Gaussian construction: the log-likelihood peaks at the mean,
-- and the profile likelihood is the full one at the sigma that maximizes it, in value, score and
-- information. Kolmogorov's distance is a leaf (numpy's sort), characterized by its native
-- definition exactly (the same operations in the same order, v0.1 probability_python.lut) and by
-- what it is: of a multiset, zero on nothing, `max u (1 - u)` on one value, in [0, 1]. The
-- elementary functions and the array leaves are the imported models, as arrays.lth takes its
-- square root [proposed; the alternative is a parameter `(e : Elementary) (a : Arrays)` on
-- every definition, which the port would have to thread].
--
-- Index (all sections written in this draft):
--   §1 Derivatives by central differences at a resolution: `IsGradient`, `IsJacobian`
--      (7.R2; v0.1 array.lut:181-192).                                                    done
--   §2 `MeanModel`, `ScaledModel` and their laws (v0.1 probability.lut:275-286).          done
--   §3 `Likelihood` and what a likelihood is (v0.1 probability.lut:114-120, 133-156).     done
--   §4 The Gaussian construction: `gaussian`, `profiled`, their laws
--      (v0.1 probability.lut:288-313).                                                    done
--   §5 Uniform values: `normalCdf`, `normalTail`, `valueSums`, Kolmogorov's distance as a
--      theory, `kolmogorovTail`, `UniformAtLevel` (v0.1 probability.lut:36-86).           done

import "numbers.lth" Tolerance Positive within withinOf abs
import "numbers_model.lut" elementary : Elementary
import "arrays.lth" Vec Mat VecOf MatOf Dim vec mat sumTo forallBelow approxVec approxMat zeros exact
import "arrays_model.lut" numpy : Arrays add sub scale dot norm matVec matMul transpose madd mscale
import "generators.lth" Level

-- ---------------------------------------------------------------- §1 Derivatives (7.R2, P11)

-- How a slope is measured: the step of the central difference, in the units of the parameter,
-- and the tolerance of the comparison. Both are the demand's (P11, 11.S18): v0.1 held
-- `fdStep := cbrt eps` and `fdTol := sqrt eps` as constants (array.lut:181-182), the truncation
-- and the rounding of the difference being each of order eps^(2/3) at that step.
Resolution : U := { step : Float64, tol : Tolerance | 0.0 < step and 0.0 <= tol }

-- g is the gradient of f at t: g t is a vector of the dimension, and the slope of f along it, by
-- the central difference at the resolution's step, is its norm; compared relative to the size of
-- f at t, since the difference of two values of f loses the digits they share (v0.1 array.lut:184)
-- spec 7.R2
IsGradient (n : Nat) (r : Resolution) (f : VecOf n -> Float64) (g : VecOf n -> Vec Float64) (t : VecOf n) : Bool :=
  { v := g t
    nv := norm v
    if v.n /= n then false
    else if nv == 0.0 then true
    else {
      h := scale (r.step / nv) v
      slope := (f (add t h) - f (sub t h)) / (2.0 * r.step)
      withinOf r.tol (1.0 + abs (f t) + nv) slope nv } }

-- j is the Jacobian of m at t: along a drawn direction v, the central difference of m at the
-- resolution's step is j t applied to the unit vector of v, entry by entry within the tolerance
IsJacobian (n : Nat) (r : Resolution) (m : VecOf n -> Vec Float64) (j : VecOf n -> Mat Float64) (t v : VecOf n) : Bool :=
  { nv := norm v
    if nv == 0.0 then true
    else {
      h := scale (r.step / nv) v
      slope := scale (1.0 / (2.0 * r.step)) (sub (m (add t h)) (m (sub t h)))
      approxVec r.tol slope (matVec (j t) (scale (1.0 / nv) v)) } }

-- ---------------------------------------------------------------- §2 The mean model

-- A mean model on the vectors of dimension n: the k predicted observations and their Jacobian,
-- k x n. [proposed] `k` is a field (v0.1 had none; `TangentShapes` was a law on the data's
-- length) so that the laws can quantify the data over `VecOf l.k`; the port sets `k := i.n`.
MeanModel (n : Nat) : { k : Nat, mean : VecOf n -> Vec Float64, jac : VecOf n -> Mat Float64 }
-- spec 7.R2: the shapes are the model's, and the Jacobian is the derivative of the mean
MeanShape (n : Nat) (m : MeanModel n) (t : VecOf n) : Bool := (m.mean t).n == m.k
JacShape (n : Nat) (m : MeanModel n) (t : VecOf n) : Bool := (m.jac t).m == m.k and (m.jac t).n == n
JacIsJacobian (n : Nat) (m : MeanModel n) (r : Resolution) (t v : VecOf n) : Bool := IsJacobian n r m.mean m.jac t v
MeanModel (n : Nat) := MeanShape n & JacShape n & JacIsJacobian n

-- A scaled model: a mean model whose parameter also carries u = log sigma, a homogeneous error,
-- with the gradient of u in the parameter space (zero when sigma is known, v0.1
-- probability.lut:283-286)
ScaledModel (n : Nat) : { model : MeanModel n, logSigma : VecOf n -> Float64, dLogSigma : VecOf n -> Vec Float64 }
ScaledShapes (n : Nat) (m : ScaledModel n) (t : VecOf n) : Bool := (m.dLogSigma t).n == n and (m.model.mean t).n == m.model.k
DLogSigmaIsGradient (n : Nat) (m : ScaledModel n) (r : Resolution) (t : VecOf n) : Bool := IsGradient n r m.logSigma m.dLogSigma t
ScaledModel (n : Nat) := ScaledShapes n & DLogSigmaIsGradient n

-- ---------------------------------------------------------------- §3 What a likelihood is

-- What a likelihood reports on data y, k observations, at a parameter t: the log-likelihood, its
-- score (the gradient in t) and the information it claims, n x n (v0.1 probability.lut:114-120;
-- the paper's diagnostics read the three). The data are vectors: v0.1's `(Y : U)` is fixed to
-- `Vec Float64` [proposed], which is what the slice has and what 7.R2 asks of type parameters.
Likelihood (n : Nat) : {
  k : Nat,
  loglik : Vec Float64 -> VecOf n -> Float64,
  score : Vec Float64 -> VecOf n -> Vec Float64,
  info : Vec Float64 -> VecOf n -> Mat Float64,
}
-- the score and the information live in the space of directions: their dimension is n; the data
-- the laws run on have the likelihood's length
-- spec 7.R2
TangentShapes (n : Nat) (l : Likelihood n) (y : VecOf l.k) (t : VecOf n) : Bool :=
  y.n == l.k and (l.score y t).n == n and (l.info y t).m == n and (l.info y t).n == n
-- the score is the gradient of the log-likelihood (v0.1 probability.lut:146-147)
ScoreIsGradient (n : Nat) (l : Likelihood n) (r : Resolution) (y : VecOf l.k) (t : VecOf n) : Bool :=
  IsGradient n r (l.loglik y) (l.score y) t
-- the information reported is a Fisher information: symmetric within the tolerance, and its
-- quadratic form on a drawn direction is not negative beyond rounding (v0.1 probability.lut:155-156
-- read the spectrum; here the form, which the array leaves state)
InfoSymmetric (n : Nat) (l : Likelihood n) (tol : Tolerance) (y : VecOf l.k) (t : VecOf n) : Bool :=
  approxMat tol (l.info y t) (transpose (l.info y t))
InfoNonNegative (n : Nat) (l : Likelihood n) (tol : Tolerance) (y : VecOf l.k) (t v : VecOf n) : Bool :=
  { q := dot v (matVec (l.info y t) v)
    0.0 <= q or within tol q 0.0 }
Likelihood (n : Nat) := TangentShapes n & ScoreIsGradient n & InfoSymmetric n & InfoNonNegative n

-- ---------------------------------------------------------------- §4 The Gaussian construction

-- constants of the density, not criteria (P11): pi and log (2 pi)
pi : Float64 := 3.141592653589793
log2pi : Float64 := 1.8378770664093453
-- the outer product of two vectors, natively (arrays.lth has no leaf for it)
outerDef (x y : Vec Float64) : Mat Float64 := mat Float64 x.n y.n (fn i j { x.f i * y.f j })

-- Full Gaussian likelihood, u = log sigma a parameter. With r = y - mean, J the Jacobian, K the
-- number of observations and g the gradient of u (v0.1 probability.lut:288-300):
--   loglik = -1/2 e^{-2u} |r|^2 - K u - K/2 log 2 pi
--   score  = e^{-2u} J^T r + (e^{-2u} |r|^2 - K) g
--   info   = e^{-2u} J^T J + 2 K g g^T
gaussian (n : Nat) (m : ScaledModel n) : Likelihood n := {
  k := m.model.k,
  loglik := fn y t {
    r := sub y (m.model.mean t)
    u := m.logSigma t
    0.0 - 0.5 * elementary.exp (-2.0 * u) * dot r r - toFloat64 r.n * u - 0.5 * toFloat64 r.n * log2pi },
  score := fn y t {
    r := sub y (m.model.mean t)
    e := elementary.exp (-2.0 * m.logSigma t)
    add (scale e (matVec (transpose (m.model.jac t)) r)) (scale (e * dot r r - toFloat64 r.n) (m.dLogSigma t)) },
  info := fn y t {
    j := m.model.jac t
    e := elementary.exp (-2.0 * m.logSigma t)
    g := m.dLogSigma t
    madd (mscale e (matMul (transpose j) j)) (mscale (2.0 * toFloat64 j.m) (outerDef g g)) },
}

-- Profile likelihood, sigma eliminated by its maximum sigma^2 = RSS / K (v0.1
-- probability.lut:302-313):
--   loglik = -K/2 log(2 pi RSS / K) - K/2
--   score  = (K / RSS) J^T r
--   info   = (K / RSS) J^T J
profiled (n : Nat) (m : MeanModel n) : Likelihood n := {
  k := m.k,
  loglik := fn y t {
    r := sub y (m.mean t)
    kk := toFloat64 r.n
    0.0 - 0.5 * kk * elementary.log (2.0 * pi * dot r r / kk) - 0.5 * kk },
  score := fn y t {
    r := sub y (m.mean t)
    scale (toFloat64 r.n / dot r r) (matVec (transpose (m.jac t)) r) },
  info := fn y t {
    r := sub y (m.mean t)
    j := m.jac t
    mscale (toFloat64 r.n / dot r r) (matMul (transpose j) j) },
}

-- a mean model with sigma known, u = log sigma a constant of the model and its gradient zero:
-- what experiment_zero.lut builds for `known s` (:89)
fixedSigma (n : Nat) (m : MeanModel n) (u : Float64) : ScaledModel n :=
  { model := m, logSigma := fn s { u }, dLogSigma := fn s { zeros n } }

-- The laws of the construction, per model (7.R4: a record of functions has no generator; the
-- test binds the model). The full log-likelihood is greatest at the mean, exactly: there the
-- residual is zero and elsewhere a non-negative quantity is subtracted, which rounding keeps
-- (11.S4, monotone).
-- spec 4.R10
GaussianPeaksAtMean (n : Nat) (m : ScaledModel n) (t : VecOf n) (y : VecOf m.model.k) : Bool :=
  (gaussian n m).loglik (m.model.mean t) t >= (gaussian n m).loglik y t
-- The profile likelihood is the full one at the sigma that maximizes it, u* = 1/2 log (RSS / K),
-- held fixed: equal in value, score and information within the tolerance (distances.lut of the
-- slice stated it for its model; here for any mean model)
-- spec 11.S18
ProfiledIsGaussianAtItsSigma (n : Nat) (m : MeanModel n) (tol : Tolerance) (t : VecOf n) (y : VecOf m.k) : Bool :=
  { r := sub y (m.mean t)
    ustar := 0.5 * elementary.log (dot r r / toFloat64 r.n)
    fixed := gaussian n (fixedSigma n m ustar)
    prof := profiled n m
    within tol (prof.loglik y t) (fixed.loglik y t)
    and approxVec tol (prof.score y t) (fixed.score y t)
    and approxMat tol (prof.info y t) (fixed.info y t) }

-- ---------------------------------------------------------------- §5 Uniform values

-- the distribution function of the standard normal, by erf, and the probability of a departure
-- beyond z standard errors on either side (v0.1 probability.lut:36-38)
sqrt2 : Float64 := 1.4142135623730951
normalCdf (x : Float64) : Float64 := 0.5 * (1.0 + elementary.erf (x / sqrt2))
normalTail (z : Float64) : Float64 := 1.0 - elementary.erf (z / sqrt2)

-- the sums of u and u^2 over every entry of a list of vectors, and how many entries: a triple,
-- as v0.1 gave it (probability.lut:57-58) and experiment_zero.lut matches it
valueSums (vs : List (Vec Float64)) : Float64 * Float64 * Int :=
  match vs {
    nil -> (0.0, 0.0, 0) ;
    cons u rest -> match valueSums rest { (s1, s2, c) -> (s1 + sumTo u.n (fn k { u.f k }), s2 + dot u u, c + u.n) } }

-- Kolmogorov's distance of the values from the uniform on [0, 1]: on the values sorted, the
-- largest of i/n - u_i and u_i - (i - 1)/n, zero on no values. The native definition sorts by
-- insertion (v0.1 probability.lut:63-76).
entriesOnto (v : Vec Float64) (k : Nat) (tail : List Float64) : List Float64 :=
  if k >= v.n then tail else cons (v.f k) (entriesOnto v (k + 1) tail)
pooled (vs : List (Vec Float64)) : List Float64 := match vs { nil -> nil ; cons v rest -> entriesOnto v 0 (pooled rest) }
insertSorted (x : Float64) (xs : List Float64) : List Float64 :=
  match xs { nil -> cons x nil ; cons y ys -> if x <= y then cons x xs else cons y (insertSorted x ys) }
sortedValues (xs : List Float64) : List Float64 := match xs { nil -> nil ; cons y ys -> insertSorted y (sortedValues ys) }
larger (a b : Float64) : Float64 := if a > b then a else b
kolmogorovFrom (n i : Int) (us : List Float64) (acc : Float64) : Float64 :=
  match us {
    nil -> acc ;
    cons u rest -> {
      a := toFloat64 i / toFloat64 n - u
      b := u - toFloat64 (i - 1) / toFloat64 n
      kolmogorovFrom n (i + 1) rest (larger acc (larger a b)) } }
lengthOf (xs : List Float64) : Int := match xs { nil -> 0 ; cons x rest -> 1 + lengthOf rest }
kolmogorovDistanceDef (vs : List (Vec Float64)) : Float64 :=
  { us := sortedValues (pooled vs)
    kolmogorovFrom (lengthOf us) 1 us 0.0 }
reverseOnto (vs acc : List (Vec Float64)) : List (Vec Float64) := match vs { nil -> acc ; cons v rest -> reverseOnto rest (cons v acc) }

-- the values the distance is stated on: in [0, 1], where it is bounded by one; a list of such
-- vectors is a subtype of the list (not a list of a subtype), so that it refines the leaf's domain
unitVec (v : Vec Float64) : Bool := forallBelow v.n (fn k { 0.0 <= v.f k and v.f k <= 1.0 })
allUnit (vs : List (Vec Float64)) : Bool := match vs { nil -> true ; cons v rest -> unitVec v and allUnit rest }
UnitList : U := { vs : List (Vec Float64) | allUnit vs }
UnitValue : U := { u : Float64 | 0.0 <= u and u <= 1.0 }
single (u : Float64) : List (Vec Float64) := cons (vec Float64 1 (fn k { u })) nil

-- The distance as a theory of one leaf (numpy's sort, probability_model.lut). Characterized:
-- zero on no values; on one value `max u (1 - u)`, exactly; of the multiset, so the list reversed
-- gives the same, exactly; within [0, 1] on unit values; and equal to the native definition
-- exactly, the same operations on the same sorted values in the same order (v0.1 certified the
-- exact agreement, probability_python.lut), so a tolerance is not taken.
-- spec 4.R10
Kolmogorov : { distance : List (Vec Float64) -> Float64 }
KolmogorovOfNothing (d : Kolmogorov) : Bool := d.distance nil == 0.0
KolmogorovOfOne (d : Kolmogorov) (u : UnitValue) : Bool := d.distance (single u) == larger u (1.0 - u)
KolmogorovOfMultiset (d : Kolmogorov) (vs : UnitList) : Bool := d.distance vs == d.distance (reverseOnto vs nil)
KolmogorovBounded (d : Kolmogorov) (vs : UnitList) : Bool := 0.0 <= d.distance vs and d.distance vs <= 1.0
KolmogorovAgrees (d : Kolmogorov) (vs : UnitList) : Bool := d.distance vs == kolmogorovDistanceDef vs
Kolmogorov := KolmogorovOfNothing & KolmogorovOfOne & KolmogorovOfMultiset & KolmogorovBounded & KolmogorovAgrees

-- Kolmogorov's limit of the tail P(sqrt n D > x), 2 sum_k (-1)^(k-1) exp(-2 k^2 x^2), with
-- Stephens's correction for a finite n, x = (sqrt n + 0.12 + 0.11 / sqrt n) D (Stephens, JRSS B
-- 32, 1970); one below x = 0.2, where the series is slow and the tail is above 1 - 1e-13.
-- [proposed] The truncation of the series (100 terms, from x = 0.2) is the precision of the
-- definition, below what a double resolves, and not a criterion a demand would set, so it is
-- written here and not taken as a parameter (P11 read on criteria).
tailSeriesTerms : Int := 100
tailSeriesFrom : Float64 := 0.2
kolmogorovTail (x : Float64) : Float64 :=
  if x < tailSeriesFrom then 1.0
  else 2.0 * sumTo tailSeriesTerms (fn k { (if k mod 2 == 0 then 1.0 else -1.0) * elementary.exp (-2.0 * toFloat64 ((k + 1) * (k + 1)) * x * x) })

-- the tail probability of the distance of n values, with Stephens's correction: the p-value of
-- the values against the uniform on [0, 1]; one on no values
uniformPValue (d : Kolmogorov) (vs : List (Vec Float64)) : Float64 :=
  match valueSums vs { (s1, s2, count) ->
    if count < 1 then 1.0
    else { q := elementary.sqrt (toFloat64 count)
           kolmogorovTail ((q + 0.12 + 0.11 / q) * d.distance vs) } }

-- A statistical law declares its level (7.S17, 6.S5): the values are uniform on [0, 1] at the
-- level alpha when the tail probability of their Kolmogorov distance is not below alpha; the
-- level is the demand's (`Level` of generators.lth, as `UniformAtLevel` there), and as a Bool law
-- it holds on a fraction 1 - alpha of calibrated samples, which is what its certificate says.
UniformAtLevel (d : Kolmogorov) (l : Level) (vs : UnitList) : Bool := uniformPValue d vs >= l.alpha
````

### `probability_model.lut`

````
-- probability_model.lut: numpy's sort as the model of `Kolmogorov` (probability.lth §5), and the
-- distance bound to it by name.
--
-- Draft 0, 2026-10-14, by Claude Fable 5.1, an agent of the coordinating session, on the brief
-- record/IA/slice-theories-2-2026-10-14/prompt.md (item 1; inventory row 24). A model file
-- (12.S23): one value of the theory, its field a route to the host (3.S40, 10.S8), certified
-- against probability.lth §5 like any extern (10.S10). The host code is
-- src/luthier/arrays.py `kolmogorov_distance`, which survives from v0.1 (probability_python.lut
-- at the tag v0.1-final bound the same route) and computes the native definition's operations
-- on the values sorted, so `KolmogorovAgrees` is exact. What crosses: a Luthier `List (Vec
-- Float64)`, each vector's `f` materialized over `Fin n` (3.S23), as a Python list of arrays;
-- back, a float. The Gaussian construction has no model here: `gaussian` and `profiled` are
-- native, over the leaves of arrays_model.lut; v0.1's `normalVec` (the sampler's normals) is
-- not bound, since probability.lth states no theory for it yet.

import "probability.lth" Kolmogorov Vec

numpySort : Kolmogorov := {
  distance := extern "python:luthier.arrays.kolmogorov_distance",
}

-- the leaf by name, as experiment_zero.lut calls it (:161)
kolmogorovDistance : List (Vec Float64) -> Float64 := numpySort.distance
````

### `belief.lth`

````
-- belief.lth: a Gaussian belief about a parameter in information form, the maximizer Laplace's
-- update needs, stated as a theory so that the host's can be validated, and the update itself.
--
-- Draft 0, 2026-10-14, by Claude Fable 5.1, an agent of the coordinating session, on the brief
-- record/IA/slice-theories-2-2026-10-14/prompt.md (item 2; inventory §6 item 7, row 22; the
-- callback crossing of D-2026-10-14-a). Sources: spec 7.R2 (over `VecOf n`), 3.S23 as it stands
-- (a Luthier lambda passed to the host is a callback; a record whose fields are functions
-- crosses as the record), 10.S8 to 10.S10 (an extern is a route, validated against its type's
-- laws at the first action that asks for it), 11.S18 (a tolerance is the demand's), 7.R4 (a law
-- over the models of a theory is certified per model), 4.R10, P11 (every criterion is a
-- parameter: the maximizer's tolerance, budget and floor). The v0.1 file is `belief.lut` at the
-- tag v0.1-final (lines 110-136 are what the slice uses); the names are its. What is not here:
-- v0.1's `BeliefFamily`, `Discrete`, the evidence and the calibration laws, which need a
-- sampler and the generator of normals probability.lth lacks; and `laplaceEvidence`, which
-- needs a log-determinant no leaf gives.
--
-- What this file states. A Gaussian belief on the vectors of dimension n is a mean and a
-- precision, the inverse covariance; zero precision along a direction is a belief that knows
-- nothing there, how the gauge of the positions enters without inventing a scale. Its laws: the
-- precision is symmetric and its log density is greatest at the mean (the precision is not
-- negative on any direction). A maximizer is a theory of one function: given the settings, the
-- objective with its score and its information on the vectors of a dimension and a start, it
-- gives where it stopped and whether it converged there (v0.1's `Maximizer` was a bare function
-- type with its laws in optimization.lut; here the laws are the type's, so that 10.S10 can
-- validate the host's `lm.maximize`, belief_model.lut, at its first action). The laws: the
-- objective does not fall from the start; where it says it converged the Newton decrement, half
-- of g^T M^+ g at the settings' floor, is within the settings' tolerance; the dimension is kept;
-- and on a concave quadratic, whose maximum is known, it converges. The first three are stated
-- over any `Posterior`, a record of functions with no generator, so they are certified per
-- problem (7.R4, listed cases); the quadratic family has the generators of `VecOf n` and
-- `Positive`, so it is sampled. Laplace's update is then a definition on the parts: the new mean
-- is the maximizer's `x` on belief times likelihood, the new precision the prior's plus the
-- information there; its laws are those of its parts (L9.2) and none is restated.
--
-- Index (all sections written in this draft):
--   §1 `GaussianBelief`, `gaussianLogDensity`, the laws of a belief (v0.1 belief.lut:110-116). done
--   §2 `Settings`, `MaxResult`, `Posterior`, `Maximizer` and the laws a maximizer must meet
--      (v0.1 belief.lut:118-122, optimization.lut:118-128).                                   done
--   §3 Laplace's update: `laplacePosterior`, `laplaceMode`, `laplaceAt`, `laplaceUpdate`
--      (v0.1 belief.lut:124-136).                                                              done

import "numbers.lth" Tolerance Positive within withinOf abs
import "arrays.lth" Vec Mat VecOf MatOf Dim vec mat identity approxVec approxMat exact RankFloor
import "arrays_model.lut" numpy : Arrays add sub scale dot norm matVec matMul madd mscale transpose pinvSym
import "probability.lth" Likelihood Resolution IsGradient

-- ---------------------------------------------------------------- §1 Gaussian beliefs

-- Information form on the vectors of dimension n: the mean and the precision, n x n. The log
-- density, up to its constant (v0.1 belief.lut:113-116).
GaussianBelief (n : Nat) : { mean : VecOf n, precision : MatOf n n }
gaussianLogDensity (n : Nat) (b : GaussianBelief n) (t : VecOf n) : Float64 :=
  { d := sub t b.mean
    0.0 - 0.5 * dot d (matVec b.precision d) }

-- the precision is symmetric within the tolerance, and the log density is greatest at the mean:
-- zero there, and elsewhere minus half a quadratic form that is not negative beyond rounding
-- (the precision is positive semidefinite, read through the density, which is what the belief
-- says; a zero direction is allowed, the belief knows nothing there)
-- spec 11.S18
PrecisionSymmetric (n : Nat) (b : GaussianBelief n) (tol : Tolerance) : Bool := approxMat tol b.precision (transpose b.precision)
DensityPeaksAtMean (n : Nat) (b : GaussianBelief n) (tol : Tolerance) (t : VecOf n) : Bool :=
  { q := gaussianLogDensity n b t
    gaussianLogDensity n b b.mean == 0.0 and (q <= 0.0 or within tol q 0.0) }
GaussianBelief (n : Nat) := PrecisionSymmetric n & DensityPeaksAtMean n

-- ---------------------------------------------------------------- §2 The maximizer (3.S23, 10.S10, P11)

-- The settings a maximizer runs with, the demand's (P11; experiment_zero.lut:98 took `tol` and
-- `maxIter` from its parameters): the tolerance of the decrement at which it has converged, the
-- budget of iterations, and the floor of the step matrix's spectrum below which a direction is
-- not stepped nor counted in the decrement. [proposed] The floor is the third setting (v0.1's
-- `solve` inverted the matrix whole, and raised where it was singular).
Settings : U := { tol : Positive, maxIter : Nat, floor : RankFloor | 0.0 < tol and 0 < maxIter and 0.0 <= floor }

-- where a maximizer stopped on the vectors of dimension n, and whether it converged there (a
-- method with a budget can run out of it before the gradient vanishes, and says so)
MaxResult (n : Nat) = { x : VecOf n, converged : Bool }

-- What a maximizer is given: a log posterior with its score and its information on the vectors
-- of dimension n, as three functions (what crosses to the host, each a callback, D-2026-10-14-a).
-- The laws: the score is the gradient of the log posterior at the demand's resolution, the
-- information symmetric. Certified per posterior (7.R4).
Posterior (n : Nat) : { logp : VecOf n -> Float64, score : VecOf n -> Vec Float64, info : VecOf n -> Mat Float64 }
PosteriorScoreIsGradient (n : Nat) (p : Posterior n) (r : Resolution) (t : VecOf n) : Bool := IsGradient n r p.logp p.score t
PosteriorInfoSymmetric (n : Nat) (p : Posterior n) (tol : Tolerance) (t : VecOf n) : Bool := approxMat tol (p.info t) (transpose (p.info t))
Posterior (n : Nat) := PosteriorScoreIsGradient n & PosteriorInfoSymmetric n

-- the Newton decrement of a log posterior at x: half of g^T M^+ g, the increase the information
-- predicts to the maximum, with the pseudo-inverse at the settings' floor (v0.1
-- optimization.lut:51 solved the matrix whole)
decrement (n : Nat) (s : Settings) (g : VecOf n -> Vec Float64) (m : VecOf n -> Mat Float64) (x : VecOf n) : Float64 :=
  { gx := g x
    0.5 * dot gx (matVec (pinvSym s.floor (m x)) gx) }

-- A maximizer: the settings, the dimension, the log posterior, its score, its information and a
-- start in; where it stopped and whether it converged out. It evaluates the functions only at
-- vectors of that dimension, which their types say (v0.1 belief.lut:122).
Maximizer : {
  maximize : Settings -> (n : Nat) -> (VecOf n -> Float64) -> (VecOf n -> Vec Float64) -> (VecOf n -> Mat Float64) -> VecOf n -> MaxResult n,
}

-- what any maximizer must meet, on any posterior (v0.1 optimization.lut:118-128): the log
-- posterior does not fall from the start; where it says it converged, the decrement there,
-- recomputed from the posterior and not from the run, is within the settings' tolerance; and
-- the dimension is kept. That it converges within its budget is a quality of the method on a
-- problem, not a law, except where the maximum is known: a concave quadratic, below.
-- spec 10.S10, P11
MaximizerAscends (mx : Maximizer) (s : Settings) (n : Dim) (p : Posterior n) (x0 : VecOf n) : Bool :=
  p.logp (mx.maximize s n p.logp p.score p.info x0).x >= p.logp x0
MaximizerStationary (mx : Maximizer) (s : Settings) (n : Dim) (p : Posterior n) (x0 : VecOf n) : Bool :=
  { r := mx.maximize s n p.logp p.score p.info x0
    if r.converged then decrement n s p.score p.info r.x <= s.tol else true }
MaximizerKeepsDimension (mx : Maximizer) (s : Settings) (n : Dim) (p : Posterior n) (x0 : VecOf n) : Bool :=
  (mx.maximize s n p.logp p.score p.info x0).x.n == n

-- the concave quadratic with its maximum at b and curvature c on every direction: the family
-- with generators (`VecOf n`, `Positive`), on which a maximizer converges within any budget that
-- is not tiny (Levenberg-Marquardt takes a handful of accepted steps on it) and ends at b within
-- the decrement's tolerance, c |x - b|^2 / 2 <= tol
quadratic (n : Nat) (b : VecOf n) (c : Positive) : Posterior n := {
  logp := fn x { d := sub x b
                 0.0 - 0.5 * c * dot d d },
  score := fn x { scale (0.0 - c) (sub x b) },
  info := fn x { mscale c (identity n) },
}
QuadraticConverges (mx : Maximizer) (s : Settings) (n : Dim) (b : VecOf n) (c : Positive) (x0 : VecOf n) : Bool :=
  { q := quadratic n b c
    r := mx.maximize s n q.logp q.score q.info x0
    d := sub r.x b
    r.converged and 0.5 * c * dot d d <= s.tol }
Maximizer := MaximizerAscends & MaximizerStationary & MaximizerKeepsDimension & QuadraticConverges

-- ---------------------------------------------------------------- §3 Laplace's update

-- belief times likelihood on datum y, as the posterior a maximizer is given: the log posterior
-- up to its constant, its score and its information, the prior's precision plus the
-- likelihood's (v0.1 belief.lut:127-131, the three lambdas of laplaceMode)
laplacePosterior (n : Nat) (l : Likelihood n) (b : GaussianBelief n) (y : Vec Float64) : Posterior n := {
  logp := fn t { gaussianLogDensity n b t + l.loglik y t },
  score := fn t { sub (l.score y t) (matVec b.precision (sub t b.mean)) },
  info := fn t { madd b.precision (l.info y t) },
}

-- Laplace's update: the new mean is the maximum of belief times likelihood, found from the
-- prior mean; the new precision the prior's plus the information the likelihood reports there
laplaceMode (n : Nat) (mx : Maximizer) (s : Settings) (l : Likelihood n) (b : GaussianBelief n) (y : Vec Float64) : MaxResult n :=
  { p := laplacePosterior n l b y
    mx.maximize s n p.logp p.score p.info b.mean }
-- the Gaussian belief at a mode m: mean m, precision the prior's plus the information there
laplaceAt (n : Nat) (l : Likelihood n) (b : GaussianBelief n) (y : Vec Float64) (m : VecOf n) : GaussianBelief n :=
  { mean := m, precision := madd b.precision (l.info y m) }
laplaceUpdate (n : Nat) (mx : Maximizer) (s : Settings) (l : Likelihood n) (b : GaussianBelief n) (y : Vec Float64) : GaussianBelief n :=
  laplaceAt n l b y (laplaceMode n mx s l b y).x
````

### `belief_model.lut`

````
-- belief_model.lut: the host's Levenberg-Marquardt as the model of `Maximizer` (belief.lth §2),
-- reached through the callback crossing, and the maximizer bound to it by name.
--
-- Draft 0, 2026-10-14, by Claude Fable 5.1, an agent of the coordinating session, on the brief
-- record/IA/slice-theories-2-2026-10-14/prompt.md (item 2; inventory row 22; D-2026-10-14-a).
-- A model file (12.S23): one value of the theory, its field a route to the host (3.S40, 10.S8),
-- validated against belief.lth §2 the first time an action asks for it (10.S10), its calls to
-- the three Luthier functions counted and recorded in the run's record (D-2026-10-14-a, 12.S18).
-- The host code is src/luthier/lm.py, the successor in this repository of sonolocalización's
-- src/lm.py (P7: the host code of the fit lives here); it does not exist yet, and the report
-- (record/IA/slice-theories-2-2026-10-14/report.md) says what it must do. What crosses in: the
-- settings as a record of three numbers; `n`; the three lambdas over `VecOf n` as callbacks,
-- each called with a numpy array and answering a float, an array or a matrix; the start as an
-- array. What crosses out: a record `{ x, converged }` read at `MaxResult n`. [proposed] The
-- route `luthier.lm.maximize` takes the settings as its first argument (v0.1's took `tol` and
-- `maxIter` apart, experiment_zero.lut:95 `fastMaximizer lm.tol lm.maxIter`); the damping
-- schedule of the method is the host's own (optimization.lth `Damping`), not a setting of the
-- maximizer.

import "belief.lth" Maximizer Settings MaxResult
import "arrays.lth" Vec Mat VecOf

lm : Maximizer := {
  maximize := extern "python:luthier.lm.maximize",
}

-- the maximizer by name, as experiment_zero.lut will call it through laplaceMode (:116)
maximize : Settings -> (n : Nat) -> (VecOf n -> Float64) -> (VecOf n -> Vec Float64) -> (VecOf n -> Mat Float64) -> VecOf n -> MaxResult n := lm.maximize
````

### `optimization.lth`

````
-- optimization.lth: Levenberg-Marquardt as types with laws over the array leaves: the objective
-- as a record of functions, the damping and the state of a run, one step as a theory whose
-- model is the host's or the native one, and the native driver.
--
-- Draft 0, 2026-10-14, by Claude Fable 5.1, an agent of the coordinating session, on the brief
-- record/IA/slice-theories-2-2026-10-14/prompt.md (item 3; inventory §6 item 7; the record of
-- functions crossing of D-2026-10-14-a). Sources: spec 7.R2 (over `VecOf n`), 3.S23 as it
-- stands (a record whose fields are functions crosses as the record, each a callback), 10.S10
-- (an extern validated against its type's laws), 11.S18 (a tolerance is the demand's), 7.R4
-- (per model), 4.R10, P11 (every criterion is a parameter: the damping schedule, v0.1's
-- `muInit`, `muFactor`, `muMin`, `muMax`, and the settings of belief.lth). The v0.1 file is
-- `optimization.lut` at the tag v0.1-final; the names are its. The settings (tolerance, budget,
-- floor) and the decrement are belief.lth's, so that one `Settings` serves the maximizer and
-- the step; `pinvSym` and `trace` are arrays.lth's (added for this file, one commit each).
--
-- What this file states. An objective is what is minimized: a value on the vectors of a
-- dimension, its gradient and a positive step matrix (the information, or Gauss-Newton); its
-- laws tie the gradient to the value and ask the step matrix symmetric and not negative. The
-- algorithm is split into pieces that each carry a law: the damped direction, (M + mu diag M)^+
-- applied to -g at the settings' floor; one step, a trial that either accepts (the value falls,
-- the damping divides by the factor, not below the least) or rejects (the point and the value
-- stay, the damping multiplies by the factor); `finished` says why a run stops (converged by the
-- decrement, exhausted by the budget, stalled by the damping beyond its most); the driver
-- iterates the step until it does. `LMStep` is the theory of the direction and the step, with
-- the laws above and the descent of the direction; its models are the native definitions and
-- the host's (optimization_model.lut). Correctness does not depend on the path: a run that ends
-- converged is certified by the decrement at its end, recomputed from the objective, which is
-- the law `MaximizerStationary` of belief.lth on the native runner (optimization_model.lut
-- `lmMaximizer`).
--
-- Index (all sections written in this draft):
--   §1 `Objective`, its laws, `negate`, `posteriorOf` (v0.1 optimization.lut:16-24, 108-110). done
--   §2 `Damping`, `LMState`, `start`, `dampedStep`, `lmStep`, `Reason`, `finished`, `Run`,
--      `minimize` (v0.1 optimization.lut:27-73).                                              done
--   §3 `LMStep`, the laws of a step: descent, the damping, the decrease; the quadratic family
--      (v0.1 optimization.lut:76-92).                                                         done

import "numbers.lth" Tolerance Positive within withinOf abs
import "arrays.lth" Vec Mat VecOf MatOf Dim vec mat identity approxVec approxMat exact RankFloor
import "arrays_model.lut" numpy : Arrays add sub scale dot norm matVec matMul madd mscale transpose pinvSym
import "probability.lth" Resolution IsGradient
import "belief.lth" Settings Posterior decrement quadratic

-- ---------------------------------------------------------------- §1 The objective (D-2026-10-14-a)

-- A record whose fields are functions (what crosses to the host as the record with each field
-- a callback, D-2026-10-14-a): the value on the vectors of dimension n, its gradient and the
-- step matrix. The gradient is the gradient of the value at the demand's resolution; the step
-- matrix is symmetric and its quadratic form not negative beyond rounding. Whether it
-- approximates the Hessian is a quality of the method, not a law of the objective (v0.1
-- optimization.lut:18-24). Certified per objective (7.R4), and on the quadratic family below.
Objective (n : Nat) : { value : VecOf n -> Float64, grad : VecOf n -> Vec Float64, stepMatrix : VecOf n -> Mat Float64 }
-- spec 7.R2, 11.S18
GradIsGradient (n : Nat) (o : Objective n) (r : Resolution) (x : VecOf n) : Bool := IsGradient n r o.value o.grad x
StepMatrixSymmetric (n : Nat) (o : Objective n) (tol : Tolerance) (x : VecOf n) : Bool :=
  approxMat tol (o.stepMatrix x) (transpose (o.stepMatrix x))
StepMatrixNonNegative (n : Nat) (o : Objective n) (tol : Tolerance) (x v : VecOf n) : Bool :=
  { q := dot v (matVec (o.stepMatrix x) v)
    0.0 <= q or within tol q 0.0 }
Objective (n : Nat) := GradIsGradient n & StepMatrixSymmetric n & StepMatrixNonNegative n

-- a log posterior (belief.lth) as the objective that minimizes its negative, the information
-- its step matrix (v0.1 optimization.lut:108-110); and the three functions a maximizer takes,
-- as one posterior
negate (n : Nat) (p : Posterior n) : Objective n :=
  { value := fn x { 0.0 - p.logp x }, grad := fn x { scale (0.0 - 1.0) (p.score x) }, stepMatrix := p.info }
posteriorOf (n : Nat) (f : VecOf n -> Float64) (g : VecOf n -> Vec Float64) (m : VecOf n -> Mat Float64) : Posterior n :=
  { logp := f, score := g, info := m }

-- ---------------------------------------------------------------- §2 The damping and the state (P11)

-- The damping schedule, the method's own, a parameter (P11; v0.1 held `muInit := 0.001`,
-- `muFactor := 3.0`, `muMin := 1e-15`, `muMax := 1e15` as constants, optimization.lut:29-32):
-- the damping a run starts at, the factor it divides by on acceptance and multiplies by on
-- rejection, the least it falls to, and the most beyond which the run has stalled.
Damping : U := { init factor least most : Float64 | 0.0 < least and least <= init and init <= most and 1.0 < factor }

-- the state of a run on the vectors of dimension n: the point, its value, the damping, the
-- iterations so far, and whether the last trial was accepted (v0.1 optimization.lut:27)
LMState (n : Nat) = { x : VecOf n, phi : Float64, mu : Float64, iter : Int, accepted : Bool }

start (n : Nat) (o : Objective n) (d : Damping) (x0 : VecOf n) : LMState n :=
  { x := x0, phi := o.value x0, mu := d.init, iter := 0, accepted := true }

-- the diagonal part of a matrix
diagOf (m : Mat Float64) : Mat Float64 := mat Float64 m.m m.n (fn i j { if i == j then m.f i i else 0.0 })

-- the damped direction: (M + mu diag M)^+ applied to -g, the pseudo-inverse at the settings'
-- floor (v0.1 optimization.lut:51 solved the matrix whole)
dampedStep (n : Nat) (s : Settings) (o : Objective n) (x : VecOf n) (mu : Float64) : Vec Float64 :=
  { m := o.stepMatrix x
    scale (0.0 - 1.0) (matVec (pinvSym s.floor (madd m (mscale mu (diagOf m)))) (o.grad x)) }

-- the damping after an acceptance: divided by the factor, not below the least
lowered (d : Damping) (mu : Float64) : Float64 := if mu / d.factor > d.least then mu / d.factor else d.least

-- one trial: the value at the damped step is taken if it falls, and the damping lowered; else
-- the point and the value stay and the damping is raised (v0.1 optimization.lut:54-59)
lmStep (n : Nat) (s : Settings) (d : Damping) (o : Objective n) (st : LMState n) : LMState n :=
  { xt := add st.x (dampedStep n s o st.x st.mu)
    pt := o.value xt
    if pt < st.phi
    then { x := xt, phi := pt, mu := lowered d st.mu, iter := st.iter + 1, accepted := true }
    else { x := st.x, phi := st.phi, mu := st.mu * d.factor, iter := st.iter + 1, accepted := false } }

-- why a run stops: converged when the decrement is below the settings' tolerance, exhausted by
-- the budget, stalled by the damping beyond its most; running otherwise (v0.1
-- optimization.lut:63-69)
Reason = { running : Unit || converged : Unit || exhausted : Unit || stalled : Unit }
isConverged (r : Reason) : Bool := match r { converged u -> true ; _ -> false }
finished (n : Nat) (s : Settings) (d : Damping) (o : Objective n) (st : LMState n) : Reason :=
  if decrement n s o.grad o.stepMatrix st.x < s.tol then converged unit
  else if st.iter >= s.maxIter then exhausted unit
  else if st.mu > d.most then stalled unit
  else running unit

Run (n : Nat) = { state : LMState n, reason : Reason }

-- the native driver: the step iterated until the run is finished (v0.1 optimization.lut:72-73)
minimize (n : Nat) (s : Settings) (d : Damping) (o : Objective n) (st : LMState n) : Run n :=
  match finished n s d o st {
    running u -> minimize n s d o (lmStep n s d o st) ;
    r -> { state := st, reason := r } }

-- ---------------------------------------------------------------- §3 The laws of a step (10.S10)

-- The direction and the step as a theory of two functions, so that the host's (lm.step,
-- optimization_model.lut) is validated against them at its first action (10.S10) and the native
-- definitions above are its other model. The laws: the direction descends (its inner product
-- with the gradient is not positive beyond rounding) and agrees with the native one within the
-- demand's tolerance; a step accepted lowers the value, takes the point along the direction,
-- lowers the damping by the schedule, and counts the iteration; a step rejected keeps the point
-- and the value, raises the damping by the factor, and counts the iteration; and on a concave
-- quadratic the first step from the start is accepted unless the start is the minimum.
LMStep : {
  direction : (n : Nat) -> Settings -> Objective n -> VecOf n -> Float64 -> Vec Float64,
  step : (n : Nat) -> Settings -> Damping -> Objective n -> LMState n -> LMState n,
}
-- spec 11.S18
DirectionDescends (m : LMStep) (tol : Tolerance) (s : Settings) (n : Dim) (o : Objective n) (x : VecOf n) (mu : Positive) : Bool :=
  { q := dot (o.grad x) (m.direction n s o x mu)
    q <= 0.0 or within tol q 0.0 }
DirectionAgrees (m : LMStep) (tol : Tolerance) (s : Settings) (n : Dim) (o : Objective n) (x : VecOf n) (mu : Positive) : Bool :=
  approxVec tol (m.direction n s o x mu) (dampedStep n s o x mu)
-- spec P11 (the damping is the schedule's)
StepRule (m : LMStep) (s : Settings) (d : Damping) (n : Dim) (o : Objective n) (st : LMState n) : Bool :=
  { s2 := m.step n s d o st
    if s2.accepted
    then s2.phi < st.phi and approxVec exact s2.x (add st.x (m.direction n s o st.x st.mu))
         and s2.mu == lowered d st.mu and s2.iter == st.iter + 1
    else approxVec exact s2.x st.x and s2.phi == st.phi and s2.mu == st.mu * d.factor and s2.iter == st.iter + 1 }
-- the quadratic family of belief.lth, minimized: its minimum at b, curvature c
quadraticObjective (n : Nat) (b : VecOf n) (c : Positive) : Objective n := negate n (quadratic n b c)
QuadraticStepAccepts (m : LMStep) (s : Settings) (d : Damping) (n : Dim) (b : VecOf n) (c : Positive) (x0 : VecOf n) : Bool :=
  { o := quadraticObjective n b c
    norm (sub x0 b) == 0.0 or (m.step n s d o (start n o d x0)).accepted }
LMStep := DirectionDescends & DirectionAgrees & StepRule & QuadraticStepAccepts
````

### `optimization_model.lut`

````
-- optimization_model.lut: the two models of `LMStep` (optimization.lth §3), the native
-- definitions and the host's Levenberg-Marquardt reached through the record crossing, and the
-- native driver as a model of belief.lth's `Maximizer`.
--
-- Draft 0, 2026-10-14, by Claude Fable 5.1, an agent of the coordinating session, on the brief
-- record/IA/slice-theories-2-2026-10-14/prompt.md (item 3; D-2026-10-14-a). A model file
-- (12.S23): values of the theories, certified against optimization.lth §3 and belief.lth §2
-- (10.S10); the host's fields are routes (3.S40, 10.S8) to src/luthier/lm.py, the successor in
-- this repository of sonolocalización's src/lm.py (P7), not yet written; the report says what
-- it must do. What crosses to the host's step: `n`, the settings and the damping as records of
-- numbers, the objective as a record whose three fields are callbacks (D-2026-10-14-a), the
-- state as a record of an array and numbers; back, a record read at `LMState n`. The native
-- model is the one the host's is compared with (`DirectionAgrees`; the step's laws determine
-- the step from the direction, so agreement of the steps is a corollary, 4.R10).

import "belief.lth" Maximizer Settings MaxResult
import "optimization.lth" LMStep Objective Damping LMState Run dampedStep lmStep minimize start negate posteriorOf isConverged
import "arrays.lth" Vec Mat VecOf

-- the native definitions, as one model
native : LMStep := { direction := dampedStep, step := lmStep }

-- the host's, routes to lm.py
host : LMStep := {
  direction := extern "python:luthier.lm.damped_step",
  step := extern "python:luthier.lm.step",
}

-- the native driver as a maximizer of belief.lth: the negative of the log posterior minimized
-- from the start, with the damping given (P11); converged when the run's reason says so
-- (v0.1 optimization.lut:112-115)
lmMaximizer (d : Damping) : Maximizer := {
  maximize := fn s n f g m x0 {
    o := negate n (posteriorOf n f g m)
    r := minimize n s d o (start n o d x0)
    res := { x := r.state.x, converged := isConverged r.reason }
    res },
}
````

### `arrays.lth`

````
-- arrays.lth: vectors and matrices as functions on indices, the folds over the indices, the
-- native definitions of the operations, and the laws the host's leaves must meet.
--
-- Draft 0, 2026-10-14, by Claude Fable 5.1, an agent of the coordinating session, on the brief
-- record/IA/slice-theories-2026-10-14/prompt.md (item 2 of the inventory's §6) and the answers
-- of the sonolocalización session (record/IA/sonolocalizacion-inventory-2026-10-13/
-- answers-2026-10-14.md: the names the first stage uses). Sources: spec 11.S9 (`Array`, `Vec`,
-- `Mat` as records), 3.S21 to 3.S28 (a numpy array is a value of `Fin n -> Float64`, the four
-- rules of the bridge, the order of a sum, what is certified at the bridge), 11.S14 (a sum of n
-- terms is within gamma n of the exact one relative to the sum of the magnitudes; likewise an
-- inner product), 11.S18 (the tolerance is the demand's: the law takes it, D-2026-10-12-h),
-- 4.R10 (a law characterizes; agreement with a native definition is a corollary), 12.S9 (the
-- pattern of a library: native definitions here, the host's leaves as a model), P11 (every
-- criterion is a parameter: the rank floor). The v0.1 files are `array.lut`, `array_python.lut`
-- and the folds of `algebra.lut` at the tag v0.1-final; the names below are theirs, so that the
-- port of positions.lut and distance_graph.lut is a rename at most.
--
-- What this file states. A vector is `{ n, f }` and a matrix `{ m, n, f }` (11.S9); a numpy
-- array is a value of `f` as it is (3.S21). The operations are defined natively through the
-- entries (`dotDef`, `matMulDef`, ...); `Arrays` is the theory of the leaves the host computes
-- faster, a record of operations (the pattern of kernel_laws.lth) whose laws are exact where the
-- operation is entrywise (the host does the same machine operation entry by entry) and within
-- the demand's tolerance where it sums (11.S14: relative to the sum of the magnitudes of the
-- terms, never to the result, which can cancel). The retained rank takes its floor as a
-- parameter (P11; v0.1 wrote `n eps` inside the leaf, inventory row 13) and is characterized on
-- diagonals, by scale, by a bound, and under rotation; its model is arrays_model.lut. The square
-- root of `normDef` is the elementary functions' (numbers_model.lut), the one model this theory
-- names: [proposed], the alternative being a parameter `(e : Elementary)` on every norm.
--
-- Index (all sections written in this draft):
--   §1 The types: `Array`, `Vec`, `Mat`, their constructors, the shapes `Dim`, `VecOf`,
--      `MatOf`, `MatRows`, `Square`, `Symmetric` (11.S9; v0.1 array.lut:22-33).             done
--   §2 Folds over the indices: `sumTo` in the order of 3.S27, `sumToInt`, `forallBelow`,
--      `existsBelow`, `forallPairs`, `countBelow` (v0.1 algebra.lut:188-203).             done
--   §3 The native definitions, and the comparisons of arrays within a tolerance
--      (v0.1 array.lut:49-78, 351-352).                                                  done
--   §4 The leaves: `Arrays`, its laws, exact or within the demand's tolerance (3.S28,
--      11.S14, 11.S18); the retained rank with its floor (P11); the trace and the
--      pseudo-inverse of a symmetric matrix (added 2026-10-14 for the fit's theories,
--      record/IA/slice-theories-2-2026-10-14/prompt.md item 3).                           done

import "numbers.lth" Tolerance within withinOf abs Positive Elementary
import "numbers_model.lut" elementary : Elementary

-- ---------------------------------------------------------------- §1 The types (11.S9)

-- spec 11.S9: an array of length n is a function on the n indices; a vector carries its length,
-- a matrix its two
Array (A : U) (n : Nat) = Fin n -> A
Vec (A : U) = { n : Nat, f : Fin n -> A }
Mat (A : U) = { m : Nat, n : Nat, f : Fin m -> Fin n -> A }
-- the constructors: a vector from its length and its entries, a matrix from its shape and its
-- entries (v0.1 wrote the pair `(n, fn k { ... })`; a record is not a pair, D-2026-10-13-x)
vec (A : U) (n : Nat) (f : Fin n -> A) : Vec A := { n := n, f := f }
mat (A : U) (m n : Nat) (f : Fin m -> Fin n -> A) : Mat A := { m := m, n := n, f := f }

-- the shapes (v0.1 array.lut:26-33)
Dim : U := { n : Int | 1 <= n }
VecOf (k : Int) : U := { v : Vec Float64 | v.n == k }
MatOf (r c : Int) : U := { a : Mat Float64 | a.m == r and a.n == c }
MatRows (r : Int) : U := { a : Mat Float64 | a.m == r }
Square : U := { a : Mat Float64 | a.m == a.n }
-- symmetric exactly: what the spectral leaves take (the host reads one triangle)
Symmetric : U := { a : Mat Float64 | if a.m == a.n then forallPairs a.m (fn i j { a.f i j == a.f j i }) else false }
SymmetricOf (k : Int) : U := { s : Symmetric | s.m == k }

-- ---------------------------------------------------------------- §2 Folds over the indices

-- the fold of an operation with a unit over n terms, associated to the right:
-- `f 0 op (f 1 op (... op (f (n - 1) op unit)))`; no law claimed of the operation (v0.1
-- algebra.lut `foldWith`): what the doubles have, since they are not a monoid (11.S15)
foldFrom (A : U) (op : A -> A -> A) (unit : A) (n : Int) (lo : Nat) (f : Fin n -> A) : A :=
  if lo >= n then unit else op (f lo) (foldFrom A op unit n (lo + 1) f)
foldWith (A : U) (op : A -> A -> A) (unit : A) (n : Int) (f : Fin n -> A) : A := foldFrom A op unit n 0 f

-- spec 3.S27: the sum of n doubles is `f 0 + (f 1 + (... + (f (n - 1) + 0.0)))`; the order is
-- part of the definition, and any specimen keeps it
sumTo (n : Int) (f : Fin n -> Float64) : Float64 := foldWith Float64 (fn a b { a + b }) 0.0 n f
sumToInt (n : Int) (f : Fin n -> Int) : Int := foldWith Int (fn a b { a + b }) 0 n f
-- a law over every index, some index, every pair of indices below n: the closure, evaluated
forallBelow (n : Int) (p : Fin n -> Bool) : Bool := foldWith Bool (fn a b { a and b }) true n p
existsBelow (n : Int) (p : Fin n -> Bool) : Bool := foldWith Bool (fn a b { a or b }) false n p
forallPairs (n : Int) (p : Fin n -> Fin n -> Bool) : Bool := forallBelow n (fn i { forallBelow n (p i) })
countBelow (n : Int) (p : Fin n -> Bool) : Int := sumToInt n (fn k { if p k then 1 else 0 })
-- the sum of the magnitudes of n terms: the scale a rounded sum is compared at (11.S14)
absSumTo (n : Int) (f : Fin n -> Float64) : Float64 := sumTo n (fn k { abs (f k) })

-- ---------------------------------------------------------------- §3 The native definitions

-- vectors (v0.1 array.lut:49-54, 78)
zeros (n : Nat) : Vec Float64 := vec Float64 n (fn k { 0.0 })
ones (n : Nat) : Vec Float64 := vec Float64 n (fn k { 1.0 })
-- the j-th vector of the basis
basis (n : Nat) (j : Fin n) : Vec Float64 := vec Float64 n (fn k { if k == j then 1.0 else 0.0 })
dotDef (x : Vec Float64) (y : VecOf x.n) : Float64 := sumTo x.n (fn k { x.f k * y.f k })
normDef (x : Vec Float64) : Float64 := elementary.sqrt (dotDef x x)
addDef (x : Vec Float64) (y : VecOf x.n) : Vec Float64 := vec Float64 x.n (fn k { x.f k + y.f k })
subDef (x : Vec Float64) (y : VecOf x.n) : Vec Float64 := vec Float64 x.n (fn k { x.f k - y.f k })
scaleDef (c : Float64) (x : Vec Float64) : Vec Float64 := vec Float64 x.n (fn k { c * x.f k })
-- the metric of the Euclidean space: the norm of the difference (v0.1 array.lut:78)
distance (x : Vec Float64) (y : VecOf x.n) : Float64 := normDef (subDef x y)

-- matrices (v0.1 array.lut:51, 55-67)
identity (n : Nat) : Mat Float64 := mat Float64 n n (fn i j { if i == j then 1.0 else 0.0 })
zeroMat (m n : Nat) : Mat Float64 := mat Float64 m n (fn i j { 0.0 })
diagonal (d : Vec Float64) : Mat Float64 := mat Float64 d.n d.n (fn i j { if i == j then d.f i else 0.0 })
row (a : Mat Float64) (i : Fin a.m) : Vec Float64 := vec Float64 a.n (a.f i)
column (a : Mat Float64) (j : Fin a.n) : Vec Float64 := vec Float64 a.m (fn i { a.f i j })
matVecDef (a : Mat Float64) (x : VecOf a.n) : Vec Float64 := vec Float64 a.m (fn i { sumTo a.n (fn j { a.f i j * x.f j }) })
matMulDef (a : Mat Float64) (b : MatRows a.n) : Mat Float64 :=
  mat Float64 a.m b.n (fn i j { sumTo a.n (fn k { a.f i k * b.f k j }) })
transposeDef (a : Mat Float64) : Mat Float64 := mat Float64 a.n a.m (fn i j { a.f j i })
maddDef (a : Mat Float64) (b : MatOf a.m a.n) : Mat Float64 := mat Float64 a.m a.n (fn i j { a.f i j + b.f i j })
msubDef (a : Mat Float64) (b : MatOf a.m a.n) : Mat Float64 := mat Float64 a.m a.n (fn i j { a.f i j - b.f i j })
mscaleDef (c : Float64) (a : Mat Float64) : Mat Float64 := mat Float64 a.m a.n (fn i j { c * a.f i j })
-- the trace of a square matrix, the sum of its diagonal in the order of 3.S27 (v0.1 array.lut:70)
traceDef (a : Square) : Float64 := sumTo a.m (fn i { a.f i i })
-- the Frobenius norm, the root of the sum of the squares of the entries (v0.1 array.lut:75); a
-- bound on every eigenvalue in magnitude, which is what the pseudo-inverse's laws use it for
frobDef (a : Mat Float64) : Float64 := elementary.sqrt (sumTo a.m (fn i { sumTo a.n (fn j { a.f i j * a.f i j }) }))
-- the pseudo-inverse of a diagonal matrix at a floor: one over each entry above the floor times
-- the largest in magnitude, zero elsewhere (negative entries are never retained, as retainedRank
-- counts them)
pinvOfDiagonal (fl : RankFloor) (d : Vec Float64) : Mat Float64 :=
  { big := foldWith Float64 (fn a b { if a > b then a else b }) 0.0 d.n (fn k { abs (d.f k) })
    diagonal (vec Float64 d.n (fn k { if d.f k > fl * big then 1.0 / d.f k else 0.0 })) }

-- Functions have no structural equality (4.R8): arrays compare entry by entry, within the
-- tolerance given, and differ when their shapes do; with tolerance zero the comparison is exact.
-- Inside the branch the shapes agree, which is what lets `y.f` take `x`'s index (4.R11).
approxVec (tol : Tolerance) (x y : Vec Float64) : Bool :=
  if x.n == y.n then forallBelow x.n (fn k { within tol (x.f k) (y.f k) }) else false
approxMat (tol : Tolerance) (a b : Mat Float64) : Bool :=
  if a.m == b.m and a.n == b.n then forallPairs2 a.m a.n (fn i j { within tol (a.f i j) (b.f i j) }) else false
forallPairs2 (m n : Int) (p : Fin m -> Fin n -> Bool) : Bool := forallBelow m (fn i { forallBelow n (p i) })
exact : Tolerance := 0.0
-- the same comparison of matrices with a slack added to the tolerance's share: what a law states
-- when the two sides differ by a known amount (the part of a matrix below a floor) and rounding
approxMatSlack (slack : Float64) (tol : Tolerance) (a b : Mat Float64) : Bool :=
  if a.m == b.m and a.n == b.n then
    forallPairs2 a.m a.n (fn i j { abs (a.f i j - b.f i j) <= slack + tol * (1.0 + abs (a.f i j) + abs (b.f i j)) })
  else false

-- the same comparison with each entry's scale given: the entries differ by at most the tolerance
-- times the scale of that entry (what the sum compared adds in magnitude, 11.S14), so the
-- comparison follows the magnitudes and not a flat constant; the scale is a matrix of the shape
-- compared, else the comparison fails
-- [proposed, D-2026-10-14-c; 11.S14]
absMat (a : Mat Float64) : Mat Float64 := mat Float64 a.m a.n (fn i j { abs (a.f i j) })
approxMatOf (tol : Tolerance) (scale a b : Mat Float64) : Bool :=
  if a.m == b.m and a.n == b.n and scale.m == a.m and scale.n == a.n then
    forallPairs2 a.m a.n (fn i j { withinOf tol (scale.f i j) (a.f i j) (b.f i j) })
  else false
-- the same with a slack added: the known difference (the part dropped below a floor) plus the
-- tolerance times the scale of the entry [proposed, D-2026-10-14-c; 11.S14]
approxMatSlackOf (slack : Float64) (tol : Tolerance) (scale a b : Mat Float64) : Bool :=
  if a.m == b.m and a.n == b.n and scale.m == a.m and scale.n == a.n then
    forallPairs2 a.m a.n (fn i j { abs (a.f i j - b.f i j) <= slack + tol * scale.f i j })
  else false

-- ---------------------------------------------------------------- §4 The leaves (3.S28, 12.S9)

-- The operations the host computes faster, as one record: what a model of it must meet is below,
-- and arrays_model.lut names numpy's as the model. Each takes and gives the records of §1; the
-- bridge reads `f` as the array (3.S22 to 3.S24). The rank floor is a parameter of the rank
-- (P11, 11.S18): the retained eigenvalues of a symmetric matrix are those above the floor times
-- the largest in magnitude, so the floor is a fraction below one.
RankFloor : U := { f : Float64 | 0.0 <= f and f < 1.0 }
Arrays : {
  add sub : Vec Float64 -> Vec Float64 -> Vec Float64,
  scale : Float64 -> Vec Float64 -> Vec Float64,
  dot : Vec Float64 -> Vec Float64 -> Float64,
  norm : Vec Float64 -> Float64,
  matVec : Mat Float64 -> Vec Float64 -> Vec Float64,
  matMul madd msub : Mat Float64 -> Mat Float64 -> Mat Float64,
  mscale : Float64 -> Mat Float64 -> Mat Float64,
  transpose : Mat Float64 -> Mat Float64,
  retainedRank : RankFloor -> Mat Float64 -> Int,
  trace : Mat Float64 -> Float64,
  pinvSym : RankFloor -> Mat Float64 -> Mat Float64,
}

-- entrywise operations are exact: the host applies the machine's operation to each entry, which
-- is the native definition (11.S4), so the two agree bit for bit and the shape is the definition's
-- spec 3.S28
AddPointwise (m : Arrays) (n : Dim) (x y : VecOf n) : Bool := approxVec exact (m.add x y) (addDef x y)
SubPointwise (m : Arrays) (n : Dim) (x y : VecOf n) : Bool := approxVec exact (m.sub x y) (subDef x y)
ScalePointwise (m : Arrays) (n : Dim) (c : Float64) (x : VecOf n) : Bool := approxVec exact (m.scale c x) (scaleDef c x)
TransposePointwise (m : Arrays) (r c : Dim) (a : MatOf r c) : Bool := approxMat exact (m.transpose a) (transposeDef a)
MaddPointwise (m : Arrays) (r c : Dim) (a b : MatOf r c) : Bool := approxMat exact (m.madd a b) (maddDef a b)
MsubPointwise (m : Arrays) (r c : Dim) (a b : MatOf r c) : Bool := approxMat exact (m.msub a b) (msubDef a b)
MscalePointwise (m : Arrays) (r c : Dim) (s : Float64) (a : MatOf r c) : Bool := approxMat exact (m.mscale s a) (mscaleDef s a)

-- the inner product: symmetric exactly (the same products, summed in one order), the basis
-- orthonormal exactly (one term, the rest exact zeros), and within the demand's tolerance of the
-- native sum relative to the sum of the magnitudes of the terms (11.S14, 11.S18)
DotSymmetric (m : Arrays) (n : Dim) (x y : VecOf n) : Bool := m.dot x y == m.dot y x
DotOnBasis (m : Arrays) (n : Dim) (x : VecOf n) (j : Fin n) : Bool := m.dot x (basis n j) == x.f j
DotAgrees (m : Arrays) (tol : Tolerance) (n : Dim) (x y : VecOf n) : Bool :=
  withinOf tol (absSumTo n (fn k { x.f k * y.f k })) (m.dot x y) (dotDef x y)
-- the norm: the root of the inner product, one on the basis, scaling with the magnitude
NormOfBasis (m : Arrays) (n : Dim) (j : Fin n) : Bool := m.norm (basis n j) == 1.0
NormOfDot (m : Arrays) (tol : Tolerance) (n : Dim) (x : VecOf n) : Bool := within tol (m.norm x) (elementary.sqrt (m.dot x x))
NormScales (m : Arrays) (tol : Tolerance) (n : Dim) (c : Positive) (x : VecOf n) : Bool :=
  within tol (m.norm (m.scale c x)) (c * m.norm x)

-- a matrix acting: its table on the basis is the matrix, exactly; on any vector it is within
-- the tolerance of the native sum, row by row relative to the magnitudes of the row's terms
MatVecOnBasis (m : Arrays) (r c : Dim) (a : MatOf r c) (j : Fin c) : Bool := approxVec exact (m.matVec a (basis c j)) (column a j)
MatVecAgrees (m : Arrays) (tol : Tolerance) (r c : Dim) (a : MatOf r c) (x : VecOf c) : Bool :=
  if (m.matVec a x).n == r then
    forallBelow r (fn i { withinOf tol (absSumTo c (fn j { a.f i j * x.f j })) ((m.matVec a x).f i) ((matVecDef a x).f i) })
  else false
-- the product: the identity is neutral exactly, the transpose reverses it, and each entry is
-- within the tolerance of the native sum relative to the magnitudes of its terms (11.S14)
MatMulIdentity (m : Arrays) (r c : Dim) (a : MatOf r c) : Bool :=
  approxMat exact (m.matMul a (identity c)) a and approxMat exact (m.matMul (identity r) a) a
MatMulTransposes (m : Arrays) (tol : Tolerance) (r k c : Dim) (a : MatOf r k) (b : MatOf k c) : Bool :=
  approxMat tol (m.transpose (m.matMul a b)) (m.matMul (m.transpose b) (m.transpose a))
MatMulAgrees (m : Arrays) (tol : Tolerance) (r k c : Dim) (a : MatOf r k) (b : MatOf k c) : Bool :=
  if (m.matMul a b).m == r and (m.matMul a b).n == c then
    forallPairs2 r c (fn i j { withinOf tol (absSumTo k (fn l { a.f i l * b.f l j }))
                                        ((m.matMul a b).f i j) ((matMulDef a b).f i j) })
  else false

-- The retained rank of a symmetric matrix at a floor: the number of its eigenvalues above the
-- floor times the largest eigenvalue in magnitude. Characterized where the spectrum is read off
-- the matrix: a diagonal whose entries are zero or well above the floor has as many retained as
-- it has positive entries; the zero matrix none, the identity all; the rank is bounded by the
-- size, is the same at any positive scale (the floor is relative), and under rotation by an
-- orthogonal matrix (the spectrum is invariant), whose generator is a family of the model's
-- (7.S5, bound by the test, 7.R1). Agreement with a native spectrum (Jacobi's method, v0.1
-- array.lut:95-154) is a corollary (4.R10) and is not restated here.
-- spec 11.S18, P11
ClearFloor : U := { f : RankFloor | f < 0.001 }
ClearDiagonal : U := { d : Vec Float64 | forallBelow d.n (fn k { d.f k == 0.0 or (1.0 <= abs (d.f k) and abs (d.f k) <= 1000.0) }) }
Orthogonal (tol : Tolerance) (k : Int) : U := { q : MatOf k k | approxMat tol (matMulDef (transposeDef q) q) (identity k) }
RankOfDiagonal (m : Arrays) (fl : ClearFloor) (d : ClearDiagonal) : Bool :=
  m.retainedRank fl (diagonal d) == countBelow d.n (fn k { 0.0 < d.f k })
RankOfZeroAndIdentity (m : Arrays) (fl : RankFloor) (k : Dim) : Bool :=
  m.retainedRank fl (zeroMat k k) == 0 and m.retainedRank fl (identity k) == k
RankBounded (m : Arrays) (fl : RankFloor) (s : Symmetric) : Bool := 0 <= m.retainedRank fl s and m.retainedRank fl s <= s.m
RankScales (m : Arrays) (fl : RankFloor) (c : Positive) (s : Symmetric) : Bool :=
  m.retainedRank fl (mscaleDef c s) == m.retainedRank fl s
RankUnderRotation (m : Arrays) (tol : Tolerance) (fl : RankFloor) (k : Dim) (q : Orthogonal tol k) (s : SymmetricOf k) : Bool :=
  m.retainedRank fl (m.matMul (m.transpose q) (m.matMul s q)) == m.retainedRank fl s

-- The trace: of the identity its size, exactly (a sum of ones); linear and cyclic within the
-- demand's tolerance, the cyclic law relative to the magnitudes of the products summed (both
-- sides sum the same r c products in different orders, 11.S14); and within the tolerance of the
-- native sum relative to the magnitudes of the diagonal (v0.1 array.lut:247-252 held the
-- tolerance; here the demand gives it, 11.S18).
-- spec 11.S14, 11.S18
TraceOfIdentity (m : Arrays) (k : Dim) : Bool := m.trace (identity k) == toFloat64 k
TraceAdditive (m : Arrays) (tol : Tolerance) (k : Dim) (a b : MatOf k k) : Bool :=
  within tol (m.trace (m.madd a b)) (m.trace a + m.trace b)
TraceCyclic (m : Arrays) (tol : Tolerance) (r c : Dim) (a : MatOf r c) (b : MatOf c r) : Bool :=
  withinOf tol (absSumTo r (fn i { absSumTo c (fn j { a.f i j * b.f j i }) })) (m.trace (m.matMul a b)) (m.trace (m.matMul b a))
TraceAgrees (m : Arrays) (tol : Tolerance) (k : Dim) (a : MatOf k k) : Bool :=
  withinOf tol (absSumTo k (fn i { a.f i i })) (m.trace a) (traceDef a)

-- The pseudo-inverse of a symmetric matrix on its retained subspace, at the same floor as the
-- rank (P11; v0.1 array.lut:157 held `n eps` inside): P = V diag(1 / w on the retained, 0) V^T.
-- Characterized where the spectrum is read off: a diagonal clear of the floor, the zero matrix
-- (nothing retained), the identity; and on any symmetric matrix by what holds of the projector
-- S P = V_r V_r^T whatever is discarded: P S P = P, S P symmetric, P symmetric, the trace of S P
-- the retained rank; S P S = S up to the part of S discarded, which is below the floor times the
-- largest eigenvalue in magnitude, itself below the Frobenius norm (the slack); P at a positive
-- scale is P over the scale (the floor is relative). Each within the demand's tolerance, which
-- 11.S18 says depends on the conditioning (so the demand sets it); agreement with a native
-- spectrum is a corollary (4.R10) and is not restated.
-- spec 11.S18, P11
PinvOfDiagonal (m : Arrays) (tol : Tolerance) (fl : ClearFloor) (d : ClearDiagonal) : Bool :=
  approxMat tol (m.pinvSym fl (diagonal d)) (pinvOfDiagonal fl d)
PinvOfZero (m : Arrays) (fl : RankFloor) (k : Dim) : Bool := approxMat exact (m.pinvSym fl (zeroMat k k)) (zeroMat k k)
PinvOfIdentity (m : Arrays) (tol : Tolerance) (fl : RankFloor) (k : Dim) : Bool := approxMat tol (m.pinvSym fl (identity k)) (identity k)
-- [proposed, 2026-10-14, on the evidence report's Findings] Two changes.
-- (1) PinvRestricts is stated over the matrices that are positive semidefinite at the floor,
-- `PsdAt m fl`: the retained rank at the floor of the negative of the matrix is zero, that is,
-- every eigenvalue of s is at least minus the floor times the largest in magnitude. Reading
-- taken: the one the leaf `retainedRank` already gives, so the predicate needs no spectrum of its
-- own and is the predicate of the slack (the part dropped is then at most the floor times the
-- largest eigenvalue in magnitude, below `fl * frobDef s`, 11.S18). Rejected: the dropped part's
-- norm as the slack (needs the spectrum, which the law has no leaf for), and quadratic forms on a
-- listed basis (do not decide semidefiniteness). On an indefinite matrix pinvSym drops the
-- negative eigenvalues by design, and s p s differs from s by the negative part.
-- (2) PinvProjects, PinvSymmetric, PinvScales compare relative to the magnitudes (11.S14): the
-- entries of p s p are sums of products, compared to p within the tolerance times the sum of the
-- magnitudes of those products; the symmetry laws likewise with the scale of the matrix compared;
-- and P at a scale is compared with a scale of the condition of s read from the retained
-- spectrum, `frobDef s * frobDef p` (a bound on the condition number of s on its retained
-- subspace), since the error of p is of order cond times eps (11.S18: the tolerance depends on the
-- conditioning). The tolerance stays a parameter of each law (D-2026-10-14-c).
-- spec 11.S14, 11.S18
PsdAt (m : Arrays) (fl : RankFloor) : U := { s : Symmetric | m.retainedRank fl (mscaleDef (0.0 - 1.0) s) == 0 }
PinvProjects (m : Arrays) (tol : Tolerance) (fl : RankFloor) (s : Symmetric) : Bool :=
  { p := m.pinvSym fl s
    approxMatOf tol (matMulDef (absMat p) (matMulDef (absMat s) (absMat p))) (m.matMul p (m.matMul s p)) p }
PinvSymmetric (m : Arrays) (tol : Tolerance) (fl : RankFloor) (s : Symmetric) : Bool :=
  { p := m.pinvSym fl s
    approxMatOf tol (absMat p) p (m.transpose p)
      and approxMatOf tol (matMulDef (absMat s) (absMat p)) (m.matMul s p) (m.transpose (m.matMul s p)) }
PinvRestricts (m : Arrays) (tol : Tolerance) (fl : RankFloor) (s : PsdAt m fl) : Bool :=
  { p := m.pinvSym fl s
    -- [proposed, 2026-10-15; 11.S14] the rounding of s p s is of the magnitudes (cond times eps, as
    -- its siblings, 7032d7b), not a flat constant: scale |s||p||s|; the slack stays for the dropped part
    approxMatSlackOf (fl * frobDef s) tol (matMulDef (absMat s) (matMulDef (absMat p) (absMat s))) (m.matMul s (m.matMul p s)) s }
PinvTraceIsRank (m : Arrays) (tol : Tolerance) (fl : RankFloor) (s : Symmetric) : Bool :=
  within tol (m.trace (m.matMul s (m.pinvSym fl s))) (toFloat64 (m.retainedRank fl s))
PinvScales (m : Arrays) (tol : Tolerance) (fl : RankFloor) (c : Positive) (s : Symmetric) : Bool :=
  { p := m.pinvSym fl s
    approxMatOf (frobDef s * frobDef p * tol) (mscaleDef (1.0 / c) (absMat p) )
      (m.pinvSym fl (mscaleDef c s)) (mscaleDef (1.0 / c) p) }

Arrays := AddPointwise & SubPointwise & ScalePointwise & TransposePointwise & MaddPointwise & MsubPointwise & MscalePointwise
  & DotSymmetric & DotOnBasis & DotAgrees & NormOfBasis & NormOfDot & NormScales
  & MatVecOnBasis & MatVecAgrees & MatMulIdentity & MatMulTransposes & MatMulAgrees
  & RankOfDiagonal & RankOfZeroAndIdentity & RankBounded & RankScales & RankUnderRotation
  & TraceOfIdentity & TraceAdditive & TraceCyclic & TraceAgrees
  & PinvOfDiagonal & PinvOfZero & PinvOfIdentity & PinvProjects & PinvSymmetric & PinvRestricts & PinvTraceIsRank & PinvScales
````

### `experiment_zero.lut`

````
-- experiment_zero.lut: the positions of the microphones and the speaker placements from the tape
-- distances, as a Laplace update of the prior the graph declares.
--
-- Ported 2026-10-14 by Claude Opus 5.5, an agent of the coordinating session, on the brief
-- record/IA/slice-port-2-2026-10-14/prompt.md, from prototipo-cero/luthier/experiment_zero.lut of
-- sonolocalización at its commit 5ffc36ef70e16e11182bc09e4a927c381e35df1c (v0.1 syntax), with the
-- three tables of src/distance_graph.py:248-284 there (`positions_table`, `residuals_table`,
-- `transform_table`) written here natively, as `Table` values (tables.lth), in place of the
-- externs. The renames and the changes beyond them follow the theories' report
-- (record/IA/slice-theories-2-2026-10-14/report.md, last section); what changed and every reading
-- the spec or the theories left open: this port's report, record/IA/slice-port-2-2026-10-14/report.md.
--
-- From experiment_zero.lut's header, kept: the graph directory (nodes.csv, measurements.csv) is
-- the input. The parameter is the whole position vector, node by node; the belief is Gaussian in
-- information form, with the prior's diagonal precision. The distances enter through the profile
-- likelihood (sigma eliminated), so the fit does not need the tape's error, and sigma is read off
-- the residuals afterwards as sqrt(RSS / nu), with nu = K - tr(F Sigma) the residual degrees of
-- freedom. Outputs: positions.csv (posterior mean and sd per node, shift from the prior),
-- residuals.csv (each measurement with its prediction and standardized residual) and
-- transform.csv (each residual over its own sd, with its leverage, and its probability integral
-- transform under the fitted model). The summary line says how far the transforms are from
-- uniform: it reports, it does not stop the run.
--
-- Two control runs, each an entry with its own parameter, say where a large sigma comes from (25.7
-- cm in session A, with every standardized residual below 0.8):
--   priorWidened  the prior sds of the horizontal coordinates multiplied by horizontalWidening: if
--                 the prior on the microphones (0.2 m) is too tight, the fit moves them and sigma falls
--   sigmaKnown    the tape's error given, fixedSigma, instead of eliminated: the transforms say
--                 whether the distances agree with it
-- With 22 data and 30 parameters a test on the residuals has little power; the controls say more.
--
-- The host has no action that writes a table to a file yet (world_model.lut: `print` and
-- `readFile`), so each table is printed to the standard output after a header line `== <path>`, the
-- path it would be written at under outDir. The three plots of the tables (figures.lut, plan G4 of
-- record/plan/plots/plan-plots-2026-10-14-decisions.md) are rendered after them by the host's
-- renderer (plot_model.lut) to outDir/positions.png, residuals.png and transform.png; outDir must
-- exist. The summary line is printed last.
--
-- Run from the root of this repository with
--   PYTHONPATH=src python3 -m luthier.cli run examples/sonolocalizacion/experiment_zero.lut \
--     --set graphDir=examples/sonolocalizacion/A/graph --set outDir=<dir> \
--     --set lmTol=1e-12 --set lmMaxIter=500 --set lmFloor=6.661338147750939e-15
-- (v0.1's values of session A; the floor is v0.1's `n eps` for the 30 coordinates of session A),
-- and the controls with --main priorWidened --set horizontalWidening=5.0, or --main sigmaKnown
-- --set fixedSigma=0.03, each with its own outDir.

import "world_model.lut" HostConsole host : HostConsole
import "numbers.lth" Doubles Elementary
import "numbers_model.lut" doubles : Doubles elementary : Elementary
import "arrays.lth" Arrays Vec Mat VecOf MatOf RankFloor vec mat zeros
import "arrays_model.lut" numpy : Arrays sub dot matMul transpose trace pinvSym
import "tables.lth" Table Codec Cell int real text
import "tables_model.lut" csv : Codec
import "probability.lth" Kolmogorov MeanModel ScaledModel Likelihood gaussian profiled normalCdf kolmogorovTail valueSums
import "probability_model.lut" numpySort : Kolmogorov kolmogorovDistance
import "belief.lth" GaussianBelief Settings MaxResult Maximizer laplaceMode laplaceAt
import "belief_model.lut" lm : Maximizer
import "positions.lut" Design Separated flatten
import "positions_model.lut" positionsModel nodesOf
import "plot.lth" Canvas
import "plot_model.lut" matplotlib
import "figures.lut" Style positionsPlot residualsPlot transformPlot keptCount
import "distance_graph.lut" DistanceGraph GraphWithColumns ValidDistanceGraph ValidGraph MapInput toMapInput designOf readGraph nameOf iOf jOf dOf intToString realToString

-- ---------------------------------------------------------------- parameters
-- run parameters: declared holes that `run --set name=value` fills (3.S9, 8.S1, 12.S18). The graph
-- directory and the directory of the tables, relative to where the run starts.
graphDir : String
outDir : String
-- the parameters of the two controls, needed only by their entries
horizontalWidening : Float64
fixedSigma : Float64
-- Levenberg-Marquardt: the tolerance on the Newton decrement, in nats, below which it says it
-- converged, its budget of iterations (session A: 1e-12 and 500), and the floor of the step
-- matrix's spectrum below which a direction is neither stepped nor counted (belief.lth `Settings`)
lmTol : Float64
lmMaxIter : Int
lmFloor : Float64

-- ---------------------------------------------------------------- the model on the full position vector
-- theta is the positions of the graph's nodes, node by node (positions.lut), and the mean model is
-- the one of the design the graph measures, the model distances.lut certifies with the gauge fixed
meanModel (m : MapInput) : MeanModel (3 * m.x0.n) := positionsModel (designOf m)

-- the prior as a Gaussian belief: mean x0, diagonal precision 1 / sd^2, flattened node by node
priorBelief (m : MapInput) : GaussianBelief (3 * m.x0.n) := {
  s := flatten m.sdx
  b := { mean := flatten m.x0, precision := mat Float64 s.n s.n (fn a c { if a == c then 1.0 / (s.f a * s.f a) else 0.0 }) }
  b }

-- the graph with the prior sds of the horizontal coordinates (x and y) multiplied by c: the heights
-- were measured and the horizontal positions guessed, and a gauge fixed by a tiny sd stays fixed
widenedPrior (m : MapInput) (c : Float64) : MapInput :=
  { x0 := m.x0, sdx := mat Float64 3 m.x0.n (fn a k { if a < 2 then c * m.sdx.f a k else m.sdx.f a k }), i := m.i, j := m.j, d := m.d }

-- how the fit treats the tape's error: eliminated by the profile likelihood, sigma read off the
-- residuals; or known
SigmaTreatment = { eliminated : Unit || known : { s : Float64 | 0.0 < s } }

-- with sigma known, u = log s is a constant of the model and its gradient zero: probability.lth's
-- `fixedSigma`, written here under another name, since the run parameter of the control has that
-- one (v0.1's `--set fixedSigma=0.03`)
knownSigma (n : Nat) (m : MeanModel n) (u : Float64) : ScaledModel n := { model := m, logSigma := fn s { u }, dLogSigma := fn s { zeros n } }
likelihoodOf (m : MapInput) (st : SigmaTreatment) : Likelihood (3 * m.x0.n) :=
  match st {
    eliminated u -> profiled (3 * m.x0.n) (meanModel m) ;
    known s -> gaussian (3 * m.x0.n) (knownSigma (3 * m.x0.n) (meanModel m) (elementary.log s)) }

-- ---------------------------------------------------------------- the update
-- The maximizer is the host's Levenberg-Marquardt (belief_model.lut, src/luthier/lm.py), a model
-- of `Maximizer` validated against belief.lth §2 at the first action that asks for it (10.S10),
-- with the settings the run takes from its parameters.
runSettings : Settings := { tol := lmTol, maxIter := lmMaxIter, floor := lmFloor }

-- The floor of the pseudo-inverse of a posterior precision, its covariance: v0.1's `n eps`, n the
-- size of the matrix and eps the spacing of the doubles at one (arrays.lth §4, P11).
covFloor (n : Int) : RankFloor := toFloat64 n * doubles.epsilon

-- Every result of the host that is used more than once is bound by a one-arm `match`, which the
-- run evaluates once; a `:=` binding or an argument is passed unevaluated and computed again at
-- each use until run.py has call by need (8.S4; record/IA/fit-host-2026-10-14/report.md).
-- The posterior's mean is the mode itself (laplaceAt, belief.lth §3), so it is read as `mode.x`.
--
-- What the fit gives, on the positions of n coordinates. A zero distance between two measured nodes
-- cannot be excluded ahead for the points the maximizer visits: the Jacobian does not exist there
-- (positions.lut), so the fit says whether the measured pairs are apart where it ended, and the run
-- reports it with convergence.
Fit (n : Int) = { posterior : GaussianBelief n, sigma : Float64, nu : Float64, predicted : Vec Float64, converged : Bool, separated : Bool }

-- the fit of a valid graph, with its horizontal prior sds widened by c (1 for the experiment)
Widening : U := { c : Float64 | 0.0 < c }
fitOf (g : ValidDistanceGraph) (c : Widening) : MapInput := widenedPrior (toMapInput g) c

fit (settings : Settings) (g : ValidDistanceGraph) (c : Widening) (st : SigmaTreatment) : Fit (3 * g.nodes.nRows) := {
  m := fitOf g c
  model := meanModel m
  lik := likelihoodOf m st
  prior := priorBelief m
  d := designOf m
  match laplaceMode (3 * m.x0.n) lm settings lik prior m.d { mode ->
  match (laplaceAt (3 * m.x0.n) lik prior m.d mode.x).precision { precision ->
  match model.mean mode.x { h ->
  match sub m.d h { r ->
  match toFloat64 m.d.n - trace (matMul (lik.info m.d mode.x) (pinvSym (covFloor (3 * m.x0.n)) precision)) { nu ->
    { posterior := { mean := mode.x, precision := precision },
      sigma := (match st { eliminated u -> elementary.sqrt (dot r r / nu) ; known s -> s }), nu := nu,
      predicted := h, converged := mode.converged,
      separated := Separated mode.x (nodesOf d mode.x d.i) (nodesOf d mode.x d.j) } } } } } } }

-- ---------------------------------------------------------------- the transform of the residuals
-- Under the linearized model each residual has variance sigma^2 (1 - h_k), with h_k = (J Sigma J^T)_kk
-- / s^2 its leverage, s^2 the variance the likelihood assumes (RSS / K for the profile one) and Sigma
-- the posterior covariance; the leverages sum to K - nu. A residual over its own sd, z_k, is a
-- standard normal, and Phi(z_k) is uniform (with sigma estimated a t with nu degrees of freedom would
-- be exact; the normal is what is reported). A datum the fit reproduces exactly, h_k = 1, has a
-- residual of zero and no distribution, and is left out of the distance.
Transform = { leverage : Vec Float64, z : Vec Float64, u : Vec Float64, distance : Float64, count : Int }

-- the transforms of the data with a residual of their own, each as a vector of one
keptTransforms (sd u : Vec Float64) (k : Nat) : List (Vec Float64) :=
  if k >= sd.n then nil
  else if k < u.n and sd.f k > 0.0 then cons (vec Float64 1 (fn q { u.f k })) (keptTransforms sd u (k + 1))
  else keptTransforms sd u (k + 1)

-- the leverage of each datum, (J Sigma J^T)_kk / s^2; the sd of each residual; each residual over its
-- sd; and the transform of each
leverages (jac cov : Mat Float64) (assumed : Float64) : Vec Float64 :=
  match matMul jac (matMul cov (transpose jac)) { h -> vec Float64 h.m (fn k { h.f k k / assumed }) }
residualSds (lev : Vec Float64) (sigma : Float64) : Vec Float64 :=
  vec Float64 lev.n (fn k { if lev.f k < 1.0 then sigma * elementary.sqrt (1.0 - lev.f k) else 0.0 })
overSds (r sd : Vec Float64) : Vec Float64 := vec Float64 sd.n (fn k { if sd.f k > 0.0 and k < r.n then r.f k / sd.f k else 0.0 })
normalTransforms (z : Vec Float64) : Vec Float64 := vec Float64 z.n (fn k { normalCdf (z.f k) })

transformOf (g : ValidDistanceGraph) (c : Widening) (st : SigmaTreatment) (f : Fit (3 * g.nodes.nRows)) : Transform := {
  m := fitOf g c
  match sub m.d f.predicted { r ->
  match (match st { eliminated u -> dot r r / toFloat64 r.n ; known s -> s * s }) { assumed ->
  match leverages ((meanModel m).jac f.posterior.mean) (pinvSym (covFloor (3 * m.x0.n)) f.posterior.precision) assumed { lev ->
  match residualSds lev f.sigma { sd ->
  match normalTransforms (overSds r sd) { u ->
  match keptTransforms sd u 0 { kept ->
  match valueSums kept { (s1, s2, count) ->
    { leverage := lev, z := overSds r sd, u := u, distance := kolmogorovDistance kept, count := count } } } } } } } } }

-- the tail probability of the distance, by Kolmogorov's limit with Stephens's correction
transformTail (t : Transform) : Float64 :=
  if t.count < 1 then 1.0
  else { q := elementary.sqrt (toFloat64 t.count)
         kolmogorovTail ((q + 0.12 + 0.11 / q) * t.distance) }

posteriorSd (n : Nat) (b : GaussianBelief n) : Vec Float64 :=
  match pinvSym (covFloor n) b.precision { cov -> vec Float64 b.mean.n (fn k { elementary.sqrt (cov.f k k) }) }

-- ---------------------------------------------------------------- the tables
-- The three tables of a run, as `Table` values (tables.lth): their columns and kinds, and each
-- cell from the node or the measurement of its row (v0.1's externs positions_table,
-- residuals_table and transform_table of src/distance_graph.py:248-284, written here). An entry
-- outside a vector reads 0.0, which a row of the graph never asks for.
entry (v : Vec Float64) (k : Int) : Float64 := if 0 <= k and k < v.n then v.f k else 0.0
names3 (a b c : String) : List String := cons a (cons b (cons c nil))
real3 : List String := names3 "float" "float" "float"

-- one row per node: its name, the posterior mean and sd of each coordinate, and how far the mean
-- moved from the prior's
shiftOf (mean prior : Vec Float64) (r : Int) : Float64 :=
  elementary.sqrt ((entry mean (3 * r) - entry prior (3 * r)) * (entry mean (3 * r) - entry prior (3 * r))
    + (entry mean (3 * r + 1) - entry prior (3 * r + 1)) * (entry mean (3 * r + 1) - entry prior (3 * r + 1))
    + (entry mean (3 * r + 2) - entry prior (3 * r + 2)) * (entry mean (3 * r + 2) - entry prior (3 * r + 2)))
positionCell (g : GraphWithColumns) (mean sd prior : Vec Float64) (c : String) (r : Fin g.nodes.nRows) : Maybe Cell :=
  if c == "name" then just (text (nameOf g r))
  else if c == "x" then just (real (entry mean (3 * r)))
  else if c == "y" then just (real (entry mean (3 * r + 1)))
  else if c == "z" then just (real (entry mean (3 * r + 2)))
  else if c == "sx" then just (real (entry sd (3 * r)))
  else if c == "sy" then just (real (entry sd (3 * r + 1)))
  else if c == "sz" then just (real (entry sd (3 * r + 2)))
  else if c == "shift" then just (real (shiftOf mean prior r))
  else nothing
positionsTable (g : GraphWithColumns) (mean sd prior : Vec Float64) : Table := {
  nRows := g.nodes.nRows,
  names := cons "name" (cons "x" (cons "y" (cons "z" (cons "sx" (cons "sy" (cons "sz" (cons "shift" nil))))))),
  kinds := cons "str" (cons "float" (cons "float" (cons "float" (cons "float" (cons "float" (cons "float" (cons "float" nil))))))),
  cell := fn c r { positionCell g mean sd prior c r },
}

-- one row per measurement: its nodes, the distance, the prediction, the residual and the residual
-- over sigma
residualCell (g : GraphWithColumns) (predicted : Vec Float64) (sigma : Float64) (c : String) (r : Fin g.measurements.nRows) : Maybe Cell :=
  if c == "i" then just (int (iOf g r))
  else if c == "j" then just (int (jOf g r))
  else if c == "d" then just (real (dOf g r))
  else if c == "predicted" then just (real (entry predicted r))
  else if c == "residual" then just (real (dOf g r - entry predicted r))
  else if c == "standardized" then just (real ((dOf g r - entry predicted r) / sigma))
  else nothing
residualsTable (g : ValidDistanceGraph) (predicted : Vec Float64) (sigma : Float64) : Table := {
  nRows := g.measurements.nRows,
  names := cons "i" (cons "j" (cons "d" (names3 "predicted" "residual" "standardized"))),
  kinds := cons "int" (cons "int" (cons "float" real3)),
  cell := fn c r { residualCell g predicted sigma c r },
}

-- one row per measurement: its nodes, its leverage, its residual over its own sd, and the transform
transformCell (g : GraphWithColumns) (lev z u : Vec Float64) (c : String) (r : Fin g.measurements.nRows) : Maybe Cell :=
  if c == "i" then just (int (iOf g r))
  else if c == "j" then just (int (jOf g r))
  else if c == "leverage" then just (real (entry lev r))
  else if c == "z" then just (real (entry z r))
  else if c == "u" then just (real (entry u r))
  else nothing
transformTable (g : ValidDistanceGraph) (lev z u : Vec Float64) : Table := {
  nRows := g.measurements.nRows,
  names := cons "i" (cons "j" (names3 "leverage" "z" "u")),
  kinds := cons "int" (cons "int" real3),
  cell := fn c r { transformCell g lev z u c r },
}

-- ---------------------------------------------------------------- the program
summary (settings : Settings) (n : Int) (f : Fit n) (t : Transform) (g : DistanceGraph) : String :=
  "nodes " + intToString g.nodes.nRows + ", measurements " + intToString g.measurements.nRows
  + ", sigma " + realToString f.sigma + " m, nu " + realToString f.nu
  + ", transform of the residuals: Kolmogorov distance " + realToString t.distance + " over " + intToString t.count
  + ", tail probability " + realToString (transformTail t)
  + (if f.converged then "" else ", NOT CONVERGED: the maximizer ran out of its " + intToString settings.maxIter + " iterations")
  + (if f.separated then "" else ", NOT SEPARATED: two measured nodes coincide where the fit ended")

-- What a run writes and says, from a valid graph: the tables of the positions, the residuals and
-- their transforms, and the summary. A function of the graph, so its laws are tested on graphs drawn
-- valid; the run reads the graph and writes what this gives.
Report = { positions : Table, residuals : Table, transform : Table, summary : String }

reportOf (settings : Settings) (g : ValidDistanceGraph) (c : Widening) (st : SigmaTreatment) : Report :=
  match fit settings g c st { f ->
  match transformOf g c st f { t ->
  match posteriorSd (3 * g.nodes.nRows) f.posterior { sd ->
    { positions := positionsTable g f.posterior.mean sd (flatten (toMapInput g).x0),
      residuals := residualsTable g f.predicted f.sigma,
      transform := transformTable g t.leverage t.z t.u,
      summary := summary settings (3 * g.nodes.nRows) f t g } } } }

-- A table as text (tables_model.lut's codec), at a path. The host has no write action yet
-- (world_model.lut), so the text goes to the standard output after a header line naming the path.
writeTable (w : W) (path : String) (t : Table) : W * Unit := {
  (w1, done) <- host.print w ("== " + path)
  host.print w1 (csv.render t) }

-- The figures (plan G4, figures.lut) and what they take from the demand (P11), each a definition
-- [proposed by the agent of record/IA/plots-2026-10-15/prompt-figures.md]: the canvas, in inches
-- and dots per inch; the marks' sizes in points and the automatic scales' expansion; the
-- ellipses' semi-axes in posterior sds; the node whose measurements the residual plot colours
-- (the speaker placement A2, whose block of distances is in question in session A) and the two
-- colours, for "other" and "touches" in that order; the level of the Kolmogorov band.
figureCanvas : Canvas := { width := 6.0, height := 5.0, dpi := 100.0 }
figureStyle : Style := { pointSize := 5.0, textSize := 7.0, lineWidth := 1.0, expand := 0.08 }
ellipseLevel : Float64 := 2.0
highlightedNode : String := "parlante_A2"
pairColours : List String := ["#0072B2", "#D55E00"]
bandLevel : Float64 := 0.05

-- [proposed] The half-width of the Kolmogorov band at level alpha over n transforms: c / (sqrt n +
-- 0.12 + 0.11 / sqrt n), with Stephens's correction as in `transformTail`, and c = sqrt(-log(alpha /
-- 2) / 2), where the first term of Kolmogorov's tail, 2 exp(-2 c^2), equals alpha (c = 1.358 at
-- 0.05; the omitted terms change it in the fourth digit).
bandHalfWidth (alpha : Float64) (n : Int) : Float64 :=
  if n < 1 then 1.0
  else { q := elementary.sqrt (toFloat64 n)
         elementary.sqrt (0.0 - elementary.log (alpha / 2.0) / 2.0) / (q + 0.12 + 0.11 / q) }

writeReport (w : W) (r : Report) : W * Unit := {
  (w1, u1) <- writeTable w (outDir + "/positions.csv") r.positions
  (w2, u2) <- writeTable w1 (outDir + "/residuals.csv") r.residuals
  (w3, u3) <- writeTable w2 (outDir + "/transform.csv") r.transform
  (w4, u4) <- matplotlib.render w3 (positionsPlot figureCanvas figureStyle ellipseLevel r.positions) (outDir + "/positions.png")
  (w5, u5) <- matplotlib.render w4 (residualsPlot figureCanvas figureStyle highlightedNode pairColours r.positions r.residuals)
                (outDir + "/residuals.png")
  (w6, u6) <- matplotlib.render w5 (transformPlot figureCanvas figureStyle (bandHalfWidth bandLevel (keptCount r.transform)) r.transform)
                (outDir + "/transform.png")
  host.print w6 r.summary }

-- The graph is checked against its invariants before the fit; an invalid one is reported, not fit.
-- The run of the experiment and its two controls differ in the prior and in how sigma is treated.
runOn (w : W) (read : Maybe DistanceGraph) (c : Widening) (st : SigmaTreatment) : W * Unit :=
  match read {
    nothing -> host.print w ("FAIL ReadGraph: " + graphDir + " has no nodes.csv and measurements.csv that read as typed tables") ;
    just g -> if ValidGraph g then (match reportOf runSettings g c st { r -> writeReport w r }) else host.print w ("the graph in " + graphDir + " is not valid") }

runWith (w : W) (c : Widening) (st : SigmaTreatment) : W * Unit := {
  (w1, read) <- readGraph w graphDir
  runOn w1 read c st }

-- The entries: the experiment, and its two controls (`run --main priorWidened`, `run --main
-- sigmaKnown`). A run parameter is a plain `Float64` (`--set` fills only the plain types), so the
-- control's entry asks it positive, which v0.1 asked in the parameter's type.
main (w : W) : W * Unit := runWith w 1.0 (eliminated unit)
priorWidened (w : W) : W * Unit :=
  if 0.0 < horizontalWidening then runWith w horizontalWidening (eliminated unit)
  else host.print w ("horizontalWidening must be positive: " + realToString horizontalWidening)
sigmaKnown (w : W) : W * Unit :=
  if 0.0 < fixedSigma then runWith w 1.0 (known fixedSigma)
  else host.print w ("fixedSigma must be positive: " + realToString fixedSigma)
````

### `docs/spec/11-numbers.md`, section 2 (context)

````
## §2 The primitive types

**11.R1. The number types and the end of `R`.** [implemented] `Int` is ℤ without bound, `Real` is the ideal, `Float64` is the finite doubles and refines `Real` (every finite double is a real number), `String` is text. `Nat` is `{ k : Int | 0 <= k }` and `Fin n` is `{ k : Int | 0 <= k and k < n }`. A value of `Float64` passes where a `Real` is expected. `R` names no type. Each primitive states in its body what it is: `Int : U := primitive "integer"`, `Real : U := primitive "real"`, `Float64 : Real := primitive "ieee754-binary64"`, `String : U := primitive "unicode"`.
Files: n1_numbers.accept.lut, n2_r_gone.reject.lut.

**11.R2. Only the core says what the interpreter provides.** [implemented] The body `primitive` is allowed only in `core.lut`.
Files: n1_numbers.accept.lut, n3_primitive_outside_core.reject.lut.

**11.S4. What a primitive is.** [implemented] `Int` is realized exactly by the host's unbounded integers. `Real` has no implementation of its own: the interpreter computes none of its operations, and its structure is an axiom (11.R3). The operations of `Float64` are the machine's rounded ones, not those of `Real`: the refinement is of the values, not of the operations. `Rational : Real` is a primitive of `core.lut`, represented by the host's fractions, with `+ − × /` and the comparisons exact and no `mod`; its values come from `fromInt`, `ratio` and `toQ` of `lib/rational.lut`.

**11.S5. The conversion from an integer.** [implemented] `toFloat64 : Int -> Float64` is the nearest double to an integer, exact below 2^53; the name stays with the integers (D-2026-10-05-c). A value of `Real` that is not known to be a double enters a leaf only through an explicit rounding to the nearest double, exact on doubles. [decided D-2026-10-12-ah] That rounding waits for a `Real` that computes (11.S10): until then no value of `Real` is not a double and no law over `Real` is tested.

````

### `docs/spec/06-certification.md`, item 6.S16 (context)

````
**6.S16. `lib/certification.lut`.** [decided D-2026-10-13-g] The theory of this chapter, written over a parameter `C`: the theory `CostAlgebra C` with the operations and laws of 6.S5; the record `Certificate C` of 6.S6; the function `grade` of 6.S7; `transport` of 6.S11 and `compose` of 6.S12; `serves` of 6.S15; and their laws, among them monotonicity (6.S13) and that `serves` is monotone in the cutoff. The file is not written. The host's `certify.py` and `testing.py` are its specimen, certified against it (L14.3), and each library of costs gives a model of `CostAlgebra`. Once its laws are written, L9 and L10 are read back from them (D-2026-10-12-ag).
````
