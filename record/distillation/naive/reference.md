# Reference for the naive run on Luthier: the pipeline's candidates

The ten candidates found blind by find_principles_v2 on 2026-10-09 (step A2 of the night's plan), from `record/distillation/2026-10-09_find_principles_v2_claude-code_opus.json`
(sha256 36069e9a04e8033edc02ef14ff20b1c71eb5ab4cc6c4031a0dd3580db5fc49dc), renamed C<n> to S<n> so that they do not collide with the ids of the candidates judged. Written
before the naive run.

- S1 A type is the proposition its values must satisfy, extended to functions whose type is their laws, so membership is a guarantee.
- S2 Code is a datum of the language itself, so a program can be built, inspected and run by other programs, and Luthier operates on Luthier.
- S3 From a type and a predicate over it, derive a certified subtype, a validating constructor and the projection back, the one pattern for values, functions and programs.
- S4 For each concept find the mathematical object that best represents it and put it as the type's invariant, characterizing an operation rather than reproducing its implementation.
- S5 Luthier first describes the problem and its equivalences and only then executes; execution is the verification of those equivalences, as mathematics verifies rather than runs.
- S6 Keep the native core to a handful of primitives, self-extensible and executable by hand, and build every complex concept on top of it.
- S7 Luthier is an abstraction mechanism whose aim is to express the invariances of the disciplines clearly.
- S8 A declaration without a body is a first-class hole, an opaque name that does not reduce, and nothing executes until it is defined.
- S9 A function has many equivalent implementations (paths), each with its precision and cost, and Luthier chooses among them by expected loss and speed.
- S10 Verification is one operation, exact when it can compute and statistical when it samples, and every value carries the grade of guarantee it was checked to.
