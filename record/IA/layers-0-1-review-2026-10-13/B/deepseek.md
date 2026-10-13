1. **Rows of 2.S12 without a law, or translated otherwise.**  
   - Mismatched: row `{ x := a, y := b }` → `(a, b)` and row `e.y` → one-branch `match`; `translation.lth` has `Records` giving `RecordValue [("x", Var "u"), ("y", Var "v")]` and `(Proj (Var "r") "y")`. Row `{ x : A, y : B }` → `(x : A) * B`; `TypeForms` gives `Record [("x", Var "A"), ("y", Var "B")]`. This follows D-2026-10-13-x, but the 2.S12 table still says the old kernel forms.
   - Row 3 (`| p, q := t` under a multi-parameter header) is not tested: `Shapes` second law is `nt (b : Bool)`, one parameter, not a tuple match.
   - Row 11 (`m.f` imported module) has no law; `Atoms` only gives `nm "x"` → `Var "x"`.
   - Row 20 (`w1 <- act w0 ...`) has no law.
   - Row 24 (`-x`) only tests `Int`: `Negation` gives `bin "-" (Lit (IntConst 0)) (Var "i")`; no `0.0 - x` on `Float64`.
   - Rows 14–16 (`Bool`, `Maybe A`, `Failures E`) are core definitions, so perhaps not required here, but no translation law states them.

2. **Rules of chapter 4 misstated.**  
   - 4.R2: `violatesR2Exists` only checks existence: `anyUnknown p (concat (dOf p a) (bOf p a))`. It accepts a declared-only type in type position outside its theory. Program: `A : U` then `f : A := extern "x"`; 4.R2 rejects, predicate false.
   - 4.R3: `predicateUntouched` uses `untouched k (patternBinds k q) law`, but `untouched` returns `false` on `nil`, so `{ _ : T | true }` is accepted. Also `lawNames` only sees `just (name "Bool")`, so parameterized laws are invisible.
   - 4.R9: `violatesR9` checks application argument mismatch: `not (t.refines at d)`. It does not check function-type variance. Program: `f : A -> B`; `h : A' -> B' := f` with bad variance; 4.R9 rejects, predicate false.
   - 4.R12: `violatesR12` only counts top-level `definedNames`: `count n (definedNames p) >= 2`. Block rebinding is not checked. Program: `f : Int := { x := 1 ; x := 2 ; x }`; 4.R12 rejects, predicate false.
   - 4.S14: `violatesS14` only sees `t == just (name "Bool")`, so a parameterized unclaimed law like `law (x : Int) : Bool := x == x` is accepted.

3. **Approximations.**  
   - Reading a law as a definition at `Bool` is unsound: `lawNames` uses `just (name "Bool")`, but 4.R6 allows `T -> Bool`, `T -> Failures E`, and `Law T`. Parameterized laws are missed.
   - Reporting rather than rejecting loose functions is acceptable as an interim, but `looseFunction` is wrong: `nonEmptyBinders bs or (match t { just (binop o l r) -> o == "->" ... })` flags every function with binders, not only a bare top-level exponential.
   - `ReportsExactly` is not logically vacuous, but testing it by random programs is vacuous in practice. The domain is `NamedIn`, yet a random generator rarely produces a name that violates a rule, so `reported == violates` is usually `false == false`. The generator must draw from each rule’s violating and non-violating programs, e.g. `tests/spec/r*_*.reject.lut` and `r*_*.accept.lut` plus mutations; or split the law over `Violates` and `DoesNotViolate` subtypes. L9.6 applies: the distribution must include the edges.

4. **Typing.**  
   Not right and not enough. `TypeOfLam` returns `true` when the body does not type: `match t.typeOf ... { nothing -> true ; just bt -> ... }`. `TypeOfApp` only tests an application of a literal lambda with `Int`. There are no laws for `Pi`, `Sigma`, `Sum`, `Data`, `Subtype`, `Record`, `Proj`, `Match`, or `FloatConst`. `same` and `refines` are underdefined. 4.R11’s pattern case (`match m { just y -> a }`) is absent: `BranchRefines` only handles `if` on a variable. So 4.R6, 4.R8, 4.R9, and 4.R11 can be satisfied vacuously or accept ill-typed terms.

5. **Names.**  
   `namesIn` respects many binders (`pi`, `sigma`, `lambda`, `match`, `subtype`, record law), but it does not compute D(n)/B(n) correctly. In `itemsNames`, `rebind x t -> concat (namesIn k t) (itemsNames k rest e)` does not remove `x` from later items, so `{ x <- 1 ; x }` returns `x` as free. `quoted a -> namesIn k a` descends into quoted syntax, though quoted names are data, not free variables. `sigmaNamed x a y b` removes both `x` and `y` from `b`, but the second name is a label, not a binder. `patternBinds` also depends on the global constructor list, so a variable named like a constructor is misread.

6. **What I would change first.**  
   Finish `Typing`: add proper laws for application, type formers, `same`, `refines`, and pattern `branchContext`, and make `typeOf` total enough that ill-typed terms do not satisfy the laws. Reason: 4.R6, 4.R8, 4.R9, 4.R11, and any sound law detection all read types through `Typing`; until it exists, those predicates and the `Bool`-law approximation remain either vacuous or wrong.