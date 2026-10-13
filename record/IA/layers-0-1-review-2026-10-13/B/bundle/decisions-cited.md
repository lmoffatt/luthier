# Decisions cited by the files of bundle B

From record/decisions.md at 869fc4cb3434a4583d19a9a6870ab43e6d2a1238.

D-2026-10-11-b  An if without else is a guarded value: `if c then a` is `if c then just a else
                nothing` when c is a Bool, and `ok a` or `failed` with the first failure when c
                is a Failures E (D-2026-10-11-a), which a demand for Maybe forgets. Without
                effects (L18) a branch that does nothing has no meaning, so this is the only
                reading; a forgotten else is caught by the type checker (a Maybe where a value
                was expected). An else belongs to the nearest if without one. Precedent: Rust
                bool::then, Scala Option.when.
Author:     Luciano
Quote:      "monoide (T:U) (op:T->T->T ) -> Maybe monoide := if (leyesdeMonoide T op ->
            monoide{T op}" (note); "acepto eso, entonces." (chat)
Source:     record/Lucianos ideas/El problema de las tipos recursivos.txt (0cbe437); chat
            (session of 2026-10-11); record/recursive-types-and-objects-2026-10-11.md §3
Kind:       language design, grammar. For L18 (a definition has no effects), P8 (no more
            bureaucracy than it pays for). Sugar only: no kernel construct added
Status:     current; spec amended (02 §3, 04 §5); not implemented

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

D-2026-10-12-x  A new principle, L14: what can be written in Luthier is written in Luthier. The
                specification of how Luthier runs is a theory in Luthier where the kernel can
                express it; the libraries' theories, the generators, the plan, the certificate and
                the program itself (`Program`, `Term` as data) are values of Luthier; the host
                implements and is a specimen certified against the statement; two orders of
                bootstrapping are two paths to one theory; what the kernel cannot express yet is
                written in the host and marked as a hole. `Program` and `Term` as data enter version
                0.
Author:     Luciano for the principle and for Term as data in version 0; Claude for the four
            clauses' wording, proposed
Quote:      "todas las especificaciones de como se corre luthier tienen que estar escritas en
            luthier, de ser esto posible."
            "La implementacion puede ser en python, of course y podemos intentar ambos caminos"
            "Y podemos agregar el principle de que si se puede se escribe en Luthier"
            "eso es el boostrap no?"
Source:     luthier@a066adc:record/plan-spec-2026-10-12-decisions.md:85
            luthier@a066adc:record/plan-spec-2026-10-12-decisions.md:86
            chat:4f7f0dc5:1046
            chat:4f7f0dc5:1056
Kind:       principles (L14 new, under G0; L7, W2, W5 as precedents). For G0, L7, P13 (the decisions
            it already guided: D8 of the spec plan, W5's restatement, Term as data in version 0)
Status:     current; L14 in record/principles-language.md, its clauses proposed, his mark pending

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

D-2026-10-13-n  His marks on the plan from zero and on the nine clauses of the second screen. The
                plan: Z1 (Luthier's own theories first, those that allow bootstrapping first), Z3
                (a parser first), Z4 (retire the old code), Z5 (import names what enters with its
                theory, the theory itself imported from a `.lth` first), Z6, Z7, and Z8 enforced
                (a theory file is a `.lth`, and the checker rejects an extern, an action or a model
                value in it); Z2 unmarked, taken as recommended. The principles: L2.6, L6.13,
                L6.14, L9.11, L9.12, L12.7 settled; L8.9 settled with his note that `W` has a
                thousand laws associated with it, none of which defines it; L14.6 settled with his
                note that a theory is refined when its specimens show it wrong, a false positive for
                one; L12.6 rewritten on his correction: Bayesian evidence is a likelihood, a density
                of any value, and not this; what sampling gives is the probability of a
                counterexample not yet seen.
Author:     Luciano
Quote:      "Yes, Luthiers own first, specially the ones that allow bootstrapping"
            "OK, of course LinearAlgebra had to be imported from a .lth first"
            "Yes, enforced"
            "pensaba si el W no tiene laws, pero si, tiene miles de laws asociadas a el, pero no lo
            definen."
            "Si, pero luego las teorias se podrian refinar, por ejemplo al detectar falsos
            positivos."
            "el tema es que evidence en realidad no va de 0 a 1, la evidence bayesiana es una
            likelihood y puede tener cualquier valor, es una densidad de probabilidad."
            "otra cosa es la probabilidad de encontrar un contraejemplo, ahi si tiene mas sentido
            hablar de probabilidad"
Source:     luthier@93be21b:record/plan-from-zero-2026-10-13-decisions.md:25
            luthier@93be21b:record/plan-from-zero-2026-10-13-decisions.md:83
            luthier@93be21b:record/plan-from-zero-2026-10-13-decisions.md:131
            luthier@93be21b:record/principles-2026-10-13-b-for-his-marks.md:26
            luthier@93be21b:record/principles-2026-10-13-b-for-his-marks.md:31
            luthier@93be21b:record/principles-2026-10-13-b-for-his-marks.md:52
            luthier@93be21b:record/principles-2026-10-13-b-for-his-marks.md:53
Kind:       plan and principles (Z1 to Z8; L2, L6, L8, L9, L12, L14; spec 12). For P13
Status:     current; amends D-2026-10-12-ad (no `la := import "x.lut"`) and -af (the import line
            carries the theory), and D-2026-10-13-m (the probability is of a counterexample)

D-2026-10-13-o  His answers on the review of the first code (record/IA/first-code-review-2026-10-13).
                Q1: a sum is a `data` without recursion; a `data` is freely generated by named
                constructors, recursive or not, and its constructors mean something only through
                observers bound to them by laws (G1, 4.S19); a constructor no observer distinguishes
                means nothing. Q2 (a): a theory file may hold the definitions its laws need and a
                value that is part of the theory, never what touches the world or a model of a
                theory declared elsewhere. Q3: a bare term is an act, a datum of the module. Q4: a
                trailing separator is allowed, and an import line names several things. Q5: no
                positions in the tree; errors carry them. Q6: `operator` and `quote` are keywords.
                Q7: a parameterized theory repeats its binders in its definition by laws. Q8: `let`
                retired; negation a level above application; a single labeled field with a law is a
                subtype, `record` holds two or more names with an optional law; 12.S8 retired, a
                model is a named value of its theory; the stale prose of chapter 2 fixed.
Author:     Luciano; the recommendations the model's, on the four reviewers
Quote:      "como nos aseguramos que la estructura data tenga significado? donde expresamos las
            leyes que justifican a cada componente?"
            "Si, me parece la respuesta."
            "a"
            "acepto tu sugerencia, y ya estan mis respuestas."
Source:     chat:da165104:2221
            chat:da165104:2243
            luthier@1b07bc8:record/IA/first-code-review-2026-10-13/questions-for-luciano.md:54
            chat:da165104:2288
Kind:       language and spec (2.S5, 2.S6, 2.S9, 2.S15, 2.S19, 2.S20, 2.S21, 3.R3, 3.S7, 4.R3,
            4.R4, 4.R6, 12.S8, 12.S22, 12.S23; principles L2.6). For G1, L14, P5, P16
Status:     current. The model's, by the same mark, reversible: a record has two or more names, so
            `{ x : A }` with no law is not a form (it is `A`)

D-2026-10-13-p  A definition is a concept, and a collection of types is not. An alias names a
                structure: a shape we use before we know what it is for. A definition promotes it
                to a theory, and what makes it one is a law it must follow, a law that states the
                role of each part. For a `data`, distinct constructors are free by construction and
                give no role; an observer that only lists the constructors (`keywordText`) with a
                law of injectivity is an automatic accessor, and does not count. A `data` whose
                constructors have no law of their role is a collection, written as an alias of a sum.
                So `Keyword`, `Op` and `TokenKind` in grammar.lth go: keywords are the words the
                grammar takes as literals, operators the literals of its precedence levels, token
                kinds its categories, and their roles are laws over `luthierSyntax`. Precedence is
                one clear table, the open forms (`(x : A) ->`, `(x : A) *`, `\`, `if`) at its
                loosest level. His marks on round 2 besides: R1, R2, R5, R6 as recommended.
Author:     Luciano; the application to the three enumerations and the precedence table the model's
Quote:      "esto es cheating. La idea es que haya leyes acerca de los campos de data, algo que
            obligue a pensar para que uso cada cosa"
            "Un nombre es un concepto, una coleccion de tipos no es un concepto."
            "necesitamos reglas claras y obvias de precedencia de operadores."
            "hay una sola observacion relevante, es mi cruzada para que una definicion sea un
            concepto, una idea. Una coleccion de tipos no lo es."
            "Es la idea del alias, un alias es una estructura que no sabemos para que esta, la usamos
            pero no definimos su funcionalidad aun. Luego la promovemos a teoria."
            "Entonces con un alias le ponemos un nombre a una estructura, pero para que sea teoria
            tiene que tener una definicion que le dice que  ley tiene que seguir."
Source:     luthier@13641e8:record/IA/first-code-review-2026-10-13/round-2/questions-for-luciano.md:48
            luthier@13641e8:record/IA/first-code-review-2026-10-13/round-2/questions-for-luciano.md:50
            luthier@13641e8:record/IA/first-code-review-2026-10-13/round-2/questions-for-luciano.md:64
            chat:da165104:2551
            chat:da165104:2568
            chat:da165104:2568
Kind:       principles (L2.7 new; Terms) and spec (2.S8, 3.R3, 4.R3, 4.R4). For G0, L2, L8,
            D-2026-10-07-e
Status:     current; reverses the model's reading of Q1 in D-2026-10-13-o (observers with laws of
            injectivity)

D-2026-10-13-q  Three readings `grammar.lth` took where chapter 2 was silent, which the files of
                round 3 depend on, are decided: string escapes `\"`, `\\`, `\n` (2.S1); `_` as a
                pattern atom (2.S5); the layout readings of 2.S4 (the braces of a `data` separate
                constructors by line breaks, a `}` at column 0 closes its brace, blank and comment
                lines are dropped with their line breaks). The trailing comma in a list stays
                proposed.
Author:     Luciano
Quote:      "Ok a los tres."
Source:     chat:da165104:2971
Kind:       spec (2.S1, 2.S4, 2.S5)
Status:     current

D-2026-10-13-s  Braces inside the scrutinee of a `match` go in parentheses: the first `{` after
                `match` and its scrutinee opens the arms. Found by ChatGPT writing the parser:
                `match f { p -> q } { r -> s }` had two trees, the match on `f` applied to the block
                `{ r -> s }`, or the match on `f { p -> q }` with the arm `r -> s`. Chosen over
                forbidding a `match` to be applied without parentheses (one rule less in the
                grammar, but the scrutinee would swallow a block). The scrutinee is a term of the
                levels `or` to `.field` whose atoms carry no braces outside brackets; open forms,
                `->` and `&` there go in parentheses too.
Author:     Luciano, on the model's recommendation (A of two)
Quote:      "A"
Source:     chat:da165104:3515
Kind:       spec (2.S9) and grammar.lth
Status:     current

D-2026-10-13-t  The laws of role of the core's `data` (L2.7, 4.R3): `Bool` has `not`, `and`, `or` and
                the laws of a Boolean algebra; `Nat` has its own (Peano's, and those of its
                operations); `Unit` is the terminal object (one map into it from every type) and
                `Empty` the initial one (one map out of it to every type). They are stated in
                `kernel_laws.lth` (step 2.1 of the plan from zero). The model's reading of "first"
                is initial. `List` is the free monoid (`nil` the unit of `append`, associative;
                `fold` gives `cons` its role), the model's proposal, accepted ("Si, dale").
Author:     Luciano
Quote:      "Bool tiene not, and y todas las leyes booleanas, Nat tiene las suyas. Unit y Empty son first y terminal object"
            "Ves que todo tiene leyes, es cuestion de buscarlas."
Source:     chat:da165104:3712
            chat:da165104:3733
Kind:       spec (3.S7, 3.S36), the plan (step 2.1), principles (L2.7, his words added)
Status:     current

D-2026-10-13-w  A labeled sum is written in braces with `||` between alternatives,
                `{ circle : Float64 || square : Float64 }`; `,` and `||` are not mixed at one level,
                a mixture nests (`{ s : { a : A || b : B }, d : D }`); a sum has two alternatives or
                more (one is a record); a line beginning with `||` continues inside braces. `< >`
                for sums is retired, and with it the rule that a comparison by `>` inside `< >` goes
                in parentheses (2.S9, proposed, never marked) and the form `(a : A) + (b : B)`; the
                anonymous sum stays `A + B`. `|` keeps its two roles, "such that" in a subtype and
                the start of a clause. Reasons: `<` and `>` are left with one meaning, comparison;
                one bracket for all structures, `,` the product and `||` the sum; a sum is a
                disjunction (Curry-Howard), hence the sign of "or".
Author:     Luciano (braces, then `||`); no precedence between `,` and `||` the model's
Quote:      "y si usamos || para la suma  (como C++ para el o)?"
            "SI, aplicalo asi."
Source:     chat:52b10bff:3663
            chat:52b10bff:3676
Kind:       spec (2.S4, 2.S8, 2.S9, 2.S10, 2.S12, 3.S3, 3.S4, 4, 11) and grammar.lth
Status:     current; reverses the proposed `>` rule of 4bc59f4

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
