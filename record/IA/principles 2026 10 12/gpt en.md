Yes. Draft 10 is much more coherent than the earlier versions, but I think it has reached the point where **further merging inside the existing L1–L15 structure is not enough**. The main improvement now should be hierarchical: separate *fundamental principles* from *derived design rules* and from *specification mechanisms*.

At present there are nominally 4 organizers + 15 principles, but I think the conceptual core is closer to **8 principles**.

## 1. The most important contradictions

I would fix these before further implementation work.

| Priority | Conflict | Why it matters | Suggested resolution |
|---|---|---|---|
| **1** | **Does an `assumed` certificate make something a model or not?** | The Terms define a model as an inhabitant whose law is certified, and `assumed` is one certificate grade. L2 says an assumed certificate is a hole, while L4 says an assumed axiom *does not inhabit*. Those cannot all mean the same `a : A`. principles principles principles | Separate **truth/modelhood** from **evidence**. E.g. `a ⊨ T` means semantic satisfaction; `a : T [g]` means “supported at grade g”. `assumed` permits reasoning but does not establish `a ⊨ T`. |
| **2** | **A cost-valued equality cannot simultaneously be a quotient and a tolerance ball.** | G0 says laws determine a quotient and the representative within the class is free. L5 says identity composes transitively. But L13 correctly says approximate closeness is *not transitive* and therefore uses a weighted graph. principles principles principles | Reserve **quotient/equivalence class** for exact/zero-cost equivalence. Quantitative equality should be a distance/path structure. A demand applies a radius to that structure; the radius does not create an equivalence relation. |
| **3** | **A law is being confused with a procedure for checking the law.** | L3 says a law gives a constructor returning `Maybe` and a membership function, which suggests every law is executable. L7 allows laws established by theorem, citation, sampling, cases, etc.; universal laws such as associativity over `Int` cannot generally be decided by executing the law over all inputs. principles principles | Introduce an explicit distinction: **law = semantic proposition/cost; certifier = method that produces evidence for it**. One law may have several certifiers. |
| **4** | **An extern without laws is both forbidden and allowed.** | L14 first says that without a type carrying a law the extern “is not applied”; later the same L says an extern with no law is allowed in a named world and may run there with `assumed` certificates. principles | Say instead: an uncertified extern **may execute inside an explicit world but may not inhabit/cross into a certified theory or enter the planner's substitution graph**. |
| **5** | **The proposed `Bool → Cost` “homomorphism” is underspecified.** | L6 gives Boolean `and`, `or`, `then`, quantification, but only sum/max/weighted-sum on costs, and then calls `lift` and `exact` homomorphisms. There is no single homomorphism here without specifying which quantitative operation corresponds to every logical connective—e.g. Boolean OR naturally asks for something like `min`. principles | Do not call it a homomorphism yet. Define the quantitative interpretation connective-by-connective after deciding the cost algebra. |
| **6** | **Where does tolerance belong?** | L3 makes tolerance a parameter of the certified subtype constructor, while L6 says `within ε` exists **only in the demand**. principles principles | I prefer the L6 version: laws produce costs independently of tolerance; the demand decides whether the resulting cost is acceptable. Then remove tolerance from the fundamental subtype construction. |
| **7** | **“Statements commute” is too strong at source level.** | L9 itself gives `x <- 1; y := x+10; x <- 2`, where textual order determines which `x` occurs in `y`. What actually commutes are independent nodes **after elaboration into fresh SSA-like bindings**. principles | Rename it: “After elaboration, evaluation is a dependency DAG; independent nodes commute.” |
| **8** | **“An action is verified” contradicts the body of L11.** | The body correctly admits that irreversible/concurrent external effects can only be logged and audited, never verified. principles | Title it “Actions are specified by observations before and after where observable; otherwise they are audited.” |

The first three are not cosmetic. They affect what `a : A`, equality, and law mean—the semantic centre of the language.

---

## 2. There is substantial redundancy

The repetitions are mostly caused by the same idea appearing once as a G organizer and again as one or several L principles.

| Current material | Overlap |
|---|---|
| **G0 + G1 + L1 + L2 + part of L3** | All describe the same central idea: disciplines supply invariants; laws define theories; values/models satisfy them. |
| **G2 + L5 + L6 + part of L7/L8** | Quantitative laws, equality, error and their composition. |
| **G3 + L10 + L12** | Demand determines what is produced, tolerated and optimized. |
| **L5 + L13 + L14** | Identity/equivalence certificates and transport/substitution between implementations. |
| **L7 + L14** | Citation, delegation, certification and transport of evidence. |
| **L8** | Mostly a consequence of quantitative laws + alternative realizations: ideal `Real` programs can have certified `Float64` realizations. |
| **L14** | Contains at least four things: FFI, worlds, delegated evidence and evidence transport. Most follow from more general principles. |

L10 and L14 in particular have stopped behaving like principles. Each has become a miniature specification chapter. L10 alone contains demand propagation, AD, error propagation, tests, memo identity, certificate evolution, sessions, caching, subtype propagation and observer independence. principles

That is strong material—but it should not all be inside one principle.

---

# 3. I think 15 principles can become about 8

I would make **“Luthier expresses the invariances of the disciplines” the unnumbered mission**, and make “type theory is the guide” an unnumbered design stance rather than another principle.

Then I would use approximately these eight.

### P1. Types are theories; values claim to be models

A theory consists of structure and laws. A value of the theory is a model when those laws hold.

This absorbs G1 and the semantic core of L1/L2/L3.

### P2. Truth and evidence are distinct

A law says what must hold; a certificate records why Luthier is entitled to believe it holds, including its grade, domain, hypotheses, tolerance where relevant, environment and dependencies. Evidence may weaken through composition but never strengthen itself.

This absorbs most of L2 and L7 and fixes the `assumed` problem.

This principle is, surprisingly, **missing in explicit form** even though the whole language already depends on it.

### P3. Declaration, definition and inhabitation are distinct

A hole may represent an input, pending implementation, axiom or external implementation, but these cases are distinguished during elaboration. A hole is not thereby a model.

This is the essential part of L4.

### P4. Laws and equality may be quantitative, but their algebra is explicit

Equality belongs to the type/theory. Exact equality may induce equivalence classes; quantitative identity carries cost/distance. Boolean and quantitative laws compose only according to their declared algebra.

This combines the useful core of G2, L5 and L6 without prematurely claiming one universal algebra.

### P5. Evaluation is pure dependency; effects are explicit actions

Definitions elaborate to a dependency graph. Independent nodes commute. Anything changing an external world is an action represented explicitly in the semantics.

This combines L9 and the essence of L11.

### P6. Demand selects realization, not meaning

The program determines what is true and derivable independently of its observer. A demand selects what is materialized, the requested representation/decorations, tolerance, evidence grade and optimization criteria. Every such criterion is an explicit parameter.

This combines G3 + L10 + L12.

Importantly, the existing document already contains the crucial sentence that **derivability is independent of demand and the demand merely chooses what is derived/certified/carried**. That deserves to be the headline rather than being buried near the end of L10. principles

### P7. Realizations are interchangeable only through scoped certified relations

There may be many implementations, numerical realizations and foreign implementations. The planner may substitute among them only through evidence valid for the current inputs, hypotheses and demand; it optimizes only among admissible alternatives. An uncertified foreign implementation may execute only inside an explicit world and cannot enter this substitution relation.

This absorbs L8 + L13 + most of L14.

### P8. The trusted core is minimal and reflective

The kernel is small enough to specify and execute independently; programs, plans and certificates are values that programs can inspect and manipulate. Libraries, planner and host runtime sit outside progressively weaker trust boundaries.

This is L15, cleaned up.

So:

**19 numbered conceptual statements now → 8 principles + 1 mission + 1 design stance.**

I think that is a much better size.

---

# 4. Important principles/mechanisms that are still missing

There are four gaps I would regard as more important than adding any new domain-specific principle such as units.

### A. A general calculus of evidence scope

You repeatedly specify pieces of it in L5, L7, L10, L13 and L14, but there should be one place saying exactly:

> A certificate supports **this law**, at **this grade**, for **this domain/hypotheses**, under **this environment/dependency cone**, and where applicable under **this distribution/tolerance**.

And then one meta-rule:

> **No operation on certificates may increase either their grade or their domain of validity unless new evidence is supplied.**

That single principle would eliminate a surprising amount of repeated text.

### B. Semantic truth versus certified knowledge

This is the most important missing distinction. At present `a : A` is being asked to mean simultaneously:

1. `a` really satisfies `A`;
2. Luthier has proved it;
3. Luthier sampled it;
4. the programmer assumed it.

Those are not the same judgment.

Once this is separated, `proved`, `sampled`, `assumed`, citation, delegation and transport become much cleaner.

### C. A typed/algebraic notion of Cost

The open section already acknowledges that distance, `−log p`, numerical error, sensitivity and composition remain unsettled. principles

I would go further: **do not assume yet that they are all values of one undifferentiated `Cost`.**

Distance, probability evidence, numerical error and resource consumption have different units and different composition laws. L13 already implicitly recognizes this by refusing to collapse time, memory and error into one scalar. principles

A powerful principle may turn out to be:

> Costs compose only inside a declared cost algebra; conversion between cost kinds is explicit.

That still permits a common abstraction without pretending all costs add in the same way.

### D. World/effect ownership

The open section already recognizes that the `world` needs to be an opaque unique value so actions cannot accidentally be memoized. principles

That should become a semantic rule before effects are implemented. Otherwise L9/L10's caching semantics and L11's actions can collide.

---

# 5. One more hidden inconsistency: settled material versus open material

The Terms currently say that carriers come with their setoid/field and even that every function type has carrier setoids. principles

But “What is open” says precisely this design—types coming with their equality/setoid—is still proposed and its syntax unresolved. principles

That is not primarily a theoretical contradiction; it is a **document-status contradiction**. A reader or implementation agent cannot know whether to implement it.

I would enforce a hard rule:

> **Nothing unresolved may appear declaratively in Terms as though it were part of the language.**

Put it in “Candidate semantics” until accepted.

The same applies to clauses labelled “settled” whose paragraphs contain several “proposed” mechanisms.

---

# 6. How I would improve the document itself

The biggest structural change would be to stop using `principles.md` as the place where every consequence and implementation decision is preserved.

I would organize it as:

| Section | Content |
|---|---|
| **Purpose** | One paragraph: invariances of disciplines. |
| **Semantic stance** | Type theory as guide; 5–10 lines. |
| **Core terms** | Only settled definitions. |
| **Eight principles** | Each principle: **one sentence + at most one short explanatory paragraph**. |
| **Derived rules** | Certified subtype, holes, equality levels, certificate transport, externs, memoization, sessions, etc. |
| **Open semantic questions** | Only questions whose answer changes the language. |
| **Rationale/examples** | Separate documents. |
| **History/status/provenance** | `record/`, not inside the normative reading path. |

The present “What is open” also mixes genuine open questions, finished implementation work, pending implementation, historical notes, proposed syntax and possible future principles. principles That makes it difficult to tell what blocks the language theoretically.

I would divide that material into **Open semantics**, **Open specification**, **Implementation backlog**, and **Ideas/candidates**.

---

## My main recommendation

I would **not merge L10 with another L or L14 with another L** and call Draft 11 finished.

I would change the abstraction level.

The strongest version of this document would have:

**1 mission → 8 fundamental principles → derived semantic rules → specification.**

And before anything else I would settle these three statements precisely:

> **What does `a : A` assert when its certificate is `sampled` or `assumed`?**

> **Is quantitative equality an equality relation, or is it a cost/distance from which a demand derives admissibility?**

> **Is a law the mathematical property, or the executable thing that checks the property?**

Once those three are answered, I suspect another **30–40% of the current text will collapse naturally**, because many of the long clauses are currently compensating for ambiguity in those three concepts.


does separation of G0-G3 do any good or it would be better to just list the Ls?
I think the current **G0–G3 separation does more harm than good**.

The problem is not that the four ideas are bad. They are actually the conceptual center of Luthier. The problem is that they are presented as a second set of principles **above another set of principles**, while substantially repeating them.

For example:

- **G1** says “A type is a theory and its values are its models.” That is essentially the conceptual foundation of L2 and L3. principles
- **G2** says laws extend from Boolean logic into cost. That is then developed normatively in L5, L6, L7 and L8. principles
- **G3** says the demand defines what is computed. L10 says almost exactly that, and L12 supplies its parameterization. principles principles
- **G0** already tries to connect all three of those ideas into one picture. principles

So the reader has to ask: **which level is authoritative?** Is G3 the principle and L10 its consequence? Or are both principles? If they conflict slightly, which one wins?

### I would remove G0–G3 as numbered normative items.

But I would **not throw their content away**.

Instead, put a very short unnumbered section before the Ls, something like:

> **Conceptual picture.** Luthier uses type theory to describe scientific theories and their models. Laws may express exact propositions or quantitative costs. Programs state what is known independently of how it will be realized; an external demand selects the representation, tolerance, evidence and execution plan required for a particular computation.

That does almost everything G0–G3 currently do, but tells the reader:

**this is orientation, not a second layer of laws.**

Then the actual normative document begins:

> ## Principles

and every rule that an implementation or user can rely on is an L.

---

There is one alternative that could justify retaining Gs: make them explicitly **orthogonal design axes**, not principles.

For example:

> **Three organizing ideas**
>
> 1. **Theory:** structures + laws + models.
> 2. **Evidence:** exact and quantitative certification.
> 3. **Demand:** realization selected by an external request.

Then each L could be tagged `[Theory]`, `[Evidence]`, `[Demand]`, or combinations thereof.

That might be useful internally while designing Luthier. But I would still **not number them G0–G3 or give them “settled/proposed” status**, because that makes them look like another normative hierarchy.

There is also something suspicious about G0 specifically. It currently says:

> “Type theory is the guide”

but then contains theory/models, demand, cost, normalization and search. principles

So G0 is not really one organizer. It is almost a **thesis statement for the whole language**. That is exactly what belongs in an introduction.

### Therefore my preferred architecture is:

**Purpose / thesis**  
“Luthier expresses the invariances of disciplines.”

**Conceptual picture**  
One short paragraph containing what is now G0–G3.

**Principles**  
Probably ~8–10 Ls after reduction.

**Derived semantic rules**  
Certificates, externs, planner paths, memo identity, sessions, etc.

**Open questions**

That gives you **one hierarchy rather than two**.

And I think this matters particularly for Luthier because one of its appealing properties is conceptual economy. A document saying “here are four organizers, and now here are fifteen principles which partly restate the organizers” works against that. If the language really has a small conceptual core, the principles document should make that smallness visually obvious.
