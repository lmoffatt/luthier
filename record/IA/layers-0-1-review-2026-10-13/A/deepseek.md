1. **Laws that are wrong**  
- `kernel_laws.lth` §6: `Beta ... := e.apply (fn y { f y }) x == f x` states eta pointwise, not beta; it does not constrain application of an arbitrary lambda.  
- `term.lth` §5: `IotaPair ... sb.subst f.y (Var y) (sb.subst y f.s b)` uses sequential substitution; for a body using both pattern variables this gives capture, not the simultaneous substitution 3.S16 intends.  
- `kernel_laws.lth` §1: `Object (A : U) : { eq : A -> A -> Bool }` and `Structural (A : U)` claim equality for every `U`, false for function types (spec 4.R8).

2. **Laws that do not determine what they claim**  
- `term.lth` §5: `agree ... nothing -> true ;` — a model `reduce p n t := nothing` satisfies every reduction law.  
- `term.lth` §3: `SubstPassesBinder ... x == f.y or ...` only covers binders not free in the substituted term; a capturing substitution passes all stated substitution laws.  
- `kernel_laws.lth` §6: `ProjectionNamesDistinct ... := not (r.firstName == r.secondName)` only says names differ; swapped or arbitrary names still pass.  
- `term.lth` §2: `AlphaCongruent` only tests singleton lists and `PWild` for `Match`; an alpha that ignores match patterns passes.

3. **Roles (L2.7)**  
- `term.lth` §1: `Primitive : String -> Term ;` has no role law; the header omits it.  
- `term.lth` §1: `FloatConst : Float64 -> Constant ;` and `StringConst : String -> Constant ;` have no role law.  
- `term.lth` §1: `PLit : Constant -> Pattern ;` has no role law.  
- `term.lth` §1: `Datum : Term -> Act ;` has no role law.  
- `kernel_laws.lth` §6: `ProjectionNamesDistinct` only lists that names differ, not what the names do.

4. **The models against their theories**  
- `kernel_models.lut`: `structuralEquality (A : U) : Structural A := { eq := fn x y { x == y } }` breaks on `A = Unit -> Unit`; `==` is not the structural equality the theory requires for functions. Case: `x = fn u { unit }`, `y = fn u { unit }`; `x == y` is not the structural equality of the theory.

5. **Reduction**  
- `Beta` in `term.lth` is faithful to 3.S14.  
- `Delta` is not: it only tests `App (Var f) arg` and forces unfolding even when the argument is stuck, contrary to 3.S15.  
- `Iota` is not fully faithful: pair substitution order is wrong, and the constructor case is skipped by `defines p l`.  
- `ProjOfRecord` is faithful to D-2026-10-13-x.  
- `Prim` is not: it covers only `Int`, not `Float64`, `String`, or structural `==` per 3.S17.  
- `HolesStay` is too narrow: it does not cover a hole inside a term where reduction needs a value.  
- `ValuesStay` is faithful as a value law.  
- `Final` is vacuous when `reduce` returns `nothing`.  
- Fuel treatment `agree` is unsound: `nothing` agrees with everything, so a trivial `reduce` passes all laws.

6. **Against the specification**  
- `kernel_laws.lth` §6 `Beta` is eta, not the `Beta` of 3.S36.  
- `kernel_laws.lth` §6 lacks the named `IfTrue`, `IfFalse`, `CaseNothing`, `CaseJust` that 3.S36 says are stated.  
- `kernel_laws.lth` §5 `Prim` only covers `Int`, against 3.S17’s `Int`, `Float64`, `String` and structural `==`.  
- `Object (A : U)` and `Structural (A : U)` for all `U` contradict L3.1/L3.3 and D-2026-10-12-ak: structures have no equality.  
- `Delta` contradicts 3.S15 on head unfolding.  
- `IotaPair` contradicts 3.S16’s simultaneous pattern substitution.

7. **What I would change first**  
Change `agree` in `term.lth`: `nothing` should not agree with `just`; it should agree only with `nothing`. Reason: as written, a model that always returns `nothing` satisfies every reduction law, so no reduction is actually certified.