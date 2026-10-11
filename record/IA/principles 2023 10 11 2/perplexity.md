Text of `critical analysis. Focus on detecting possible con.pdf` (Perplexity, on draft 4), extracted with pdftotext -layout on 2026-10-11; the PDF is the original.

critical analysis. Focus on detecting possible
contradictions that might hamper its implementation
The draft is internally more coherent than a typical principles document because it already
records and patches several earlier contradictions. The remaining risks are not mostly logical
inconsistencies at the level of slogans; they are semantic and operational contradictions that
will appear when G3, the planner, certificates, and externality must be implemented together.
[1]


Central tension: cost, demand, and reproducibility
The deepest unresolved conflict is between G1/L19 (“the demand determines the computation”)
and L18/W10 (definitions are effect-free; results are reproducible and carry how they were
derived). [1]
L10 says the planner chooses among equivalent implementations using expected loss and cost
estimated from a database of measured runs. L19 then makes the plan part of the result’s
identity, and says the run database is not an input “once the plan is fixed.” [1]
But the plan is itself selected from that database. Therefore:
      The same program, same inputs, and same demanded type can yield different numerical
      results under different plans.
      A later run can select a different implementation because accumulated evidence changed
      the estimated costs.
      The system’s output then depends on its own execution history, even though L18 declares
      definitions effect-free. [1]
The draft’s patch—record the plan in the memo key—is necessary but insufficient for scientific
reproducibility. It makes a result reproducible relative to a plan, not reproducible as the
meaning of the program. That is a major implementation decision, not merely a bookkeeping
detail. [1]
Consequence: Luthier needs an explicit distinction between semantic result, realization under a
plan, and evidence state. Without it, “same code, same inputs” will not mean “same certified
result.”
G3 is load-bearing but undefined
The document correctly recognizes that G3 guides G0 and G2 wherever a carrier has distance,
yet G3 is explicitly the least developed organizer and its composition algebra is open. [1]
This creates a practical contradiction:
    L10 requires cost-based selection among paths.
    L15 requires an error algebra for rounding, condition numbers, and additive defects.
    L11 requires graded evidence for sampled checks.
    L21 requires identity certificates carrying a distance. [1]
But the open questions include how costs compose, how uncertainty is represented, whether
cost is      , distance, runtime, memory, or all of these, and how additive rounding defects
combine with multiplicative sensitivity. [1]
There is also a possible category error: G3 treats “truth,” approximation error, statistical
uncertainty, execution time, and memory as values in           . These are not naturally one
ordered cost. A fast but inaccurate path and a slow but accurate path cannot be ranked by a
single scalar without a loss function or preference ordering. L10’s phrase “expected loss and
cost” implicitly acknowledges two objectives, but the language principles do not say how the
planner resolves their trade-off. [1]
Consequence: G3 cannot remain a “wish” if L10, L15, and L21 are to be implemented. Either the
kernel must initially restrict G3 to decidable Boolean laws, or the project must define a
minimal, explicit cost algebra before building the planner.

Quotient versus non-transitive approximation
L10 states that implementations of a function form a quotient: one class per mathematical
function, with the representative chosen by cost. Draft 4 correctly observes that closeness on
floats is not transitive. Its repair is to define the class as the component connected by certified
equivalence links, with link distances summed and charged against the demanded tolerance. [1]
This repair introduces a new contradiction with the word “quotient.”
    A quotient by a mathematical equivalence is transitive by definition.
    A “component connected by certificates” is not necessarily an equivalence class unless the
    certified relation itself is transitive.
    Summing link distances can make a chain invalid even when every individual substitution
    was locally certified. [1]
So the planner cannot merely check each substitution against its own tolerance. It needs a
global error budget over the whole path, and the “class” is really a bounded, certified
substitution graph—not a quotient in the usual sense. [1]
Consequence: L10 should either rename the construction or specify that the admissible class is
the set of representatives reachable by certified chains whose accumulated distance remains
below the demand’s tolerance.
“Laws define the object” versus accumulating laws
G2’s original eureka says laws determine the function; L5, after revision, says laws need not
determine it and may merely accumulate. G4 explicitly favors expressiveness over restriction.
[1]

That revision is philosophically sound, but it weakens several downstream claims:
      L2 says membership in a type is a “guarantee.”
      L3 says defining a function defines its test.
      L4 says the certified subtype is the fundamental construction pattern. [1]
If laws do not characterize the function, then passing the laws is not a guarantee of correctness;
it is only evidence of consistency with the stated properties. Likewise, “definition and
verification are one act” becomes too strong: defining the tests is one act, but verification
remains partial, graded, and potentially non-diagnostic. [1]
The draft partially recognizes this through evidence grades—proved, exhaustive, cases,
sampled, assumed—but the language of “guarantee” still overstates what sampled or assumed
certificates can deliver. [1]
Consequence: The implementation should use a precise vocabulary: certificate, evidence grade,
consistency check, and guarantee under stated assumptions. Otherwise users will treat sampled
validation as proof.

Statistical verification versus falsifiability
L11 says sampled verification depends on the distribution sampled, because errors concentrate
at the edges. That is correct. But it creates a conflict with W6: “a test must fail when the thing is
wrong.” [1]
A sampled law can pass because:
      The distribution avoided the failing region.
      The sample size was too small.
      The assumed distribution was wrong.
      The implementation is wrong only for rare inputs. [1]
The certificate can record the distribution and grade, but the distribution itself is usually an
unverified assumption. If assumed evidence can enter a dependency cone and travel with a
value, then L2’s “guarantee is what the certificate says and no more” becomes especially fragile:
the guarantee may rest on an assumption that no test can falsify within Luthier. [1]
Consequence: The system needs a rule for when an assumed certificate may propagate.
Otherwise “certified” becomes a misleading label for externally trusted or statistically weak
evidence.
Demand-selected forgetting versus complete certificates
L13 says forgetting is determined by the demand: what the demanded value does not need is
forgotten. L19 says a result that reaches an output carries the certificates of its dependency
cone. [1]
These can conflict when a certificate is needed later but was forgotten earlier:
    A value may initially be demanded at a loose tolerance.
    Later, the same value may be needed as part of a stricter computation.
    The original certificate may have been discarded because the first demand did not need it.
    [1]

L4 partially addresses this: a stricter demand asks for a new check. But that means the language
does not really “forget what the demand does not need”; it must retain enough information—
code, inputs, model, seed, plan, tolerance—to recompute or revalidate. That is close to retaining
the full provenance graph. [1]
Consequence: “Forgetting” must be defined as not materializing a derived value, not as erasing the
information needed to reconstruct or certify it. Otherwise the memo and certificate system will be
unsound.

Pure definitions versus an impure world
L18 says definitions have no effects; L12 says execution is an action on the world and is verified
by observing the world before and after. Draft 4 adds that an observation is itself an action. [1]
This creates a regress and an implementation problem:
    To verify an action, one observes before and after.
    But observation changes the world.
    For irreversible actions—sending a message, deleting a file, allocating a resource—there
    may be no meaningful “before” observation to repeat.
    For concurrent or external processes, the world can change between observations for
    reasons unrelated to the action. [1]
The proposed “world as an opaque, unique value” prevents memoized actions, but it does not
solve verification of non-repeatable or concurrent effects. [1]
Consequence: Luthier should distinguish deterministic effects on owned state, which can be
checked, from irreversible or concurrent external effects, which can at most be logged, typed, and
audited—not verified in the mathematical sense.

DAG purity versus interactive sessions
L9 says a program is a DAG and statements commute. L19 introduces sessions with <- for
exploration and := to lock values; <- is rebinding and is banned only at a file’s top level. [1]
Within a session, therefore, order matters: a later <- changes what a name denotes. That is not a
commuting DAG in the strong sense; it is a stateful sequence embedded in an otherwise
dataflow language. [1]
The draft restricts the damage by confining <- to blocks and treating a saved session as a main
block. Still, the contradiction remains: the declarative story says dependencies give “the only
order there is,” while the interactive story makes textual or temporal order semantically
relevant. [1]
Consequence: The specification must state exactly which equivalences survive inside a session.
In particular, two sessions differing only in the order of independent <- bindings should be
provably equivalent; otherwise “statements commute” is false in the implemented language.

Self-hosting versus hand-executable kernel
L6 says code is data and the interpreter should be written in Luthier. L7 says the core must be
minimal and executable by hand. [1]
These are compatible only if there is a strict layer separation:
  1. A tiny trusted kernel, executable by hand.
  2. A Luthier-written metacircular interpreter, certified against the kernel.
  3. Libraries and planner machinery above that. [1]
But L10’s planner, L19’s memo, L11’s statistical checking, and L14’s orchestration all seem to
require machinery that is not plausibly hand-executable. If those components are part of the
“core,” L7 fails; if they are outside it, the specification must say precisely what the trusted
computing base is. [1]
Consequence: The project needs a formal trust boundary: what is kernel, what is certified
library, what is host runtime, and what is merely advisory planner heuristics.

Externality versus certification
L14 says external functions are validated like any other function, on first demand, with the
certificate kept by hash. L21 correctly separates identity certificates from law certificates. [1]
Still, there is a gap:
    An external library can change version, environment, hardware, or backend between runs.
    A sampled validation at one tolerance does not certify all future invocations.
    A hash of a certificate does not necessarily identify the external artifact that produced it
    unless the artifact, version, and environment are hashed too. [1]
The identity law can detect that an external function changed only if it is rerun under
comparable conditions. But if validation occurs only on first demand, later demands may reuse
a stale certificate. [1]
Consequence: External certificates need a validity scope: artifact hash, version, platform,
tolerance, seed, distribution, and possibly time or environment. Without this, L14 conflicts
with W10’s provenance requirement.

Process contradictions
The way of working contains tensions that are productive in moderation but dangerous as
implementation constraints. [1]

                   Tension                                                            Risk
  W4: real application drives growth vs.     Application pressure can force premature generalization; minimality can starve the
  W3: start minimal                          application. [1]

  W1: specification first vs. W13: rethink   Repeated foundational revision can undermine the stability that specification-first
  foundations                                development requires. [1]

  G4: expressive over restrictive vs. W3:    Expressiveness invites many valid designs; minimality demands rejecting most of
  add only what is used                      them. [1]

  W7: design stays with Luciano vs.          The human bottleneck may prevent timely evaluation of the growing decision and
  extensive AI-derived records               specification space. [1]

  W14: few rich concepts vs. the             The principles document itself violates its own communication criterion unless it is
  document’s density                         accompanied by a much shorter operational summary. [1]

W15 wisely turns principle conflicts into explicit reports, but it does not provide a priority
order among organizers. When G1’s demand, G3’s cost, and G4’s expressiveness conflict, the
document does not say which governs. [1]

Highest-priority fixes
  1. Define the trusted kernel boundary. Specify exactly which rules, judgments, and
     certificates are kernel-level and hand-checkable; everything else is library or planner
     machinery. [1]
  2. Separate semantic equality from realized equality. A program’s mathematical meaning, its
     result under a particular plan, and its accumulated evidence must be distinct objects. [1]
  3. Make the cost algebra a prerequisite, not an open appendix. At minimum, define: Boolean
     cost, distance cost, additive rounding defect, multiplicative sensitivity, and the rule for
     combining them along a certified path. [1]
  4. Replace “quotient” in L10 with a precise certified-substitution structure. State the global
     tolerance condition for chains, not only per-link checks. [1]
  5. Restrict propagation of assumed and sampled certificates. Define which downstream
     demands may consume them and what warning or downgrade they carry. [1]
  6. Specify external validity scopes. A certificate for an extern should bind artifact identity,
     version, environment, tolerance, and validation evidence. [1]
  7. Give organizers a conflict-resolution order. For example: soundness of certificates first,
     then demand, then cost, then expressiveness. Without such an order, W15 will repeatedly
     report deadlocks rather than resolve them. [1]
The most dangerous contradiction is not any single wording issue: it is that G3 is
simultaneously declared optional, load-bearing, and undefined. Until its algebra and its
relation to planning are fixed, L10, L15, L21, and parts of L19 cannot be implemented without
making implicit choices that may later contradict the stated principles. [1]
                                              ⁂


  1. principles.md
