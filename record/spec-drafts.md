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
| 1 Terms and notation | the §0 of 04, 05, 06, 08, 09 | bd4537e | | | |
| 2 Grammar | 02 | 02, 08 §12 at bd4537e | | | |
| 3 Kernel | 04 | 04 at bd4537e; D-2026-10-12-x (Term as data) | | | |
| 4 Static semantics | 05 §1 to §6, §8 | 05 at bd4537e; D-2026-10-12-z | | | |
| 5 Laws | 05 §9 | 05 §9, 11 §2 and §5 | | | |
| 6 Certification | 05 §7, 03 §4 | 05 §7, 03 §4, 08 §8 and §9 | | | |
| 7 Tests and generators | 08 | 08 at bd4537e; D-2026-10-12-y (grades), -r | | | |
| 8 The demand and the plan | | 02 §8 and §9 | | | |
| 9 Specimens and the planner | | 04 §6, 05 R10 | | | |
| 10 Actions and the world | | 05 R5 and R12, 02 §9, 09 | | | |
| 11 Numbers | 06 | 06 at bd4537e; D-2026-10-12-y (D6) | | | |
| 12 Files and tools | 03 §1 to §4 | 03, 05 §7 as implemented; D-2026-10-12-y (D7) | | | |
