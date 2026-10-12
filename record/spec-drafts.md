# The drafts of the specification

The record of how each chapter of `docs/spec/` was written: its sources by commit, who wrote it,
the commits, what changed by draft (P2, P3). The sibling of the drafts table of
`record/principles-language.md`. Started 2026-10-12 with step 0 of
`record/plan-spec-2026-10-12-execution.md`.

## Before the chapters

The specification of 2026-10-04 to 2026-10-11, six files under one numbering shared with the guide
and the rationale: `02-grammar.md`, `03-libraries.md`, `04-kernel.md`, `05-static-semantics.md`,
`06-numbers.md`, `08-tests.md`, all at bd4537e. They describe version 0 as implemented, with the
laws into `Bool`, seven grades and no demand, planner, cost or world. Each chapter below names
which of them it replaces; the file is deleted in the commit that writes the chapter, and git
keeps it.

The libraries' table of `03 §5` (2026-10-11), kept here by D8 of the spec plan until the manual
exists:

| file | what it holds |
|---|---|
| `real`, `real_python` | functions on `Float64` (declared, bound to Python's math), `approx` (the equality of `Float64` within a relative tolerance), `NonNegative`, the tolerances of laws |
| `random` | `Gen A = Nat -> Int -> A * Int`, a congruential generator, generators for `Int`, `Nat`, `Bool`, `Float64`, lists |
| `array`, `array_python` | `Vec`, `Mat`, their shapes, native definitions of every operation including the determinant and Jacobi's spectrum, numpy leaves certified against them |
| `algebra`, `algebra_python` | setoids, rings, fields, vector and inner product spaces, linear maps; instances on `Int`, `Float64`, vectors |
| `probability` | samplers and likelihoods, the kernel with its three presentations (sampler, likelihood, transform), the Gaussian and profile constructions, the ensemble diagnostics |
| `belief` | belief families, discrete and Gaussian (Laplace) beliefs, their laws |
| `optimization` | Levenberg-Marquardt in pieces, each with its law |
| `table`, `table_python` | native tables, the CSV codec as a theory and its model |

## The chapters

| Chapter | Replaces | Sources | Written by | Draft 0 | Later drafts |
|---|---|---|---|---|---|
| 1 Terms and notation | the §0 of 04, 05, 06, 08, 09 | bd4537e | Sonnet, brief at 3445ad8 | 2026-10-12: 15 statements, no rules; 1.S11 (the symbol table: ε the demand's cutoff, d a distance, L a Lipschitz constant, p a predicate or a probability, n cases or samples) proposed, the meanings of L and p the agent's guesses; 1.S12 reads the old grades through the five of Terms (D-2026-10-12-y); question: is that mapping chapter 1's or chapter 6's | |
| 2 Grammar | 02 | 02, 08 §12 at bd4537e | Sonnet, brief at 3445ad8 | 2026-10-12: 6 rules, ~20 statements; 2.S19 (test extended, profile, gen removed) and 2.S20 (quote, eval) proposed; `let`, negation, implicit parameters added from the parser; questions: the metric after `sampled` as a plain name; primitive and axiom bodies kept in 2.S5 | 2026-10-12, integration: 2.S19 decided D-2026-10-06-ac (d84904b) |
| 3 Kernel | 04 | 04 at bd4537e; D-2026-10-12-x (Term as data) | Sonnet, brief at 3445ad8 | 2026-10-12: 3 rules, ~38 statements; 3.S29 Term/Program as data and 3.S35 no self-modification decided; 3.S30 to 3.S34 (the four choices, canonical form), 3.S38 `lib/term.lut`, 3.S12 `Cost` proposed; questions: does `Failures E` stay a law type; is the kernel described as a theory; weak points: beta/delta/iota/prim marked implemented on checked-only programs | |
| 4 Static semantics | 05 §1 to §6, §8 | 05 at bd4537e; D-2026-10-12-z | Sonnet, brief at 3445ad8 | 2026-10-12: 13 rules, ~21 statements; R10, R11, S16, S20, S21 (`WellFormed` in `lib/program.lut`) proposed; decided without an id: R10 (2026-10-05), R11 (2026-10-06), consistent-not-characterized, the R5/R7 details of 2026-10-05; 4.S17 names files not written; question: does 4.S9 keep concrete type against theory as two kinds | 2026-10-12, integration: 4.R10 decided D-2026-10-05-a, 4.R11 D-2026-10-06-aa, 4.S20 D-2026-10-05-b (d84904b) |
| 5 Laws | 05 §9 | 05 §9 at bd4537e; rationale 11 §2, §5; principles L3, L12 at 2b79c02; D-2026-10-12-al, -am | Opus, the integrating session, no brief | 2026-10-13: 14 statements, no rules; a law needs only `verdict : V -> C` (5.S3, proposed); `exact c = c ≤ 0`, and a sixth law for spec 6.S5 proposed (`⊤ ≤ 0` false, else the trivial algebra breaks L12.2); checks and `Failures E` to a library `lib/checks.lut` (5.S10, proposed); found: `Failures E` is not in the interpreter, so 3.S12 and 4.R6 corrected | |
| 6 Certification | 05 §7, 03 §4 | 05 §7, 03 §4 at bd4537e; principles L9, L10 at 2b79c02; D-2026-10-12-al | Opus, the integrating session, no brief | 2026-10-12: 1 rule (6.R1 cite, implemented), 16 statements; certification over a cost type `C` taken as a parameter (D-2026-10-12-al), with five operations asked of it (6.S5, proposed: order, 0, ⊤, ⊕, lift); proposed: 6.S5, 6.S6 (fields), the chain of 6.S8, 6.S9 (delegation), 6.S13 (monotone), 6.S16 (`lib/certification.lut`), and the grade correspondence placed in that file (6.S7, for D-2026-10-12-ag); found: the 1/n averages of D-2026-10-12-p are not associative, so not a `⊕` along a path | 2026-10-12: 6.S5 decided on his mark (D-2026-10-12-am) |
| 7 Tests and generators | 08 | 08 at bd4537e; D-2026-10-12-y (grades), -r | Sonnet, brief at 3445ad8 | 2026-10-12: 4 rules without files (no programs for generators exist), 19 statements, all proposed except 7.S10 (grades, decided -y) and 7.S11 (evidence cost, decided -r); G/C items mapped (G1-3 S1-3, G7 S4, G8 S5, G10-12 S6-8, C1 S9, C2 S10+S11, C3-C10 S12-S19; G4-6, G9 R1-R4); decided without an id: his notes of 2026-10-06; questions: sampling 'cost' renamed 'weight' (collides with Terms), 10 against 50 redraws, grades and conversion as two items; the integrator found it under-claims: `test x with n`, `exhaustive` and `size` are in the parser (`parser.py` 155-161) and budgets exist in `generators.py`, yet nothing is marked implemented; to correct in step 2 | 2026-10-12, integration: statuses corrected on D-2026-10-06-ab and -ac: 16 items decided, S7 implemented, S2 (his candidate), S6, S12, S14 proposed; the parts that run today marked `[implemented]` inline, checked against `parser.py`, `generators.py`, `testing.py` and `cli.py` |
| 8 The demand and the plan | | principles L5, L4; D-2026-10-10-c, -d, -e; spec 2, 6, 12 at e8409ef | Sonnet, brief `record/spec-briefs/08-demand.md` at e8409ef | 2026-10-13: 15 statements, no rules; the interface asked of a library of demands (8.S2: entry, cutoff, delta, assumed, key) proposed; implemented: call by need in `machine.py`, a per-function memo, a session that re-evaluates the whole block; questions: may a result computed under a tighter tolerance serve a looser demand (8.S9 asks equal keys); L5.6 read as extending D-2026-10-10-d's key; integrator: 8.S8's status moved to D-2026-10-10-d | |
| 9 Specimens and the planner | | principles L6, L9.8, L9.9, L10.7, L10.8, L11; D-2026-10-11-m, D-2026-10-12-q, -u; spec 3, 4, 6 at e8409ef | Sonnet, brief `record/spec-briefs/09-planner.md` at e8409ef | 2026-10-13: 17 statements, no rules; nothing chooses between implementations today (9.S2); the interface of a ranking library (9.S14: rank, an order, the `0` of C) proposed, D-2026-10-12-u its first candidate model; question: L6.4 and L6.8 are settled in the principles with no decision id, so 9.S8 and 9.S11 are marked proposed; integrator: `exact` in the ranking table replaced by the `0` of C | |
| 10 Actions and the world | | principles L4, L11; D-2026-10-10-c, D-2026-10-12-m, -ab, -ac; rationale 09; spec 2, 3, 4, 12 at e8409ef | Sonnet, brief `record/spec-briefs/10-world.md` at e8409ef | 2026-10-13: 14 statements, no rules; the world as a token threaded through actions, the interface of a world library (10.S5: W, act, own) proposed; no program can name an action today, `print` exists in no library; questions: L11.7 is proposed in the principles while D-2026-10-12-ac is current; the validation at the first action asking has no entry of its own (cited through D-2026-10-11-n); integrator: the file hash moved out of the world's interface, `checker.py` named for the check-time import | |
| 11 Numbers | 06 | 06 at bd4537e; D-2026-10-12-y (D6) | Sonnet, brief at 3445ad8 | 2026-10-12: 4 rules, 19 statements; S3, S10, S11, S16 to S19 proposed; decided without an id: `toFloat64` stays with the integers (2026-10-05); 11.R3 borrows `n5_arrays.accept.lut` | 2026-10-12, integration: 11.S5 cites D-2026-10-05-c (d84904b) |
| 12 Files and tools | 03 §1 to §4 | 03, 05 §7 as implemented; D-2026-10-12-y (D7) | Sonnet, brief `record/spec-briefs/12-files-and-tools.md` at 3445ad8 | 2026-10-12: 20 statements, 1 rule; S1 (a file denotes a dependent record type, `lib/library.lut`) and S9 (the pure file plus `_python` file pattern) proposed; S17 strict `run` decided; two questions for Luciano: do `--checked` and `--no-record` stay, and does `eval` refuse an uncertified cone as `run` does; the old 03 kept until step 2 | |
