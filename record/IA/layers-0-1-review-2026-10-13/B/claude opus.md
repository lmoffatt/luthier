Grounds: `translation.lth`, `program.lth`, `term.lth` (for `Term`, `Alpha`), chapters 2 and 4, `decisions-cited.md`, `principles.md`. Chapter 1 is not in the bundle, so in item 5 I read D(n) and B(n) from how 4.R1, 4.R2 and 4.S15 use them.

## 1. Rows of 2.S12

**Rows with no law:**
- **Clauses over two or more parameters.** The row is `f (x : A) (y : B) | p, q := t` → `match (x, y) {...}`. `Shapes` only tests one parameter (`nt`), where no tuple is formed.
- **`m.f` for an imported module.** No law.
- **`w1 <- act w0 ...`, an action in a block.** No law.
- **`-x` on `Float64` (`0.0 - x`).** Only the `Int` case is stated (`Negation`).
- **`Maybe A`, `Failures E` as alias expansion.** §5 calls these core definitions. But `ActsKept` only expands an alias without binders. An alias with binders (`Maybe A`, `P (A : U) = A * A`, where substitution is the point) is untested.
- **Demand for `Maybe A` forgets `e`.** This part of the `if c then a` row on `Failures E` is unstated.

**Laws that differ from their row:**
- **Records and projection.** `{ x := a, y := b }` → `RecordValue`, `e.y` → `Proj`, `{ x : A, y : B }` → `Record`. The table still says pair, one-branch `match`, and `(x : A) * B`. The file follows D-2026-10-13-x, whose Kind lists 2.S12. So the table lags the decision; the file does not contradict it.
- **Block encoding.** The row says "the definitions of its items with fresh names". `Blocks` fixes a beta-redex, `App (Lam "x" (Var "Int") (Var "x")) (Lit 1)`. A model that elaborates to definitions fails the law. Item 7 explains why the redex is also the wrong reading.
- **`Conditions` reason form.** It writes `PCon "cons" [PVar "x", PVar "xs"]` where the row writes `cons e es`. That is only equal up to alpha if `Alpha` renames pattern binders. `term.lth`'s `RenameBound` covers only `Lam` and `Pi`, so a lawful `Alpha` may reject an elaborator that follows the row.
- **Contexts that do not declare their names.** `term` returns "`nothing` when the term does not elaborate (it does not type)". Yet §2 calls `e.term []` on undeclared `x`, `f`, `m`, `A`, `B`. `typesAndValues` declares `f : Failures E` with `E` undeclared. `Lists` gives no expected type, though the row takes the element type from it. A scope-checking elaborator fails `Atoms`, `Lambdas`, `Patterns` (second case), `Lists`, `TypeForms` and `Conditions`.
- **`A + B` → `Sum [("left", …), ("right", …)]`.** Labels are not bound names, so alpha does not rescue them. Nothing in the bundle fixes `left`/`right`; check 3.S4.
- **Constructor type in `TypeForms`.** `s : List C` is not a constructor of `C`. `term.lth` writes constructor types as arrows (`IntConst : Int -> Constant`); this law writes a non-arrow.

**Unstated forms that are not rows:** `pi`, `sigma`, `sigmaNamed`, `subtype`, `tuple`, `quoted`, and `&`. `&` is the one that matters: every theory head is `T := L1 & L2`, and 4.R6 needs its type.

## 2. Rules of chapter 4 misstated

**4.R1, 4.R2 (`violatesR1`, `violatesR2Exists`) reject well-formed programs.** `namesIn`'s `name s -> [s]` keeps a dotted name whole, and `known` never resolves it (item 5). So every law using `m.f` violates. Constructors are also not `known`:
```
C : U := data { r : C ; s : C }
f (c : C) : C := r          -- rule accepts; violatesR2Exists: "r" unknown
```
This file violates its own rule at line 370, where `bodyApplications (e : Elaboration a)` has `a` unbound.

**4.R2 accepts what it rejects.** `A : U` / `f (x : A) : A := x` has a merely declared type outside its theory. The file says this is todo. But `ReportsExactly` then forbids a correct checker from reporting it (item 3).

**4.R3 accepts what it rejects:**
- The normal theory form, a declared record plus a separate definition by laws, is never checked:
  ```
  M : { eq : A -> A -> Bool, add : A -> A -> A, mul : A -> A -> A }
  Assoc (m : M) (x y z : A) : Bool := m.eq (m.add (m.add x y) z) (m.add x (m.add y z))
  M := Assoc                 -- mul untouched; predicateUntouched only sees inline record/subtype
  ```
- `T : U := { _ : Int | true }` passes: `_` binds nothing, so nothing is untouched.
- `P : Int` / `P := fn p { true }` passes: lambda bodies are not inspected.

**4.R3 on `data` accepts the "cheating" of D-2026-10-13-p.** `isR (c : C) : Bool := c == r` claims `r`, because any `: Bool` definition counts as a law. In the other direction, roles stated in another file always fail. `term.lth` says its type formers get their roles in `program.lth`, so `term.lth` violates 4.R3 by this predicate.

**4.R4 and 4.R5 miss the declare-then-define form**, because they test `t == just universe` on the define act only. Both of these pass:
```
P : U
P := A * B                       -- 4.R4 rejects
T : U
T := extern "python:x"           -- 4.R5 rejects
```
4.R4 is also written as a blacklist where the rule is a whitelist ("only if `t` is a subtype with a predicate … or a `data`"). So `Ints : U := List Int` and `X : U := Int` are accepted. The 4.R5 requirement that `T` be defined is absent.

**4.S14 (`violatesS14`) rejects what the spec accepts.** 4.S14 says an unclaimed law "is a branch … and 4.R2 applies to it". It does not say it is an error. `isEven (n : Int) : Bool := n mod 2 == 0`, unused, is rejected.

**4.R6 (`fits`) rejects every parameterized theory and every multi-argument law:**
- `Elaboration (a : Alpha) : {...}` / `Elaboration (a : Alpha) := ...`: the declared type is `Pi a Alpha Record`. `fits` compares the body against `Pi "_" (Pi a …) Bool` instead of comparing under the binders.
- `Codec : {...}` / `Codec := RoundTrip`: the body type is `Codec -> Table -> Bool`, not `Codec -> Bool`. The `Law` case depends on `&`, which has no elaboration.
- If `Failures E` is expanded as its row says, `Var "Failures"` never appears.

**4.R8 (`containsArrow`) errs both ways:**
- **Over-rejects.** For a `Data` it scans constructor types, which are arrows (`Var : String -> Term`). So `==` on any data with a non-nullary constructor is rejected, including this file's `f == Var "Failures"`. It should scan the argument types of each constructor.
- **Under-rejects.** It looks through `definedBody`, but a theory's base is in its declaration, so `==` on it passes:
  ```
  Codec : { parse : String -> Maybe Int, eq : Int -> Int -> Bool }
  L (c : Codec) (s : String) : Bool := c.eq 0 0
  Codec := L
  Bad (c d : Codec) : Bool := c == d
  ```
- **Misses pattern-bound variables.** `armsApplications` does not extend the context with them, so `match m { just g -> g == g }` is not caught.

**4.R9 (`mismatch`).** It rejects any argument whose type does not refine the domain. 4.R11 and 4.R5 treat a coercion into a subtype as an obligation, not an error. So `recip (p : Pos)` applied to `x : Int` should owe `x > 0`, not be rejected. The check should be on bases, with refinements left as obligations; see also item 7.

**4.R12 and 4.R7.** These are right at the top level. The 4.R12 block part is todo, with the same "exactly" problem as 4.R2.

## 3. The approximations

**"A law is a definition at `Bool`" is neither sound nor complete.** It counts every Bool helper (`member`, `isExtern`, accessors) as a law. That satisfies 4.R3 by accessors and makes 4.S14 reject helpers. It misses laws at `Failures E`, at `Law`, or declared apart from their body.

A better reading is available now from names alone: a law is a definition reachable from some head's `&`-conjunction. That excludes free helpers. An accessor law that a head claims stays a report (4.S19), as the comment already concedes. Once `Typing` is lawful, the result type of the body can be read instead of the annotation.

**Loose functions reported (4.S17).** The report itself is consistent with D-2026-10-13-x Q3. But `looseFunction` (`nonEmptyBinders bs or …`) reports every law and every parameterized theory head. It misses a function at an alias of an exponential and at the surface form `pi`. It should be decided on the elaborated type: a `Pi` after alias expansion, at no named type with laws, and not a law or a head. Because `ReportsExactlyAs` uses "exactly", the noise is mandatory.

**"Exactly" with partial predicates is unsound.** `violatesR2Exists`, the top-level-only `violatesR12`, and `violatesR6` all under-approximate their rules. `ReportsExactly` then makes a checker that implements the full rule fail the law. Until a predicate is complete, state only its sound direction: `violates → reported`. Add the converse when the predicate is finished.

**Vacuity: yes, and in both directions.** With a generic generator of `SurfaceProgram`, names are random strings:
- **R1, R2, R3-on-data.** These are violated almost always, since names are unknown and constructors unmentioned. A checker that always reports passes.
- **R5–R9, R7, R12.** These need collisions or typable programs and are almost never violated. A checker that reports nothing passes.

Each case tests only one side of the biconditional (L9.6).

**What to do instead:**
- **Split each rule into two laws over two subtypes**, `{ c : NamedIn | violates c.p c.n }` and its complement. Each gets its own evidence and grade.
- **Use a generator of well-formed programs** that draws names from a small pool (act names, core, imports), so references resolve and terms type.
- **Mutate those programs by one rule-targeted edit**: duplicate a `:=`, retype a body to `U`, insert `==` on a function, reference an unknown name.
- **Seed with chosen cases**: the accept/reject pairs of `tests/spec/` (L9.5) and the library's own `.lth` files as accept cases.

## 4. Typing

**The laws are satisfied by a trivial model.** With `same _ _ = true` and `refines _ _ = true`, every law holds whatever `typeOf` returns. Then 4.R6 and 4.R9 never fire.

**Missing:**
- **Definitional equality.** `same` should be an equivalence that contains `a.alphaEq`, separates distinct heads (`not (same Universe (Var "Int"))`), and unfolds definitions (3.S20).
- **Refinement non-triviality.** `not (refines (Var "String") (Var "Int"))`, and a base does not refine its subtype unless the predicate is trivial.
- **Untypable terms.** `typeOf` gives `nothing` for an application of a non-function.
- **Global names.** `typeOf p ctx (Var n)` should equal `n`'s declared type when `n` is not in `ctx`. 4.R6, 4.R8 and 4.R9 all apply top-level names, `==` included.
- **Other formers.** Rules for `Match` (with pattern variables in context), `Pair`/`Sigma`, `Record`/`Proj`, `Inj`/`Sum`, constructors of `Data`, and `Subtype` formation.

**Coverage of what is stated:**
- `TypeOfApp` only covers `Lam` at `Int`.
- `TypeOfLam` and `TypeOfApp` are implications (`nothing -> true`) that random terms rarely meet. They should quantify over typed terms.

**4.R11:**
- `branchContext` is never tied to `typeOf`. No law says that the arms of the elaborated `if` are typed in it, so a typing can compute it and ignore it.
- `BranchRefines` only covers `q x` with `q` a name. `x > 0` is the common case; the law should be `Subtype x ty c` for any Bool `c` in which `x` occurs.
- The pattern half (`match m { just y -> a }` knows `m == just y`) and the obligation `q x -> p x` are unstated.

**4.R9.** `RefinesFunctions` has the variance right.

## 5. `namesIn`, D(n), B(n)

The structure is right: D(n) is binders plus declared type, B(n) is the body, and the binder names are removed. Pattern, lambda, block (`bind`), `pi`/`sigma` and clause scoping are respected. The errors:

- **Dotted names.** `"c.parse"` is never stripped to `c` (2.S14: whole qualified name first, else the longest prefix that is a variable or definition). So no binder or import ever matches it.
- **Earlier binders are not in scope in later ones.** `binderNames` does not remove earlier binders from later binder types and defaults. So `WellFormed (a : Alpha) (sb : Substitution a)` reports `a` free. 2.S7 defaults that mention earlier parameters, and implicit `{A : U} (x : A)`, have the same problem. The same holds for `paramsNames` in lambdas and for `fieldsNames` in dependent records (`{ n : Nat, v : Vec n }`, 2.S14).
- **`rebind x t` does not bind `x` in the items that follow.** A block `{ y <- 1; y <- y + 1; y }` reports `y` free.
- **`sigmaNamed x a y b` removes `y` from `b`, its own type.**
- **Constructor lists are too narrow.** `k` holds only the program's own constructors. Imported or core nullary constructors in patterns (`nil`, `universe`, `pWild`) are read as binders. This is harmless for free names but wrong for 4.R3's pattern variables.
- **`quoted`.** Whether names inside `quote` count toward dependence (4.S15) is undecided; the file counts them.

## 6. What I would change first

Fix name resolution in `namesIn` and `known`:
- strip dotted names to their prefix;
- bring earlier binders and fields into scope;
- make `rebind` bind;
- count constructors and imported names as known.

Then add, as a chosen case, the law that `term.lth`, `translation.lth` and `program.lth` themselves violate neither 4.R1 nor 4.R2.

The reason: 4.R1, 4.R2, 4.R3 and 4.S14 all run on `namesIn`. Today they reject every law in these files, including the one stating them, so no other finding can be tested until this holds. The self-check also gives `ReportsExactly` its first real non-violating programs, which is the start of the fix in item 3.

## 7. Against the specification

- **The block reading.** 2.S12 and 2.S17 say a block is "definitions with fresh names". In a dependent kernel that is a `let`, which a beta-redex is not: under `(fn x { b }) e`, `b` cannot use `x ≡ e`. So `{ n := 3; v : Vec n := ... }` types as a `let` but not as a redex. Either the kernel gets a local definition, or 2.S12 should say which encoding it means.
- **4.R3 is internally ambiguous.** "Each constructor needs a law" (reject if any constructor lacks one?) sits beside "a `data` with no constructor so bound … is reported" (report only if none has one?). The file implements "any → reject". Its §6 comment promises a report that no law states.
- **4.R9 vs obligations.** 4.R9 as written, read with 4.R11 and 4.R5, should say whether passing a base value where a subtype is expected is an error or an obligation. The file assumes error.