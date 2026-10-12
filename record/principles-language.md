# The principles of the language: the record

The record of the organizers (G) and the principles of the language (L) of Luthier, one entry
each, written for anyone tracing where an idea came from and how its statement changed
(D-2026-10-12-d). It is the source of `docs/principles.md`, which `scripts/project_principles.py`
writes from it and which is not edited by hand; `docs/principles-for-readers.md` is written in
prose and cites these entries. The way of working, W1 to W15, is `docs/way-of-working.md`
(D-2026-10-12-b); the principles of the method, P1 to P15, are `record/principles.md`.

An entry starts at column 0 with its tag and its statement, which may continue on indented
lines; its fields follow, one per `Name:` at column 0, continued on indented lines. The fields:

- `Tier:` (G only) the guide, eureka, or good use, in his three tiers.
- `From:` (L only) the organizers it derives from, and the derivation. The derivation is the
  model's unless marked his.
- `Formulation:` the current text of the principle, the model's proposal unless a clause is marked
  "(his words)" or "(his correction)". It is the text the projection prints; it carries no draft
  marks, which are in `History:`.
- `Quote:` his words, verbatim, with where they were said.
- `Source:` where the idea was first said and where it was restated, in the grammar of the ideas
  pipeline (`written:`, `day:`, `note:`, `dialogue:` ids), the audios by file and minute, chats by
  date, commits by hash.
- `Status:` settled, proposed (the model's, awaiting his mark), candidate, retired; what is
  pending is named.
- `History:` what changed in which draft, with the draft's commit and who moved it.

Since draft 10 the entries carry the numbering of 2026-10-12: G1 theory and model, G2 cost, G3
the demand; L1 to L15 in his six topics. The table under Numbering maps the old tags to the
new; inside `Quote:`, `Source:` and `History:` a tag written before draft 10 is an old one, and
`record/decisions.md` keeps the old tags in its Kind lines until it is updated.

## The drafts of `docs/principles.md`

Before D-2026-10-12-d the file carried its own history in its header; it is here now, by draft.

| Draft | Date | Commit | What happened |
|---|---|---|---|
| 0 | 2026-10-10 | 6d9dbd3 | L1 to L17 and W1 to W13, each with who first said it and its source. |
| 1 | 2026-10-10 | 5769005 | L18, L19, L20 added; twenty L and fourteen W as peers. The header of drafts 2 to 9 cited d6a4ff5 for draft 1. |
| 2 | 2026-10-11 | cd24137 | The twenty L derived from his organizers, as he asked in `record/Lucianos ideas/principios organizadores.txt` ("un principio es un organizador y como su nombre lo indica es el primero"), following `record/plan-principles-generative-2026-10-11-decisions.md` (D1 to D8, taken as recommended on his instruction; his marks pending) and `record/organizing-principles-2026-10-11.md` (addenda 1 to 8). Three tiers: the guide G0, two eurekas G1 and G2, good use G3 and G4. His annotations at 2c18c41. |
| 3 | 2026-10-11 | c085ba4 (the record at f156aeb) | Two rounds of annotations incorporated (`record/answers-annotations-principles-2026-10-11.md`, his reply 18da042, `...-b.md`): L12 actions verified, L16 law of a binding, L20 theories, L15 functor, L21 transport, G4 decides, W15 new, terminology, open items. Terminology fixed: a *theory* is a type with laws, usually parameterized; a *model* is a value of a theory; a *module* is a file as a namespace today and a value by design; an *object* is the cycle of a type and its laws (`05 §3`). D-2026-10-11-f, -g. |
| 4 | 2026-10-11 | c7c6396 | Eight models read draft 3 for the contradictions that would hamper implementation (`record/IA/principles 2023 10 11/`, a8e28f0; synthesis `record/contradictions-ia-2026-10-11.md`, his marks 0d6932d). D-2026-10-11-m (the planner substitutes only along a certified equivalence) and -n (certification by default, opt-out in the demand). |
| 5 | 2026-10-11 | 5b1446c | Seven models read draft 4 with the same prompt (`record/IA/principles 2023 10 11 2/`, 4f4e208, 15fcaf7; synthesis `record/contradictions-ia-2026-10-11-b.md`); what the first five caught reworded: the planner's graph is weighted, not a class; a law into Cost returns a measure. |
| 6 | 2026-10-11 | 8809e20 | What Kimi and Perplexity showed still spoken in exact terms propagated: each node once per plan, the four layers of trust, "guarantee" per grade, effects outside Luthier audited. Three items waited for his mark: L14's gate, the holotype, the order of the organizers. |
| 7 | 2026-10-11 | 6a15cec, e8ba100, 9d1c435, cd314a4 | Four models asked to break L10, L19 and L14 with worked examples (`record/IA/principles round 3/`, d824b21; synthesis `record/contradictions-ia-2026-10-11-c.md`). All three broke; L10 and L19 repaired, L14 amended and then settled by his correction (a function with no laws is a theory's hole). Kimi's two holes and Claude's three added. |
| 8 | 2026-10-12 | 4f6beef | His observation on draft 7 (66f0bef): the eurekas were in the model's order and a third, objects as models of theories, was missing. D-2026-10-12-a: Luthier verifies models of theories; G2 widened, printed before G1, L20 moved under it. The P13 table not recounted. His annotations at bcdac41 (nine marks). |
| 9 | 2026-10-12 | 0636378, 120a49a | His nine marks applied (`record/answers-annotations-principles-2026-10-12.md` §5): holotype removed (settled), lift/exact/within named (G3), G4 retired (D-2026-10-12-c) and its content L22, L3 widened to the theory, L8, L11, L18 completed in his words, L20 absorbed into G2, L21 restated as graded transport (his mark pending). The W split into `docs/way-of-working.md` at 0db35c2 (D-2026-10-12-b). |
| record | 2026-10-12 | 72cc7be | D-2026-10-12-d: the entries below rewritten from draft 9 (120a49a) into fields, the draft marks moved into `History:`, nothing dropped; `docs/principles.md` becomes the projection. |
| 10 | 2026-10-12 | 72cc7be, 81c1794, 25f9c5e, b7a7e23 | Written by hand from the projection of 44df5a7 and his corrections (d5e81e3, e3fa339, 323bda0, 59ea8e9, 01ba854, 660b019, 792ac84): the L reordered in six topics and renumbered L1 to L15 on his marks on the reorder plan (14ea9f0): five merges, L6 new, L21 dissolved, L3 and L20 absorbed into G1; the organizers renumbered (G1 theory and model, G2 cost, G3 the demand). `--check` failed until the record caught up. |
| record | 2026-10-12 | this file | Step 1 of `record/plan-principles-draft-11-2026-10-12-execution.md`: the entries rewritten from draft 10 by `scripts/migrate_record_draft10.py` with the new numbering, the fields of the merged entries carried into the entry that absorbed them, G4 and the former L20 kept as (History:) paragraphs; the projection shows the From and Tier lines draft 10 had lost and no longer the "(was …)" in the headings, which the table below carries. |

The check of P13 (a principle is worth the decisions it guides), over the 56 entries of
`record/decisions.md` by the L and P named in their Kind lines (D5 of the generative plan, counted
at draft 2 and not recounted since):

| Organizer | Decisions guided |
|---|---|
| G0 the guide | 15 |
| G1 demand | 5 |
| G2 description | 8 |
| G3 cost | 1 (D-2026-10-10-g) |
| G4 expressive, retired in draft 9 | 4, none depending on it |

G3 guides one decision so far and is marked candidate, as D5 says; the section on how the
organizers depend on each other says why it is load-bearing anyway.

## Numbering

The tags of draft 10 against those of drafts 1 to 9 (his marks on the reorder plan, 14ea9f0).

| Draft 10 | Before | What happened |
|---|---|---|
| G0 | G0 | kept |
| G1 | G2 | theory and model, printed first since draft 8; the former L3 and L20 absorbed |
| G2 | G3 | cost, the second eureka on his note; lift, exact and within moved to L6 |
| G3 | G1 | the demand, printed third |
| retired | G4 | retired in draft 9 (D-2026-10-12-c); its content became L22, now in L14 |
| L1 | L1 | kept |
| L2 | L2 | kept |
| L3 | L4 | renumbered; "from a law" his correction |
| L4 | L8 | renumbered |
| L5 | L16, L21 | merged: equality has levels, with the identity clauses of L21 |
| L6 | new | how laws combine, the lift and the cutoff, from the former G3 |
| L7 | L5, L11, L21 | merged: a law characterizes, verified by one operation; identity is not the law |
| L8 | L15 | renumbered |
| L9 | L9, L18 | merged: a DAG of definitions without effects |
| L10 | L19, L13 | merged: the demand determines the computation and the types produced |
| L11 | L12 | renumbered and shortened |
| L12 | L17 | renumbered; statement in his words |
| L13 | L10 | renumbered; statement in his words |
| L14 | L14, L22, L11 (delegation), L21 (transport) | merged |
| L15 | L6, L7 | merged: the core is minimal and its programs are data |
| absorbed | L3 | into G1 (draft 10) |
| absorbed | L20 | into G1 (draft 9) |

## Terms

- A *structure* is a type in the kernel's language (`04`), built from four forms: a product, a
  value made of several named fields (a record, a tuple); a sum, a value that is one of several
  cases, each tagged (a variant, an enumeration, `Maybe`); a function type `A -> B`; and a
  recursive type, one defined in terms of itself (a list, a tree). Each form may hold the others.
- A *predicate* is a function into `Bool`. A *cost* is a function into `Cost`, the non-negative
  reals with infinity, 0 true and ∞ false.
- A *law* is a predicate or a cost, or a combination of laws that is again a predicate or a cost;
  how laws combine is stated under G2.
- A *theory* is a structure with its law.
- A *model* is an inhabitant of a theory: a value of its structure whose law is certified.
- A *function* is a value of a function type `A -> B`, in the standard sense. A function type with
  its law is a theory, and a function that satisfies it is a model of that theory.
- The *dependences* of a theory are the theories whose models its structure and law use
  (`Monoid A` depends on `Setoid A`; `VectorSpace K V` on `Field K`). A carrier is assumed to come
  with the models it names, `A` with its setoid, `K` with its field, so a theory reads them from
  the type (his note of 2026-10-12; today the libraries pass them as parameters). Every theory has
  dependences; a function type has at least the setoids of its carriers, since its law uses their
  equality.
- A *certificate* is the record that a law was checked, with its grade (proved, exhaustive, cases,
  sampled at a level, assumed); a proof is a certificate of grade proved. To *certify* is to
  produce one.
- *Evaluation* computes a function, and has no effect (L9). *Execution* is an action on the world
  (print, save). Writing a certificate into the store Luthier owns is an action on Luthier's own
  state, verified by reading the store back (L11); `test` is that action (L10).
- The *demand* is a request for a value from outside the program, an action, carrying the type and
  the tolerance it wants, the type possibly decorated: the value with its error, its derivative,
  its certificate. The *planner* is what chooses, among the models certified equivalent, the one
  that runs, and plans the decorated type the demand asks for.

Status of the terms: his list (D-2026-10-12-f); the names structure, cost and certificate are the
model's where he left a question mark, marked OK by him on 2026-10-12; *dependences* replaces the
model's "dependent theory" on his note (every theory is one, so the emphasis goes on what it
depends on); the reading of certification as an action on Luthier's own state is proposed, kept
by him on 2026-10-12 with the clause "never an action on the world" removed as obscuring; the
carrier coming with its setoid and its field is his note of the same day. *Object* (`05 §3`) is
not a term; see What is open.

(History: the Terms of draft 9, before his note of 2026-10-12 on dependences and on the carrier
coming with its models: His list (2026-10-12, `docs/principles_corr.md` at d5e81e3, D-2026-10-12-f),
in his order; where he left a question mark the name is the model's proposal and says so. - A
*structure* (proposed; his candidates structure, object, data) is a type in the kernel's language
(`04`): products, sums, function types and recursive types, built from each other. - A *predicate*
is a function into `Bool`. A *cost* (proposed) is a function into `Cost`, the non-negative reals
with infinity, 0 true and ∞ false (G3). - A *law* is a predicate or a cost over the symbols of a
structure; both are laws and coexist (G3). - A *theory* is a structure with its laws. - A *model* is
an inhabitant of a theory: a value of its structure whose laws are certified. - A *function* is a
value of a function type `A -> B`, in the standard sense (his correction). A function type with its
laws is a theory of one symbol, and a function that satisfies them is a model of it; this is the
common case in practice (D-2026-10-12-e), and a function has sense only in that context. - A
*certificate* (proposed; his "validation or proof") is the record that a law was checked, with its
grade (proved, exhaustive, cases, sampled at a level, assumed) and, for a cost, the worst value
seen; a proof is a certificate of grade proved. To *certify* is to produce one. - *Evaluation*
computes a value, or the value of a law, and has no effect (L18). *Execution* is an action on the
world (print, save). On his doubt, whether checking a law is an execution since it changes state
(proposed): checking the law is evaluation; recording that it was checked writes a certificate into
the store Luthier owns, with the memo, and that is an action, verified by reading the store back
(L12) and never an action on the world outside; `test` is that action (L19). - The *demand* is a
request for a value from outside the program, an action, carrying the type and the tolerance it
wants. The *planner* is what chooses, among the models certified equivalent, the one that runs. The
spec's *object* (`05 §3`, a strongly connected component of the dependency graph, the names a cycle
of laws joins) is not among his terms; in them it is a theory written in one cycle of names with its
models. Whether `05` renames it is open.)

## The organizers

The guide, then the two eurekas, then the demand. Renumbered on his note of 2026-10-12: G1 is
theory and model (G2 until draft 9), G2 is cost (G3 until draft 9), G3 is the demand (G1 until
draft 9); the record and `record/decisions.md` keep the old tags until the record is updated with
this mapping.

```
G0  Type theory is the guide.
Tier:       the guide
Formulation: A type is a proposition and a value its proof; a law is a proposition over terms, so it
            defines a mathematical object and a quotient, and inside the class the representative is
            free. Type theory guides what is declared. What governs execution is the demand (G3),
            read in the same theory: a demanded type is a judgment to inhabit, execution is the
            search for an inhabitant, and cost or execution time ranks the candidates (G2); where
            type theory normalizes a given term, Luthier searches for one.
Quote:      "Un principio es hott/Category theory/ type theory guidance. De ahi sale types as
            propositions y funcions as types y por ende functions defined as propositions, laws. De
            ahi sale que las laws definen objetos matematicos. y tambien que con una law tenes un
            cociente y por lo tanto valores intercambiables y por lo tanto optimizacion por tiempo y
            costo en memoria o por error." (note, fa3f972) "la guía es la te[o]ría de tipos" (audio
            09.19, 00:00)
Source:     record/Lucianos ideas/principios organizadores.txt (fa3f972); WhatsApp Ptt 2026-10-11 at
            09.19.36.md, 00:00
Status:     settled, marked OK by him on 2026-10-12
History:    draft 2 (cd24137): stated from his note and the audio, formulation proposed. draft 5
            (5b1446c): "free in the theory, where the law is exact; in a model, L10". draft 10
            (72cc7be, 81c1794, 25f9c5e, b7a7e23): statement and formulation kept; the organizers
            renumbered on his note of 2026-10-12 (G1 theory and model, G2 cost, G3 the demand).

G1  A type is a theory and its values are its models.
Tier:       eureka, the first (the trigger, audio 09.19, 00:00 to 00:14); G2 until draft 9, printed
            first since draft 8 (D-2026-10-12-a)
Formulation: If a type is a proposition, then a proposition can say that a structure follows the
            rules of a theory; so "this structure satisfies the laws of the theory" is said, in the
            language of types, as "it is of the type of the theory": it is a model of the theory,
            and Luthier verifies that it is. Types thereby carry a strong semantic meaning, and
            coding and testing are one act: to declare `m : T` is to declare the tests `m` will pass
            (G1). What type theory lacks: it knows a value by its term; Luthier knows it by the law
            it satisfies.
Quote:      "el disparador es darme cuenta de eso, que los tipos de funciones son las leyes que las
            definen. Esa fue mi eureka moment" (audio 09.19, 00:00 to 00:14) "Las leyes deben ser
            propiedades (matematicas o no) que determinen univocamente la funcion que estamos
            definiendo. Las funciones se definen a lo Russel. Y se testean empiricamente. Que una
            implementacion sea valor de un tipo de funcion siginfica que ya fue validada aunque sea
            una vez. Y la validacion de las funciones es progresiva" (note) "no ser a lo tarski
            (constructivo) sino a lo matematico (desde afuera, como un entomologo observa un bicho)"
            (chat, D-2026-10-11-d) "Un tercer momento eureka fue cuando me di cuenta que necesitaba
            los objetos ya que hay funciones que se testean mutuamente, o sea que 'la programacion
            basada en objetos' tiene una base matematica, solo que las clases (o interfases) serian
            las Teorias y los objetos serian los modelos de las teorias" (66f0bef) "que tal si en
            lugar de presentar Luthier como verificador de funciones lo presentamos como verificador
            de modelos de teorias? Al tomar elementos de CCC como estructuras donde se escriben las
            leyes, las teorias y modelos pasarian a ser los elementos de Luthier" (chat, 2026-10-12,
            D-2026-10-12-a) "me parece que es muy difcil encontrar un caso en que verifiques una
            funcion relevante aislada, siempre viene con un tipo asociado al menos, y siempre tiene
            la igualdad asociada tambien... Y las igualdades vienen asociadas con funciones tambien"
            (chat, 2026-10-12, D-2026-10-12-e) "Si, lo comun es extender una teoria con un caso. Lo
            que pasa es que yo sospecho que son funciones porque no nos tomamos el trabajo de pensar
            cual es su inversa o a que teoria pertenecen. una funcion sola, aislada no tendria
            sentido, tiene sentido en un contexto, a eso voy." (chat, 2026-10-12, D-2026-10-12-e)
            "Pensa un poco que es una funcion. Una funcion tiene una definicion estandard."
            (docs/principles_corr.md, d5e81e3)
Source:     WhatsApp Ptt 2026-10-11 at 09.19.36.md, 00:00 to 00:14; record/Lucianos ideas/
            principios organizadores.txt; the composition of invariances as "la parte Tarski",
            WhatsApp Ptt 2026-10-11 at 08.58.46.md, 32:01 to 34:07; his observation on draft 7,
            66f0bef; chat 2026-10-12, D-2026-10-12-a; his words on laws and theories,
            record/answers-annotations-principles-2026-10-12.md §5 (bcdac41); the function as the
            common case, chat 2026-10-12 (D-2026-10-12-e), after a survey of the .lut files (58
            certified functions, each with an imported equality; 12 models; 341 definitions without
            a law); his annotation on the projection, d5e81e3 (§6 of the answers)
Status:     settled; this wording is his note of 2026-10-12 put in order; the long form in the
            record
History:    draft 2 (cd24137): "a function is known by description", the second eureka, printed
            after G1. drafts 3 to 8: a holotype paragraph, his metaphor for the representative of a
            class, later recognized as L10's and removed. draft 8 (4f6beef): widened to theories and
            models on his observation (66f0bef) and D-2026-10-12-a; printed first, in his order; L20
            moved under it; what model theory lacks added; the derivations that follow directly
            named. draft 9 (0636378): the holotype removed, settled; his words put in its place (a
            law an implementation of itself, a theory an object classifier made of laws). record
            (2026-10-12), D-2026-10-12-e and his annotation d5e81e3: the common case is a theory of
            one symbol whose model is a function in the standard sense; an isolated function has
            sense only in a context. draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): renumbered from
            G2 on his note of 2026-10-12; the formulation is his note put in order, the long form of
            draft 9 kept below in this History; the former L3 (defining a model defines its test)
            and L20 (a function is declared in a theory) absorbed, their fields below. the long form
            of G2 at draft 9: a theory is a signature with its laws, written in the kernel's
            language (`04`, a bicartesian closed category: this is where G0 is used); a model is a
            value of a theory, and declaring `m : T` records the obligation to satisfy the laws of
            `T`; a law relates several symbols (`inverse x * x = unit`), which no single function
            can carry, so the unit declared is the theory and the unit valued is the model. The
            common case in practice is not the smallest theory but one that adds a single symbol, a
            function type with its laws, to structures already modelled with their equality: every
            law is an equality, and the equality of a carrier is itself a function with laws
            (reflexive, symmetric, transitive, or those of a distance) that the new symbol must
            respect; the model of such a theory is a function in the standard sense, and the eureka
            of 09.19 is this case, where he saw it first. (His words, D-2026-10-12-e) An isolated
            function has no sense; it has sense in a context, and what looks like a lone function is
            one whose inverse and whose theory nobody took the trouble to find. Luthier verifies
            models of theories; what it verifies about a function is that it is a model of its
            type's laws. The function: the laws are what is known of a function, and the
            implementation, native or extern, is the specimen under observation. A description is
            derived by composition of the laws of the parts when such a law exists, and observed
            otherwise; laws accumulate, and a set of laws that determines the function up to its
            equality is the limit a definition may reach, not what it must reach (D-2026-10-11-d).
            (His words) A law is written as an implementation of itself, a program that returns its
            Bool or Cost; a theory is written as an object classifier made of laws, the map that
            sends a structure over the signature to the cost of its being a model, which is where G3
            enters G2; the implementation of a model is then verified against the laws. What type
            theory lacks: it knows a function by acquaintance, as its term. What model theory lacks:
            a grade and a demand; a model of Luthier satisfies its theory up to a cost, certified at
            a grade and progressively (G3), and is chosen for execution by a demand (G1); naming it
            "model" must not promise exactness. What follows from G2 as its definition rather than
            by derivation: L20 (a function is declared in a theory and is universal over its
            models), the object of `05 §3` (the names a cycle of laws joins), D-2026-10-07-e (no
            loose functions: a definition at a bare exponential is not a defined type) and
            D-2026-10-11-j (a carrier with two models is two types); and three L read in its terms:
            L10 is many models of one theory, interchangeable in the quotient; L21 is the difference
            between two models being identified and both satisfying the theory; L14's extern is a
            model whose carrier is foreign. The precedent in programming is algebraic specification,
            the module systems of ML and the lawful type classes of Haskell, where the mechanism
            exists without being the organizing idea (references to be checked before they are
            cited). (absorbed L3) L3 Defining a model defines its test. From: G2 directly: the
            eureka of 09.19 in its 2022 form Formulation: declaring a model of a theory, `m : T`,
            declares the tests it will be run on, so definition and verification are one act; a
            function type with its laws is the one-symbol case, and its model a function. Source:
            Luciano, 2022-08-03 (written:2022-08-03_haskell:declarar-funcion-es-declarar-su-test)
            Status: settled (the widening is his mark) History: draft 0 (6d9dbd3): stated as
            "defining a function defines its test". draft 9 (0636378), his mark: widened to the
            theory. (absorbed L20) L20 A function is declared in a theory and is universal over its
            models. From: G2, of which it is the definition rather than a consequence: a function
            belongs to the theory its laws are stated in, and a model is where it runs; before draft
            8 from G0 (a theory is a type, a model its inhabitant) and G1 ("lo declarativo pasa a
            ser todo lo universal posible"; instantiated on demand) Formulation: a function belongs
            to a theory (Real, Field, LinearAlgebra) and takes its model as its first, often
            implicit, argument, so it is written once for every model; the model is named by the
            type of the argument (D-2026-10-11-j) and can be passed explicitly. A theory over a
            model of another theory is a theory. Every type belongs to a theory; the concrete types
            (products, sums, exponentials, `data`) belong to the kernel's, whose laws are the β and
            η rules and the recursion principle, stated in `lib/kernel_laws.lut`. Operators are
            resolved by the type, the type naming its model; a carrier with two models is two types
            (D-2026-10-11-j). Modules are values by design, files today: a parametrized module is a
            function from models to definitions, applicative because definitions have no effects
            (L18), instantiated on demand with the parameter threaded down from the action. A
            specialization is one more representative of the law's class (L10), valid on a subtype,
            certified against the same law; where representations differ, the orchestrator inserts
            bridges by cost, coherent up to the law, carrying their error, visible in the plan; a
            specialization and a bridge each enter the planner's graph by an identity certificate
            with its distance (L10, D-2026-10-11-m). The conditions on bridges are the model's,
            accepted. Quote: "el codigo seria, en principio universal a los valores de funciones que
            cumplan las leyes requeridas" (chat, 2026-10-10) "no entiendo porque hacerlo un
            principio. Surge solo" (bcdac41) Source: Luciano, 2026-10-10 (chat; WhatsApp Ptt
            2026-10-10 at 17.00.40.md; WhatsApp Ptt 2026-10-10 at 17.25.23.md, 00:00 to 04:25;
            D-2026-10-10-g) Status: absorbed into G2 on his mark (draft 9): the clause on
            specializations and bridges belongs to L10 and modules as values to the spec (`03`); the
            tag stays for the record's citations and the text stays until the spec takes its parts
            History: draft 1 (5769005): stated as "code is universal over the models of its theory".
            draft 3 (c085ba4): reworded after his annotation (theories). draft 4 (c7c6396): the
            model named by the type of the argument (D-2026-10-11-j). draft 5 (5b1446c):
            specializations and bridges enter by identity certificates. third and fourth rounds
            (9395268, 55da213): every type belongs to a theory; the kernel's theory in
            `lib/kernel_laws.lut`. draft 8 (4f6beef): moved under G2 as its definition. draft 9
            (0636378), his mark: absorbed into G2.

G2  Laws are valued in cost: one logic, extended to the non-negative reals.
Tier:       the second eureka on his note of 2026-10-12; good use until draft 9, when it was G3
Formulation: Not every theory is easily described by Booleans; many are represented better by costs;
            and since object classifiers exist that extend logic to the non-negative reals, the
            composition of errors in numerical libraries can be attacked with this one unified
            logic. How laws combine and how a predicate lifts to a cost is L6; how a law is
            verified, L7; what a run teaches is kept.
Quote:      "queremos que Luthier use Bayes como guia tambien. Esto implica que las leyes no sean
            predicativos a un bool sino a un costo real positivo. Esta parte es la menos
            desarrollada ... Usar un object classifier de Lavwere seria el marco unificador. Y usar
            estadistica bayesiana para componerlo" (note) "El problema de la teoria de tipos es que
            funciona para enteros y deja de funcionar para float y para linear algebra o
            estadistica. Ahi la teoria de tipos booleana falla y si queres ser estricto o expresivo,
            necesitas otra cosa. De ahi el [0, +inf)" (el problema de los floating point.txt,
            5cc41fa) "cuando vos corres un programa aprendés algo y eso que aprendés queda en algún
            lado ... es como un deseo más que un principio" (audio 08.58, 05:47 to 06:08) "no podes
            promover booleans a cost a troche y moche" (bcdac41) "luego vamos a analizar la parte
            mas dificil es la extencion de logica booleana a Lawvere/bayesiana, otro
            motivador/Eureka" (chat, 2026-10-12)
Source:     record/Lucianos ideas/principios organizadores.txt; record/Lucianos ideas/el problema de
            los floating point.txt (5cc41fa); WhatsApp Ptt 2026-10-11 at 08.58.46.md, 05:47 to
            06:08; his annotation on draft 8, bcdac41; the lift, exact and within,
            record/answers-annotations-principles-2026-10-12.md §4
Status:     the second eureka on his note of 2026-10-12 (candidate by the P13 count, one decision
            guided so far); the algebra of costs open (`11`), the analysis he announced pending
History:    draft 2 (cd24137): stated, good use. draft 9 (0636378): on his mark, Bool and Cost
            coexist, the lift explicit and named, the cutoff only in the demand. draft 10 (72cc7be,
            81c1794, 25f9c5e, b7a7e23): renumbered from G3 on his note of 2026-10-12 and named the
            second eureka; lift, exact and within moved to the new L6; the formulation rewritten in
            his words.

G3  The demand defines what is computed.
Tier:       the executive face; an eureka until draft 9, when it was G1; printed third on his
            renumbering of 2026-10-12
Formulation: The declarative face states what is known, universal and minimally processed; the
            executive face is a demand from outside, and the demanded type fixes the path, the types
            and the tolerances actually produced. What type theory lacks: an executive face; there,
            computation is the normalization of a given term, with no demand.
Quote:      "la demanda de un valor por el mundo externo me define todos los tipos necesarios para
            obtener eso" (audio 09.19, 00:24) "la compilacion se dispara por la demanda externa (es
            decir un print o un valor que sale al mundo), y la demanda determina el tipo que quiere
            el print, y eso determinan 1) el camino que efectivamente se computa y los tipos que
            efectivamente se computan" (note) "la clara separacion entre lo declarativo y lo
            ejecutivo. Esto dio lugar a la idea de que lo ejecutivo se da por la demanda. Y lo
            declarativo pasa a ser todo lo universal posible, minimamente procesado" (note, 1c7a284)
            "lo que se sabe, que es un poco como la idea del prior" (audio 08.58, 08:59)
Source:     WhatsApp Ptt 2026-10-11 at 09.19.36.md, 00:24; record/Lucianos ideas/principios
            organizadores.txt; its root, 1c7a284; WhatsApp Ptt 2026-10-11 at 08.58.46.md, 08:59
Status:     settled; printed third on his renumbering; whether it is an eureka of its own or the
            executive clause of the guide (G0) is his to say
History:    draft 2 (cd24137): stated, printed as the first eureka. draft 8 (4f6beef): printed
            second, in his order. draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): renumbered from G1
            on his note of 2026-10-12, printed third.
```

(History: the introduction of draft 9: Three tiers, in his words (`record/audios/WhatsApp Ptt
2026-10-11 at 09.19.36.md`, 00:00 to 00:53): the guide, two eureka moments, and after them
"principios de buen uso".)

(History: G4, retired in draft 9 and no longer projected since draft 10: G4 Expressive over
restrictive; it decides between designs. Retired. Tier: good use, retired (draft 9, D-2026-10-12-c);
the tag stays so that the record's citations resolve Formulation: retired. What he meant by it is
concrete and is a rule, L22 (a non-Luthier way is allowed inside a named world). "The law that makes
two ways equivalent" is L21; P5 (a free choice is a legitimate principle) stays in
`record/principles.md`. The decisions it was named for stand without it: `:=` once and `<-` for
rebinding with default arguments (D-2026-10-11-c), `if` without `else` as a guarded value
(D-2026-10-11-b), many paths expressible (L10), accumulating laws rather than required
characterization (D-2026-10-11-d): each stands on L10, G0 or his own decision, and none needed the
tie-breaker. Quote: "Luthier debe ser expresivo mas que restrictivo: si hay mas de una forma de
hacer las cosas, todas deberian poder ser expresadas en Luthier" (note) "me da que es una
declaracion de buenas intenciones nomas" (bcdac41) Source: record/Lucianos ideas/principios
organizadores.txt; his annotation on draft 8, bcdac41;
record/answers-annotations-principles-2026-10-12.md §5 (G4) Status: retired (D-2026-10-12-c),
reversible by him in one line History: draft 2 (cd24137): stated from his note, the tie-breaker
between designs. draft 3 (c085ba4): "it decides between designs" added. drafts 2 to 8: cited by
D-2026-10-11-b, -c, -k, -m, -n in their Kind lines; generated no L. draft 9 (0636378, 120a49a):
retired on his doubt and the model's recommendation; its content became L22.)

(History: the section "How the organizers depend on each other", proposed (D8 of the generative
plan), projected until draft 9 and dropped from the projection in draft 10; in the old numbering:
*Proposed* (D8 of the generative plan). 1. G0's quotient needs G1 and G3 where the carrier carries a
distance: there two implementations are interchangeable only up to a distance and below the
tolerance the demanded type carries. On decidable carriers the exact quotient is correct and the
kernel proceeds without G3; "optimización por error" has no meaning there and needs none. The
interface that lets G3 arrive without a rewrite: every law returns a `Cost`, and `Bool` is the
two-valued case, the type of the result saying which (`11` §2, L21). A law into `Cost` returns a
measure; the proposition is cost ≤ ε with ε the demand's, so G0's "a law is a proposition" holds
once the tolerance is supplied. Until G3's algebra exists the application runs on this Boolean
interim: laws of the form d(f x, g x) ≤ tol with tol a parameter (L17), no composition of tolerances
along a chain, no run database. 2. G2's inhabitance needs G3: "validada aunque sea una vez" gives
the certificate of a : A a grade, which is sound only if truth is graded. The judgment itself stays
one and structural; the grade is its evidence (L2, `11` §4). 3. G1's planner is G0's proof search
with G3's cost: it searches for an inhabitant of the demanded type and ranks candidates by cost. So
G3, the least developed, is load-bearing for G0 and G2 over carriers with a distance, whatever the
P13 count says today; over decidable carriers the Boolean kernel stands on its own. (History: items
1 and 2 were extended in draft 4, c7c6396, with the decidable case and the judgment staying one, and
in draft 5, 5b1446c, with the law as a measure.))

## The principles of the language

Fifteen L in six topics, from the most general to the most particular, renumbered on 2026-10-12
(`record/plan-principles-reorder-2026-10-12.md`, his marks 14ea9f0); each heading names the former
numbers it joins, and the record keeps the map. Five merges (L5+L11, L9+L18, L19+L13, L14+L22, L6+L7
by the former numbers), one new L on how laws combine, the former L21 dissolved into the new L5, L7
and L14, the former L3 and L20 absorbed into G1. Formulations are joined, not reworded, except where
his note asked.

### 1. What the language is for

```
L1  Luthier expresses the invariances of the disciplines.
From:       G1 (what is known of a thing is its description; "la idea de luthier es ayudar a
            descubrir las invariantes de los calculos", note), with P14 (a type is a concept)
Formulation: What moves the language: a species mates within itself, electrons are fermions, a
            probability integrates to one. A definition states the invariances that determine a
            concept, and the language exists so that stating them is natural.
Quote:      "la idea de luthier es ayudar a descubrir las invariantes de los calculos" (note)
Source:     Luciano, 2026-05-29 (dialogue:20260529T1400:expresar-invarianzas-de-disciplinas)
Status:     settled
History:    draft 0 (6d9dbd3): stated. draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): number kept;
            first of the six topics.
```

### 2. Types, theories and models: the declarative face

```
L2  A type is a proposition, and membership is a guarantee.
From:       G0 directly; the second clause is the step to G1
Formulation: Belonging to a type asserts the propositions, laws included, that the value satisfies;
            function types carry their laws the same way. `a : A` is one judgment, structural and
            decidable for the kernel's types; it asserts the structural proposition outright and the
            laws through the certificate, at the grade the certificate has, so "guarantee" means
            what the grade says: proved or exhaustive, a guarantee; sampled, evidence at a level;
            assumed, a hole that says so. What a law adds is evidence, and the certificate of the
            law carries its grade (proved, exhaustive, cases, sampled, assumed) and, for a law into
            `Cost`, the worst cost seen (`11` §4). The guarantee is what the certificate says and no
            more, and what leaves the program carries one (L10, D-2026-10-11-n).
Source:     Luciano, 2022-08-03 (written:2022-08-03_haskell:proposicion-que-cada-tipo-cumple);
            restated 2026-05-26 (day:2026-05-26:tipos-como-conceptos-y-proposiciones)
Status:     settled
History:    draft 1 (5769005): stated. draft 4 (c7c6396): one judgment, structural; the certificate
            carries the grade and the worst cost; what leaves the program carries a certificate
            (D-2026-10-11-n). draft 6 (8809e20): what "guarantee" means at each grade. draft 10
            (72cc7be, 81c1794, 25f9c5e, b7a7e23): number kept.

L3  The certified subtype from a law is the fundamental construction pattern.
From:       G0 (a law is a proposition; its subtype is the type of its proofs) with G1 (verified,
            not constructed)
Formulation: From a material type and a law, a predicate or a cost with its tolerance, come the
            certified type, its only constructor and the forgetful projection; the same pattern
            builds values, functions and programs. A law gives the three at once: the type, the
            constructor with Maybe, the membership function. Where the law is into `Cost`, the
            constructor takes the tolerance as a parameter (L12) and the certificate records the
            tolerance it was checked at, so a stricter demand asks for a new check (`11` §4). Types
            are verified before they are constructed: Luthier starts from types by verification, and
            types by construction may come in later.
Source:     Luciano, 2022-08-03 (written:2022-08-03_haskell:subtipos-con-predicado); named
            fundamental 2026-09-29 (record/distillation/2026-10-09_find_principles_v2_claude-code_
            opus.md, C3); the three things and the scope 2026-10-10 (WhatsApp Ptt 2026-10-10 at
            10.12.21.md, 05:24 to 08:10)
Status:     settled. "From a law" is his correction of 2026-10-12
History:    draft 1 (5769005): stated. draft 4 (c7c6396): the tolerance a parameter of the
            constructor, recorded in the certificate. draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23):
            renumbered from L4; "from a law" is his correction of 2026-10-12.

L4  Declare, then define, then inhabit.
From:       G0 (a hole is a hypothesis of the context) with G3 (nothing is produced until demanded)
Formulation: A declaration without a body is a first-class hole: at once axiom, program input,
            external function, pending definition and dead code; nothing executes until it is
            defined, and no value inhabits an undefined type; an axiom is not a value but a law with
            grade `assumed`, so it does not inhabit. To the type checker the five are one, and the
            elaborated form records which it is, since the demand treats them differently: an input
            asks for a value, an external calls the host, a pending definition is an error, an axiom
            is a law with grade `assumed`, reasoned with and never run (an item for the spec;
            `assumed` has one meaning, the grade). `extern` is the operation that inhabits a hole
            with a body in another language, naming the language; a theoretical module (types,
            functions, laws, no values) is a module of holes. (His words) A declared name is assumed
            to have its declared type, and its use where that type is incompatible is an error (`05`
            R1, the checker).
Source:     Luciano, 2026-05-29 (dialogue:20260529T1400:tipos-no-definidos-y-forward-reference); the
            hole named 2026-09-29; `external` and the theoretical module 2026-10-10 (WhatsApp Ptt
            2026-10-10 at 17.41.53.md; WhatsApp Ptt 2026-10-10 at 17.25.23.md, 00:00 to 00:40); his
            annotation on draft 8, bcdac41
Status:     settled
History:    draft 0 (6d9dbd3): stated. draft 4 (c7c6396): the elaborated form records which of the
            five it is. draft 5 (5b1446c): `assumed` has one meaning. draft 6 (8809e20): an axiom is
            not a value. draft 9 (0636378): his words on a declared name's type. draft 10 (72cc7be,
            81c1794, 25f9c5e, b7a7e23): renumbered from L8.

L5  Equality has levels, belongs to the object, and is a law that composes.
From:       G0 (the identity type and its levels) with G2 (under cost, the identity proposition
            acquires a distance); the identity clauses from G1 (the specimen can be recognized as
            the same specimen, or described)
Formulation: Definition (`:=`), the identity proposition (`=`), decidable equality (`==`) and
            definitional equality by reduction (`≡`) are different things, and each object carries
            the observational equality that fits it. (His annotation) The binding acts are two, `:=`
            once and `<-` rebinding, and they share one law: after the act the name equals the term
            in the equality its type has, structural `==` where it exists (`05` R8), observational
            otherwise, a distance under G2; after `:=` for all time, after `<-` until the next `<-`
            (`05` R12). In the kernel the binding is exact: the name denotes the term, and reduction
            does not depend on a tolerance; the distance enters when the planner realizes the term
            by another representative, which it does only along a certified equivalence carrying its
            distance (L13, D-2026-10-11-m). The identity law between two specimens, with its
            distance, is what admits a second implementation into the class the planner moves in
            (L13, D-2026-10-11-m); the agreement test of W5 between native and extern is this law,
            and the reference formula of a law evaluated over `Rational` is one more specimen, with
            grade exact, checked by the same law. Identity is a law, so it composes as HoTT composes
            paths: reflexive, symmetric, transitive; under cost the composed path costs the sum of
            its links and holds at the weakest of their grades, and a sampled link holds only on the
            inputs its samples cover, so the composition holds on the intersection of the domains
            certified (his note of 2026-10-12 on the plan; what L13 states for the planner's paths).
Quote:      (L16) "luego de <- lh == rh, de hecho creo que es la ley de <-" (reply, 18da042) (L21,
            the identity clauses) "verificar bit a bit que sea igual ... por lo menos sabés que no
            cambia la implementación" (audio 08.58, 09:20 to 13:19); the statistical kind for
            "prueba científica" (same)
Source:     (L16) Luciano, 2026-05-30 (day:2026-05-30:niveles-de-equivalencia); the law of a binding
            2026-10-11 (reply, 18da042) (L21, the identity clauses) Luciano, 2026-10-11 (WhatsApp
            Ptt 2026-10-11 at 08.58.46.md, 09:20 to 13:19); his annotation on draft 2 (2c18c41); his
            annotation on draft 8 (bcdac41)
Status:     settled. The identity clauses come from the former L21 (candidate); the composition is
            his note put in words, proposed
History:    (L16) draft 0 (6d9dbd3): stated. draft 3 (c085ba4), his annotation: the law of a
            binding. draft 4 (c7c6396): the kernel's binding is exact; the distance enters with the
            planner. (L21, the identity clauses) draft 1 (5769005): proposed, candidate. draft 3
            (c085ba4), his annotation: the certificate of the law travels by the certificate of
            identity. draft 4 (c7c6396), D-2026-10-11-m: the identity law admits a second
            implementation into the planner's class. draft 7 (9d1c435, cd314a4): two clauses from
            Kimi and Claude on when transport fails. draft 9 (0636378), his correction: the two
            clauses replaced by graded transport on X ∩ Y, the counterexamples following from it.
            draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): renumbered from L16; the identity clauses
            of the former L21 joined; the composition of identities as paths added from his note of
            2026-10-12 on the reorder plan, proposed.
```

### 3. Laws and their verification

```
L6  Laws combine, and a predicate lifts to a cost.
From:       G2 directly (lift, exact and within were named under it on his mark, draft 9) with G3
            (the cutoff lives in the demand)
Formulation: A law is a predicate or a cost. Predicates combine by and, or, then, and by a
            quantifier over a carrier, and the result is a predicate; costs combine by sum, max and
            weighted sum, and the result is a cost; a combination that mixes the two is a cost, each
            predicate lifted. The lift is explicit and named: `lift : Bool -> Cost` sends true to 0
            and false to ∞, `exact : Cost -> Bool` is c == 0, both homomorphisms with `exact ∘ lift
            = id`, so `Bool` is a retract of `Cost`, not a subtype, and the planner inserts the lift
            as a bridge of cost zero. The cutoff `within ε : Cost -> Bool` lives only in the demand,
            since it does not compose (two links within ε are within 2ε). `&`, the only join the
            libraries use today, is the Boolean and. The law of a theory is one law, so its
            certificate is one certificate, and its grade is composed from the grades of the parts:
            with `&`, the weakest; with a sum of costs, the costs summed, each at its grade
            (proposed, on his note on Terms).
Source:     his note of 2026-10-12 on the reorder plan (14ea9f0)
Status:     proposed on his note of 2026-10-12 on the plan ("faltan las leyes de los costos y de los
            predicates y cómo se lift a costos"); the text is the record's G3 (lift, exact, within,
            his to rename) and the paragraph that stood in G2; the composed grade from the former
            L11
History:    draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): new, on his note of 2026-10-12 on the
            plan ("faltan las leyes de los costos y de los predicates y cómo se lift a costos"); the
            text is the record's G3 of draft 9 (lift, exact, within) and the paragraph that stood in
            G2; the composed grade from the former L11.

L7  A law characterizes; it is verified by one operation, exact or statistical; and the certificate
    of identity is not the certificate of the law.
From:       G0 (a law defines the object) and G1 (a law that transcribes the specimen is
            acquaintance, not description; observation is how a description is verified) with G2
            (the grade is the uncertainty of the cost); extends P10 (the mathematical object that
            best represents a concept is the invariant of its type)
Formulation: A law states a mathematical property of an operation; a second implementation checked
            against the first is consistency, and the native definition is one more model certified
            against the law. A law over several functions is tested on the values actually computed,
            as a puzzle whose pieces must fit; the cases to test are chosen by the law, its arity
            (three elements for associativity) and the distribution sampled (L7), never every path.
            Laws accumulate, and a law need not determine the operation; when the laws do determine
            it up to the presentation's equality, that is the limit (D-2026-10-11-d). The generators
            are the model's addition. What is known by a theorem is cited, what can be enumerated is
            checked exhaustively, what has chosen cases is checked on them, what can only be sampled
            is checked statistically, and the grade of the evidence (proved, exhaustive, cases,
            sampled at a level, assumed) travels with the value in a certificate hashed over its
            dependency cone; the line is the method, since associativity over `Int` is computable
            and cannot be checked by running. The grade of a sampled certificate depends on the
            distribution sampled, not only on the number of samples, because errors concentrate at
            the edges (the model's correction, from the practice of property-based testing).
            Checking that an implementation gives the same bits as before, with the same seed,
            certifies that the implementation has not changed; checking it against its laws, by
            chosen or sampled cases, certifies the description. Both are kept, apart, and the
            certificate of the law travels by the certificate of identity (his annotation): exactly
            where the identity is boolean (`==` structural, `05` R8: integers, decidable types, the
            same implementation rerun), and with the observed distance added where it is a cost
            (G2), since two implementations over floats are almost never bit-identical. The type of
            the identity law's result says which (`Bool` or `Cost`).
Quote:      (L5) "La idea en realidad es buscar el objeto matematico que mejor lo represente y
            decirlo" (chat, 2026-10-05) (L11) "verificacion externa por teoremas o por delegacion
            (creo en Lapack)" (bcdac41) (L21, the distinction identity/law) "verificar bit a bit que
            sea igual ... por lo menos sabés que no cambia la implementación" (audio 08.58, 09:20 to
            13:19); the statistical kind for "prueba científica" (same)
Source:     (L5) Luciano, 2026-10-05 (chat:52d3e68e:2760); the puzzle 2026-10-10 (WhatsApp Ptt
            2026-10-10 at 10.12.21.md, 11:38 to 18:20) (L11) Luciano, 2022-08-03 and 2023-02-22
            (written:2023-02-22_tapp-wish-list:untested-a- tested); the grades by samples 2026-10-10
            (WhatsApp Ptt 2026-10-10 at 11.11.22.md, 03:02 to 04:12); his annotation on draft 8,
            bcdac41 (L21, the distinction identity/law) Luciano, 2026-10-11 (WhatsApp Ptt 2026-10-11
            at 08.58.46.md, 09:20 to 13:19); his annotation on draft 2 (2c18c41); his annotation on
            draft 8 (bcdac41)
Status:     settled. The distinction identity/law is from the former L21
History:    (L5) draft 1 (5769005): stated. draft 3 (c085ba4), on D-2026-10-11-d: laws accumulate
            and need not determine the operation. (L11) draft 0 (6d9dbd3): stated. draft 4
            (c7c6396): the four methods and the grade in the certificate; the dependence on the
            distribution. draft 9 (0636378), on his mark: delegation as citation of the host's
            guarantee. readers' draft 0 (afdd7c7): his correction adds the library as a source of
            proof. (L21, the distinction identity/law) draft 1 (5769005): proposed, candidate. draft
            3 (c085ba4), his annotation: the certificate of the law travels by the certificate of
            identity. draft 4 (c7c6396), D-2026-10-11-m: the identity law admits a second
            implementation into the planner's class. draft 7 (9d1c435, cd314a4): two clauses from
            Kimi and Claude on when transport fails. draft 9 (0636378), his correction: the two
            clauses replaced by graded transport on X ∩ Y, the counterexamples following from it.
            draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): the former L5 and L11 merged and
            renumbered; the distinction identity/law of the former L21 joined; delegation as
            citation moved to L14.

L8  The ideal world is realized with a guarantee.
From:       G2 directly: the realization's distance to the ideal law is the law's value, and the
            tolerance is the demand's (G3)
Formulation: Code is written over ideal objects (Real) and realized by concrete ones (Float64); the
            realization's laws hold within a stated tolerance, and the error of each step is itself
            a law rather than a false claim of exactness. (His reading) Rounding `Real -> Float64`
            is a functor in Lawvere's sense, and each law of `Real` is projected onto `Float64` with
            its cost; it is not a homomorphism, and the exact map is the inclusion the other way.
            (Correction proposed, his mark pending) Rounding does not expand distances by at most a
            constant: two reals astride a rounding boundary land one ulp apart at any distance, so
            no multiplicative constant exists; rounding is non-expansive up to an additive defect of
            about ε|x|, and for subtraction and division the sensitivity is per input, the condition
            number (`11` §7). The functor reading stands with "non-expansive plus an additive term",
            and the cost algebra needs both parts: a multiplicative one where a Lipschitz constant
            exists and an additive one where rounding enters (`11` §5, open).
Quote:      "un functor que va de Real--> Float64 y que ahi vemos algunas propiedades de Real
            proyectadas en Float" (annotation on draft 2, 2c18c41)
Source:     Luciano, 2026-05-29; the floats note of 2026-10-11 (5cc41fa); the functor 2026-10-11
            (annotation on draft 2, 2c18c41)
Status:     settled in its statement; the correction on rounding is proposed, his mark pending
History:    draft 0 (6d9dbd3): stated. draft 3 (c085ba4), his annotation: rounding as a functor.
            draft 4 (c7c6396): the correction on the additive defect, proposed. draft 10 (72cc7be,
            81c1794, 25f9c5e, b7a7e23): renumbered from L15.
```

### 4. Programs and their execution: the executive face

```
L9  A program is a DAG of definitions without effects, and statements commute.
From:       G3 (the DAG is what the demand walks backward) with G2 (the second structure's metric);
            a definition without effects is G3's precondition rather than its consequence: the
            declarative face can be universal and minimally processed only if definitions have no
            effects; the separation of the second structure is the model's proposal
Formulation: The unit is the definition; dependencies give the only order there is, and time is
            reconstructed from them rather than from the text. Inside a block the text fixes which
            binding a name means, each `<-` a fresh name (D-2026-10-11-i), and then dependencies
            give the only order: after `x <- 1`, `y := x + 10`, `x <- 2`, y is 11, as the session
            answers. Operations are declared before their laws, so a law that binds two operations
            is a node with two parents, not a cycle; a mutable parameter is two variables, before
            and after, and mutation in place is the planner's optimization when the earlier one has
            no other consumer. The DAG says what depends on what; the structure the laws generate
            over terms (an equivalence when laws are boolean, a metric space when they carry a
            distance) is a second structure, where L13 and L11 live. Its result depends only on its
            inputs; effects live only in the actions (print, save). A mutable parameter written as
            before and after is not an effect, the dependence is an edge; what is forbidden is what
            the graph does not show. It is the one assumption under which every evaluation strategy
            gives the same result; over a carrier with a distance, a result in the same class at a
            distance the plan records, and for the Boolean case this is `Confluent` in
            `lib/plan.lut`, a law a dataflow is certified against rather than a theorem assumed.
            (His words) No effect on the world; its one effect is on the program: it takes its name,
            once, and enters the map of definitions, so the same name is not defined twice (`:=`
            once; `<-` only in a block, D-2026-10-11-i).
Quote:      (L18) "lo que si es no-side effects" (chat, 2026-10-10)
Source:     (L9) Luciano, 2026-05-29 (note:2026-05-29T14.46.22:contexto-como-dag); the unordered set
            of definitions already in 2023-03-13 (written:2023-03-13_hacia-luthier); the two
            structures and the mutable parameters 2026-10-10 (chat; D-2026-10-10-e) (L18) Luciano,
            2026-10-10 (chat; D-2026-10-10-c); his annotation on draft 8, bcdac41
Status:     settled
History:    (L9) draft 0 (6d9dbd3): stated. draft 2 (cd24137): the two structures. draft 5
            (5b1446c): inside a block the text fixes the binding (D-2026-10-11-i). (L18) draft 1
            (5769005): stated. draft 4 (c7c6396): `Confluent` as the law a dataflow is certified
            against. draft 9 (0636378), his words: the one effect, on the program. draft 10
            (72cc7be, 81c1794, 25f9c5e, b7a7e23): the former L9 and L18 merged.

L10 The demand determines the computation and the types produced.
From:       G3 directly; the audio of 08.58 (15:35 to 17:12, 30:37 to 31:21) adds the iteration
            step, read every demand, run, collapse to the outputs, write, and asks whether the code
            object is consumed or stable: kept; with G1 for what is derived (the former L13)
Formulation: The evaluation strategy is a parameter separate from the program (L12); by default, a
            plan backward from the actions over names, evaluating nothing, then a strict forward run
            over the live subgraph, each node once and whole: forward on demand. What the action
            asks for flows backward along the plan and is produced forward: the value, its error,
            its derivative, its test, the type of its result; at the leaves a value lifts on its
            own, takes a mark given with the demand, or is a hole. A decoration of the output is
            another model of the theory the code was written over (G1): run over dual numbers the
            code gives its derivative, run over intervals or over pairs of value and cost it gives
            its error; the demand choosing the output type is the demand choosing the model, and the
            planner inserts the bridges (L13). The derivative needs nothing new; the error waits for
            the algebra of costs (proposed, on his note on Terms). The tests are actions, so
            verifying is demanding. What never reaches an output needs no certificate, and what
            reaches one carries its cone's certificates (D-2026-10-11-n; `test` demands certificates
            without values). A result is identified by code, inputs, mode, the demanded type and
            tolerance, the model its type names, the seed, the plan that produced it, the plan being
            a value (`lib/plan.lut`), and the hashes of the certificates in its live cone, so a host
            library or platform that changed is a new result; the grade the demand states is in the
            identity too, and a memo hit serves a demand only if the cached cone meets that grade,
            checked at the hit and not only when the certificate was issued; the runtime includes
            the thread count and scheduling of the host, and an extern whose bits depend on
            scheduling is not bit-identical to itself, so its identity law is `Cost`, never `Bool`
            (L5). The run database is what the planner reads to choose the plan and is not an input
            of the result once the plan is fixed; evidence accumulates by a separate action with its
            own record, so "each node once" and G2's "kept across runs" never meet on one node. A
            test is an action whose result is a certificate, memoized by the certificate's identity
            (code, cases, seed, the distribution and level sampled, L7) and rerun when asked or when
            that identity changed; the demand states the grade it requires (P11), and a certificate
            serves every demand whose tolerance and grade it meets (`11` §4). "Each node once" is
            once per plan: a stricter demand on the same definition is another node of another plan,
            and the looser certificate still serves what it met. Three objects, never one: the
            meaning of a program, the class its laws fix; a realization, the result under a plan;
            the evidence, its certificates. A certificate is a frozen snapshot by hash; a later test
            does not change it, it issues a new one that supersedes it, both kept, the latest in
            front (P3), so progress is the chain of certificates. Two sessions that differ only in
            the order of independent bindings are equivalent by `Confluent` (L9), the law the
            session block is certified against. The program is the synthesis and is kept, the
            computation is the expansion and is redone. Script and interpreter are the same under
            this L, one batch of demands or demands one at a time with the memo between them (08.58,
            17:12 to 23:35; an item for the spec, 04 §7); a session is a block and a file is never
            one, so a session saved to a file becomes its `main` block (D-2026-10-11-i). The three
            cases at the leaves and the memo key are the model's, accepted. What is produced, and
            which types, is what the demanded value needs; what it does not need, the complement of
            its dependency cone, is not produced, so the choice is canonical, one per demand, and
            the types being spoken are what was asked for. Not producing at run time (a node freed
            after its last consumer) and not carrying in the type (how much history a certificate
            keeps) are one; the program is always kept, only what leaves scope is lost; not
            producing is not materializing a derived value, never erasing what reconstructs or
            recertifies it (code, inputs, model, seed, plan, tolerance), which the memo's identity
            keeps. A function on a type applied to a subtype does not produce one overload per
            subtype; the demanded return type selects which law to derive by composition (G1), and
            the rest is not produced: doubling positives is positive only when positivity is
            demanded and derivable, sin of positives is only Real because no law composes. What is
            derivable is a property of the expression, independent of the demand; the demand chooses
            which of it is derived, certified and carried, so the elaboration (types, derivable
            laws) does not depend on the observer; the memo of results does (L10), and they are two
            caches.
Quote:      (L13) "olvidar esta determinado por todo lo que no hay que recordar, es decir lo que
            pide el valor demandado. Eso soluciona el tema de los functores de olvido" (chat,
            2026-10-10)
Source:     (L19) Luciano, 2026-10-10 (WhatsApp Ptt 2026-10-10 at 11.11.22.md, 00:00; WhatsApp Ptt
            2026-10-10 at 11.42.15.md, 01:02 to 04:07; WhatsApp Ptt 2026-10-10 at 16.49.14.md, 03:20
            to 07:06; WhatsApp Ptt 2026-10-10 at 17.25.23.md, 05:49 to 07:53; WhatsApp Ptt
            2026-10-10 at 17.28.45.md; D-2026-10-10-d, f, h); WhatsApp Ptt 2026-10-11 at
            08.58.46.md, 15:35 to 23:35, 30:37 to 31:21 (L13) Luciano, 2026-05-29
            (note:2026-05-29T14.52.08:problema-del-olvido); resolved 2026-10-10 (chat; WhatsApp Ptt
            2026-10-10 at 11.42.15.md, 01:07 and 03:20 to 03:55; WhatsApp Ptt 2026-10-10 at
            17.28.45.md); the overloads 2026-10-11 (WhatsApp Ptt 2026-10-11 at 09.21.05.md, 00:00 to
            00:29; 09.01.13.md)
Status:     settled; the identity of a result, the memo gate and the three objects are the model's,
            from the rounds of critiques. The former L13 restated without the forgetful functor on
            his note of 2026-10-12
History:    (L19) draft 1 (5769005): stated. draft 2 (cd24137): the iteration step from audio 08.58.
            draft 4 (c7c6396): the identity of a result; what reaches an output carries its cone's
            certificates (D-2026-10-11-n). draft 5 (5b1446c): a test is an action memoized by its
            certificate's identity. draft 6 (8809e20): once per plan; three objects; the chain of
            certificates; sessions equivalent by `Confluent`. draft 7 (9d1c435, Kimi): the demand's
            grade in the identity, re-gated at the memo hit; (cd314a4, Claude): thread count and
            scheduling in the runtime, identity by `Cost`. fourth round (55da213), D-2026-10-11-i: a
            session is a block. (L13) draft 0 (6d9dbd3): stated. draft 2 (cd24137), audios 09.01 and
            09.21: no overload per subtype; the demanded return type selects the law. draft 4
            (c7c6396): what is derivable is independent of the demand. draft 5 (5b1446c): the
            elaboration and the memo are two caches. draft 6 (8809e20): forgetting is not
            materializing, never erasing what recertifies. draft 10 (72cc7be, 81c1794, 25f9c5e,
            b7a7e23): the former L19 and L13 merged; the decorated output as another model added
            (proposed, on his note on Terms); the former L13 restated without the forgetful functor
            on his note of 2026-10-12.

L11 An action is verified by observing the world before and after it.
From:       G0 (identity is the first proposition; his "path equivalence is the fundamental
            concept", 2026-05-29); the two faces are G3's statement; the verification of actions
            from G1 (observation) and G3
Formulation: Executing is the executive face (his annotation): an action changes the state of the
            world, and it is verified too, by observing the world before and after it; the laws over
            actions are stated over those two observations, as a mutable parameter is two variables
            (L9). An observation is itself an action, so this stops where the world can be read back
            (a file written and reread), and says nothing beyond; an effect on state Luthier owns is
            verified this way, an irreversible or concurrent effect outside it is typed, logged and
            audited, never verified.
Quote:      "la matemática no ejecuta ... la ejecución en Luthier sería esa verificación de
            equivalencias" (2026-05-30) "una funcion genera equivalencias f(a)==f(b) ==> a~b y mas
            si f(a)=true" (chat, 2026-10-11) "las ejecuciones tambien se verifican observando el
            mundo antes y despues del acto" (annotation on draft 2, 2c18c41)
Source:     Luciano, 2026-05-30; the kernel reading 2026-10-11 (chat); the actions 2026-10-11
            (annotation on draft 2, 2c18c41)
Status:     settled. Shortened on his note of 2026-10-12: evaluation and execution are in Terms; the
            reading of computation as the kernel of a function stays in the record
History:    draft 0 (6d9dbd3): stated. draft 2 (cd24137), addenda 7 and 8: the kernel of a function
            as the equivalence on its domain. draft 3 (c085ba4), his annotation: actions verified by
            observing the world before and after. draft 4 (c7c6396): an observation is an action;
            stops where the world can be read back. draft 5 (5b1446c): the kernel reading is an
            interpretation, not the mechanism; a name only where a normal form exists (formerly
            under G4). draft 6 (8809e20): effects outside Luthier typed, logged and audited. draft
            10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): renumbered from L12; shortened on his note of
            2026-10-12: evaluation and execution are in Terms, the reading of computation as the
            kernel of a function stays in this record (History below). the reading dropped from the
            projection at draft 10: Luthier first describes the problem and its equivalences;
            evaluating is checking them, as mathematics verifies rather than runs. (His annotation)
            Executing is the executive face: an action changes the state of the world, and it is
            verified too, by observing the world before and after it; the laws over actions are
            stated over those two observations, as a mutable parameter is two variables (L9). An
            observation is itself an action, so this stops where the world can be read back (a file
            written and reread), and says nothing beyond; an effect on state Luthier owns is
            verified this way, an irreversible or concurrent effect outside it is typed, logged and
            audited, never verified. Every function induces an equivalence on its domain, its
            kernel, so computing f(x) is placing x in its class and the value is the class's name:
            an interpretation of computation, not the evaluator's mechanism, and a name exists only
            where a normal form does, the decidable fragment (no canonical form elsewhere); a
            predicate is the two-class case and `Maybe T` places x in one of them. This equivalence
            on the domain is distinct from the equivalence between terms that a law induces, which
            is L10's quotient.

L12 No hardcoded constants: every criterion is a parameter.
From:       G3 (the tolerance belongs to the demand) and G2 (a law states a distance, not a
            threshold), so a constant in the code has no place to live; restates P11 (every
            criterion is a parameter, never a constant in the code)
Formulation: Thresholds, budgets, limits and statistical levels are never constants in code; they
            are declared, passed and recorded. The outermost demand, an action with no caller,
            carries its tolerance as a declared default argument (D-2026-10-11-c), recorded with the
            call, so there is a root and it is a parameter.
Source:     P11, in force; first applied as a rule of the language 2026-10-05
            (dialogue:c7437496:lmmaxiter-should-be-a-parameter)
Status:     settled. Statement in his words, 2026-10-12
History:    draft 0 (6d9dbd3): stated. Draft 0 of the generative plan proposed moving it to the way
            of working; withdrawn (D3). draft 6 (8809e20): the outermost demand's default argument.
            draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): renumbered from L17; statement in his
            words, 2026-10-12.
```

### 5. Implementations and the outside

```
L13 One function, many paths, chosen by maximizing the performance the demander chooses.
From:       G0 (the quotient), G2 (the choice by cost and the database of runs) and, before its
            retirement, G4 (every path expressible; now L13's own clause)
Formulation: A function has many equivalent implementations, each with its precision, speed, memory
            and place of execution; equivalence is established first, and the choice among paths
            follows expected loss and cost, estimated from a database of measured runs; error, time
            and memory are not one scalar, and the trade-off among them is a parameter of the demand
            (L12), never the planner's own; his formula of 2026-10-12 for what the planner ranks is
            an efficiency, exp(−cost) over the resources used (time, memory), so that a model of
            cost zero has efficiency 1/resources and not zero, with the weight between cost and
            resources the demand's parameter (proposed wording of his chat note). Two regimes: on a
            decidable carrier (`Int`, `Fin n`) two implementations compute the same function or not,
            the quotient is exact, there is no precision to trade and the Boolean kernel stands on
            its own; on a carrier with a distance (`Float64`) they are interchangeable only up to a
            distance within the demanded tolerance, and precision can be traded for resources, which
            is where cost (G2) and the demand (G3) enter G0's quotient. Stated as a quotient: the
            implementations of a function are the quotient by "compute the same function up to the
            law's equality", one class per mathematical function, and inside the class the fibre of
            what differs; the class is chosen by law, the representative by cost. The class is exact
            in the theory (`Real`); in a model that carries a distance it is the ball of the
            demanded radius (`11` §3), and closeness is not transitive, so the planner substitutes
            one implementation for another only along a certified equivalence between the two, the
            identity law of L5 with its result `Bool` or `Cost` (D-2026-10-11-m). The law gives the
            candidates; the identity certificates say which the planner may exchange, and they form
            a weighted graph, not a class: a substitution is a path whose summed distance (`11` §2)
            is within the demanded tolerance, so two specimens joined through a third may each
            replace it and not each other; the sum is a bound only when every link is one (proved,
            exhaustive), otherwise an estimate with the weakest grade and the samples it was seen
            on; a lone implementation is never replaced. A sampled edge is admissible only on inputs
            the distribution it sampled covers, and only as a direct edge, never summed into a path,
            until a probabilistic bound exists as a law; the tolerance charged at a node is the
            demand's pulled back through the sensitivity of the cone from the node to the demand
            (`11` §5), and where no sensitivity is known there is no substitution. The same for
            every grade: a link certified on a subtype is a link only at inputs certified (L3) in
            that subtype, so a path exists at x only where every link does; a `proved` link by
            citation carries the theorem's hypotheses as parameters (γ_n needs n·u < 1, false for
            float32 over an hour at 48 kHz) and is void where they fail. The author's free choice
            among the inhabitants of an under-determined function (D-2026-10-11-d, P5) stays; the
            planner's choice is only among what has been compared.
Source:     Luciano, 2022-06-28 (written:2022-06-28_luciano-code-style:choose-efficient-path-
            after-validity); the quotient 2026-10-10 (WhatsApp Ptt 2026-10-10 at 16.49.14.md, 00:04
            to 01:39), the same idea without the word 2026-05-30 (note:2026-05-30T18.01.53:
            equivalencias-para-clasificar-y-separar-decoraciones)
Status:     settled; the weighted graph, the admissibility of sampled edges and the subtype clause
            are the model's, from the rounds of critiques. Statement in his words, 2026-10-12
History:    draft 0 (6d9dbd3): stated. draft 2 (cd24137): stated as a quotient. draft 4 (c7c6396),
            D-2026-10-11-m: exact in the theory, a ball in the model; substitution only along a
            certified equivalence. draft 5 (5b1446c): a weighted graph, not a class; a lone
            implementation never replaced. draft 6 (8809e20): error, time and memory not one scalar.
            draft 7 (6a15cec, cd314a4): from the third round's counterexamples, a sampled edge only
            on covered inputs and only direct, the tolerance pulled back through the sensitivity;
            Claude's clause on subtypes and cited hypotheses. draft 9 (120a49a): G4 retired; "every
            path expressible" is L10's own clause. draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23):
            renumbered from L10; statement in his words, 2026-10-12; his formula for the efficiency,
            exp(−cost) over the resources, added (proposed wording).

L14 Luthier orchestrates other languages; what does not follow its way lives in a world; a foreign
    function is certified by delegation, and certification transports along equality.
From:       G1: an absorbed library is a specimen known by its description, and its code is not
            needed ("que la IA pueda ... extraer de librerías ajenas, chuparlas y usar las funciones
            con sus propias invarianzas", audio 08.58, 31:25 to 32:00); the world from G3 (the
            demand names the world it runs in) with L11; delegation from G1 and G2 (the former L11);
            transport from G1 (the former L21)
Formulation: Types and laws are native; values may come through `extern` from Python or any host,
            declared over what they really receive and return, with description and verification
            kept on Luthier's side. An external function is validated like any other, against its
            type with its laws, the first time an action asks for it, and its certificate stays by
            hash; without a type with a law to validate against it is not applied. (His words) "si
            el tipo no sigue la ley no se aplica el calculo": an extern is declared over a type, a
            type carries its laws (L2), the extern is validated against them before it is applied
            and refused if it fails; the agreement test with the native is in addition (W5), and the
            planner's substitution is D-2026-10-11-m. A function with no laws at all is not a
            function to run but a hole of a theory being defined (L4). The extern's certificate
            binds the host library's version and the platform (W10), and its declaration says
            whether it is a definition or an action (L11, L9). Certification is the default for
            every value: demanding a value demands every certificate in its dependency cone, paid
            once through the memo, unless the demand asks otherwise by a mechanism to be named,
            which leaves a certificate of grade `assumed` (D-2026-10-11-n), since what could be done
            Luthier gives a way to do (L14); `test` is the action that demands certificates without
            values (L10). Luthier is in use a coupling language: the joint between two libraries is
            a theory of which each is a model, the bridges between representations live at the joint
            with their cost and error, and no coupling without a law. A definition or an
            implementation that does not follow Luthier's way, an extern with no law yet, a foreign
            algorithm taken as is, is allowed inside a named world (L11): its certificates are
            `assumed` (D-2026-10-11-n), the plan shows the world it ran in, and nothing from it
            enters the planner's graph (L13) until a law is certified. Verification by a theorem is
            `proved` by citation (D-2026-10-11-f); verification by delegation is the same mechanism
            with the host library's guarantee as the theorem cited (LAPACK's backward-error bounds,
            the condition number their hypothesis) and the library's version and platform as
            hypotheses the certificate carries (L14); no new grade (*Proposed*, on his mark). (His
            correction) Certification transports along identity: if B is certified at grade g on
            inputs X and the identity A ≡ B is certified at grade h on inputs Y, then A is certified
            at the weaker of g and h on X ∩ Y, and by nothing else. The two counterexamples of the
            third round follow: with B's laws only `assumed` the transport gives A `assumed`,
            nothing (Kimi); a lookup table equal to the native on a grid is certified on the grid
            and nowhere else (Claude). A function known correct by a theorem outside Luthier is
            certified `proved` by citation (D-2026-10-11-f), and the chain law, citation, native,
            identity, extern is carried by hash.
Quote:      (L14) "si el tipo no sigue la ley no se aplica el calculo" (chat, 2026-10-10) "que la IA
            pueda ... extraer de librerías ajenas, chuparlas y usar las funciones con sus propias
            invarianzas" (audio 08.58, 31:25 to 32:00) (L22) "si hay una forma 'no luthieriana' de
            definir o implementar algo, luthier deberia dar la posibilidad de hacerlo con un world
            especifico" (bcdac41) (L11, delegation as citation) "verificacion externa por teoremas o
            por delegacion (creo en Lapack)" (bcdac41) (L21, the graded transport) "verificar bit a
            bit que sea igual ... por lo menos sabés que no cambia la implementación" (audio 08.58,
            09:20 to 13:19); the statistical kind for "prueba científica" (same)
Source:     (L14) Luciano, 2026-05-26 (note:2026-05-26T12.32.24:lenguaje-no-atado-a-cpp); the
            validation on first demand and the coupling language 2026-10-10 (chat; WhatsApp Ptt
            2026-10-10 at 17.41.53.md; WhatsApp Ptt 2026-10-10 at 16.49.14.md, 01:39 to 03:18);
            WhatsApp Ptt 2026-10-11 at 08.58.46.md, 31:25 to 32:00 (L22) his annotation on draft 8
            (bcdac41), on G4 (L11, delegation as citation) Luciano, 2022-08-03 and 2023-02-22
            (written:2023-02-22_tapp-wish-list:untested-a- tested); the grades by samples 2026-10-10
            (WhatsApp Ptt 2026-10-10 at 11.11.22.md, 03:02 to 04:12); his annotation on draft 8,
            bcdac41 (L21, the graded transport) Luciano, 2026-10-11 (WhatsApp Ptt 2026-10-11 at
            08.58.46.md, 09:20 to 13:19); his annotation on draft 2 (2c18c41); his annotation on
            draft 8 (bcdac41)
Status:     settled by his correction (draft 7); the opt-out's syntax open. proposed, candidate; the
            wording is the model's. Delegation (from the former L11) and transport (from the former
            L21, his correction) placed here on his note of 2026-10-12
History:    (L14) draft 0 (6d9dbd3): stated. Draft 0 of the generative plan proposed moving its
            orchestration half to the way of working; withdrawn (D3). draft 4 (c7c6396),
            D-2026-10-11-n: certification the default, the opt-out in the demand. draft 5 (5b1446c):
            the opt-out leaves a certificate `assumed`. drafts 5 and 6: carried "every function
            starts with zero laws", which came from a critique, not from D-2026-10-11-d, wrongly.
            draft 7 (e8ba100): the zero-laws clause removed; the extern validated against its type's
            laws in his words; a function with no laws is a hole (L8). (L22) draft 9 (0636378,
            120a49a): stated from his words on G4, which it replaces (D-2026-10-12-c). (L11,
            delegation as citation) draft 0 (6d9dbd3): stated. draft 4 (c7c6396): the four methods
            and the grade in the certificate; the dependence on the distribution. draft 9 (0636378),
            on his mark: delegation as citation of the host's guarantee. readers' draft 0 (afdd7c7):
            his correction adds the library as a source of proof. (L21, the graded transport) draft
            1 (5769005): proposed, candidate. draft 3 (c085ba4), his annotation: the certificate of
            the law travels by the certificate of identity. draft 4 (c7c6396), D-2026-10-11-m: the
            identity law admits a second implementation into the planner's class. draft 7 (9d1c435,
            cd314a4): two clauses from Kimi and Claude on when transport fails. draft 9 (0636378),
            his correction: the two clauses replaced by graded transport on X ∩ Y, the
            counterexamples following from it. draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): the
            former L14 and L22 merged; delegation (former L11) and transport (former L21, his
            correction) placed here on his note of 2026-10-12.
```

### 6. The language itself

```
L15 The core is minimal, executable by hand, and its programs are data.
From:       G0 (a type theory is a few rules whose judgments a person checks; a small trusted
            kernel) and G1 (the paper semantics is the description, and every interpreter is a
            specimen certified against it); programs as data from G0 through the universe, the type
            of types (the object classifier of HoTT; the note's "object classifier" names this when
            it means types as values, and the subobject classifier when it means G2's truth values)
Formulation: A handful of well-specified primitives, so that a program can be run with pencil and
            paper; everything else is a library whose translation to the core is mechanical. Hand
            execution is of the kernel given a plan, an order of execution that is a value
            (`lib/plan.lut`); the planner's choice among plans is outside the kernel. Four layers,
            each trusted differently: the kernel, checked by hand; the libraries and the interpreter
            in Luthier, certified against the kernel's laws; the host runtime, a specimen; the
            planner, advice that the plan records. A Luthier program is an element of Luthier;
            programs build, inspect and run other programs, and the interpreter is meant to be
            written in the language it interprets.
Quote:      (L7) "Luthier tendría que ser ejecutable a mano" (2026-05-29)
Source:     (L6) Luciano, 2022-06-15 (written:2022-06-15_sin-titulo-2:codigo-es-dato) (L7) Luciano,
            2026-05-29
Status:     settled
History:    (L6) draft 1 (5769005): stated. (L7) draft 0 (6d9dbd3): stated. Draft 0 of the
            generative plan proposed moving it to the way of working; withdrawn (D3). draft 4
            (c7c6396): hand execution is of the kernel given a plan. draft 6 (8809e20): the four
            layers of trust. draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): the former L6 and L7
            merged.
```

(History: the introduction of draft 9: Each L keeps its number and source from draft 1. `From:`
names the organizers it derives from and the derivation, the model's unless marked his. Order: by
first organizer, G0, G2, G1, G3.)

(History: the former L20, absorbed into G1 in draft 9 and no longer projected since draft 10; the
clause on specializations and bridges belongs to L13 and modules as values to the spec (`03`): L20 A
function is declared in a theory and is universal over its models. From: G2, of which it is the
definition rather than a consequence: a function belongs to the theory its laws are stated in, and a
model is where it runs; before draft 8 from G0 (a theory is a type, a model its inhabitant) and G1
("lo declarativo pasa a ser todo lo universal posible"; instantiated on demand) Formulation: a
function belongs to a theory (Real, Field, LinearAlgebra) and takes its model as its first, often
implicit, argument, so it is written once for every model; the model is named by the type of the
argument (D-2026-10-11-j) and can be passed explicitly. A theory over a model of another theory is a
theory. Every type belongs to a theory; the concrete types (products, sums, exponentials, `data`)
belong to the kernel's, whose laws are the β and η rules and the recursion principle, stated in
`lib/kernel_laws.lut`. Operators are resolved by the type, the type naming its model; a carrier with
two models is two types (D-2026-10-11-j). Modules are values by design, files today: a parametrized
module is a function from models to definitions, applicative because definitions have no effects
(L18), instantiated on demand with the parameter threaded down from the action. A specialization is
one more representative of the law's class (L10), valid on a subtype, certified against the same
law; where representations differ, the orchestrator inserts bridges by cost, coherent up to the law,
carrying their error, visible in the plan; a specialization and a bridge each enter the planner's
graph by an identity certificate with its distance (L10, D-2026-10-11-m). The conditions on bridges
are the model's, accepted. Quote: "el codigo seria, en principio universal a los valores de
funciones que cumplan las leyes requeridas" (chat, 2026-10-10) "no entiendo porque hacerlo un
principio. Surge solo" (bcdac41) Source: Luciano, 2026-10-10 (chat; WhatsApp Ptt 2026-10-10 at
17.00.40.md; WhatsApp Ptt 2026-10-10 at 17.25.23.md, 00:00 to 04:25; D-2026-10-10-g) Status:
absorbed into G2 on his mark (draft 9): the clause on specializations and bridges belongs to L10 and
modules as values to the spec (`03`); the tag stays for the record's citations and the text stays
until the spec takes its parts History: draft 1 (5769005): stated as "code is universal over the
models of its theory". draft 3 (c085ba4): reworded after his annotation (theories). draft 4
(c7c6396): the model named by the type of the argument (D-2026-10-11-j). draft 5 (5b1446c):
specializations and bridges enter by identity certificates. third and fourth rounds (9395268,
55da213): every type belongs to a theory; the kernel's theory in `lib/kernel_laws.lut`. draft 8
(4f6beef): moved under G2 as its definition. draft 9 (0636378), his mark: absorbed into G2.)

## What is open

- The Boolean interim the application runs on until G2's algebra exists: laws of the form
  d(f x, g x) ≤ tol with tol a parameter (L12), every law returning `Bool` or `Cost` with the
  result type saying which (`11` §2, L5), no composition of tolerances along a chain, no run
  database.
- The articulation of G2, `docs/rationale/11-cost-valued-laws.md` draft 0 (D6): Ω replaced by
  [0,∞), quantitative equality, graded judgments, cost as −log p or as distance, how the
  uncertainty of a cost is represented in a certificate; the algebra of composition (second
  round §16): a Lipschitz constant per function type where known (sensitivity types, Reed and
  Pierce 2010; condition numbers), a sampled cost where not, costs adding as −log p under
  independence; worked examples the sum of n floats, a matrix inverse with κ(A), a sampled
  probability integrating to one.
- The extension of Boolean logic to Lawvere and Bayes, G2, which he names as another motivator or
  eureka (chat, 2026-10-12); whether it is the third eureka or a principle of good use is his to
  mark after that analysis.
- The composition of invariances (G1's derived route): which laws compose and how the demand
  selects them (audio 08.58, 32:01 to 34:07; audio 09.21).
- The session as a block over the dataflow of L10: `<-` to explore, `:=` to lock, a file may
  contain a block, `<-` banned at the top level of a file (decided, D-2026-10-11-i); the spec's
  `04 §7` and a section on the session.
- Done 2026-10-11, in the spec: blocks (`02 §9`, `04 §5`, `05` R12, D-2026-10-11-i); operators by
  the type naming its model (`05` R13, D-2026-10-11-j; `examples/z7ring.lut` rewritten, Z7 its
  own type and `mod 7` a certified homomorphism); Python-like separators (`02 §1`,
  D-2026-10-11-k); `cite` and `proved` by citation (`05 §7`, D-2026-10-11-f); `lib/laws.lut`
  split from `algebra.lut` (D-2026-10-11-l). Implemented 2026-10-11 in the interpreter: blocks
  and the session (`luthier session`), defaults and named arguments, R13's refusal of two models
  on one type, `cite` with `.bib` modules, exhaustive tables of `Fin n -> T`; `lib/plan.lut`
  states an order of execution as a value and confluence as a law, checked exhaustively in
  `examples/plan_confluence.lut`. Pending: actions and the world as a value; the memo between
  the items of a session.
- From the round of critiques: the interface of `Cost` in a certificate (a multiplicative
  constant where it exists, an additive defect where rounding enters, the grade as a lattice,
  the worst cost seen; `11` §5, §6); the identity of a result in the memo (L10) and `plan.lut`
  as its carrier; the opt-out of certification in a demand (D-2026-10-11-n, syntax open); the
  kind of a hole in the elaborated form (L4); the world as an opaque, unique value so that an
  action is never served from the memo (L9, L10); L8's rounding, his mark pending.
- The kernel's theory stated in Luthier: `src/luthier/lib/kernel_laws.lut`, tested on `Fin 3`,
  `Fin 2` (`examples/kernel_finite.lut`, 10 laws, sampled); eta not statable (`05` R8),
  functions over `Fin n` not enumerated by `exhaustive` (to fix).
- `proved` by citation: the citation a `.bib` key with a resolved DOI, ISBN or URL, and who
  checked (human, ai+human, none) recorded; syntax `cite name bibkey checked ai+human` proposed,
  allowed in user code (D-2026-10-11-f as amended; to `05 §7`).
- *Object* in the spec (`05 §3`, a strongly connected component of the dependency graph): not among
  the terms; in them it is a theory written in one cycle of names with its models, never a
  function. Proposed: `05 §3` becomes "theories are cycles" and the word survives only in "object
  classifier"; one commit over `04` and `05`; his decision.
- The decorated output (L10): the derivative by dual numbers as a model of the theory, the error
  by intervals or value-and-cost pairs once the algebra of costs exists; what in the planner
  chooses the model and inserts the bridges.
- Units as a candidate L under G0: a dimension is a proposition, dimensions form a group under
  multiplication, the quantities of one dimension a one-dimensional vector space, the whole a
  graded algebra; addition inside a dimension, multiplication across (second round §18).
  Precedent quimulun (his repository); pressure from sonolocalización (metres, seconds, the
  speed of sound).
- The type with its equality as the base case of every theory (a setoid; a metric space where
  the equality is a cost), the kernel's structural `==` its model for the decidable types
  (`05` R8), the equality of functions extensional and derived from it (L5), the equality of
  models componentwise; and whether a type names its equality as it names its model (`05` R13).
  Proposed by the model on his observation of 2026-10-12 (D-2026-10-12-e); his note of the same
  day on Terms goes the same way ("podríamos suponer que A viene con su Setoid", `K` with its
  `Field`); the syntax, how a type names its setoid and its field, is the open part.
- The names he left with a question mark in his list of terms (structure, cost, certificate) and
  the three-level answer to his doubt on validation as execution; and whether `05 §3` renames
  *object* (D-2026-10-12-f).
- His marks pending on this record: L5's wording (graded transport), L8's correction on
  rounding, L7's delegation as citation, the names lift, exact and within (G2), L14 as a
  candidate.
