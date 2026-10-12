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

The statements and the sources of the L are those of draft 1 unless the history says otherwise;
L numbers are kept (D4 of the generative plan), and the entries are printed by organizer, in his
order of the eurekas (G2 first, D-2026-10-12-a).

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
| record | 2026-10-12 | this file | D-2026-10-12-d: the entries below rewritten from draft 9 (120a49a) into fields, the draft marks moved into `History:`, nothing dropped; `docs/principles.md` becomes the projection. |

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

## Terms

His list (2026-10-12, `docs/principles_corr.md` at d5e81e3, D-2026-10-12-f), in his order; where he
left a question mark the name is the model's proposal and says so.

- A *structure* (proposed; his candidates structure, object, data) is a type in the kernel's
  language (`04`): products, sums, function types and recursive types, built from each other.
- A *predicate* is a function into `Bool`. A *cost* (proposed) is a function into `Cost`, the
  non-negative reals with infinity, 0 true and ∞ false (G3).
- A *law* is a predicate or a cost over the symbols of a structure; both are laws and coexist (G3).
- A *theory* is a structure with its laws.
- A *model* is an inhabitant of a theory: a value of its structure whose laws are certified.
- A *function* is a value of a function type `A -> B`, in the standard sense (his correction). A
  function type with its laws is a theory of one symbol, and a function that satisfies them is a
  model of it; this is the common case in practice (D-2026-10-12-e), and a function has sense only
  in that context.
- A *certificate* (proposed; his "validation or proof") is the record that a law was checked, with
  its grade (proved, exhaustive, cases, sampled at a level, assumed) and, for a cost, the worst
  value seen; a proof is a certificate of grade proved. To *certify* is to produce one.
- *Evaluation* computes a value, or the value of a law, and has no effect (L18). *Execution* is an
  action on the world (print, save). On his doubt, whether checking a law is an execution since it
  changes state (proposed): checking the law is evaluation; recording that it was checked writes a
  certificate into the store Luthier owns, with the memo, and that is an action, verified by
  reading the store back (L12) and never an action on the world outside; `test` is that action
  (L19).
- The *demand* is a request for a value from outside the program, an action, carrying the type and
  the tolerance it wants. The *planner* is what chooses, among the models certified equivalent,
  the one that runs.

The spec's *object* (`05 §3`, a strongly connected component of the dependency graph, the names a
cycle of laws joins) is not among his terms; in them it is a theory written in one cycle of names
with its models. Whether `05` renames it is open.

## The organizers

Three tiers, in his words (`record/audios/WhatsApp Ptt 2026-10-11 at 09.19.36.md`, 00:00 to
00:53): the guide, two eureka moments, and after them "principios de buen uso".

```
G0  Type theory is the guide.
Tier:       the guide
Formulation: a type is a proposition and a value its proof; a law is a proposition over terms, so it
            defines a mathematical object and a quotient, and inside a class the representative is
            free: free in the theory, where the law is exact; in a model the planner's freedom is
            what L10 states. Luthier departs from type theory in three places, named under G1, G2
            and G3 by what type theory lacks.
Quote:      "Un principio es hott/Category theory/ type theory guidance. De ahi sale types as
            propositions y funcions as types y por ende functions defined as propositions, laws.
            De ahi sale que las laws definen objetos matematicos. y tambien que con una law tenes
            un cociente y por lo tanto valores intercambiables y por lo tanto optimizacion por
            tiempo y costo en memoria o por error." (note, fa3f972)
            "la guía es la te[o]ría de tipos" (audio 09.19, 00:00)
Source:     record/Lucianos ideas/principios organizadores.txt (fa3f972); WhatsApp Ptt 2026-10-11
            at 09.19.36.md, 00:00
Status:     settled; the formulation is the model's
History:    draft 2 (cd24137): stated from his note and the audio, formulation proposed.
            draft 5 (5b1446c): "free in the theory, where the law is exact; in a model, L10".

G2  A type with laws is a theory and its value a model; a function type is its laws, and a
    function is known by description.
Tier:       eureka, the first (the trigger, audio 09.19, 00:00 to 00:14), printed first
            (D-2026-10-12-a)
Formulation: a theory is a signature with its laws, written in the kernel's language (`04`, a
            bicartesian closed category: this is where G0 is used); a model is a value of a
            theory, and declaring `m : T` records the obligation to satisfy the laws of `T`; a law
            relates several symbols (`inverse x * x = unit`), which no single function can carry,
            so the unit declared is the theory and the unit valued is the model. The common case
            in practice is not the smallest theory but one that adds a single symbol, a function
            type with its laws, to structures already modelled with their equality: every law is
            an equality, and the equality of a carrier is itself a function with laws (reflexive,
            symmetric, transitive, or those of a distance) that the new symbol must respect; the
            model of such a theory is a function in the standard sense, and the eureka of 09.19
            is this case, where he saw it first. (His words, D-2026-10-12-e) An isolated function
            has no sense; it has sense in a context, and what looks like a lone function is one
            whose inverse and whose theory nobody took the trouble to find. Luthier verifies
            models of theories; what it verifies about a function is that it is a model of its
            type's laws.
            The function: the laws are what is known of a function, and the implementation,
            native or extern, is the specimen under observation. A description is derived by
            composition of the laws of the parts when such a law exists, and observed otherwise;
            laws accumulate, and a set of laws that determines the function up to its equality is
            the limit a definition may reach, not what it must reach (D-2026-10-11-d).
            (His words) A law is written as an implementation of itself, a program that returns
            its Bool or Cost; a theory is written as an object classifier made of laws, the map
            that sends a structure over the signature to the cost of its being a model, which is
            where G3 enters G2; the implementation of a model is then verified against the laws.
            What type theory lacks: it knows a function by acquaintance, as its term. What model
            theory lacks: a grade and a demand; a model of Luthier satisfies its theory up to a
            cost, certified at a grade and progressively (G3), and is chosen for execution by a
            demand (G1); naming it "model" must not promise exactness.
            What follows from G2 as its definition rather than by derivation: L20 (a function is
            declared in a theory and is universal over its models), the object of `05 §3` (the
            names a cycle of laws joins), D-2026-10-07-e (no loose functions: a definition at a
            bare exponential is not a defined type) and D-2026-10-11-j (a carrier with two models
            is two types); and three L read in its terms: L10 is many models of one theory,
            interchangeable in the quotient; L21 is the difference between two models being
            identified and both satisfying the theory; L14's extern is a model whose carrier is
            foreign. The precedent in programming is algebraic specification, the module systems
            of ML and the lawful type classes of Haskell, where the mechanism exists without being
            the organizing idea (references to be checked before they are cited).
Quote:      "el disparador es darme cuenta de eso, que los tipos de funciones son las leyes que
            las definen. Esa fue mi eureka moment" (audio 09.19, 00:00 to 00:14)
            "Las leyes deben ser propiedades (matematicas o no) que determinen univocamente la
            funcion que estamos definiendo. Las funciones se definen a lo Russel. Y se testean
            empiricamente. Que una implementacion sea valor de un tipo de funcion siginfica que ya
            fue validada aunque sea una vez. Y la validacion de las funciones es progresiva" (note)
            "no ser a lo tarski (constructivo) sino a lo matematico (desde afuera, como un
            entomologo observa un bicho)" (chat, D-2026-10-11-d)
            "Un tercer momento eureka fue cuando me di cuenta que necesitaba los objetos ya que
            hay funciones que se testean mutuamente, o sea que 'la programacion basada en objetos'
            tiene una base matematica, solo que las clases (o interfases) serian las Teorias y
            los objetos serian los modelos de las teorias" (66f0bef)
            "que tal si en lugar de presentar Luthier como verificador de funciones lo
            presentamos como verificador de modelos de teorias? Al tomar elementos de CCC como
            estructuras donde se escriben las leyes, las teorias y modelos pasarian a ser los
            elementos de Luthier" (chat, 2026-10-12, D-2026-10-12-a)
            "me parece que es muy difcil encontrar un caso en que verifiques una funcion
            relevante aislada, siempre viene con un tipo asociado al menos, y siempre tiene la
            igualdad asociada tambien... Y las igualdades vienen asociadas con funciones
            tambien" (chat, 2026-10-12, D-2026-10-12-e)
            "Si, lo comun es extender una teoria con un caso. Lo que pasa es que yo sospecho que
            son funciones porque no nos tomamos el trabajo de pensar cual es su inversa o a que
            teoria pertenecen. una funcion sola, aislada no tendria sentido, tiene sentido en un
            contexto, a eso voy." (chat, 2026-10-12, D-2026-10-12-e)
            "Pensa un poco que es una funcion. Una funcion tiene una definicion estandard."
            (docs/principles_corr.md, d5e81e3)
Source:     WhatsApp Ptt 2026-10-11 at 09.19.36.md, 00:00 to 00:14; record/Lucianos ideas/
            principios organizadores.txt; the composition of invariances as "la parte Tarski",
            WhatsApp Ptt 2026-10-11 at 08.58.46.md, 32:01 to 34:07; his observation on draft 7,
            66f0bef; chat 2026-10-12, D-2026-10-12-a; his words on laws and theories,
            record/answers-annotations-principles-2026-10-12.md §5 (bcdac41); the function as
            the common case, chat 2026-10-12 (D-2026-10-12-e), after a survey of the .lut files
            (58 certified functions, each with an imported equality; 12 models; 341 definitions
            without a law); his annotation on the projection, d5e81e3 (§6 of the answers)
Status:     settled (the widening, the order, the removal of the holotype and the function as
            the common case are his decisions);
            the formulation is the model's except the paragraph marked his; the precedent's
            references unchecked
History:    draft 2 (cd24137): "a function is known by description", the second eureka, printed
            after G1.
            drafts 3 to 8: a holotype paragraph, his metaphor for the representative of a class,
            later recognized as L10's and removed.
            draft 8 (4f6beef): widened to theories and models on his observation (66f0bef) and
            D-2026-10-12-a; printed first, in his order; L20 moved under it; what model theory
            lacks added; the derivations that follow directly named.
            draft 9 (0636378): the holotype removed, settled; his words put in its place (a law an
            implementation of itself, a theory an object classifier made of laws).
            record (2026-10-12), D-2026-10-12-e and his annotation d5e81e3: the common case is a
            theory of one symbol whose model is a function in the standard sense; an isolated
            function has sense only in a context.
```

```
G1  The demand defines what is computed.
Tier:       eureka, the second, printed second (D-2026-10-12-a)
Formulation: the declarative face states what is known, universal and minimally processed; the
            executive face is a demand from outside, and the demanded type fixes the path, the
            types and the tolerances actually produced. What type theory lacks: an executive
            face; there, computation is the normalization of a given term, with no demand.
Quote:      "la demanda de un valor por el mundo externo me define todos los tipos necesarios
            para obtener eso" (audio 09.19, 00:24)
            "la compilacion se dispara por la demanda externa (es decir un print o un valor que
            sale al mundo), y la demanda determina el tipo que quiere el print, y eso determinan
            1) el camino que efectivamente se computa y los tipos que efectivamente se computan"
            (note)
            "la clara separacion entre lo declarativo y lo ejecutivo. Esto dio lugar a la idea de
            que lo ejecutivo se da por la demanda. Y lo declarativo pasa a ser todo lo universal
            posible, minimamente procesado" (note, 1c7a284)
            "lo que se sabe, que es un poco como la idea del prior" (audio 08.58, 08:59)
Source:     WhatsApp Ptt 2026-10-11 at 09.19.36.md, 00:24; record/Lucianos ideas/principios
            organizadores.txt; its root, 1c7a284; WhatsApp Ptt 2026-10-11 at 08.58.46.md, 08:59
Status:     settled; the formulation is the model's
History:    draft 2 (cd24137): stated, printed as the first eureka.
            draft 8 (4f6beef): printed second, in his order.

G3  Laws are valued in cost, and what a run teaches is kept.
Tier:       good use; named by him on 2026-10-12 as a further motivator or eureka, to be
            analyzed (the extension of Boolean logic to Lawvere and Bayes)
Formulation: a law is valued in [0,∞), 0 true and ∞ false, and the demand supplies the
            tolerance. A Bool-valued law and a Cost-valued law are both laws and coexist (his
            mark: "no podes promover booleans a cost a troche y moche"); Bool is a retract of
            Cost, not a subtype: `lift : Bool -> Cost` (true to 0, false to ∞) and `exact : Cost
            -> Bool` (c == 0), both homomorphisms with `exact ∘ lift = id`; the lift is explicit
            and named, inserted by the planner as a bridge of cost zero; the cutoff `within ε :
            Cost -> Bool` lives only in the demand, since it does not compose (two links within ε
            are within 2ε). Over floats the cost of a law is itself estimated, so its value is
            uncertain and evidence composes as Bayes composes it, and is kept across runs. What
            type theory lacks: two truth values, and a run that leaves nothing. The reason to
            depart is not that type theory fails on floats (Flocq proves exact theorems about
            them) but what the Boolean way costs: a tolerance fixed in each law, worst-case
            bounds that compose into condition numbers, and nothing to say about data
            (`record/organizing-principles-2026-10-11.md`, addendum 2). Articulated in
            `docs/rationale/11-cost-valued-laws.md`, draft 0 (D6).
Quote:      "queremos que Luthier use Bayes como guia tambien. Esto implica que las leyes no sean
            predicativos a un bool sino a un costo real positivo. Esta parte es la menos
            desarrollada ... Usar un object classifier de Lavwere seria el marco unificador. Y
            usar estadistica bayesiana para componerlo" (note)
            "El problema de la teoria de tipos es que funciona para enteros y deja de funcionar
            para float y para linear algebra o estadistica. Ahi la teoria de tipos booleana falla
            y si queres ser estricto o expresivo, necesitas otra cosa. De ahi el [0, +inf)" (el
            problema de los floating point.txt, 5cc41fa)
            "cuando vos corres un programa aprendés algo y eso que aprendés queda en algún lado
            ... es como un deseo más que un principio" (audio 08.58, 05:47 to 06:08)
            "no podes promover booleans a cost a troche y moche" (bcdac41)
            "luego vamos a analizar la parte mas dificil es la extencion de logica booleana a
            Lawvere/bayesiana, otro motivador/Eureka" (chat, 2026-10-12)
Source:     record/Lucianos ideas/principios organizadores.txt; record/Lucianos ideas/el problema
            de los floating point.txt (5cc41fa); WhatsApp Ptt 2026-10-11 at 08.58.46.md, 05:47 to
            06:08; his annotation on draft 8, bcdac41; the lift, exact and within,
            record/answers-annotations-principles-2026-10-12.md §4
Status:     candidate by the P13 check (one decision, D-2026-10-10-g), in his words a wish; the
            names lift, exact and within are the model's, his to change; whether it is a third
            eureka or a principle of good use is his to mark after the analysis he announced
History:    draft 2 (cd24137): stated, good use.
            draft 9 (0636378): on his mark, Bool and Cost coexist, the lift explicit and named,
            the cutoff only in the demand.

G4  Expressive over restrictive; it decides between designs. Retired.
Tier:       good use, retired (draft 9, D-2026-10-12-c); the tag stays so that the record's
            citations resolve
Formulation: retired. What he meant by it is concrete and is a rule, L22 (a non-Luthier way is
            allowed inside a named world). "The law that makes two ways equivalent" is L21; P5
            (a free choice is a legitimate principle) stays in `record/principles.md`. The
            decisions it was named for stand without it: `:=` once and `<-` for rebinding with
            default arguments (D-2026-10-11-c), `if` without `else` as a guarded value
            (D-2026-10-11-b), many paths expressible (L10), accumulating laws rather than required
            characterization (D-2026-10-11-d): each stands on L10, G0 or his own decision, and
            none needed the tie-breaker.
Quote:      "Luthier debe ser expresivo mas que restrictivo: si hay mas de una forma de hacer las
            cosas, todas deberian poder ser expresadas en Luthier" (note)
            "me da que es una declaracion de buenas intenciones nomas" (bcdac41)
Source:     record/Lucianos ideas/principios organizadores.txt; his annotation on draft 8,
            bcdac41; record/answers-annotations-principles-2026-10-12.md §5 (G4)
Status:     retired (D-2026-10-12-c), reversible by him in one line
History:    draft 2 (cd24137): stated from his note, the tie-breaker between designs.
            draft 3 (c085ba4): "it decides between designs" added.
            drafts 2 to 8: cited by D-2026-10-11-b, -c, -k, -m, -n in their Kind lines; generated
            no L.
            draft 9 (0636378, 120a49a): retired on his doubt and the model's recommendation; its
            content became L22.
```

## How the organizers depend on each other

*Proposed* (D8 of the generative plan).

1. G0's quotient needs G1 and G3 where the carrier carries a distance: there two implementations
   are interchangeable only up to a distance and below the tolerance the demanded type carries.
   On decidable carriers the exact quotient is correct and the kernel proceeds without G3;
   "optimización por error" has no meaning there and needs none. The interface that lets G3
   arrive without a rewrite: every law returns a `Cost`, and `Bool` is the two-valued case, the
   type of the result saying which (`11` §2, L21). A law into `Cost` returns a measure; the
   proposition is cost ≤ ε with ε the demand's, so G0's "a law is a proposition" holds once the
   tolerance is supplied. Until G3's algebra exists the application runs on this Boolean interim:
   laws of the form d(f x, g x) ≤ tol with tol a parameter (L17), no composition of tolerances
   along a chain, no run database.
2. G2's inhabitance needs G3: "validada aunque sea una vez" gives the certificate of a : A a
   grade, which is sound only if truth is graded. The judgment itself stays one and structural;
   the grade is its evidence (L2, `11` §4).
3. G1's planner is G0's proof search with G3's cost: it searches for an inhabitant of the
   demanded type and ranks candidates by cost.

So G3, the least developed, is load-bearing for G0 and G2 over carriers with a distance, whatever
the P13 count says today; over decidable carriers the Boolean kernel stands on its own.

(History: items 1 and 2 were extended in draft 4, c7c6396, with the decidable case and the
judgment staying one, and in draft 5, 5b1446c, with the law as a measure.)

## The principles of the language

Each L keeps its number and source from draft 1. `From:` names the organizers it derives from and
the derivation, the model's unless marked his. Order: by first organizer, G0, G2, G1, G3.

### From the guide, G0

```
L2  A type is a proposition, and membership is a guarantee.
From:       G0 directly; the second clause is the step to G2
Formulation: belonging to a type asserts the propositions, laws included, that the value
            satisfies; function types carry their laws the same way. `a : A` is one judgment,
            structural and decidable for the kernel's types; it asserts the structural proposition
            outright and the laws through the certificate, at the grade the certificate has, so
            "guarantee" means what the grade says: proved or exhaustive, a guarantee; sampled,
            evidence at a level; assumed, a hole that says so. What a law adds is evidence, and
            the certificate of the law carries its grade (proved, exhaustive, cases, sampled,
            assumed) and, for a law into `Cost`, the worst cost seen (`11` §4). The guarantee is
            what the certificate says and no more, and what leaves the program carries one (L19,
            D-2026-10-11-n).
Source:     Luciano, 2022-08-03 (written:2022-08-03_haskell:proposicion-que-cada-tipo-cumple);
            restated 2026-05-26 (day:2026-05-26:tipos-como-conceptos-y-proposiciones)
Status:     settled
History:    draft 1 (5769005): stated.
            draft 4 (c7c6396): one judgment, structural; the certificate carries the grade and
            the worst cost; what leaves the program carries a certificate (D-2026-10-11-n).
            draft 6 (8809e20): what "guarantee" means at each grade.

L4  The certified subtype from a predicate is the fundamental construction pattern.
From:       G0 (a predicate is a proposition; its subtype is the type of its proofs) with G2
            (verified, not constructed)
Formulation: from a material type and a predicate come the certified type, its only constructor
            and the forgetful projection; the same pattern builds values, functions and programs.
            A law gives the three at once: the type, the constructor with Maybe, the membership
            function. Where the law is into `Cost`, the constructor takes the tolerance as a
            parameter (L17) and the certificate records the tolerance it was checked at, so a
            stricter demand asks for a new check (`11` §4). Types are verified before they are
            constructed: Luthier starts from types by verification, and types by construction may
            come in later.
Source:     Luciano, 2022-08-03 (written:2022-08-03_haskell:subtipos-con-predicado); named
            fundamental 2026-09-29 (record/distillation/2026-10-09_find_principles_v2_claude-code_
            opus.md, C3); the three things and the scope 2026-10-10 (WhatsApp Ptt 2026-10-10 at
            10.12.21.md, 05:24 to 08:10)
Status:     settled
History:    draft 1 (5769005): stated.
            draft 4 (c7c6396): the tolerance a parameter of the constructor, recorded in the
            certificate.

L5  A law characterizes; it does not re-run.
From:       G0 (a law defines the object) and G2 (a law that transcribes the specimen is
            acquaintance, not description); extends P10 (the mathematical object that best
            represents a concept is the invariant of its type)
Formulation: a law states a mathematical property of an operation; a second implementation
            checked against the first is consistency, and the native definition is one more model
            certified against the law. A law over several functions is tested on the values
            actually computed, as a puzzle whose pieces must fit; the cases to test are chosen by
            the law, its arity (three elements for associativity) and the distribution sampled
            (L11), never every path. Laws accumulate, and a law need not determine the operation;
            when the laws do determine it up to the presentation's equality, that is the limit
            (D-2026-10-11-d). The generators are the model's addition.
Quote:      "La idea en realidad es buscar el objeto matematico que mejor lo represente y
            decirlo" (chat, 2026-10-05)
Source:     Luciano, 2026-10-05 (chat:52d3e68e:2760); the puzzle 2026-10-10 (WhatsApp Ptt
            2026-10-10 at 10.12.21.md, 11:38 to 18:20)
Status:     settled
History:    draft 1 (5769005): stated.
            draft 3 (c085ba4), on D-2026-10-11-d: laws accumulate and need not determine the
            operation.

L6  Code is data.
From:       G0 through the universe, the type of types (the object classifier of HoTT; the note's
            "object classifier" names this when it means types as values, and the subobject
            classifier when it means G3's truth values)
Formulation: a Luthier program is an element of Luthier; programs build, inspect and run other
            programs, and the interpreter is meant to be written in the language it interprets.
Source:     Luciano, 2022-06-15 (written:2022-06-15_sin-titulo-2:codigo-es-dato)
Status:     settled
History:    draft 1 (5769005): stated.

L7  The core is minimal and executable by hand.
From:       G0 (a type theory is a few rules whose judgments a person checks; a small trusted
            kernel) and G2 (the paper semantics is the description, and every interpreter is a
            specimen certified against it)
Formulation: a handful of well-specified primitives, so that a program can be run with pencil and
            paper; everything else is a library whose translation to the core is mechanical. Hand
            execution is of the kernel given a plan, an order of execution that is a value
            (`lib/plan.lut`); the planner's choice among plans is outside the kernel. Four
            layers, each trusted differently: the kernel, checked by hand; the libraries and the
            interpreter in Luthier, certified against the kernel's laws; the host runtime, a
            specimen; the planner, advice that the plan records.
Quote:      "Luthier tendría que ser ejecutable a mano" (2026-05-29)
Source:     Luciano, 2026-05-29
Status:     settled
History:    draft 0 (6d9dbd3): stated. Draft 0 of the generative plan proposed moving it to the
            way of working; withdrawn (D3).
            draft 4 (c7c6396): hand execution is of the kernel given a plan.
            draft 6 (8809e20): the four layers of trust.

L8  Declare, then define, then inhabit.
From:       G0 (a hole is a hypothesis of the context) with G1 (nothing is produced until
            demanded)
Formulation: a declaration without a body is a first-class hole: at once axiom, program input,
            external function, pending definition and dead code; nothing executes until it is
            defined, and no value inhabits an undefined type; an axiom is not a value but a law
            with grade `assumed`, so it does not inhabit. To the type checker the five are one,
            and the elaborated form records which it is, since the demand treats them
            differently: an input asks for a value, an external calls the host, a pending
            definition is an error, an axiom is a law with grade `assumed`, reasoned with and
            never run (an item for the spec; `assumed` has one meaning, the grade). `extern` is
            the operation that inhabits a hole with a body in another language, naming the
            language; a theoretical module (types, functions, laws, no values) is a module of
            holes. (His words) A declared name is assumed to have its declared type, and its use
            where that type is incompatible is an error (`05` R1, the checker).
Source:     Luciano, 2026-05-29 (dialogue:20260529T1400:tipos-no-definidos-y-forward-reference);
            the hole named 2026-09-29; `external` and the theoretical module 2026-10-10 (WhatsApp
            Ptt 2026-10-10 at 17.41.53.md; WhatsApp Ptt 2026-10-10 at 17.25.23.md, 00:00 to
            00:40); his annotation on draft 8, bcdac41
Status:     settled
History:    draft 0 (6d9dbd3): stated.
            draft 4 (c7c6396): the elaborated form records which of the five it is.
            draft 5 (5b1446c): `assumed` has one meaning.
            draft 6 (8809e20): an axiom is not a value.
            draft 9 (0636378): his words on a declared name's type.

L10 One function, many paths.
From:       G0 (the quotient), G3 (the choice by cost and the database of runs) and, before its
            retirement, G4 (every path expressible; now L10's own clause)
Formulation: a function has many equivalent implementations, each with its precision, speed,
            memory and place of execution; equivalence is established first, and the choice among
            paths follows expected loss and cost, estimated from a database of measured runs;
            error, time and memory are not one scalar, and the trade-off among them is a
            parameter of the demand (L17), never the planner's own. Stated as a quotient: the
            implementations of a function are the quotient by "compute the same function up to
            the law's equality", one class per mathematical function, and inside the class the
            fibre of what differs; the class is chosen by law, the representative by cost. The
            class is exact in the theory (`Real`); in a model that carries a distance it is the
            ball of the demanded radius (`11` §3), and closeness is not transitive, so the planner
            substitutes one implementation for another only along a certified equivalence
            between the two, the identity law of L21 with its result `Bool` or `Cost`
            (D-2026-10-11-m). The law gives the candidates; the identity certificates say which
            the planner may exchange, and they form a weighted graph, not a class: a substitution
            is a path whose summed distance (`11` §2) is within the demanded tolerance, so two
            specimens joined through a third may each replace it and not each other; the sum is a
            bound only when every link is one (proved, exhaustive), otherwise an estimate with
            the weakest grade and the samples it was seen on; a lone implementation is never
            replaced. A sampled edge is admissible only on inputs the distribution it sampled
            covers, and only as a direct edge, never summed into a path, until a probabilistic
            bound exists as a law; the tolerance charged at a node is the demand's pulled back
            through the sensitivity of the cone from the node to the demand (`11` §5), and where
            no sensitivity is known there is no substitution. The same for every grade: a link
            certified on a subtype is a link only at inputs certified (L4) in that subtype, so a
            path exists at x only where every link does; a `proved` link by citation carries the
            theorem's hypotheses as parameters (γ_n needs n·u < 1, false for float32 over an hour
            at 48 kHz) and is void where they fail. The author's free choice among the
            inhabitants of an under-determined function (D-2026-10-11-d, P5) stays; the planner's
            choice is only among what has been compared.
Source:     Luciano, 2022-06-28 (written:2022-06-28_luciano-code-style:choose-efficient-path-
            after-validity); the quotient 2026-10-10 (WhatsApp Ptt 2026-10-10 at 16.49.14.md,
            00:04 to 01:39), the same idea without the word 2026-05-30 (note:2026-05-30T18.01.53:
            equivalencias-para-clasificar-y-separar-decoraciones)
Status:     settled; the weighted graph, the admissibility of sampled edges and the subtype
            clause are the model's, from the rounds of critiques
History:    draft 0 (6d9dbd3): stated.
            draft 2 (cd24137): stated as a quotient.
            draft 4 (c7c6396), D-2026-10-11-m: exact in the theory, a ball in the model;
            substitution only along a certified equivalence.
            draft 5 (5b1446c): a weighted graph, not a class; a lone implementation never
            replaced.
            draft 6 (8809e20): error, time and memory not one scalar.
            draft 7 (6a15cec, cd314a4): from the third round's counterexamples, a sampled edge
            only on covered inputs and only direct, the tolerance pulled back through the
            sensitivity; Claude's clause on subtypes and cited hypotheses.
            draft 9 (120a49a): G4 retired; "every path expressible" is L10's own clause.

L12 Evaluation is verification; execution is an action on the world.
From:       G0 (identity is the first proposition; his "path equivalence is the fundamental
            concept", 2026-05-29); the two faces are G1's statement; the verification of actions
            from G2 (observation) and G1
Formulation: Luthier first describes the problem and its equivalences; evaluating is checking
            them, as mathematics verifies rather than runs. (His annotation) Executing is the
            executive face: an action changes the state of the world, and it is verified too, by
            observing the world before and after it; the laws over actions are stated over those
            two observations, as a mutable parameter is two variables (L9). An observation is
            itself an action, so this stops where the world can be read back (a file written and
            reread), and says nothing beyond; an effect on state Luthier owns is verified this
            way, an irreversible or concurrent effect outside it is typed, logged and audited,
            never verified. Every function induces an equivalence on its domain, its kernel, so
            computing f(x) is placing x in its class and the value is the class's name: an
            interpretation of computation, not the evaluator's mechanism, and a name exists only
            where a normal form does, the decidable fragment (no canonical form elsewhere); a
            predicate is the two-class case and `Maybe T` places x in one of them. This
            equivalence on the domain is distinct from the equivalence between terms that a law
            induces, which is L10's quotient.
Quote:      "la matemática no ejecuta ... la ejecución en Luthier sería esa verificación de
            equivalencias" (2026-05-30)
            "una funcion genera equivalencias f(a)==f(b) ==> a~b y mas si f(a)=true" (chat,
            2026-10-11)
            "las ejecuciones tambien se verifican observando el mundo antes y despues del acto"
            (annotation on draft 2, 2c18c41)
Source:     Luciano, 2026-05-30; the kernel reading 2026-10-11 (chat); the actions 2026-10-11
            (annotation on draft 2, 2c18c41)
Status:     settled
History:    draft 0 (6d9dbd3): stated.
            draft 2 (cd24137), addenda 7 and 8: the kernel of a function as the equivalence on
            its domain.
            draft 3 (c085ba4), his annotation: actions verified by observing the world before
            and after.
            draft 4 (c7c6396): an observation is an action; stops where the world can be read
            back.
            draft 5 (5b1446c): the kernel reading is an interpretation, not the mechanism; a name
            only where a normal form exists (formerly under G4).
            draft 6 (8809e20): effects outside Luthier typed, logged and audited.

L16 Equality has levels and belongs to the object.
From:       G0 (the identity type and its levels) with G3 (under cost, the identity proposition
            acquires a distance)
Formulation: definition (`:=`), the identity proposition (`=`), decidable equality (`==`) and
            definitional equality by reduction (`≡`) are different things, and each object
            carries the observational equality that fits it. (His annotation) The binding acts
            are two, `:=` once and `<-` rebinding, and they share one law: after the act the name
            equals the term in the equality its type has, structural `==` where it exists (`05`
            R8), observational otherwise, a distance under G3; after `:=` for all time, after
            `<-` until the next `<-` (`05` R12). In the kernel the binding is exact: the name
            denotes the term, and reduction does not depend on a tolerance; the distance enters
            when the planner realizes the term by another representative, which it does only
            along a certified equivalence carrying its distance (L10, D-2026-10-11-m).
Quote:      "luego de <- lh == rh, de hecho creo que es la ley de <-" (reply, 18da042)
Source:     Luciano, 2026-05-30 (day:2026-05-30:niveles-de-equivalencia); the law of a binding
            2026-10-11 (reply, 18da042)
Status:     settled
History:    draft 0 (6d9dbd3): stated.
            draft 3 (c085ba4), his annotation: the law of a binding.
            draft 4 (c7c6396): the kernel's binding is exact; the distance enters with the
            planner.
```

### From theory and model, G2

```
L1  Luthier expresses the invariances of the disciplines.
From:       G2 (what is known of a thing is its description; "la idea de luthier es ayudar a
            descubrir las invariantes de los calculos", note), with P14 (a type is a concept)
Formulation: what moves the language: a species mates within itself, electrons are fermions, a
            probability integrates to one. A definition states the invariances that determine a
            concept, and the language exists so that stating them is natural.
Quote:      "la idea de luthier es ayudar a descubrir las invariantes de los calculos" (note)
Source:     Luciano, 2026-05-29 (dialogue:20260529T1400:expresar-invarianzas-de-disciplinas)
Status:     settled
History:    draft 0 (6d9dbd3): stated.

L3  Defining a model defines its test.
From:       G2 directly: the eureka of 09.19 in its 2022 form
Formulation: declaring a model of a theory, `m : T`, declares the tests it will be run on, so
            definition and verification are one act; a function type with its laws is the
            one-symbol case, and its model a function.
Source:     Luciano, 2022-08-03 (written:2022-08-03_haskell:declarar-funcion-es-declarar-su-test)
Status:     settled (the widening is his mark)
History:    draft 0 (6d9dbd3): stated as "defining a function defines its test".
            draft 9 (0636378), his mark: widened to the theory.

L11 Verification is one operation, exact or statistical.
From:       G2 (observation is how a description is verified) and G3 (the grade is the
            uncertainty of the cost)
Formulation: what is known by a theorem is cited, what can be enumerated is checked exhaustively,
            what has chosen cases is checked on them, what can only be sampled is checked
            statistically, and the grade of the evidence (proved, exhaustive, cases, sampled at a
            level, assumed) travels with the value in a certificate hashed over its dependency
            cone; the line is the method, since associativity over `Int` is computable and
            cannot be checked by running. The grade of a sampled certificate depends on the
            distribution sampled, not only on the number of samples, because errors concentrate
            at the edges (the model's correction, from the practice of property-based testing).
            Verification by a theorem is `proved` by citation (D-2026-10-11-f); verification by
            delegation is the same mechanism with the host library's guarantee as the theorem
            cited (LAPACK's backward-error bounds, the condition number their hypothesis) and the
            library's version and platform as hypotheses the certificate carries (L14); no new
            grade (*Proposed*, on his mark).
Quote:      "verificacion externa por teoremas o por delegacion (creo en Lapack)" (bcdac41)
Source:     Luciano, 2022-08-03 and 2023-02-22 (written:2023-02-22_tapp-wish-list:untested-a-
            tested); the grades by samples 2026-10-10 (WhatsApp Ptt 2026-10-10 at 11.11.22.md,
            03:02 to 04:12); his annotation on draft 8, bcdac41
Status:     settled; the reading of delegation as citation is proposed, his mark pending; he
            restated the delegation in his own words on the readers' document ("proved by citing
            a theorem or taken from a software library", afdd7c7), the reading as citation not
            marked
History:    draft 0 (6d9dbd3): stated.
            draft 4 (c7c6396): the four methods and the grade in the certificate; the dependence
            on the distribution.
            draft 9 (0636378), on his mark: delegation as citation of the host's guarantee.
            readers' draft 0 (afdd7c7): his correction adds the library as a source of proof.

L14 Luthier orchestrates other languages.
From:       G2: an absorbed library is a specimen known by its description, and its code is not
            needed ("que la IA pueda ... extraer de librerías ajenas, chuparlas y usar las
            funciones con sus propias invarianzas", audio 08.58, 31:25 to 32:00)
Formulation: types and laws are native; values may come through `extern` from Python or any
            host, declared over what they really receive and return, with description and
            verification kept on Luthier's side. An external function is validated like any
            other, against its type with its laws, the first time an action asks for it, and its
            certificate stays by hash; without a type with a law to validate against it is not
            applied. (His words) "si el tipo no sigue la ley no se aplica el calculo": an extern
            is declared over a type, a type carries its laws (L2), the extern is validated
            against them before it is applied and refused if it fails; the agreement test with
            the native is in addition (W5), and the planner's substitution is D-2026-10-11-m. A
            function with no laws at all is not a function to run but a hole of a theory being
            defined (L8). The extern's certificate binds the host library's version and the
            platform (W10), and its declaration says whether it is a definition or an action
            (L12, L18). Certification is the default for every value: demanding a value demands
            every certificate in its dependency cone, paid once through the memo, unless the
            demand asks otherwise by a mechanism to be named, which leaves a certificate of grade
            `assumed` (D-2026-10-11-n), since what could be done Luthier gives a way to do (L22);
            `test` is the action that demands certificates without values (L19). Luthier is in
            use a coupling language: the joint between two libraries is a theory of which each
            is a model, the bridges between representations live at the joint with their cost
            and error, and no coupling without a law.
Quote:      "si el tipo no sigue la ley no se aplica el calculo" (chat, 2026-10-10)
            "que la IA pueda ... extraer de librerías ajenas, chuparlas y usar las funciones con
            sus propias invarianzas" (audio 08.58, 31:25 to 32:00)
Source:     Luciano, 2026-05-26 (note:2026-05-26T12.32.24:lenguaje-no-atado-a-cpp); the
            validation on first demand and the coupling language 2026-10-10 (chat; WhatsApp Ptt
            2026-10-10 at 17.41.53.md; WhatsApp Ptt 2026-10-10 at 16.49.14.md, 01:39 to 03:18);
            WhatsApp Ptt 2026-10-11 at 08.58.46.md, 31:25 to 32:00
Status:     settled by his correction (draft 7); the opt-out's syntax open
History:    draft 0 (6d9dbd3): stated. Draft 0 of the generative plan proposed moving its
            orchestration half to the way of working; withdrawn (D3).
            draft 4 (c7c6396), D-2026-10-11-n: certification the default, the opt-out in the
            demand.
            draft 5 (5b1446c): the opt-out leaves a certificate `assumed`.
            drafts 5 and 6: carried "every function starts with zero laws", which came from a
            critique, not from D-2026-10-11-d, wrongly.
            draft 7 (e8ba100): the zero-laws clause removed; the extern validated against its
            type's laws in his words; a function with no laws is a hole (L8).

L21 A certificate of identity is not a certificate of the law.
From:       G2 (the specimen can be recognized as the same specimen, or described)
Formulation: checking that an implementation gives the same bits as before, with the same seed,
            certifies that the implementation has not changed; checking it against its laws, by
            chosen or sampled cases, certifies the description. Both are kept, apart, and the
            certificate of the law travels by the certificate of identity (his annotation):
            exactly where the identity is boolean (`==` structural, `05` R8: integers, decidable
            types, the same implementation rerun), and with the observed distance added where it
            is a cost (G3), since two implementations over floats are almost never bit-identical.
            The type of the identity law's result says which (`Bool` or `Cost`). The identity law
            between two specimens, with its distance, is what admits a second implementation
            into the class the planner moves in (L10, D-2026-10-11-m); the agreement test of W5
            between native and extern is this law, and the reference formula of a law evaluated
            over `Rational` is one more specimen, with grade exact, checked by the same law.
            (His correction) Certification transports along identity: if B is certified at grade
            g on inputs X and the identity A ≡ B is certified at grade h on inputs Y, then A is
            certified at the weaker of g and h on X ∩ Y, and by nothing else. The two
            counterexamples of the third round follow: with B's laws only `assumed` the transport
            gives A `assumed`, nothing (Kimi); a lookup table equal to the native on a grid is
            certified on the grid and nowhere else (Claude). A function known correct by a
            theorem outside Luthier is certified `proved` by citation (D-2026-10-11-f), and the
            chain law, citation, native, identity, extern is carried by hash.
Quote:      "verificar bit a bit que sea igual ... por lo menos sabés que no cambia la
            implementación" (audio 08.58, 09:20 to 13:19); the statistical kind for "prueba
            científica" (same)
Source:     Luciano, 2026-10-11 (WhatsApp Ptt 2026-10-11 at 08.58.46.md, 09:20 to 13:19); his
            annotation on draft 2 (2c18c41); his annotation on draft 8 (bcdac41)
Status:     proposed, candidate; the graded transport is his correction, his mark on the wording
            pending
History:    draft 1 (5769005): proposed, candidate.
            draft 3 (c085ba4), his annotation: the certificate of the law travels by the
            certificate of identity.
            draft 4 (c7c6396), D-2026-10-11-m: the identity law admits a second implementation
            into the planner's class.
            draft 7 (9d1c435, cd314a4): two clauses from Kimi and Claude on when transport fails.
            draft 9 (0636378), his correction: the two clauses replaced by graded transport on
            X ∩ Y, the counterexamples following from it.

L20 A function is declared in a theory and is universal over its models.
From:       G2, of which it is the definition rather than a consequence: a function belongs to
            the theory its laws are stated in, and a model is where it runs; before draft 8 from
            G0 (a theory is a type, a model its inhabitant) and G1 ("lo declarativo pasa a ser
            todo lo universal posible"; instantiated on demand)
Formulation: a function belongs to a theory (Real, Field, LinearAlgebra) and takes its model as
            its first, often implicit, argument, so it is written once for every model; the
            model is named by the type of the argument (D-2026-10-11-j) and can be passed
            explicitly. A theory over a model of another theory is a theory. Every type belongs
            to a theory; the concrete types (products, sums, exponentials, `data`) belong to the
            kernel's, whose laws are the β and η rules and the recursion principle, stated in
            `lib/kernel_laws.lut`. Operators are resolved by the type, the type naming its
            model; a carrier with two models is two types (D-2026-10-11-j). Modules are values
            by design, files today: a parametrized module is a function from models to
            definitions, applicative because definitions have no effects (L18), instantiated on
            demand with the parameter threaded down from the action. A specialization is one
            more representative of the law's class (L10), valid on a subtype, certified against
            the same law; where representations differ, the orchestrator inserts bridges by
            cost, coherent up to the law, carrying their error, visible in the plan; a
            specialization and a bridge each enter the planner's graph by an identity
            certificate with its distance (L10, D-2026-10-11-m). The conditions on bridges are
            the model's, accepted.
Quote:      "el codigo seria, en principio universal a los valores de funciones que cumplan las
            leyes requeridas" (chat, 2026-10-10)
            "no entiendo porque hacerlo un principio. Surge solo" (bcdac41)
Source:     Luciano, 2026-10-10 (chat; WhatsApp Ptt 2026-10-10 at 17.00.40.md; WhatsApp Ptt
            2026-10-10 at 17.25.23.md, 00:00 to 04:25; D-2026-10-10-g)
Status:     absorbed into G2 on his mark (draft 9): the clause on specializations and bridges
            belongs to L10 and modules as values to the spec (`03`); the tag stays for the
            record's citations and the text stays until the spec takes its parts
History:    draft 1 (5769005): stated as "code is universal over the models of its theory".
            draft 3 (c085ba4): reworded after his annotation (theories).
            draft 4 (c7c6396): the model named by the type of the argument (D-2026-10-11-j).
            draft 5 (5b1446c): specializations and bridges enter by identity certificates.
            third and fourth rounds (9395268, 55da213): every type belongs to a theory; the
            kernel's theory in `lib/kernel_laws.lut`.
            draft 8 (4f6beef): moved under G2 as its definition.
            draft 9 (0636378), his mark: absorbed into G2.
```

### From the demand, G1

```
L9  A program is a DAG and statements commute.
From:       G1 (the DAG is what the demand walks backward) with G3 (the second structure's
            metric); the separation of the second structure is the model's proposal
Formulation: the unit is the definition; dependencies give the only order there is, and time is
            reconstructed from them rather than from the text. Inside a block the text fixes
            which binding a name means, each `<-` a fresh name (D-2026-10-11-i), and then
            dependencies give the only order: after `x <- 1`, `y := x + 10`, `x <- 2`, y is 11,
            as the session answers. Operations are declared before their laws, so a law that
            binds two operations is a node with two parents, not a cycle; a mutable parameter is
            two variables, before and after, and mutation in place is the planner's optimization
            when the earlier one has no other consumer. The DAG says what depends on what; the
            structure the laws generate over terms (an equivalence when laws are boolean, a
            metric space when they carry a distance) is a second structure, where L10 and L12
            live.
Source:     Luciano, 2026-05-29 (note:2026-05-29T14.46.22:contexto-como-dag); the unordered set
            of definitions already in 2023-03-13 (written:2023-03-13_hacia-luthier); the two
            structures and the mutable parameters 2026-10-10 (chat; D-2026-10-10-e)
Status:     settled
History:    draft 0 (6d9dbd3): stated.
            draft 2 (cd24137): the two structures.
            draft 5 (5b1446c): inside a block the text fixes the binding (D-2026-10-11-i).

L13 Forgetting is determined by the demand.
From:       G1 directly, with G2 for what is derived
Formulation: dependent typing accumulates history, so the language needs non-invertible
            forgetful projections, and the demand chooses them: what is forgotten is everything
            the demanded value does not need, the complement of its dependency cone, so the
            projection is canonical, one per demand, and the language being spoken is what was
            asked for. Forgetting at run time (a node freed after its last consumer) and
            forgetting in the type (how much history a certificate keeps) are one; the program
            is never forgotten, only what leaves scope is lost; forgetting is not materializing
            a derived value, never erasing what reconstructs or recertifies it (code, inputs,
            model, seed, plan, tolerance), which the memo's identity keeps. A function on a type
            applied to a subtype does not produce one overload per subtype; the demanded return
            type selects which law to derive by composition (G2), and the rest is forgotten:
            doubling positives is positive only when positivity is demanded and derivable, sin
            of positives forgets to Real because no law composes. What is derivable is a
            property of the expression, independent of the demand; the demand chooses which of
            it is derived, certified and carried, so the elaboration (types, derivable laws)
            does not depend on the observer; the memo of results does (L19), and they are two
            caches.
Quote:      "olvidar esta determinado por todo lo que no hay que recordar, es decir lo que pide
            el valor demandado. Eso soluciona el tema de los functores de olvido" (chat,
            2026-10-10)
Source:     Luciano, 2026-05-29 (note:2026-05-29T14.52.08:problema-del-olvido); resolved
            2026-10-10 (chat; WhatsApp Ptt 2026-10-10 at 11.42.15.md, 01:07 and 03:20 to 03:55;
            WhatsApp Ptt 2026-10-10 at 17.28.45.md); the overloads 2026-10-11 (WhatsApp Ptt
            2026-10-11 at 09.21.05.md, 00:00 to 00:29; 09.01.13.md)
Status:     settled
History:    draft 0 (6d9dbd3): stated.
            draft 2 (cd24137), audios 09.01 and 09.21: no overload per subtype; the demanded
            return type selects the law.
            draft 4 (c7c6396): what is derivable is independent of the demand.
            draft 5 (5b1446c): the elaboration and the memo are two caches.
            draft 6 (8809e20): forgetting is not materializing, never erasing what recertifies.

L17 Every criterion is a parameter.
From:       G1 (the tolerance belongs to the demand) and G3 (a law states a distance, not a
            threshold), so a constant in the code has no place to live; restates P11 (every
            criterion is a parameter, never a constant in the code)
Formulation: thresholds, budgets, limits and statistical levels are never constants in code;
            they are declared, passed and recorded. The outermost demand, an action with no
            caller, carries its tolerance as a declared default argument (D-2026-10-11-c),
            recorded with the call, so there is a root and it is a parameter.
Source:     P11, in force; first applied as a rule of the language 2026-10-05
            (dialogue:c7437496:lmmaxiter-should-be-a-parameter)
Status:     settled
History:    draft 0 (6d9dbd3): stated. Draft 0 of the generative plan proposed moving it to the
            way of working; withdrawn (D3).
            draft 6 (8809e20): the outermost demand's default argument.

L18 A definition has no effects.
From:       G1 as its precondition rather than its consequence: the declarative face can be
            universal and minimally processed only if definitions have no effects
Formulation: its result depends only on its inputs; effects live only in the actions (print,
            save). A mutable parameter written as before and after is not an effect, the
            dependence is an edge; what is forbidden is what the graph does not show. It is the
            one assumption under which every evaluation strategy gives the same result; over a
            carrier with a distance, a result in the same class at a distance the plan records,
            and for the Boolean case this is `Confluent` in `lib/plan.lut`, a law a dataflow is
            certified against rather than a theorem assumed. (His words) No effect on the world;
            its one effect is on the program: it takes its name, once, and enters the map of
            definitions, so the same name is not defined twice (`:=` once; `<-` only in a block,
            D-2026-10-11-i).
Quote:      "lo que si es no-side effects" (chat, 2026-10-10)
Source:     Luciano, 2026-10-10 (chat; D-2026-10-10-c); his annotation on draft 8, bcdac41
Status:     settled
History:    draft 1 (5769005): stated.
            draft 4 (c7c6396): `Confluent` as the law a dataflow is certified against.
            draft 9 (0636378), his words: the one effect, on the program.

L19 The demand determines the computation.
From:       G1 directly; the audio of 08.58 (15:35 to 17:12, 30:37 to 31:21) adds the iteration
            step, read every demand, run, collapse to the outputs, write, and asks whether the
            code object is consumed or stable: kept
Formulation: the evaluation strategy is a parameter separate from the program (L17); by default,
            a plan backward from the actions over names, evaluating nothing, then a strict
            forward run over the live subgraph, each node once and whole: forward on demand.
            What the action asks for flows backward along the plan and is produced forward: the
            value, its error, its derivative, its test, the type of its result; at the leaves a
            value lifts on its own, takes a mark given with the demand, or is a hole. The tests
            are actions, so verifying is demanding. What never reaches an output needs no
            certificate, and what reaches one carries its cone's certificates (D-2026-10-11-n;
            `test` demands certificates without values). A result is identified by code,
            inputs, mode, the demanded type and tolerance, the model its type names, the seed,
            the plan that produced it, the plan being a value (`lib/plan.lut`), and the hashes
            of the certificates in its live cone, so a host library or platform that changed is
            a new result; the grade the demand states is in the identity too, and a memo hit
            serves a demand only if the cached cone meets that grade, checked at the hit and not
            only when the certificate was issued; the runtime includes the thread count and
            scheduling of the host, and an extern whose bits depend on scheduling is not
            bit-identical to itself, so its identity law is `Cost`, never `Bool` (L21). The run
            database is what the planner reads to choose the plan and is not an input of the
            result once the plan is fixed; evidence accumulates by a separate action with its
            own record, so "each node once" and G3's "kept across runs" never meet on one node.
            A test is an action whose result is a certificate, memoized by the certificate's
            identity (code, cases, seed, the distribution and level sampled, L11) and rerun when
            asked or when that identity changed; the demand states the grade it requires (P11),
            and a certificate serves every demand whose tolerance and grade it meets (`11` §4).
            "Each node once" is once per plan: a stricter demand on the same definition is
            another node of another plan, and the looser certificate still serves what it met.
            Three objects, never one: the meaning of a program, the class its laws fix; a
            realization, the result under a plan; the evidence, its certificates. A certificate
            is a frozen snapshot by hash; a later test does not change it, it issues a new one
            that supersedes it, both kept, the latest in front (P3), so progress is the chain of
            certificates. Two sessions that differ only in the order of independent bindings are
            equivalent by `Confluent` (L18), the law the session block is certified against.
            The program is the synthesis and is kept, the computation is the expansion and is
            redone. Script and interpreter are the same under this L, one batch of demands or
            demands one at a time with the memo between them (08.58, 17:12 to 23:35; an item for
            the spec, 04 §7); a session is a block and a file is never one, so a session saved
            to a file becomes its `main` block (D-2026-10-11-i). The three cases at the leaves
            and the memo key are the model's, accepted.
Source:     Luciano, 2026-10-10 (WhatsApp Ptt 2026-10-10 at 11.11.22.md, 00:00; WhatsApp Ptt
            2026-10-10 at 11.42.15.md, 01:02 to 04:07; WhatsApp Ptt 2026-10-10 at 16.49.14.md,
            03:20 to 07:06; WhatsApp Ptt 2026-10-10 at 17.25.23.md, 05:49 to 07:53; WhatsApp Ptt
            2026-10-10 at 17.28.45.md; D-2026-10-10-d, f, h); WhatsApp Ptt 2026-10-11 at
            08.58.46.md, 15:35 to 23:35, 30:37 to 31:21
Status:     settled; the identity of a result, the memo gate and the three objects are the
            model's, from the rounds of critiques
History:    draft 1 (5769005): stated.
            draft 2 (cd24137): the iteration step from audio 08.58.
            draft 4 (c7c6396): the identity of a result; what reaches an output carries its
            cone's certificates (D-2026-10-11-n).
            draft 5 (5b1446c): a test is an action memoized by its certificate's identity.
            draft 6 (8809e20): once per plan; three objects; the chain of certificates;
            sessions equivalent by `Confluent`.
            draft 7 (9d1c435, Kimi): the demand's grade in the identity, re-gated at the memo
            hit; (cd314a4, Claude): thread count and scheduling in the runtime, identity by
            `Cost`.
            fourth round (55da213), D-2026-10-11-i: a session is a block.

L22 The escape hatch is a world.
From:       G1 (the demand names the world it runs in) with L12 and L14
Formulation: a definition or an implementation that does not follow Luthier's way, an extern
            with no law yet, a foreign algorithm taken as is, is allowed inside a named world
            (L12): its certificates are `assumed` (D-2026-10-11-n), the plan shows the world it
            ran in, and nothing from it enters the planner's graph (L10) until a law is
            certified.
Quote:      "si hay una forma 'no luthieriana' de definir o implementar algo, luthier deberia
            dar la posibilidad de hacerlo con un world especifico" (bcdac41)
Source:     his annotation on draft 8 (bcdac41), on G4
Status:     proposed, candidate; the wording is the model's
History:    draft 9 (0636378, 120a49a): stated from his words on G4, which it replaces
            (D-2026-10-12-c).
```

### From cost, G3

```
L15 The ideal world is realized with a guarantee.
From:       G3 directly: the realization's distance to the ideal law is the law's value, and
            the tolerance is the demand's (G1)
Formulation: code is written over ideal objects (Real) and realized by concrete ones (Float64);
            the realization's laws hold within a stated tolerance, and the error of each step is
            itself a law rather than a false claim of exactness. (His reading) Rounding `Real ->
            Float64` is a functor in Lawvere's sense, and each law of `Real` is projected onto
            `Float64` with its cost; it is not a homomorphism, and the exact map is the inclusion
            the other way. (Correction proposed, his mark pending) Rounding does not expand
            distances by at most a constant: two reals astride a rounding boundary land one ulp
            apart at any distance, so no multiplicative constant exists; rounding is
            non-expansive up to an additive defect of about ε|x|, and for subtraction and
            division the sensitivity is per input, the condition number (`11` §7). The functor
            reading stands with "non-expansive plus an additive term", and the cost algebra
            needs both parts: a multiplicative one where a Lipschitz constant exists and an
            additive one where rounding enters (`11` §5, open).
Quote:      "un functor que va de Real--> Float64 y que ahi vemos algunas propiedades de Real
            proyectadas en Float" (annotation on draft 2, 2c18c41)
Source:     Luciano, 2026-05-29; the floats note of 2026-10-11 (5cc41fa); the functor 2026-10-11
            (annotation on draft 2, 2c18c41)
Status:     settled in its statement; the correction on rounding is proposed, his mark pending
History:    draft 0 (6d9dbd3): stated.
            draft 3 (c085ba4), his annotation: rounding as a functor.
            draft 4 (c7c6396): the correction on the additive defect, proposed.
```

## What is open

- The articulation of G3, `docs/rationale/11-cost-valued-laws.md` draft 0 (D6): Ω replaced by
  [0,∞), quantitative equality, graded judgments, cost as −log p or as distance, how the
  uncertainty of a cost is represented in a certificate; the algebra of composition (second
  round §16): a Lipschitz constant per function type where known (sensitivity types, Reed and
  Pierce 2010; condition numbers), a sampled cost where not, costs adding as −log p under
  independence; worked examples the sum of n floats, a matrix inverse with κ(A), a sampled
  probability integrating to one.
- The extension of Boolean logic to Lawvere and Bayes, G3, which he names as another motivator or
  eureka (chat, 2026-10-12); whether it is the third eureka or a principle of good use is his to
  mark after that analysis.
- The composition of invariances (G2's derived route): which laws compose and how the demand
  selects them (audio 08.58, 32:01 to 34:07; audio 09.21).
- The session as a block over the dataflow of L19: `<-` to explore, `:=` to lock, a file may
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
  the worst cost seen; `11` §5, §6); the identity of a result in the memo (L19) and `plan.lut`
  as its carrier; the opt-out of certification in a demand (D-2026-10-11-n, syntax open); the
  kind of a hole in the elaborated form (L8); the world as an opaque, unique value so that an
  action is never served from the memo (L18, L19); L15's rounding, his mark pending.
- The kernel's theory stated in Luthier: `src/luthier/lib/kernel_laws.lut`, tested on `Fin 3`,
  `Fin 2` (`examples/kernel_finite.lut`, 10 laws, sampled); eta not statable (`05` R8),
  functions over `Fin n` not enumerated by `exhaustive` (to fix).
- `proved` by citation: the citation a `.bib` key with a resolved DOI, ISBN or URL, and who
  checked (human, ai+human, none) recorded; syntax `cite name bibkey checked ai+human` proposed,
  allowed in user code (D-2026-10-11-f as amended; to `05 §7`).
- Units as a candidate L under G0: a dimension is a proposition, dimensions form a group under
  multiplication, the quantities of one dimension a one-dimensional vector space, the whole a
  graded algebra; addition inside a dimension, multiplication across (second round §18).
  Precedent quimulun (his repository); pressure from sonolocalización (metres, seconds, the
  speed of sound).
- The type with its equality as the base case of every theory (a setoid; a metric space where
  the equality is a cost), the kernel's structural `==` its model for the decidable types
  (`05` R8), the equality of functions extensional and derived from it (L21), the equality of
  models componentwise; and whether a type names its equality as it names its model (`05` R13).
  Proposed by the model on his observation of 2026-10-12 (D-2026-10-12-e); his mark pending.
- The names he left with a question mark in his list of terms (structure, cost, certificate) and
  the three-level answer to his doubt on validation as execution; and whether `05 §3` renames
  *object* (D-2026-10-12-f).
- His marks pending on this record: L21's wording (graded transport), L15's correction on
  rounding, L11's delegation as citation, the names lift, exact and within (G3), L22 as a
  candidate.
