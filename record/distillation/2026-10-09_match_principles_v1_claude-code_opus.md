# Candidate principles of Luthier, 2026-10-09

Written by `scripts/match_principles.py` (match_principles v1) for Luciano to mark. Two steps, each a model's reading:
the candidates were found blind by `find_principles_v2` (sha256 5eb0cb1b3e6b, opus, effort
low; it saw only the lineages and the criterion of infectability), then set against the principles in
force, the log and the objectives by `match_principles_v1` (sha256 007b56b7e8bb, opus, effort low).
Whose words each quote is and its source were filled in from the rows by the scripts. Under each candidate, a
Mark: line for ok, no, or a correction.

```
C1  A type is the proposition its values must satisfy, extended to functions whose type is their
    laws, so membership is a guarantee.
Scope:      language
Quote:      "los tipos tienen que ser conceptos, tipos como proposiciones y los tipos incluyen
            también funciones, funciones y funciones de orden superior"
Said by:    Luciano, 2026-05-26 12:33
Source:     WhatsApp Ptt 2026-05-26 at 12.32.24.md [00:38] (row day:2026-05-26:tipos-como-conceptos-y-proposiciones)
Found:      conceptual. collapsing type, test and proposition into one thing reorganizes what it
            means to define anything, so a function's type is the law it obeys.
Harms:      punishes code whose guarantees cannot be stated as laws
Harms:      can make every definition carry proof obligations it does not need
Harms:      excludes quick prototyping where a bare value suffices
Against:    new
Assumption: That membership in a type can carry a checked proposition so nothing is verified twice
            (O2); false if laws end up decorative and values still get re-checked downstream.
Would have guided (for P13, later): D-2026-10-07-b, D-2026-10-07-d, D-2026-10-07-e
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C2  Code is a datum of the language itself, so a program can be built, inspected and run by other
    programs, and Luthier operates on Luthier.
Scope:      language
Quote:      "La idea de que el codigo sea dato es muy, pero muy fuerte en cuanto a la flexibilidad
            que ofrece pero es notable que los lenguajes modernos no sigan ese camino Lispeano."
Said by:    Luciano, 2022-06-15 08:55
Source:     2022-06-15 Sin título 2 .md line 13 (row written:2022-06-15_sin-titulo-2:codigo-es-dato)
Found:      conceptual. erasing the code/data line lets the language operate on itself, so the
            interpreter, the trace and the verifier all become ordinary data.
Harms:      homoiconicity invites self-hacking if eval injects arbitrary terms
Harms:      a program manipulating its own code is harder to reason about
Harms:      blurs a distinction many programmers rely on for safety
Against:    new
Assumption: That a self-applied, code-as-data kernel buys the flexibility claimed; false if the
            metacircular core proves unimplementable or never used to operate on Luthier.
Would have guided (for P13, later): D-2026-10-08-c
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C3  From a type and a predicate over it, derive a certified subtype, a validating constructor and
    the projection back, the one pattern for values, functions and programs.
Scope:      language
Quote:      "este tipo Almacen que en realidad confunde dos cosas el constructor de almacen y el
            almacen es el concepto fundamental de Luthier (no almacen sino el patron de
            construccion)."
Said by:    Luciano, 2026-09-29 06:00
Source:     2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 58 (row dialogue:175c0408:patron-de-construccion-concepto-fundamental)
Found:      conceptual. one pattern (material type plus predicate yields certified type, validating
            constructor and forgetful projection) is read as the single core act the whole language
            is built from.
Harms:      every construction forced through a predicate check has a cost per build
Harms:      a value you just want cheaply must pay the pattern
Harms:      overgeneralizing one shape risks hiding domain differences
Against:    new
Assumption: That one subtype/constructor/projection pattern covers values, functions and programs
            alike; false if programs or functions need a different construction.
Would have guided (for P13, later): D-2026-10-07-e, D-2026-10-07-f, D-2026-10-07-h
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C4  For each concept find the mathematical object that best represents it and put it as the type's
    invariant, characterizing an operation rather than reproducing its implementation.
Scope:      language
Quote:      "La idea en realidad es buscar el objeto matematico que mejor lo represente y decirlo."
Said by:    Luciano, 2026-10-05 00:35
Source:     2026-10-04_52d3e68e_lee-la-ultima-trascripcion-de-audio.md turn 128 (row dialogue:52d3e68e:buscar-el-objeto-matematico-y-ponerlo-como-invariante)
Found:      ethical. it says a law must state the property that determines an operation up to
            equality, not re-run its implementation, which is a discipline about what counts as a
            real invariant.
Harms:      finding the best mathematical object is slow and may never settle
Harms:      a wrong characterization is worse than an honest reimplementation
Harms:      demands math literacy the everyday coder may lack
Against:    extends P10: Adds that the invariant characterizes the operation up to the presentation's equality, so a second implementation is consistency not characterization and the native definition is one more model certified against it.
Assumption: That stating the law characterizes rather than merely constrains the operation; false if
            a characterizing law cannot be written and only ad hoc postconditions remain.
Would have guided (for P13, later): D-2026-10-07-b, D-2026-10-07-c, D-2026-10-07-e
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C5  Luthier first describes the problem and its equivalences and only then executes; execution is
    the verification of those equivalences, as mathematics verifies rather than runs.
Scope:      language
Quote:      "Hay una idea, que la matemática no ejecuta, porque lo único que hace es verificar
            equivalencias. Entonces, bueno, sí, la ejecución en Luthier sería esa verificación de
            equivalencias"
Said by:    Luciano, 2026-05-30 18:03
Source:     WhatsApp Ptt 2026-05-30 at 18.01.53.md [01:47] (row day:2026-05-30:matematica-no-ejecuta-verifica-equivalencias)
Found:      conceptual. reading execution as mathematics does, verifying equivalences, inverts the
            usual picture: the program describes and the run certifies, with a declarative and an
            executive side.
Harms:      treating execution as verification downplays the real cost of running
Harms:      delegating execution risks a gap between what is checked and what runs
Harms:      a declarative-first stance can stall before anything executes
Against:    new
Assumption: That execution can be read as verifying declared equivalences (the declarative/executive
            map, O4); false if the equivalence proofs cannot be computed by running.
Would have guided (for P13, later): D-2026-10-08-b
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C6  Keep the native core to a handful of primitives, self-extensible and executable by hand, and
    build every complex concept on top of it.
Scope:      language
Quote:      "Luthier tendría que ser ejecutable a mano es decir que uno pudiese con l y papel
            escribir las cosas"
Said by:    Luciano, 2026-05-29 14:14
Source:     2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 7 (row dialogue:20260529T1400:ejecutable-a-mano)
Found:      aesthetic. the demand that a well-written Luthier be executable by hand with pencil and
            paper is an austere standard of economy that shapes every primitive.
Harms:      few primitives push complexity into libraries that grow unwieldy
Harms:      executable-by-hand can conflict with the speed real work needs
Harms:      self-extensibility is a bootstrap burden before anything else
Against:    new
Assumption: That a few primitives suffice to build the rest in Luthier and reduce by hand (O5);
            false if the complex edifice forces primitives that cannot be run on paper.
Would have guided (for P13, later): D-2026-10-08-c
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C7  Luthier is an abstraction mechanism whose aim is to express the invariances of the disciplines
    clearly.
Scope:      language
Quote:      "la idea de luthier es expresar invarianzas de los de las disciplinas"
Said by:    Luciano, 2026-05-29 14:29
Source:     2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 11 (row dialogue:20260529T1400:expresar-invarianzas-de-disciplinas)
Found:      emotive. it names what moves the author to invent the language: a relator of
            invariances, against the statistical predictor, a species mates within itself, electrons
            are fermions.
Harms:      aiming to express every discipline's invariances risks growing to encompass the universe
Harms:      invariance-hunting can detach from any usable program
Harms:      what counts as an invariance is itself a hard judgment
Against:    new
Assumption: That the disciplines' invariances are what Luthier most needs to express; false if no
            design decision turns on expressing an invariance.
Would have guided (for P13, later): no decision in the log
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C8  A declaration without a body is a first-class hole, an opaque name that does not reduce, and
    nothing executes until it is defined.
Scope:      language
Quote:      "porque necesitamos el simbolo para el hueco, ?. No basta con decri f: A-> B y no
            definirlo?"
Said by:    Luciano, 2026-09-29 04:20
Source:     2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 3 (row dialogue:175c0408:por-que-simbolo-hueco)
Found:      conceptual. a bodyless declaration plays axiom, program input, external function,
            pending definition and dead code at once, so one construct absorbs five roles usually
            kept apart.
Harms:      holes everywhere can hide how much is actually undefined
Harms:      deferring bodies invites programs that never become executable
Harms:      a first-class gap complicates reasoning about totality
Against:    new
Assumption: That a bodyless declaration already is the hole, with 'nothing runs until defined' as
            its semantics, needing no External type or ? symbol; false if the five roles need
            distinct constructs.
Would have guided (for P13, later): D-2026-10-07-f
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C9  A function has many equivalent implementations (paths), each with its precision and cost, and
    Luthier chooses among them by expected loss and speed.
Scope:      language
Quote:      "una funci esta funci puede ser implementada de muchas maneras, son los distintos paths y
            cada forma tiene una precisión y una velocidad"
Said by:    Luciano, 2026-05-26 12:33
Source:     2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 1 (row dialogue:20260526T1233:luthier-paths-con-precision-y-velocidad)
Found:      conceptual. one function with many implementations (paths), each with its precision and
            speed, chosen by expected loss, turns a program into a declarative object that
            self-optimizes.
Harms:      many implementations per function multiplies maintenance and testing
Harms:      choosing by measured cost needs a reliable performance database
Harms:      equivalence of paths is the hardest thing to prove
Against:    new
Assumption: That a function admits many equivalent paths and Luthier can choose by loss and speed
            (O4); false if choosing the fastest cannot be done or kept, which Luciano says is not
            yet started.
Would have guided (for P13, later): no decision in the log
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

C10  Verification is one operation, exact when it can compute and statistical when it samples, and
    every value carries the grade of guarantee it was checked to.
Scope:      language
Quote:      "La comprobación de un valor es un cómputo; la de una función es un experimento. Luthier
            tiene que tratar a los dos como la misma operación de construir, sabiendo que uno es
            exacto y el otro estadístico."
Said by:    model, 2026-09-29 05:56
Source:     2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 55 (row dialogue:175c0408:comprobar-valor-computo-comprobar-funcion-experimento)
Found:      conceptual. treating checking a value and checking a function as one construct
            operation, exact or statistical, and reading verification as a Bayesian observer
            updating a posterior, makes the grade of guarantee part of what membership means.
Harms:      sampled verification certifies a risk, never a universal truth
Harms:      a tuned generator can make a false law pass
Harms:      certificate and record proliferate if not pruned
Against:    new
Assumption: That checking a value and sampling a function are one construct differing only in exact
            vs statistical, with every value carrying its grade; false if the two cannot share one
            operation or grades do not compose.
Would have guided (for P13, later): D-2026-10-06-z, D-2026-10-08-a
Conflicts:  none named
Status:     proposed, for Luciano to mark
Mark:       

```

## Principles in force the candidates argue against

none
