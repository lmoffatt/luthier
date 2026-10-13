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
the demand; L1 to L15 in his six topics. Since draft 11 (D-2026-10-12-v) they are
numbered contiguously in document order, L1 to L13. The table under Numbering maps the tags of
each draft; inside `Quote:`, `Source:` and `History:` a tag carries the numbering of its time, and
`record/decisions.md` keeps in its Kind lines the tags of the day each decision was taken.

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
| record | 2026-10-12 | this file | Step 3 of the draft 11 plan (D-2026-10-12-g, -s): the shape applied by `scripts/migrate_record_draft11_shape.py`, nothing reworded. Done items that stood in What is open until draft 10: in the spec on 2026-10-11, blocks (`02 §9`, `04 §5`, `05` R12, D-2026-10-11-i); operators by the type naming its model (`05` R13, D-2026-10-11-j; `examples/z7ring.lut` rewritten, Z7 its own type and `mod 7` a certified homomorphism); Python-like separators (`02 §1`, D-2026-10-11-k); `cite` and `proved` by citation (`05 §7`, D-2026-10-11-f); `lib/laws.lut` split from `algebra.lut` (D-2026-10-11-l). Implemented 2026-10-11 in the interpreter: blocks and the session (`luthier session`), defaults and named arguments, R13's refusal of two models on one type, `cite` with `.bib` modules, exhaustive tables of `Fin n -> T`; `lib/plan.lut` states an order of execution as a value and confluence as a law, checked exhaustively in `examples/plan_confluence.lut`. |

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

The tags of draft 11 (contiguous, in document order, D-2026-10-12-v) against those of draft 10
(his marks on the reorder plan, 14ea9f0) and of drafts 1 to 9.

| Draft 11 | Draft 10 | Before | What happened |
|---|---|---|---|
| G0 | G0 | G0 | kept |
| G1 | G1 | G2 | theory and model, printed first since draft 8; the former L3 and L20 absorbed |
| G2 | G2 | G3 | cost, the second eureka on his note; lift, exact and within moved to L6 |
| dissolved | G3 | G1 | the demand, printed third in draft 10; dissolved in draft 11 into G0's second sentence and L10.1 |
| — | retired | G4 | retired in draft 9 (D-2026-10-12-c); its content became L22, now in L14 |
| L1 | L1 | L1 | kept; the Purpose section since draft 11 |
| L8 | L2 | L2 | kept |
| merged into L8 | L3 | L4 | renumbered; "from a law" his correction; merged into L2 in draft 11 |
| L2 | L4 | L8 | renumbered |
| L3 | L5 | L16, L21 | merged: equality has levels, with the identity clauses of L21 |
| L12 | L6 | new | how laws combine, the lift and the cutoff, from the former G3 |
| L9 | L7 | L5, L11, L21 | merged: a law characterizes, verified by one operation; identity is not the law |
| L13 | L8 | L15 | renumbered |
| L4 | L9 | L9, L18 | merged: a DAG of definitions without effects |
| L5 | L10 | L19, L13 | merged: the demand determines the computation and the types produced |
| merged into L4 | L11 | L12 | renumbered and shortened; merged into L9 in draft 11 |
| merged into L5 | L12 | L17 | renumbered; statement in his words; merged into L10 in draft 11 |
| L6 | L13 | L10 | renumbered; statement in his words |
| L11 | L14 | L14, L22, L11 (delegation), L21 (transport) | merged |
| L7 | L15 | L6, L7 | merged: the core is minimal and its programs are data |
| — | absorbed | L3 | into G1 (draft 10) |
| L10 | L16 | new | certificates, draft 11 (step 4) |
| L14 | new | new | what can be written in Luthier is written in Luthier, his principle of 2026-10-12; under G0 after L7, to take its place by document order at the next renumbering |
| — | absorbed | L20 | into G1 (draft 9) |

## Purpose

One sentence, which is L1, heads the document: the language exists so that the invariances of a
discipline can be stated in it. Everything below says how.

```
L1  Luthier expresses the invariances of the disciplines.
From:       G1 (what is known of a thing is its description; "la idea de luthier es ayudar a
            descubrir las invariantes de los calculos", note), with P14 (a type is a concept)
L1.1   What moves the language: a species mates within itself, electrons are fermions, a probability
       integrates to one. A definition states the invariances that determine a concept, and the
       language exists so that stating them is natural. [settled]
Quote:      "la idea de luthier es ayudar a descubrir las invariantes de los calculos" (note)
Source:     Luciano, 2026-05-29 (dialogue:20260529T1400:expresar-invarianzas-de-disciplinas)
Status:     settled; the purpose, not a design rule, so it heads the document
History:    draft 0 (6d9dbd3): stated. draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): number kept;
            first of the six topics. draft 11, step 3 (2026-10-12): the formulation split into
            numbered clauses with the status each sentence had in draft 10, the examples into
            Example, the provenance phrases into this History, the wording otherwise as draft 10 had
            it. draft 11, step 3 (2026-10-12): moved to the Purpose section, the tag kept so that
            citations resolve.
```

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

(History: the status paragraph of the Terms at draft 10: his list (D-2026-10-12-f); the names
structure, cost and certificate are the model's where he left a question mark, marked OK by him on
2026-10-12; *dependences* replaces the model's "dependent theory" on his note (every theory is one,
so the emphasis goes on what it depends on); the reading of certification as an action on Luthier's
own state is proposed, kept by him on 2026-10-12 with the clause "never an action on the world"
removed as obscuring; the carrier coming with its setoid and its field is his note of the same day,
and "today the libraries pass them as parameters" was the implementation's state. Draft 11, step 3:
the grades defined here, with the meaning each had across L2, L7 and L14; the two faces named, since
the organizers and the headings use them; nothing marked proposed or open stays in Terms.)

## The organizers

The guide and the two eurekas, in his order. An organizer is two sentences: what it says and what
it decides; it carries no mechanics and no status, and the principles under it are its section
below. The history of the eurekas and the P13 count are in the record.

(History: draft 10's introduction: the guide, then the two eurekas, then the demand; renumbered on
his note of 2026-10-12: G1 is theory and model (G2 until draft 9), G2 is cost (G3 until draft 9), G3
is the demand (G1 until draft 9). Draft 11, step 3: G3 dissolved into G0's second sentence and
L10.1, as its own status asked (D-2026-10-12-s); its entry is the paragraph below.)

```
G0  Type theory is the guide.
Tier:       the guide
Formulation: A type is a proposition and a value its proof; a law is a proposition over terms, so it
            defines a mathematical object and a quotient, and inside the class the representative is
            free. Type theory guides what is declared, and what governs execution is the demand,
            read in the same theory: a demanded type is a judgment to inhabit, execution is the
            search for an inhabitant, and where type theory normalizes a given term, Luthier
            searches for one.
Quote:      "Un principio es hott/Category theory/ type theory guidance. De ahi sale types as
            propositions y funcions as types y por ende functions defined as propositions, laws. De
            ahi sale que las laws definen objetos matematicos. y tambien que con una law tenes un
            cociente y por lo tanto valores intercambiables y por lo tanto optimizacion por tiempo y
            costo en memoria o por error." (note, fa3f972) "la guía es la te[o]ría de tipos" (audio
            09.19, 00:00)
Source:     record/Lucianos ideas/principios organizadores.txt (fa3f972); WhatsApp Ptt 2026-10-11 at
            09.19.36.md, 00:00
History:    draft 2 (cd24137): stated from his note and the audio, formulation proposed. draft 5
            (5b1446c): "free in the theory, where the law is exact; in a model, L10". draft 10
            (72cc7be, 81c1794, 25f9c5e, b7a7e23): statement and formulation kept; the organizers
            renumbered on his note of 2026-10-12 (G1 theory and model, G2 cost, G3 the demand).
            status at draft 10: settled, marked OK by him on 2026-10-12. draft 11, step 3
            (2026-10-12): cut to two sentences, no status, no mechanics (D-2026-10-12-s); the
            executive clause of G3 (the demand defines what is computed) read into it, as G3's own
            status asked; "cost or execution time ranks the candidates" dropped, since the ranking
            is L13's; the Ls under it listed in its section.

G1  A type is a theory and its values are its models.
Tier:       eureka, the first (the trigger, audio 09.19, 00:00 to 00:14)
Formulation: If a type is a proposition, then a proposition can say that a structure follows the
            rules of a theory, so "this structure satisfies the laws of the theory" is said, in the
            language of types, as "it is of the type of the theory": it is a model of the theory,
            and Luthier verifies that it is. Types thereby carry a strong semantic meaning, and
            coding and testing are one act: to declare `m : T` is to declare the tests `m` will
            pass.
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
            (0636378), his mark: absorbed into G2. status at draft 10: settled; this wording is his
            note of 2026-10-12 put in order; the long form in the record. draft 11, step 3
            (2026-10-12): cut to two sentences, no status, no mechanics (D-2026-10-12-s); "what type
            theory lacks: it knows a value by its term; Luthier knows it by the law it satisfies"
            kept here; the Ls under it listed in its section.

G2  Laws are valued in cost: one logic, extended to the non-negative reals.
Tier:       the second eureka on his note of 2026-10-12
Formulation: Not every theory is easily described by Booleans; many are represented better by costs.
            Since object classifiers exist that extend logic to the non-negative reals, with the
            Booleans as a special case, the composition of errors in numerical libraries can be
            attacked with this one unified logic.
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
History:    draft 2 (cd24137): stated, good use. draft 9 (0636378): on his mark, Bool and Cost
            coexist, the lift explicit and named, the cutoff only in the demand. draft 10 (72cc7be,
            81c1794, 25f9c5e, b7a7e23): renumbered from G3 on his note of 2026-10-12 and named the
            second eureka; lift, exact and within moved to the new L6; the formulation rewritten in
            his words. status at draft 10: the second eureka on his note of 2026-10-12 (candidate by
            the P13 count, one decision guided so far); the algebra of costs open (`11`), the
            analysis he announced pending. draft 11, step 3 (2026-10-12): cut to two sentences, no
            status, no mechanics (D-2026-10-12-s); "how laws combine is L6; how a law is verified,
            L7; what a run teaches is kept" and the status of draft 10 (the second eureka on his
            note of 2026-10-12, candidate by the P13 count, one decision guided so far; the algebra
            of costs open, the analysis he announced pending) kept here; the Ls under it listed in
            its section.
```

(History: G3 at draft 10, dissolved in draft 11: G3 The demand defines what is computed. Tier: the
executive face; an eureka until draft 9, when it was G1; printed third on his renumbering of
2026-10-12 Formulation: The declarative face states what is known, universal and minimally
processed; the executive face is a demand from outside, and the demanded type fixes the path, the
types and the tolerances actually produced. What type theory lacks: an executive face; there,
computation is the normalization of a given term, with no demand. Quote: "la demanda de un valor por
el mundo externo me define todos los tipos necesarios para obtener eso" (audio 09.19, 00:24) "la
compilacion se dispara por la demanda externa (es decir un print o un valor que sale al mundo), y la
demanda determina el tipo que quiere el print, y eso determinan 1) el camino que efectivamente se
computa y los tipos que efectivamente se computan" (note) "la clara separacion entre lo declarativo
y lo ejecutivo. Esto dio lugar a la idea de que lo ejecutivo se da por la demanda. Y lo declarativo
pasa a ser todo lo universal posible, minimamente procesado" (note, 1c7a284) "lo que se sabe, que es
un poco como la idea del prior" (audio 08.58, 08:59) Source: WhatsApp Ptt 2026-10-11 at 09.19.36.md,
00:24; record/Lucianos ideas/principios organizadores.txt; its root, 1c7a284; WhatsApp Ptt
2026-10-11 at 08.58.46.md, 08:59 Status: settled; printed third on his renumbering; whether it is an
eureka of its own or the executive clause of the guide (G0) is his to say History: draft 2
(cd24137): stated, printed as the first eureka. draft 8 (4f6beef): printed second, in his order.
draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): renumbered from G1 on his note of 2026-10-12, printed
third.)

## Precedence

When two statements conflict, the organizer they derive from decides; when two organizers
conflict, G0 decides; within an entry, the statement decides over its clauses. A clause marked
proposed, candidate or mark pending yields to one marked settled.

## The principles of the language

Fifteen principles, each under the organizer it derives from, in the order of his six topics.
Each is a statement, the fixed part, and numbered clauses, each with its own status: settled,
proposed (the model's, awaiting his mark), candidate, or mark pending (his words, the wording
awaiting his mark). Where a clause has a worked example, the example follows the clauses; what
each entry rests on among the open questions is named. The Numbering table at the end maps the
numbers of drafts 1 to 10.

(History: draft 10's introduction: fifteen L in six topics, from the most general to the most
particular, renumbered on 2026-10-12 (`record/plan-principles-reorder-2026-10-12.md`, his marks
14ea9f0); each heading named the former numbers it joined; five merges, one new L on how laws
combine, the former L21 dissolved into the new L5, L7 and L14, the former L3 and L20 absorbed into
G1; formulations joined, not reworded, except where his note asked. Draft 11, step 3: the six topics
give the order inside each organizer's section and are no longer headings, since a topic cuts across
organizers (types, theories and models has L2 and L3 under G1 and L4 and L5 under G0).)

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

### Under G0, the guide

```
L2  Declare, then define, then inhabit.
From:       G0 (a hole is a hypothesis of the context) with G0, the demand (nothing is produced
            until demanded)
L2.1   A declaration without a body is a first-class hole: at once axiom, program input, external
       function, pending definition and dead code; nothing executes until it is defined, and no
       value inhabits an undefined type. [settled]
L2.2   An axiom is not a value but a law with grade `assumed`, so it does not inhabit; `assumed` has
       one meaning, the grade. [settled]
L2.3   To the type checker the five are one, and the elaborated form records which it is, since the
       demand treats them differently: an input asks for a value, an external calls the host, a
       pending definition is an error, an axiom is a law with grade `assumed`, reasoned with and
       never run (O9). [settled]
L2.4   `extern` is the operation that inhabits a hole with a body in another language, naming the
       language; a theoretical module (types, functions, laws, no values) is a module of holes.
       [settled]
L2.5   (His words) A declared name is assumed to have its declared type, and its use where that type
       is incompatible is an error (spec 4.R1, the checker). [settled]
L2.6   The theoretical module of clause 4 is a file of its own: a theory file holds types,
       declarations and laws, and is what the checker reads; each model of it, or each algorithm
       written against it, lives in a file of its own, read only when a demand needs it and
       certified against the theory. What a file imports has its theory in a theory file
       (D-2026-10-13-i, -j). A theory file may hold the definitions its laws need and a value that
       is part of the theory, never a model of a theory declared elsewhere (D-2026-10-13-o).
       [settled]
L2.7   (His words) A definition is a concept, and a collection of types is not. An alias names a
       structure we use before we know what it is for; a definition promotes it to a theory, and
       what makes it one is a law it must follow, stating the role of each part. Distinct
       constructors are free and state no role; an observer that only lists them is an automatic
       accessor, not a law; a `data` with no law of its constructors' roles is a collection and is
       written as an alias (D-2026-10-13-p, D-2026-10-07-e). It costs thought, and that is its
       purpose. Everything has laws; it is a matter of finding them, usually in the place the thing
       holds in a known structure (`Unit` terminal, `List` the free monoid, D-2026-10-13-t).
       [settled]
References: spec 4.R1; D-2026-10-13-i, D-2026-10-13-j
Rests on:   O9 (the kind of a hole in the elaborated form, for the spec)
Source:     Luciano, 2026-05-29 (dialogue:20260529T1400:tipos-no-definidos-y-forward-reference); the
            hole named 2026-09-29; `external` and the theoretical module 2026-10-10 (WhatsApp Ptt
            2026-10-10 at 17.41.53.md; WhatsApp Ptt 2026-10-10 at 17.25.23.md, 00:00 to 00:40); his
            annotation on draft 8, bcdac41
Status:     settled; clause 6 settled (D-2026-10-13-i, -j, -n); clause 7 his (D-2026-10-13-p)
History:    draft 0 (6d9dbd3): stated. draft 4 (c7c6396): the elaborated form records which of the
            five it is. draft 5 (5b1446c): `assumed` has one meaning. draft 6 (8809e20): an axiom is
            not a value. draft 9 (0636378): his words on a declared name's type. draft 10 (72cc7be,
            81c1794, 25f9c5e, b7a7e23): renumbered from L8. draft 11, step 3 (2026-10-12): the
            formulation split into numbered clauses with the status each sentence had in draft 10,
            the examples into Example, the provenance phrases into this History, the wording
            otherwise as draft 10 had it. draft 11 (2026-10-12): renumbered from L4 of draft 10
            (D-2026-10-12-v).

L3  Equality has levels and belongs to the object.
From:       G0 (the identity type and its levels) with G2 (under cost, the identity proposition
            acquires a distance); clause 4 from G1 (the specimen can be recognized as the same
            specimen, or described)
L3.1   Definition (`:=`), the identity proposition (`=`), decidable equality (`==`) and definitional
       equality by reduction (`≡`) are different things, and each object carries the observational
       equality that fits it. [settled]
L3.2   In the kernel the binding is exact: the name denotes the term, and reduction does not depend
       on a tolerance; the distance enters when the planner realizes the term by another
       representative, which it does only along a certified equivalence carrying its distance (L6,
       D-2026-10-11-m). [settled]
L3.3   Equality is a law of the object: Boolean where the carrier is decidable, a distance where it
       carries one, and the type of the identity law's result, `Bool` or `Cost`, says which (L9);
       how a certified identity composes along a path is L10.7. [proposed]
References: D-2026-10-11-m
Rests on:   O2 (the equality a type comes with)
Quote:      (L16) "luego de <- lh == rh, de hecho creo que es la ley de <-" (reply, 18da042) (L21,
            the identity clauses) "verificar bit a bit que sea igual ... por lo menos sabés que no
            cambia la implementación" (audio 08.58, 09:20 to 13:19); the statistical kind for
            "prueba científica" (same)
Source:     (L16) Luciano, 2026-05-30 (day:2026-05-30:niveles-de-equivalencia); the law of a binding
            2026-10-11 (reply, 18da042) (L21, the identity clauses) Luciano, 2026-10-11 (WhatsApp
            Ptt 2026-10-11 at 08.58.46.md, 09:20 to 13:19); his annotation on draft 2 (2c18c41); his
            annotation on draft 8 (bcdac41)
Status:     settled; clause 3 proposed
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
            2026-10-12 on the reorder plan, proposed. draft 11, step 3 (2026-10-12): the formulation
            split into numbered clauses with the status each sentence had in draft 10, the examples
            into Example, the provenance phrases into this History, the wording otherwise as draft
            10 had it. clause 5 is his note of 2026-10-12 on the reorder plan put in words, and what
            L13.7 states for the planner's paths. draft 11, step 4 (2026-10-12): the binding-acts
            clause (2) moved to L9, the identity-law clause (4) to L13, the composition clause (5)
            to L16.7 with its intersection rule deleted (D-2026-10-12-q); clause 3 written in their
            place. draft 11 (2026-10-12): renumbered from L5 of draft 10 (D-2026-10-12-v).

L4  A program is a DAG of definitions without effects, and statements commute; actions have effects,
    and are verified by observing the world before and after.
From:       G0, the demand (the DAG is what the demand walks backward) with G2 (the second
            structure's metric); a definition without effects is G0, the demand's precondition
            rather than its consequence: the declarative face can be universal and minimally
            processed only if definitions have no effects; the separation of the second structure is
            the model's proposal
L4.1   The unit is the definition; dependencies give the only order there is, and time is
       reconstructed from them rather than from the text. [settled]
L4.2   Inside a block the text fixes which binding a name means, each `<-` a fresh name
       (D-2026-10-11-i), and then dependencies give the only order. [settled]
L4.3   (His annotation) The binding acts are two, `:=` once and `<-` rebinding, and they share one
       law: after the act the name equals the term in the equality its type has, structural `==`
       where it exists (spec 4.R8), observational otherwise, a distance under G2; after `:=` for all
       time, after `<-` until the next `<-` (spec 4.R12). [settled]
L4.4   Operations are declared before their laws, so a law that binds two operations is a node with
       two parents, not a cycle. [settled]
L4.5   A mutable parameter is two variables, before and after, so it is not an effect, the
       dependence is an edge, and mutation in place is the planner's optimization when the earlier
       one has no other consumer; what is forbidden is what the graph does not show. [settled]
L4.6   The DAG says what depends on what; the structure the laws generate over terms (an equivalence
       when laws are boolean, a metric space when they carry a distance) is a second structure,
       where L6 and the verification of actions (clause 9) live. [settled]
L4.7   A definition's result depends only on its inputs; effects live only in the actions (print,
       save). It is the one assumption under which every evaluation strategy gives the same result;
       over a carrier with a distance, a result in the same class at a distance the plan records,
       and for the Boolean case this is `Confluent` in `lib/plan.lut`, a law a dataflow is certified
       against rather than a theorem assumed. [settled]
L4.8   (His words) No effect on the world; its one effect is on the program: it takes its name,
       once, and enters the map of definitions, so the same name is not defined twice (`:=` once;
       `<-` only in a block, D-2026-10-11-i). [settled]
L4.9   (His annotation) Executing is the executive face: an action changes the state of the world,
       and it is verified too, by observing the world before and after it; the laws over actions are
       stated over those two observations, as a mutable parameter is two variables (clause 5).
       [settled]
L4.10  An observation is itself an action, so this stops where the world can be read back (a file
       written and reread), and says nothing beyond; an effect on state Luthier owns is verified
       this way, an irreversible or concurrent effect outside it is typed, logged and audited, never
       verified. [settled]
L4.11  An action on Luthier's own state, writing a certificate or running a test, is idempotent and
       memoizable; an action on the world never is: the world is an opaque, unique value, so an
       action on it is never served from the memo (D-2026-10-12-m, O3). Unique is meant literally:
       the world is `W`, a primitive of the core beside `U`, with no introduction (it enters at
       `main` or the session), no `==`, and each value of it used once (D-2026-10-13-b). [settled]
L4.12  There is one world. Its parts, a file or a clock, are parts of Luthier's representation of
       it, and whether two of them are independent is a theory of that representation, written in
       a library and certified like any law; the language imposes no partition. Two actions on the
       world commute only where such a certified law says so, and only over what can be read back
       (clause 10) (D-2026-10-13-a). [settled]
Example:    after `x <- 1`, `y := x + 10`, `x <- 2`, y is 11, as the session answers (clause 2)
References: spec 4.R12, spec 4.R8; D-2026-10-11-i, D-2026-10-12-m
Rests on:   O3 (the world as a value)
Quote:      (L18) "lo que si es no-side effects" (chat, 2026-10-10)
Source:     (L9) Luciano, 2026-05-29 (note:2026-05-29T14.46.22:contexto-como-dag); the unordered set
            of definitions already in 2023-03-13 (written:2023-03-13_hacia-luthier); the two
            structures and the mutable parameters 2026-10-10 (chat; D-2026-10-10-e) (L18) Luciano,
            2026-10-10 (chat; D-2026-10-10-c); his annotation on draft 8, bcdac41
Status:     settled; clauses 11 and 12 on his mark (D-2026-10-13-e)
History:    (L9) draft 0 (6d9dbd3): stated. draft 2 (cd24137): the two structures. draft 5
            (5b1446c): inside a block the text fixes the binding (D-2026-10-11-i). (L18) draft 1
            (5769005): stated. draft 4 (c7c6396): `Confluent` as the law a dataflow is certified
            against. draft 9 (0636378), his words: the one effect, on the program. draft 10
            (72cc7be, 81c1794, 25f9c5e, b7a7e23): the former L9 and L18 merged. draft 11, step 3
            (2026-10-12): the formulation split into numbered clauses with the status each sentence
            had in draft 10, the examples into Example, the provenance phrases into this History,
            the wording otherwise as draft 10 had it. clause 4 joins the two sentences of draft 10
            on the mutable parameter, which said the same thing twice. draft 11, step 4
            (2026-10-12): L11 (an action is verified by observing the world before and after it)
            merged in as clauses 9 and 10, the binding acts of L5.2 as clause 3, clause 11 on
            actions on Luthier's own state written (D-2026-10-12-m) (absorbed L11) From: G0
            (identity is the first proposition; his "path equivalence is the fundamental concept",
            2026-05-29); the two faces are G0, the demand's statement; the verification of actions
            from G1 (observation) and G0, the demand Quote: "la matemática no ejecuta ... la
            ejecución en Luthier sería esa verificación de equivalencias" (2026-05-30) "una funcion
            genera equivalencias f(a)==f(b) ==> a~b y mas si f(a)=true" (chat, 2026-10-11) "las
            ejecuciones tambien se verifican observando el mundo antes y despues del acto"
            (annotation on draft 2, 2c18c41) Source: Luciano, 2026-05-30; the kernel reading
            2026-10-11 (chat); the actions 2026-10-11 (annotation on draft 2, 2c18c41) Status:
            settled History: draft 0 (6d9dbd3): stated. draft 2 (cd24137), addenda 7 and 8: the
            kernel of a function as the equivalence on its domain. draft 3 (c085ba4), his
            annotation: actions verified by observing the world before and after. draft 4 (c7c6396):
            an observation is an action; stops where the world can be read back. draft 5 (5b1446c):
            the kernel reading is an interpretation, not the mechanism; a name only where a normal
            form exists (formerly under G4). draft 6 (8809e20): effects outside Luthier typed,
            logged and audited. draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): renumbered from L12;
            shortened on his note of 2026-10-12: evaluation and execution are in Terms, the reading
            of computation as the kernel of a function stays in this record (History below). the
            reading dropped from the projection at draft 10: Luthier first describes the problem and
            its equivalences; evaluating is checking them, as mathematics verifies rather than runs.
            (His annotation) Executing is the executive face: an action changes the state of the
            world, and it is verified too, by observing the world before and after it; the laws over
            actions are stated over those two observations, as a mutable parameter is two variables
            (L9). An observation is itself an action, so this stops where the world can be read back
            (a file written and reread), and says nothing beyond; an effect on state Luthier owns is
            verified this way, an irreversible or concurrent effect outside it is typed, logged and
            audited, never verified. Every function induces an equivalence on its domain, its
            kernel, so computing f(x) is placing x in its class and the value is the class's name:
            an interpretation of computation, not the evaluator's mechanism, and a name exists only
            where a normal form does, the decidable fragment (no canonical form elsewhere); a
            predicate is the two-class case and `Maybe T` places x in one of them. This equivalence
            on the domain is distinct from the equivalence between terms that a law induces, which
            is L10's quotient. draft 11, step 3 (2026-10-12): the formulation split into numbered
            clauses with the status each sentence had in draft 10, the examples into Example, the
            provenance phrases into this History, the wording otherwise as draft 10 had it.
            shortened at draft 10 on his note of 2026-10-12: evaluation and execution are in Terms,
            the reading of computation as the kernel of a function stays in this History. draft 11
            (2026-10-12): renumbered from L9 of draft 10 (D-2026-10-12-v).

L5  The demand determines the computation and the types produced; the meaning of a program, its
    realization under a plan and its evidence are three objects, never one.
From:       G0, the demand directly; the audio of 08.58 (15:35 to 17:12, 30:37 to 31:21) adds the
            iteration step, read every demand, run, collapse to the outputs, write, and asks whether
            the code object is consumed or stable: kept; with G1 for what is derived (the former L6)
L5.1   The declarative face states what is known, universal and minimally processed; the executive
       face is a demand from outside, and the demanded type fixes the path, the types and the
       tolerances actually produced. [settled]
L5.2   The evaluation strategy is a parameter separate from the program (clause 18); by default, a
       plan backward from the actions over names, evaluating nothing, then a strict forward run over
       the live subgraph, each node once and whole: forward on demand. [settled]
L5.3   What the action asks for flows backward along the plan and is produced forward: the value,
       its error, its derivative, its test, the type of its result; at the leaves a value lifts on
       its own, takes a mark given with the demand, or is a hole. [settled]
L5.4   A decoration of the output is another model of the theory the code was written over (G1): run
       over dual numbers the code gives its derivative, run over intervals or over pairs of value
       and cost it gives its error; the demand choosing the output type is the demand choosing the
       model, and the planner inserts the bridges (L6). The derivative needs nothing new; the error
       waits for the algebra of costs (O1, O5). [proposed]
L5.5   The tests are actions, so verifying is demanding; what a demand requires of the certificates
       in its cone, and when a certificate serves it, is L10.5 and L10.6. [settled]
L5.6   A result is identified by code, inputs, mode, the demanded type and tolerance, the model its
       type names (Terms), the seed, the plan that produced it, the plan being a value
       (`lib/plan.lut`), and the hashes of the certificates in its live cone, so a host library or
       platform that changed is a new result. [settled]
L5.7   The runtime includes the thread count and scheduling of the host, and an extern whose bits
       depend on scheduling is not bit-identical to itself, so its identity law is `Cost`, never
       `Bool` (L3). [settled]
L5.8   The run database is what the planner reads to choose the plan and is not an input of the
       result once the plan is fixed; evidence accumulates by a separate action with its own record,
       so "each node once" and G2's "kept across runs" never meet on one node. [settled]
L5.9   A test is an action whose result is a certificate (L10.4), rerun when asked or when the
       certificate's identity changed; "each node once" is once per plan: a stricter demand on the
       same definition is another node of another plan, and the looser certificate still serves what
       it met. [settled]
L5.10  The meaning of a program is the class its laws fix; a realization is the result under a plan;
       the evidence is its certificates (L10): three objects, never one. [settled]
L5.11  Two sessions that differ only in the order of independent bindings are equivalent by
       `Confluent` (L4), the law the session block is certified against. [settled]
L5.12  The program is the synthesis and is kept, the computation is the expansion and is redone.
       Script and interpreter are the same under this L, one batch of demands or demands one at a
       time with the memo between them (spec 8, O8); a session is a block and a file is never one,
       so a session saved to a file becomes its `main` block (D-2026-10-11-i). [settled]
L5.13  What is produced, and which types, is what the demanded value needs; what it does not need,
       the complement of its dependency cone, is not produced, so the choice is canonical, one per
       demand, and the types being spoken are what was asked for. [settled]
L5.14  Not producing at run time (a node freed after its last consumer) and not carrying in the type
       (how much history a certificate keeps) are one; the program is always kept, only what leaves
       scope is lost; not producing is not materializing a derived value, never erasing what
       reconstructs or recertifies it (code, inputs, model, seed, plan, tolerance), which the memo's
       identity keeps. [settled]
L5.15  A function on a type applied to a subtype does not produce one overload per subtype; the
       demanded return type selects which law to derive by composition (G1, O4), and the rest is not
       produced. [settled]
L5.16  What is derivable is a property of the expression, independent of the demand; the demand
       chooses which of it is derived, certified and carried, so the elaboration (types, derivable
       laws) does not depend on the observer; the memo of results does, and they are two caches.
       [settled]
L5.17  The demand carries the cutoff: the minimal cutoff for a specimen to be considered, applied to
       the composed bound and the composed evidence cost of a path (D-2026-10-12-h, L10.5); a cutoff
       does not compose (L12.3), so it lives in the demand and is passed down from it, and no law
       carries one. [proposed]
L5.18  No unrecorded policy constants: thresholds, budgets, limits, statistical levels and the
       planner's default policies are never constants in code; they are declared, passed and
       recorded. The kernel's primitives (0, ∞, `lift`, `exact`) and mathematical constants are not
       policies (D-2026-10-12-n). [proposed]
L5.19  The outermost demand, an action with no caller, carries its tolerance as a declared default
       argument (D-2026-10-11-c), recorded with the call, so there is a root and it is a parameter.
       [settled]
Example:    doubling positives is positive only when positivity is demanded and derivable, sin of
            positives is only Real because no law composes (clause 15)
References: spec 3; D-2026-10-11-c, D-2026-10-11-i, D-2026-10-12-h, D-2026-10-12-n
Rests on:   O1 (the error decoration), O3 (the world as a value), O5, O8, O12
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
Status:     settled; clause 4 proposed on his note on Terms; clauses 17 and 18 proposed
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
            on his note of 2026-10-12. draft 11, step 3 (2026-10-12): the formulation split into
            numbered clauses with the status each sentence had in draft 10, the examples into
            Example, the provenance phrases into this History, the wording otherwise as draft 10 had
            it. clause 1 is G3 of draft 10, the demand defines what is computed, read here as its
            own status asked; the identity of a result (6), the memo gate (7) and the three objects
            (12) are the model's, from the rounds of critiques; the three cases at the leaves (3)
            and the memo key are the model's, accepted; clause 15's source is audio 08.58, 17:12 to
            23:35; the former L13 restated without the forgetful functor on his note of 2026-10-12
            (16 to 19). draft 11, step 4 (2026-10-12): L12 (no hardcoded constants) merged in as
            clauses 18 and 19, clause 18 reworded to "no unrecorded policy constants"
            (D-2026-10-12-n); the cutoff clause 17 written (D-2026-10-12-h); the three objects
            raised to the statement; the memo gate (7), the certificate's identity (10) and the
            frozen snapshot (13) moved to L16.4 and L16.5, clauses 5 and 9 citing them (absorbed
            L12) From: G0, the demand (the tolerance belongs to the demand) and G2 (a law states a
            distance, not a threshold), so a constant in the code has no place to live; restates P11
            (every criterion is a parameter, never a constant in the code) Source: P11, in force;
            first applied as a rule of the language 2026-10-05
            (dialogue:c7437496:lmmaxiter-should-be-a-parameter) Status: settled; statement in his
            words, 2026-10-12 History: draft 0 (6d9dbd3): stated. Draft 0 of the generative plan
            proposed moving it to the way of working; withdrawn (D3). draft 6 (8809e20): the
            outermost demand's default argument. draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23):
            renumbered from L17; statement in his words, 2026-10-12. draft 11, step 3 (2026-10-12):
            the formulation split into numbered clauses with the status each sentence had in draft
            10, the examples into Example, the provenance phrases into this History, the wording
            otherwise as draft 10 had it. draft 11, step 4 (2026-10-12): vocabulary pass
            (D-2026-10-12-l): structure for a kernel type, theory for a Luthier type, cost for the
            law and resources for time and memory, model for what a type names and specimen for the
            planner's candidates; applied where the old word stood. draft 11 (2026-10-12):
            renumbered from L10 of draft 10 (D-2026-10-12-v).

L6  One function, many specimens, chosen by maximizing the performance the demander chooses, along
    certified identities.
From:       G0 (the quotient), G2 (the choice by cost and the database of runs) and, before its
            retirement in draft 9, the organizer "expressive over restrictive" (every path
            expressible; now L6's own clause)
L6.1   A function has many equivalent implementations, its specimens, each with its precision,
       speed, memory and place of execution; equivalence is established first, and the choice among
       paths follows expected loss and resources, estimated from a database of measured runs.
       [settled]
L6.2   The cost of a law and the resources of a run, time and memory, are not one scalar, and the
       trade-off among them is a parameter of the demand (L5), never the planner's own. [settled]
L6.3   (His formula) What the planner ranks is an efficiency, exp(−cost) over the resources used, so
       that a specimen of cost zero has efficiency 1/resources and not zero; the weight between cost
       and resources, w, the demand's parameter, may enter as log(resources) added to the cost, so
       that the rank is cost + w·log resources, minimized, the same as exp(−cost)/resources^w
       (D-2026-10-12-u). [candidate]
L6.4   Two regimes: on a decidable carrier (`Int`, `Fin n`) two implementations compute the same
       function or not, the quotient is exact, there is no precision to trade and the Boolean kernel
       stands on its own; on a carrier with a distance (`Float64`) they are interchangeable only up
       to a distance within the demanded tolerance, and precision can be traded for resources, which
       is where cost (G2) and the demand enter G0's quotient. [settled]
L6.5   Semantic equivalence forms classes; certified substitutability forms a graph. In the theory
       the specimens of a function are the quotient by "compute the same function up to the law's
       equality", one class per mathematical function, the class chosen by law; in a model that
       carries a distance closeness is not transitive, there is no class, only the ball of the
       demanded radius (`11` §3), and the planner substitutes one specimen for another only along a
       certified identity between the two, the identity law of L3 with its result `Bool` or `Cost`
       (D-2026-10-11-m). [proposed]
L6.6   The law gives the candidates; the identity certificates say which the planner may exchange,
       and they form a weighted graph: a substitution is a path whose summed distance (`11` §2) and
       summed evidence cost (L10.7) are within the demand's cutoff, so two specimens joined through
       a third may each replace it and not each other; a lone specimen is never replaced. [proposed]
L6.7   A sampled edge is admissible on the distribution it sampled; it composes with edges sampled
       over the same distribution, the failure fractions summed, and not with others; the demand's
       evidence cutoff says whether it accepts the path (L10.8, D-2026-10-12-q). [proposed]
L6.8   The tolerance charged at a node is the demand's pulled back through the sensitivity of the
       cone from the node to the demand (`11` §5), and where no sensitivity is known there is no
       substitution. [settled]
L6.9   A link certified on a subtype is a link only at inputs certified (L8) in that subtype, so a
       path exists at x only where every link does; a `proved` link by citation carries the
       theorem's hypotheses as parameters and is void where they fail. [settled]
L6.10  The author's free choice among the inhabitants of an under-determined function
       (D-2026-10-11-d, P5) stays; the planner's choice is only among what has been compared.
       [settled]
L6.11  The identity law between two specimens, with its distance, is what admits a second
       implementation into the planner's graph (D-2026-10-11-m); the agreement test of W5 between
       native and extern is this law, and the reference formula of a law evaluated over `Rational`
       is one more specimen, with grade exact, checked by the same law. [candidate]
L6.12  An importer sees a module only through the theory it gives the module as type, so the
       module's representation stays private and another model of the same theory can take its place
       without the importer noticing; privacy is ascription, not a keyword (D-2026-10-13-c).
       [settled]
L6.13  An algorithm is written against a theory, never against a model: it is a functor that takes
       any model of the theory, so each specimen can stand in for another, and it is certified per
       instance unless a cited proof covers every model (D-2026-10-13-j). [settled]
L6.14  An import line names what enters with its theory, `import "x.lut" M : T`, so the importer is
       checked against `T` without reading `x.lut`, and the ascription of clause 12 happens there
       (Z5 of the plan from zero; the theory itself imported from a theory file first,
       D-2026-10-13-n). [settled]
Example:    γ_n needs n·u < 1, false for float32 over an hour at 48 kHz, so the cited bound is void
            there (clause 9)
References: `11`; D-2026-10-11-d, D-2026-10-11-m, D-2026-10-12-q, D-2026-10-12-u; W5; P5
Rests on:   O1 (the sensitivity), O2
Source:     Luciano, 2022-06-28 (written:2022-06-28_luciano-code-style:choose-efficient-path-
            after-validity); the quotient 2026-10-10 (WhatsApp Ptt 2026-10-10 at 16.49.14.md, 00:04
            to 01:39), the same idea without the word 2026-05-30 (note:2026-05-30T18.01.53:
            equivalencias-para-clasificar-y-separar-decoraciones)
Status:     settled; statement in his words, 2026-10-12, with "specimens" and "along certified
            identities" added; clause 3 candidate on his mark (D-2026-10-12-u); clauses 5, 6, 7
            proposed; clause 11 candidate, from L3; clause 12 settled (D-2026-10-13-c, -e); clauses
            13 and 14 settled (D-2026-10-13-j, -n)
History:    draft 0 (6d9dbd3): stated. draft 2 (cd24137): stated as a quotient. draft 4 (c7c6396),
            D-2026-10-11-m: exact in the theory, a ball in the model; substitution only along a
            certified equivalence. draft 5 (5b1446c): a weighted graph, not a class; a lone
            implementation never replaced. draft 6 (8809e20): error, time and memory not one scalar.
            draft 7 (6a15cec, cd314a4): from the third round's counterexamples, a sampled edge only
            on covered inputs and only direct, the tolerance pulled back through the sensitivity;
            Claude's clause on subtypes and cited hypotheses. draft 9 (120a49a): G4 retired; "every
            path expressible" is L10's own clause. draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23):
            renumbered from L10; statement in his words, 2026-10-12; his formula for the efficiency,
            exp(−cost) over the resources, added (proposed wording). draft 11, step 3 (2026-10-12):
            the formulation split into numbered clauses with the status each sentence had in draft
            10, the examples into Example, the provenance phrases into this History, the wording
            otherwise as draft 10 had it. clauses 7, 8 and 10 (the weighted graph, the admissibility
            of sampled edges, the subtype and cited hypotheses) are the model's, from the rounds of
            critiques. draft 11, step 4 (2026-10-12): "never summed into a path" deleted
            (D-2026-10-12-q); the quotient and the ball joined into clause 5 with GPT sp's wording;
            the sum now a bound with its evidence cost (clause 6); cost reserved for the law and
            resources for time and memory (D-2026-10-12-l); the weight named in his formula; the
            identity-law clause of L5.4 joined as clause 11. draft 11 (2026-10-12), his mark: clause
            3 a candidate, with log(resources) added to the cost as the better form
            (D-2026-10-12-u). draft 11 (2026-10-12): renumbered from L13 of draft 10
            (D-2026-10-12-v).

L7  The core is minimal, executable by hand, and its programs are data.
From:       G0 (a type theory is a few rules whose judgments a person checks; a small trusted
            kernel) and G1 (the paper semantics is the description, and every interpreter is a
            specimen certified against it); programs as data from G0 through the universe, the type
            of types (the object classifier of HoTT; the note's "object classifier" names this when
            it means types as values, and the subobject classifier when it means G2's truth values)
L7.1   A handful of well-specified primitives, so that a program can be run with pencil and paper;
       everything else is a library whose translation to the core is mechanical. [settled]
L7.2   Hand execution is of the kernel given a plan, an order of execution that is a value
       (`lib/plan.lut`); the planner's choice among plans is outside the kernel. [settled]
L7.3   Four layers, each trusted differently: the kernel, checked by hand; the libraries and the
       interpreter in Luthier, certified against the kernel's laws; the host runtime, a specimen;
       the planner, advice that the plan records. The five certifiers of L9.1 are kernel: names of
       core the checker recognizes, as `extern` and `axiom`, checked by hand (D-2026-10-13-d, -e).
       [settled]
L7.4   A Luthier program is an element of Luthier; programs build, inspect and run other programs,
       and the interpreter is meant to be written in the language it interprets. [settled]
L7.5   What a library can decide, the core does not: the core asks of each library the fewest
       operations and laws it uses (for costs, spec 6.S5), and the open choices of the library are
       taken when it is implemented and its invariants are found (D-2026-10-12-al, P16).
       [settled]
Rests on:   O11 (the kernel's theory stated in Luthier)
Quote:      (L7) "Luthier tendría que ser ejecutable a mano" (2026-05-29)
Source:     (L6) Luciano, 2022-06-15 (written:2022-06-15_sin-titulo-2:codigo-es-dato) (L7) Luciano,
            2026-05-29
Status:     settled; clause 5 on his mark (D-2026-10-13-e)
History:    (L6) draft 1 (5769005): stated. (L7) draft 0 (6d9dbd3): stated. Draft 0 of the
            generative plan proposed moving it to the way of working; withdrawn (D3). draft 4
            (c7c6396): hand execution is of the kernel given a plan. draft 6 (8809e20): the four
            layers of trust. draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): the former L6 and L7
            merged. draft 11, step 3 (2026-10-12): the formulation split into numbered clauses with
            the status each sentence had in draft 10, the examples into Example, the provenance
            phrases into this History, the wording otherwise as draft 10 had it. draft 11
            (2026-10-12): renumbered from L15 of draft 10 (D-2026-10-12-v).

L14 What can be written in Luthier is written in Luthier.
From:       G0 (a type theory states its own rules in its own terms; L7, programs are data and the
            interpreter is written in the language it interprets) with G1 (the host's implementation
            is a specimen certified against the statement in Luthier); his principle, on his comment
            on D8 of the specification plan
L14.1  The specification of how Luthier runs is written in Luthier where the kernel can express it:
       a theory with its laws, whose models and counter-models are the accept and reject programs of
       the suite; the prose explains, it does not define. [proposed]
L14.2  The libraries' theories, the generators, the plan, the certificate and the program itself
       (`Program`, `Term` as data) are values of Luthier, stated with their laws before they are
       implemented. [proposed]
L14.3  The host implements what Luthier states and is a specimen of it, certified against the
       statement like any other model (L7.3, L9); two orders of bootstrapping are two paths to the
       same theory, a minimal kernel in Python with the rest in Luthier, or theory and testing in
       Luthier with everything implemented in Python, and the agreement of the two is the law W5
       names. [proposed]
L14.4  What the kernel cannot yet express is written in the host and marked as such, a hole of the
       theory it belongs to (L2), so that the boundary of "where it can" is visible and shrinks with
       each version. [proposed]
L14.5  (His words) Keyword or not, the semantics of every construct is expressible in Luthier: a
       keyword is surface syntax, and what it means is stated as a theory in Luthier (`match` and
       `data` by the laws of the kernel, `if` as a `match` on `Bool`); every other construct is a
       name of core or of a library, with named arguments for its options (D-2026-10-12-ab).
       [proposed]
L14.6  Of the two orders of bootstrapping, the theory comes first: Luthier's theories are written
       in Luthier before any implementation, they are the authority, and the host's files and later
       the Luthier implementations are their specimens, written after them and certified against
       them (D-2026-10-13-h). The theory is not frozen: a specimen that shows it wrong, a false
       positive for one, is evidence against it, and the theory is refined (D-2026-10-13-n).
       [settled]
Rests on:   O11 (the kernel's theory stated in Luthier); `Program` and `Term` as data, decided for
            version 0 in chat on 2026-10-12, to be specified in chapter 3
Quote:      "necesitamos una teoria de librerias, la iremos haciendo a medida que la necesitemos.
            Pero tiene que ser una teoria escrita en luthier. Aqui algo que es un principio de
            luthier: todas las especificaciones de como se corre luthier tienen que estar escritas
            en luthier, de ser esto posible. La implementacion puede ser en python, of course y
            podemos intentar ambos caminos: nucleo minimo en python e implementacion en luthier y lo
            contrario, solo teoria y testeo en luthier y todo implementado en python." (his comment
            on D8, a066adc) "Y podemos agregar el principle de que si se puede se escribe en
            Luthier" (chat, 2026-10-12)
Source:     record/plan-spec-2026-10-12-decisions.md, his comment on D8 (a066adc); chat 2026-10-12;
            the precedents W2 (the specification is an executable suite), W5 (concepts live in
            Luthier, execution in the host), L7.4, `lib/kernel_laws.lut`, `lib/plan.lut`, 08
            (generators are values)
Status:     his principle, stated in his words; the clauses are the model's wording, proposed, his
            mark pending; placed under G0 after L7 and numbered L14 until the next renumbering by
            document order (D-2026-10-12-v); clause 6 settled (D-2026-10-13-h, -n)
History:    draft 11 (2026-10-12): new, on his comments on the specification plan (D8) and his
            request in chat; the decisions it already guided: D8 of the spec plan, W5's restatement,
            the decision to put `Program` and `Term` as data in version 0.
```

### Under G1, theory and model

```
L8  A type is a proposition, membership is a guarantee, and the certified subtype from a law is the
    fundamental construction pattern.
From:       G0 directly; the second clause is the step to G1
L8.1   Belonging to a type asserts the propositions, laws included, that the value satisfies;
       function types carry their laws the same way. [settled]
L8.2   `a : A` is one judgment, structural and decidable for the kernel's structures; it asserts the
       structural proposition outright and the laws through the certificate, with the evidence the
       certificate has. [settled]
L8.3   A value with a sampled or assumed certificate is a model of its theory with the cost its
       certificate records (D-2026-10-12-j); "guarantee" means what the evidence says, and the word
       model promises the evidence, not exactness. [proposed]
L8.4   What a law adds is evidence, recorded in a certificate (L10); what leaves the program carries
       one (L10.6, D-2026-10-11-n). [settled]
L8.5   From a material type and a law, a predicate or a cost with its tolerance, come the certified
       type, its only constructor and the forgetful projection; the same pattern builds values,
       functions and programs. [settled]
L8.6   A law gives the three at once: the type, the constructor with Maybe, the membership function.
       [settled]
L8.7   Where the law is into `Cost`, the certificate records the bound it observed, and the demand's
       cutoff decides whether it serves (L10.5, D-2026-10-12-h); the constructor takes no tolerance.
       [proposed]
L8.8   Types are verified before they are constructed: Luthier starts from types by verification,
       and types by construction may come in later. [settled]
L8.9   Everything has laws, at the least those of its equality (D-2026-10-12-ak): there is no data
       without them. What comes from the world enters as bytes or a `String`, whose laws are the
       kernel's, and a check refines it once into its lawful type (spec 5.S9, 5.S12;
       D-2026-10-06-aa, D-2026-10-13-j). `W`, which has no `==`, is a structure: a thousand laws
       are associated with it, the observations of what actions do, and none of them defines it
       (D-2026-10-13-n). [settled]
References: D-2026-10-11-n, D-2026-10-12-h, D-2026-10-12-j
Rests on:   O1 (the bound in a certificate)
Source:     Luciano, 2022-08-03 (written:2022-08-03_haskell:proposicion-que-cada-tipo-cumple);
            restated 2026-05-26 (day:2026-05-26:tipos-como-conceptos-y-proposiciones)
Status:     settled; clauses 3 and 7 proposed (D-2026-10-12-j, -h); clause 9 settled
            (D-2026-10-13-j, -n); "from a law" is his correction
            of 2026-10-12
History:    draft 1 (5769005): stated. draft 4 (c7c6396): one judgment, structural; the certificate
            carries the grade and the worst cost; what leaves the program carries a certificate
            (D-2026-10-11-n). draft 6 (8809e20): what "guarantee" means at each grade. draft 10
            (72cc7be, 81c1794, 25f9c5e, b7a7e23): number kept. draft 11, step 3 (2026-10-12): the
            formulation split into numbered clauses with the status each sentence had in draft 10,
            the examples into Example, the provenance phrases into this History, the wording
            otherwise as draft 10 had it. the grade list deleted here, defined in Terms. draft 11,
            step 4 (2026-10-12): L3 (the certified subtype from a law) merged in as clauses 5 to 8;
            clause 3 written on D-2026-10-12-j; the grade meanings of draft 10's clause 3 are now
            L16.2; the tolerance left the constructor (D-2026-10-12-h) (absorbed L3) From: G0 (a law
            is a proposition; its subtype is the type of its proofs) with G1 (verified, not
            constructed) Source: Luciano, 2022-08-03
            (written:2022-08-03_haskell:subtipos-con-predicado); named fundamental 2026-09-29
            (record/distillation/2026-10-09_find_principles_v2_claude-code_ opus.md, C3); the three
            things and the scope 2026-10-10 (WhatsApp Ptt 2026-10-10 at 10.12.21.md, 05:24 to 08:10)
            Status: settled; "from a law" is his correction of 2026-10-12 History: draft 1
            (5769005): stated. draft 4 (c7c6396): the tolerance a parameter of the constructor,
            recorded in the certificate. draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): renumbered
            from L4; "from a law" is his correction of 2026-10-12. draft 11, step 3 (2026-10-12):
            the formulation split into numbered clauses with the status each sentence had in draft
            10, the examples into Example, the provenance phrases into this History, the wording
            otherwise as draft 10 had it. draft 11 (2026-10-12): renumbered from L2 of draft 10
            (D-2026-10-12-v).

L9  A law characterizes; a certifier produces its evidence, exact or statistical; and the
    certificate of identity is not the certificate of the law.
From:       G0 (a law defines the object) and G1 (a law that transcribes the specimen is
            acquaintance, not description; observation is how a description is verified) with G2
            (the grade is the uncertainty of the cost); extends P10 (the mathematical object that
            best represents a concept is the invariant of its type)
L9.1   A law is the proposition; a certifier is a method that produces evidence for it, and one law
       may have several: a theorem cited, an exhaustive run, chosen cases, a sample, an assumption
       (D-2026-10-12-k). The law is not the procedure that checks it, and a universal law over an
       infinite carrier has no certifier that runs it. [proposed]
L9.2   A law states a mathematical property of an operation; a second implementation checked against
       the first is consistency, and the native definition is one more model certified against the
       law. [settled]
L9.3   A law over several functions is tested on the values actually computed, as a puzzle whose
       pieces must fit; the cases to test are chosen by the law, its arity (three elements for
       associativity) and the distribution sampled, never every path. [settled]
L9.4   Laws accumulate, and a law need not determine the operation; when the laws do determine it up
       to the presentation's equality, that is the limit (D-2026-10-11-d). [settled]
L9.5   The certifier is chosen by what the law admits: what is known by a theorem is cited, what can
       be enumerated is checked exhaustively, what has chosen cases is checked on them, what can
       only be sampled is checked statistically; the evidence travels with the value in a
       certificate (L10). The line is the method, since associativity over `Int` is computable and
       cannot be checked by running. [settled]
L9.6   The grade of a sampled certificate depends on the distribution sampled, not only on the
       number of samples, because errors concentrate at the edges. [settled]
L9.7   Verification by a theorem is `proved` by citation (D-2026-10-11-f); verification by
       delegation is the same certifier with the host library's guarantee as the theorem cited
       (LAPACK's backward-error bounds, the condition number their hypothesis) and the library's
       version and platform as hypotheses the certificate carries; no new grade. A function known
       correct by a theorem outside Luthier is certified this way, and the chain law, citation,
       native, identity, extern is carried by hash. [proposed]
L9.8   Checking that an implementation gives the same bits as before, with the same seed, certifies
       that the implementation has not changed; checking it against its laws, by chosen or sampled
       cases, certifies the description. Both are kept, apart. [settled]
L9.9   (His annotation) The certificate of the law travels by the certificate of identity (L10.7):
       exactly where the identity is boolean (`==` structural, spec 4.R8: integers, decidable types,
       the same implementation rerun), and with the observed distance added where it is a cost (G2),
       since two implementations over floats are almost never bit-identical; the type of the
       identity law's result says which (`Bool` or `Cost`). [settled]
L9.10  A certifier is a value, as a generator is (D-2026-10-06-ab): the five of clause 1 are
       primitive, and any other is a value of the theory `Certifier`, certified against its own law,
       its level on laws that hold and its power on controls (spec 7.S17 to 7.S19); a certificate it
       emits carries the certifier's own certificate in its cone, and the evidence composes (spec
       6.S12). Certification is not a keyword (D-2026-10-13-d). [settled]
L9.11  A law is a theory: its predicate presents it, `forall` and `exists` and the connectives form
       it, and its models are its evidence, which follows its form: a case is evaluated, a `forall`
       is covered exhaustively, by listed cases or by a sample, an `exists` by a witness with its
       cost, `and` by both sides and `or` by one; a citation or an assumption covers any part whole
       (D-2026-10-13-l). [settled]
L9.12  The two quantifiers are dual in their evidence: a `forall` is refuted exactly by a
       counterexample and, over an infinite domain, confirmed only by statistics; an `exists` is
       confirmed by a witness whose cost is determinate rather than statistical, though over the
       reals not zero (D-2026-10-13-l). [settled]
L9.13  (His words) To design certificates, first see how the law fails: the evidence a law needs,
       and the certifier that produces it, are found on a real case and on the ways it fails, not
       chosen in advance; so a layer is run before its certification is designed (D-2026-10-13-ad).
       [settled]
References: spec 4.R8; D-2026-10-11-d, D-2026-10-11-f, D-2026-10-12-k, D-2026-10-13-d, D-2026-10-13-ad
Rests on:   O1 (what a sampled level asserts, and its conversion to a cost, D-2026-10-12-r)
Quote:      (L5) "La idea en realidad es buscar el objeto matematico que mejor lo represente y
            decirlo" (chat, 2026-10-05) (L11) "verificacion externa por teoremas o por delegacion
            (creo en Lapack)" (bcdac41) (L21, the distinction identity/law) "verificar bit a bit que
            sea igual ... por lo menos sabés que no cambia la implementación" (audio 08.58, 09:20 to
            13:19); the statistical kind for "prueba científica" (same) (L9.13) "Para diseñar los
            certificados primero tenemos que ver como falla." (chat, 2026-10-13)
Source:     (L5) Luciano, 2026-10-05 (chat:52d3e68e:2760); the puzzle 2026-10-10 (WhatsApp Ptt
            2026-10-10 at 10.12.21.md, 11:38 to 18:20) (L11) Luciano, 2022-08-03 and 2023-02-22
            (written:2023-02-22_tapp-wish-list:untested-a- tested); the grades by samples 2026-10-10
            (WhatsApp Ptt 2026-10-10 at 11.11.22.md, 03:02 to 04:12); his annotation on draft 8,
            bcdac41 (L21, the distinction identity/law) Luciano, 2026-10-11 (WhatsApp Ptt 2026-10-11
            at 08.58.46.md, 09:20 to 13:19); his annotation on draft 2 (2c18c41); his annotation on
            draft 8 (bcdac41) (L9.13) Luciano, 2026-10-13 (chat:52b10bff:5037)
Status:     settled; clause 1 proposed (D-2026-10-12-k); clause 7 proposed on his mark; clause 10
            settled (D-2026-10-13-d, -e); clauses 11 and 12 settled (D-2026-10-13-l, -n); clause 13
            settled (his words, on D-2026-10-13-ad; his ok, chat:52b10bff:5083)
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
            citation moved to L14. draft 11, step 3 (2026-10-12): the formulation split into
            numbered clauses with the status each sentence had in draft 10, the examples into
            Example, the provenance phrases into this History, the wording otherwise as draft 10 had
            it. the generators of clause 2 are the model's addition; clause 5 is the model's
            correction, from the practice of property-based testing; the grade list deleted here,
            defined in Terms. draft 11, step 4 (2026-10-12): clause 1 written on D-2026-10-12-k (GPT
            en's distinction); delegation as citation moved here from L14.8 as clause 7; clause 5
            reworded with the certifier and the grade list cited from Terms; clause 9 cites L16.7.
            draft 11 (2026-10-12): renumbered from L7 of draft 10 (D-2026-10-12-v).

L10 A certificate records what is known of a law, its domain, its bound and its evidence; it is
    frozen, it serves every demand it meets, and it transports along identity.
From:       G1 (a model is known by the law it satisfies, with the evidence it has) with G2
            (evidence is a cost) and G0, the demand (what the demand requires of the evidence is its
            own)
L10.1  A certificate (Terms) names the law it records as checked, the domain the check covered (a
       subtype, the cases listed, or the distribution sampled), the bound observed (for a law into
       `Cost`, the distance its `forall` gives over the costs seen, D-2026-10-13-m), and the evidence: its grade and, for a sampled check, the
       sample's statistics converted to an evidence cost (D-2026-10-12-r). [proposed]
L10.2  The grade is derived from the domain and the evidence cost: proved and exhaustive have
       evidence cost 0 on their domain; cases, 0 on the cases listed and ∞ outside; sampled, the
       finite cost of its statistics on the distribution sampled. An `assumed` certificate carries
       what is asserted and no check: a Boolean law asserted true, with bound 0, or a cost law
       asserted with a formula of the inputs, a library's documented bound such as p(n)·ε·κ(A), with
       the formula evaluated at the input as its bound; its evidence cost is the demand's parameter
       for assumptions, with no default, so that a demand that names none refuses assumed values
       (D-2026-10-11-n, D-2026-10-12-t). When the formula is a cited guarantee with its hypotheses,
       the certificate is proved by delegation (L9.7), not assumed. The five names stay in the
       certificate for the reader; the planner reads the costs. [proposed]
L10.3  The conversion from statistics to an evidence cost is a function with a declared shape, the
       sample's statistics and the demand's level in, a cost out, filled per theory
       (D-2026-10-12-r); the first instance is −log(1 − ε̂(n, δ)) in nats, with ε̂ the bound on the
       fraction of the distribution where the law's bound fails, from n samples at confidence 1 − δ,
       and δ the demand's parameter. [settled]
L10.4  A certificate is identified by a hash over its dependency cone (code, cases, seed, the
       distribution and level sampled); it is a frozen snapshot, and a later check does not change
       it but issues a new one that supersedes it, both kept, the latest in front (P3), so progress
       is the chain of certificates. [settled]
L10.5  A certificate serves every demand whose cutoff it meets, on the bound and on the evidence
       cost alike (D-2026-10-12-h); the demand states what it requires (P11), and a memo hit serves
       a demand only if the cached cone meets it, checked at the hit and not only when the
       certificate was issued. [settled]
L10.6  Certification is the default: demanding a value demands every certificate in its dependency
       cone, paid once through the memo, with no opt-out at the start (D-2026-10-12-y: a cone with
       an uncertified or provisional name is refused); an exception, if a real case asks for one, is
       O3 and would leave a certificate of grade `assumed` (D-2026-10-11-n); what never reaches an
       output needs no certificate, and what reaches one carries its cone's; `test` is the action
       that demands certificates without values (L5). [settled]
L10.7  Certification transports along identity: if B is certified on inputs X with bound b and
       evidence cost e, and the identity A ≡ B is certified on inputs Y with distance d and evidence
       cost e′, then A is certified on X ∩ Y with bound b + d and evidence cost e + e′, and by
       nothing else; a path of identities composes the same way, link by link, the distances summed
       and the evidence summed (D-2026-10-12-q). (His correction, in grades) A is certified at the
       weaker of the two grades on X ∩ Y. [proposed]
L10.8  Links sampled over different distributions do not compose without a law relating the
       distributions; links sampled over the same distribution compose by the union bound, the
       failure fractions summed, which is the probabilistic bound the planner waited for
       (D-2026-10-12-q). The composition algebra belongs to the theory's cost type, the sum its
       first instance; whether a demand accepts a sampled path is its evidence cutoff, a parameter
       (P11). [proposed]
L10.9  No operation on certificates raises a grade, lowers an evidence cost or widens a domain
       without new evidence. [settled]
L10.10 Only a certifier builds a certificate: the constructor of `Certificate` is in no interface
       outside the theory of certification (L6.12), so clause 9 is enforced by the language and not
       left to good conduct (D-2026-10-13-c); the precedent is the abstract type `thm` of the LCF
       provers, which only the kernel's rules build. [settled]
Example:    with B's laws only `assumed`, A inherits the cost of an assumption and nothing more; a
            lookup table equal to the native on a grid is certified on the grid and nowhere else
            (clause 7)
References: D-2026-10-11-n, D-2026-10-12-h, D-2026-10-12-q, D-2026-10-12-r, D-2026-10-12-t; P3, P11
Rests on:   O1 (the conversion and the algebra), O3 (the opt-out's syntax)
Quote:      "a is model of A with cost C, we pass the statistics to cost, we need a convertion.
            might be we work with logCost in nat." "The same, the conversion is expressed by a
            dedicated function and we might choose different functions on different theories.
            Luthier would ask for some input output shape, that the particular function is filled on
            each case." (his marks, e8d7db1, 57a0023)
Source:     the critiques of draft 10 (`record/IA/principles 2026 10 12/`, 1429f35: Claude, the
            certificate as the object every L leans on, scattered over L2, L5, L7, L10, L13, L14;
            GPT en, the calculus of evidence scope and the rule that no operation increases grade or
            domain without new evidence); his decisions D-2026-10-12-j, -q, -r; clauses 4 to 6 moved
            from L10.7, L10.10, L10.13, L10.5 and L14.5 of draft 11 step 3
Status:     proposed in draft 11; clauses 3 and 9 settled on his marks (D-2026-10-12-w); clauses 4
            to 6 settled, moved from L5 and L11; clause 2 reworded on D-2026-10-12-t; clause 7
            carries his correction of draft 7 in grades; clause 10 settled (D-2026-10-13-c, -e)
History:    draft 11, step 4 (2026-10-12): new entry, under G1, after L7. draft 11 (2026-10-12), his
            marks: clause 2 elaborated with the two kinds of assumption (D-2026-10-12-t); clauses 3
            and 9 marked ok (D-2026-10-12-w). draft 11 (2026-10-12): renumbered from L16 of draft 10
            (D-2026-10-12-v).

L11 Luthier orchestrates other languages: an extern is a specimen certified by its laws, and what
    does not follow Luthier's way lives in a world.
From:       G1: an absorbed library is a specimen known by its description, and its code is not
            needed ("que la IA pueda ... extraer de librerías ajenas, chuparlas y usar las funciones
            con sus propias invarianzas", audio 08.58, 31:25 to 32:00); the world from G0, the
            demand (the demand names the world it runs in) with L4; delegation (now L9.7) from G1
            and G2; transport (now L10.7) from G1
L11.1  Types and laws are native; values may come through `extern` from Python or any host, declared
       over what they really receive and return, with description and verification kept on Luthier's
       side. [settled]
L11.2  (His words, "si el tipo no sigue la ley no se aplica el calculo") An extern is declared over
       a type, a type carries its laws (L8), and the extern is validated against them, like any
       other function, the first time an action asks for it, before it is applied, and refused if it
       fails; its certificate stays by hash; without a type with a law to validate against it is not
       applied; the agreement test with the native is in addition (W5), and the planner's
       substitution is D-2026-10-11-m. [settled]
L11.3  A function with no laws at all is not a function to run but a hole of a theory being defined
       (L2). [settled]
L11.4  The extern's certificate binds the host library's version and the platform (W10), and its
       declaration says whether it is a definition or an action (L4). [settled]
L11.5  Luthier is in use a coupling language: the joint between two libraries is a theory of which
       each is a model, the bridges between representations live at the joint with their cost and
       error, and no coupling without a law. [settled]
L11.6  A definition or an implementation that does not follow Luthier's way, an extern with no law
       yet, a foreign algorithm taken as is, may execute inside a named world (L4): its certificates
       carry the cost of an assumption (L10.2), the plan shows the world it ran in, and nothing from
       it enters the planner's graph (L6) nor a certified theory until a law is certified.
       [candidate]
L11.7  (His words) A file is read when some demand needs it: an extern is a route to a function, its
       file opened only when a demand reaches the node, and not even required to exist when the
       program is checked; a module is a value, and its file is read when a demand first needs one
       of its names, so an import is not an action either; `test` of a module is the action that
       demands everything in it, the one that finds what is latent and ill defined (D-2026-10-12-ac,
       -ad). [settled]
References: D-2026-10-11-m; W5, W10
Rests on:   O3 (the opt-out's syntax; the world as a value)
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
Status:     settled by his correction of draft 7; clause 6 candidate, reworded; clause 7 settled
            (D-2026-10-13-g)
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
            correction) placed here on his note of 2026-10-12. draft 11, step 3 (2026-10-12): the
            formulation split into numbered clauses with the status each sentence had in draft 10,
            the examples into Example, the provenance phrases into this History, the wording
            otherwise as draft 10 had it. clause 2 joins the two sentences of draft 10 on validation
            before application, which said it twice; clause 8 joins the two on `proved` by citation;
            the two counterexamples of the example are Kimi's and Claude's, from the third round;
            delegation (clause 8) is from the former L11 and transport (clause 9) from the former
            L21, placed here on his note of 2026-10-12. draft 11, step 4 (2026-10-12): certification
            by default (5) moved to L16.6, delegation (8) to L7.7, the graded transport (9, his
            correction) to L16.7 with its example; clause 6 reworded so that an extern without a law
            executes in a world and enters neither the planner's graph nor a certified theory
            (DeepSeek, GPT en, GPT sp). draft 11 (2026-10-12): renumbered from L14 of draft 10
            (D-2026-10-12-v).
```

### Under G2, cost

```
L12 Laws combine, and a predicate lifts to a cost.
From:       G2 directly (lift, exact and within were named under it on his mark, draft 9) with G0,
            the demand (the cutoff lives in the demand)
L12.1  Predicates combine by and, or, then, and by a quantifier over a carrier, and the result is a
       predicate; costs combine by sum, max and weighted sum, and the result is a cost; a
       combination that mixes the two is a cost, each predicate lifted. [proposed]
L12.2  The lift is explicit and named: `lift : Bool -> Cost` sends true to 0 and false to ∞, `exact
       : Cost -> Bool` is c == 0, with `exact ∘ lift = id`, so `Bool` is a retract of `Cost`, not a
       subtype, and the planner inserts the lift as a bridge of cost zero; whether the two are
       homomorphisms waits for the algebra (O1), since Boolean or has no counterpart among the
       operations of `Cost` yet. [settled]
L12.3  The cutoff is the demand's (L5.17), passed down from it; it does not compose (two links
       within ε are within 2ε), so no law carries one. [proposed]
L12.4  `&`, the only join the libraries use today, is the Boolean and. [settled]
L12.5  The law of a theory is one law, so its certificate is one certificate; how the grades of its
       parts combine is the demand's parameter, the vector of grades or the weakest
       (D-2026-10-12-i); how the costs of its parts combine is the theory's algebra, with two
       candidate models, min and max, or 1/n log-sum-exp and 1/n sum (D-2026-10-12-p); the
       composition along a path is the sum (L10.7, D-2026-10-12-q). [proposed]
L12.6  Cost is two things (D-2026-10-13-m, -n). A distance says how far an approximate value is
       from the ideal; it composes by the triangle inequality, or by the worst link where it is
       ultrametric, and it is the one logic of G2: a law's value is a distance, and the demand's
       cutoff says whether it is enough. A probability, in a certificate, is that of a
       counterexample not yet seen: having drawn a million cases and found none, how likely one
       is; how such probabilities combine is an assumption about the dependence of what fails,
       nested (max) or independent and rare (sum, log-sum-exp). Bayesian evidence is neither: it is
       a likelihood, a density of any value, and its logarithm is not a cost in [0, ∞]. [proposed]
L12.7  `then` is material, `not (p and not q)`; conditioning is not a connective, since no
       connective has the conditional probability as its probability (Lewis, 1976), but an
       operation on a measure whose law is the chain rule. For distances, `then` is the triangle
       inequality, which is transport along an identity (L10.7) (D-2026-10-13-l, -m). [settled]
References: D-2026-10-12-i, D-2026-10-12-p, D-2026-10-12-q
Rests on:   O1 (the algebra of costs; the two candidate models, D-2026-10-12-p)
Source:     his note of 2026-10-12 on the reorder plan (14ea9f0)
Status:     proposed on his note of 2026-10-12; the names lift, exact and within his to rename;
            clause 2 settled on his mark (D-2026-10-12-w); clauses 3, 5 reworded on D-2026-10-12-h,
            -i, -p, -q; clause 6 proposed, rewritten on his correction, and clause 7
            settled (D-2026-10-13-l, -m, -n)
History:    draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23): new, on his note of 2026-10-12 on the
            plan ("faltan las leyes de los costos y de los predicates y cómo se lift a costos"); the
            text is the record's G3 of draft 9 (lift, exact, within) and the paragraph that stood in
            G2; the composed grade from the former L11. draft 11, step 3 (2026-10-12): the
            formulation split into numbered clauses with the status each sentence had in draft 10,
            the examples into Example, the provenance phrases into this History, the wording
            otherwise as draft 10 had it. clause 1 is the paragraph that stood in G2 at draft 10;
            clause 5 is the composed grade from the former L11, on his note on Terms; "a law is a
            predicate or a cost" deleted here, defined in Terms. draft 11, step 4 (2026-10-12):
            "homomorphisms" withdrawn until the algebra exists (GPT en, GPT sp); "only in the
            demand" became "the demand's, passed down" (D-2026-10-12-h); the grade of a sum
            parameterizable (D-2026-10-12-i); the two candidate algebras named (D-2026-10-12-p).
            draft 11 (2026-10-12), his mark: clause 2, the retraction, ok (D-2026-10-12-w). draft 11
            (2026-10-12): renumbered from L6 of draft 10 (D-2026-10-12-v).

L13 The ideal world is realized with a guarantee.
From:       G2 directly: the realization's distance to the ideal law is the law's value, and the
            tolerance is the demand's (G0, the demand)
L13.1  Code is written over ideal objects (Real) and realized by concrete ones (Float64); the
       realization's laws hold within a stated tolerance, and the error of each step is itself a law
       rather than a false claim of exactness. [settled]
L13.2  (His reading) Rounding `Real -> Float64` is a functor in Lawvere's sense, and each law of
       `Real` is projected onto `Float64` with its cost; it is not a homomorphism, and the exact map
       is the inclusion the other way. [settled]
L13.3  Rounding does not expand distances by at most a constant: two reals astride a rounding
       boundary land one ulp apart at any distance, so no multiplicative constant exists; rounding
       is non-expansive up to an additive defect of about ε|x|, and for subtraction and division the
       sensitivity is per input, the condition number (`11` §7). [mark pending]
L13.4  The functor reading stands with "non-expansive plus an additive term", and the cost algebra
       needs both parts: a multiplicative one where a Lipschitz constant exists and an additive one
       where rounding enters (`11` §5). [mark pending]
References: `11`
Rests on:   O1 (the two parts of the algebra)
Quote:      "un functor que va de Real--> Float64 y que ahi vemos algunas propiedades de Real
            proyectadas en Float" (annotation on draft 2, 2c18c41)
Source:     Luciano, 2026-05-29; the floats note of 2026-10-11 (5cc41fa); the functor 2026-10-11
            (annotation on draft 2, 2c18c41)
Status:     settled in its statement; clauses 3 and 4 are the correction proposed, his mark pending
History:    draft 0 (6d9dbd3): stated. draft 3 (c085ba4), his annotation: rounding as a functor.
            draft 4 (c7c6396): the correction on the additive defect, proposed. draft 10 (72cc7be,
            81c1794, 25f9c5e, b7a7e23): renumbered from L15. draft 11, step 3 (2026-10-12): the
            formulation split into numbered clauses with the status each sentence had in draft 10,
            the examples into Example, the provenance phrases into this History, the wording
            otherwise as draft 10 had it. draft 11 (2026-10-12): renumbered from L8 of draft 10
            (D-2026-10-12-v).
```

(History: L11 at draft 11 step 3, merged into L9 in step 4: L11 An action is verified by observing
the world before and after it. 1. (His annotation) Executing is the executive face: an action
changes the state of the world, and it is verified too, by observing the world before and after it;
the laws over actions are stated over those two observations, as a mutable parameter is two
variables (L9). [settled] 2. An observation is itself an action, so this stops where the world can
be read back (a file written and reread), and says nothing beyond; an effect on state Luthier owns
is verified this way, an irreversible or concurrent effect outside it is typed, logged and audited,
never verified. [settled])
(History: L12 at draft 11 step 3, merged into L10 in step 4: L12 No hardcoded constants: every
criterion is a parameter. 1. Thresholds, budgets, limits and statistical levels are never constants
in code; they are declared, passed and recorded. [settled] 2. The outermost demand, an action with
no caller, carries its tolerance as a declared default argument (D-2026-10-11-c), recorded with the
call, so there is a root and it is a parameter. [settled])
(History: L3 at draft 11 step 3, merged into L2 in step 4: L3 The certified subtype from a law is
the fundamental construction pattern. 1. From a material type and a law, a predicate or a cost with
its tolerance, come the certified type, its only constructor and the forgetful projection; the same
pattern builds values, functions and programs. [settled] 2. A law gives the three at once: the type,
the constructor with Maybe, the membership function. [settled] 3. Where the law is into `Cost`, the
constructor takes the tolerance as a parameter (L12) and the certificate records the tolerance it
was checked at, so a stricter demand asks for a new check (`11` §4). [settled] 4. Types are verified
before they are constructed: Luthier starts from types by verification, and types by construction
may come in later. [settled])

## What is open

Only questions whose answer changes the language or the specification, each with the entries it
blocks; the done and implemented items are in the record's drafts table.

- **O1** (language) The algebra of costs. Its articulation is `docs/rationale/11-cost-valued-laws.md`
  draft 0: Ω replaced by [0,∞), quantitative equality, graded judgments, cost as −log p or as
  distance, how the uncertainty of a cost is represented in a certificate; the composition: a
  Lipschitz constant per function type where known (sensitivity types, Reed and Pierce 2010;
  condition numbers), a sampled cost where not, costs adding as −log p under independence; the
  interface of `Cost` in a certificate (a multiplicative constant where it exists, an additive
  defect where rounding enters, the grade as a lattice, the worst cost seen; `11` §5, §6); worked
  examples the sum of n floats, a matrix inverse with κ(A), a sampled probability integrating to
  one. Two candidate models (D-2026-10-12-p): min and max, or 1/n log-sum-exp with 1/n sum.
  `Cost` is a library (D-2026-10-12-al): its algebra is settled when it is implemented, and the
  certification written in Luthier says what it asks of it; the two candidates can be two of its
  models. The
  extension of Boolean logic to Lawvere and Bayes, which he names as another motivator or eureka;
  whether it is the third eureka or a principle of good use is his to mark after that analysis.
  Until it exists the application runs on a Boolean interim: laws of the form d(f x, g x) ≤ tol
  with tol a parameter (L5), every law returning `Bool` or `Cost` with the result type saying
  which (`11` §2, L3), no composition of tolerances along a chain, no run database. Blocks L8.7,
  L3.3, L12, L13.3, L13.4, L5.4, L6.6, L6.8, L10.3, L10.8.
- **O2** (language) The type with its equality as the base case of every theory (a setoid; a
  metric space where the equality is a cost), the kernel's structural `==` its model for the
  decidable types (spec 4.R8), the equality of functions extensional and derived from it (L3), the
  equality of models componentwise; and whether a type names its equality as it names its model
  (spec 4.R13). Proposed by the model on his observation of 2026-10-12 (D-2026-10-12-e); his note of
  the same day on Terms goes the same way ("podríamos suponer que A viene con su Setoid", `K` with
  its `Field`); the syntax, how a type names its setoid and its field, is the open part. Blocks
  Terms (dependences), L3, L9, L6.
- **O3** (language) An opt-out of certification in a demand, if a real case asks for one
  (D-2026-10-11-n; none at the start, D-2026-10-12-y); the world as an opaque, unique value so that
  an action is never served from the memo (L4, L5); actions and the world as a value, designed and
  not implemented. Blocks L4.11, L5.6, L11.6, L10.6.
- **O4** (language) The composition of invariances (G1's derived route): which laws compose and how
  the demand selects them (audio 08.58, 32:01 to 34:07; audio 09.21). Blocks L5.15.
- **O5** (language) The decorated output (L5.4): the derivative by dual numbers as a model of the
  theory, the error by intervals or value-and-cost pairs once O1 exists; what in the planner
  chooses the model and inserts the bridges. Blocks L5.4.
- **O6** (language) Units as a candidate L under G0: a dimension is a proposition, dimensions form
  a group under multiplication, the quantities of one dimension a one-dimensional vector space,
  the whole a graded algebra; addition inside a dimension, multiplication across (second round
  §18). Precedent quimulun (his repository); pressure from sonolocalización (metres, seconds, the
  speed of sound). Blocks nothing.
- **O7** (spec) Closed on 2026-10-12 (D-2026-10-12-z) by the term *object* in Terms; spec 4 §4 reads
  "theories are cycles" in chapter 4 of the specification. Blocks nothing.
- **O8** (spec) The session as a block over the dataflow of L5: `<-` to explore, `:=` to lock, a
  file may contain a block, `<-` banned at the top level of a file (decided, D-2026-10-11-i); the
  spec's spec 8 and a section on the session; the memo between the items of a session. Blocks
  L5.12.
- **O9** (spec) The kind of a hole in the elaborated form (L2.3). Blocks L2.3.
- **O10** (spec) `proved` by citation: the citation a `.bib` key with a resolved DOI, ISBN or URL,
  and who checked (human, ai+human, none) recorded; syntax `cite name bibkey checked ai+human`
  proposed, allowed in user code (D-2026-10-11-f as amended; to spec 6). Blocks L9.7.
- **O11** (spec) The kernel's theory stated in Luthier: `src/luthier/lib/kernel_laws.lut`, tested
  on `Fin 3`, `Fin 2` (`examples/kernel_finite.lut`, 10 laws, sampled); eta not statable (spec 4
  R8), functions over `Fin n` not enumerated by `exhaustive` (to fix). Blocks L7.
- **O12** (spec) The identity of a result in the memo (L5.6) and `plan.lut` as its carrier.
  Blocks L5.6.

## His marks pending

- L10.7 and L10.8, the composition of identities as paths (his note of 2026-10-12 put in
  words, with D-2026-10-12-q).
- L12, the names lift, exact and within (his to rename), and clauses 1 and 5.
- L13.3 and L13.4, the correction on rounding.
- L5.4, the decorated output as another model.
- L6.3, the wording of his formula for the efficiency.
- L11.6, the world as a candidate; L9.7, delegation as citation; L10.7, the wording of the graded
  transport (his correction).
- L10.1, L10.2, L10.7, L10.8, the certificate entry; L8.3, what `a : A` asserts; L4.11, actions on Luthier's own state;
  L5.17 and L5.18, the cutoff and the policy constants; L6.5, 6, 7; L12.3, 5; L9.1.
- The two faces defined in Terms, and the shape of this draft (D-2026-10-12-g, -s).

## Keys

- G0, G1, G2: the organizers above; L1 to L7: the principles; L5.4: clause 4 of L5.
- O1 to O12: the open questions above.
- D-2026-10-11-n and the like: decisions, in `record/decisions.md`.
- P1 to P15: the principles of the method, `record/principles.md`.
- W1 to W15: the way of working, `docs/way-of-working.md`.
- spec 1 to spec 12: the chapters of the specification, `docs/spec/`, index `00-index.md`; spec 4.R8
  is rule 8 of chapter 4. `07`, `09`, `10`, `11` in backticks: the rationale documents of
  `docs/rationale/`, `11` the cost-valued laws.
- His words, his annotation, his correction, his reading, his formula: Luciano's; a clause without
  such a mark is the model's.
