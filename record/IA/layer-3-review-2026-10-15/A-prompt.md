# Review of layer 3 of Luthier (world and certification), round 1

You are reviewing theory files written in Luthier, a language whose interpreter is being rebuilt from its own theories: a type is a theory (a structure with laws), a value of it is a model, and the language certifies models against their theories by testing. A theory file (`.lth`) declares a record type of operations, states its laws as Bool-valued definitions over a model (`(m : T)`), and defines the theory as their conjunction (`T := Law1 & Law2`); a model file (`.lut`) holds values of theories. Every constructor of a `data` must have a law stating its role (principle L2.7: a definition is a concept; distinct constructors and accessors state no role). A law quantifies over the subtype it means rather than over an implication whose premise random cases rarely meet. The files parse with the project's parser; nothing yet type-checks or certifies them, so you are the first check of their meaning. Grammar, kernel and earlier layers were reviewed in earlier rounds and are not in scope. Do not reopen a decision listed under "Decisions the files cite" unless a file contradicts it; where you disagree with the specification itself, say so as a separate item.

This prompt covers layer 3. `world.lth` states the world as a token threaded through actions (each token used once), actions described over the library's representation of the world, externs as routes validated at their first action, and `Host`, a theory whose laws are the agreement of each action with its description (§5, `agreement`). `world_model.lut` is a model of it. `certification.lth` states what a certificate, a grade and a certifier are, and `certification_model.lut` is a model. The two chapters they realize are `docs/spec/10-world.md` and `docs/spec/06-certification.md`. The material below, in this order: terms and principles L2.7, L9.6, L10, L11 and P11; the decisions the files cite; then the six files. Frozen at commit 055589c.

Cutoffs: D-2026-10-14-c says every law is a Boolean predicate and every cutoff it needs (a tolerance, a resolution, a rank floor, a convergence threshold, a level) is a parameter of the law that the demand supplies (P11), never a constant in a file.

Answer per file, numbered, quoting the line you mean, as briefly as each allows:
1. **Laws that are wrong**: false of the intended model, or unsatisfiable together.
2. **Laws that do not determine what they claim**: where a wrong model passes every law; give it.
3. **Roles (L2.7)**: a constructor of a `data` with no law of its role, or a role law that only lists constructors.
4. **The models against their theories**: a law `world_model.lut` or `certification_model.lut` breaks, with the case.
5. **Against the specification**: where a file says other than its chapter (`10-world.md`, `06-certification.md`) or a cited decision.
6. **Implication over a type**: laws stated over a type with an implication a random case rarely meets, where the subtype should be the quantified domain.
7. **What you would change first**, one thing, with the reason.
8. **Cutoffs**: a cutoff written as a constant where it should be a parameter the demand supplies (D-2026-10-14-c, above).
9. **Certifying the host**: what law is missing for the host to be certified against its description (world.lth §5's `agreement` and `Host`).

Put anything you cannot verify from the files in a final "not sure" list instead of asserting it. Do not rewrite the files.


---

## Material

Frozen at commit 055589c.

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

D-2026-10-11-m  The planner substitutes one implementation for another only along a certified
                equivalence between the two: the identity law of L21, with its result `Bool` or
                `Cost`. The class of L10 is the component connected by such certificates, not
                the set of everything that passes the laws accumulated so far; the distance of a
                chain of substitutions is the sum of its links (rationale 11 §2). A lone
                implementation is never replaced. The author's free choice among the inhabitants
                of an under-determined function (D-2026-10-11-d, P5) stays; the planner's choice
                is only among what has been compared.
Author:     Claude, proposed; Luciano, accepted ("OK")
Quote:      "OK" (0d6932d, under the proposed resolution)
Source:     record/contradictions-ia-2026-10-11.md §2 (the planner's freedom); raised by six of the
            eight critiques in record/IA/principles 2023 10 11/ (a8e28f0)
Kind:       semantics of the planner (L10, L21, W5). For G0 (the quotient lives in the theory; in
            the model the class is what the certificates connect), G3 (the chain carries its
            budget), G4 (every path is written; only the substitution waits for its law). W5's
            agreement test between native and extern is the law that admits the second specimen.
            Dissolves the holotype objection: the formula over Rational is a specimen with grade
            exact, checked by the same pairwise law
Status:     current; in docs/principles.md draft 4 (L10, L16, L21, W5); the spec of the planner
            pending; not implemented

D-2026-10-11-n  Demanding a value demands every certificate in its dependency cone, paid once
                through the memo. The demand may ask otherwise, by a mechanism to be named
                (probably `assumed`), since what could be done Luthier gives a way to do (G4).
                `test` is the action that demands certificates without values. L14 (validated
                the first time an action asks) is the default; L19's "what never reaches an
                output needs no certificate" is its complement, not an exception.
Author:     Luciano
Quote:      "bueno, si, demandar un valor demanda sus certificados, salvo que se pida lo
            contrario (por el principio de que si algo se podria hacer Luthier deberia dar un
            mecanismo para hacerlo) (probablemente con assumed?) test es exactamente eso."
            (0d6932d)
Source:     record/contradictions-ia-2026-10-11.md §2 (one default needs a sentence); raised by
            the three Claude critiques
Kind:       semantics of demand (L14, L19, L2, G1, G4). For L2 (membership is a guarantee for
            what leaves the program), P11 (the opt-out is a parameter of the demand)
Status:     current; in docs/principles.md draft 4 (L2, L14, L19); 04 §7 pending; the opt-out's
            syntax open; not implemented

D-2026-10-12-ac When a file is read. An `extern` is a definition like any other: its name, its
                declared type and the route to the host's function, a datum. The checker registers
                its type and its edge in the graph and does not open the file, which need not exist
                when the program is checked; the file is read when a demand reaches the node, once
                per plan, its hash entering the identity of the result and its certificate; an
                extern no demand reaches is never read and needs no certificate. `import` is read
                at once, since the names it adds are unknown until it is read (the checker is the
                demand that needs them), but the functions it brings are not loaded or evaluated
                until a demand reaches them. One rule: a file is read when some demand needs it;
                the checker demands names and types, `run` and `test` demand values.
Author:     Luciano; the unifying rule and the consequences for certification the model's
Quote:      "todo tiene o no tiene efecto sobre el mundo depende cuando."
            "extern tiene efecto cuando se ejecuta el programa."
            "debemos ejecutar extern si la funcion no es usada por la demanda? yo creo que no."
            "SOlo se registrarian los tipos de la variables y su inclusion en el compilation tree
            pero no se abriria el archivo ni nada (habria que definir si el archivo debiera existir,
            calculo que no debiera)."
            "declaras la ruta para llegar a la funcion."
            "import es otro costal porque import te agrega nombres que si no los importas no sabes
            que existen"
            "entonces import seria de ejecucion inmediata en cuanto a la lectura, pero no en cuanto
            a cargar las funciones."
Source:     chat:4f7f0dc5:1526
            chat:4f7f0dc5:1526
            chat:4f7f0dc5:1526
            chat:4f7f0dc5:1526
            chat:4f7f0dc5:1526
            chat:4f7f0dc5:1539
            chat:4f7f0dc5:1539
Kind:       language (L11, L5, L10.6; spec 3, 10, 12). The interpreter does otherwise today: the
            checker imports the Python module of every extern when it checks the file
            (`src/luthier/checker.py`, the `importlib.import_module` in the registration of an
            extern) and rejects one it cannot resolve
Status:     current; to implement; resolves the question of D-2026-10-12-ab on extern and import
            inside definitions

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

D-2026-10-12-k  A law is the proposition; a certifier is a method that produces evidence for it;
                one law may have several certifiers.
Author:     Luciano, on GPT en
Quote:      "yes"
Source:     same, §4.6
Kind:       principles (L3, L7). For G1
Status:     current; to apply in draft 11

D-2026-10-12-m  Actions on Luthier's own state (writing a certificate, a test) are idempotent and
                memoizable; actions on the world never are.
Author:     Luciano, on Claude
Quote:      "good"
Source:     same, §4.8
Kind:       principles (L9, L10, L11, Terms). For P6 (every change can be undone)
Status:     current; to apply in draft 11

D-2026-10-12-n  L12 reads "no unrecorded policy constants"; kernel primitives (0, ∞, lift, exact)
                and mathematical constants are excluded.
Author:     Luciano, on DeepSeek
Quote:      "ok"
Source:     same, §4.9
Kind:       principles (L12). For P11
Status:     current; to apply in draft 11

D-2026-10-12-p  The algebra of costs is not open at large: two candidate models, min/max and
                1/n log-sum-exp with 1/n sum, the 1/n his addition.
Author:     Luciano
Quote:      "but G2 cost algebra is not that open, there are basically two models: min max vs 1/n
            logsumexp 1/n sum (the 1/n is my addition is it ok?ok)"
Source:     same, §2.4
Kind:       principles (G2, L6). For G2
Status:     current; which combination is parameterizable and which is forced by soundness is D1
            of the plan decisions

D-2026-10-12-q  Sampled links compose along a path when sampled over the same distribution:
                distance summed, failure fraction summed (the union bound), confidence summed in
                δ; the evidence cost of a sampled link, in nats, sums as the distance does. L13's
                "never summed into a path" is deleted; refusing sampled paths is a demand with
                evidence cost zero, a parameter. Luthier supports any composition algebra one
                might think of, starting with the simplest, the sum; the algebra belongs to the
                theory's cost type, the cutoff and the weights to the demand.
Author:     Luciano for the decision and the correction (any algebra, the simplest first); Claude
            for the elaboration (D1 of the plan) and for the reading that the algebra is the
            theory's and the cutoff the demand's
Quote:      "But the idea would be that Luthier should support any algebra that we might think on,
            we should start with the simplest" "ok"
Source:     record/plan-principles-draft-11-2026-10-12-decisions.md D1 (57a0023)
Kind:       principles (L5, L13, the certificate entry, G2). For P11 (the composition algebra a
            parameter), G2 (one logic extended to cost). Against DeepSeek, Kimi and GPT sp, who
            kept L13's prohibition
Status:     current; to apply in step 4 of the execution plan

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

D-2026-10-12-t  An `assumed` certificate carries what is asserted: a Boolean law asserted true, or a
                cost law asserted with a formula of the inputs (a library's documented bound, such as
                LAPACK's p(n)·ε·κ(A)); its bound is 0 or the formula evaluated at the input, its
                evidence cost the demand's parameter for assumptions, with no default. When the
                formula is a cited guarantee with its hypotheses it is proved by delegation, not
                assumed.
Author:     Luciano for the two kinds; Claude for the evidence cost as the demand's parameter
            without default (L16.2 of draft 11, marked by him to elaborate, not refused) and for the
            border with delegation
Quote:      "elabora un poco, supongo que asumed tiene o es boolean o tiene una formula de cost (por
            ejemplo lapack libraries con eps y condition number." (chat, 2026-10-12)
Source:     chat 2026-10-12, on record/draft-11-for-his-marks-2026-10-12.md item 1
Kind:       principles (the certificate entry, L7 delegation, L4 holes). For G2 (evidence is a
            cost), P11 (the cost of an assumption a parameter)
Status:     current; applied in draft 11 as the certificate entry's clause on assumed, proposed
            wording

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

D-2026-10-13-a  There is one world. Its parts (a file, a clock) exist in Luthier's internal
                representation of it: an action is a directed request, checked by comparing the
                representation before and after. Whether two parts are independent is a theory of
                that model, in a library, certified like any law, and not imposed by the language.
Author:     Luciano
Quote:      "No porque en realidad nosotros tenemos una representacion interna del W y podemos
            hacer solicitudes dirigidas y comparamos al principio y final, por lo que la distincion
            esta en nuestra cabeza y no afuera."
            "es un mundo solo, despues podemos tener una teoria de que distintas partes del mundo
            son independientes pero eso estaria en nuestro modelo, no esta impuesto desde el
            lenguaje."
Source:     chat:f15ae1b6:1481
            chat:f15ae1b6:1515
Kind:       principles (L4.12 new; spec 10.S4). For L4, D-2026-10-12-al
Status:     current; L4.12 proposed in its wording

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

D-2026-10-13-b  `W`, the world, is a keyword and a primitive of the core, the counterpart of `U`:
                definitions live in the mind (the universe `U`, timeless, copied, compared,
                memoized) and actions act on the world. The model's proposal for its rules: `W`
                has no introduction (it enters at `main` or the session), no `==`, and each value
                of it is used once (Clean's uniqueness). `U` keeps its name; `M` is a reading of
                the duality, not a symbol.
Author:     Luciano for `W` as a keyword beside `U` and the duality; the model for the three rules
            and for keeping `U`
Quote:      "W como contraparte de U  como palabra clave suena bien."
            "estoy pensando si no seria interesante tener dos primitivas duales  M (mind/model) y W
            (wolrd)"
Source:     chat:f15ae1b6:1473
            chat:f15ae1b6:1481
Kind:       language and principles (amends D-2026-10-12-ab: the keywords gain `W`; L4.11, L7.1,
            Terms; spec 2, 3, 10). For L4, L7, P16
Status:     current, the three rules too since D-2026-10-13-e. His "Si" to keeping `U`
            (chat:f15ae1b6:1498) read as such

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


### `world.lth`

````
-- world.lth: the world as a token threaded through actions, actions described over the library's
-- representation of the world, externs as routes validated at their first action, and the parts of
-- the world a program touches.
--
-- Draft 1, 2026-10-13, by Claude Fable 5.1 in the session (step 6.1 of
-- record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md, before evidence by
-- D-2026-10-13-ad); draft 0 at 1f8c61c, rewritten on the internal review of layers 2 and 3
-- (record/IA/opus-2026-10-13/review-layers-2-3-report.md, world.1 to world.9). 2026-10-15, by Claude
-- Opus 5.5, an agent of the coordinating session, on record/IA/certification-2026-10-14/
-- prompt-first-action.md: `Host` a theory with its laws (§5), `appendStr` given a body (§4).
-- Sources: spec 10.S1
-- to 10.S13; L11; L4.5; D4 and D8 of record/plan/archive/plan-implementation-2026-10-13-decisions.md
-- (the token used exactly once; `W` optional in `main`); D-2026-10-13-a (one world; an action is a
-- directed request, checked by comparing the representation before and after), -b (`W` a
-- keyword), -g; D-2026-10-14-a (functions cross the bridge as callbacks, counted). Pattern of
-- ebnf.lth: a theory, its laws over a model, `T := laws`.
--
-- What this file states. The core knows of the world only the table of 10.S5: the token `W`, a
-- keyword with no `==` and no introduction, which a program never constructs and uses exactly once
-- (D4); and `own`, whether an action concerns Luthier's own store. An action is a function that
-- takes the token first and gives the token after with its result, `W -> ... -> W * A` (10.S3; D8;
-- 2.S17's `w1 <- print w0 "x"`). Since a token is used once and nothing generates one, no law can
-- apply an action to a token twice or compare what two tokens read (the review's world.1): the laws
-- are stated over the library's representation of the world, a type `S` with structural equality,
-- and over an action's description, a function `S -> S * A` that says what the action does to the
-- representation. Those laws are tested by sampling `S`. The host's action is then certified
-- against its description along one chain of tokens: observe, act once, observe again, compare
-- (D-2026-10-13-a); that protocol is stated at the end as a definition, `agreement`, since it
-- threads the token and so is itself an action (10.S3, 12.S23), and `Host`'s laws are its Bool at
-- the action's arguments, which the runner evaluates at an action's first application in a run
-- (10.S10). What cannot be tested (the disk persists while the program is off) is assumed
-- (10.S13, 6.S10).
--
-- Index. Status of each section: done, or todo with what it needs. A session or Codex continuing
-- this file takes the first todo, writes it in the pattern of the done ones, checks it with
-- `luthier parse src/luthier/lib/world.lth`, sets its status to done here, and commits.
--
--   §1 The token, the representation, actions and their descriptions; own actions idempotent
--      (10.S3 to 10.S6; D4, D8).                                                      done
--   §2 Places: what is read at one; an action changes only the places it declares, at every
--      other place; what is assumed (10.S7, 10.S13).                                   done
--   §3 Externs as routes: read at the first demand, the hash of what was read in the
--      identity, validated against the type's laws before applied, refused if refuted, a
--      provisional one applied as debt without validation (10.S8 to 10.S10, L11.2, 4.R5);
--      a Luthier function crossing as a callback, its calls counted, a record of
--      functions crossing by field (3.S23; D-2026-10-14-a, 12.S18).                   done
--   §4 The actions the first slice needs, by their descriptions: `print`, reading a file
--      (10.S2; D8).                                                                   done
--   §5 Certifying a host action against its description along one chain of tokens: the
--      protocol, as a definition (D-2026-10-13-a); `Host` a theory whose laws are the
--      agreement of each action with its description and an observation that changes
--      nothing, validated at the action's first application (10.S10, L11.2).          done
--   §6 Named worlds: an extern with no law runs in one, priced as an assumption (10.S12,
--      L11.6). Waits for evidence (certification.lth).                                 todo
--   §7 The externs of sonolocalización (numpy and its data formats). Waits for the
--      inventory, record/IA/sonolocalizacion-inventory-2026-10-13/.                     todo

import "kernel_laws.lth" Concrete
import "laws.lth" Verdict Refuted Confirmed Supported Unsettled Cites Assumes

-- ---------------------------------------------------------------- §1 The token, the representation, actions

-- An action takes the token first and gives the token after with its result (10.S3, 10.S4, D8):
-- its type says it is an action, and a function that mentions no `W` holds no effect (10.S1).
Action (A : U) = W -> W * A

-- The library's representation of the world: a type `S` with structural equality, so that two
-- states can be compared (D-2026-10-13-a: an action is checked by comparing the representation
-- before and after). What is read at a place of it is `read`; the places are any string (a file
-- path, "stdout", "clock"), so an action that writes where nothing was declared is seen (the
-- review's world.6).
World (S : Concrete) : { read : S -> String -> Maybe String }

-- An action's description: what it does to the representation, a function `S -> S * A`, with
-- whether it concerns Luthier's own store (10.S6, `own`, from the declaration and not from the
-- effect; what declares nothing is a world action, the safer reading) and the places it declares
-- it changes or reads (10.S7; what `agreement` observes). The token is used exactly once (D4): an action whose new token nobody uses is
-- not demanded; that is the checker's over blocks (program.lth), not a law here.
Described (S : Concrete) (A : U) (m : World S) : {
  describe : S -> S * A,
  own : Bool,
  places : List String,
}
stateAfter (S : Concrete) (A : U) (p : S * A) : S := match p { (s, x) -> s }
resultOf (S : Concrete) (A : U) (p : S * A) : A := match p { (s, x) -> x }

-- an own action is idempotent (10.S6): describing it on its own result gives the same state
OwnIsIdempotent (S : Concrete) (A : U) (m : World S) (d : Described S A m) (s : S) : Bool :=
  not d.own or stateAfter S A (d.describe (stateAfter S A (d.describe s))) == stateAfter S A (d.describe s)

-- ---------------------------------------------------------------- §2 Places and what an action changes

-- An action may change the world and Luthier's store, and nothing else (10.S7): not a definition,
-- not a binding of another block. In the world it changes only the places it declares: at any other
-- place, what is read after is what was read before. Quantified over every place, so a random path
-- is one the action must leave alone, which is the case to test.
memberStr (x : String) (xs : List String) : Bool := match xs { nil -> false ; cons y rest -> x == y or memberStr x rest }
ChangesOnlyDeclared (S : Concrete) (A : U) (m : World S) (d : Described S A m) (s : S) (p : String) : Bool :=
  memberStr p d.places or m.read (stateAfter S A (d.describe s)) p == m.read s p

Described (S : Concrete) (A : U) (m : World S) := OwnIsIdempotent S A m & ChangesOnlyDeclared S A m

-- What cannot be tested is assumed, so that the certificate of a run says under what hypotheses it
-- holds (10.S13, 6.S10): what is written at a place is read back at it, and a write changes no
-- other place (the disk persists). Stated as laws of the representation; their evidence for the
-- host is a citation or an assumption (laws.lth, `Assumes`), never a sample.
Persistence (S : Concrete) : {
  world : World S,
  write : S -> String -> String -> S,
}
WriteThenRead (S : Concrete) (s : Persistence S) (st : S) (p c : String) : Bool :=
  s.world.read (s.write st p c) p == just c
WriteChangesOnlyItsPlace (S : Concrete) (s : Persistence S) (st : S) (p c q : String) : Bool :=
  p == q or s.world.read (s.write st p c) q == s.world.read st q
Persistence (S : Concrete) := WriteThenRead S & WriteChangesOnlyItsPlace S

-- ---------------------------------------------------------------- §3 Externs as routes

-- An extern is a name, a declared type and a route to a host function: data (3.S40, 10.S8;
-- D-2026-10-12-ac: a definition like any other, not an action). Its file is read when a demand
-- reaches the node, once per plan, and may be absent while the program is checked (L11.7); the hash
-- of the bytes read, computed by the core, enters the identity of what the extern produces and of
-- its certificate (10.S9). `hash` is the core's (spec 6.S8), declared here until core names it.
hash : String -> String
Route = { name : String, route : String, provisional : Bool }

-- The first time an action asks for an extern, before it is applied, it is tested against the laws
-- of its declared type like any function, and refused if it fails (10.S10, L11.2). The verdict is
-- of the bytes read, so a changed file is validated again and the certificate stays by hash. An
-- extern whose type has no law to validate against is not applied (L11.3). A provisional extern
-- is the declared exception: applied without validation, recorded as debt, listed by `check -v`
-- and never certified (4.R5), so its verdict is an assumption. A model of `Externs` is the
-- validator of a run: the test it runs is test.lth's, and what the evidence settles is laws.lth's.
Externs : {
  verdictOf : Route -> String -> Verdict,
  applied : Route -> String -> Bool,
  identity : Route -> String -> String,
}
settled (v : Verdict) : Bool := match v { Confirmed -> true ; Supported -> true ; Cites r -> true ; _ -> false }
-- applied exactly when its laws are settled by the validation, or it is provisional
AppliedWhenSettled (e : Externs) (r : Route) (h : String) : Bool :=
  e.applied r h == (r.provisional or settled (e.verdictOf r h))
-- a provisional extern is not validated: its verdict is an assumption
ProvisionalIsAssumed (e : Externs) (r : Route) (h : String) : Bool :=
  not r.provisional or e.verdictOf r h == Assumes
-- the identity of what it produces carries the hash of what was read: two reads with different
-- hashes are two identities (`hash` itself is the core's, and what it tells apart is its own law)
IdentityCarriesHash (e : Externs) (r : Route) (h k : String) : Bool :=
  h == k or not (e.identity r h == e.identity r k)
Externs := AppliedWhenSettled & ProvisionalIsAssumed & IdentityCarriesHash

-- A Luthier function passed to a host function crosses as a callback (3.S23; D-2026-10-14-a): the
-- host calls it through the bridge, at the arguments it chooses, and each call gives the
-- function's value there, nothing more than applying it here. The callback takes no token: a
-- function that mentions no `W` holds no effect (10.S1), so the host's calls change no place of
-- the world, and the host's action, with or without a callback, stays one action of the world,
-- described as one (`Described`) and certified along one chain of tokens (§5; D4: the token is
-- the action's, used once by it, and never the callback's). A record whose fields are functions
-- crosses as the record with each field a callback (D-2026-10-14-a): the host reads a field and
-- calls it, and calling the field is calling the function, counted the same. The calls are
-- counted, and the count is in the run's record (12.S18, P2), beside the result: the cost of a
-- fit is in the calls to its objective. [proposed] (D-2026-10-14-a names the count and the record,
-- not its key) The count is per callback crossing, recorded with the route of the extern that
-- received it. A model of `Crossing` is the bridge (run.py): what it gives the host when the host
-- calls at `xs`, the arguments it asked at, with how many calls that was. The theory says nothing
-- of what the host does between the calls; that is the host action's, under `Described`.
Crossing (A B : Concrete) : {
  callBack : (A -> B) -> List A -> List B * Nat,
  callField : List (String * (A -> B)) -> String -> List A -> List B * Nat,
}
mapList (A B : Concrete) (f : A -> B) (xs : List A) : List B :=
  match xs { nil -> nil ; cons x rest -> cons (f x) (mapList A B f rest) }
lengthOf (A : Concrete) (xs : List A) : Nat := match xs { nil -> 0 ; cons x rest -> 1 + lengthOf A rest }
-- each call gives the function's value at the argument: the crossing is faithful
CallbackGivesTheFunction (A B : Concrete) (b : Crossing A B) (f : A -> B) (xs : List A) : Bool :=
  match b.callBack f xs { (ys, n) -> ys == mapList A B f xs }
-- and the calls are counted, one per argument the host asked at (12.S18)
CallsAreCounted (A B : Concrete) (b : Crossing A B) (f : A -> B) (xs : List A) : Bool :=
  match b.callBack f xs { (ys, n) -> n == lengthOf A xs }
-- a record of functions crosses by field: calling a field is calling the function, counted the same
RecordCrossesByField (A B : Concrete) (b : Crossing A B) (l : String) (f : A -> B) (xs : List A) : Bool :=
  b.callField [(l, f)] l xs == b.callBack f xs
Crossing (A B : Concrete) := CallbackGivesTheFunction A B & CallsAreCounted A B & RecordCrossesByField A B

-- ---------------------------------------------------------------- §4 The actions the first slice needs

-- `print` writes its text as a line at the standard output, a place of the world, and changes no
-- other place; reading a file gives what is at its place, and changes nothing (10.S2; D8: `print`
-- the first action). Stated by their descriptions over the representation; the host's actions in
-- world_model.lut are certified against them by the protocol of §5. `appendStr` is `String`
-- concatenation, the core's `+` on strings [proposed: a body, so that a description runs when a
-- host action is validated against it (§5); declared without one in draft 1, A12 of the naive
-- review, record/IA/review-naive-2026-10-15/].
appendStr (a b : String) : String := a + b
Console (S : Concrete) : {
  world : World S,
  printLine : String -> S -> S * Unit,
  readFile : String -> S -> S * Maybe String,
  stdout : String,
}
lineOf (s : String) : String := appendStr s "\n"
PrintAppendsALine (S : Concrete) (c : Console S) (st : S) (s : String) : Bool :=
  c.world.read (stateAfter S Unit (c.printLine s st)) c.stdout
    == just (match c.world.read st c.stdout { nothing -> lineOf s ; just prior -> appendStr prior (lineOf s) })
PrintChangesOnlyStdout (S : Concrete) (c : Console S) (st : S) (s p : String) : Bool :=
  p == c.stdout or c.world.read (stateAfter S Unit (c.printLine s st)) p == c.world.read st p
-- [proposed] The standard output is a place and not a file: reading the file at a path gives what
-- is read at that place, for every path other than the standard output's place (refuted at
-- p = "stdout" without the premise, by tests/tester/world_laws.lut: `readFile` reads files, and
-- the representation reads the printed text there).
ReadGivesThePlace (S : Concrete) (c : Console S) (st : S) (p : String) : Bool :=
  p == c.stdout or resultOf S (Maybe String) (c.readFile p st) == c.world.read st p
ReadChangesNothing (S : Concrete) (c : Console S) (st : S) (p : String) : Bool :=
  stateAfter S (Maybe String) (c.readFile p st) == st
Console (S : Concrete) := PrintAppendsALine S & PrintChangesOnlyStdout S & ReadGivesThePlace S & ReadChangesNothing S

-- ---------------------------------------------------------------- §5 Certifying a host action

-- A host action is certified against its description along one chain of tokens (D-2026-10-13-a):
-- observe the representation at the places the action declares, act once, observe them again, and
-- compare what the description says with what the host did. Each token is used once. The
-- observation takes the places, since the host cannot read the whole world: a representation
-- stands for the world at the places observed (the coordinator's point on `files`: a read of a
-- file not yet observed looked like a change). The observation is not an action of the program:
-- it changes no place, and the token threads through it.
--
-- The host's side of the console is a theory (L11.2: an extern is declared over a type whose laws
-- it is validated against; D-2026-10-13-a; the naive review's A16/B25, record/IA/
-- review-naive-2026-10-15/for-luciano.md): its actions, routes to the host (world_model.lut), the
-- observation, and for each action the description it is held to, a `Described` value over the
-- representation `world` reads. [proposed] The descriptions are fields of the host's model, so
-- that a model says what each of its actions does and the law needs nothing beyond the model and
-- the action's arguments; `printDescribed s` is `print w s`'s, `readFileDescribed p` is
-- `readFile w p`'s.
Host (S : Concrete) : {
  world : World S,
  observe : W -> List String -> W * S,
  print : W -> String -> W * Unit,
  readFile : W -> String -> W * Maybe String,
  printDescribed : String -> Described S Unit world,
  readFileDescribed : String -> Described S (Maybe String) world,
}
agreement (S : Concrete) (A : Concrete) (m : World S) (o : Host S) (d : Described S A m) (host : Action A) (w0 : W) : W * Bool :=
  match o.observe w0 d.places { (w1, before) ->
  match host w1 { (w2, x) ->
  match o.observe w2 d.places { (w3, after) ->
    (w3, d.describe before == (after, x)) } } }

-- The laws of `Host`. `HostAgrees`, one law per action: each action agrees with its description
-- on the chain of tokens the protocol threads, at the action's arguments; the law is the Bool
-- `agreement` gives, and the token after is the runner's, which goes on with it (D4: used once).
-- And the observation changes nothing: observing twice at the same places reads the same, so
-- that the protocol's own observations are not a change of the world (10.S7). A law that takes
-- the token is not drawn by a sampler (a token is not generated, D4) and `luthier test` does not
-- run it; the runner runs it once, the first time a run asks for the action, with the run's own
-- arguments, and the action the protocol applies is the one the program asked for, applied once
-- (10.S10, L11.2). Its Bool is the evidence (`Evaluated`, laws.lth) of one case at those
-- arguments; the entry is kept by the hash of the model's cone, which holds the host's code (10.S9,
-- 6.S8), so a changed host is validated again.
HostAgreesPrint (S : Concrete) (o : Host S) (s : String) (w0 : W) : Bool :=
  match agreement S Unit o.world o (o.printDescribed s) (fn w { o.print w s }) w0 { (w1, holds) -> holds }
HostAgreesReadFile (S : Concrete) (o : Host S) (p : String) (w0 : W) : Bool :=
  match agreement S (Maybe String) o.world o (o.readFileDescribed p) (fn w { o.readFile w p }) w0 { (w1, holds) -> holds }
HostObserveChangesNothing (S : Concrete) (o : Host S) (places : List String) (w0 : W) : Bool :=
  match o.observe w0 places { (w1, first) -> match o.observe w1 places { (w2, second) -> first == second } }
Host (S : Concrete) := HostAgreesPrint S & HostAgreesReadFile S & HostObserveChangesNothing S
````

### `world_model.lut`

````
-- world_model.lut: the first model of the world: a representation, the descriptions of the console's
-- actions over it, and the host's actions as externs.
--
-- Draft 1, 2026-10-13, by Claude Fable 5.1 in the session (step 6.1; draft 0 at 1f8c61c). The
-- representation `State` is what the host observes of the world at the places it is asked for:
-- the standard output, and the files at the paths observed (10.S5: the library gives the
-- representation and the observations). `observe w places` reads those places from the world; a
-- path with no file is absent from `files`, so `readFile` of it gives `nothing`. `console` describes `print` and `readFile` over it, pure functions that world.lth's
-- laws test by sampling `State`; `host` is the actions themselves, routes to host functions
-- (10.S8), certified against `console` by the protocol of world.lth §5 along one chain of tokens.

import "world.lth" World Described Console Host appendStr lineOf

-- the representation: the standard output so far, and the files by path
State = { stdout : String, files : List (String * String) }
lookupFile (fs : List (String * String)) (p : String) : Maybe String :=
  match fs { nil -> nothing ; cons (q, c) rest -> if p == q then just c else lookupFile rest p }

-- the observable world: what is read at a place of the representation
theWorld : World State := {
  read := fn st p { if p == "stdout" then just st.stdout else lookupFile st.files p },
}

-- the console, by its descriptions: `print` appends a line to the standard output and changes
-- nothing else; `readFile` gives what is at the path and changes nothing
console : Console State := {
  world := theWorld,
  printLine := fn s st { ({ stdout := appendStr st.stdout (lineOf s), files := st.files }, unit) },
  readFile := fn p st { (st, lookupFile st.files p) },
  stdout := "stdout",
}

-- the descriptions the host's actions are held to (world.lth §5, `Host`'s laws): `print w s` is a
-- world action that changes the standard output only, as `console.printLine s` says; `readFile w p`
-- a world action that reads the file at `p`, its one declared place, and changes nothing, as
-- `console.readFile p` says (10.S7: the places are what `agreement` observes)
printDescribed (s : String) : Described State Unit theWorld := {
  describe := console.printLine s,
  own := false,
  places := ["stdout"],
}
readFileDescribed (p : String) : Described State (Maybe String) theWorld := {
  describe := console.readFile p,
  own := false,
  places := [p],
}

-- the host's actions, routes to Python: the token comes first and goes back unchanged (run.py
-- makes it once per run); `observe w places` reads the standard output and the files at `places`.
-- `Host`'s laws hold each action to its description; run.py validates an action at its first
-- application in a run (10.S10, L11.2) and keeps the entry in world_model.cert.json.
HostConsole = Host State
host : HostConsole := {
  world := theWorld,
  observe := extern "python:luthier.host.observe",
  print := extern "python:luthier.host.print_line",
  readFile := extern "python:luthier.host.read_file",
  printDescribed := printDescribed,
  readFileDescribed := readFileDescribed,
}
````

### `certification.lth`

````
-- certification.lth: the entry of a test's outcome, a law's certificate, what a run requires, and
-- the hash of a cone; Boolean, with the cutoffs as parameters.
--
-- Draft 0, 2026-10-14, by Claude Opus 5.5, an agent of the coordinating session, on the brief
-- record/IA/certification-2026-10-14/prompt-theory.md (step 5.1 of
-- record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md). Sources: spec 6.S1 to
-- 6.S16 (docs/spec/06-certification.md); 7.S9, 7.S10, 7.S12, 7.S13, 7.S15; 12.S11, 12.S16, 12.S17;
-- D-2026-10-14-c (first everything Boolean: every cutoff is a parameter the demand supplies);
-- D-2026-10-13-m (the cost types come later); laws.lth §3 (`Evidence`); test.lth §3 (`Grade`, its
-- order, `weakest`); generators.lth (`Seed`, `Budgets`; `Binding`, which 7.S9 expands); term.lth §4
-- (the canonical form the hash of a cone covers, 3.S34). Pattern of test.lth.
--
-- What this file states. 6.S16 asks for a theory over a cost type `C`. D-2026-10-14-c says first
-- everything Boolean, so here a law passes or does not, the bound of an entry is `lift` of its
-- outcome (a pass is `0`, a failure `top`, refused by every cutoff, 6.S5), and the evidence cutoff
-- of a demand is the weakest grade it accepts, a parameter of the demand. Where a cost would enter
-- (6.S5, 6.S6, 6.S11, 6.S12, 6.S15) there is a hole `C`, with the comment "D-2026-10-13-m, after
-- the slice's failures". A model of `Certifying` reads the store; `certification_model.lut` is
-- the reference, and the host's certify.py, tester.py and `run`'s refusal are its specimen
-- (6.S16, L14.3). What the brief or the spec leaves open is marked [proposed] at the item above it.
--
-- Index (all sections written in this draft):
--   §1 The entry: its identity, what it holds, its state; the store (7.S9, 7.S12, 7.S13, 6.S6,
--      6.S8, 12.S11).                                                                          done
--   §2 The certificate: the entries of one law, its grade the weakest; transport along an
--      identity and a path, no evidence for free (6.S7, 7.S10, 6.S11, 6.S12, 6.S13).           done
--   §3 What a run requires: `serves`, the refusal, `Certified` (6.S14, 6.S15, 7.S15, 12.S17).  done
--   §4 The hash of a cone (6.S8, 12.S11, 3.S34).                                                 done
--   §5 The theory `Certifying`, the laws of §1 to §3 claimed.                                    done

import "laws.lth" Evidence
import "test.lth" Grade Proved ExhaustiveGrade Cases Sampled AssumedGrade gradeRank weakest
import "generators.lth" Seed Budgets
import "term.lth" Term Alpha CanonicalForm

-- The cost type of 6.S4, and what an entry carries in it (6.S6: the bound observed and the
-- evidence cost), compared with a demand's cutoff in the order of `C` (6.S15) and composed by its
-- `⊕` along an identity or a path (6.S11, 6.S12): holes. D-2026-10-13-m, after the slice's
-- failures. In this draft the bound is `lift` of the outcome (§1) and the evidence is the grade
-- (§2), compared with the grade a demand accepts (§3).
C : U
entryBound : Entry -> C
entryEvidence : Entry -> C

-- ---------------------------------------------------------------- §1 The entry

Hash = String

-- 7.S9: the binding of an entry, expanded: for each parameter, the generator that drew it, as a
-- functor with its parameters (printed) or as a name, with its fingerprint. A `Binding` of
-- generators.lth (by parameter or by type, in `where` or in a profile) resolved for one parameter
-- (`resolve`) gives one of these.
Drawing = { parameter : String, generator : String, fingerprint : String }

-- A value a run gives a parameter (7.S15: the holes filled by `--set`): a number, or any other
-- value by its printed canonical form. [proposed] Two kinds suffice to compare with a reach: an
-- interval reads numbers, a census compares by equality.
Value : U := data {
  Number : Float64 -> Value ;
  Printed : String -> Value ;
}

-- The reach of a parameter (7.S10, 7.S15): the support of its type, which contains every value
-- the type admits (the type check is the checker's); an interval of numbers, ends included; or the
-- members of a census. Roles: `ReachesAsSets` (§5).
Reach : U := data {
  Support : Reach ;
  Interval : Float64 -> Float64 -> Reach ;
  Members : List Value -> Reach ;
}
ParameterReach = { parameter : String, reach : Reach }

-- What a run that ran gave (6.S3, 7.S12): passed; failed, with its case printed; or not run, with
-- its reason (no generator, no case evaluated with the counts, fuel spent, a hole without a value).
-- A citation (6.R1) and an assumption (6.S10) are entries that passed, with grade proved or assumed
-- [proposed: the outcome is the verdict's, the grade says on what it stands]. Roles:
-- `OnlyAPassServes`, `AFailureRefutes`, `NotRunAddsNothing` (§5).
Outcome : U := data {
  Passed : Outcome ;
  Failed : String -> Outcome ;
  NotRunFor : String -> Outcome ;
}

-- The identity of an outcome: 7.S9's identity of an entry (the law, the hash of its cone, the
-- binding expanded), with the seed and `n` of 7.S13, under which a test is deterministic.
Identity = { law : String, cone : Hash, binding : List Drawing, seed : Seed, cases : Nat }

-- An entry: its identity; what it holds, the budgets (7.S8), the reach of each parameter (7.S10),
-- the evidence of laws.lth, the grade of test.lth (`nothing` unless it passed), its outcome, the
-- date, the interpreter's revision and the hash of the host code behind each extern the cone
-- calls, by route (6.S8). The counts of 7.S12 and the labels of 7.S14 are in the evidence and its
-- reasons. [proposed] `cases` is the `n` asked, which 7.S12 compares with the cases evaluated.
Entry = { law : String, cone : Hash, binding : List Drawing, seed : Seed, cases : Nat,
          budgets : Budgets, reach : List ParameterReach, evidence : Evidence, grade : Maybe Grade,
          outcome : Outcome, date : String, interpreter : String, hosts : List (String * Hash) }

-- The state of a law in the store, as a refusal lists it (12.S11, 12.S17): the outcome of its
-- latest entry at the current hash; stale, when every entry it has is at another hash (the latest
-- such hash kept); uncertified, with no entry; or provisional, a name built on a provisional
-- extern (4.R5), refused whatever its entries. Stale is never stored: it is read against the
-- current hash. [proposed] A passed entry that does not serve (a reach that misses the run's
-- values, a grade below the cutoff) is listed as `Current Passed`; the refusal says it does not
-- serve. Roles: `RefusalSaysWhy`, `ProvisionalIsRefused` (§5).
State : U := data {
  Current : Outcome -> State ;
  Stale : Hash -> State ;
  Uncertified : State ;
  Provisional : State ;
}

-- The store: the entries, the latest in front (6.S8). Two entries with the same identity have the
-- same outcome (7.S13, determinism), and an entry has a grade exactly when it passed (6.S3: only a
-- pass certifies; test.lth: a refutation or nothing settled has no grade). These are the predicate
-- of the type, so every store built owes them: the tester's, and one read from `x.cert.json`.
agreesWith (k : Certifying) (e : Entry) (es : List Entry) : Bool :=
  match es { nil -> true ; cons f rest ->
    (not (k.identity e == k.identity f) or e.outcome == f.outcome) and agreesWith k e rest }
determined (k : Certifying) (es : List Entry) : Bool :=
  match es { nil -> true ; cons e rest -> agreesWith k e rest and determined k rest }
gradedAsOutcome (es : List Entry) : Bool :=
  match es { nil -> true ; cons e rest -> ((e.outcome == Passed) == not (e.grade == nothing)) and gradedAsOutcome rest }
Store (k : Certifying) : U := { es : List Entry | determined k es and gradedAsOutcome es }

-- A known outcome is not recomputed (7.S13): the latest entry with the identity asked, whatever
-- its outcome. The tester asks before it runs; `--deep` runs again, and a new seed or `n` is a
-- new identity.
known (k : Certifying) (i : Identity) (es : List Entry) : Maybe Entry :=
  match es { nil -> nothing ; cons e rest -> if k.identity e == i then just e else known k i rest }

-- Recording never edits an entry (6.S8): a new entry goes in front and the old ones stay. Writing a
-- certificate is idempotent (6.S15) [proposed: an entry whose identity the store has leaves the
-- store as it is, since 7.S13 says its outcome is the one kept; so `--deep` rechecks and adds
-- nothing, and a new seed adds an entry].
record (k : Certifying) (e : Entry) (st : Store k) : Store k :=
  match known k (k.identity e) st { just f -> st ; nothing -> cons e st }

-- ---------------------------------------------------------------- §2 The certificate

-- A law's certificate (6.S6 for the Boolean case): the law, the current hash of its cone, and its
-- entries. What it is certified on and its grade are read from the entries, not stored apart
-- (6.S7): only the entries of the law at the current hash count (12.S11). [proposed] A failure at
-- the current hash, under any binding, refutes the law, and the certificate has no grade (6.S3: a
-- definition fails when one law fails); otherwise, under one binding the entries add evidence, so
-- the binding's grade is the strongest of its passes (6.S13: a better grade comes from a new
-- check), and across bindings the grade is the weakest (7.S10: the grade is summarized by the
-- weakest). The cost form of the grade (an evidence cost in `C`, 6.S7) is the hole above.
Certificate = { law : String, cone : Hash, entries : List Entry }
withEntry (c : Certificate) (e : Entry) : Certificate := { law := c.law, cone := c.cone, entries := cons e c.entries }
stronger (g h : Grade) : Grade := if gradeRank g <= gradeRank h then h else g

-- The older names of a grade (point, census of k, bounded, witnessed, sampled) read as the five
-- (6.S7, decided D-2026-10-13-g; 7.S10): a point is cases with one case, a census is cases,
-- bounded is exhaustive on the box its domain names, witnessed is cases with a witness.
gradeOfOldName (s : String) : Maybe Grade :=
  if s == "point" then just Cases else if s == "census" then just Cases
  else if s == "bounded" then just ExhaustiveGrade else if s == "witnessed" then just Cases
  else if s == "sampled" then just Sampled else if s == "proved" then just Proved
  else if s == "assumed" then just AssumedGrade else if s == "exhaustive" then just ExhaustiveGrade
  else if s == "cases" then just Cases else nothing

-- What a law stands certified on, and with which grade: the reach of each parameter (7.S10) and the
-- grade. Transport (6.S11) takes B's standing and the standing of the identity of A and B, and gives
-- A on the intersection of the two, with the weaker grade; on nothing outside it. For the Boolean
-- identity of this draft the distance is `lift true = 0`, so B's certificate transports exactly;
-- an identity valued in `C` adds its distance by `⊕` (the hole above). [proposed] A parameter that
-- only one of the two standings reaches is not reached by the transport.
Standing = { law : String, on : List ParameterReach, grade : Grade }

-- Along a path (6.S12): link by link, each link the standing of an identity and the name it reaches.
-- Two links sampled over one distribution compose by the union bound, their failure fractions and
-- their δ summed: that is a cost, the hole above (D-2026-10-13-m, after the slice's failures); here
-- the grades meet by `weakest` and the reaches intersect.
along (k : Certifying) (b : Standing) (path : List (String * Standing)) : Standing :=
  match path { nil -> b ; cons (a, i) rest -> along k (k.transport b i a) rest }

-- ---------------------------------------------------------------- §3 What a run requires

-- A demand on one law (6.S15, 7.S15): the law, the current hash of its cone, what the run gives
-- its parameters (the holes filled by `--set`, compared when the run starts), and the cutoff, the
-- weakest grade the demand accepts (D-2026-10-14-c: a parameter the demand supplies). An assumed
-- entry serves only a demand that accepts `AssumedGrade` (6.S10: the demand names the price of
-- assumptions, with no default). [proposed] The run gives each law its values by parameter name;
-- values computed during the run are compared at each call under `--checked` (7.S15), not here.
-- The cost cutoff of 6.S15 (a bound and an evidence cost in `C`) is the hole above.
Demand = { law : String, cone : Hash, given : List (String * Value), accepts : Grade }
withAccepts (d : Demand) (g : Grade) : Demand := { law := d.law, cone := d.cone, given := d.given, accepts := g }

-- the reach recorded for a parameter, and whether the reaches cover what the run gives
-- [proposed: a value given to a parameter the entry records no reach for is not covered]
reachOf (p : String) (rs : List ParameterReach) : Maybe Reach :=
  match rs { nil -> nothing ; cons r rest -> if r.parameter == p then just r.reach else reachOf p rest }
coversAll (contains : Reach -> Value -> Bool) (rs : List ParameterReach) (given : List (String * Value)) : Bool :=
  match given { nil -> true ; cons (p, v) rest ->
    (match reachOf p rs { just r -> contains r v ; nothing -> false }) and coversAll contains rs rest }
anyServes (serves : Demand -> Entry -> Bool) (d : Demand) (es : List Entry) : Bool :=
  match es { nil -> false ; cons e rest -> serves d e or anyServes serves d rest }

-- The dependency cone of the entry of a run (6.S14, 12.S17): each name, whether it is provisional
-- (4.R5), and the demands on its laws. A name whose type states no law is certified with nothing
-- to run [proposed, 6.S1: certified when each law its type states has a passing entry].
ConeName = { name : String, provisional : Bool, laws : List Demand }
Refusal = { name : String, law : Maybe String, state : State }
appendRefusals (xs ys : List Refusal) : List Refusal := match xs { nil -> ys ; cons x rest -> cons x (appendRefusals rest ys) }
-- the latest entry of a law, and the latest at a hash
latestOf (l : String) (es : List Entry) : Maybe Entry :=
  match es { nil -> nothing ; cons e rest -> if e.law == l then just e else latestOf l rest }
latestAt (l : String) (h : Hash) (es : List Entry) : Maybe Entry :=
  match es { nil -> nothing ; cons e rest -> if e.law == l and e.cone == h then just e else latestAt l h rest }

-- What a run requires (7.S15, 12.S17, 6.S14): a cone the store refuses nothing of. `run` starts
-- only on a value of this type, and otherwise lists each refusal with its state; there is no flag
-- that opts out (D-2026-10-12-y). `test` demands certificates without values (6.S14), which this
-- type does not cover.
Certified (k : Certifying) (es : List Entry) : U := { cone : List ConeName | k.refuse es cone == nil }

-- ---------------------------------------------------------------- §4 The hash of a cone

-- What the hash of a cone covers (6.S8, 12.S11): the code of the cone, each name with its
-- definition (a hole filled is a definition, so an entry is kept per filling); the hash of the host
-- code behind each extern it calls, by route (the source files of the module's directory, or the
-- installed package and its version); and the interpreter's revision. [proposed] The code and the
-- hosts are listed in one order the host fixes (by name, by route), so a list is a cone.
Cone = { code : List (String * Term), hosts : List (String * Hash), interpreter : String }
-- the code in canonical form (3.S34): names without module prefix, terms canonical
canonCode (a : Alpha) (m : CanonicalForm a) (code : List (String * Term)) : List (String * Term) :=
  match code { nil -> nil ; cons (x, t) rest -> cons (m.unqualify x, m.canon t) (canonCode a m rest) }

-- The hash is the host's (an extern, certification_model.lut). Its laws (6.S8): it is a function
-- of the canonical form, and a change to the code, to the host code or to the interpreter changes
-- it. [proposed] "Changes it" is stated as: two cones that differ there have different hashes; a
-- collision of the hash function is the host's, and a sample that finds one refutes the model.
ConeHashing (a : Alpha) (m : CanonicalForm a) : { hash : Cone -> Hash }
HashOfTheCanonicalForm (a : Alpha) (m : CanonicalForm a) (h : ConeHashing a m) (c : Cone) : Bool :=
  h.hash { code := canonCode a m c.code, hosts := c.hosts, interpreter := c.interpreter } == h.hash c
HashSeesTheCode (a : Alpha) (m : CanonicalForm a) (h : ConeHashing a m) (c : Cone) (code : List (String * Term)) : Bool :=
  canonCode a m code == canonCode a m c.code
    or not (h.hash { code := code, hosts := c.hosts, interpreter := c.interpreter } == h.hash c)
HashSeesTheHost (a : Alpha) (m : CanonicalForm a) (h : ConeHashing a m) (c : Cone) (hosts : List (String * Hash)) : Bool :=
  hosts == c.hosts or not (h.hash { code := c.code, hosts := hosts, interpreter := c.interpreter } == h.hash c)
HashSeesTheInterpreter (a : Alpha) (m : CanonicalForm a) (h : ConeHashing a m) (c : Cone) (r : String) : Bool :=
  r == c.interpreter or not (h.hash { code := c.code, hosts := c.hosts, interpreter := r } == h.hash c)
ConeHashing (a : Alpha) (m : CanonicalForm a) := HashOfTheCanonicalForm a m & HashSeesTheCode a m
  & HashSeesTheHost a m & HashSeesTheInterpreter a m

-- ---------------------------------------------------------------- §5 The theory

-- A model of certification reads the store: the identity of an entry, whether it is stale against
-- a hash, the grade of a certificate, whether a reach contains a value, whether an entry serves a
-- demand, what a cone is refused, and transport along an identity.
Certifying : {
  identity : Entry -> Identity,
  stale : Hash -> Entry -> Bool,
  grade : Certificate -> Maybe Grade,
  contains : Reach -> Value -> Bool,
  serves : Demand -> Entry -> Bool,
  refuse : List Entry -> List ConeName -> List Refusal,
  transport : Standing -> Standing -> String -> Standing,
}

-- §1. 7.S9, 7.S13: the identity of an outcome is the law, the cone's hash, the binding expanded,
-- the seed and `n`, and nothing the entry holds besides
IdentityIsTheKey (k : Certifying) (e : Entry) : Bool :=
  k.identity e == { law := e.law, cone := e.cone, binding := e.binding, seed := e.seed, cases := e.cases }
-- 12.S11: an entry is stale when its hash differs from the current hash of its cone
StaleIsAnotherHash (k : Certifying) (h : Hash) (e : Entry) : Bool := k.stale h e == not (e.cone == h)

-- §2. 6.S7, 7.S10: a certificate with no entry has no grade; a failure at the current hash refutes
NoEntryNoGrade (k : Certifying) (l : String) (h : Hash) : Bool := k.grade { law := l, cone := h, entries := nil } == nothing
AFailureRefutes (k : Certifying) (c : Certificate) (e : Entry) : Bool :=
  not (e.law == c.law and e.cone == c.cone)
    or (match e.outcome { Failed x -> k.grade (withEntry c e) == nothing ; _ -> true })
-- 12.S11, 7.S12, 6.S13: an entry of another law, a stale one or one not run adds nothing
OnlyCurrentEntriesCount (k : Certifying) (c : Certificate) (e : Entry) : Bool :=
  (e.law == c.law and not (k.stale c.cone e)) or k.grade (withEntry c e) == k.grade c
NotRunAddsNothing (k : Certifying) (c : Certificate) (e : Entry) : Bool :=
  match e.outcome { NotRunFor r -> k.grade (withEntry c e) == k.grade c ; _ -> true }
-- 7.S10 [proposed reading above]: two passes under different bindings give the weaker grade, under
-- one binding the stronger
WeakestAcrossBindings (k : Certifying) (c : Certificate) (e f : Entry) (g h : Grade) : Bool :=
  not (c.entries == nil and e.law == c.law and e.cone == c.cone and f.law == c.law and f.cone == c.cone
       and e.outcome == Passed and f.outcome == Passed and e.grade == just g and f.grade == just h
       and not (e.binding == f.binding))
    or k.grade (withEntry (withEntry c f) e) == just (weakest g h)
StrongestUnderOneBinding (k : Certifying) (c : Certificate) (e f : Entry) (g h : Grade) : Bool :=
  not (c.entries == nil and e.law == c.law and e.cone == c.cone and f.law == c.law and f.cone == c.cone
       and e.outcome == Passed and f.outcome == Passed and e.grade == just g and f.grade == just h
       and e.binding == f.binding)
    or k.grade (withEntry (withEntry c f) e) == just (stronger g h)
-- 6.S11: transport gives A, on the intersection of the two reaches, with the weaker grade
TransportTakesTheWeaker (k : Certifying) (b i : Standing) (a : String) : Bool :=
  (k.transport b i a).law == a and (k.transport b i a).grade == weakest b.grade i.grade
TransportOnTheIntersection (k : Certifying) (b i : Standing) (a : String) (given : List (String * Value)) : Bool :=
  coversAll k.contains (k.transport b i a).on given
    == (coversAll k.contains b.on given and coversAll k.contains i.on given)
-- 6.S13 (L10.9), for the Boolean case: transport never raises a grade nor widens a reach, and a
-- path neither (the bound is `lift true = 0` along a Boolean identity; in `C`, monotone `⊕`)
NoEvidenceForFree (k : Certifying) (b i : Standing) (a : String) (given : List (String * Value)) : Bool :=
  gradeRank (k.transport b i a).grade <= gradeRank b.grade
    and (not (coversAll k.contains (k.transport b i a).on given) or coversAll k.contains b.on given)
PathNeverRaises (k : Certifying) (b : Standing) (path : List (String * Standing)) : Bool :=
  gradeRank (along k b path).grade <= gradeRank b.grade

-- §3. 7.S10, 7.S15: a reach as a set of values; the support holds every value
ReachesAsSets (k : Certifying) (x lo hi : Float64) (s : String) (vs : List Value) : Bool :=
  k.contains Support (Number x) and k.contains Support (Printed s)
    and k.contains (Interval lo hi) (Number x) == (lo <= x and x <= hi)
    and not (k.contains (Interval lo hi) (Printed s))
    and k.contains (Members vs) (Number x) == anyIs (Number x) vs
    and k.contains (Members vs) (Printed s) == anyIs (Printed s) vs
anyIs (v : Value) (vs : List Value) : Bool := match vs { nil -> false ; cons w rest -> w == v or anyIs v rest }
-- 12.S11: a stale entry certifies nothing
StaleCertifiesNothing (k : Certifying) (d : Demand) (e : Entry) : Bool := not (k.stale d.cone e) or not (k.serves d e)
-- 6.S3: only a pass certifies
OnlyAPassServes (k : Certifying) (d : Demand) (e : Entry) : Bool := not (k.serves d e) or e.outcome == Passed
-- 7.S9, 7.S15: an entry certifies its law only under its binding, on the reach it drew, so it serves
-- a run only when that reach covers what the run gives the law
CertifiesOnlyUnderItsBinding (k : Certifying) (d : Demand) (e : Entry) : Bool :=
  not (k.serves d e) or (e.law == d.law and coversAll k.contains e.reach d.given)
-- 6.S15, D-2026-10-14-c: it serves only at or above the grade the demand accepts
ServesAtTheCutoff (k : Certifying) (d : Demand) (e : Entry) : Bool :=
  not (k.serves d e) or (match e.grade { just g -> gradeRank d.accepts <= gradeRank g ; nothing -> false })
-- and an entry that meets all of these serves (6.S15: a certificate serves every demand it meets)
ACoveringPassServes (k : Certifying) (d : Demand) (e : Entry) (g : Grade) : Bool :=
  not (e.law == d.law and not (k.stale d.cone e) and e.outcome == Passed and e.grade == just g
       and gradeRank d.accepts <= gradeRank g and coversAll k.contains e.reach d.given)
    or k.serves d e
-- 6.S16: `serves` is monotone in the cutoff
ServesIsMonotoneInTheCutoff (k : Certifying) (d : Demand) (e : Entry) (g : Grade) : Bool :=
  not (k.serves d e and gradeRank g <= gradeRank d.accepts) or k.serves (withAccepts d g) e
-- 6.S14, 12.S17: a provisional name is refused whole [proposed: its laws not listed]
ProvisionalIsRefused (k : Certifying) (es : List Entry) (n : String) (ds : List Demand) : Bool :=
  k.refuse es [{ name := n, provisional := true, laws := ds }] == [{ name := n, law := nothing, state := Provisional }]
-- 7.S15, 12.S17: a law no entry serves is refused, listed with its state: the latest entry at the
-- current hash, stale when there is none there, uncertified when there is none at all
RefusalSaysWhy (k : Certifying) (es : List Entry) (n : String) (d : Demand) : Bool :=
  k.refuse es [{ name := n, provisional := false, laws := [d] }]
    == (if anyServes k.serves d es then nil
        else [{ name := n, law := just d.law,
                state := (match latestAt d.law d.cone es { just e -> Current e.outcome ;
                            nothing -> (match latestOf d.law es { just f -> Stale f.cone ; nothing -> Uncertified }) }) }])
-- each name and each law is refused on its own, and a cone with nothing in it is refused nothing
RefusalIsPerLaw (k : Certifying) (es : List Entry) (c : ConeName) (rest : List ConeName) (n : String) (d : Demand) (ds : List Demand) : Bool :=
  k.refuse es nil == nil
    and k.refuse es (cons c rest) == appendRefusals (k.refuse es [c]) (k.refuse es rest)
    and k.refuse es [{ name := n, provisional := false, laws := cons d ds }]
        == appendRefusals (k.refuse es [{ name := n, provisional := false, laws := [d] }])
                          (k.refuse es [{ name := n, provisional := false, laws := ds }])
    and k.refuse es [{ name := n, provisional := false, laws := nil }] == nil

Certifying := IdentityIsTheKey & StaleIsAnotherHash & NoEntryNoGrade & AFailureRefutes & OnlyCurrentEntriesCount
  & NotRunAddsNothing & WeakestAcrossBindings & StrongestUnderOneBinding & TransportTakesTheWeaker
  & TransportOnTheIntersection & NoEvidenceForFree & PathNeverRaises & ReachesAsSets & StaleCertifiesNothing
  & OnlyAPassServes & CertifiesOnlyUnderItsBinding & ServesAtTheCutoff & ACoveringPassServes
  & ServesIsMonotoneInTheCutoff & ProvisionalIsRefused & RefusalSaysWhy & RefusalIsPerLaw
````

### `certification_model.lut`

````
-- certification_model.lut: the store as a value, the reference model of `Certifying`, and the hash
-- of a cone as a route to the host.
--
-- Draft 0, 2026-10-14, by Claude Opus 5.5, an agent of the coordinating session, on the brief
-- record/IA/certification-2026-10-14/prompt-theory.md (item 4). A model file (12.S23): `certifying`
-- reads the store written in Luthier over the kernel's types, and is what certify.py, tester.py's
-- store and `run`'s refusal are certified against (6.S16, L14.3). `hashing` is the host's hash of
-- a cone (6.S8), a route the specimen gives: src/luthier/certify.py must define `cone_hash`, taking
-- a cone (the code in canonical form, the hosts by route, the interpreter's revision) and answering
-- a string; it is validated against certification.lth §4 like any extern (3.S28).

import "certification.lth" Certifying ConeHashing Store Entry Identity Certificate Demand ConeName Refusal
  Standing ParameterReach Reach Value Hash Support Interval Members Number Printed Passed Failed State Current Stale
  Uncertified Provisional Drawing stronger reachOf coversAll anyServes appendRefusals latestOf latestAt
import "test.lth" Grade gradeRank weakest
import "term_model.lut" alpha canonical

-- the store as a value: the entries, the latest in front (6.S8); it starts empty
emptyStore : Store certifying := nil

-- 7.S9, 7.S13: the identity of an outcome
identity (e : Entry) : Identity := { law := e.law, cone := e.cone, binding := e.binding, seed := e.seed, cases := e.cases }

-- 12.S11: stale against the current hash of the cone
stale (h : Hash) (e : Entry) : Bool := not (e.cone == h)

-- 7.S10, 7.S15: a reach as a set of values
anyValue (v : Value) (vs : List Value) : Bool := match vs { nil -> false ; cons w rest -> w == v or anyValue v rest }
contains (r : Reach) (v : Value) : Bool := match r {
  Support -> true ;
  Interval lo hi -> (match v { Number x -> lo <= x and x <= hi ; Printed s -> false }) ;
  Members vs -> anyValue v vs }

-- 6.S7, 7.S10: the grade of a certificate. The entries that count are the law's at the current
-- hash; a failure among them leaves no grade; under one binding the strongest pass, across
-- bindings the weakest.
counts (c : Certificate) (e : Entry) : Bool := e.law == c.law and e.cone == c.cone
anyFailure (c : Certificate) (es : List Entry) : Bool :=
  match es { nil -> false ; cons e rest -> (counts c e and isFailure e) or anyFailure c rest }
isFailure (e : Entry) : Bool := match e.outcome { Failed x -> true ; _ -> false }
-- the passes that count, each with its grade
passes (c : Certificate) (es : List Entry) : List (List Drawing * Grade) :=
  match es { nil -> nil ; cons e rest ->
    if counts c e and e.outcome == Passed
    then (match e.grade { just g -> cons (e.binding, g) (passes c rest) ; nothing -> passes c rest })
    else passes c rest }
-- the strongest grade under one binding
bestUnder (b : List Drawing) (ps : List (List Drawing * Grade)) (g : Grade) : Grade :=
  match ps { nil -> g ; cons (b2, h) rest -> bestUnder b rest (if b2 == b then stronger g h else g) }
-- the weakest of the bindings' bests
weakestOfBests (all ps : List (List Drawing * Grade)) (acc : Maybe Grade) : Maybe Grade :=
  match ps { nil -> acc ; cons (b, g) rest ->
    weakestOfBests all rest (just (match acc { nothing -> bestUnder b all g ; just h -> weakest h (bestUnder b all g) })) }
grade (c : Certificate) : Maybe Grade :=
  if anyFailure c c.entries then nothing else weakestOfBests (passes c c.entries) (passes c c.entries) nothing

-- 6.S15, 7.S15: an entry serves a demand when it is the law's at the current hash, passed, at or
-- above the cutoff, and its reach covers what the run gives
atLeast (accepts : Grade) (g : Maybe Grade) : Bool := match g { just h -> gradeRank accepts <= gradeRank h ; nothing -> false }
serves (d : Demand) (e : Entry) : Bool :=
  e.law == d.law and e.cone == d.cone and e.outcome == Passed and atLeast d.accepts e.grade
    and coversAll contains e.reach d.given

-- 6.S14, 7.S15, 12.S17: what a cone is refused, each with its state
stateOf (d : Demand) (es : List Entry) : State :=
  match latestAt d.law d.cone es { just e -> Current e.outcome ;
    nothing -> (match latestOf d.law es { just f -> Stale f.cone ; nothing -> Uncertified }) }
refuseLaws (es : List Entry) (n : String) (ds : List Demand) : List Refusal :=
  match ds { nil -> nil ; cons d rest ->
    if anyServes serves d es then refuseLaws es n rest
    else cons { name := n, law := just d.law, state := stateOf d es } (refuseLaws es n rest) }
refuseName (es : List Entry) (c : ConeName) : List Refusal :=
  if c.provisional then [{ name := c.name, law := nothing, state := Provisional }] else refuseLaws es c.name c.laws
refuse (es : List Entry) (cs : List ConeName) : List Refusal :=
  match cs { nil -> nil ; cons c rest -> appendRefusals (refuseName es c) (refuse es rest) }

-- 6.S11: transport along a Boolean identity: the intersection of the reaches, the weaker grade
larger (x y : Float64) : Float64 := if x <= y then y else x
smaller (x y : Float64) : Float64 := if x <= y then x else y
keepWithin (r : Reach) (vs : List Value) : List Value :=
  match vs { nil -> nil ; cons v rest -> if contains r v then cons v (keepWithin r rest) else keepWithin r rest }
meet (r s : Reach) : Reach := match r {
  Support -> s ;
  Interval lo hi -> (match s { Support -> r ; Interval lo2 hi2 -> Interval (larger lo lo2) (smaller hi hi2) ;
                                Members vs -> Members (keepWithin r vs) }) ;
  Members vs -> Members (keepWithin s vs) }
meetReaches (bs is : List ParameterReach) : List ParameterReach :=
  match bs { nil -> nil ; cons r rest ->
    (match reachOf r.parameter is { just s -> cons { parameter := r.parameter, reach := meet r.reach s } (meetReaches rest is) ;
                                    nothing -> meetReaches rest is }) }
transport (b i : Standing) (a : String) : Standing := { law := a, on := meetReaches b.on i.on, grade := weakest b.grade i.grade }

certifying : Certifying := {
  identity := identity, stale := stale, grade := grade, contains := contains, serves := serves,
  refuse := refuse, transport := transport,
}

-- 6.S8: the hash of a cone, the host's
hashing : ConeHashing alpha canonical := {
  hash := extern "python:luthier.certify.cone_hash",
}
````

### `10-world.md`

````
# 10. Actions and the world

Chapter 10 of the specification, draft 0, 2026-10-13. Sources: `docs/principles.md` L4, L11, L10.6 and O3; the decisions D-2026-10-10-c, D-2026-10-11-i, D-2026-10-12-m, -ab, -ac, -al; `docs/rationale/09-extern-and-the-world.md` (draft 0, 2026-10-07); `docs/spec/02-grammar.md`, `03-kernel.md`, `04-static-semantics.md` and `12-files-and-tools.md` at e8409ef; `src/luthier/` (cli.py, certify.py, evaluator.py, machine.py), read only. Written by Claude Sonnet 5.5, in wave 3. It realizes L4 (the part on actions) and L11. What a demand is and how a plan is run is `spec 8`; what the planner may substitute is `spec 9`; what a certificate holds is `spec 6`.

## §1 Notation

The notation common to all chapters is in `spec 1`. Here, `W` is a type, the world's token (§3), and `w`, `w0`, `w1` are values of it. An *action* is a function that takes a token and gives a token together with a result. A *world action* acts on something Luthier does not own (a terminal, a file, a clock, a foreign process); a *state action* acts on Luthier's own store (a certificate, the record of a test). `h` is the hash of the bytes of a file.

## §2 What an action is

**10.S1. Evaluation has no effect; an action does.** [decided D-2026-10-10-c] What a definition gives is a function of its inputs alone (L4.7), so no definition holds an effect. An effect lives in an action: printing, saving, writing a certificate, running a host program. The consequence is that evaluation may proceed in any order the dependencies allow, and a memo may serve a result without running anything (`spec 8`).

**10.S2. Where an action may occur.** [implemented] An action occurs in a block, in `main`, or in the session, the three places `spec 2.S17` names for a block; it is refused at a file's top level, where nothing orders the acts (spec 4.R12). Inside a block an action is an item with its result bound, as in `w1 <- a w0 x` (D-2026-10-11-i). Each `<-` makes a fresh name (spec 4.R12), so the block is a sub-DAG whose dependencies fix the order, and two items that share no name commute (spec 2.S17). Today the actions that exist are those of the commands: `run` prints a result and appends to `x.run.json`, and `test` writes `x.cert.json` (spec 12.S10, 12.S18). [decided D-2026-10-13-ad] A program names the actions a world library defines: `print` and `readFile` of `world.lth` §4, modelled in `world_model.lut`, used by `examples/hello.lut`.

**10.S3. An action is declared by its type.** [decided D-2026-10-13-g] L11.4 asks that the declaration of an extern say which of the two it is, definition or action. The proposal is that the type says it: a function whose type takes and gives a `W` is an action, and one that mentions no `W` is a definition and holds no effect (10.S1). The check is then the type's, and spec 4 needs no new rule for it.

## §3 The world

**10.S4. The world is a token threaded through actions.** [decided D-2026-10-13-g] The sources fix that an action on the world is never served from the memo (D-2026-10-12-m) and leave the form to O3: an opaque, unique value. The proposal follows the rationale (its section 3): an action takes the token before and returns the token after, so two readings of one place, before and after a write, are two terms with a dependency between them, and the number and order of operations are in the graph (L4.5 does the same for a mutable parameter). The token has no `==` (spec 4.R8). There is one world (D-2026-10-13-a): its parts exist in Luthier's representation of it, and their independence, if any, is a theory of that representation in a library, never a second token.

**10.S5. What the core asks of a world.** [decided D-2026-10-13-g] Under D-2026-10-12-al the form of the world is a library's, as `Cost` is (spec 6.S4). The core uses the following and nothing more; it chooses no representation, no names and no set of parts of the world.

| operation | used for | laws |
|---|---|---|
| `W` | the token an action takes and gives; a keyword of the core beside `U` (D-2026-10-13-b), the library gives its representation and observations | no `==` (spec 4.R8); a program does not construct one, it enters at `main` or the session |
| `act` | applying an action to a token | gives a new token each time, so two applications to one token are two nodes the memo never merges |
| `own` | saying that an action concerns Luthier's own store | a predicate on actions; an action with `own` is idempotent (10.S6) |

Nothing undoes an action in the language: undoing a change is the history of the repository (P6). Which parts of the world exist, what an observation of one is, and how a class of machines is described belong to the library (§6).

## §4 Two kinds of action

**10.S6. State actions are idempotent and memoizable; world actions never are.** [decided D-2026-10-12-m] Writing a certificate or recording a test acts on Luthier's own state and is verified by reading the store back (Terms). Doing it twice with the same inputs leaves the same store, so it may be memoized, keyed by the hash of the cone (spec 6.S8). An action on the world runs each time it is demanded. [decided D-2026-10-13-g] What separates the two is `own` of 10.S5, taken from the action's declaration and not guessed from its effect; an action with no such declaration counts as a world action, the safer reading.

**10.S7. What an action may change.** [decided D-2026-10-10-c] An action may change the world and Luthier's store, and nothing else: not a definition, not a binding of another block, not a certificate already issued (a new check issues a new certificate and keeps the old, spec 6.S8). A parameter that changes is split in two, its value before and its value after (L4.5); the planner may overwrite in place when nothing else reads the earlier one (`spec 9`), never a semantics. [decided D-2026-10-13-a] That an action changes only what its declaration says is a law of the world's library over the observations it defines, certified as any law (spec 6); until a world library exists nothing checks it.

## §5 Externs as routes

**10.S8. An extern is a route, read when a demand reaches it.** [decided D-2026-10-12-ac] An extern has a name, a declared type and a route to a host function, which is data (spec 3.S40). The file behind the route is read when a demand reaches the node, once per plan; a file that no demand reaches stays unread and may be absent while the program is checked (L11.7). The checker records the target and the type and does not resolve it (spec 4.S24). D-2026-10-12-ac settled that an `extern` is an ordinary definition, a route that is data, and not an action: opening its file is the demand's, not the program's. [implemented] Today the checker imports the host module, and a target that does not resolve is an error, whether or not a demand reaches it (`checker.py` imports the module at check time); D-2026-10-12-ac changes this.

**10.S9. The file's hash is in the identity of what the extern produces.** [decided D-2026-10-12-ac] The hash `h` of the bytes read, computed by the core and not asked of the world's library, enters the identity of the result and of the extern's certificate (`spec 8` gives the identity of a result, spec 6.S8 the certificate's). [implemented] Today the certificate's hash covers the source files of the module behind each extern in the cone (for a library, the package installed with its version) together with the interpreter (spec 6.S8); it is computed when the certificate is, not when a demand reaches the node.

**10.S10. An extern is validated against its type's laws, then applied.** [decided D-2026-10-11-n] The first time an action asks for an extern, before it is applied, it is tested against the laws of its declared type like any function, and refused if it fails (L11.2). Its certificate stays by hash (spec 6.S8). An extern with no type to validate against is not applied; `extern provisional` is the declared exception, recorded as debt, listed by `check -v` and never certified (spec 4.R5). The agreement test with a native definition comes in addition, and substitution follows D-2026-10-11-m (`spec 9`). [implemented] Today `test` certifies the laws of an extern's type as it does any function's, and `run --checked` tests each value that an extern gives back, as it crosses, against the Bool laws of its type (spec 12.S18, 4.R5); `test` takes the laws quantified over a domain, and a function handed back by an extern is tested at each call. An uncertified extern in the cone is listed and the run refused, with no opt-out (spec 12.S17, D-2026-10-12-y; `--require-certified` is retired). The moment of the validation is what runs since 788b7f4: a host action whose theory states the agreement with its description (world.lth §5, `Host`) is validated at its first application in the run by the protocol of `agreement`, with the program's own arguments, refused if the host disagrees (naming the place), and recorded in the model's store when it agrees; `run --checked` tests the subtype predicates of what an extern returns (12.S18).

**10.S11. The bridge.** [implemented] How a value crosses between the host and the kernel, and what is certified at the crossing, is spec 3.S22 to 3.S28. This chapter adds only that a crossing is where each refinement of the declared type becomes an obligation (spec 4.R5).

**10.S12. A foreign algorithm runs in a named world.** [decided D-2026-10-13-g] L11.6 is a candidate and this statement follows it. An extern with no law yet may run in a named world; each certificate it earns is priced as an assumption (L10.2, spec 6.S10), the plan shows which world it ran in, and until a law is certified the planner's graph and every certified theory stay closed to it. L11.4 says what the extern's certificate binds in the host: library version, platform. The name of the world is a parameter of the demand (P11).

## §6 The theory of actions in Luthier

**10.S13. `lib/world.lut`.** [decided D-2026-10-13-g] L14 asks that what can be written in Luthier be written there. The file would state a theory of the world with the table of 10.S5 as its structure and laws; the theory of an action as a function over `W` together with its result, with the law of 10.S7; and, for each part of the world the library chooses, a theory with its observations and its laws, those that cannot be tested marked `assumed` (the disk persists while the program is off, the clock is monotone) so that the certificate of a run says under what hypotheses it holds (spec 6.S10). [decided D-2026-10-13-ad] The file is `src/luthier/lib/world.lth`: the laws of an action are stated over the library's representation of the world and the action's description (D-2026-10-13-a), the host's action certified against its description along one chain of tokens; `world_model.lut` is the first model (the console, through externs), and `examples/hello.lut` the first program with an action. `print` is a library's, not core's (D-2026-10-12-al), which revises D8 of the archived plan. A library may offer more than the table; the core uses only the table.

**10.S14. What this chapter leaves out.** [decided D-2026-10-13-g] The rationale also treats the trace of a run, equality of consequence, observations as functors and classes of machines described statistically. They need a form of the record of a run that `spec 8` and the libraries decide; the interface of 10.S5 names none of them, so that adding them later changes a library and not the core (P16).

## Open

- O3: the opt-out of certification, and the world as an opaque, unique value, which 10.S4 and 10.S5 state as an interface and not as a representation.
- O1: the algebra of costs, on which the cost an assumed foreign algorithm carries rests (10.S12).
- O12: what identifies a memoized result, where the hash of an extern's file enters (10.S9).
````

### `06-certification.md`

````
# 6. Certification

Chapter 6 of the specification, draft 0, 2026-10-12. Sources: `docs/spec/05-static-semantics.md` §7 and `docs/spec/03-libraries.md` §4 at bd4537e; `docs/principles.md` L9 and L10 at 2b79c02; the decisions D-2026-10-11-f, D-2026-10-11-n, D-2026-10-12-h, -k, -m, -q, -r, -t, -y, -ag, -ak and -al; `src/luthier/testing.py`, `certify.py` and `cli.py`, read only. Written by Claude Opus 5.5, the session integrating the specification, as wave 2 was reshaped by D-2026-10-12-al: `Cost` is a library, and this chapter states certification over a cost type it takes as a parameter, fixing only what it asks of that type. It realizes L9 and L10, in Luthier where the kernel can say it (L14). How a test draws, counts and records its cases is spec 7; what the files hold and what an importer accepts is spec 12.

## §1 Notation

Notation shared by every chapter is `spec 1`. Here: `C` is a type of costs, the parameter of the chapter (§3), and `c`, `c′` are values of it. `≤` is the order of `C`, `0` its least element, `⊤` its greatest, `⊕` the composition of two costs along a path, and `lift : Bool -> C` the reading of a Boolean verdict as a cost. `X`, `Y` are domains: a subtype, a list of cases, or a distribution sampled. A *cutoff* is what a demand requires of a certificate (D-2026-10-12-h): a largest bound and a largest evidence cost, both values of `C`. `h` is the hash of a dependency cone (`spec 3.S34` gives the canonical form it is computed over).

## §2 What is certified

**6.S1. A law over a domain, never a name.** [implemented] The thing certified is a law of a name's type, applied to the values that law quantifies over, on some domain. A definition counts as certified when each law its type states has a passing entry; `check -v` summarizes the entries of a name, and that summary is not a state the name keeps once and for all. The obligations a type raises, and which of them are laws and which coercions, are `spec 4`.

**6.S2. Law, certifier, certificate.** [decided D-2026-10-12-k] The law states; the certifier is how evidence for it is obtained, and a law can have more than one: citing a theorem, running every case, running listed cases, sampling, or assuming. A certificate is the record of what one certifier established (§4). When a law quantifies over infinitely many values, no run reaches all of them: such a law is cited, sampled or assumed, and its certificate says which.

**6.S3. Three outcomes.** [implemented] A law run by `test` passes; fails, by a counterexample, by an error while evaluating a case, or by a generator giving a value outside its type; or is not run, when a parameter has no generator, no case could be drawn, the reduction ran out of fuel, or a hole without a value blocks it. A definition passes when all its laws pass, fails when one fails, and is not run otherwise. Only a pass certifies.

## §3 What certification asks of costs

**6.S4. Certification takes its cost type as a parameter.** [decided D-2026-10-12-al] The theory of this chapter is written over a type `C` and the operations of §1, not over a fixed `Cost`. A library of costs supplies models of `C`; which algebra it uses, how a sample's statistics become a cost and what its operations are called are decided when that library is implemented. This chapter fixes only what it uses.

**6.S5. Five operations and their laws.** [decided D-2026-10-12-am] Certification uses exactly these (the sixth law of `⊤` added by D-2026-10-13-g), and asks of them these laws, so that a library of costs is a model of them:

| operation | used for | laws |
|---|---|---|
| `≤` | comparing a certificate with a cutoff (§7) | a preorder |
| `0` | a check with no error and no doubt: exhaustive, proved | least element |
| `⊤` | a failed check, refused by every cutoff | greatest element, absorbing for `⊕`, and `⊤ ≤ 0` is false (D-2026-10-13-g; spec 5.S5) |
| `⊕` | composing bounds and evidence along a path (§6) | associative, unit `0`, monotone in each argument |
| `lift` | a law valued in `Bool` | `lift true = 0`, `lift false = ⊤` |

No subtraction, product or inverse is asked: nothing in certification takes evidence away (6.S13). Turning what a sample observed into a cost (L10.3) belongs to the library, with the shape D-2026-10-12-r gives it. Of the two algebras of D-2026-10-12-p, max and the plain sum satisfy the laws asked of `⊕`; the averaged forms with 1/n do not, since an average of averages is not associative, so a library that takes them needs another `⊕` along a path. That choice is the library's. The names D-2026-10-12-n listed as primitives (0, ∞, lift, exact) are the table's `0`, `⊤` and `lift`. The bound of a certificate and its evidence cost are both values of `C`; whether they should be two cost types is left to the library.

## §4 The certificate

**6.S6. What a certificate holds.** [decided D-2026-10-13-g] As a value of a record type `Certificate C`: the law; the domain it covered; the bound observed (for a law into `C`, the worst cost seen; for a Boolean law, `lift` of its verdict); the evidence, an evidence cost in `C` (D-2026-10-12-r) with the grade derived from it (6.S7); and the identity, the hash `h` of the cone with the binding of spec 7.S9. [implemented] Today an entry of `x.cert.json` (spec 12.S10) holds the law's label, its outcome, the mode and count it ran with, the generators and their fingerprints, the seed, the first cases, the time each law took, and `h`; the bound and the evidence cost are not recorded.

**6.S7. The grade is a view of domain and evidence.** [decided D-2026-10-12-r] The grade is computed, not stored apart. A proof or a run of every case gives evidence `0` over the whole domain. A run of listed cases gives `0` at those cases and `⊤` at every other value. A sample gives the cost the library converts its statistics to. An assumption gives the cost the demand assigns to assumptions (6.S10). A person reads the five names; the planner reads the costs. [decided D-2026-10-13-g] The correspondence of the older names (point, census of k, bounded, witnessed) to these five is a function of `lib/certification.lut` (6.S16), so that spec 1.S12 cites it; this settles the place D-2026-10-12-ag left open.

**6.S8. A certificate is identified by its cone and frozen.** [implemented] The hash covers the code of the cone in canonical form, the host code behind each extern it calls (the source files of the module's directory, or the installed package and its version) and the interpreter; any change to one of them makes the entry stale (spec 12.S11). An entry is kept per filling of the holes its cone depends on, up to four. [decided D-2026-10-13-g] A new check never edits an entry: it writes a new one, and both are kept, the latest in front (L10.4). Today the new entry replaces the old one with the same hash in the file, and the chain exists only in the history of the repository.

## §5 Certifiers that run nothing

**6.R1. Proved by citation.** [implemented] `cite name ref checked who` records a certificate of grade proved for the laws of `name`: `ref` must be a value of `Reference`, read from a `.bib` file (spec 12.R1), and `who` says who checked that the theorem cited matches the laws, `human`, `ai+human` or `none` (D-2026-10-11-f). It is allowed in user code. The certificate holds the reference and who checked; `test` runs no case for a cited name. In the language designed `cite` is a function of core with named arguments (spec 2.S21), and its syntax is O10.
Files: cite_proved.accept.lut, cite_not_reference.reject.lut.

**6.S9. Proved by delegation.** [decided D-2026-10-13-g] A host library's documented guarantee is cited as the theorem, with its hypotheses (a condition number, the library's version and the platform) carried by the certificate: LAPACK's backward-error bound for a solve, say. This is citation with a theorem outside Luthier, and adds no grade (L9.7).

**6.S10. Assumed.** [decided D-2026-10-12-t] Nothing is checked; the certificate records the assertion itself. For a Boolean law the assertion is that it holds, and the bound is `0`. For a law into `C` it is a formula of the inputs, and the bound is that formula's value at the input. The demand sets the evidence cost of assumptions, with no default, so a demand that names none refuses every assumed value. A formula that some source guarantees, cited with the conditions it needs, makes the certificate 6.S9 instead. [implemented] The laws of an `axiom` (spec 11.R3) are assumed: stated, never tested, and `check -v` says so (spec 4.S19).

## §6 Transport and composition

**6.S11. Along an identity.** [decided D-2026-10-11-f] Let B be certified on X with bound `c` and evidence `e`, and the identity of A and B certified on Y with distance `c′` and evidence `e′`. Then A is certified on the intersection of X and Y, with bound `c ⊕ c′`, evidence `e ⊕ e′`, and the weaker of the two grades; on nothing outside that intersection. When the identity law is valued in `Bool` (structural `==`, spec 4.R8), `c′` is `lift true = 0` and the certificate of B transports exactly; when it is valued in `C`, the distance observed is added. This is the only operation of §3 that transport uses. The example of L10 is a lookup table that agrees with the native definition at the points of a grid: the intersection, and so its certificate, is that grid.

**6.S12. Along a path, and sampled links.** [decided D-2026-10-12-q] A path of identities composes link by link with `⊕`. Two links sampled over one distribution compose by the union bound, their failure fractions and their δ summed; two links sampled from different distributions need a law that relates those distributions before they compose. A demand that refuses sampled paths says so by its evidence cutoff.

**6.S13. No evidence for free.** [decided D-2026-10-13-g] As a law of the theory of 6.S16: every operation on certificates is monotone, so a better grade, a smaller evidence cost or a wider domain comes only from a new check (L10.9). It is the reason 6.S5 asks `⊕` to be monotone and asks for nothing that subtracts.

## §7 The demand

**6.S14. Demanding a value demands its certificates.** [decided D-2026-10-11-n] Every name in the dependency cone of a demanded value must be certified, each certificate paid once through the memo. What no demand reaches needs none. `test` demands certificates without values, and `test` of a module demands every name it defines (D-2026-10-12-ad). There is no opt-out (D-2026-10-12-y): if any name of the cone lacks a certificate, or is provisional (spec 4.R5), the demand is refused, and `run`'s refusal is spec 12.S17.

**6.S15. A certificate serves a demand when it meets the cutoff.** [decided D-2026-10-12-h] The demand states the cutoff; the certificate meets it when its bound is `≤` the cutoff's bound and its evidence `≤` the cutoff's evidence, in the order of `C`. A certificate taken from the memo is compared with the demand that hits it, at the hit. A certificate issued for one cutoff serves every demand it meets. Writing a certificate is an action on Luthier's own state, idempotent and memoizable (D-2026-10-12-m).

## §8 Certification in Luthier

**6.S16. `lib/certification.lut`.** [decided D-2026-10-13-g] The theory of this chapter, written over a parameter `C`: the theory `CostAlgebra C` with the operations and laws of 6.S5; the record `Certificate C` of 6.S6; the function `grade` of 6.S7; `transport` of 6.S11 and `compose` of 6.S12; `serves` of 6.S15; and their laws, among them monotonicity (6.S13) and that `serves` is monotone in the cutoff. The file is not written. The host's `certify.py` and `testing.py` are its specimen, certified against it (L14.3), and each library of costs gives a model of `CostAlgebra`. Once its laws are written, L9 and L10 are read back from them (D-2026-10-12-ag).

## Open

- O1, the algebra of costs, now the library's (6.S5).
- O3, for 6.S14.
- O10, the syntax of citation (6.R1).
````
