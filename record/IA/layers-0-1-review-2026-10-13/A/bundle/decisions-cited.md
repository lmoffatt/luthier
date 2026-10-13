# Decisions cited by the files of bundle A

From record/decisions.md at 869fc4cb3434a4583d19a9a6870ab43e6d2a1238.

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

