# Review of layer 3 of Luthier, generators, tests and laws (round 1, bundle C)

You are reviewing theory files written in Luthier, a language whose interpreter is being rebuilt from its own theories: a type is a theory (a structure with laws), a value of it is a model, and the language certifies models against their theories by testing. A theory file (`.lth`) declares a record type of operations, states its laws as Bool-valued definitions over a model (`(m : T)`), and defines the theory as their conjunction (`T := Law1 & Law2`); a model file (`.lut`) holds values of theories. Every constructor of a `data` must have a law stating its role (principle L2.7: a definition is a concept; distinct constructors and accessors state no role). A law quantifies over the subtype it means rather than over an implication whose premise random cases rarely meet. The files parse with the project's parser; nothing yet type-checks or certifies them, so you are the first check of their meaning. Grammar, kernel and earlier layers were reviewed in earlier rounds and are not in scope. Do not reopen a decision listed under "Decisions the files cite" unless a file contradicts it; where you disagree with the specification itself, say so as a separate item.

This prompt covers generators, tests and laws (layer 3, bundle C of its external review; world, certification, demand and plan are reviewed apart and not included). `generators.lth` states generators as values (from a size and a seed, a value and the next seed), the generic ones over a type's form, sizes, subtypes, censuses and budgets, each with the theory it is a model of. `test.lth` states a test as data, what running it gives, and the grade of what it gives. `laws.lth` states what a law's value must give, the laws of relations, and a law as a theory with its evidence. `generators_model.lut` and `test_model.lut` are models. The chapters they realize are `docs/spec/07-tests.md` and `docs/spec/05-laws.md`. The material below, in this order: terms and principles L2.7, L9.6, L10, L11 and P11; the decisions the files cite; then the seven files. Frozen at commit 2710cfc.

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
9. **A missing generator**: which generator is missing for a sampled law that today runs on listed cases only (spec 7.R1 and 7.R4: a test names its generators; a law over the models of a theory is certified per model). Name the law, the type it quantifies over, and the generator it would need.

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

D-2026-10-06-ab Generators and certificates, his answers on record/generators-2026-10-06.md. A
                test says which generators it used, binding by parameter as the base and named
                profiles as an abbreviation, and its certificate records the choices expanded.
                Generators are values of Luthier; the random source is an extern whose laws of
                stochasticity are stated in Luthier. Generators are functors over a type
                (`exhaustive`, a static error on an infinite type; `sampled` with a linear or a
                logarithmic metric), with sampling by a cumulative cost as a candidate to unify
                numbers and lists. There are generators only of defined types; drawing over `U`
                is a static error. The bounds of a number are part of its type. A certificate of
                a function covers what its generators drew, and a run must stay inside it; a
                result is checked once, when produced. A statistical law declares its level,
                repeats a failure with an independent seed and measures its power on controls.
                The matrix families of the analysis stand. A function over an infinite domain
                is drawn from a census of the program's values. Every budget (the tries of a
                rejection first) is an argument, and a law not run is not run again while its
                code and seed are unchanged.
Author:     Luciano; the bindings, the certificate of results and the three parts of 5.5 the
            model's proposals, accepted
Quote:      "yo quisiera que los tests  pidan un generador explicito para cada tipo involucrado."
            "Bueno, seria el caso mas simple: un censo sobre los valores registrados no?"
            "Los generadores son Luthier citizens como cualquier otro."
            "O sea en realidad la idea es solo tengo generadores  sobre tipos definidos."
            "Listo."
            "la tolerancia de Levenberg-Marquardt no puede ser cualquiera, tiene limites"
            "OK"
            "OK"
            "Si, exacto."
            "Estoy evaluando si los generadores deberian ser propiedad del tipo o functores sobre
            el tipo"
            "Los geradores de matrices ya los planteaste bien."
            "OK"
Source:     chat:aa680014:3732
            chat:aa680014:3732
            sonolocalizacion@6485d1a:Lucianos feedbacks/oct 6 0703.txt:62
            sonolocalizacion@6485d1a:Lucianos feedbacks/oct 6 0703.txt:54
            sonolocalizacion@6485d1a:Lucianos feedbacks/oct 6 0734.txt:32
            sonolocalizacion@6485d1a:Lucianos feedbacks/oct 6 0734.txt:36
            sonolocalizacion@6485d1a:Lucianos feedbacks/oct 6 0734.txt:45
            sonolocalizacion@6485d1a:Lucianos feedbacks/oct 6 0734.txt:62
            sonolocalizacion@6485d1a:Lucianos feedbacks/oct 6 0734.txt:66
            sonolocalizacion@6485d1a:Lucianos feedbacks/oct 6 0734.txt:71
            sonolocalizacion@6485d1a:Lucianos feedbacks/oct 6 0734.txt:72
            sonolocalizacion@6485d1a:Lucianos feedbacks/oct 6 0703.txt:77
Kind:       language and tool (spec 7; the decisions listed at the head of the old 08, d12b554).
            For L10.3, L5.18, P11
Status:     current; the functors and the cumulative cost were "estoy evaluando" (his leaning,
            "creo que es lo segundo"), the rest answered. The request that started the analysis is
            of 2026-10-05 (chat:aa680014:3732); the "OK" of 0703:77 answers the round of R11, the
            budget of rejection as an argument and no rerun of laws not run. Entered 2026-10-12 by
            the same session

D-2026-10-06-ac The grammar of D-2026-10-06-ab (old 08 §12): `test name [with n | exhaustive]
                [sampled metric] [size k] [under profile] [where { bindings }]`, a new act
                `profile name := { bindings }`, and the act `gen` removed, since no type owns a
                generator.
Author:     the model, writing the specification he asked for
Quote:      "Ok, esta en tus manos. Esta todo especificado? Escribi la especificacion."
Source:     sonolocalizacion@6485d1a:Lucianos feedbacks/oct 6 0734.txt:80
Kind:       language (spec 2.S19, 7.R1). For D-2026-10-06-ab
Status:     replaced in its syntax by D-2026-10-12-ab (`test` a function with named arguments, the
            profile a record value); `gen` removed stands. Entered 2026-10-12 by the same session

D-2026-10-11-a  smartMaybe: a predicate is written once, in its explaining form (the failures
                it finds), and the poorer forms (the first failure, Maybe, Bool) are its
                forgetful projections, chosen by the demand. Laws too return the explaining
                form. The demand asks for the first n failures or for all of them, as a
                compiler's error limit; Bool is the first failure, forgotten. Inverts the
                primacy of 05 §9 (Checks), where Bool is primary and the explaining forms are
                written apart and tied by a law (firstViolation and ReportsValidity).
Author:     Luciano
Quote:      "Yo quisiera un smartMaybe que de acuerdo a la demanda sea o un Maybe comun o un
            maybeError" (note); "Si, vamos con smartMaybe. Y la idea es que podes pedir
            n-fallas o completo (como un compilador, no?)" (chat)
Source:     record/Lucianos ideas/El problema de las tipos recursivos.txt (ba108aa); chat
            (session of 2026-10-11); analysis in record/recursive-types-and-objects-2026-10-11.md
            §4 and §5
Kind:       language design. For L13 (forgetting is determined by the demand), L19 (the demand
            determines the computation), P11 (n is a parameter of the demand). Cost: not of an
            explaining form explains only as much as its success side carries
Status:     current; spec amended (05 §9, 04 §3); not implemented; stopping the fold at n failures is open

D-2026-10-11-d  Laws accumulate; a function need not be characterized. A law may only constrain
                (a subtype of A → B with many inhabitants); a set of laws that determines the
                function up to its equality (the definite description, "à la Russell") is the
                limit a definition may reach, never what it must reach. Requiring it of every
                function would forbid adding laws one at a time, and that is against being
                expressive (organizer E). The implementation of an under-determined function is
                a free choice among the inhabitants (P5), certified against the laws it has.
Author:     Luciano
Quote:      "si es a lo Russell para toda funcion no puedo contruir leyes acumulativamente, y eso
            va en contra de ser expresivo" (chat)
Source:     record/Lucianos ideas/principios organizadores.txt (fa3f972, 1c7a284); chat (session
            of 2026-10-11); record/organizing-principles-2026-10-11.md §5
Kind:       language design, semantics of laws. For E (expressive over restrictive) and P5 (a
            free choice is legitimate); bounds C's "properties that determine the function
            univocally" to the limit case; consistent with L4, L5 as drafted
Clarified:  "à la Russell" in the note does not mean uniqueness; it means definition by
            description, from outside, as against constructive definition by a term: "no ser a lo
            tarski (constructivo) sino a lo matematico (desde afuera, como un entomologo observa
            un bicho)" (chat). The model's reading: Russell's knowledge by description against
            knowledge by acquaintance; a function is known by the properties observed of it, and
            the implementation, native or extern, is the specimen. The accumulation of laws
            stands as decided above. Correction from the audio of 08.58 (45df807, 32:01 to
            34:07): by "Tarski" he means the compositional derivation of a property from the
            properties of the parts (the sum of two normals is normal), not constructivism;
            Luthier wants both routes, derived and observed, and the demand chooses which
            invariances are produced.
Status:     current; settles the first of the two open items of the analysis of 2026-10-11; W5
            (native against extern) still open

D-2026-10-11-f  A function known correct by a theorem outside Luthier is certified `proved` by
                citation: the citation is recorded in the certificate, the grade is `proved`,
                allowed in user code (unlike `axiom`, whose grade `assumed` records nothing). The
                certificate of a law travels to another implementation by a certificate of
                identity: exactly where the identity law is boolean (`==` structural, 05 R8),
                with the observed distance added where it is a cost (G3); the type of the
                identity law's result (Bool or Cost) says which. Proposed syntax `cite name
                "..."`, a directive next to `test`.
Author:     Luciano for the idea (axiom for a known-correct implementation, verified by bitwise
            identity) and the yes; Claude for `proved` by citation instead of `axiom`, the
            condition on floats and the syntax
Quote:      "cuando sabemos por ejemplo que una implementacion es correcta por teorema matematico
            conocido (esto seria algo que requeriria una palabra clave nueva, quizas axiom ?) y
            luego por identidad bitwise con valores conocidos se verifica una implementacion
            externa"; "Si, desde ya" (annotations, 2c18c41, 18da042)
Source:     record/answers-annotations-principles-2026-10-11.md §11, §4; -b.md §11
Kind:       language design, certification (05 §7). For G2 (description), L21, L11; distinguishes
            assumed (no justification) from proved (a citation to check)
Amended:    (same day, his feedback at 9d65118) the citation is a key into a .bib whose entry
            carries a DOI, ISBN or URL resolved by record/bibliography/checkdoi.py; the
            certificate records who checked the correspondence: human, ai+human, or none.
            Proposed syntax `cite name bibkey checked ai+human`. Amended again (c167022): the
            citation is a value of a type Reference (key, doi, isbn, url, sha256, law
            Resolvable), read from a .bib as a module (`biblio.kantorovich1948`), and the
            certificate records its identifiers and hash.
Status:     current; spec amended and implemented 2026-10-11: lib/reference.lut, .bib as a module,
            `cite x biblio.key checked ai+human`, grade proved in the certificate

D-2026-10-11-l  The laws of relations and actions (Reflexive, Symmetric, Antisymmetric,
                Transitive, Total, Associative, the identities, inverses, commutativity,
                distributivity, homomorphism) move from lib/algebra.lut to lib/laws.lut;
                algebra.lut imports it and keeps the structures (Setoid, Monoid, Group, Ring,
                Field and their instances). No change of meaning.
Author:     Luciano for the question; Claude for the split and the name; accepted ("Si a todo")
Quote:      "ahora las leyes de asociatividad, simetria etc deberian definirse en un modulos laws
            o algebra o un nombre mejor?" (c167022)
Source:     record/answers-annotations-principles-2026-10-11-d.md
Kind:       libraries (03). For G2 (laws come first, stated once over the signature they need)
Status:     current; done 2026-10-11 (addff54)

D-2026-10-12-ab The reserved words. Keywords: `data`, `match`, `if`, `then`, `else`, `U` (his
                correction: the universe is a kernel former), and possibly `operator`. Everything
                else that can be Luthier is Luthier: `let`/`in` (blocks), `forget`, `provisional`, `gen` (removed), `extern`, `primitive`,
                `axiom`, `test`, `cite` and the contextual words of tests become names of core or
                of a library, with named arguments where they take options (`test` will be the
                function with the most parameters, so a positional or keyword syntax does not
                fit it). Keyword or not, the semantics of every construct is expressible in
                Luthier (L14). Modules are values. `extern` is an action, since it opens a file.
                Implicit arguments inferred from the expected type (bidirectional) are needed.
Author:     Luciano; the one-by-one analysis and the classification the model's (chat)
Quote:      "test justamente va a ser una de las funciones con mas parameterizaciones de modo que la
            alternativa, usar posicional, no es buena."
            "Yo creo que todo lo que pueda ser luthier debe ser luthier."
            "el extern es una accion no? porque abre un file"
            "necesitamos el tipo de implicitos creo."
            "If then else match data--> keywords"
            "operator -> podria ser keyword..."
            "Igual sean o no keyword, su semantica debiera ser expresable por luthier no?"
            "los modulos son valores."
            "U me parece que es keyword no?"
Source:     chat:4f7f0dc5:1508
            chat:4f7f0dc5:1508
            chat:4f7f0dc5:1508
            chat:4f7f0dc5:1508
            chat:4f7f0dc5:1508
            chat:4f7f0dc5:1508
            chat:4f7f0dc5:1508
            chat:4f7f0dc5:1508
            chat:4f7f0dc5:1591
Kind:       language (spec 2, 3, 10, 12; L14, L4, L11). For L14, P16
Status:     current; the question of extern and import as actions inside definitions (against
            L4.7) open, one question to him

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

D-2026-10-12-ak An *object* is a type with its equality: the base theory (a setoid, O2), whose laws
                (reflexive, symmetric, transitive, substitutive) the kernel guarantees for a
                structural `==` and the author states for an observational one. Three levels: a
                structure (a kernel type with no equality, a function over an infinite domain), an
                object (with its equality), a theory (an object with further laws). A concrete type
                has no law written by its author; the laws of its equality are the kernel's. Those
                laws are to be stated in `lib/kernel_laws.lut` (L14), not there yet.
Author:     the model, on his question; accepted by Luciano
Quote:      "pero la == estuctural no es una ley?"
            "Ok, aceptado."
Source:     chat:f15ae1b6:878
            chat:f15ae1b6:894
Kind:       terms (Terms of docs/principles.md; spec 3.S36, 4.S9; O2, L3). For L3, L14, O2
Status:     current; refines D-2026-10-12-z (object no longer "anything a name defines") and
            D-2026-10-12-aj. His remark: it follows category theory in some way

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

D-2026-10-12-am What certification asks of a library of costs, spec 6.S5: a preorder `≤` to compare
                with the cutoff, a least element `0` for what is exact, a greatest `⊤` for what
                fails and absorbs, a composition `⊕` along a path (associative, unit `0`, monotone
                in each argument), and `lift` from `Bool` (`true` to `0`, `false` to `⊤`); nothing
                that subtracts. Of the algebras of D-2026-10-12-p, max and the plain sum satisfy
                it; the averaged forms with 1/n are not associative, and a library that takes them
                needs another `⊕` along a path.
Author:     the model; accepted by Luciano
Quote:      "asi como esta bien"
Source:     chat:f15ae1b6:1139
Kind:       language (spec 6.S5; the interface of the library of costs, D-2026-10-12-al; O1). For
            P16 (the smallest interface is the cheapest to keep), L10.9
Status:     current; the interface the core depends on, so a library of costs can add to it and
            not change it

D-2026-10-12-h  The cutoff is a parameter of the demand: the minimal cutoff for an implementation
                to be considered. It is not a parameter of the certified-subtype constructor.
Author:     Luciano
Quote:      "I know a place for the cutoff, a minimal cutoff to consider an implementation, it is a
            parameter at the demand level."
Source:     record/recommendations-ia-principles-2026-10-12.md (e8d7db1), §4.3
Kind:       principles (L3, L6, L13). For P11 (every criterion is a parameter), G3 (the demand)
Status:     current; to apply in draft 11

D-2026-10-12-i  The grade of a sum of costs is parameterizable: the vector of grades (L6) or the
                weakest (L13), the demand's choice.
Author:     Luciano
Quote:      "thats parameterizable, both."
Source:     same, §4.4
Kind:       principles (L6, L13). For P11
Status:     current; the composition along a path stays the sum (plan decisions, D1)

D-2026-10-12-p  The algebra of costs is not open at large: two candidate models, min/max and
                1/n log-sum-exp with 1/n sum, the 1/n his addition.
Author:     Luciano
Quote:      "but G2 cost algebra is not that open, there are basically two models: min max vs 1/n
            logsumexp 1/n sum (the 1/n is my addition is it ok?ok)"
Source:     same, §2.4
Kind:       principles (G2, L6). For G2
Status:     current; which combination is parameterizable and which is forced by soundness is D1
            of the plan decisions

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

D-2026-10-12-y  His marks on the wave 1 decisions of the specification (D1 to D10 of
                record/plan-spec-2026-10-12-decisions.md): D1 a directory of chapters; D2, D3,
                D9, D10 as proposed; D4 resolved by the rule "do the thing that is easier to
                build from", which is the derived representation of the grades (domain and
                evidence cost, the five names a view); D6 kept reversible, the rounding
                correction proposed and parameterized, nothing about epsilon fixed; D7 inverted:
                `run` is strict from the start, no opt-out, and (the model's reading, not
                answered) a cone with a `provisional` extern is refused like an uncertified
                one; D8 accepted with a theory of libraries written in Luthier, which became L14.
Author:     Luciano; Claude for the reading of D7 on provisional externs
Quote:      "fist option"
            "ok"
            "yes"
            "I am not sure if this is a matter for the specification or for different libraries, I
            think it is something we will learn by doing."
            "so as a general rule, lets do the thing that it is easier to build from."
            "esta no puede ser una decision irreversible, todo lo que tenga que ver con epsilon lo
            iremos descubriendo along the way"
            "no, empecemos siendo estrictos, sino es un viva la pepa y no testeamos Luthier nunca."
            "si, confio en tu criterio"
Source:     luthier@a066adc:record/plan-spec-2026-10-12-decisions.md:21
            luthier@a066adc:record/plan-spec-2026-10-12-decisions.md:32
            luthier@a066adc:record/plan-spec-2026-10-12-decisions.md:41
            luthier@a066adc:record/plan-spec-2026-10-12-decisions.md:53
            luthier@a066adc:record/plan-spec-2026-10-12-decisions.md:54
            luthier@a066adc:record/plan-spec-2026-10-12-decisions.md:70
            luthier@a066adc:record/plan-spec-2026-10-12-decisions.md:77
            luthier@a066adc:record/plan-spec-2026-10-12-decisions.md:96
Kind:       document and principles (L10.6, O3: the opt-out of D-2026-10-11-n reversed in its
            opt-out part; the certificate's grades; the specification's layout). For P16, P11,
            W4 (strictness is the application paying for certification)
Status:     current; D-2026-10-11-n stands for certification by default and is reversed on the
            opt-out, which waits for a real case (O3); the "dale" the entry quoted at first
            is in no transcript of the day and was dropped (2026-10-12)

D-2026-10-13-aa Answers on the review of layers 0 and 1 (record/questions-for-luciano-2026-10-13-layers-0-1-review.md), all as recommended. Q1: the kernel
                gains `Let` (name, type, value, body; the name equal to its value inside the
                body), a block becomes nested `Let`s; reverses the kernel half of
                D-2026-10-13-x's Q2 (a block as a lambda applied), the surface unchanged. Q2:
                `Act` as in term.lth (`Declare`, `Define`, `Datum`), chapter 3 brought up to the
                files. Q3: a `data` with any constructor lacking a law of its role is rejected,
                the table of observers reported besides (4.R3, L2.7). Q4: version 0 keeps `U : U`,
                a known limit stated in chapter 3. Q5: a theory with a single model becomes a
                definition with laws only for what characterizes it (4.R10). Q6: `Law` stays
                Boolean until the cost library, when there is a use case. Q7: reduction unfolds a
                defined name in head position, "stays folded" retired from 3.S15, folding back for
                display is the printer's.
Author:     Luciano, on the sessions' recommendations
Quote:      "OK"
            "OK, lets wait for the Cost Library, when we have a use case."
Source:     luthier@3d8f912:record/questions-for-luciano-2026-10-13-layers-0-1-review.md:18
            luthier@3d8f912:record/questions-for-luciano-2026-10-13-layers-0-1-review.md:66
Kind:       spec (3.S15, 3.S29, 3.S36, 3, 4.R3, 4.R10, 5.S1) and term.lth, program.lth, laws.lth,
            checks.lth
Status:     current; Q1 reverses the kernel half of D-2026-10-13-x Q2

D-2026-10-13-ad After `v0.2`, execution before evidence, in part: first the world, the externs and
                `run` (spec 10, `world.lth`), minimal, so that sonolocalización runs uncertified,
                an extern validated at its first action by a minimal tester over `test.lth`; then
                evidence and certification, designed on its laws and on how they fail; then the
                demand and the planner (spec 8), which substitute only along certified equivalences
                (D-2026-10-11-m) and so need certificates. Reorders steps 5 and 6 of the plan from
                zero.
Author:     Luciano (execution first; his reason), the split of layer 3 the model's
Quote:      "Para diseñar los certificados primero tenemos que ver como falla."
Source:     chat:52b10bff:5037
Kind:       plan (steps 5 and 6 of record/plan/luthier-from-zero/), with S1 (D-2026-10-13-ac)
Status:     current

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

D-2026-10-13-l  A law is a theory: its predicate presents it, `forall` (Π) and `exists` (Σ) and the
                connectives form it, and its models are its evidence, which follows its form: a case
                is evaluated; a `forall` is modelled exhaustively, by listed cases or by a sample; an
                `exists` by a witness with its cost; `and` by a pair, `or` by one side; a citation or
                an assumption models any part whole. A `forall` is refuted exactly by a
                counterexample and over an infinite domain confirmed only by statistics; an `exists`
                is confirmed by a witness whose cost is determinate, not statistical, though over the
                reals not zero. `then` is material, `not (p and not q)`; conditioning is not a
                connective (Lewis, 1976) but an operation on a measure, with the chain rule.
Author:     Luciano for the question, `forall` and `exists`, the certifiers as models of the
            quantifier and citation of the whole law, and the inexact witness over the reals; the
            model for the rest
Quote:      "Las leyes a su vez son teorias o son  modelos?"
            "Tenes ambos el Forall y el Exist (para optimizacion o inversas por ejemplo)"
            "yo estoy tentado a pensar que el exhaustive y el sampled son modelos del Forall , el cite
            es modelo de toda la Ley."
            "Si, me cierra."
Source:     chat:f15ae1b6:2245
            chat:f15ae1b6:2273
            chat:f15ae1b6:2273
            chat:f15ae1b6:2311
Kind:       principles (L9.11, L9.12, L12.1) and spec (5, 6.S7). For L8.1, L9, G2
Status:     current; the clauses proposed in their wording

D-2026-10-13-z  An object's laws are reflexive, symmetric, transitive; substitutivity over every
                function is the structural equality's (`Structural` in kernel_laws.lth §1); an
                observational equality, such as alpha-equivalence of terms or doubles within a
                tolerance, is respected by the operations of its own theory, each stating it as a
                congruence (`AlphaCongruent` in term.lth). Refines D-2026-10-12-ak; 3.S36 and 5.S4.
                Q5 of record/questions-for-luciano-2026-10-13-layers-0-1.md, raised by the Codex
                writing kernel.py (`fn x { x }` and `fn y { y }` are alpha-equal, and a function
                reading the binder's name tells them apart).
Author:     Luciano, on the sessions' recommendation
Quote:      "si, que sea alfacongruente"
Source:     chat:52b10bff:4255
Kind:       spec (3.S36, 5.S4) and kernel_laws.lth, term.lth
Status:     current; refines D-2026-10-12-ak

D-2026-10-14-b  4.R3 stays read per file, and a data's constructors have their role laws in the
                file that defines the data, without repeating a law: core.lut claims the
                theories of kernel_laws.lth for its own data (the bindings of Unit, Bool, Maybe,
                List move from kernel_models.lut into core.lut), and the law that gives
                Coverage's constructors their roles moves from test.lth into laws.lth. No change
                to the spec's text of 4.R3 nor to check.py.
Author:     Luciano; the form (core claims its models) is the model's answer to his question
            "¿no se puede definir el rol en core?"
Quote:      "la verdad prefiero que las construcciones tengan su ley en su archivo. pero es peor
            repetir cosas. No se puede definir el rol en core, que seria lo correcto?"
Source:     luthier@c707f7c:record/plan/questions-2026-10-14.md:50
Kind:       theories (core.lut, kernel_models.lut, laws.lth, test.lth)
Status:     current

### `generators.lth`

````
-- generators.lth: generators as values, the generic ones over a type's form, sizes, subtypes,
-- censuses and budgets; and the generators of programs the checker's laws are tested on.
--
-- Draft 1, 2026-10-13, by Claude Fable 5.1 in the session (layer 2 of
-- record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md, step 5.1); draft 0 at
-- d9e1490 by Claude Opus 5.5, rewritten on the internal review of layers 2 and 3
-- (record/IA/opus-2026-10-13/review-layers-2-3-report.md, gen.1 to gen.16). Sources: spec 7.S1 to
-- 7.S8, 7.R1 to 7.R4, 7.S17, 7.S18; 7.S3's proposed sized rule for recursive `data`; program.lth's
-- `Violating` and `Clean` domains; L2.7; L5.18; L9.6; P10 (the invariant of a metric is what
-- represents it). Pattern of ebnf.lth: a theory, its laws over a model, `T := laws`.
--
-- What this file states. A generator of `T` is a value of `Gen T`: from a size and a seed, a
-- value and the next seed (7.S1). Its validity is its type: every value it gives belongs to `T`,
-- which for a subtype is the obligation of its predicate. What else a generator promises is a
-- theory each generator is a model of, and in each theory the operation the laws speak of is a
-- field, so that a wrong model is told apart (the review's gen.3: a theory whose operation is a
-- definition outside it has every value as a model); the definitions here are the reference
-- models, named in generators_model.lut. Types are not inspected here (7.R2), so what a size is,
-- one function per form of type (7.S3), is a parameter of the theories that use it. The functors
-- of 7.S3 over the forms of a type wait for core (gen.9).
--
-- Index. Status of each section: done, or todo with what it needs. A session or Codex continuing
-- this file takes the first todo, writes it in the pattern of the done ones, checks it with
-- `luthier parse src/luthier/lib/generators.lth`, sets its status to done here, and commits.
--
--   §1 Seeds and generators: `Seed`, `Gen T`, the unit interval; the random source and its
--      laws, uniform and independent (7.S1, 7.S17).                                         done
--   §2 Sampling by weight: the cumulative inversion as a field, proportional to the weight;
--      the metrics of numbers by their invariance (7.S2, 7.S4).                              done
--   §3 Exhaustive and sized generators, the size the type's (7.S3, 7.R3).                    done
--   §4 Subtypes and dependent records: a filter with its budget; components in order
--      (7.S6, 7.S7).                                                                        done
--   §5 Censuses, walked in turn (7.R4); bindings by parameter and by type (7.R1).             done
--   §6 Budgets, every one an argument (7.S8).                                               done
--   §7 The programs a rule of the checker is tested on (program.lth).                        done
--   §8 The functors over the forms of a type, with the core's instances (7.S3): waits for
--      core.lut.                                                                            todo

import "kernel_laws.lth" Concrete
import "laws.lth" Coverage Drawn

-- ---------------------------------------------------------------- §1 Seeds and generators

-- A seed is an integer in [0, 2^31) (7 §1); a generator of `T` gives, from a size and a seed, a
-- value of `T` and the next seed (7.S1). Its type is its validity: a generator of a subtype owes
-- the predicate of every value it gives, an obligation tested as an extern's is (spec 4).
Seed : U := { k : Int | 0 <= k and k < 2147483648 }
Gen (T : U) = Nat -> Seed -> T * Seed
-- the unit interval, drawn within its bounds with no rejection (7.S6); the laws below quantify
-- over it, not over a `Float64` with a guard (gen.14)
UnitInterval : U := { v : Float64 | 0.0 <= v and v < 1.0 }
OrderedUnitPair : U := { v w : Float64 | 0.0 <= v and v <= w and w < 1.0 }

-- The random source is an extern that gives seeds and uniform doubles (7.S1); its laws of
-- stochasticity are stated here and certified as any extern's. Each value is in [0, 1); a seed
-- moves on; the values are uniform, and successive values are independent (7.S1). The last two
-- are statistical laws (7.S17): each returns the p-value of the host's test (goodness of fit to
-- the uniform law; the pairs of successive draws uniform in the unit square), to be read against
-- the level the demand sets, and a failure is repeated once (7.S18). As Bool laws they hold on a
-- fraction `1 - alpha` of seeds, which is what their certificate says (gen.2); the level and the
-- count are parameters of the certification, `Level`.
Random : { next : Seed -> Seed, uniform : Seed -> Float64 }
uniformPValue : List Float64 -> Float64
serialPValue : List (Float64 * Float64) -> Float64
Level : U := { alpha : Float64, n : Nat | 0.0 < alpha and alpha < 1.0 and 0 < n }
draws (r : Random) (s : Seed) (n : Nat) : List Float64 :=
  if n == 0 then nil else cons (r.uniform s) (draws r (r.next s) (n - 1))
pairs (r : Random) (s : Seed) (n : Nat) : List (Float64 * Float64) :=
  if n == 0 then nil else cons ((r.uniform s, r.uniform (r.next s))) (pairs r (r.next (r.next s)) (n - 1))
UniformInUnit (r : Random) (s : Seed) : Bool := 0.0 <= r.uniform s and r.uniform s < 1.0
SeedMoves (r : Random) (s : Seed) : Bool := not (r.next s == s)
UniformAtLevel (r : Random) (l : Level) (s : Seed) : Bool := uniformPValue (draws r s l.n) >= l.alpha
IndependentAtLevel (r : Random) (l : Level) (s : Seed) : Bool := serialPValue (pairs r s l.n) >= l.alpha
Random := UniformInUnit & SeedMoves & UniformAtLevel & IndependentAtLevel

-- ---------------------------------------------------------------- §2 Sampling by weight

-- To draw from a support with weights, draw `u` uniform in [0, C), `C` the total weight, and give
-- the value at which the cumulative weight first exceeds `u` (7.S2). Weights are non-negative.
-- The reference `pick` gives the last value of positive weight when rounding leaves `u` beyond the
-- running sum (gen.1: in doubles the sum of the parts need not reach the total).
total (T : U) (ws : List (T * Float64)) : Float64 := match ws { nil -> 0.0 ; cons (x, w) rest -> w + total T rest }
pick (T : U) (ws : List (T * Float64)) (u : Float64) : Maybe T := match ws { nil -> nothing ;
  cons (x, w) rest -> if u < w then just x else (match pick T rest (u - w) { nothing -> (if 0.0 < w then just x else nothing) ; r -> r }) }

-- A support with weights and its inversion: `pick` is a field, so that the laws tell a model apart
-- (gen.3, gen.4). The laws: a value of weight zero is never drawn; a value is drawn exactly on a
-- part of [0, C) as wide as its weight, the one between the running sum before it and the running
-- sum through it (7.S2's proportionality); one value of positive weight always gives itself.
Support (T : Concrete) : { weights : List (T * Float64), pick : Float64 -> Maybe T }
weightOf (T : Concrete) (ws : List (T * Float64)) (x : T) : Float64 :=
  match ws { nil -> 0.0 ; cons (y, w) rest -> (if x == y then w else 0.0) + weightOf T rest x }
allNonNegative (T : Concrete) (ws : List (T * Float64)) : Bool :=
  match ws { nil -> true ; cons (x, w) rest -> 0.0 <= w and allNonNegative T rest }
-- the running sum before the first occurrence of `x`
before (T : Concrete) (ws : List (T * Float64)) (x : T) : Float64 :=
  match ws { nil -> 0.0 ; cons (y, w) rest -> if x == y then 0.0 else w + before T rest x }
occurs (T : Concrete) (ws : List (T * Float64)) (x : T) : Bool :=
  match ws { nil -> false ; cons (y, w) rest -> x == y or occurs T rest x }
NonNegative (T : Concrete) (s : Support T) : Bool := allNonNegative T s.weights
PickedHasWeight (T : Concrete) (s : Support T) (v : UnitInterval) : Bool :=
  match s.pick (total T s.weights * v) { nothing -> total T s.weights == 0.0 ; just x -> 0.0 < weightOf T s.weights x }
-- proportionality: `u` within `x`'s part gives `x`, stated on every value of the support
ProportionalToWeight (T : Concrete) (s : Support T) (x : T) (v : UnitInterval) : Bool :=
  not (occurs T s.weights x) or 0.0 == weightOf T s.weights x
  or s.pick (before T s.weights x + weightOf T s.weights x * v) == just x
Support (T : Concrete) := NonNegative T & PickedHasWeight T & ProportionalToWeight T

-- The metrics of numbers (7.S2, 7.S4): a metric places a uniform `u` in [0, 1) into an interval,
-- within its bounds and growing with `u`, from the lower bound at `u = 0`. What tells the two
-- apart is the invariance that represents each (P10, gen.5): `linear` commutes with translation,
-- for a quantity whose meaning does not change when shifted, and is defined on any interval;
-- `log` commutes with scaling, for a quantity that is a magnitude, and needs `0 < lo` (7.S4's
-- atom at 0 and the sign are the generator's, outside this theory). The models are in
-- generators_model.lut; `power` is core's (spec 11), declared until written.
power : Float64 -> Float64 -> Float64
Interval : U := { lo hi : Float64 | lo < hi }
PositiveInterval : U := { lo hi : Float64 | 0.0 < lo and lo < hi }
Metric : { place : Float64 -> Float64 -> Float64 -> Float64 }
WithinBounds (m : Metric) (i : PositiveInterval) (v : UnitInterval) : Bool :=
  i.lo <= m.place i.lo i.hi v and m.place i.lo i.hi v <= i.hi
Grows (m : Metric) (i : PositiveInterval) (p : OrderedUnitPair) : Bool := m.place i.lo i.hi p.v <= m.place i.lo i.hi p.w
StartsAtLo (m : Metric) (i : PositiveInterval) : Bool := m.place i.lo i.hi 0.0 == i.lo
Metric := WithinBounds & Grows & StartsAtLo
-- the linear metric: on any interval, and shifted with it
Translates (m : Metric) (i : Interval) (c : Float64) (v : UnitInterval) : Bool :=
  m.place (i.lo + c) (i.hi + c) v == m.place i.lo i.hi v + c
WithinAnyBounds (m : Metric) (i : Interval) (v : UnitInterval) : Bool :=
  i.lo <= m.place i.lo i.hi v and m.place i.lo i.hi v <= i.hi
LinearMetric : { metric : Metric }
LinearTranslates (l : LinearMetric) (i : Interval) (c : Float64) (v : UnitInterval) : Bool := Translates l.metric i c v
LinearWithinAny (l : LinearMetric) (i : Interval) (v : UnitInterval) : Bool := WithinAnyBounds l.metric i v
LinearMetric := LinearTranslates & LinearWithinAny
-- the log metric: scaled with its interval
Scales (m : Metric) (i : PositiveInterval) (k : Float64) (v : UnitInterval) : Bool :=
  not (0.0 < k) or m.place (k * i.lo) (k * i.hi) v == k * m.place i.lo i.hi v
LogMetric : { metric : Metric }
LogScales (l : LogMetric) (i : PositiveInterval) (k : Float64) (v : UnitInterval) : Bool := Scales l.metric i k v
LogMetric := LogScales

-- ---------------------------------------------------------------- §3 Exhaustive and sized generators

memberOf (T : Concrete) (x : T) (xs : List T) : Bool := match xs { nil -> false ; cons y rest -> x == y or memberOf T x rest }
allOf (T : U) (p : T -> Bool) (xs : List T) : Bool := match xs { nil -> true ; cons x rest -> p x and allOf T p rest }
firstOf (T : U) (r : T * Seed) : T := match r { (x, s) -> x }
noDuplicates (T : Concrete) (xs : List T) : Bool := match xs { nil -> true ; cons x rest -> not (memberOf T x rest) and noDuplicates T rest }
upTo (T : U) (size : T -> Nat) (n : Nat) (xs : List T) : List T :=
  match xs { nil -> nil ; cons x rest -> if size x <= n then cons x (upTo T size n rest) else upTo T size n rest }

-- An exhaustive generator lists every value of a finite type, once; its values up to a size are
-- those whose size is at most it (7.S3, 7.R3). The size is the type's, one function per form
-- (7.S3), so it is a parameter and not the model's choice (gen.7); a type with no finite list of
-- all its values has no model (gen.8: `exhaustive` over an unbounded type is an error, 7.R3).
-- Named `Enumeration`, apart from laws.lth's coverage `Exhaustive` (one name, two meanings; the
-- coordinator, 2026-10-14).
Enumeration (T : Concrete) (size : T -> Nat) : { all : List T }
ReachesEvery (T : Concrete) (size : T -> Nat) (e : Enumeration T size) (x : T) : Bool := memberOf T x e.all
EachOnce (T : Concrete) (size : T -> Nat) (e : Enumeration T size) : Bool := noDuplicates T e.all
Enumeration (T : Concrete) (size : T -> Nat) := ReachesEvery T size & EachOnce T size
values (T : Concrete) (size : T -> Nat) (e : Enumeration T size) (n : Nat) : List T := upTo T size n e.all

-- A sized generator keeps the size of what it gives within the size asked: for a recursive `data`
-- the size bounds the depth, so at size 0 only constructors with no recursive argument are drawn
-- (7.S3, proposed), and drawing ends.
Sized (T : U) (size : T -> Nat) : { gen : Gen T }
SizeBounded (T : U) (size : T -> Nat) (g : Sized T size) (n : Nat) (s : Seed) : Bool := size (firstOf T (g.gen n s)) <= n
Sized (T : U) (size : T -> Nat) := SizeBounded T size

-- ---------------------------------------------------------------- §4 Subtypes and dependent records

-- A subtype with an interval predicate is drawn within its bounds by a metric (§2), with no
-- rejection; with any other predicate, by its base's generator redrawn while the predicate fails,
-- up to a budget of tries, after which there is no value and the law is not run, with that reason
-- (7.S6, 7.S8, 7.S12). `draw` is the field; the laws relate it to the base (gen.3): what it gives
-- holds; it gives nothing only when none of the base's draws in the budget holds; and what it
-- gives is the first of them that holds. The reference is `filtered`.
filtered (T : U) (g : Gen T) (p : T -> Bool) (tries n : Nat) (s : Seed) : Maybe T * Seed :=
  if tries == 0 then (nothing, s) else match g n s { (x, s2) -> if p x then (just x, s2) else filtered T g p (tries - 1) n s2 }
Filter (T : U) : { base : Gen T, keep : T -> Bool, draw : Nat -> Nat -> Seed -> Maybe T * Seed }
firstKept (T : U) (g : Gen T) (p : T -> Bool) (tries n : Nat) (s : Seed) : Maybe T :=
  match filtered T g p tries n s { (m, s2) -> m }
DrawKeeps (T : U) (f : Filter T) (tries n : Nat) (s : Seed) : Bool :=
  match f.draw tries n s { (m, s2) -> match m { nothing -> true ; just x -> f.keep x } }
DrawIsTheFirstKept (T : U) (f : Filter T) (tries n : Nat) (s : Seed) : Bool :=
  match f.draw tries n s { (m, s2) -> m == firstKept T f.base f.keep tries n s }
Filter (T : U) := DrawKeeps T & DrawIsTheFirstKept T

-- The components of a dependent pair are drawn in order, the second with the first in its type
-- (7.S7); when the second's type is empty for a first, the first is drawn again, up to the
-- `redraws` budget (7.S8): that is the generator of a dependent subtype, a filter over the pair.
dependent (A : U) (B : A -> U) (ga : Gen A) (gb : (x : A) -> Gen (B x)) : Gen ((x : A) * B x) :=
  fn n s { match ga n s { (x, s2) -> match gb x n s2 { (y, s3) -> ((x, y), s3) } } }

-- ---------------------------------------------------------------- §5 Censuses and bindings

-- A function over an infinite domain, or a model of a theory, has no generic generator: a test
-- binds it to a census, an explicit list of the program's values of that type (7.R4), walked in
-- turn, each value once (7.S3's table; gen.10: a draw by weight repeats and misses, and could not
-- be graded as listed).
Census (T : U) = List T
lengthOf (T : U) (xs : List T) : Nat := match xs { nil -> 0 ; cons x rest -> 1 + lengthOf T rest }
nth (T : U) (xs : List T) (i : Nat) : Maybe T :=
  match xs { nil -> nothing ; cons x rest -> if i == 0 then just x else nth T rest (i - 1) }
nextSeed (s : Seed) : Seed := (s + 1) mod 2147483648
walk (T : U) (c : Census T) : Gen (Maybe T) :=
  fn n s { (if lengthOf T c == 0 then nothing else nth T c (s mod lengthOf T c), nextSeed s) }

-- A binding names the generator of a parameter, or of every parameter of a type, inline or through
-- a profile, with the coverage that generator gives (every value, a census, a draw); a parameter
-- binding wins over a type binding, and one in `where` over one in the profile (7.R1). The
-- resolution is a field (gen.3); the reference is `resolve`.
Binding = { parameter : Maybe String, type : Maybe String, generator : String, coverage : Coverage }
bindsParameter (x : String) (b : Binding) : Bool := b.parameter == just x
bindsType (t : String) (b : Binding) : Bool := b.parameter == nothing and b.type == just t
firstBinding (f : Binding -> Bool) (bs : List Binding) : Maybe Binding :=
  match bs { nil -> nothing ; cons b rest -> if f b then just b else firstBinding f rest }
resolve (whereBs profile : List Binding) (x t : String) : Maybe Binding :=
  match firstBinding (bindsParameter x) whereBs { just g -> just g ; nothing ->
  match firstBinding (bindsParameter x) profile { just g -> just g ; nothing ->
  match firstBinding (bindsType t) whereBs { just g -> just g ; nothing ->
  firstBinding (bindsType t) profile } } }
Resolution : { bindingOf : List Binding -> List Binding -> String -> String -> Maybe Binding }
byParameter (x g : String) : Binding := { parameter := just x, type := nothing, generator := g, coverage := Drawn 0 }
byType (t g : String) : Binding := { parameter := nothing, type := just t, generator := g, coverage := Drawn 0 }
generatorOf (b : Maybe Binding) : Maybe String := match b { nothing -> nothing ; just k -> just k.generator }
ParameterWins (r : Resolution) (whereBs profile : List Binding) (x t g h : String) : Bool :=
  generatorOf (r.bindingOf (cons (byParameter x g) whereBs) (cons (byType t h) profile) x t) == just g
WhereWins (r : Resolution) (profile : List Binding) (x t g h : String) : Bool :=
  generatorOf (r.bindingOf [byParameter x g] (cons (byParameter x h) profile) x t) == just g
TypeBindsEveryParameter (r : Resolution) (x t g : String) : Bool :=
  generatorOf (r.bindingOf nil [byType t g] x t) == just g
NothingBindsNothing (r : Resolution) (x t : String) : Bool := r.bindingOf nil nil x t == nothing
Resolution := ParameterWins & WhereWins & TypeBindsEveryParameter & NothingBindsNothing

-- ---------------------------------------------------------------- §6 Budgets

-- Every budget is an argument of the test, recorded in the entry (7.S8, L5.18): the tries per
-- value of a filter, the redraws of a dependent record, the probes of a law quantified inside a
-- type, the draws per evaluated case (a multiple of `n`), the product of finite parameters above
-- which a covering array chooses the cases (7.R3), the runs that estimate a level, the seeds per
-- control (7.S19), the draws that certify a generator's distribution (7.S1), and the total
-- probability of special values and of the atom at 0 of a `log` metric. The largest size is the
-- spec's (`TestSpec.size`, test.lth). The defaults are `test`'s.
positiveBudgets (tries redraws probes drawsPerCase coveringAbove levelRuns seedsPerControl distributionDraws : Nat) : Bool :=
  0 < tries and 0 < redraws and 0 < probes and 0 < drawsPerCase and 0 < coveringAbove
  and 0 < levelRuns and 0 < seedsPerControl and 0 < distributionDraws
budgetMasses (specialMass atomAtZero : Float64) : Bool :=
  0.0 <= specialMass and specialMass < 1.0 and 0.0 <= atomAtZero and atomAtZero < 1.0
Budgets : U := { tries redraws probes drawsPerCase coveringAbove levelRuns seedsPerControl distributionDraws : Nat,
                   specialMass atomAtZero : Float64 |
                   positiveBudgets tries redraws probes drawsPerCase coveringAbove levelRuns seedsPerControl distributionDraws
                     and budgetMasses specialMass atomAtZero }

-- ---------------------------------------------------------------- §7 The programs a rule is tested on

import "grammar.lth" SurfaceProgram
import "program.lth" Violating Clean

-- For each rule of the checker, the programs with a name that violates it and those with a name
-- that does not (program.lth: `ReportsViolations`, `ReportsNoFalseFailure`; review of layers 0-1,
-- B). At size 0 each generator walks its census, the programs of tests/spec/ for that rule, one per
-- seed in order, the next seed the next program (gen.11); at larger sizes it draws a well-formed
-- program from a small pool of names (act names, core's, imports) and changes it by one edit aimed
-- at the rule (a second `:=` of a name, a body at `U` that is no type, an `==` on a function, a
-- name nothing defines, a constructor no law mentions). What `violating` gives violates the rule
-- because its type says so: that is its obligation, tested as any generator's (7.S1).
RuleCases (v : SurfaceProgram -> String -> Bool) : {
  violating : Gen (Violating v),
  clean : Gen (Clean v),
  census : List (Violating v),
  cleanCensus : List (Clean v),
}
-- at size 0, seed `i` gives the census's `i`-th program, and the next seed is `i + 1`
CensusFirst (v : SurfaceProgram -> String -> Bool) (c : RuleCases v) (i : Seed) : Bool :=
  match nth (Violating v) c.census i { nothing -> true ;
    just w -> (match c.violating 0 i { (x, s) -> x.p == w.p and x.n == w.n and s == nextSeed i }) }
CleanCensusFirst (v : SurfaceProgram -> String -> Bool) (c : RuleCases v) (i : Seed) : Bool :=
  match nth (Clean v) c.cleanCensus i { nothing -> true ;
    just w -> (match c.clean 0 i { (x, s) -> x.p == w.p and x.n == w.n and s == nextSeed i }) }
RuleCases (v : SurfaceProgram -> String -> Bool) := CensusFirst v & CleanCensusFirst v
````

### `generators_model.lut`

````
-- generators_model.lut: the models of generators.lth.
--
-- Draft 1, 2026-10-13, by Claude Fable 5.1 in the session (layer 2; draft 0 at 8570a0d). The two
-- metrics of numbers (7.S2, 7.S4), the reference support, filter and resolution of bindings, from
-- the definitions of generators.lth; the core's instances of the forms of a type wait for core.
-- [proposed, 2026-10-15, record/IA/tester-2026-10-14/prompt-3.md] The families a test binds a
-- parameter to (7.R1, 7.S5), host generators with their routes and the law each must meet.

import "generators.lth" Metric LinearMetric LogMetric Support Filter Resolution Gen power pick resolve filtered Seed Level
import "kernel_laws.lth" Concrete

-- `linear`: uniform between the bounds, for a quantity whose meaning does not change when shifted
linear : Metric := { place := fn lo hi v { lo + v * (hi - lo) } }
linearMetric : LinearMetric := { metric := linear }
-- `log`: uniform in the logarithm, for a quantity whose meaning does not change when scaled
logarithmic : Metric := { place := fn lo hi v { lo * power (hi / lo) v } }
logMetric : LogMetric := { metric := logarithmic }

-- a support drawn by the reference inversion
supportOf (T : Concrete) (ws : List (T * Float64)) : Support T := { weights := ws, pick := fn u { pick T ws u } }
-- a filter drawn by the reference redraw
filterOf (T : U) (g : Gen T) (p : T -> Bool) : Filter T :=
  { base := g, keep := p, draw := fn tries n s { filtered T g p tries n s } }
-- the reference resolution of bindings
resolution : Resolution := { bindingOf := resolve }

-- ---------------------------------------------------------------- the families a test binds (7.S5)

-- [proposed, 2026-10-15, record/IA/tester-2026-10-14/prompt-3.md] Generators a `where` or profile
-- binding names (7.R1), host code in src/luthier/generators.py (P7). Each is a value of `Gen T`,
-- or a family `(k : Dim) -> Gen T` whose parameters are named after the law's earlier parameters
-- they read (7.S7: `dependent`'s `gb`); the seed crosses as an `Int` and the next one comes back
-- with the value (7.S1). The criteria of a family (an atom's probability, a magnitude's bounds)
-- are its arguments, set here (P11). Each comes with the law its values must meet, quantified
-- over the size and the seed; the type a generator gives is its validity, which the tester also
-- checks on every value it draws (7.S1).
import "arrays.lth" Vec Mat Dim MatOf Symmetric SymmetricOf ClearDiagonal RankFloor approxMat exact
  transposeDef matMulDef mscaleDef identity forallBelow
import "numbers.lth" Tolerance abs
import "probability.lth" UnitList allUnit UniformAtLevel
import "probability_model.lut" numpySort
import "arrays_model.lut" numpy : Arrays

-- The host's families as one record, as a model file holds its externs (12.S23): check.py's 4.R5
-- reads a standalone extern's type against the file's own definitions only, and refuses one
-- over an imported type (`Symmetric`); a record's fields are typed by the record's type.
hostGenerators : {
  symmetric : Gen Symmetric,
  symmetricOf : (k : Dim) -> Gen (SymmetricOf k),
  gram : Gen Symmetric,
  orthogonal : (k : Dim) -> Gen (MatOf k k),
  unitListWith : Float64 -> Gen UnitList,
  uniformSample : Gen UnitList,
  clearDiagonalWith : Float64 -> Float64 -> Float64 -> Gen ClearDiagonal,
} := {
  symmetric := extern "python:luthier.generators.symmetric",
  symmetricOf := extern "python:luthier.generators.symmetric_of",
  gram := extern "python:luthier.generators.gram",
  orthogonal := extern "python:luthier.generators.orthogonal",
  unitListWith := extern "python:luthier.generators.unit_list",
  uniformSample := extern "python:luthier.generators.uniform_sample",
  clearDiagonalWith := extern "python:luthier.generators.clear_diagonal",
}
-- symmetric matrices, v0.1's B + B^T (arrays.py's gen_symmetric), of a size between 1 and the
-- size, entries in [-size, size]; and of k rows
symmetric : Gen Symmetric := hostGenerators.symmetric
symmetricOf (k : Dim) : Gen (SymmetricOf k) := hostGenerators.symmetricOf k
-- positive semidefinite: B^T B with B of fewer rows than columns in most draws (rank deficient)
gram : Gen Symmetric := hostGenerators.gram
-- orthogonal, Haar: the QR of a Gaussian matrix with the signs of R's diagonal (7.S5, Mezzadri)
orthogonal (k : Dim) : Gen (MatOf k k) := hostGenerators.orthogonal k
-- lists of vectors of values in [0, 1], an entry an atom (0, 1 or a tie) with probability 0.2
-- (as lambdas: run.py's Runner leaves a constant that is a partial application of an extern stuck
-- when applied to the remaining arguments)
unitList : Gen UnitList := fn size seed { hostGenerators.unitListWith 0.2 size seed }
-- a calibrated sample: every value independent and uniform in [0, 1) (7.S17)
uniformSample : Gen UnitList := hostGenerators.uniformSample
-- a diagonal clear of the floor: an atom at 0 of probability 0.25, else a sign and a magnitude
-- log-uniform in [1, 1000], ClearDiagonal's bounds (7.S4)
clearDiagonal : Gen ClearDiagonal := fn size seed { hostGenerators.clearDiagonalWith 0.25 1.0 1000.0 size seed }

symmetricGives (a : Mat Float64) : Bool := a.m == a.n and approxMat exact a (transposeDef a)
SymmetricGivesSymmetric (size : Nat) (seed : Seed) : Bool := match symmetric size seed { (a, next) -> symmetricGives a }
SymmetricOfGivesItsSize (k : Dim) (size : Nat) (seed : Seed) : Bool :=
  match symmetricOf k size seed { (a, next) -> a.m == k and symmetricGives a }
-- positive semidefinite at a floor as arrays.lth's `PsdAt` reads it: nothing retained of `-a`
GramGivesPsd (fl : RankFloor) (size : Nat) (seed : Seed) : Bool :=
  match gram size seed { (a, next) -> symmetricGives a and numpy.retainedRank fl (mscaleDef (0.0 - 1.0) a) == 0 }
-- `transpose q * q == identity` within a tolerance, the demand's (P11)
OrthogonalGivesOrthogonal (tol : Tolerance) (k : Dim) (size : Nat) (seed : Seed) : Bool :=
  match orthogonal k size seed { (q, next) -> q.m == k and q.n == k and approxMat tol (matMulDef (transposeDef q) q) (identity k) }
UnitListGivesUnitValues (size : Nat) (seed : Seed) : Bool := match unitList size seed { (vs, next) -> allUnit vs }
-- calibrated: uniform at the level (probability.lth's `UniformAtLevel` on numpy's sort), a law that
-- holds on a fraction 1 - alpha of seeds (7.S17)
UniformSampleIsUniform (l : Level) (size : Nat) (seed : Seed) : Bool :=
  match uniformSample size seed { (vs, next) -> UniformAtLevel numpySort l vs }
ClearDiagonalGivesClear (size : Nat) (seed : Seed) : Bool :=
  match clearDiagonal size seed { (d, next) ->
    forallBelow d.n (fn k { d.f k == 0.0 or (1.0 <= abs (d.f k) and abs (d.f k) <= 1000.0) }) }
````

### `test.lth`

````
-- test.lth: a test as data, what running it gives, and the grade of what it gives.
--
-- Draft 1, 2026-10-13, by Claude Fable 5.1 in the session (layer 2 of
-- record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md, step 5.1); draft 0 at
-- 163eca2 by Claude Opus 5.5, rewritten on the internal review of layers 2 and 3
-- (record/IA/opus-2026-10-13/review-layers-2-3-report.md, test.1 to test.7). Sources: spec 7.S20
-- (`test` is a function with named arguments), 7.R1 (a test names its generators; a census is a
-- binding, not a mode), 7.S8 (budgets), 7.S9 (an entry's identity includes its binding), 7.S10
-- (grades; the weakest summarizes), 7.S12 (`n` counts evaluated cases; an entry is accepted only
-- when they reach `n`), 7.S13; L10.9 (no operation raises a grade without new evidence); L9.12; D9
-- of record/plan/archive/plan-implementation-2026-10-13-decisions.md (top-level `test` lines are
-- data, `test "x.lut"` the action); laws.lth; generators.lth. Pattern of ebnf.lth.
--
-- What this file states. `test` builds a `TestSpec`, a value the module keeps (D9): what law to
-- test, under which mode (every value, or a sample with its metric), how many cases, at what
-- size, from which seed, with which bindings and budgets. Running it is an action, the module's
-- `test "x.lut"` or `luthier test`; a model of `Tester` runs a spec and gives the evidence of
-- laws.lth: the points of the law's domain with their evidence and the coverage the run reached,
-- which is the weakest of the mode's and of each binding's (7.S10), or `NotRun` with its reason
-- when a budget gave nothing (7.S12). The grade is read from the verdict and the coverage, and
-- the grades are ordered, so that "the weakest" means something (test.5); the order of the
-- coverages themselves is laws.lth's since D-2026-10-14-b.
--
-- Index (all sections written in this draft):
--   §1 The spec: modes, `TestSpec`, `test` with its defaults (7.S20, 7.R1, 7.S8).            done
--   §2 Running: the evidence a run gives, its coverage the weakest reached, its count the
--      cases asked or not run (7.S10, 7.S12, 7.S13).                                        done
--   §3 Grades: read from the verdict and the coverage, ordered (7.S10, L10.2).              done

import "generators.lth" Seed Binding Budgets Metric
import "laws.lth" Evidence Points At NotRun Coverage Exhaustive Bounded Listed Drawn Verdict Confirmed Refuted
  Supported Unsettled Cites Assumes rankOf weaker

-- ---------------------------------------------------------------- §1 The spec

-- How the cases of a test are chosen (7.R1): every value of the parameters' types, or a sample
-- with a metric; a census is a binding of a parameter, not a mode. Roles: `CoverageIsTheWeakest`.
Mode : U := data {
  ExhaustiveMode : Mode ;
  SampledMode : Metric -> Mode ;
}

-- what to test and how (D9: a value the module keeps): the law, the mode, the cases asked, the
-- largest size, the seed, the bindings in `where` and the profile's, the budgets (7.S8, 7.S9)
TestSpec = { law : String, mode : Mode, cases : Nat, size : Nat, seed : Seed,
             whereBindings : List Binding, profile : List Binding, budgets : Budgets }

-- `test`: every option a named argument with a default (7.S20). The defaults of the budgets that
-- today's code holds (the tries of a filter, the redraws, the probes) are those numbers, named
-- here as defaults and not as constants (7.S8, L5.18); the rest are proposed.
defaultBudgets : Budgets := { tries := 2000, redraws := 50, probes := 5, drawsPerCase := 10, coveringAbove := 20000,
                              levelRuns := 10, seedsPerControl := 5, distributionDraws := 10000,
                              specialMass := 0.05, atomAtZero := 0.01 }
test (law : String) (mode : Mode) (cases : Nat <- 100) (size : Nat <- 10)
     (seed : Seed <- 0) (whereBindings : List Binding <- nil) (profile : List Binding <- nil)
     (budgets : Budgets <- defaultBudgets) : TestSpec :=
  { law := law, mode := mode, cases := cases, size := size, seed := seed, whereBindings := whereBindings,
    profile := profile, budgets := budgets }

-- ---------------------------------------------------------------- §2 Running

-- A tester runs a spec and gives the evidence of the law it names (laws.lth): points of the law's
-- domain with their evidence and the coverage reached, or `NotRun` with the reason. It is the
-- action `test "x.lut"` (D9); deterministic given the code, the binding, the seed and `n`, so a
-- known outcome is not recomputed (7.S13), which is the store's and not a law here.
Tester : { run : TestSpec -> Evidence }

coverageOf (e : Evidence) : Maybe Coverage := match e { Points A pts c -> just c ; _ -> nothing }
pointCount (e : Evidence) : Nat := match e { Points A pts c -> countPoints A pts ; _ -> 0 }
countPoints (A : U) (pts : List (A * Evidence)) : Nat := match pts { nil -> 0 ; cons x rest -> 1 + countPoints A rest }
isNotRun (e : Evidence) : Bool := match e { NotRun r -> true ; _ -> false }
-- the coverages in order of strength, `rankOf` and `weaker`, are laws.lth's, which defines
-- `Coverage` (7.S10; D-2026-10-14-b): read here, not repeated
modeCoverage (m : Mode) (size : Nat) (s : Seed) : Coverage := match m {
  ExhaustiveMode -> Bounded size ; SampledMode k -> Drawn s }
bindingsCoverage (bs : List Binding) (c : Coverage) : Coverage :=
  match bs { nil -> c ; cons b rest -> bindingsCoverage rest (weaker b.coverage c) }
-- the coverage a spec reaches: the mode's, exhaustive up to the size, weakened by every binding
-- (7.S10: the entry lists the reach of each parameter, and the grade is summarized by the weakest)
specCoverage (s : TestSpec) : Coverage :=
  bindingsCoverage s.profile (bindingsCoverage s.whereBindings (modeCoverage s.mode s.size s.seed))
-- and when the types are finite and enumerated whole, which the tester knows and this theory does
-- not (tester.py refuses an infinite type under `ExhaustiveMode`, 7.R3), the whole type, weakened
-- by the bindings likewise
wholeCoverage (s : TestSpec) : Coverage :=
  bindingsCoverage s.profile (bindingsCoverage s.whereBindings Exhaustive)

-- a run is points of the law, or not run with a reason (test.1)
RunIsPointsOrNotRun (t : Tester) (s : TestSpec) : Bool :=
  match t.run s { Points A pts c -> true ; NotRun r -> true ; _ -> false }
-- the coverage of a sampled run is at most the spec's; an exhaustive run's is the spec's, bounded
-- by the size, or the whole type's, both weakened by the bindings (the coordinator, 2026-10-14:
-- the law asked `Bounded size` where tester.py and laws.lth's `ForallOnPoints` give `Exhaustive`)
CoverageIsTheWeakest (t : Tester) (s : TestSpec) : Bool :=
  match coverageOf (t.run s) { nothing -> true ;
    just c -> match s.mode { ExhaustiveMode -> c == specCoverage s or c == wholeCoverage s ;
                             _ -> rankOf c <= rankOf (specCoverage s) } }
-- a sampled run that ran has exactly the cases asked, counting the cases evaluated (7.S12); fewer
-- is not run, with the reason (test.2: an empty sample is no evidence)
CountsCases (t : Tester) (s : TestSpec) : Bool :=
  match s.mode { SampledMode k -> isNotRun (t.run s) or pointCount (t.run s) == s.cases ; _ -> true }
Tester := RunIsPointsOrNotRun & CoverageIsTheWeakest & CountsCases

-- ---------------------------------------------------------------- §3 Grades

-- The grades of Terms (7.S10): proved, exhaustive, cases, sampled, assumed. A run's grade is read
-- from its verdict and its coverage: a confirmation over all of a finite type is exhaustive, so is
-- one bounded on the box the domain names (7.S10), one over a census is cases, a draw is sampled;
-- a witness is cases whatever the coverage (L9.12: its cost is determinate, test.4); a citation
-- stands as proved (its source's proof, spec 6), an assumption is assumed; a refutation or nothing
-- settled has no grade. The grades are ordered by the evidence cost they carry (L10.2: none for
-- proved and exhaustive on their domain, none on the cases listed and everything outside, finite
-- for sampled, an assumption's price for assumed), so that the weakest of several is defined and
-- no operation raises a grade without new evidence (L10.9).
Grade : U := data {
  Proved : Grade ;
  ExhaustiveGrade : Grade ;
  Cases : Grade ;
  Sampled : Grade ;
  AssumedGrade : Grade ;
}
gradeRank (g : Grade) : Nat := match g { Proved -> 4 ; ExhaustiveGrade -> 3 ; Cases -> 2 ; Sampled -> 1 ; AssumedGrade -> 0 }
weakest (g h : Grade) : Grade := if gradeRank g <= gradeRank h then g else h
grade (v : Verdict) (c : Maybe Coverage) : Maybe Grade := match v {
  Confirmed -> (match c { just k -> (match k { Exhaustive -> just ExhaustiveGrade ; Bounded n -> just ExhaustiveGrade ;
                                               Listed -> just Cases ; Drawn s -> just Cases }) ;
                          nothing -> just Cases }) ;
  Supported -> (match c { just k -> (match k { Bounded n -> just ExhaustiveGrade ; Drawn s -> just Sampled ; _ -> just Cases }) ;
                          nothing -> just Cases }) ;
  Cites r -> just Proved ;
  Assumes -> just AssumedGrade ;
  _ -> nothing }
-- the roles of the grades: each is the grade of the evidence it names, and the order is total,
-- with proved above exhaustive above cases above sampled above assumed
Grading : { gradeOf : Verdict -> Maybe Coverage -> Maybe Grade, below : Grade -> Grade -> Bool }
GradesAsTerms (g : Grading) (s n : Nat) (r : String) : Bool :=
  g.gradeOf Confirmed (just Exhaustive) == just ExhaustiveGrade and g.gradeOf Supported (just (Bounded n)) == just ExhaustiveGrade
  and g.gradeOf Supported (just Listed) == just Cases and g.gradeOf Supported (just (Drawn s)) == just Sampled
  and g.gradeOf Confirmed (just (Drawn s)) == just Cases and g.gradeOf (Cites r) nothing == just Proved
  and g.gradeOf Assumes nothing == just AssumedGrade and g.gradeOf Refuted (just Exhaustive) == nothing
  and g.gradeOf Unsettled (just (Drawn s)) == nothing
GradesAreOrdered (g : Grading) (x y : Grade) : Bool := g.below x y == (gradeRank x < gradeRank y)
Grading := GradesAsTerms & GradesAreOrdered
````

### `test_model.lut`

````
-- test_model.lut: the grading of test.lth, by its reference definition.
--
-- Draft 0, 2026-10-13, by Claude Fable 5.1 in the session (layer 2; test.6 of the review). The
-- tester itself is the certifier's action (spec 6, 7), written with it.

import "test.lth" Grading grade gradeRank

grading : Grading := { gradeOf := grade, below := fn x y { gradeRank x < gradeRank y } }
````

### `laws.lth`

````
-- laws.lth: what a law's value must give, the laws of relations, and a law as a theory.
--
-- Draft 0, 2026-10-13, by Claude Opus 5.5 in the session (step 3.2 of
-- record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md). Sources: spec 5.S1 to 5.S8 (a law has a
-- verdict; `lift` and `exact`; how laws combine; no cutoff); D-2026-10-11-l (the laws of relations
-- live here); D-2026-10-13-l (a law is a theory: `forall`, `exists`, the connectives, and evidence
-- that follows the form); 6.S5 (the cost algebra, whose six laws are certification.lth's, step 5);
-- L2.7. Pattern of ebnf.lth.
--
-- Index. Status of each section: done, or todo with what it needs. A session or Codex continuing
-- this file takes the first todo, writes it in the pattern of the done ones, checks it with
-- `luthier parse src/luthier/lib/laws.lth`, sets its status to done here, and commits.
--
--   §1 The verdict: `lift`, `exact`, and the verdicts as definitions, what the core asks
--      of a law's value (5.S2, 5.S3, 5.S5; D-2026-10-13-aa Q5).                                                       done
--   §2 The laws of relations and operations, as templates a theory applies
--      (D-2026-10-11-l).                                                              done
--   §3 A law as a theory: its forms (`forall`, `exists`, and, or, then, a case) and
--      its evidence, with what each kind of evidence settles (D-2026-10-13-l); the
--      coverages in order (7.S10; D-2026-10-14-b, from test.lth).                   done

import "checks.lth" Failures isEmpty

-- ---------------------------------------------------------------- §1 The verdict

-- A cost `C` (5.S2, 6.S5) with what a verdict needs of it: `zero`, holding exactly; `top`, failing;
-- and its order. The algebra of costs, with its six laws, is certification.lth's (step 5); here
-- only the two laws the retraction needs (5.S5): `zero <= zero`, and `top <= zero` false, so a
-- library cannot take `zero = top`.
CostScale (C : U) : { zero : C, top : C, leq : C -> C -> Bool }
ZeroIsExact (C : U) (s : CostScale C) : Bool := s.leq s.zero s.zero
TopIsNotExact (C : U) (s : CostScale C) : Bool := not (s.leq s.top s.zero)
CostScale (C : U) := ZeroIsExact C & TopIsNotExact C & VerdictsAreExact C

-- `lift` reads a Boolean law as a cost, `exact` reads a cost back as whether it holds exactly
-- (5.S5); `exact (lift b) == b` follows from the two laws above
lift (C : U) (s : CostScale C) (b : Bool) : C := if b then s.zero else s.top
exact (C : U) (s : CostScale C) (c : C) : Bool := s.leq c s.zero

-- What the core asks of a law's value (5.S3): a verdict in `C`. For `Bool` it is `lift`; for `C`
-- the identity; for a check, `lift` of whether it holds (5.S9). These are definitions, not a
-- theory with one model whose laws would restate them (D-2026-10-13-aa, Q5; 4.R10). A law into a
-- type with none of these verdicts is not a law: that is the checker's (4.R6, program.lth).
verdictOfBool (C : U) (s : CostScale C) (b : Bool) : C := lift C s b
verdictOfCost (C : U) (s : CostScale C) (c : C) : C := c
verdictOfCheck (C : U) (s : CostScale C) (E : U) (fs : Failures E) : C := lift C s (isEmpty E fs)

-- What characterizes a verdict is its retraction: reading it back as whether it holds exactly
-- gives what the law said (5.S5). Claimed by `CostScale`, whose two laws make it hold.
VerdictsAreExact (C : U) (s : CostScale C) (b : Bool) (E : U) (fs : Failures E) : Bool :=
  exact C s (verdictOfBool C s b) == b and exact C s (verdictOfCheck C s E fs) == isEmpty E fs

-- ---------------------------------------------------------------- §2 The laws of relations

-- Templates a theory applies to its own relation or operation (D-2026-10-11-l): definitions the
-- laws of a theory are written with, not laws on their own, so a theory that claims them gives
-- them their subject (4.S14). The relation `r` and the operation `op` are the theory's; equality
-- is the structural `==` (4.R8) or the theory's own `eq`, passed as `same`.
isReflexive (A : U) (r : A -> A -> Bool) (x : A) : Bool := r x x
isSymmetric (A : U) (r : A -> A -> Bool) (x y : A) : Bool := not (r x y) or r y x
isAntisymmetric (A : U) (same r : A -> A -> Bool) (x y : A) : Bool := not (r x y and r y x) or same x y
isTransitive (A : U) (r : A -> A -> Bool) (x y z : A) : Bool := not (r x y and r y z) or r x z
isTotal (A : U) (r : A -> A -> Bool) (x y : A) : Bool := r x y or r y x
isAssociative (A : U) (same : A -> A -> Bool) (op : A -> A -> A) (x y z : A) : Bool := same (op (op x y) z) (op x (op y z))
isCommutative (A : U) (same : A -> A -> Bool) (op : A -> A -> A) (x y : A) : Bool := same (op x y) (op y x)
isLeftIdentity (A : U) (same : A -> A -> Bool) (op : A -> A -> A) (e x : A) : Bool := same (op e x) x
isRightIdentity (A : U) (same : A -> A -> Bool) (op : A -> A -> A) (e x : A) : Bool := same (op x e) x
isInverse (A : U) (same : A -> A -> Bool) (op : A -> A -> A) (inv : A -> A) (e x : A) : Bool :=
  same (op x (inv x)) e and same (op (inv x) x) e
isDistributive (A : U) (same : A -> A -> Bool) (times plus : A -> A -> A) (x y z : A) : Bool :=
  same (times x (plus y z)) (plus (times x y) (times x z))
isHomomorphism (A B : U) (same : B -> B -> Bool) (f : A -> B) (opA : A -> A -> A) (opB : B -> B -> B) (x y : A) : Bool :=
  same (f (opA x y)) (opB (f x) (f y))
-- The implications above (symmetric, antisymmetric, transitive) are written as alternatives:
-- sampled at random, their premises rarely hold (7.S12), so a theory quantifies them over the
-- pairs its relation relates, as kernel_laws.lth §1 does for equality.

-- ---------------------------------------------------------------- §3 A law as a theory

-- The forms of a law (D-2026-10-13-l): a case, a `forall` (Π) and an `exists` (Σ) over a type, and
-- the connectives; `then` is material, `not (p and not q)`, so `Not` is a form and `Then` is
-- stated by it (conditioning is an operation on a measure, not a connective). This is the type
-- `Law` of what a test runs (5.S1, 3.S12); it is Boolean until the cost library (D-2026-10-13-aa,
-- Q6), when a case valued in `C` joins it. In `U` with constructors over `U`: version 0 keeps
-- `U : U` (3.S8).
Law : U := data {
  Case : Bool -> Law ;
  Forall : (A : U) -> (A -> Law) -> Law ;
  Exists : (A : U) -> (A -> Law) -> Law ;
  Both : Law -> Law -> Law ;
  Either : Law -> Law -> Law ;
  Not : Law -> Law ;
  Then : Law -> Law -> Law ;
}

-- How much of a type the cases of a `forall` cover: all of it; all of it up to a size, the box
-- the domain names (7.S10: bounded is exhaustive on that box, and on the whole type a support);
-- a census chosen by hand; or a draw from a seed (7.R1, 7.S8). Roles: `ForallOnPoints` and
-- `ExistsOnPoints` (only the exhaustive coverage confirms a `forall` or refutes an `exists`), and
-- `CoveragesAreOrdered`, the order of the four by strength, from which the weakest of several is
-- read (7.S10; D-2026-10-14-b: a data's constructors have their roles in the file that defines
-- it, so the order moved here from test.lth, which reads it). The grade each coverage gives is
-- test.lth's (`GradesAsTerms`).
Coverage : U := data {
  Exhaustive : Coverage ;
  Bounded : Nat -> Coverage ;
  Listed : Coverage ;
  Drawn : Nat -> Coverage ;
}

-- The coverages in order of strength (7.S10: an entry's grade is summarized by the weakest of the
-- reaches of its parameters): exhaustive above bounded above listed above drawn. `rankOf` is the
-- reference order and `weaker` the weakest of two, which test.lth reads to give a run the weakest
-- of its mode's and its bindings'. A model of `Covering` ranks coverages; the law is the chain of
-- the four, stated by the constructors, whatever a bound's size or a draw's seed.
rankOf (c : Coverage) : Nat := match c { Exhaustive -> 3 ; Bounded n -> 2 ; Listed -> 1 ; Drawn s -> 0 }
weaker (c d : Coverage) : Coverage := if rankOf c <= rankOf d then c else d
Covering : { rank : Coverage -> Nat }
CoveragesAreOrdered (k : Covering) (n s : Nat) : Bool :=
  k.rank (Drawn s) < k.rank Listed and k.rank Listed < k.rank (Bounded n) and k.rank (Bounded n) < k.rank Exhaustive
Covering := CoveragesAreOrdered

-- Evidence follows the form of the law (D-2026-10-13-l): a case evaluated, with the value the
-- evaluation gave; a value of the quantified type with the evidence for the law at it (a witness
-- of an `exists`, a counterexample to a `forall`); points of the type with their evidence and how
-- much they cover; a pair for `and`; one side for `or`; a citation or an assumption, which models
-- any law whole; a run that gave no case, with its reason (a budget spent, a generator that could
-- not draw; 7.S12), which settles nothing.
Evidence : U := data {
  Evaluated : Bool -> Evidence ;
  At : (A : U) -> A -> Evidence -> Evidence ;
  Points : (A : U) -> List (A * Evidence) -> Coverage -> Evidence ;
  Pair : Evidence -> Evidence -> Evidence ;
  Side : Bool -> Evidence -> Evidence ;
  Cited : String -> Evidence ;
  Assumed : Evidence ;
  NotRun : String -> Evidence ;
}

-- What evidence settles: confirmed, refuted, supported (by a census or a sample, never confirmed),
-- unsettled, or taken on a citation or on an assumption. Roles: the laws of `Settling`.
Verdict : U := data {
  Confirmed : Verdict ;
  Refuted : Verdict ;
  Supported : Verdict ;
  Unsettled : Verdict ;
  Cites : String -> Verdict ;
  Assumes : Verdict ;
}

-- A model says what evidence settles, and how the verdicts of the parts of a conjunction combine:
-- that combination is the demand's (5.S8: the vector of grades or the weakest), so it is the
-- model's, held to the laws every combination keeps. The certifier of spec 6 and 7 is a model.
Settling : {
  settles : Law -> Evidence -> Verdict,
  combine : Verdict -> Verdict -> Verdict,
}

isRefuted (v : Verdict) : Bool := match v { Refuted -> true ; _ -> false }
isConfirmed (v : Verdict) : Bool := match v { Confirmed -> true ; _ -> false }
allConfirmed (vs : List Verdict) : Bool := match vs { nil -> true ; cons v rest -> isConfirmed v and allConfirmed rest }
anyRefuted (vs : List Verdict) : Bool := match vs { nil -> false ; cons v rest -> isRefuted v or anyRefuted rest }
anyConfirmed (vs : List Verdict) : Bool := match vs { nil -> false ; cons v rest -> isConfirmed v or anyConfirmed rest }
-- the verdicts of the law at each point
pointVerdicts (m : Settling) (A : U) (p : A -> Law) (pts : List (A * Evidence)) : List Verdict :=
  match pts { nil -> nil ; cons (a, e) rest -> cons (m.settles (p a) e) (pointVerdicts m A p rest) }
-- an `exists` on points: confirmed by any witness; refuted only when the points are all of the type
-- and each refutes
existsVerdict (vs : List Verdict) (c : Coverage) : Verdict :=
  if anyConfirmed vs then Confirmed
  else match c { Exhaustive -> (if allRefutedOf vs then Refuted else Unsettled) ; _ -> Unsettled }
allRefutedOf (vs : List Verdict) : Bool := match vs { nil -> true ; cons v rest -> isRefuted v and allRefutedOf rest }
flip (v : Verdict) : Verdict := match v { Confirmed -> Refuted ; Refuted -> Confirmed ; _ -> Unsettled }

-- a case is settled by evaluating it, and evidence that does not agree with the case settles
-- nothing (it cannot lie; review of layers 0-1, C)
CaseIsEvaluated (m : Settling) (c b : Bool) : Bool :=
  m.settles (Case c) (Evaluated b) == (if not (b == c) then Unsettled else if c then Confirmed else Refuted)
-- a `forall` is refuted exactly by a counterexample: evidence at one point refutes it when it
-- refutes the law there, and otherwise settles nothing
ForallAtOnePoint (m : Settling) (A : U) (p : A -> Law) (a : A) (e : Evidence) : Bool :=
  m.settles (Forall A p) (At A a e) == (if isRefuted (m.settles (p a) e) then Refuted else Unsettled)
-- a `forall` on points: refuted by any counterexample; confirmed only when the points are all of
-- the type and each confirms; supported when a census or a sample confirms at every point. Written
-- out in the law, not through a helper, since it is the role of `Supported` (4.R3, L2.7: a law
-- depends on the names in its body, 4.S15)
ForallOnPoints (m : Settling) (A : U) (p : A -> Law) (pts : List (A * Evidence)) (c : Coverage) : Bool :=
  m.settles (Forall A p) (Points A pts c)
    == (if anyRefuted (pointVerdicts m A p pts) then Refuted
        else if allConfirmed (pointVerdicts m A p pts) then (match c { Exhaustive -> Confirmed ; _ -> Supported })
        else Unsettled)
-- an `exists` is confirmed by a witness, and a failing instance does not refute it
ExistsAtOnePoint (m : Settling) (A : U) (p : A -> Law) (a : A) (e : Evidence) : Bool :=
  m.settles (Exists A p) (At A a e) == (if isConfirmed (m.settles (p a) e) then Confirmed else Unsettled)
ExistsOnPoints (m : Settling) (A : U) (p : A -> Law) (pts : List (A * Evidence)) (c : Coverage) : Bool :=
  m.settles (Exists A p) (Points A pts c) == existsVerdict (pointVerdicts m A p pts) c
-- `and` by a pair, its verdicts combined; `or` by either side, which confirms when its side does,
-- or by a pair of refutations
BothByPair (m : Settling) (p q : Law) (e f : Evidence) : Bool :=
  m.settles (Both p q) (Pair e f) == m.combine (m.settles p e) (m.settles q f)
EitherBySide (m : Settling) (p q : Law) (side : Bool) (e : Evidence) : Bool :=
  m.settles (Either p q) (Side side e)
    == (if isConfirmed (m.settles (if side then p else q) e) then Confirmed else Unsettled)
EitherRefutedByBoth (m : Settling) (p q : Law) (e f : Evidence) : Bool :=
  m.settles (Either p q) (Pair e f)
    == (if isRefuted (m.settles p e) and isRefuted (m.settles q f) then Refuted else Unsettled)
-- `not` exchanges confirmation and refutation; what is only supported or unsettled stays unsettled
NotFlips (m : Settling) (p : Law) (e : Evidence) : Bool := m.settles (Not p) e == flip (m.settles p e)
-- `then` is material: settled as `not (p and not q)`, by the same evidence
ThenIsMaterial (m : Settling) (p q : Law) (e : Evidence) : Bool :=
  m.settles (Then p q) e == m.settles (Not (Both p (Not q))) e
-- a citation or an assumption models any law whole, and says on what it is taken
CitedWhole (m : Settling) (p : Law) (r : String) : Bool := m.settles p (Cited r) == Cites r
AssumedWhole (m : Settling) (p : Law) : Bool := m.settles p Assumed == Assumes
-- a run that did not run settles nothing
NotRunIsUnsettled (m : Settling) (p : Law) (r : String) : Bool := m.settles p (NotRun r) == Unsettled
-- the combination of a conjunction's verdicts: commutative and associative, a refutation absorbs
-- everything, an unsettled part absorbs all but a refutation, and confirmation is neutral; beyond
-- that it is the demand's (5.S8)
CombineCommutes (m : Settling) (u v : Verdict) : Bool := m.combine u v == m.combine v u
CombineAssociates (m : Settling) (u v w : Verdict) : Bool := m.combine (m.combine u v) w == m.combine u (m.combine v w)
CombineAbsorbs (m : Settling) (v : Verdict) : Bool :=
  m.combine Refuted v == Refuted and (isRefuted v or m.combine Unsettled v == Unsettled) and m.combine Confirmed v == v

Settling := CaseIsEvaluated & ForallAtOnePoint & ForallOnPoints & ExistsAtOnePoint & ExistsOnPoints & BothByPair
  & EitherBySide & EitherRefutedByBoth & NotFlips & ThenIsMaterial & CitedWhole & AssumedWhole & NotRunIsUnsettled
  & CombineCommutes & CombineAssociates & CombineAbsorbs
````

### `07-tests.md`

````
# 7. Tests and generators

Chapter 7 of the specification, draft 0, 2026-10-12. It rewrites `docs/spec/08-tests.md` (draft 1 of 2026-10-06, commit d12b554 as the brief names it), which turned the analysis `record/generators-2026-10-06.md` into rules with the decisions Luciano took on it the same day (`sonolocalizacion/Lucianos feedbacks/oct 6 0703.txt` and `oct 6 0734.txt`); the grades and the evidence cost follow `docs/principles.md` (L10, L9, L5.18) at its projection of 2026-10-12, and the code read is `src/luthier/generators.py`, `testing.py`, `certify.py`, `cli.py` and `lib/random.lut`. Written by Claude Sonnet 5.5. It realizes L10.3 and L5.18. The grammar changes of the source's section 12 are applied by chapter 2, not here. The decisions Luciano took on 2026-10-05 and 2026-10-06 are D-2026-10-06-ab, and the grammar written for them D-2026-10-06-ac; an item resting on them is `[decided]`, and a part of an item that runs today is marked `[implemented]` where the item says so:

- A type has no single generator, so every test says which generators it used, and its certificate records them.
- Generators are values of Luthier like any other. The random source is an extern whose laws of stochasticity are stated in Luthier; what is heavy runs as an extern.
- Generators are functors over types: when a type is well defined, its generator is obvious. So the generic generators are few (exhaustive, and sampled with a linear or a logarithmic metric), and sampling by a weight puts numbers and lists under one rule.
- Drawing a type is an error. There are generators only of defined types.
- The bounds of a number are part of its type, decided when the type is defined.
- A certificate says that a defined value belongs to a defined type. For a function the value is the function, and a run must use it inside what the certificate's generators covered. For the result of an analysis the value is the result, checked once, when it is produced.
- A statistical law declares its level and its power.

## §1 Notation

The notation of the specification is `spec 1`; what follows is local to this chapter.

`T`, `A`, `B` are types, `x : T` says that `x` has type `T`, and the subtype is as `spec 1` writes it. `U` is the type of types. A *case* gives a value to each parameter of a law, the parameters being the variables it quantifies over. A *test* evaluates the laws of a name on cases; `n` is the number of cases its directive asks for. `Gen T` is the type of the generators of `T` (spec 7.S1). The *size* `s : Nat` bounds lengths and depths. A *seed* is a value of `Seed`, an integer in [0, 2^31). The *support* of a generator is the set of values it gives with nonzero probability; its *measure* says how likely each part of the support is.

A *weight* `c : T -> Float64` is a non-negative function on the values of `T`: the density of a measure, with respect to counting on a finite support and to length on an interval of numbers. The source called it a cost; that word is kept for the values of laws (Terms), so a weight and a cost are different things here. `C` is the total weight of a support. A *binding* maps parameters, or types, to generators; a *profile* is a binding with a name. A *census* is a finite list of values given explicitly. The *reach* of a certificate entry is what its generators covered, parameter by parameter: one value, the `k` values of a census, a whole finite type, or an interval with its measure.

`α` is the *level* of a statistical law: the probability that it fails when the model it tests is correct. `β` is its *power* against a given wrong model: the probability that it fails then. `Φ` is the distribution function of the standard normal. `κ` is the condition number of a matrix, its largest singular value over its smallest. `ε̂(n, δ)` is the bound on the fraction of a distribution where a law fails, given `n` samples and the confidence 1 - δ (spec 7.S11).

## §2 Generators are values

**7.S1. A generator is a value of type `Gen T`.** [decided D-2026-10-06-ab] `Gen T = Nat -> Seed -> T * Seed`: a size and a seed give a value and the next seed, as in `lib/random.lut` today with `Seed` in place of `Int`. [implemented] The file defines `Gen` over `Int`, `Seed` beside it, and generators written in Luthier (`genInt`, `genList`) that the interpreter runs. A generator is defined, typed and certified like any other value (L14.2), and its type states what it promises. Validity: every value it gives belongs to `T`; for `g : Gen { x : T | p x }` this is the obligation that `p` holds of the value `g` gives, for every size and seed, tested as the obligation of an extern is (spec 4). Distribution, when the generator claims one (orthogonal matrices drawn uniformly, a log-uniform number, the random source itself): a law that the probability integral transform of its values is uniform, certified as a statistical law is (spec 7.S17), with its own count of draws (spec 7.S8). The random source is an extern that gives seeds in batches; its laws (uniform values, independent successive draws) are stated in Luthier and certified like those of any extern. [decided D-2026-10-12-ah] The distribution law and its count of draws are the model's. The act `gen T := g`, which made `g` the generator of `T`, is removed (D-2026-10-06-ac): no type owns a generator (spec 7.R1). Today the interpreter still registers generators by type with `gen`.

## §3 Generic generators are functors over the type

A generic generator takes a type and builds a generator of it by following the type's structure, the same way for every type. There are four, each with its parameters.

| generic generator | parameters | gives |
|---|---|---|
| `value v` | a value | `v`, always |
| `census vs` | a list of values; optionally a weight | each value of the list in turn, or draws from it by its weight |
| `exhaustive` | none | every value of a finite type |
| `sampled m` | a metric: `linear`, `log`, or a weight | draws by the inverse of the cumulative weight |

**7.S2. Sampling inverts a cumulative weight.** [decided D-2026-10-12-ah] His idea (D-2026-10-06-ab), decided with the chapter. To draw from a support with weight `c`, draw `u` uniform in [0, C) and return the first value at which the cumulative weight exceeds `u`. Over a finite list `v1, ..., vk` the cumulative weight at `vi` is the running sum `c(v1) + ... + c(vi)`. Over an interval [lo, hi] of numbers it is the integral of `c` from `lo` to `x`. The two metrics of numbers are two weights: `linear` is `c(x) = 1`, uniform between the bounds, and `log` is `c(x) = 1/|x|`, uniform in the logarithm of the magnitude, which needs a positive lower bound on the magnitude. A census with weights and a range of numbers are drawn by the same rule. Feat [Duregård, Jansson and Wang 2012] draws values of algebraic types in this way, indexing into the cumulative counts of the values of each size.

**7.S3. How the functors follow a type.** [decided D-2026-10-06-ab] That generic generators are functors over the type is his; the table below is the model's, [decided D-2026-10-12-ah]. `exhaustive` and `sampled m` apply to a type by its form, as the table gives.

| form of the type | `exhaustive` | `sampled m` |
|---|---|---|
| `Unit`, `Bool`, `Fin n` | every value | by weight, equal unless given |
| `Int`, `Nat` with bounds | every value between them | the metric over the bounds |
| `Int`, `Nat` without bounds | error (spec 7.R3) | the metric over [-s, s] or [0, s] |
| `Float64`, `Rational` | error (spec 7.R3) | the metric over the bounds, continuous; without bounds, error (spec 7.S4) |
| product, record | the product of the components | each component, dependent ones in order (spec 7.S7) |
| sum | each constructor with each payload | a constructor by weight, then its payload; [proposed] on a recursive `data` the size bounds the depth: at size 0 only constructors with no recursive argument, otherwise the size less one is split among the recursive arguments, as Feat counts by size (spec 7.S2) |
| `List A`, `Vec A` | every length up to the size, entries exhaustive | a length (spec 7.S5), then that many entries |
| function over `Fin n` | every table, when the codomain is finite | a table, each entry from the codomain |
| function over an infinite domain | error: bind a census (spec 7.R4) | error: bind a census (spec 7.R4) |
| the models of a theory | error: bind a census (spec 7.R4) | error: bind a census (spec 7.R4) |
| `{ x : T \| p x }` | the values of `T` where `p` holds | bounds when `p` is an interval, otherwise a filter (spec 7.S6) |
| `U` | error (spec 7.R2) | error (spec 7.R2) |

[implemented] Without the names of the functors, `generators.py` follows most rows today: under `exhaustive` it enumerates `Fin n`, an integer with closed bounds, non-recursive data, products, sums and the tables of a function over `Fin n` (up to 20000 tables), takes an `Int` without bounds in [-s, s] and grades the test bounded, and stops on any other infinite type; sampled, it draws `Int` and `Float64` uniformly in [-s, s], a sum by a constructor drawn uniformly, a function over `Fin n` as a table, a subtype by a filter, and a type with a registered generator by that generator. It has no metric, no census, and draws a function over an infinite domain as a constant or an affine map (spec 7.R4).

**7.R1. A test names its generators.** [decided D-2026-10-06-ab] The directive of a test names the functor it applies to every parameter (`with n` is `sampled` with `n` cases; `exhaustive`), the metric of `sampled`, and may bind single parameters, or types, to other generators, inline or through a profile: In the language designed the directive is the function of 7.S20.

    profile tape := { Seed := sampled linear, TestedFull := scaledPositionsWithin freeDim positionBox }

    test gaussianFamily with 100 sampled linear under tape where {
      n   := census [0, 1, 2, 3, 5],
      tol := sampled log }

A binding keyed by a parameter applies to that parameter in every law of the test; one keyed by a type applies to every parameter of that type, aliases expanded (spec 4). A parameter binding wins over a type binding, and a binding in `where` over one in the profile. A parameter that the functor cannot generate and that nothing binds is a static error, which names the parameter and the kind of binding it needs. The certificate records, for every parameter of every law, the generator that drew it, expanded (spec 7.S9). Binding by parameter is the base because it is the only form that tells two parameters of one type apart: in the example, `tol` and the entries of the mean are both `Float64`, and need different metrics. [implemented] Today the directive is `test name [with n | exhaustive] [size k]` (`parser.py`), and `luthier test` takes `--n`, `--exhaustive`, `--size` and `--seed`; there are no bindings and no profile.

**7.R2. No generator gives a type.** [decided D-2026-10-06-ab] A binding of a parameter of type `U`, and a test of a law quantified over a parameter of type `U`, are static errors. A law over a declared type is certified per filling of the hole (spec 4), with the generators of the type that fills it, and a law over the models of a theory is certified per model (spec 7.R4). Few definitions should take a type as a parameter. The legitimate ones are containers (`List A`, `Vec A`) and the laws of `algebra.lut`, which are predicates applied at a concrete type where they are used. A test of a container names the instance it runs at; for a parametric property one well-chosen instance can stand for all of them [Bernardy, Jansson and Claessen 2010]. The libraries that quantify over a type where they mean a vector (`Theta : U` in `probability.lut`, `belief.lut` and `optimization.lut`, and `IsGradient` in `array.lut`) are to be rewritten over `VecOf n` with `n : Nat`, whose generators exist. Today a parameter of type `U` is not a static error: the test stops on it with "no generator" and the law is not run.

**7.R3. `exhaustive` applies to finite types only.** [decided D-2026-10-06-ab] Under `exhaustive`, a parameter of an infinite type (an integer without bounds, any `Float64`, `Rational` or `Real`) is a static error unless it is bound to a census. Lists are enumerated up to the size. [decided D-2026-10-12-ah] When the product of the finite parameters exceeds a budget (spec 7.S8), the cases are a covering array of pairs [Kuhn et al. 2004], which contains every pair of values of any two parameters, and the grade says so (spec 7.S10). [implemented] Today a type that cannot be enumerated stops the test, at test time and not statically, with a message asking for `with n`.

## §4 Numbers

**7.S4. The bounds of a number are in its type; its metric is in its generator.** [decided D-2026-10-06-ab] The bounds of a numeric parameter belong to its type and are decided when the type is defined: a tolerance of Levenberg-Marquardt is not any positive double. `lmTol : { t : Float64 | 0.0 < t }` becomes a type with both bounds, and so do the tolerances of the libraries. A double without bounds in its type needs them from its binding (`sampled log in [1.0e-15, 1.0e-2]`). The metric is chosen by the generator. `linear` is the measure that does not change under translation, for quantities whose meaning does not change when they are shifted: a coordinate, a residual, a log-likelihood. `log` is the measure invariant under scaling, for quantities that keep their meaning under multiplication: a standard deviation, a distance, a tolerance, a condition number. [decided D-2026-10-12-ah] The two readings of the metrics, the atom at 0 and the special values are the model's. A `log` metric over a type that contains 0 draws 0 as an atom, with a probability that is a parameter, and draws a sign when both signs are allowed. Special values join every numeric generator with a total probability (spec 7.S8): the bounds and their neighbours, 0, 1 and -1 when they are in the support, and the literals of the program that fall inside the bounds (thresholds such as `zMax >= 3` are where off-by-one errors sit). Doubles are drawn continuously between the bounds. NaN and the infinities are not values of `Float64` (`core.lut`), and no generator gives them.

## §5 Vectors and matrices

**7.S5. Dimensions from a census, entries from a numeric generator, structure from a family.** [decided D-2026-10-06-ab] A vector generator is a dimension generator and an entry generator. The dimensions default to the census 0, 1, 2, 3, 5, 10 (LAPACK tests at these and at 50), which a binding can change. Matrices with structure are drawn by named families, each a generator: unit vectors, uniform on the sphere; probability vectors (Dirichlet); positions in a box; symmetric; symmetric positive definite with a given spectrum; orthogonal, drawn uniformly (the Haar measure, from the QR factorization of a Gaussian matrix with the signs of the diagonal of R); prescribed singular values with a condition number `κ` and a mode (one large value, one small value, geometric, arithmetic, log-uniform), as LAPACK's xLATMS; low rank; nearly singular; scaled near underflow or overflow; diagonal and triangular. The constructions are those of section 5 of `record/generators-2026-10-06.md`. A family that claims a distribution states it as a law (spec 7.S1); Mezzadri shows that a QR without the sign correction gives orthogonal matrices with the wrong distribution, which their type cannot see. A family can give the pair (`κ`, A), so that a law states its tolerance as a function of `κ`.

The generic generators (spec 7.S2, spec 7.S3) and the families are to be written in Luthier (L14.2): the functors and the numeric generators in `lib/generators.lut`, the families in `lib/array.lut`, both `[proposed]` and not written. [decided D-2026-10-13-ad] Their theories are `src/luthier/lib/generators.lth` (the source and its laws, sampling by weight, the metrics by their invariance, exhaustive and sized generators, filters, censuses, bindings, budgets) with the models of `generators_model.lut`; the functors over the forms of a type wait for core. What exists is `lib/random.lut`: `Gen`, the congruential source `nextSeed`, `randBelow`, the generators `genInt`, `genNat`, `genBool`, `genFloat64`, `genList`, `genSeed`, and the type `Seed`; it has no census, no metric, no family.

## §6 Functions and theories

**7.R4. A function over an infinite domain is drawn from a census of models.** [decided D-2026-10-06-ab] A function over `Fin n` is a table (spec 7.S3). A function over an infinite domain, and a value of a theory (a labeled base with laws whose components are functions, such as `Objective`, `Likelihood`, `Sampler`, `Maximizer`), has no generic generator: a test binds it to a census, an explicit list of the program's values of that type.

    likelihoods : Gen (Likelihood FullCoords) := census [fastFull, nativeFull]
    objectives  : Gen Objective := census [from objectiveAt]

A member of a census may be a family, `from f`, where `f` builds a value from its arguments; the arguments are drawn by the binding's generators for their types, so the member stands for the family. This is the certification per model of spec 4, with the models listed. The census is explicit: an implicit one, every value of the type the program defines, would change a certificate's meaning when an unrelated definition is added. `check -v` lists the candidates the program defines. [decided D-2026-10-12-ah] The families as members, the explicit census and the random functions are the model's. Random functions, drawn lazily and memoized per argument, are a later generator, for laws that must hold for every function (those of a fold or a map). Equality of functions is not structural (spec 4), so a law that compares two functions compares their values at points its binding draws.

## §7 Subtypes and dependent records

**7.S6. A subtype is drawn within its bounds or through a filter.** [decided D-2026-10-12-ah] An interval predicate (`lo <= x and x <= hi`, strict or not, on an integer or a double) gives the bounds of spec 7.S4, with no rejection. A subtype with any other predicate is drawn by its base's generator filtered by the predicate. The filter's acceptance rate is recorded, and the draw of one value gives up after a budget of tries (spec 7.S8), which makes the law not run with that reason. A subtype that a filter reaches too rarely is defined constructively, as the image of a construction whose arguments the functor draws, or bound to a named family. [implemented] The filter, with 2000 tries fixed in the code and a message that names the predicate and some rejected values; every value a generator gives is checked against the predicate of its type. An interval predicate is drawn by the filter too.

**7.S7. Dependent components are drawn in order.** [implemented] The components of a record or a pair are drawn in the order of their dependencies, each with the earlier ones in its type. When a component's type is empty for the earlier ones (the entries of `Fin 0`), the earlier ones are drawn again, up to a budget: 10 tries in `generators.py`, an argument by spec 7.S8 [decided D-2026-10-06-ab]. `testing.py` redraws such a case a fixed number of times and counts it as holding vacuously when every draw meets an empty domain.

## §8 Budgets

**7.S8. Every budget is an argument of the test, recorded in the entry.** [decided D-2026-10-06-ab] This is L5.18 applied to tests: the interpreter holds no fixed number for any of these (today it holds some, named here). The budgets are the tries per value of a filter (2000 in the code); the redraws of a dependent record (50 in the code); the probes of a quantified law inside a type (5 in the code); the draws per evaluated case, as a multiple of `n`; the largest size, with a schedule that reaches it within the `n` cases; the product of finite parameters above which a covering array chooses the cases; the total probability of special values, and of the atom at 0 of a `log` metric; the runs that estimate a level (spec 7.S17), and the seeds per control that measure power (spec 7.S19); the count of draws that certifies the distribution of a generator (spec 7.S1). `luthier test` takes each as an option with a default, and every entry records the values it ran with. [implemented] For two of them only: the number of cases and the size are options (`--n`, `--size`), and the seed is recorded. The source named 10 redraws; the code at the commit read has 50, and the figure is the code's.

## §9 Certificates of definitions

For a definition with laws, the value a certificate speaks of is the definition (a function, an extern, a model) and the type is its declared type. Its laws quantify over parameters, so the evidence is a sample, and the certificate says what the sample was drawn from. What a certificate is, its identity, its transport and certification by default are spec 6 (L10.4 to L10.7); this section keeps what is about the test.

**7.S9. The identity of an entry includes its binding.** [decided D-2026-10-06-ab] An entry is identified by the law, the hash of its cone (spec 6) and its binding, expanded: for each parameter, the generator that drew it, as a functor with its parameters or as a name with its fingerprint. One law has as many entries as bindings it was tested under, and "certified" is always "certified under a binding". An entry also records the seed, the budgets (spec 7.S8), the counts of spec 7.S12, the reach, the labels (spec 7.S14) and the time. [implemented] Today the entry records the hash of the cone, the seed, the generation record (generators used, sizes) and the fingerprints of the generators; the binding is not yet in the hash.

**7.S10. Grades.** [decided D-2026-10-12-y] The grades are the five of Terms: proved, exhaustive, cases, sampled, assumed, with the domain and the evidence cost carrying what the older list said. A point is cases with one case; a census of `k` is cases; bounded is exhaustive on the box the domain names; witnessed is cases with a witness; sampled carries its evidence cost. When the parameters of a law are drawn differently, its entry lists the reach of each, and the grade is summarized by the weakest. The fields of the certificate are spec 6. Today `testing.py` labels a law exhaustive, bounded, sampled or certified, the last for a result taken from a stored entry.

**7.S11. The evidence cost of a sampled law.** [decided D-2026-10-12-r] A sampled law costs -log(1 - ε̂(n, δ)) nats of evidence, where ε̂ bounds the failure fraction and δ is the demand's parameter (D-2026-10-12-h). With no failure seen in `n` cases, ε̂ is 3/n at δ = 0.05 [Hanley and Lippman-Hand 1983], the rule of three: the probability that one more draw from the same generators fails is at most 3/n at 95% confidence. The conversion has a declared shape (statistics and δ in, a cost out) and is filled per theory (L10.3); the file that would state it in Luthier is `lib/evidence.lut`, `[proposed]` and not written. How these costs combine along a path is O1.

**7.S12. `n` counts evaluated cases.** [decided D-2026-10-12-ah] A case counts toward `n` when the law was evaluated to a verdict on it. Counted apart: cases whose parameters could not be drawn, cases skipped because the computation of a type obligation raised (spec 4), and cases where a premise was false (the left side of an implication, or the condition of the branch that carries the obligation). A test draws until `n` cases are evaluated or the budget of draws is spent, and an entry is accepted only if its evaluated cases reach the directive's `n`. A law none of whose cases evaluates is not run, with the counts as its reason. A law whose premises never held passed vacuously, and its entry says so. [implemented] Today `testing.py` counts the evaluated cases and the skipped ones, and marks a law not run when no case evaluates; `n` counts draws, not evaluated cases, and premises are not counted.

**7.S13. A known outcome is not recomputed.** [decided D-2026-10-06-ab] A test is deterministic given its code, its binding, its seed and `n`. An entry whose identity, seed and `n` match is reused whatever its outcome: a passed entry certifies, and a failed or not-run one is reported as known, with its date and reason, and not run again. `--deep` runs it again, and a new seed makes a new entry. [implemented] A passed entry whose cone hash matches is reused, and `--deep` runs it again; a failed or not-run entry that matches is listed as known by `check -v` and run again by `test`.

**7.S14. Labels and coverage.** [decided D-2026-10-12-ah] A law or a generator can label its cases (`classify`: near a bound, `κ` above 10^8, a member of a census, a premise that held), and the entry records the share of each label. A law can ask that a label hold in at least a given share of its cases (`cover`). The request is checked statistically, with a sequential Wilson bound as QuickCheck's `checkCoverage` does, and the law fails when its generators do not reach a region its author named.

**7.S15. What a run requires.** [decided D-2026-10-06-ab] `luthier run` requires, for each law in the cone of the entry, a passed entry whose reach covers what the run gives that law; certification is the default and has no opt-out (D-2026-10-12-y, L10.6), so a cone with an uncertified name is refused. The values the run receives (the holes filled by `--set`, such as `lmTol = 1e-12` or the directory of a graph) are compared with the reach when the run starts: inside the interval, or a member of the census. Values computed during the run are compared at each call when the run is `--checked`, and recorded as not compared otherwise. A reach equal to the support of the parameter's type contains every value the type admits, so a run whose values type-check is inside the reach of a test that sampled the whole type. [implemented] Today the refusal is behind `luthier run --require-certified`, not the default, and no reach is compared.

## §10 Certificates of results

**7.S16. A result is checked once, when it is produced.** [decided D-2026-10-06-ab] The result of an analysis (the maximum of a posterior, an evidence, a fit) is one value, produced by a run, and its type says what it is: an optimum of this function on these data from this start; an expensive result carries its inputs and its witness. Its membership in that type is checked once, where it is produced, by the forms of spec 5: the refined value, a witness, or a statistical verdict with its level. The check needs no generator, except for quantifiers inside the type (that no direction increases the function within a step of the optimum, say), which the check draws with generators it names. The outcome goes to the record of the run, `.run.json`, with the hash of the inputs that index the result (L5.6). Certificates of code, the `.cert.json` files, never hold results.

## §11 Statistical laws

A statistical law (the uniformity of draws, a density pair, the transform of residuals) does not settle a fact about its value: a correct model fails it with some probability, and a wrong one passes it with some probability. Its outcome is a verdict with its level, in the form spec 5 gives. The level `α` and the power `β` are parameters of the demand, never constants of the code (L5.18).

**7.S17. A statistical law declares its level.** [decided D-2026-10-06-ab] It returns its statistic, its level `α` and its outcome. `α` is computed from the law's parameters: from the null distribution of the statistic when it is known (for a statistic standardized to z and compared with the threshold `zMax`, `α = 2(1 - Φ(zMax))`; for a Kolmogorov distance, the tail probability it is compared with), and otherwise estimated by running the law on the model it tests, with the number of runs an argument (spec 7.S8), and recorded with its interval.

**7.S18. A failure is repeated once.** [decided D-2026-10-06-ab] A statistical law that fails is evaluated again, with an independent seed derived from the first, and fails when both evaluations fail. The entry records the first failure, and the level of the whole procedure: `α²` for a single-run level `α`, since the two evaluations are independent.

**7.S19. Power is measured on controls.** [decided D-2026-10-06-ab] A statistical law that has controls (models broken on purpose, as the negative controls of the kernel) records, for each control, its rate of detection over `k` seeds, with `k` an argument and a Wilson interval. With the repetition of spec 7.S18 that rate estimates `β²` for a single-run power `β`. A law whose rate on a control is below a threshold (an argument) is reported as weak, and a control it never detects as undetected. The data of 2026-10-06 show why power has to be measured. Fitted to session A, the Kolmogorov test of the transform of the residuals gave tail probabilities between 0.58 and 0.74 for fits whose sigma was 4.9, 15 and 31 cm. The transform is computed with the fitted sigma, so it does not see a problem of scale, and what does see one is an informative prior on sigma. The law passed each time, and nothing in its certificate said that it could not have failed.


## §12 The test as a function

**7.S20. `test` is a function with named arguments.** [decided D-2026-10-12-ab] `test` is a function
of `lib/test.lut`, the one with the most parameters in the language, so each option is a named
argument with a default: the mode (`exhaustive`, `sampled` with its metric), the number of cases,
the size, the bindings and the profile, which is a record value, and every budget of 7.S8. The
directive forms of 7.R1 are its older surface (`spec 2`). [decided D-2026-10-13-ad] `test` builds a
`TestSpec`, data the module keeps (D9 of the plan, `test "x.lut"` the action), in
`src/luthier/lib/test.lth`, which also states what a run gives (its coverage the weakest of the
mode's and the bindings', its cases those asked or not run, 7.S12) and the grades ordered (7.S10).

## Open

- O1: the conversion of a sample's statistics to a cost and the algebra of costs (spec 7.S11, spec 7.S17 to spec 7.S19).
- O5: the decorated output, for the error of a result that carries one (spec 7.S16).
````

### `05-laws.md`

````
# 5. Laws

Chapter 5 of the specification, draft 0, 2026-10-13. Sources: `docs/spec/05-static-semantics.md` §9 at bd4537e (presentations, translations, checks); `docs/rationale/11-cost-valued-laws.md` §2 and §5; `docs/principles.md` L3, L9.2 to L9.4 and L12 at 2b79c02; the decisions D-2026-10-11-a, -d, -l, D-2026-10-12-h, -i, -p, -al and -am; `src/luthier/checker.py` and `lib/laws.lut`, read only. Written by Claude Opus 5.5, the session integrating the specification. Since `Cost` is a library (D-2026-10-12-al), this chapter states what a law is over the cost type `C` of spec 6 and leaves the algebra to the library; the same holds for checks and their failures. It realizes L12 and the part of L3 on equality as a law. What a certificate of a law records is spec 6; how a law is tested, spec 7; which bodies the checker accepts as laws, spec 4.R6.

## §1 Notation

`C`, `≤`, `0`, `⊤`, `⊕` and `lift` are those of spec 6 §1, with the laws of spec 6.S5. `T` is a type, `x` a value of it, `p` a predicate over `T`. `E` is a type of failures, the reasons a check can give. `V` is the type a law's body is valued in: `Bool`, `C`, or a check type (§4).

## §2 What a law is

**5.S1. A law is a term with a verdict.** [implemented] A law is a term valued in `Bool`, or the type `Law` of what a test runs, possibly a function whose parameters are quantified, or a conjunction of such terms (spec 3.S12). Laws accumulate: a function may carry laws that constrain it without determining it, and the laws that determine it up to its equality are the limit a definition may reach, not a requirement (D-2026-10-11-d). Which laws to write is spec 4.R10: the properties that characterize, never a second implementation. [decided D-2026-10-13-aa] The theory `Law` of `lib/laws.lth` admits Boolean cases only until the cost library exists and a case uses it; `Law C` then gains a case valued in `C` (5.S2).

**5.S2. A law may be valued in `C`.** [decided D-2026-10-12-al] A law whose body is valued in `C` states a degree: `0` holds exactly, `⊤` fails, and what lies between is how far it is from holding. Such a law needs no cutoff to be stated; whether its cost is good enough is the demand's (5.S7). The interpreter has no `C` yet, and every law today is valued in `Bool`.

**5.S3. What the core asks of a law's value.** [decided D-2026-10-13-g] One operation, so that the certificate of spec 6 can be written over any of them:

| operation | laws |
|---|---|
| `verdict : V -> C` | for `V = Bool`, `verdict` is `lift`; for `V = C`, the identity; for a check type, `lift` of `holds` (5.S9) |

A law into a type with no `verdict` is not a law. The theory `LawValue V` that states this would live in `lib/laws.lut`, beside the laws of relations (D-2026-10-11-l), and is not written.

**5.S4. Equality is a law of the object.** [decided D-2026-10-11-f] The identity of two values is a law, and the type of its result says what kind: `Bool` where equality is decidable and structural (spec 4.R8), `C` where the carrier has a distance, the distance observed being the cost. An object's equality is the base of every theory over it (D-2026-10-12-ak), and its laws (reflexive, symmetric, transitive) are stated in Luthier. [decided D-2026-10-13-z] Substitutivity over every function belongs to a structural `==` only (`Structural` in `lib/kernel_laws.lth`, spec 3.S36); an observational equality, such as alpha-equivalence or doubles within a tolerance, is always told apart by some function, and is respected by the operations of its own theory, each stating it as a congruence, by the author of the object, with the relations of `lib/laws.lth`.

## §3 Lifting and combining

**5.S5. The lift and its retraction.** [decided D-2026-10-12-am] A Boolean law reads as a cost by `lift` (spec 6.S5). Its retraction `exact : C -> Bool` is `exact c = c ≤ 0`, so it needs nothing beyond the operations already asked. `exact (lift b) = b` holds for both values of `b`: `lift true = 0` and `0 ≤ 0`; `lift false = ⊤`, and `⊤ ≤ 0` must be false. [decided D-2026-10-13-g] That last condition, `⊤ ≤ 0` is false, is the sixth law of spec 6.S5, so that a library cannot take `0 = ⊤`: the trivial algebra satisfies the five laws there and breaks the retraction L12.2 settles. The planner inserts `lift` where a Boolean law meets a cost, at no cost.

**5.S6. How laws combine.** [implemented] Today `&` joins laws, and it is the Boolean and; the conjunction of a theory's laws is one law with one certificate. [decided D-2026-10-12-al] Beyond that, the core asks nothing: Boolean laws combine by and, or, implication and quantifiers into a Boolean law; laws valued in `C` combine by whatever conjunction the library of costs provides, of which the two candidates of D-2026-10-12-p are examples; a combination of both lifts each Boolean part. The composition along a path is `⊕` (spec 6.S12), which is not the conjunction of two laws on one value and need not be the same operation.

**5.S7. No law carries a cutoff.** [decided D-2026-10-12-h] A law states a property or its degree, never a tolerance to accept it at: a tolerance does not survive composition, since two steps each within ε end up within 2ε, so the cutoff belongs to the demand, which hands it to whatever it asks for. The tolerances written in the libraries today are spec 11.S18.

**5.S8. Grades of parts.** [decided D-2026-10-12-i] When a law is a conjunction certified part by part, how the grades of the parts combine (the vector of grades, or the weakest) is the demand's choice.

## §4 Checks

**5.S9. A check is written once, explaining.** [decided D-2026-10-11-a] A predicate is written in the form that explains its failures, `p : T -> Failures E`, the list of failures it finds in `x`, empty exactly when `x` belongs to the subtype. The poorer forms are projections of it, chosen by the demand and never written by hand: every failure; the first `n`; the reason of the first, `T -> { ok : { x : T | p x } || failed : E }`; the refined value, `refine p : T -> Maybe { x : T | p x }`; and `holds p : T -> Bool`, whether the list is empty. `Bool` is the check that explains nothing, `Failures Unit` cut at one failure. A report (`check`, `test`, a diagnostic) asks for every failure, a condition (`if`, `refine`) for one, and the number is the demand's (P11). Not implemented: the checker accepts `Bool` and `Law` as law types and nothing else (`checker.py`), so spec 3.S12 and spec 4.R6 describe `Failures E` as designed, not as running.

**5.S10. Checks belong to a library.** [decided D-2026-10-13-g] By the rule of D-2026-10-12-al, `Failures E`, its projections and their composition live in a library, `lib/checks.lut`, not in the core. The core asks of a check type only the `verdict` of 5.S3, through `holds`, and that a condition can project it to `Bool` (spec 2 §4 translates `if` with a check as its condition). `WellFormed : Program -> Failures E` of spec 4.S21 is then a client of that library.

**5.S11. How checks compose.** [decided D-2026-10-11-a] `and` concatenates the failures of independent checks, which makes the explaining form an applicative functor; `or` holds when either holds and otherwise keeps both lists; `not` has nothing to explain when `p` holds and is taken on `holds`. Checks chained along a dependency (read, then validate, then fit) compose by the bind of the reason form and stop at the first failure. With the dependencies explicit, every failure is well defined: a failure blocks only the cone of its node.

**5.S12. Forms that are not projections.** [decided D-2026-10-13-g] Three contexts ask for more than the failures. A check that computes evidence returns it with the value, a dependent pair whose law says the witness attests `p x` (a Cholesky factor for positive definiteness; *certifying algorithms*, McConnell, Mehlhorn, Näher and Schweitzer, 2011); `refine` is the case where the witness is the value. A statistical check returns its statistic and its level (spec 7.S17), never a refinement, since a passing test does not establish the fact. A check within a tolerance keeps the tolerance in the type of what it refines. A check about the world refines the content it read, not the path it read it from (spec 10).

## §5 Presentations

**5.S13. Translations between presentations.** [decided D-2026-10-13-g] One mathematical object admits several presentations, equivalent choices of primitive operations and laws (a group by product, unit and inverse, or by division alone). A translation between presentations `P` and `Q`, type operators over `U`, is a pair `to : (A : U) -> P A -> Q A` and `from : (A : U) -> Q A -> P A` whose round trip is the identity under the equality each presentation carries (5.S4). The source records it as expressible in version 0 and checked once on De Morgan's laws, certified per model and not for every model; translations as a concept the language names and certifies are later work.

**5.S14. Presentations with no computable translation.** [implemented] Where no translation can be computed, the equivalence of the presentations is a law, one per pair of presentations. `Kernel` in `lib/probability.lut` reads one probability kernel as a sampler, a likelihood and the transform of each datum, with a law on each side of the triangle (the density pair; the slope of the transform; the uniformity of simulated transforms), certified on the model of the tape distances with negative controls that break one side each.

## Open

- O1, for the conjunction of costs and the algebra, now the library's (5.S6).
- O2, for the equality an object carries (5.S4).
- O4, for which laws compose under translation (5.S13).
````
