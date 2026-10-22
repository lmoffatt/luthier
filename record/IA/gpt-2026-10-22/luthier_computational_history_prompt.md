# Instruction to Claude: make computational derivation a first-class principle of Luthier

## Purpose of this change

Revise the Luthier principles so that they explicitly capture a new design commitment:

**A value may carry the semantically relevant history of the computation that produced it, and that history must be able to survive changes of implementation and crossings between programming languages.**

This is not intended as ordinary logging, tracing, or workflow provenance. The point is stronger: the computational derivation of a value can become part of what Luthier knows about that value, can be demanded as a decoration of the value, can participate in certification and planning, and can be transported across representation and language boundaries.

This addition should strengthen, not replace, the existing architecture. In particular it should be derived from the current principles rather than introduced as an unrelated feature.

The conceptual picture is that Luthier is not primarily another host language. It is the layer that keeps the **theories, models, evidence, derivations, representations, and executions** coherent while computations may be realized in Python, Julia, C, Fortran, R, native Luthier, or other hosts. In that sense Luthier is an **orchestrator of scientific computation and theory**: host languages perform realizations; Luthier preserves and checks their scientific meaning and the evidence supporting the values they exchange.

Do not turn this metaphor into marketing language in the normative principles. Translate it into precise terms and rules.

---

## Existing principles that this must extend

Do not start from a blank page. The new idea is already latent in the present design.

### L5: demand, realization and evidence

L5 already says that:

- the demand determines the computation and the types actually produced;
- outputs may be decorated with error, derivative, certificate, etc.;
- a result is identified by code, inputs, mode, demanded type and tolerance, model, seed, plan, and certificate hashes;
- meaning, realization and evidence are separate objects;
- what is derivable is independent of the demand, while the demand chooses what is derived, certified and carried;
- what is not materialized must not erase what is needed to reconstruct or recertify a value.

The computational-history idea should be integrated here. In particular, L5.3, L5.4, L5.6, L5.10, L5.14 and L5.16 are likely to need revision or companion clauses.

### L10: certificates

L10 already makes evidence persistent, keyed to the law, domain, bound, binding and dependency cone. Do not collapse a value's derivation into a certificate. A certificate is evidence about a law or identity; a derivation is the semantically relevant account of how a particular value came to be.

The two must refer to one another where appropriate.

### L11: orchestration of other languages

L11 already states the crucial direction explicitly: **“Luthier orchestrates other languages.”** It says that:

- values may come through `extern` from Python or another host while types, laws, description and verification remain on Luthier's side;
- an extern's certificate binds the host library version and platform;
- Luthier is a coupling language, with theories at the joints between libraries and explicit bridges between representations;
- callbacks cross the bridge by declared types and calls are recorded.

The new idea should make the consequence explicit: **a language crossing must not erase the semantically relevant derivation of a value.** Representation may change; the Luthier-level account of meaning, evidence and derivation must remain transportable.

### G1 and G0

Derive the change from existing organizers if possible.

- From **G1**, a value is known as a model of a theory through the laws and evidence that characterize it. A produced value can therefore carry what is known about how that claim was obtained.
- From **G0**, a demand determines what must be inhabited and therefore which part of a derivation must actually be produced or retained.

Do not create a new organizer unless the new commitment truly cannot be derived from G0/G1/G2.

---

## New term to introduce: derivation

Introduce one canonical term. Prefer **derivation** unless the surrounding terminology makes another word demonstrably better.

Define it approximately as follows, then improve the wording to fit the style of `docs/principles.md`:

> A derivation of a value is the semantically relevant dependency history sufficient to state how that value was obtained and to reconstruct, validate, or recertify the claims about it. It is a graph of typed transformations and relevant execution facts, not necessarily a complete operational trace.

Important consequences of this definition:

1. **Derivation is not an execution trace.** Luthier should not retain every instruction, allocation or intermediate value merely because it occurred.
2. **Derivation is not a certificate.** A certificate says what evidence supports a law; a derivation says how this particular value was produced and links to the evidence relevant to that production.
3. **Derivation is not merely metadata.** It is semantically available to the language: a demand may require some facts about it, and a planner may use those facts when deciding whether a realization can satisfy a demand.
4. **Derivation is compositional.** If `y` is produced from `x`, the derivation of `y` is obtained from the relevant derivation of `x` plus the transformation, its model, bridges and evidence, modulo the projection required by the demand.
5. **Derivation can be projected.** A value need not carry its entire ancestry. The demand determines which derivable historical facts must be materialized or transported.
6. **Derivation must have a stable identity.** The exact representation is open, but hashes/references to an immutable derivation DAG are preferable to copying an arbitrarily large history into every runtime value.

The distinction between **full history** and **semantically relevant derivation** is essential. Do not specify Luthier as a tracing system.

---

## The central new invariant

Add a principle or settled/proposed clause expressing this invariant in the vocabulary of Luthier:

> **A boundary may change representation, implementation, host language or place of execution, but it does not by itself erase the derivation, theory or evidence of a value.**

A bridge must say what it preserves, changes, adds, or can no longer certify.

For example, if a value is produced in Python, converted to an Arrow/NumPy/native representation, consumed in Julia, transformed in C/LAPACK and returned to Luthier, the Luthier-level derivation should be able to record the chain without treating each host boundary as the end of semantic knowledge.

At each crossing, the derivation should be able to bind at least those facts that are relevant to the claims being made, such as:

- the Luthier theory/type before and after the bridge;
- the model/specimen selected;
- the bridge or representation conversion used;
- host/library/version/platform where those affect identity or evidence;
- assumptions and roots of trust introduced;
- error/cost contributed by the crossing;
- certificates relied on or produced;
- input derivation references needed by the output;
- the plan/run identity when relevant.

Do **not** state that every crossing must materialize every one of these fields. They are examples of derivable facts; the demand and the laws determine what must be carried.

---

## Make derivation demand-driven

The design should reuse Luthier's existing rule that the demand chooses what is produced.

Do not make every ordinary `T` value permanently contain a gigantic history object. Instead make the following conceptual distinction possible:

```text
x : T
x : T with error
x : T with certificate
x : T with derivation
x : T with some demanded projection of its derivation
```

The syntax above is illustrative only. Do not introduce syntax unless it follows from the existing type/decorated-output design.

A demand should eventually be able to express requirements such as:

- this result must have no `assumed` dependency in the relevant derivation;
- this result must descend from a calibrated input;
- this result must have crossed only bridges certified to a specified error;
- this result must carry evidence that a numerical bound is below a tolerance;
- this result must retain enough derivation to reproduce or recertify it;
- this result may discard irrelevant ancestry once a certified summary has been derived.

The important rule is:

> **What is derivable from the computation is observer-independent; what part of that derivation is materialized, certified and carried is selected by the demand.**

This should be reconciled explicitly with current L5.13-L5.16 rather than duplicated as an independent mechanism.

---

## Preserve four distinct objects

The current principles insist that meaning, realization and evidence are three objects, never one. Keep that separation and extend it carefully.

The revision should distinguish at least:

1. **Meaning / theory** - the class or object fixed by laws.
2. **Realization** - the concrete result under a plan.
3. **Evidence** - certificates supporting laws, identities and bounds.
4. **Derivation** - the semantically relevant computational ancestry of this realization, linking inputs, transformations, bridges, environments and evidence.

Do not automatically declare that these must become “four objects, never one” unless the derivation analysis supports that exact formulation. It may turn out that derivation is structurally part of realization or a relation between realization and evidence. Work that out explicitly.

However, **do not merge these responsibilities**. In particular, distinguish:

- certificate of a **model/specimen** (e.g. an implementation satisfies a theory);
- evidence about a **particular computation/result** (e.g. a residual/error bound for these inputs);
- **derivation of the value** (which model, inputs, transformations and crossings produced it, and which evidence that route relies upon).

This distinction should appear either in Terms or in the rationale accompanying the changed principles.

---

## Luthier as language orchestrator

Strengthen L11 so that “orchestrates other languages” has a precise semantic meaning.

The intended architecture is:

```text
                   LUTHIER
       theories / laws / models / demands
          evidence / derivations / plans
                    |   |   |
              typed certified bridges
                    |   |   |
             Python Julia C/Fortran ...
```

The hosts are not subordinate runtimes in a superficial sense; they may perform most of the actual computation. Luthier's responsibility is different:

- state the theories and invariants;
- know which host implementations are models/specimens of them;
- certify or record the evidence supporting those claims;
- mediate bridges between representations;
- preserve/compose the semantically relevant derivation of values across those bridges;
- answer demands by choosing or validating a realization that meets the requested theory, evidence, tolerance and resources;
- make assumptions and roots of trust explicit rather than silently losing them at foreign-function boundaries.

This is the precise version of the “conductor/orchestra” idea. The phrase may be useful in explanatory documents, but the principles should say the mechanics, not the metaphor.

A useful design test is:

> If Python computes a scientifically meaningful value, Julia consumes it, and a C library transforms it, can Luthier still answer what the final value means, how it was obtained, what was assumed, what numerical/evidential degradation occurred, and which laws justify using it?

The principles should make the intended answer **yes, to the extent demanded and certified**.

---

## Relationship to types

Do not prematurely decree that the entire derivation is literally embedded in the kernel representation of every type. The user's design intuition is that **the type of a value can carry or expose its computational history**, but the implementation mechanism remains open.

Investigate and state the weakest architecture that preserves that semantic commitment.

Possibilities include:

- derivation as a decoration/model of `T` selected by the demand;
- a dependent/refined type indexed by a derivation summary;
- a value paired with an immutable derivation reference whose propositions are reflected into the type system;
- certificates that derive a more informative type from a derivation;
- another representation consistent with G0/G1 and the current decorated-output machinery.

Do not choose among these merely for syntactic elegance. Record it as an open design question if the current specification does not force the answer.

The invariant to preserve now is semantic:

> **A computation may refine what Luthier knows of a value, and that knowledge can include facts about the value's derivation; those facts may be requested by type and transported across host-language boundaries.**

---

## Versioning / implementation scope

Treat this as an architectural commitment that must enter the principles now, but **do not require its full runtime implementation in the first working version**.

Recommended staging:

- **Now / principles:** define derivation, its separation from certificates and traces, demand-driven projection, and preservation across bridges.
- **Early implementation:** record immutable derivation identity for results using information Luthier already records (inputs, plan, model, host/version/platform, certificate hashes).
- **Next stage:** allow a demand to request a derivation decoration or selected historical properties.
- **Later:** composition and minimization of derivations, cross-language transport protocol, planner reasoning over derivation constraints.

Do not hard-code version numbers such as 0.1 or 0.2 unless the repository's current roadmap already defines what those versions mean. The conceptual dependency matters more than the label.

---

## Questions Claude must resolve while revising

Before editing normative text, answer these in the working record/rationale:

1. Is `derivation` a fourth object beside meaning, realization and evidence, or a structured part/relation of realization? Why?
2. What is the minimal information that makes two derivations distinguishable for Luthier? Which parts belong to result identity and which are merely inspectable provenance?
3. What is preserved automatically across a bridge, and what requires a certified transport law?
4. When may a detailed derivation be replaced by a certified summary without losing the ability to satisfy future demands?
5. How does a derivation refer to certificates without making certificates depend cyclically on the run they certify?
6. Which facts belong in the type/decorated value, and which remain in an external immutable store referenced by the type/value?
7. How do assumptions and roots of trust propagate across a multi-language derivation?
8. How does the new concept interact with L5.6 result identity, L5.14 retained reconstruction information, L10 certificate identity, and L11 extern/crossing records?
9. Can the same semantic derivation have several operational traces? If yes, state explicitly the equivalence/projection that makes this possible.
10. What must be in the principles now so that a later implementation cannot accidentally make language boundaries destructive of semantic history?

Where the answer is not forced, mark it proposed/open rather than inventing a settled rule.

---

## Concrete editing instructions

1. **Edit `record/principles-language.md` first**, following the repository's rule that `docs/principles.md` is projected rather than hand-edited.
2. Add `derivation` to **Terms** with a short normative definition.
3. Revise/extend **L5** so the demand may request and carry a projection of a result's derivation, and so L5.6/L5.14 are clearly connected to derivation rather than accidental bookkeeping.
4. Revise/extend **L11** so crossing a host-language/representation boundary preserves the Luthier-level derivation unless an explicit law/bridge says information is lost; add what a crossing contributes to derivation.
5. Review **L10** only as needed to establish links between derivation and certificates without conflating them.
6. Add an **open question** for the concrete representation of derivation in types/values if it is not already determined by the specification.
7. Update the appropriate rationale/concepts document so a scientist can understand the distinction among theory, model, realization, evidence and derivation.
8. Add a small worked example that crosses at least two host-language boundaries conceptually. The example should show preservation/composition of meaning and evidence, not merely serialization.
9. Project/regenerate `docs/principles.md` through the repository's existing script; do not edit the generated projection by hand.
10. Run the normal Luthier checks/tests required by the repository, but do not implement a large runtime history system merely to make the principle concrete. If implementation work is necessary, keep it to the minimal representation required to preserve current behavior and leave later machinery explicitly staged.

---

## Suggested worked example

Use a numerical/scientific chain rather than a toy string conversion. For example:

```text
raw measurements
   |  Python calibration model
   v
CalibratedData
   |  bridge Python -> Julia
   v
Julia estimator
   |  bridge Julia -> C/LAPACK
   v
Linear solve
   |  bridge back
   v
Estimate
```

At the final `Estimate`, Luthier should in principle be able to answer, if demanded:

- which theory the estimate inhabits;
- which calibrated inputs it depends on;
- which models/specimens and bridges were used;
- which host/library versions materially affect its identity;
- which certificates justify each relevant model/bridge;
- which assumptions or roots of trust remain;
- what numerical/error costs were composed;
- whether a requested evidence/tolerance condition is met.

A second implementation of one step should be substitutable only through the already-existing certified-identity/planner rules. The derivation changes as a realization even when the theory-level meaning is preserved.

---

## Non-goals / guardrails

Do not:

- turn Luthier into a general-purpose event logger;
- retain every operational step by default;
- equate provenance with proof;
- make a foreign-language boundary automatically trusted;
- duplicate the same history inside every value when an immutable shared DAG/reference is sufficient;
- invent syntax before the semantic role is settled;
- collapse model certification, run evidence and value derivation into one `certificate` object;
- require full planner/cost-algebra implementation before the principle can be stated;
- add a new top-level organizer or principle solely because the idea sounds important if it is already a consequence of G0/G1 and can be expressed coherently inside L5/L11.

---

## Acceptance criteria for the revision

The revision is successful if, after reading the principles, the following statements are unambiguously true:

1. Luthier can know more about a value than its material representation and extensional value; it can know relevant facts about how the value was obtained.
2. That knowledge is described as a derivation (or a deliberately chosen equivalent term), not confused with a full execution trace.
3. A demand determines which derivation facts are actually materialized/carried.
4. Certificates remain evidence about laws; derivations reference/compose such evidence for particular results.
5. Crossing Python/Julia/C/etc. boundaries does not automatically discard the value's Luthier-level theory, evidence or derivation.
6. Representation bridges explicitly account for preservation, added error/cost, assumptions and any information they cannot preserve.
7. Luthier's role as “orchestrator of other languages” now includes preserving theoretical and evidential integrity of values across heterogeneous computations.
8. The architecture permits future types/decorated values to expose computational-history constraints without requiring the full mechanism to be implemented immediately.
9. Existing principles about demand, result identity, certificates, planners and externs remain consistent rather than being duplicated by a second provenance subsystem.

The deepest test is this:

> **A value should be able to cross languages without becoming scientifically anonymous.**

That should become a design invariant of Luthier.
