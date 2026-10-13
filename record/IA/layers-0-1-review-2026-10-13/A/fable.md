I'll read the uploaded files that aren't in context yet.

**1. Laws that are wrong**

- `Delta` (term.lth 309–310): `agree a (m.reduce (cons (Define f ty b) p) n (App (Var f) arg)) (m.reduce … (App b arg))` unfolds unconditionally. 3.S15 says the host unfolds "only when that makes progress", so for `b = Lam x ty (Match (Var x) …)` and a stuck `arg` the host returns `App (Var f) arg` while the law demands the stuck `Match arg …`; not alpha-equal. False of the host specimen as chapter 3 describes it, true of term_model.lut. One of them must yield (see 6).
- Ill-formed rather than false: `Substitutive … (B : U) (f : A -> B) … := f p.x == f p.y` (kernel_laws 74), `Beta … == f x` (216) and `FoldNeutral … == n.neutral` (145) compare in an unrestricted `B`/`N`; for a function-typed `B`, `==` is not structural (4.R8, 3.S37). The census must exclude it, or the law say so.
- Conditional: `structuralEquality (A : U) : Structural A := { eq := fn x y { x == y } }` fails `Reflexive` on NaN and `Substitutive` on `0.0`/`-0.0` under `fn x { 1.0 / x }` if `==` on `Float64` is IEEE; whether it is belongs to spec 11.
- No two laws are unsatisfiable together.

**2. Laws that do not determine what they claim**

- `Alpha` (term.lth 187–222): `alphaEq s t := head s == head t and sameNames (freeVars s) (freeVars t)` passes every law. It is an equivalence; `FreeVariablesAreNames` holds (`[x]` and `[y]` are the same names iff `x == y`); `RenameBound` holds because `f.y` is fresh so the free names agree; `AlphaKeepsHead`/`AlphaKeepsFree` hold by definition; every clause of `AlphaCongruent` holds because each constructor's head and free names depend only on its parts' free names. Yet it makes `Lit 1 ~ Lit 2`, `App f g ~ App g f`, `Lam x A (Var x) ~ Lam x A (Lam y A (Var x))`. Every clause of §2 is an implication *into* `alphaEq`; nothing says when two terms are *not* alpha-equal beyond `Var`/`Var`. Also `RenameBound` names only `Lam` and `Pi`; a model structural on `Sigma`, `Subtype`, `Data` and pattern variables passes.
- `Substitution`: the header says "capture-avoiding", but the capture case is never drawn. `SubstPassesBinder` (246) is stated for `f : NotFreeIn`, i.e. exactly when no renaming is needed; a naive capturing `subst` passes everything. `SubstRespectsAlpha` would catch it only when a random binder of `p.s` equals a free name of `s`, which line 228 itself calls negligible. Also `SubstGoesInside` names only `App`, `Pair`, `Inj`; a `subst` that leaves `Match` arms, `Proj`, `RecordValue`, `Pi`, `Sigma`, `Subtype`, `Data` untouched passes §3, and `Beta` in §5 cannot see it since both of its sides use `sb.subst`.
- `IotaPair` (322–324): `Match (Pair f.s (Var y)) [(PPair (PVar y) (PVar f.y), b)]` puts the cross-reference in the second component only, so left-to-right sequential substitution (what term_model.lut does, by its own comment at 206) passes while the mirror `Match (Pair (Var f.y) f.s) [(PPair (PVar y) (PVar f.y), b)]` gives `f.s` in place of the outer `Var f.y`. "The pattern's variables substituted" means simultaneously; the law should also state the mirror instance.
- `Reduction`: `agree` (293–295) returns `true` on `nothing`, so `reduce := fn p n t { nothing }` passes all eleven laws, `Final` included. So does a model that fires rules only on a root redex: no law says the head of an application, the scrutinee of a match or the record of a projection is reduced first, and `Final` accepts any stable stuck form. `Delta` states only `App (Var f) arg` with one argument: a model that leaves a bare `Var f` folded, or (as term_model.lut) computes `App (App (Var "+") i) j` ignoring a program's own `+`, passes.
- `BooleanAlgebra Bool` (100–118): the dual `{ top := false, bottom := true, meet := or, join := and, complement := not }` passes all nine laws; `Coproduct Unit Unit Bool` likewise with `left := fn u { false }`. The algebra is self-dual, so "the role of `true` is its top" (96) is not stated by any law; what tells `true` from `false` is `if`, and no law joins `booleans` to `ifThenElse`.
- `NamedProduct`/`NamedCoproduct` (241–261): `firstName`, `secondName` are tied to `first`, `second` by nothing; `recordXY` with `firstName := "y", secondName := "x"` passes. D-2026-10-13-x's claim that names are part of the structure lives only in `ProjOfRecord`.
- `ListAlgebra` (156–162): `FoldNil`/`FoldCons` reduce by `foldList`'s own `match` for every `g`; the theory has every algebra as a model.
- `Evaluation` (375–384): three cases; `evalAt` is tied to `reduce` by nothing, and the theory has no program or fuel to do so.

**3. Roles (L2.7)**

- `Primitive : String -> Term` (87): in no law of §5, not even `ValuesStay`; term_model.lut's `operatorName` computes it. The header (13–17) lists every constructor's law except this one.
- `FloatConst`, `StringConst` (48–49): `Prim` (339–343) covers `IntConst` only; `StringConst` appears only in `EvalOfConstant`/`EvalChecks`. 3.S17 promises Float64 and String.
- `PLit` (59): no `Iota` law. A `PVar` arm on its own (3.S10, "a variable … branch takes the rest"): no law; `PVar` appears only inside `PInj`, `PCon`, `PPair`.
- `Datum : Term -> Act` (103): no law; `defines` and `lookupBody` skip it. "A datum changes no reduction" would state the role it has.
- kernel_laws `FoldNil`/`FoldCons` (159–161) only restate `foldList`'s match — the automatic accessor of L2.7. `cons`'s role, "the injection of `a` combined with `xs`" (132), is prose plus the definition of `appendList` in the model file; no law says `cons a xs == combine (inject a) xs`.

**4. The models against their theories**

- kernel_models.lut breaks no law I can find (Float64 caveat in 1).
- term_model.lut breaks no stated law, which is the problem. Case against 3.S16/3.S19: `p = [Declare "z" ty]`, `reduce p 3 (Match (Var "z") [(PLit (IntConst 0), a), (PWild, b)])` gives `just b`, because `demandHead` (249–250) turns `Done` (stuck) into `Miss` and the wildcard takes it; the chapter says it does not reduce. Same root: `constructorTerms (Var x) -> just (x, args)` (262) takes a declared hole for a nullary constructor, so `Match (Var "z") [(PCon "z" [], b)]` selects `b`. Also `consistentBindings` (202–205) makes non-linear patterns equality tests, which 3.S10 does not have. And `textParts`, `textJoin`, `natDecimal` (15–17) are holes: `canonical` and the capture path of `substitute` (`freshName`) cannot run, so the form that defines the hash is an uncertified model.

**5. Reduction**

`Beta` is 3.S14 on the root redex. `Delta` drops 3.S15's progress condition and states no bare `Var f`. `Iota` states a match on an already-built scrutinee; nothing reduces the scrutinee, nothing says a match on a hole stays (3.S19), no `PLit`, `PVar`, n-ary `PCon`. `ProjOfRecord` is right for two fields, the record position unreduced. `Prim` lets an undefined `Var "+"` compute, which 3.S9 forbids (a name without body is a hole); the rule belongs to `Primitive` (3.S2, L2.3) — and in the guard at 340, `defines p "+" or … or agree … and agree … and agree …` depends on `or`/`and` precedence; parenthesize. `HolesStay` is fine, but `Var f` under `Declare f` and `Hole f` are two normal forms for one hole. `ValuesStay` omits `Pair`, `Inj`, `Primitive`. `Final` is sound. `agree` is sound — it never asserts a falsehood — but each law is vacuous on `nothing`, and no law demands a value for any fuel; the one-step laws (`ValuesStay`, `HolesStay`, `ExternIsValue`, `Prim`) should say `m.reduce p 1 t == just t`. The missing piece is the strategy: the "weak head" of WHNF is stated nowhere.

**6. Against the specification**

- `Delta` vs 3.S15 (above). My own view, apart: 3.S15's "stays folded" is a presentation of stuck terms, not a definitional equality, and it makes normal forms specimen-dependent; retire it, or state the stuck form so `Final` means one thing across specimens.
- `Prim` vs 3.S9 (undefined names compute), 3.S2 (`Primitive` is the body that means the host), 3.S17 (Int only).
- `ListAlgebra` quantifies over `onCons : A -> B -> B`, which 3.S37 says has no generator.
- kernel_laws 240, "a record of more is nested", vs the flat `RecordValue : List (String * Term)` and 3.S4's association; D-2026-10-13-o says a record is two or more names, not a nest.
- Chapter 3 is stale, not the files: 3.R1 (names are binders, not identity) vs D-2026-10-13-x; 3.S36's `KernelLaws A B`, `IfTrue`…`CaseJust` vs §6's `CaseLeft`/`CaseRight`; 3.S29's `Act` with alias and directives vs D-2026-10-13-o; `Axiom : Term` without 3.S2's string.
- D-2026-10-13-t stands, but "Bool has the laws of a Boolean algebra" cannot assign `true` its role (2); the companion law `m.top == c.left unit` between `booleans` and `ifThenElse` is what does.

**7. What I would change first**

Add to `Alpha` the inverse of `AlphaCongruent`: alpha-equal wholes have alpha-equal parts, over the subtypes `{ p : AlphaPair a | head p.s == "App" }` etc., with `Lit c ~ Lit d` iff `c == d`, equal labels for `Inj`/`Proj`/`Sum`/`Record` keys, equal types and swapped bodies under binders, and `RenameBound` for every binder. Every theory after §2 is stated up to `a.alphaEq` and the models are certified against their own `alpha`, so a coarser alpha silently weakens `Substitution`, `CanonicalForm` and every `agree` of `Reduction` — and no specimen test can show it, since the right model passes today. The capture law of §3, over its own subtype, is second.