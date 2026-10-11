The document is much more coherent than the earlier versions, but I would **not yet implement the full semantics from it**. The main remaining problems are not missing features; they are places where two principles currently imply different operational meanings.

The most serious issue is that several concepts are doing double duty: **type membership vs empirical certification, law satisfaction vs function identity, and dataflow vs effects**. Those need to be separated before they become implementation rules.

### 1. `a : A` is simultaneously a proof and an uncertain empirical claim — **blocking**

L2 says membership is a **guarantee**: if a value belongs to a type, it satisfies the propositions/laws of that type. principles This follows G0's conventional proposition/proof interpretation. principles

But G3 explicitly turns truth into a value in `[0,∞)` and says the value of a law may itself be uncertain. principles Moreover, the text explicitly says that "`a : A` [becomes] a judgment with a grade" because an implementation may merely have been "validated aunque sea una vez." principles L11 then allows `sampled`, `assumed`, etc. certificates. principles

Those are two different judgments:

\[
a : A
\]

meaning *a really is an inhabitant of A*, versus something like

\[
a \models_{c,e} A
\]

meaning *we currently have evidence of grade \(e\), cost/error \(c\), that a behaves as required by A*.

If they are identified, type checking becomes probabilistic: running more tests could literally change whether an expression has a type. Worse, the same unchanged program could cease or begin to typecheck as the database accumulates evidence.

I think Luthier needs **two layers**:

- semantic inhabitation: `a : A`;
- certification/evidence: `cert(a, A) : Evidence`.

The second can be progressive, Bayesian, sampled, stale, invalidated, etc. The first should not silently change after another execution.

This one decision would remove a large fraction of the current contradictions.

---

### 2. The certified subtype construction is still Boolean, while G3 abolishes Boolean laws — **blocking**

L4 says the fundamental construction is a material type plus a **predicate**, yielding a certified subtype, a constructor returning `Maybe`, and a membership function. principles L12 likewise describes a predicate as the two-class case. principles

But G3 says a law returns a cost in `[0,∞)`, with the **demand** supplying the tolerance. principles

So what is the constructor for:

```text
PositiveFloat
```

if its law produces `0.0000037`?

It cannot return `Maybe PositiveFloat` until somebody supplies a threshold. Therefore either:

```text
certify : (x : T, ε : Cost) -> Maybe A
```

or the subtype itself must contain the criterion:

```text
Approx A ε
```

or certification must return evidence without deciding membership:

```text
check : T -> Evidence A
```

At present the document implicitly uses **all three interpretations**.

This is particularly important because L17 says criteria are parameters, while G0/L2 suggest type membership itself is intrinsic. principles

---

### 3. “Satisfies the same laws” cannot define “is the same function” if laws may be incomplete — **blocking**

This is perhaps the cleanest internal contradiction.

L5 explicitly says that laws **need not determine the operation**; characterization is merely the limit that a collection of laws may eventually reach. principles

But L10 says implementations are quotiented by

> “compute the same function up to the law's equality”

and that there is “one class per mathematical function”; the class is chosen by law. principles

If laws are incomplete, two genuinely different functions can satisfy every currently known law.

For example, suppose the only law for `f : Real -> Real` is

\[
f(0)=0.
\]

`f(x)=x`, `f(x)=x²`, and millions of other functions satisfy it. They cannot all be representatives of the same mathematical function.

L21 actually moves in the right direction by distinguishing **identity certification** from **law certification**. principles But L10 has not yet absorbed that distinction.

You need at least three relations:

\[
\text{implementation identity}
\]

\[
\text{extensional/function equality}
\]

\[
\text{satisfies the same specification}
\]

They are not interchangeable.

This affects the optimizer critically: it may choose freely only among alternatives known equivalent, **not merely alternatives satisfying the same incomplete laws**.

---

### 4. “Statements commute” contradicts world-changing actions — **blocking once effects are implemented**

L9 says the program is a DAG, dependencies determine all ordering, and statements commute. principles L18 makes this plausible for definitions because definitions have no effects. principles

But L12 says actions such as execution **change the state of the world**. principles

Consider two independent-looking nodes:

```text
print("A")
print("B")
```

They do not commute observationally.

Likewise:

```text
save(file, x)
save(file, y)
```

Their ordering clearly matters.

The clean solution is already suggested by Luthier's own philosophy: **make the world/dependency explicit**.

Conceptually:

```text
print : World × String -> World
save  : World × Path × Data -> World
```

Then:

```text
w1 := print(w0, "A")
w2 := print(w1, "B")
```

and the ordering becomes an ordinary DAG dependency.

Then L9 can safely become:

> Pure definitions commute when their dependency graph permits it; actions are ordered through explicit world-state dependencies.

Without something equivalent to this, the scheduler cannot implement L9 and L12 simultaneously.

---

### 5. Memoization has the same problem with actions

L19 says nodes execute once and that results are memoized by the hash of code, inputs, and mode. principles

That cannot apply naively to:

```text
print
save
network request
read sensor
current time
```

because on the second demand the planner could say “already computed” and suppress the action.

This compounds the previous issue. Either:

- only pure definitions are memoizable;
- actions consume a changing `World`;
- or the world state is part of their input identity.

I would make the first distinction fundamental and derive the other two from it.

---

### 6. A “hole” currently means several semantically incompatible things

L8 says the same bodyless declaration is simultaneously:

> axiom, program input, external function, pending definition and dead code. principles

But those have profoundly different semantics.

An **axiom** may legitimately participate in proofs without an implementation.

A **program input** gets a value at execution.

An **extern** receives an implementation from elsewhere.

A **pending definition** is an implementation error if demanded.

**Dead code** may safely remain unresolved forever.

The statement “nothing executes until it is defined” is perfectly reasonable for a pending implementation, but not obviously for an axiom or input.

They may share syntax internally, but they cannot share the same demand-resolution rule. At minimum the elaborated IR needs different hole capabilities/kinds.

Something like:

```text
Hole Assumed
Hole Input
Hole External
Hole Pending
```

would preserve the conceptual unity without forcing the runtime to guess what a hole means.

---

### 7. Demand-driven forgetting risks a circular type/planning dependency

L13 says the **demanded return type** determines which law is derived and what is forgotten. principles

L19 then says the planner walks backward from the demand and can produce, among other things, “the type of its result.” principles

That can become circular:

\[
\text{requested type}
\rightarrow
\text{which laws compose}
\rightarrow
\text{result type}
\rightarrow
\text{requested type}.
\]

This is not inherently fatal—many type systems solve constraints—but the implementation must know which of these is authoritative.

For example:

```text
x : Positive
y := double(x)
```

If nobody asks for `y : Positive`, does `y` have type `Real`, `Positive`, both, or some latent refinement waiting to be demanded?

The present wording sometimes suggests **the fact exists but is forgotten**, and elsewhere suggests **the fact is derived only when demanded**. Those yield different typecheckers and different cache keys.

I would choose:

> Derivable propositions are properties of the expression independent of demand; demand controls which of them are materialized/certified/carried.

That preserves G1 without making semantics depend on the observer.

---

### 8. `:=` appears to mix binding equality with approximate observational equality

L16 says after `:=` the name equals the RHS using structural equality when available and observational equality/distance otherwise. principles

This is dangerous.

For a pure language,

```text
x := e
```

should normally mean **x denotes e**. That is a syntactic/semantic binding rule. It should not depend on whether `e` is a float, what tolerance is requested, or what observational metric exists.

Approximation belongs later:

```text
realization(e) ≈ e
```

not:

```text
x ≈ e
```

If `:=` itself only establishes approximate equality, substitution and reduction become tolerance-dependent, and L7's hand-executable kernel becomes considerably harder to define.

I would keep binding exact and move G3 entirely to **realizations/certificates**.

---

### 9. There is a literal unresolved contradiction over modules

The terminology section says:

> “a module is a file as a namespace, until modules are values” principles

but L20 states:

> “Modules are values: a parametrized module is a function from models to definitions...” principles

For implementation this matters immediately: is module elaboration part of the parser/name resolver, or is a module an ordinary runtime/core-language value?

I suspect L20 represents the newer intended design. If so, the terminology at the beginning should simply be changed. This one is easy to fix, but shouldn't remain ambiguous in a spec.

---

### 10. G3 currently uses one `Cost` for quantities with incompatible algebra — **major blocker for optimizer/certifier**

The open issues explicitly say that the law value might be:

- a distance,
- `−log p`,
- a sampled cost,
- something propagated by Lipschitz constants,
- and something additive under independence. principles

These quantities do **not** in general compose the same way.

A numerical error:

\[
|x-\hat x|
\]

a negative log probability:

\[
-\log p
\]

and epistemic uncertainty about either one are three different objects.

Yet G3 currently uses that common value to support inhabitation, optimization, equivalence and Bayesian accumulation. principles

I would resist forcing these into one scalar merely because they all look like `[0,\infty)`.

A more robust abstraction would be something like:

\[
\text{LawResult} = (\text{residual},\ \text{evidence},\ \text{provenance})
\]

where the residual has a law-specific composition algebra and the evidence says how well that residual is known.

This seems particularly compatible with the idea you developed earlier that **the observable object is the law residue**, while Bayesian inference concerns our knowledge of that residue.

---

### 11. “What can be computed is checked exactly” is not implementable as stated

L11 says:

> “What can be computed is checked exactly; what can only be sampled is checked statistically.” principles

Computability is not the right dividing line.

For example, both multiplication and the predicate

\[
(xy)z=x(yz)
\]

are computable for arbitrary integers. But checking associativity for **all integers** by execution is impossible.

The implementable distinction is closer to:

- proved symbolically;
- exhaustive over a finite enumerable domain;
- checked on specified cases;
- sampled from a distribution;
- assumed/cited.

Interestingly, the document already has almost exactly that certificate taxonomy. So I would delete the “can be computed / can only be sampled” criterion and make the **verification method explicit**.

---

### 12. L12's kernel interpretation is mathematically suggestive but should not become operational semantics

L12 says every `f` induces

\[
a \sim b \iff f(a)=f(b)
\]

and then says computing `f(x)` is placing `x` into its equivalence class and the result is “the class's name.” principles

The first statement is fine: this is the kernel equivalence of `f`.

But in general:

\[
X/{\sim_f} \cong \operatorname{im}(f),
\]

not necessarily the entire codomain, and `f(x)` is not literally the equivalence class `[x]`; there is an induced injection from the quotient into the image.

As an explanatory intuition this is good. As an evaluator definition it introduces unnecessary machinery and can change representation.

I would state it as a theorem/interpretation of functions, not as how execution computes them.

---

## What I think is the underlying structural problem

The document is currently trying to make one concept serve three levels:

\[
\boxed{\text{mathematical semantics}}
\quad
\boxed{\text{evidence about an implementation}}
\quad
\boxed{\text{choice of an execution}}
\]

G0 mostly describes the first.

G2 straddles the first and second.

G3 straddles the second and third.

G1 governs the third.

A number of contradictions disappear if those interfaces become explicit.

For example:

\[
\text{Theory/Law}
\rightarrow
\text{Model}
\rightarrow
\text{Certificate}
\rightarrow
\text{Realization/Plan}
\rightarrow
\text{Action}
\]

Then:

**laws** say what is required;

**models** claim to instantiate those laws;

**certificates** say why/how strongly we believe that claim;

**plans** choose among sufficiently certified realizations according to cost/tolerance;

**actions** interact with the world.

That would preserve essentially all of G0–G4 while preventing Bayesian evidence from leaking into the meaning of `:` and runtime scheduling from leaking into mathematical equality.

### My priority before further implementation

I would settle **four things before extending the interpreter**:

1. whether `a : A` is semantic truth or certified empirical belief;
2. the difference between satisfying a specification and being extensionally the same function;
3. explicit semantics for effects/world dependencies in the DAG;
4. the type of a law result: distance/residual versus evidence/probability.

Everything else I identified can largely be deferred or repaired locally. Those four cannot: they determine the IR, the typechecker, the certificate format, the planner and the cache architecture simultaneously.

This is actually very consistent with W1: the document itself says implementation should expose a case where two rules cannot both hold, at which point the specification changes through a recorded decision rather than silently. principles These four look to me like exactly those cases.