# Principles of Luthier, asked naively, 2026-10-10

Written by `scripts/naive_principles.py` (naive_principles v1). Prompt `naive_principles_v1` (sha256 f28d1cbd5fe5),
model opus at effort low via claude-code (2.1.197 (Claude Code)); the model saw every row
of the timeline (date, who, the idea) and was asked for the rules and principles, nothing more.
Inputs by sha256: `record/ideas/timeline.jsonl` b18b5806955d.
Rows shown: 2322. The quote is the first row each candidate cites, filled in by the script.

```
C1  A type is a proposition and belonging to a type asserts a guarantee about the value, so types
    (including function types) are defined by the invariants, preconditions and postconditions they
    must satisfy.
Quote:      "con tapp quise explorar la idea de que las clases implican predicados y que el codigo es
            dato."
Said by:    Luciano, 2022-06-15 08:55 (row written:2022-06-15_sin-titulo-2:clases-implican-predicados)
Rows:       10

C2  Defining a function also defines the test over it, and that test is run either
    exhaustively/deductively when provable or statistically (Bayesian sampling) when not, yielding a
    probability of success rather than a binary certification.
Quote:      "La idea central del tapp es que al declarar una funcion vos declaras que es lo que la
            funcion debe cumplir como un test y entonces es posible generar tests automaticos."
Said by:    Luciano, 2022-08-03 11:56 (row written:2022-08-03_haskell:declarar-funcion-es-declarar-su-test)
Rows:       10

C3  A certificate is evidence tied by hash to the code and interpreter, graded by level (proved,
    exhaustive, sampled with named generators and statistical level), and it records the generators,
    seed and parameters so it is reproducible and composable.
Quote:      "no la semilla ni los rangos del generador, así que la corrida no es reproducible desde
            el certificado. Lo arreglo: cada corrida elige y guarda una semilla, guarda los
            parámetros de generación y una descripción del dominio de cada variable"
Said by:    model, 2026-09-30 07:10 (row dialogue:890a551c:certificate-must-be-reproducible)
Rows:       10

C4  Luthier has a tiny core (types and functions, with Pi, Sigma, sum, data, subtype, holes) from
    which everything else is built, self-extensible and executable by hand with pencil and paper
    like Lisp.
Quote:      "tendría que ser que solamente hay tipos y hay funciones"
Said by:    Luciano, 2026-05-29 14:00 (row day:2026-05-29:reducir-a-tipos-y-funciones)
Rows:       10

C5  A function has many implementations (paths), each with its own precision, speed, memory and
    place of execution; Luthier is at once declarative and an optimization tool that declares what
    is wanted and openly compares equivalent paths.
Quote:      "tiene una función, esta función puede ser implementada de muchas maneras, son los
            distintos paths y cada forma tiene una precisión y una velocidad"
Said by:    Luciano, 2026-05-26 12:33 (row day:2026-05-26:paths-distintas-implementaciones)
Rows:       10

C6  Code is data: a Luthier program is itself an element of Luthier (meta-recursion is native from
    the start), modeled as a DAG of definitions where statements commute and temporality emerges
    from dependency.
Quote:      "Hay que pensar que el código de Luthier sea un elemento de Luthier ya también desde el
            vamos. El código es el primer elemento."
Said by:    Luciano, 2026-05-29 14:38 (row dialogue:20260529T1400:codigo-es-el-primer-elemento)
Rows:       10

C7  A hole is a declaration without a body, a first-class citizen that plays at once the role of
    axiom, program input, external function, pending definition and dead code; nothing is executed
    until it is defined.
Quote:      "el **hueco**: una definición con tipo y sin cuerpo, `f : A → B := ?`. Una sola cosa
            cumple cinco papeles: axioma, input del programa, función externa que el entorno llena,
            definición pendiente, código muerto. Tu principio "no ejecutás hasta que está definido"
            es su semántica exacta"
Said by:    model, 2026-09-28 20:56 (row dialogue:175c0408:hueco-cinco-papeles)
Rows:       10

C8  The forgetful functor is a central mechanism: a value carries the history of operations applied
    to it, and a non-invertible selective-forgetting map keeps the decoration from outgrowing the
    value; which forgetting function you apply defines the language you speak.
Quote:      "de qué función de olvido le aplicás a los tipos, es un, digamos, eso te define
            básicamente el lenguaje que estás hablando ... los functores de olvido serían, digamos,
            uno de los componentes más importantes de Luthier"
Said by:    Luciano, 2026-05-29 14:59 (row dialogue:20260529T1400:funtores-de-olvido-definen-el-lenguaje)
Rows:       10

C9  Many functions and types form a single mathematical object defined whole by coupled, genuinely
    dependent laws (its definition graph is a connected cycle); a law relating several functions
    belongs to the group, not to any one function.
Quote:      "muchas funciones y tipos van en conjunto ... como los objetos matemáticos, como el grupo
            ... si vos tenés un objeto matemático, está definido todo junto. O sea, vos no podés
            definir una parte sola del objeto matemático"
Said by:    Luciano, 2026-10-03 23:29 (row dialogue:20261003T2329:functions-and-types-go-together-as-math-objects)
Rows:       10

C10  Luthier is language-agnostic: it describes and verifies concepts and equivalences while
    delegating execution to external code (extern), orchestrating other languages as a kind of
    butler, with the external world modeled as its own kind of element.
Quote:      "que tenga los mínimos componentes nativos posibles, cosa que básicamente sea así, un
            lenguaje puente"
Said by:    Luciano, 2026-05-27 13:42 (row day:2026-05-27:minimal-bridge-language)
Rows:       10

```
