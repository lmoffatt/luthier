# Control: naive, the blind filter, 2026-10-10

Written by `scripts/compare_principles.py` (compare_principles v1); judge prompt `compare_principles_v1` (sha256 a69f0e1f6e17),
model opus at effort low. List A is `record/distillation/naive/reference.md`; list B is Luthier's P1 to P14 and F1 to F16;
the judge was not told which is which. Rules fixed in record/controls/README.md before any run.

| candidates | hits | leaks | neither | passes |
|---|---|---|---|---|
| 10 | 8 | 0 | 2 | yes |

## Candidates

- **C1** (hit): A type is a proposition and belonging to a type asserts a guarantee about the value, so types (including function types) are defined by the invariants, preconditions and postconditions they must satisfy.
  - states reference S1: A type is the proposition its values must satisfy, extended to functions whose type is their laws, so membership is a guarantee. *(type is proposition, membership a guarantee)*
  - echoes Luthier F1: Type = theory: a named type is a subtype of a base cut out by executable laws; a value of it is a model. *(type=theory, laws cut the subtype)*
  - echoes Luthier P14: A type is a concept: declared, then defined, and only then inhabited; a function is a value of a defined function type,  *(type as concept declared then inhabited)*
- **C2** (hit): Defining a function also defines the test over it, and that test is run either exhaustively/deductively when provable or statistically (Bayesian sampling) when not, yielding a probability of success rather than a binary certification.
  - states reference S10: Verification is one operation, exact when it can compute and statistical when it samples, and every value carries the grade of guarantee it was checked to. *(verification exact or statistical)*
  - echoes Luthier F2: Laws are executable Bool predicates that the language itself runs as tests on generated cases; defining a function defin *(defining a function defines its test)*
  - echoes Luthier F8: Generators are values derived from the type; statistical laws declare level and power; evidence is read in a Bayesian wa *(Bayesian reading of statistical evidence)*
- **C3** (hit): A certificate is evidence tied by hash to the code and interpreter, graded by level (proved, exhaustive, sampled with named generators and statistical level), and it records the generators, seed and parameters so it is reproducible and composable.
  - states reference S10: Verification is one operation, exact when it can compute and statistical when it samples, and every value carries the grade of guarantee it was checked to. *(value carries grade of guarantee)*
  - echoes Luthier F3: Certificates: persistent, attached to definitions, keyed by content hash, with a grade of evidence (point, sampled, boun *(certificate by hash, graded, chained)*
  - echoes Luthier F10: Provenance: everything derived records its inputs by hash, the script version, every parameter and the seed. *(records params and seed, reproducible)*
- **C4** (hit): Luthier has a tiny core (types and functions, with Pi, Sigma, sum, data, subtype, holes) from which everything else is built, self-extensible and executable by hand with pencil and paper like Lisp.
  - states reference S6: Keep the native core to a handful of primitives, self-extensible and executable by hand, and build every complex concept on top of it. *(handful of primitives, by-hand, self-extensible)*
  - echoes Luthier F11: A minimal kernel, executable by hand, with the interpreter stated in the language. *(minimal kernel executable by hand)*
- **C5** (hit): A function has many implementations (paths), each with its own precision, speed, memory and place of execution; Luthier is at once declarative and an optimization tool that declares what is wanted and openly compares equivalent paths.
  - states reference S9: A function has many equivalent implementations (paths), each with its precision and cost, and Luthier chooses among them by expected loss and speed. *(many paths, chosen by cost/speed)*
  - echoes Luthier F5: One concept, several implementations (native and foreign), tested equivalent against the same laws, costs measured, the  *(several implementations, fastest chosen)*
- **C6** (hit): Code is data: a Luthier program is itself an element of Luthier (meta-recursion is native from the start), modeled as a DAG of definitions where statements commute and temporality emerges from dependency.
  - states reference S2: Code is a datum of the language itself, so a program can be built, inspected and run by other programs, and Luthier operates on Luthier. *(code is a datum, Luthier on Luthier)*
  - echoes Luthier F9: Plan and execution: a timeless plan, actions with laws, a trace with costs, the world reached through pointers pinned by *(timeless plan, dependency-ordered)*
- **C7** (hit): A hole is a declaration without a body, a first-class citizen that plays at once the role of axiom, program input, external function, pending definition and dead code; nothing is executed until it is defined.
  - states reference S8: A declaration without a body is a first-class hole, an opaque name that does not reduce, and nothing executes until it is defined. *(first-class hole, nothing runs till defined)*
  - echoes Luthier F4: Holes: a declaration without body, filled by another file. *(declaration without body)*
- **C8** (neither): The forgetful functor is a central mechanism: a value carries the history of operations applied to it, and a non-invertible selective-forgetting map keeps the decoration from outgrowing the value; which forgetting function you apply defines the language you speak.
- **C9** (neither): Many functions and types form a single mathematical object defined whole by coupled, genuinely dependent laws (its definition graph is a connected cycle); a law relating several functions belongs to the group, not to any one function.
- **C10** (hit): Luthier is language-agnostic: it describes and verifies concepts and equivalences while delegating execution to external code (extern), orchestrating other languages as a kind of butler, with the external world modeled as its own kind of element.
  - states reference S5: Luthier first describes the problem and its equivalences and only then executes; execution is the verification of those equivalences, as mathematics verifies rather than runs. *(describes equivalences, defers execution)*
  - echoes Luthier F6: Extern at a defined type: the type's claims are checked when a value crosses; an undescribed extern is debt. *(extern delegates execution)*
  - echoes Luthier F16: Aimed at scientific data analysis, interoperating with Python. *(interoperates with external languages)*

## Reference items no candidate states (3 of 10)

S3, S4, S7
