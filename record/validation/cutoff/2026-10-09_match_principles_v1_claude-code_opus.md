# Candidate principles of Luthier, 2026-10-09

Written by `scripts/match_principles.py` (match_principles v1) for Luciano to mark. Two steps, each a model's reading:
the candidates were found blind by `find_principles_v2` (sha256 5eb0cb1b3e6b, opus, effort
low; it saw only the lineages and the criterion of infectability), then set against the principles in
force, the log and the objectives by `match_principles_v1` (sha256 007b56b7e8bb, opus, effort low).
Whose words each quote is and its source were filled in from the rows by the scripts. Under each candidate, a
Mark: line for ok, no, or a correction.

```
C1  Defining a function means stating, as runnable tests, what it must satisfy, so definition and
    verification are one act.
Scope:      language
Quote:      "La idea central del tapp es que al declarar una funcion vos declaras que es lo que la
            funcion debe cumplir como un test y entonces es posible generar tests automaticos."
Said by:    Luciano, 2022-08-03 11:56
Source:     2022-08-03 haskell.md line 19 (row written:2022-08-03_haskell:declarar-funcion-es-declarar-su-test)
Found:      ethical. it recasts what it means to have a function: you do not have it until you have
            said, as runnable tests, what it must satisfy.
Harms:      a function with no cheap test becomes hard to admit
Harms:      blurs the line between specification and verification, hiding which is trusted
Harms:      statistical tests give false confidence of proof
Against:    extends P14: adds that defining a function at its type and writing its test are one act, so definition yields verification with no separate step
Assumption: the laws that define a function can always be run as tests; shown false if a
            definition's postconditions cannot be turned into an executable check
Would have guided (for P13, later): D-2026-10-07-b, D-2026-10-07-e
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C2  Make the predicate the primitive, and derive the certified type, its sole constructor and its
    forgetful projection from it.
Scope:      language
Quote:      "lo primitivo es el predicado, y el tipo y el constructor se derivan de él mecánicamente.
            No son dos cosas que se confunden bajo un nombre; son dos usos de una sola cosa."
Said by:    model, 2026-09-29 06:01
Source:     2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 59 (row dialogue:890a551c:lo-primitivo-es-el-predicado-tipo-y-constructor-se-derivan)
Found:      conceptual. one primitive, a predicate over a material, generates type, constructor and
            forget mechanically, unifying values, functions and whole programs.
Harms:      every value carries a certificate, costing memory and compute
Harms:      the predicate may be undecidable or only testable, so 'checked' means different
            strengths
Harms:      forces thinking in predicates even where a plain value would do
Against:    new
Assumption: every named type is a subtype carved by a predicate, so type, constructor and forget
            always derive from one predicate; false if a useful type has no predicate behind it
Would have guided (for P13, later): D-2026-10-07-f, D-2026-10-07-e
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C3  Hold a program's code as a value of an ordinary data type, so code and data are the same kind of
    thing.
Scope:      language
Quote:      "La idea de que el codigo sea dato es muy, pero muy fuerte en cuanto a la flexibilidad
            que ofrece pero es notable que los lenguajes modernos no sigan ese camino Lispeano."
Said by:    Luciano, 2022-06-15 08:55
Source:     2022-06-15 Sin título 2 .md line 13 (row written:2022-06-15_sin-titulo-2:codigo-es-dato)
Found:      conceptual. erasing the code/data line lets a program hold, inspect and transform its
            own code as an ordinary value, reorganizing what a program is.
Harms:      homoiconicity invites self-modification and self-hacking
Harms:      a core that is its own data is harder to keep consistent
Harms:      power tempts cleverness over clarity
Against:    new
Assumption: holding code as an ordinary datum buys the meta-recursion the interpreter-in-Luthier
            needs more than it costs in complexity; false if the kernel cannot reduce terms given as
            data cheaply
Would have guided (for P13, later): D-2026-10-08-c
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C4  Treat the choice of what to forget from a type as the thing that defines the language you are
    speaking.
Scope:      language
Quote:      "de qué función de olvido le aplicás a los tipos, es un, digamos, eso te define
            básicamente el lenguaje que estás hablando ... los functores de olvido serían, digamos,
            uno de los componentes más importantes de Luthier"
Said by:    Luciano, 2026-05-29 14:59
Source:     2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 21 (row dialogue:20260529T1400:funtores-de-olvido-definen-el-lenguaje)
Found:      conceptual. it reframes a language as defined by what it chooses to forget, turning the
            forgetful functor from a side tool into the identity of the language.
Harms:      choosing the wrong forgetful functor silently changes the language's meaning
Harms:      forgetting is non-invertible, so information is lost for good
Harms:      an ill-defined forgetting degenerates into crude truncation Luciano rejects
Against:    new
Assumption: the language a program speaks is fixed by which forgetful functor it applies, so
            forgetting is a first-class choice; false if controlling forgetting turns out not to
            tame the growth of accumulated typing
Would have guided (for P13, later): no decision in the log
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C5  Make execution the verification of equivalences, following mathematics, which does not run but
    only verifies.
Scope:      language
Quote:      "Hay una idea, que la matemática no ejecuta, porque lo único que hace es verificar
            equivalencias. Entonces, bueno, sí, la ejecución en Luthier sería esa verificación de
            equivalencias"
Said by:    Luciano, 2026-05-30 18:03
Source:     WhatsApp Ptt 2026-05-30 at 18.01.53.md [01:47] (row day:2026-05-30:matematica-no-ejecuta-verifica-equivalencias)
Found:      conceptual. it redefines running a program as verifying equivalences, importing
            mathematics' stance that nothing executes, equivalences are only checked.
Harms:      demoting execution may make the language impractical for real computation
Harms:      verifying equivalence is undecidable in general
Harms:      users wanting to just run things face a conceptual detour
Against:    new
Assumption: all of Luthier's execution can be cast as verifying equivalences of expressions; false
            if some needed computation has no reading as an equivalence check
Would have guided (for P13, later): D-2026-10-08-b
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C6  Aim the language at expressing the invariances of each discipline, as a relator of invariances.
Scope:      language
Quote:      "la idea de luthier es expresar invarianzas de los de las disciplinas"
Said by:    Luciano, 2026-05-29 14:29
Source:     2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 11 (row dialogue:20260529T1400:expresar-invarianzas-de-disciplinas)
Found:      emotive. it names what moves the author: a language that relates the invariances of each
            field, set against statistical predictors that only guess.
Harms:      'invariance of a discipline' is vague and hard to pin down operationally
Harms:      risks the project growing to cover the whole universe and becoming useless
Harms:      privileges domains with clean invariances over messy ones
Against:    extends P10: lifts the invariant from one concept's type to the stated aim of the whole language: to express the invariances of each discipline
Assumption: each discipline's content reduces to invariances a language can carry; false if a
            discipline's useful structure is not an invariance
Would have guided (for P13, later): D-2026-10-07-b, D-2026-10-08-a
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C7  Let the programmer declare what they want and have the engine openly weigh many equivalent
    implementation paths by estimated cost.
Scope:      language
Quote:      "que Luthier sea, en el fondo, una forma de ser a la vez un lenguaje declarativo y una
            herramienta de optimización. O sea, que vos declares lo que querés hacer, que sigan más
            decir las fórmulas, y después internamente baraja distintas formas de implementar eso,
            pero eso lo hace abiertamente"
Said by:    Luciano, 2026-05-26 12:33
Source:     2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 1 (row dialogue:20260526T1233:luthier-declarativo-y-optimizador)
Found:      conceptual. it splits a program into what it means (declared) and how it runs (openly
            chosen among estimated paths), reorganizing the frame of writing code.
Harms:      maintaining many paths and their cost estimates is heavy machinery
Harms:      a priori cost estimation is the hardest open problem, maybe unsolvable well
Harms:      the run database can grow monstrous and paralyzing
Against:    new
Assumption: many equivalent implementation paths can be proven equivalent and ranked by estimated
            cost, so declaration and optimization can be one tool; false if proving path equivalence
            stays intractable (its lineage calls it the hardest part)
Would have guided (for P13, later): no decision in the log
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C8  Let a bodyless typed declaration be the one construct that serves as axiom, input, external
    function, pending definition and dead code at once.
Scope:      language
Quote:      "el **hueco**: una definición con tipo y sin cuerpo, `f : A → B := ?`. Una sola cosa
            cumple cinco papeles: axioma, input del programa, función externa que el entorno llena,
            definición pendiente, código muerto. Tu principio "no ejecutás hasta que está definido"
            es su semántica exacta"
Said by:    model, 2026-09-28 20:56
Source:     2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 2 (row dialogue:175c0408:hueco-cinco-papeles)
Found:      aesthetic. one construct, a bodyless declaration, collapses five roles that other
            languages keep as separate features.
Harms:      overloading one construct with five meanings can confuse readers
Harms:      no way to mark intention means external vs unwritten is indistinguishable
Harms:      a program full of holes may typecheck yet do nothing
Against:    new
Assumption: a bodyless typed declaration can serve all five roles with 'do not execute until
            defined' as its only semantics, needing no External type or core symbol; false if any of
            the five roles demands its own construct
Would have guided (for P13, later): no decision in the log
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C9  Make types propositions and terms their proofs, so the code is its own mathematical
    demonstration.
Scope:      language
Quote:      "los tipos tienen que ser conceptos, tipos como proposiciones y los tipos incluyen
            también funciones, funciones y funciones de orden superior"
Said by:    Luciano, 2026-05-26 12:33
Source:     WhatsApp Ptt 2026-05-26 at 12.32.24.md [00:38] (row day:2026-05-26:tipos-como-conceptos-y-proposiciones)
Found:      conceptual. types as propositions and code as its own proof fuses programming and
            proving, validating logic before a line runs.
Harms:      Curry-Howard raises the entry cost for ordinary programmers
Harms:      making code its own proof demands discipline most code cannot pay
Harms:      proof obligations can balloon with each dependent composition
Against:    new
Assumption: Curry-Howard holds throughout Luthier so a term is a proof of its type; false if a
            useful type admits terms that are not proofs of the proposition it stands for
Would have guided (for P13, later): no decision in the log
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C10  Keep the founding components few and hand-executable, and build the whole edifice of complex
    concepts from them.
Scope:      language
Quote:      "El minimalismo está en los componentes fundantes y después a partir de esos componentes
            fundantes vos construís un edificio enorme."
Said by:    Luciano, 2026-05-30 18:07
Source:     WhatsApp Ptt 2026-05-30 at 18.07.21.md [00:12] (row day:2026-05-30:minimalismo-fundante-maximalismo-construido)
Found:      aesthetic. minimalism in the founding components, from which a huge edifice is built, is
            the classic beauty of economy.
Harms:      extreme minimalism can push complexity onto unreadable library layers
Harms:      'executable by hand' may forbid features users want
Harms:      few primitives risks cryptic error messages
Against:    new
Assumption: a small set of hand-executable founding components can generate the whole edifice of
            concepts; false if some needed concept cannot be built from them and must be native
Would have guided (for P13, later): D-2026-10-08-c
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

```

## Principles in force the candidates argue against

none
