# Review of layer 3 of Luthier, the demand and the plan (round 1, bundle B)

You are reviewing theory files written in Luthier, a language whose interpreter is being rebuilt from its own theories: a type is a theory (a structure with laws), a value of it is a model, and the language certifies models against their theories by testing. A theory file (`.lth`) declares a record type of operations, states its laws as Bool-valued definitions over a model (`(m : T)`), and defines the theory as their conjunction (`T := Law1 & Law2`); a model file (`.lut`) holds values of theories. Every constructor of a `data` must have a law stating its role (principle L2.7: a definition is a concept; distinct constructors and accessors state no role). A law quantifies over the subtype it means rather than over an implication whose premise random cases rarely meet. The files parse with the project's parser; nothing yet type-checks or certifies them, so you are the first check of their meaning. Grammar, kernel and earlier layers were reviewed in earlier rounds and are not in scope. Do not reopen a decision listed under "Decisions the files cite" unless a file contradicts it; where you disagree with the specification itself, say so as a separate item.

This prompt covers the demand and the plan (layer 3, bundle B of its external review; the world and certification files, bundle A, are reviewed apart and not included, so a name imported from `certification.lth` or `test.lth` is taken as stated). `demand.lth` states the demand as a value: what an action asks of a program, the cutoffs it carries, what it passes down to each law of the cone, and what a run records of it. `plan.lth` states the plan as a value: the dataflow of a cone, a schedule that linearizes it, the live subgraph a demand reaches, the strategy as a parameter, the law `Confluent`, and the key under which a result is kept. `demand_model.lut` and `plan_model.lut` are models of them. The chapter they realize is `docs/spec/08-demand.md`. The material below, in this order: terms and principles L2.7, L9.6, L10, L11 and P11; the decisions the files cite; then the five files. Frozen at commit 2710cfc.

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
9. **Identifying a result**: what law is missing for `run`'s record and key to identify a result (spec 8.S8 and 12.S18: the record a run writes and the key under which a result is kept; the key, its hash and the record of `demand.lth` and `plan.lth`).

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

D-2026-10-10-c  A definition has no effects. Its result depends only on its inputs; effects live
                only in the actions (print, save). A mutable parameter written as two variables,
                before and after, is not an effect: the dependence is an edge of the graph. What is
                forbidden is what the graph does not show.
Author:     Luciano
Quote:      "lo que si es no-side effects"
Source:     chat (session of 2026-10-10, on the audios of 2026-10-10)
Kind:       principle of the language, candidate for docs/principles.md. For L9 (a program is a
            DAG), L12 (execution is the verification of equivalences); it is the one assumption
            under which every evaluation strategy gives the same result
Status:     current

D-2026-10-10-d  Forward on demand: the evaluation strategy is a parameter separate from the
                program (P11). By default: a plan backward from the actions over names, evaluating
                nothing (a branch whose use depends on a value marks both branches live); then a
                strict forward run over the live subgraph, in topological order, each node once and
                whole. Three conditions it rests on: (i) errors and holes are values that flow,
                so a live-but-unused branch cannot abort the run; (ii) results are memoized in a
                store keyed by the hash of (code, inputs, mode), the retention policy a parameter;
                (iii) the tests are actions, so "verify everything" is asking for all tests and
                "verify on demand" is asking for the tests of what an action uses (L3). Named by
                Luciano "forward por demanda"; mechanism "retro-forward"; not Haskell's laziness,
                which is per expression and interleaved with the run.
Author:     Luciano for the scheme and the name; the model for the three conditions, accepted
Quote:      "1) cargas el arbol de definiciones 2) detectas los 'print' 3) corres para atras desde
            el print hasta la base, pero no ramifico (no genero 3 f, solo detecto nombres)
            4) calculo los caminos detectados forward."
            "Lo ideal es no elegir, es decir, poder expresar todo, solo elegir lo que va por
            default."
            "si, dale."
Source:     chat (session of 2026-10-10); record/audios/WhatsApp Ptt 2026-10-10 at 11.42.15.md
            (60a10aa, 01:51 to 04:07, backward and forward "las dos tienen un rol"); 11.11.22.md
            (60a10aa, 00:00, "la Lazy Evaluation sería la mejor manera de definir qué es lo que
            quiero exactamente definir")
Kind:       implementation decision. For P11 (every criterion is a parameter), L7 (the core is
            executable by hand: the plan is readable node by node), L9, L13 (forgetting: the last
            consumer of a node is known from the plan). Prior art: topological schedulers of build
            systems (Make, Bazel; Mokhov, Mitchell, Peyton Jones 2018), magic sets, Halide's
            algorithm/schedule split
Status:     current; the strategy parameter has its place from the start and only the default is
            implemented (P8)

D-2026-10-10-e  Mutable parameters are two variables, before and after, in the core (x1 = f(x0));
                in-place mutation is an optimization the planner applies when x0 has no other
                consumer after f, the same last-consumer analysis that frees nodes. The form f(x)
                that mutates is library, translated to the two names. A uniqueness or linearity
                annotation on the type (a guarantee of no copy) is foreseen, not implemented.
Author:     Luciano for the model of two variables; the model for the planner's criterion and
            the annotation, accepted
Quote:      "Los parametros mutables son una optimizacion importante y se pueden modelar como dos
            variables (antes y despues), que es como se modela un incremento con una funcion
            pura."
Source:     chat (session of 2026-10-10)
Kind:       implementation decision. For D-2026-10-10-c, L7 (both names explicit in the core),
            L2 (uniqueness as a proposition on the type). Prior art: SSA, Fortran intent(inout),
            LAPACK's overwrite of A, Clean's uniqueness types, Perceus (Reinking, Xie, de Moura,
            Leijen 2021)
Status:     current

D-2026-10-11-i  Blocks. A brace term whose last item is a bare expression is a block, its value
                that expression; without a final expression it is a record value. Items: `x := t`
                once, `x <- t` bind or rebind, an action with its result bound. Each item becomes a
                definition with a fresh name (SSA, 04 §5, 05 R12), after which dependencies give
                the only order. A name is visible from its binding to the end of its block and in
                nested blocks; `:=` of a name defined in an enclosing scope is an error, not a
                shadowing; `<-` rebinds only block-local `<-` names and the parameters of the
                enclosing definition. Actions take and return the world, `w1 <- print w0 "x"`, so
                their order is the dependency through `w`. Three kinds of block: the body of a
                definition or lambda, `main` in a file, the session; a file is never a block. A
                rebinding whose previous binding has no consumer is an error in a file and
                allowed in a session.
Author:     Luciano for the demand (blocks, boundaries, scopes; the dead-rebinding question) and
            the acceptance; Claude for the rules
Quote:      "Lo cual nos introduce al concepto de bloques. Y ahi te pido ayuda."; "tenemos que
            definir las boundaries para los blocks y los name scopes."; "Si" (c167022, read as
            accepting the two pending decisions)
Source:     record/answers-annotations-principles-2026-10-11-c.md (blocks), -d.md
Kind:       language design, grammar and static semantics (02 §3, §8; 04 §5; 05 R12). For L9 (the
            DAG is the only order), L12 draft 3 (actions verified before and after), L13, G1, G4;
            resolves the open collision of block and record syntax (02 §8)
Status:     current; spec amended (02 §9, 04 §5, 05 R12) and implemented 2026-10-11, the session included
            (`luthier session`); actions and the world wait for action primitives

D-2026-10-12-ad Import is lazy too, and `test` of a module is the total demand. A module is a
                value, a record of its definitions; `la := import "linear_algebra.lut"` binds it,
                and the file is read only when a demand needs a name of `la` (the checker meeting
                `la.f`, or `run` needing its value), so `import` is not an action either. Laziness
                leaves latent dead code, so `test "linear_algebra.lut"` is the action that
                initializes everything: it demands every name of the module, reads every import,
                checks every definition and certifies every law. Corrects D-2026-10-12-ac, which
                read `import` at once; that reason holds only for a flat import, whose names cannot
                be traced to their file.
Author:     Luciano; the correction of -ac and the flat-import caveat the model's
Quote:      "en realidad yo solo importo linear_algebra.lut cuando necesito una funcion de la..."
            "con lo que import tampoco seria una accion."
            "Esto dejaria muchos muertos latentes, con lo que deberia haber un comando que
            inicialize todo para chequear que las cosas estan definidas."
            "si yo hago test "linear_algebra.lut" por ejemplo seria una accion y ahi inicializo
            todo."
Source:     chat:4f7f0dc5:1646
            chat:4f7f0dc5:1646
            chat:4f7f0dc5:1646
            chat:4f7f0dc5:1657
Kind:       language (L11.7, L5; spec 12.S21, 12.S22; 7.S20). For L5 (only what the demand needs is
            produced), L14
Status:     current; -ac partly reversed (import); open, his: whether a flat import survives (as an
            explicit `open`, read at once) or not, and whether a module carries its own name

D-2026-10-12-al `Cost` is a library. Its algebra, the default conjunction, the conversion of a
                sample's statistics to a cost and the names lift, exact and within are decided when
                the library is implemented, its invariants found then. What the specification fixes
                is what the core asks of it, and that is precised when the certification of types
                is written in Luthier. The same holds for the questions of wave 3 (the form of the
                demand, the world's token, the ranking, the trace): libraries, their invariants found
                by implementing them. The rule: advance as far as possible by handing such work to
                the libraries that do it.
Author:     Luciano; the list of what moves the model's
Quote:      "Cost es una libreria."
            "por lo cual todas las decisiones se toman cuando esa libreria se implemente."
            "Ahora, cuando se defina el codigo Luthier para certificar los tipos hay podriemos
            precisar que se le va a pedir a esa libreria."
            "lo mismo, como va a ser una libreria, recien al implementarla vamos a descubrir sus
            invariantes."
            "O sea el tema es avanazar todo lo que se pueda tirando la pelota a las librerias que
            hagan estos trabajos."
Source:     chat:f15ae1b6:937
Kind:       language and method (O1; spec 5, 6, 8, 9, 10; the wave 2 plan). For L14, P16
Status:     current. Wave 2 changes shape: chapter 6 states certification in Luthier over a `Cost`
            it takes as a parameter, and the interface it asks of the library is what chapter 5
            fixes; the two candidate algebras of D-2026-10-12-p can be two models of that
            interface. The rule may be a principle of the method; his mark pending

D-2026-10-12-h  The cutoff is a parameter of the demand: the minimal cutoff for an implementation
                to be considered. It is not a parameter of the certified-subtype constructor.
Author:     Luciano
Quote:      "I know a place for the cutoff, a minimal cutoff to consider an implementation, it is a
            parameter at the demand level."
Source:     record/recommendations-ia-principles-2026-10-12.md (e8d7db1), §4.3
Kind:       principles (L3, L6, L13). For P11 (every criterion is a parameter), G3 (the demand)
Status:     current; to apply in draft 11

D-2026-10-12-m  Actions on Luthier's own state (writing a certificate, a test) are idempotent and
                memoizable; actions on the world never are.
Author:     Luciano, on Claude
Quote:      "good"
Source:     same, §4.8
Kind:       principles (L9, L10, L11, Terms). For P6 (every change can be undone)
Status:     current; to apply in draft 11

D-2026-10-12-r  The conversion from the statistics of a sampled certificate to a cost is a
                dedicated function with a declared shape (input: the sample's statistics and the
                demand's level; output: a cost), filled differently on different theories;
                −log(1 − ε̂(n, δ)) in nats is the first instance. The grade becomes derived from
                domain and evidence cost; `assumed` carries the evidence cost the demand assigns,
                with no default.
Author:     Luciano for the function with a declared shape per theory; Claude for the first
            instance and for `assumed` as the demand's parameter (proposed in D2, not objected)
Quote:      "The same, the conversion is expressed by a dedicated function and we might choose
            different functions on different theories. Luthier would ask for some input output
            shape, that the particular function is filled on each case."
Source:     record/plan-principles-draft-11-2026-10-12-decisions.md D2 (57a0023)
Kind:       principles (L7, the certificate entry, Terms). For P11, P10 (the invariant of the
            type: the conversion is the theory's), D-2026-10-12-j
Status:     current; to apply in step 4

D-2026-10-13-f  The demand is open: a gate through which parameters change what the program does,
                not a closed list. The type demanded is one of them: asking for `t : P T` asks the
                cone of `t` to build a `P T`, so the cone that built a `T` must be able to build a
                `P T`; one way is code generic over `G T`, with `G` the identity by default, and the
                demand replacing `G` by `P` (a derivative by dual numbers, an error by intervals,
                the decorated output of O5).
Author:     Luciano; the reading through parametricity and the interface asked of `P` the model's
Quote:      "Justamente la demand es una compuerta por la cual pasar parametros que modifiquen el
            comportamiento del programa, porque cerrar los parametros sin razon?"
            "Ahora esto implica que todo el cono que trabajaba para hace T ahora tiene que hacer P T y
            eso deberia ser posible."
            "Una forma es que sea un codigo generico sobre (G T) (donde G puede ser Identity ) y
            entonces reemplazo G por P."
            "Si reescribi"
Source:     luthier@24a0615:record/spec-wave-2-3-for-his-marks.md:52
            luthier@24a0615:record/spec-wave-2-3-for-his-marks.md:54
            luthier@24a0615:record/spec-wave-2-3-for-his-marks.md:55
            chat:f15ae1b6:1734
Kind:       language (spec 8.S1, 8.S2, 8.S8; L5, O5; spec 11.S3 as the first instance). For L5, L14
Status:     current; the interface asked of `P` proposed

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

D-2026-10-13-m  Cost is two things. A distance models how far an approximate value is from the
                ideal; it composes by the triangle inequality, or by the worst link where it is
                ultrametric, and it is the logic of G2, one logic. A probability models sampling; it
                is the evidence, and how evidences combine is an assumption about the dependence of
                what failed (nested: max; independent and rare: sum and log-sum-exp; the joint
                known: the chain rule, exact). A law's value is a distance, and the demand's cutoff
                says whether it is enough; a statistical test is a law of distance (a distance
                between distributions) with probabilistic evidence. Better or worse approximations
                describe a process, the identity of specimens with its distance (L9.9), and are not
                the fit to a law. A certificate's bound is a `Distance` and its evidence an
                `Evidence`, two types with two interfaces; they are refined when used.
Author:     Luciano for the two kinds and their reading; the model for the composition of each and
            for the two types
Quote:      "1) distancia,  modela valores aproximados"
            "2) probabilidad, modela muestreos"
            "el caso de los test de probabilidad, yo creo que es mas de distancias que de
            probabilidad"
            "el primer caso NO es el ajuste a una ley, es una descripcion de un proceso"
            "Si, esta bien. Cuando las usemos las afinamos."
Source:     chat:f15ae1b6:2328
            chat:f15ae1b6:2328
            chat:f15ae1b6:2328
            chat:f15ae1b6:2328
            chat:f15ae1b6:2336
Kind:       principles (G2 read as the logic of distances; L10.1, L12) and spec (6.S5, 6.S6). For
            G2, L10, D-2026-10-12-p
Status:     current; the two interfaces to be refined when certification.lth and cost.lth are
            written. His `not c = 1/c` for min and max (chat:f15ae1b6:2292) waits for a case
            on distances, where negation is in doubt

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


### `demand.lth`

````
-- demand.lth: the demand as a value: what an action asks of a program, with every cutoff it
-- carries; what it passes down to each law of the cone; what a run records of it.
--
-- Draft 0, 2026-10-15, by Claude Fable 5.1, an agent of the coordinating session, on the brief
-- record/IA/demand-2026-10-15/prompt.md (step 6.1 of
-- record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md). Sources: spec 8.S1, 8.S2,
-- 8.S3, 8.S8 (docs/spec/08-demand.md); 6.S10, 6.S14, 6.S15; 12.S13, 12.S17, 12.S18; L5.17, L5.18,
-- L5.19, L12.3, P11; D-2026-10-13-f (the demand is open), D-2026-10-13-m (the cost types come
-- later), D-2026-10-14-c (first everything Boolean, the cutoffs as parameters the demand
-- supplies); certification.lth §3 (the demand on one law, `serves`, `Certified`), test.lth §3
-- (`Grade`), generators.lth §6 (`Budgets`, the same rule: every budget an argument). Pattern of
-- certification.lth.
--
-- What this file states. 8.S1 says a demand is open: whatever the program declares as a
-- parameter, the demand may set; its form is a library's (D-2026-10-12-al), so what is here is
-- one library's record, with the operations of 8.S2 that the core asks for. D-2026-10-14-c says
-- first everything Boolean, so the cutoff is the weakest grade accepted, and where a cost would
-- enter (the bound, the evidence cost, the price of an assumption, 6.S15, 6.S10) there is a hole
-- `C`, with the comment "D-2026-10-13-m, after the slice's failures". certification.lth §3 keeps
-- its `Demand`, the demand on one law; here it is `LawDemand`, the same record by structure, and
-- the law of 8.S1 is that it is passed down from the run's demand and not recomputed (L12.3).
-- A model of `Demanding` builds the demand of a run from the arguments `run` takes
-- (demand_model.lut, `theDemand`), with its defaults declared there and recorded (L5.19). What
-- the brief or the spec leaves open is marked [proposed] at the item above it.
--
-- Index (all sections written in this draft):
--   §1 The demand: its fields, the holes for the costs and the decorated type (8.S1, 8.S2,
--      6.S15, 6.S10, 12.S18, 12.S13).                                                       done
--   §2 Passing down: the demand on one law, the demand an inner action receives (L12.3,
--      6.S15, 6.S10).                                                                       done
--   §3 What a run records of its demand, and what two runs of one demand owe each other
--      (12.S18, L5.18, 8.S3).                                                               done
--   §4 The theory `Demanding`, the laws of §2 and §3 claimed.                               done

import "certification.lth" Certifying Entry Value Hash ServesIsMonotoneInTheCutoff
import "test.lth" Grade Sampled AssumedGrade gradeRank
import "term.lth" Term

-- ---------------------------------------------------------------- §1 The demand

-- The cost type of 6.S4, and what a demand carries in it (6.S15: the cutoff is a bound and an
-- evidence cost in `C`; 6.S10: the evidence cost it assigns to assumptions, with no default):
-- holes. D-2026-10-13-m, after the slice's failures. In this draft the cutoff is the weakest
-- grade accepted (`accepts`, D-2026-10-14-c) and the price of an assumption is whether that grade
-- admits `AssumedGrade` (§2).
C : U
bound : Demand -> C
evidence : Demand -> C
assumed : Demand -> Maybe C

-- The decorated type (8.S1): asking for `t : P T` where the program computes a `T` asks the cone
-- of `t` to build a `P T`, the cone written generic over a type operator `G`, the identity by
-- default, which the demand replaces by `P`. [proposed, 8.S1] Whether the generic form is written
-- by hand or derived from the cone is open, and so is the interface asked of `P` beyond the
-- functor and applicative laws of 8.S2's table; both are holes. A demand that names no
-- decoration asks for the cone's own type, the identity.
Decoration : U
decorate : Decoration -> Term -> Term

-- A demand (8.S1): the entry; the type demanded, the identity when `nothing`; the cutoff, the
-- weakest grade accepted (6.S15, D-2026-10-14-c; `run --accept`); the confidence for sampled
-- evidence (D-2026-10-12-r); the limit on resources (`run --fuel`, the reduction steps); the
-- values of the program's holes (`run --set`, 12.S18); whether every value an extern gives is
-- tested against its refinements as it crosses (`run --checked`, 12.S18, P11); and the lock, the
-- interpreter's revision the program's directory pins (12.S13), `nothing` when none does.
-- [proposed] The entry is a name; 8.S1's term as entry waits for an action that asks for one.
-- [proposed] `delta` is `nothing` in this draft, since no statistic becomes a cost before
-- D-2026-10-13-m; when one does it is required as `assumed` is, with no default. Every field is a
-- parameter the first demand takes as a declared default argument and records (L5.18, L5.19);
-- none is a constant of the core.
Demand = { entry : String, decoration : Maybe Decoration, accepts : Grade, delta : Maybe Float64,
           fuel : Nat, sets : List (String * Value), checked : Bool, pinned : Maybe String }

-- the value a demand gives a hole of the program, if it gives one (12.S18: a hole left without a
-- value is an error that asks for `--set`)
given (d : Demand) (name : String) : Maybe Value := lookupValue name d.sets
lookupValue (name : String) (vs : List (String * Value)) : Maybe Value :=
  match vs { nil -> nothing ; cons (n, v) rest -> if n == name then just v else lookupValue name rest }

-- ---------------------------------------------------------------- §2 Passing down

-- The demand on one law (certification.lth §3, its `Demand`, 6.S15, 7.S15): the law, the current
-- hash of its cone, what the run gives its parameters, and the weakest grade accepted. The same
-- record by structure, so a `LawDemand` is what `Certifying.serves` and `refuse` take.
LawDemand = { law : String, cone : Hash, given : List (String * Value), accepts : Grade }

-- Whether a demand admits assumptions (6.S10) in the Boolean draft: its cutoff admits
-- `AssumedGrade`, the lowest grade (test.lth §3). The price of an assumption in `C` is the hole
-- `assumed` above; `nothing` there is what refuses every assumed value when the cost types come.
-- [proposed] Until then `run --accept assumed` is where a demand names that price.
admitsAssumptions (d : Demand) : Bool := gradeRank d.accepts <= gradeRank AssumedGrade

-- The demand an inner action receives (L12.3, L5.17): the caller's demand with the inner entry,
-- every cutoff kept, since a cutoff does not compose and so is passed down, never recomputed
-- from the inner cone.
inner (d : Demand) (entry : String) : Demand :=
  { entry := entry, decoration := d.decoration, accepts := d.accepts, delta := d.delta, fuel := d.fuel,
    sets := d.sets, checked := d.checked, pinned := d.pinned }

-- ---------------------------------------------------------------- §3 What a run records

-- What a run records of its demand (12.S18, `x.run.json`; L5.18: every threshold or level a
-- certificate needs comes from the demand and is recorded with it): the entry, the hash of the
-- cone it ran, every parameter it set, the grade it accepted, the confidence, the fuel given,
-- whether it ran checked, and the lock. The time, the output, the fuel spent and the states of
-- the cone are the run's, not the demand's, and are not here.
Record = { entry : String, cone : Hash, parameters : List (String * Value), accept : Grade,
           delta : Maybe Float64, fuel : Nat, checked : Bool, lock : Maybe String }

-- A run as its record keeps it: what was demanded, on which cone, and the result printed. The
-- same demand on the same cone gives the same result (8.S3: results are memoized under the hash
-- of code, inputs and mode; 8.S5: a definition has no effects): two runs with one record have one
-- result. That is the predicate of the type, so every store of runs owes it, one read back from
-- `x.run.json` included. [proposed] In the Boolean draft the record is the identity of a result;
-- the key of 8.S8, with the mode, the seed, the plan and the certificates, is plan.lth's.
Run = { record : Record, result : String }
agreesWithRun (r : Run) (rs : List Run) : Bool :=
  match rs { nil -> true ; cons q rest -> (not (r.record == q.record) or r.result == q.result) and agreesWithRun r rest }
determined (rs : List Run) : Bool :=
  match rs { nil -> true ; cons r rest -> agreesWithRun r rest and determined rest }
Runs : U := { rs : List Run | determined rs }

-- ---------------------------------------------------------------- §4 The theory

-- A model of the demand gives, for a run's demand, the demand on each law of its cone and what
-- the run records.
Demanding : {
  lawDemand : Demand -> String -> Hash -> LawDemand,
  recorded : Demand -> Hash -> Record,
}

-- §2. L12.3, 6.S15: the demand on a law carries the run's cutoff and the run's values, and the
-- law's own name and cone; nothing of it is recomputed from the law's cone. [proposed] The run
-- also gives the law the name it certifies, printed, to the law's model parameter
-- (certification.lth §3, run.py's `certification`); that is the run's binding and not the
-- demand's, so `given` here is what `--set` gave.
PassedDownNotRecomputed (m : Demanding) (d : Demand) (law : String) (cone : Hash) : Bool :=
  m.lawDemand d law cone == { law := law, cone := cone, given := d.sets, accepts := d.accepts }
-- 6.S10: a demand that names no price for assumptions refuses every assumed value: no entry with
-- the grade `AssumedGrade` serves a law under it
NoPriceRefusesAssumed (m : Demanding) (k : Certifying) (d : Demand) (law : String) (cone : Hash) (e : Entry) : Bool :=
  admitsAssumptions d or not (e.grade == just AssumedGrade) or not (k.serves (m.lawDemand d law cone) e)
-- 6.S16, L10.5: lowering the cutoff loses nothing accepted; certification.lth's law, applied to
-- the demand passed down, not restated
LoweringLosesNothing (m : Demanding) (k : Certifying) (d : Demand) (law : String) (cone : Hash) (e : Entry) (g : Grade) : Bool :=
  ServesIsMonotoneInTheCutoff k (m.lawDemand d law cone) e g

-- §3. 12.S18, L5.18: the record carries every cutoff and parameter the demand carries, and the
-- cone it ran; so an inner demand (`inner`) records what its caller's would, at the inner entry
RecordsEveryCutoff (m : Demanding) (d : Demand) (h : Hash) : Bool :=
  m.recorded d h == { entry := d.entry, cone := h, parameters := d.sets, accept := d.accepts, delta := d.delta,
                      fuel := d.fuel, checked := d.checked, lock := d.pinned }
Demanding := PassedDownNotRecomputed & NoPriceRefusesAssumed & LoweringLosesNothing & RecordsEveryCutoff
````

### `demand_model.lut`

````
-- demand_model.lut: the demand of a run, built from the arguments `run` takes, with its defaults
-- declared and recorded; the reference model of `Demanding`.
--
-- Draft 0, 2026-10-15, by Claude Fable 5.1, an agent of the coordinating session, on the brief
-- record/IA/demand-2026-10-15/prompt.md. A model file (12.S23): `theDemand` is the first demand
-- of all (L5.19), an action nobody called, so every argument has a declared default, and the
-- demand records them all (L5.18, 12.S18); `demanding` passes it down to each law and writes its
-- record. The host's run.py, which builds the same demand from the command line, is a specimen
-- of this file (L14.3).

import "demand.lth" Demanding Demand LawDemand Record
import "certification.lth" Value Hash
import "test.lth" Grade Sampled

-- The arguments of `run` (12.S17, 12.S18, 12.S13), each with the default the host holds today,
-- named here as a default and not as a constant (L5.18, P11). [proposed] `Sampled` as the grade
-- accepted when none is named (run.py's `ACCEPT`: an assumed entry serves only a run that accepts
-- assumed, 6.S10); 10,000,000 steps of fuel (cli.py: 10,000 was a hundred times too small for
-- validate_graph.lut); `main` as the entry; no hole set; not checked; nothing pinned; no
-- decoration (the identity, 8.S1); no confidence (demand.lth §1).
theDemand (entry : String <- "main") (accepts : Grade <- Sampled) (fuel : Nat <- 10000000)
          (sets : List (String * Value) <- nil) (checked : Bool <- false) (pinned : Maybe String <- nothing) : Demand :=
  { entry := entry, decoration := nothing, accepts := accepts, delta := nothing, fuel := fuel, sets := sets,
    checked := checked, pinned := pinned }

-- L12.3, 6.S15: the demand on one law, passed down: the run's cutoff and values, the law's name
-- and cone
lawDemand (d : Demand) (law : String) (cone : Hash) : LawDemand :=
  { law := law, cone := cone, given := d.sets, accepts := d.accepts }

-- 12.S18, L5.18: what the run records of its demand
recorded (d : Demand) (h : Hash) : Record :=
  { entry := d.entry, cone := h, parameters := d.sets, accept := d.accepts, delta := d.delta, fuel := d.fuel,
    checked := d.checked, lock := d.pinned }

demanding : Demanding := { lawDemand := lawDemand, recorded := recorded }
````

### `plan.lth`

````
-- plan.lth: the plan as a value: the dataflow of a cone, a schedule that linearizes it, the live
-- subgraph a demand reaches, the strategy as a parameter, the law `Confluent`, and the key under
-- which a result is kept.
--
-- Draft 0, 2026-10-15, by Claude Fable 5.1, an agent of the coordinating session, on the brief
-- record/IA/demand-2026-10-15/prompt.md (step 6.1 of
-- record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md). Sources: spec 8.S3,
-- 8.S4, 8.S5, 8.S8, 8.S9, 8.S10, 8.S11 (docs/spec/08-demand.md); L5.2, L5.6, L5.11, L5.13, L5.14,
-- P11; D-2026-10-10-d (forward on demand; results kept under a hash), D-2026-10-13-g (the plan a
-- value of this file, `Confluent` the law an order of evaluation is certified against; the key of
-- 8.S8), D-2026-10-14-c (every law Boolean); the retired `lib/plan.lut` at v0.1-final (a718abc:
-- `Dataflow`, `Schedule`, `Linearizes`, `run`, `Equivalent`, `Confluent` over `Fin n`), rewritten
-- over names; demand.lth (`Demand`); certification.lth §4 (the pattern of a hash's laws). Pattern
-- of certification.lth.
--
-- What this file states. A dataflow says, for each name of a cone, what it reads and how its
-- value follows from theirs (8.S4: a demand's plan is the dataflow of its cone). A schedule is an
-- order of names; it linearizes the dataflow when it holds each live name once and none before
-- what it reads (L5.2: each node once and whole). Running a schedule computes the names in its
-- order; `Confluent` says any two linearizations give every name the same value, which holds
-- because a definition has no effects (8.S5), and is here a Boolean law a dataflow is certified
-- against (8.S11, L5.11), with the two schedules as the parameters a test draws. A plan is the
-- live subgraph the entry reaches with a schedule of it and the strategy that chose the order
-- (8.S4: the strategy is a parameter). The key of 8.S8 is stated with the laws a hash of it owes;
-- 8.S10 says the memo that would read it does not exist, so plan_model.lut gives it no model. The
-- backward pass from a demand and a program to a dataflow is a hole (8.S11: not written). What
-- the brief or the spec leaves open is marked [proposed] at the item above it.
--
-- Index (all sections written in this draft):
--   §1 The dataflow over names; the live subgraph an entry reaches (8.S3, 8.S4, L5.13).     done
--   §2 Schedules: linearizing, running, `Confluent` (8.S5, 8.S11, L5.2, L5.11).             done
--   §3 The plan and the strategy; the backward pass as a hole (8.S4, 8.S11).                done
--   §4 The key of a result (8.S8, 8.S9, 8.S10, L5.6).                                       done
--   §5 The theory `Planning`, the laws of §2 to §4 claimed.                                  done

import "demand.lth" Demand Decoration
import "certification.lth" Value Hash
import "generators.lth" Seed
import "term.lth" Term Program

-- ---------------------------------------------------------------- §1 The dataflow

-- A node of the dataflow: a name and the names it reads (8.S6: a dependence is an edge; a
-- parameter is a node with nothing read). A dataflow over values of `A`: its nodes, the value a
-- name holds before it is computed, and how a name's value follows from the values so far.
-- [proposed] The nodes are listed in the program's order; a name read that no node defines is a
-- leaf that keeps `init` (a hole the demand did not fill is an error that flows, 8.S3).
Node = { name : String, reads : List String }
Dataflow (A : U) = { nodes : List Node, init : A, step : String -> (String -> A) -> A }

memberStr (x : String) (xs : List String) : Bool := match xs { nil -> false ; cons y rest -> x == y or memberStr x rest }
subset (xs ys : List String) : Bool := match xs { nil -> true ; cons x rest -> memberStr x ys and subset rest ys }
sameMembers (xs ys : List String) : Bool := subset xs ys and subset ys xs
noDuplicates (xs : List String) : Bool := match xs { nil -> true ; cons x rest -> not (memberStr x rest) and noDuplicates rest }
count (xs : List Node) : Nat := match xs { nil -> 0 ; cons x rest -> 1 + count rest }
names (ns : List Node) : List String := match ns { nil -> nil ; cons n rest -> cons n.name (names rest) }
readsOf (ns : List Node) (x : String) : List String :=
  match ns { nil -> nil ; cons n rest -> if n.name == x then n.reads else readsOf rest x }
-- the names added at the end, each once, in the order met
addNew (xs new : List String) : List String :=
  match new { nil -> xs ; cons n rest -> if memberStr n xs then addNew xs rest else addNew (appendOne xs n) rest }
appendOne (xs : List String) (n : String) : List String := match xs { nil -> [n] ; cons x rest -> cons x (appendOne rest n) }
readsOfAll (ns : List Node) (xs : List String) : List String :=
  match xs { nil -> nil ; cons x rest -> addNew (readsOf ns x) (readsOfAll ns rest) }

-- The live subgraph (8.S3, L5.13): what the entry reaches along `reads`, the backward pass over
-- names that computes no value; closed in as many rounds as there are nodes, so it ends on a
-- cycle too. What it does not reach, the complement of the cone, is not produced.
expand (ns : List Node) (seen : List String) (k : Nat) : List String :=
  if k == 0 then seen else expand ns (addNew seen (readsOfAll ns seen)) (k - 1)
reaches (A : U) (d : Dataflow A) (entry : String) : List String := expand d.nodes [entry] (count d.nodes)

-- ---------------------------------------------------------------- §2 Schedules

-- A schedule: names in the order they are computed. It linearizes a dataflow on a set of names
-- when it holds exactly those, each once (L5.2: each node once), and none before what it reads
-- among them (a name read outside the set is a leaf, §1).
Schedule = List String
placedBefore (ns : List Node) (placed s : List String) : Bool :=
  match s { nil -> true ; cons n rest -> subset (keep placed (readsOf ns n)) placed
                                         and subset (readsOf ns n) (addNew placed rest) and placedBefore ns (cons n placed) rest }
keep (within xs : List String) : List String :=
  match xs { nil -> nil ; cons x rest -> if memberStr x within then cons x (keep within rest) else keep within rest }
LinearizesOn (A : U) (d : Dataflow A) (live : List String) (s : Schedule) : Bool :=
  sameMembers s live and noDuplicates s and placedBefore d.nodes nil s

-- Running a schedule: each name in its order, from the values so far; a name not scheduled keeps
-- `init`.
update (A : U) (env : String -> A) (n : String) (v : A) : String -> A := fn m { if m == n then v else env m }
runFrom (A : U) (d : Dataflow A) (s : Schedule) (env : String -> A) : String -> A :=
  match s { nil -> env ; cons n rest -> runFrom A d rest (update A env n (d.step n env)) }
run (A : U) (d : Dataflow A) (s : Schedule) : String -> A := runFrom A d s (fn m { d.init })

-- Two schedules are equivalent on a set of names when every name of it gets the same value under
-- both; `Confluent` (8.S5, 8.S11, L5.11, D-2026-10-13-g): any two linearizations are equivalent.
-- The law a dataflow is certified against, with the schedules drawn; a session block reordered
-- is one more pair it covers (8.S14).
allNames (p : String -> Bool) (xs : List String) : Bool := match xs { nil -> true ; cons x rest -> p x and allNames p rest }
EquivalentOn (A : U) (eq : A -> A -> Bool) (d : Dataflow A) (live : List String) (s1 s2 : Schedule) : Bool :=
  allNames (fn n { eq (run A d s1 n) (run A d s2 n) }) live
Confluent (A : U) (eq : A -> A -> Bool) (d : Dataflow A) (live : List String) (s1 s2 : Schedule) : Bool :=
  not (LinearizesOn A d live s1 and LinearizesOn A d live s2) or EquivalentOn A eq d live s1 s2

-- ---------------------------------------------------------------- §3 The plan

-- The strategy, a parameter separate from the program (8.S4, L5.2, P11): forward on demand, the
-- default 8.S3 decides (the live subgraph in topological order, computed strictly); or call by
-- need, what `run.py` does today (each name reduced at its first demand and kept), which computes
-- the same live subgraph in the order of first demand. Both are linearizations, so by `Confluent`
-- they agree. [proposed] Whether the strategy is a field of the demand is open; 8.S1 does not
-- list it, so here it is an argument of the plan with its default.
Strategy : U := data {
  ForwardOnDemand : Strategy ;
  CallByNeed : Strategy ;
}

-- A plan: the strategy that chose it, the entry, the live subgraph and a schedule of it
-- (D-2026-10-13-g: the plan is a value; L5.6: its hash enters the identity of a result).
Plan (A : U) = { strategy : Strategy, entry : String, live : List String, schedule : Schedule }

-- The backward pass from a program to its dataflow (8.S4: a demand's plan is the dataflow of its
-- cone; 8.S11: a function from a demand and a program to a plan, not written): a hole. The
-- values of the dataflow are terms, the kernel's reduction its `step` (term.lth §5).
dataflowOf : Program -> Dataflow Term
-- and the plan of a demand on a program, by the strategy given, call by need unless another is
-- asked [proposed, 8.S4: the default implemented is call by need; 8.S3's decided default is
-- forward on demand]
planOf (eq : Term -> Term -> Bool) (p : Planning Term eq) (d : Demand) (prog : Program)
       (strategy : Strategy <- CallByNeed) : Plan Term :=
  p.plan strategy (dataflowOf prog) d.entry

-- ---------------------------------------------------------------- §4 The key of a result

-- Of the demand, the key holds only what the cone reads (8.S8): the type demanded, always read,
-- and the values given to holes that are live; a parameter the cone does not read leaves the key
-- as it was.
DemandKey = { decoration : Maybe Decoration, values : List (String * Value) }
keepRead (live : List String) (vs : List (String * Value)) : List (String * Value) :=
  match vs { nil -> nil ; cons (n, v) rest -> if memberStr n live then cons (n, v) (keepRead live rest) else keepRead live rest }
demandKey (d : Demand) (live : List String) : DemandKey := { decoration := d.decoration, values := keepRead live d.sets }
withSet (d : Demand) (n : String) (v : Value) : Demand :=
  { entry := d.entry, decoration := d.decoration, accepts := d.accepts, delta := d.delta, fuel := d.fuel,
    sets := cons (n, v) d.sets, checked := d.checked, pinned := d.pinned }

-- The identity of a result (8.S8, L5.6, D-2026-10-13-g): the demand's key, the hash of the cone
-- (the code, the hosts behind its externs and the interpreter, certification.lth §4), the mode,
-- the seed, the hash of the plan, and the hashes of the certificates of the live cone. A hit
-- serves a demand only with an equal key (8.S9); the memo that would hold it does not exist
-- (8.S10), and `x.run.json` is written and never read back. [proposed] The mode is a string: 8.S1
-- names `m` and the spec does not define it; today the only mode is `--checked`, printed.
MemoKey = { demand : DemandKey, cone : Hash, mode : String, seed : Seed, plan : Hash, certificates : List Hash }
withDemand (k : MemoKey) (dk : DemandKey) : MemoKey :=
  { demand := dk, cone := k.cone, mode := k.mode, seed := k.seed, plan := k.plan, certificates := k.certificates }
withCone (k : MemoKey) (h : Hash) : MemoKey :=
  { demand := k.demand, cone := h, mode := k.mode, seed := k.seed, plan := k.plan, certificates := k.certificates }
withMode (k : MemoKey) (m : String) : MemoKey :=
  { demand := k.demand, cone := k.cone, mode := m, seed := k.seed, plan := k.plan, certificates := k.certificates }
withSeed (k : MemoKey) (s : Seed) : MemoKey :=
  { demand := k.demand, cone := k.cone, mode := k.mode, seed := s, plan := k.plan, certificates := k.certificates }
withPlan (k : MemoKey) (h : Hash) : MemoKey :=
  { demand := k.demand, cone := k.cone, mode := k.mode, seed := k.seed, plan := h, certificates := k.certificates }
withCertificates (k : MemoKey) (hs : List Hash) : MemoKey :=
  { demand := k.demand, cone := k.cone, mode := k.mode, seed := k.seed, plan := k.plan, certificates := hs }

-- The hash of a key and of a plan are the host's, as the hash of a cone is (certification.lth
-- §4). Their laws (8.S2: equal demands give equal keys, which a function gives; 8.S11: the key
-- changes when any input of 8.S8 changes): two keys that differ in one input have different
-- hashes. [proposed] As in certification.lth §4, a collision of the hash function is the host's,
-- and a sample that finds one refutes the model.
Keying (A : U) : { key : MemoKey -> Hash, planHash : Plan A -> Hash }
KeySeesTheDemand (A : U) (h : Keying A) (k : MemoKey) (dk : DemandKey) : Bool := dk == k.demand or not (h.key (withDemand k dk) == h.key k)
KeySeesTheCone (A : U) (h : Keying A) (k : MemoKey) (c : Hash) : Bool := c == k.cone or not (h.key (withCone k c) == h.key k)
KeySeesTheMode (A : U) (h : Keying A) (k : MemoKey) (m : String) : Bool := m == k.mode or not (h.key (withMode k m) == h.key k)
KeySeesTheSeed (A : U) (h : Keying A) (k : MemoKey) (s : Seed) : Bool := s == k.seed or not (h.key (withSeed k s) == h.key k)
KeySeesThePlan (A : U) (h : Keying A) (k : MemoKey) (p : Hash) : Bool := p == k.plan or not (h.key (withPlan k p) == h.key k)
KeySeesTheCertificates (A : U) (h : Keying A) (k : MemoKey) (hs : List Hash) : Bool :=
  hs == k.certificates or not (h.key (withCertificates k hs) == h.key k)
PlanHashSeesTheSchedule (A : U) (h : Keying A) (p : Plan A) (s : Schedule) : Bool :=
  s == p.schedule or not (h.planHash { strategy := p.strategy, entry := p.entry, live := p.live, schedule := s } == h.planHash p)
Keying (A : U) := KeySeesTheDemand A & KeySeesTheCone A & KeySeesTheMode A & KeySeesTheSeed A & KeySeesThePlan A
  & KeySeesTheCertificates A & PlanHashSeesTheSchedule A

-- ---------------------------------------------------------------- §5 The theory

-- A model of planning gives, for a strategy, a dataflow and an entry, a plan.
Planning (A : U) (eq : A -> A -> Bool) : { plan : Strategy -> Dataflow A -> String -> Plan A }

-- §3. 8.S4, L5.13: a plan is of the strategy and entry asked, and its live set is what the entry
-- reaches, no more and no less
PlanIsTheLiveCone (A : U) (eq : A -> A -> Bool) (p : Planning A eq) (st : Strategy) (d : Dataflow A) (e : String) : Bool :=
  (p.plan st d e).strategy == st and (p.plan st d e).entry == e and sameMembers (p.plan st d e).live (reaches A d e)
-- 8.S3, L5.2: its schedule linearizes the live cone, each name once, none before what it reads
PlanLinearizes (A : U) (eq : A -> A -> Bool) (p : Planning A eq) (st : Strategy) (d : Dataflow A) (e : String) : Bool :=
  LinearizesOn A d (p.plan st d e).live (p.plan st d e).schedule
-- 8.S4, 8.S5: two strategies give one result on the live cone (an instance of `Confluent`)
StrategiesAgree (A : U) (eq : A -> A -> Bool) (p : Planning A eq) (s1 s2 : Strategy) (d : Dataflow A) (e : String) : Bool :=
  EquivalentOn A eq d (reaches A d e) (p.plan s1 d e).schedule (p.plan s2 d e).schedule
-- 8.S4: the two strategies named, call by need (run.py today) and forward on demand (8.S3's
-- default), compute the same live subgraph and give every name of it one value
TheDefaultsAgree (A : U) (eq : A -> A -> Bool) (p : Planning A eq) (d : Dataflow A) (e : String) : Bool :=
  sameMembers (p.plan CallByNeed d e).live (p.plan ForwardOnDemand d e).live
    and EquivalentOn A eq d (reaches A d e) (p.plan CallByNeed d e).schedule (p.plan ForwardOnDemand d e).schedule
-- 8.S11, L5.11: the dataflow of a plan is confluent, on the schedules drawn
PlanIsConfluent (A : U) (eq : A -> A -> Bool) (p : Planning A eq) (d : Dataflow A) (e : String) (s1 s2 : Schedule) : Bool :=
  Confluent A eq d (reaches A d e) s1 s2
-- §4. 8.S8: a value given to a hole the cone does not read leaves the demand's key as it was
KeyReadsOnlyTheCone (A : U) (eq : A -> A -> Bool) (p : Planning A eq) (st : Strategy) (d : Dataflow A) (dm : Demand) (n : String) (v : Value) : Bool :=
  memberStr n (p.plan st d dm.entry).live
    or demandKey (withSet dm n v) (p.plan st d dm.entry).live == demandKey dm (p.plan st d dm.entry).live
-- 8.S8: the type demanded is always in the key: a value and its derivative have two keys
KeyReadsTheType (A : U) (eq : A -> A -> Bool) (p : Planning A eq) (dm : Demand) (live : List String) : Bool :=
  (demandKey dm live).decoration == dm.decoration

Planning (A : U) (eq : A -> A -> Bool) := PlanIsTheLiveCone A eq & PlanLinearizes A eq & StrategiesAgree A eq
  & TheDefaultsAgree A eq & PlanIsConfluent A eq & KeyReadsOnlyTheCone A eq & KeyReadsTheType A eq
````

### `plan_model.lut`

````
-- plan_model.lut: the default plan, call by need as run.py does, and forward on demand, over a
-- small dataflow; the reference model of `Planning`.
--
-- Draft 0, 2026-10-15, by Claude Fable 5.1, an agent of the coordinating session, on the brief
-- record/IA/demand-2026-10-15/prompt.md. A model file (12.S23): `planning` schedules the live
-- cone by the strategy asked; `byNeed` is the order run.py reduces in (8.S4: each name at its
-- first demand, kept), `forward` the strict topological order of 8.S3; `example` is a dataflow of
-- five names of which the entry reaches four, and the two plans of it agree (`Confluent`). The
-- memo of 8.S8 has no model: 8.S10 says the result store does not exist, and plan.lth's `Keying`
-- waits for the host's hash of a key, as certification_model.lut's `hashing` is for a cone.

import "plan.lth" Planning Plan Dataflow Node Schedule Strategy ForwardOnDemand CallByNeed reaches memberStr appendOne
  subset count LinearizesOn EquivalentOn Confluent

-- call by need: the order of first demand, each name after what it reads and once (a depth-first
-- visit from the entry, in the order the reads are listed); bounded by the count of nodes, so a
-- cycle ends
visit (A : U) (d : Dataflow A) (n : String) (done : List String) (k : Nat) : List String :=
  if memberStr n done or k == 0 then done else appendOne (visitAll A d (readsIn d.nodes n) done (k - 1)) n
visitAll (A : U) (d : Dataflow A) (ns : List String) (done : List String) (k : Nat) : List String :=
  match ns { nil -> done ; cons n rest -> visitAll A d rest (visit A d n done k) k }
readsIn (ns : List Node) (x : String) : List String :=
  match ns { nil -> nil ; cons n rest -> if n.name == x then n.reads else readsIn rest x }
byNeed (A : U) (d : Dataflow A) (entry : String) : Schedule := visit A d entry nil (1 + count d.nodes)

-- forward on demand: the live names placed strictly, each as soon as what it reads among the live
-- names is placed, in the order of the live set; a name no round can place (a cycle) is left out
placeable (ns : List Node) (live placed : List String) (n : String) : Bool :=
  not (memberStr n placed) and subset (readsAmong ns live n) placed
readsAmong (ns : List Node) (live : List String) (n : String) : List String := keepIn live (readsIn ns n)
keepIn (within xs : List String) : List String :=
  match xs { nil -> nil ; cons x rest -> if memberStr x within then cons x (keepIn within rest) else keepIn within rest }
round (ns : List Node) (live placed candidates : List String) : List String :=
  match candidates { nil -> placed ; cons n rest ->
    round ns live (if placeable ns live placed n then appendOne placed n else placed) rest }
rounds (ns : List Node) (live placed : List String) (k : Nat) : List String :=
  if k == 0 then placed else rounds ns live (round ns live placed live) (k - 1)
forward (A : U) (d : Dataflow A) (live : List String) : Schedule := rounds d.nodes live nil (1 + count d.nodes)

plan (A : U) (st : Strategy) (d : Dataflow A) (entry : String) : Plan A :=
  { strategy := st, entry := entry, live := reaches A d entry,
    schedule := (match st { CallByNeed -> byNeed A d entry ; ForwardOnDemand -> forward A d (reaches A d entry) }) }

eqNat (x y : Nat) : Bool := x == y
planning : Planning Nat eqNat := { plan := plan Nat }

-- the example: a = 1, b = a + 1, c = a * 2, d = b + c, e = d + 100; the entry `d` reaches four
-- names and `e` is not produced (L5.13)
example : Dataflow Nat := {
  nodes := [{ name := "a", reads := nil }, { name := "b", reads := ["a"] }, { name := "c", reads := ["a"] },
            { name := "d", reads := ["b", "c"] }, { name := "e", reads := ["d"] }],
  init := 0,
  step := fn n env { if n == "a" then 1 else if n == "b" then env "a" + 1 else if n == "c" then env "a" * 2
                     else if n == "d" then env "b" + env "c" else if n == "e" then env "d" + 100 else 0 },
}
-- call by need gives a, b, c, d; forward on demand gives a, b, c, d too on this example, since the
-- live set is listed from the entry (d, b, c, a) and a round places what it can
needPlan : Plan Nat := plan Nat CallByNeed example "d"
forwardPlan : Plan Nat := plan Nat ForwardOnDemand example "d"
bothLinearize : Bool := LinearizesOn Nat example needPlan.live needPlan.schedule
  and LinearizesOn Nat example forwardPlan.live forwardPlan.schedule
-- and a third linearization by hand, c before b, gives the same values (8.S5)
agree : Bool := Confluent Nat eqNat example needPlan.live needPlan.schedule ["a", "c", "b", "d"]
  and EquivalentOn Nat eqNat example needPlan.live needPlan.schedule forwardPlan.schedule
````

### `08-demand.md`

````
# 8. The demand and the plan

Chapter 8 of the specification, draft 0, 2026-10-13. Sources: `docs/principles.md` L5, L4, L10.5, L10.6, L12.3, O5, O8 and O12; the decisions D-2026-10-10-c, -d and -e, D-2026-10-11-i and -n, D-2026-10-12-h, -m, -r, -ac, -ad and -al; `docs/spec/02-grammar.md` §8, `docs/spec/06-certification.md` §7 and `docs/spec/12-files-and-tools.md` §5 and §6, all at the commit that holds this file; `src/luthier/cli.py`, `machine.py` and `lib/plan.lth`, read only. Written by Claude Sonnet 5.5, as wave 3 of the specification. It realizes L5. The form of the demand is a library's (D-2026-10-12-al), so this chapter states what the core asks of a demand and leaves its representation open. Actions and the world are `spec 10`; specimens and the planner's ranking are `spec 9`.

## §1 Notation

Beyond `spec 1`, this chapter writes: `C` is the type of costs of `spec 6.S4`, with the five operations of `spec 6.S5`; `d` is a demand; `e` is a name or a term, the entry of a demand; `h(e)` is the hash of the dependency cone of `e` in canonical form (`spec 6 §1`); `m` is a mode of evaluation; `s` is a seed.

## §2 What a demand is

**8.S1. A demand is open, and the type demanded reinterprets the cone.** [decided D-2026-10-13-f] A demand is the gate through which parameters change what the program does, and it is not closed: whatever the program declares as a parameter, the demand may set. It carries an entry `e`; the type demanded of it; a cutoff, a bound and an evidence cost in `C` (`spec 6.S15`); a confidence δ for sampled evidence (D-2026-10-12-r); the evidence cost it assigns to assumptions, with no default (`spec 6.S10`); limits on resources if the action wants them; and the values of the program's holes, which `run --set` gives today (`spec 12.S18`). Every threshold or level a certificate needs comes from it and is recorded with it (L5.18). The first demand of all, made by an action nobody called, takes these as declared default arguments, so the root is a parameter too (L5.19). A demand made inside another is passed down from the caller and not recomputed from the cone, because a cutoff does not compose (L12.3). Asking for `t : P T` where the program computes a `T` asks the cone of `t` to build a `P T` instead: a value with its derivative, with an interval that encloses it, with a distribution, or exact in `Rational`, the decorated output of O5. The cone is written generic over a type operator `G`, with `G` the identity by default, and the demand replaces `G` by `P`; spec 11.S3, generic in the number type, is the first instance. [proposed] Whether the generic form is written by hand or derived by Luthier from the cone, which as data can be reinterpreted (L7.4), is open. A certificate obtained at the identity carries over to `P` by parametricity for the laws that hold of any `G` (Wadler, *Theorems for free!*, 1989) when `P` satisfies the laws of the table below; a law over numbers, stated with a distance, is certified again at `P` or carries the distance `P` adds.

**8.S2. What the core asks of a demand and of a decoration.** [decided D-2026-10-13-g] The core uses these operations, and no others; a library may add to them.

| operation | used for | laws |
|---|---|---|
| `entry d` | the name or term to evaluate | none |
| `type d` | the type demanded, possibly `P T` (8.S1) | none |
| `cutoff d` | a pair in `C`, compared with a certificate by `≤` (`spec 6.S15`) | none |
| `delta d` | the confidence of sampled evidence | a value of the type the library's conversion takes (`spec 7.S11`) |
| `assumed d` | the evidence cost of an assumption | none; an absent value refuses every assumed name |
| `key d` | the parameters of a demand that enter the identity of a result: those its cone reads (8.S8) | equal demands give equal keys; the key is a hash of a canonical form, and includes `type d` |
| `map` of `P` | carrying a function of the cone into `P` | the functor laws: `map id = id`, `map (g ∘ f) = map g ∘ map f` |
| `pure` and the product of `P` | carrying constants and functions of several arguments | the applicative laws, so that every operation of the cone has its image in `P` |

Whether the cutoff is a pair or two operations is the library's. The theories that state this table are `lib/demand.lut` and, for the decorations, the library of each `P`; neither is written.

## §3 The plan

**8.S3. Forward on demand.** [decided D-2026-10-10-d] The default strategy is a plan backward from the demand over names, that computes no value; then the live part of the graph is run strictly forward, in topological order, every node once and complete (L5.2). A branch whose use depends on a value marks both branches live. Three conditions bear on it: errors and holes are values that flow, so a live branch nobody uses cannot abort the run; results are memoized in a store keyed by the hash of code, inputs and mode, its retention policy a parameter; tests are actions, so verifying everything is demanding every test and verifying on demand is demanding the tests of what an action uses. What the demand does not need, the complement of its cone, is not produced (L5.13).

**8.S4. The strategy is a parameter.** [decided D-2026-10-10-d] The strategy is separate from the program (L5.2, P11), and only the default is to be implemented. [implemented] Today there is no plan: `run` evaluates the entry by call by need (in `run.py` since 9fc993f a bound value, an argument, a pattern's binding or a constant is a shared cell reduced at its first demand and kept, `record/IA/run-2026-10-13/report-9.md`), which evaluates only what the entry reaches and so computes the same live subgraph, but interleaved with the run and without a plan as a value. The state of the cone is read before evaluating (12.S18). [decided D-2026-10-13-g] The plan is a value of `lib/plan.lth`, which exists and states a dataflow, a schedule, and the law `Confluent` (any two linearizations agree); what it lacks is the backward pass and the memo key, and a demand's plan is the dataflow of its cone.

**8.S5. A definition has no effects.** [decided D-2026-10-10-c] What a definition computes depends only on its inputs, so every strategy gives one result and independent items commute (`spec 2.S17`). Effects live in actions, whose treatment is `spec 10`; the actions on Luthier's own state, a certificate or a test, are idempotent and memoizable, those on the world never (D-2026-10-12-m).

**8.S6. Mutation as before and after.** [decided D-2026-10-10-e] A mutable parameter is two variables, `x1 = f x0`, and the dependence is an edge of the graph. Changing a value in place is an optimization of the plan, allowed when `x0` has no consumer after `f`, the analysis that also frees a node after its last consumer (L5.14). The surface form that mutates is a library's and translates to the two names. Nothing in the interpreter mutates a parameter today.

**8.S7. What a demand reads.** [decided D-2026-10-12-ad] The checker is a demand for names and types; `run` and `test` are demands for values. Reading a file waits for a demand that needs it: the rule and its consequences for imports and externs are `spec 12.S21` and `spec 3.S40`, not restated. [implemented] The loader reads imports at once, and the checker resolves an extern at check time; the lazy reading of externs waits.

## §4 The memo and the identity of a result

**8.S8. The identity of a result.** [decided D-2026-10-10-d] A result is identified by the hash `h(e)` of its cone, the inputs, the mode, the type demanded and the tolerance, the model its type names, the seed, the plan that produced it, and the certificates' hashes for the part of the cone that is live (L5.6); the host's code behind an extern, read when the demand reaches it, enters through the cone (`spec 6.S8`). So a changed library or platform gives a new result. That results are kept under a hash is D-2026-10-10-d; the list of what enters it is L5.6, and the record that carries it is O12. [decided D-2026-10-13-g] The key is built from `key d` (8.S2), `h(e)`, `m`, `s` and the plan's own hash, and the hashes of certificates are those of `spec 6.S6`. Of the demand, the key holds only the parameters the cone of `e` reads: a parameter is a node of the graph, so a result depends on those in its cone and on no other, and changing a parameter it does not read leaves the key, and the memo, as they were. The type demanded is always read, so a value and its derivative have two keys.

**8.S9. A hit serves a demand only if it meets the demand.** [decided D-2026-10-12-h] For certificates a memo hit is compared with the cutoff of the demand that reaches it, at the hit (`spec 6.S15`, L10.5): a certificate issued for a tight cutoff serves every looser one, and a stricter demand than any entry is a new node of a new plan (L5.9). Writing a certificate is idempotent. [decided D-2026-10-13-g] For results the key of 8.S8 includes the tolerance, so a hit needs equal keys; whether a result computed under a tighter tolerance may serve a looser demand is not settled and is left out until a case needs it (P8).

**8.S10. Two caches.** [decided D-2026-10-10-d] What is derivable from an expression does not depend on the demand; what is produced does. The elaboration (types, derivable laws) is one cache and the memo of results is the other (L5.16). The run database that the planner reads does not enter a result's identity after the plan is chosen (L5.8). [implemented] Today the only memo is the sharing of a run's bound values and of a materialized lambda's entries (`run.py`, 8.S4, 3.S25), local to one run and keyed by the cell. The result store of D-2026-10-10-d does not exist, and `x.run.json`, which records the hash of the cone, the time, the parameters and the result (12.S18), is written and never read back, so it does not serve as a memo.

**8.S11. Where the plan lives in Luthier.** [decided D-2026-10-13-g] `lib/plan.lth` is the carrier named in L5.6 and L14: a plan is a value, the memo key contains its hash, and its `Confluent` law is what an order of evaluation is certified against (L5.11). The additions it needs are the key of 8.S8, a function from a demand and a program to a plan, and the law that the key of a result changes when any input of 8.S8 changes. They are not written.

## §5 The session

**8.S12. A session is a block over the dataflow.** [implemented] A session builds a block item by item (`spec 2.S18`; the commands are `spec 12.S20`). With `<-` an item explores: it binds a name, and rebinding is allowed; the first binding of a name and its later ones are distinct nodes, `x0`, `x1` (8.S6). With `:=` an item locks: it defines once (`spec 2.R3`, `spec 2.R4`). With the lines `x <- 1`, then `y := x + 10`, then `x <- 2`, `y` stays 11, because it depends on the first `x` (L5).

**8.S13. What a line re-evaluates.** [implemented] Today each line re-evaluates the whole block so far, with no memo (`cmd_session`); the line is wrapped as the block `{ items ; line }`, and it joins the block only if it checked and evaluated. [proposed] A line re-evaluates only the nodes whose cone changed: a node whose key (8.S8) is already in the memo is served, so adding an item does not recompute the earlier ones, and rebinding `x` recomputes exactly what depends on the new `x`. This is O8's memo between items, and it needs no new rule once 8.S8 holds, since a session item is a definition (`spec 2.S17`).

**8.S14. Sessions that differ in the order of independent items.** [decided D-2026-10-11-i] Reordering independent bindings gives an equivalent session, by the law `Confluent`, the law of `lib/plan.lth` that the session block is certified against (L5.11). A session saved to a file becomes the `main` block (L5.12); a file is never a block (`spec 2.S17`).

**8.S15. The trace.** [decided D-2026-10-13-g] L5 names no trace; what exists is the run record of 12.S18. If the planner or the user needs to see what a demand did, the core asks of a library of traces one operation, `record d p r`, that appends the demand, the plan and the result key to a store, with the law that appending never changes an earlier entry (P2, L10.4). The library's form is open (D-2026-10-12-al).

## Open

- O5, the decorated output (L5.4): which model the planner chooses for a demand and how it inserts the bridges, here only as the demanded type of 8.S8.
- O8, the session as a block, and what is kept from item to item (8.S13).
- O12, the record that carries a result's identity, and `lib/plan.lth` as its carrier (8.S8, 8.S11).
````
