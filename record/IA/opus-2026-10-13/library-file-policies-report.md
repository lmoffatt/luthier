# library.lth §4, the file policies: report

Claude Opus 5.5, 2026-10-13, on `library-file-policies-brief.md`. Commit f70ca34 (`src/luthier/lib/library.lth` only).
`luthier parse` exits 0; `luthier check` on the file is clean too.

## What I wrote

`Loader` gains `isCore` and `isLibrary` (on a path, the model's, nothing global) and a third field,
`admitsAt : String -> SurfaceProgram -> Bool`. The helpers `hasPrimitive` and `hasAxiom` read a body
as `hasExtern` reads `extern` (head of an application in a `termBody`). `mentionsR` looks for the
name `R` in type position. `policyFiles` is a small FileSystem: core.lut with a primitive,
lib/algebra.lut with an axiom, lib/money.lut with a primitive, the three reject programs n2, n3, n4,
and `R` in a binder's type and inside an arrow. The laws `PrimitiveOnlyInCore`,
`AxiomOnlyInCoreAndLibraries` and `RNamesNoType` each go one way only ("such a body, outside the
allowed paths, implies not admitted"), and they're conjoined into `Loader :=`. §4 is marked done in the index.

## Where the spec didn't say, and what I read

1. `admits` takes a `FileKind`, but core.lut and a user's model file have the same kind. If `admits`
   refused a primitive in a non-core file, it would refuse core.lut too. So I added `admitsAt` (by
   path) and stated the laws on it. I didn't state how `admitsAt` relates to `admits` (for example
   `admitsAt path p` implies `admits (kind path) p`). That's a one-line law if wanted.
2. Since `isCore` and `isLibrary` are the model's, a model that calls every path core satisfies 11.R2
   trivially. The spec does name the paths (`core.lut`; `core.lut` and `lib/`, 11.R2 and 11.R3). An
   anchoring case law can come once core exists.
3. 11.R1 "`R` names no type": I read it as the name `R` anywhere in a type tree. That covers declared
   types, act binders' types, an alias's right side and a `data` constructor's type. Refinement laws,
   record laws, binder defaults and `e.R` projections are skipped. Not covered: a binder named `R`
   (`(R : U) -> R` is refused, because the use is flagged), defining a type named `R`
   (`R : U := ...`, `R = Real`), and types inside terms (a lambda's typed parameter).
4. The R law refuses in every file, core and libraries included. The spec gives no exception.
5. A primitive in a library that isn't core is refused (11.R2 says core only). lib/money.lut is the
   case.
6. Form: the laws pass the loader's operations to recursive helpers, not the loader itself. Today's
   checker raises 4.R9 on a helper that takes `(l : Loader)`, and on a helper passed as a function
   argument when its parameters use the imported alias `SurfaceProgram` (`f2 okAll` fails,
   `f2 l.admitsAt` passes). That looks like a checker issue worth a look. I didn't touch it.
