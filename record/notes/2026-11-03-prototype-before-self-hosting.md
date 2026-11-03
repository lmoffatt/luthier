# Prototype before self-hosting — conversation note (2026-11-03)

## Why this note exists

A conversation about the trajectory of Luthier identified a likely strategic mistake in how the project has been developed and communicated.

## Diagnosis

The attraction of Luthier's self-hosting property — defining/rebuilding Luthier from Luthier's own theories — may have become a trap. Self-hosting is aesthetically powerful and potentially important, but it is not itself evidence that the central idea is useful.

Analogy with the sound-localization project: to test acoustic self-calibration, we did not build microphones, ADCs, operating systems, etc. from first principles. We bought smartphones and used them as existing components. That made it possible to test the scientific capability directly.

With Luthier, by contrast, the path has tended toward:

idea -> what should a language be? -> grammar -> parser -> semantics -> runtime -> self-hosting -> ...

This risks building the entire universe in which the idea is elegant before demonstrating the capability that makes the idea valuable.

## Separate the philosophy from the testable hypothesis

### Luthier philosophy

A computational theory should be able to exist independently of its realizations. Types are theories (structures plus laws); implementations/values are models of those theories.

### Testable Luthier hypothesis

Making the theory/realization separation explicit lets us automatically distinguish programs that appear to implement the same intended object but actually instantiate different theories.

The hypothesis can be tested without first completing the Luthier language.

## Proposed strategic inversion

Instead of:

    build Luthier -> discover what it is useful for

use:

    Luthier philosophy -> cheap experiments -> demonstrated new capability -> required architecture -> Luthier

Temporarily treat existing tools as the equivalent of the smartphones in the acoustic experiment: Python, property-based testing, SMT/Lean where useful, JSON or a minimal DSL, and LLM-generated implementations. A deliberately ugly prototype is acceptable.

## Candidate decisive experiment

Construct a minimal external prototype (even a small Python program/notebook) in which:

1. A theory is stated independently of an implementation.
2. One or more LLMs are asked to generate plausible implementations of that theory.
3. At least two implementations run and look superficially reasonable / pass ordinary tests.
4. One implementation actually violates a law of the intended theory.
5. The Luthier-style theory/model machinery detects the mismatch and produces a useful counterexample/certificate.

A scientific example would be especially valuable: "I asked an AI to implement my scientific model. The code runs and passes ordinary tests. How do I know it implemented my theory rather than a nearby one?"

If this experiment reveals a genuinely useful capability, it supplies a reason to build the language. If it does not, successful self-hosting would not by itself rescue the project.

## Communication lesson

Previous explanations of Luthier tended to lead with interests/ontology: types as theories, values as models, laws, certification, recursion, etc. That asks the listener to discover the problem that the machinery solves.

A stronger presentation should lead with the concrete failure mode, for example:

> I asked an AI to implement my scientific model. It returned code that runs and passes tests. How do I know it implemented my theory rather than a similar but different one?

Only then introduce the theory/model interpretation as the mechanism.

## Status implication

Do not discard self-hosting; demote it from near-term validation criterion. Its aesthetic and architectural value is real, but precisely because it is attractive it can absorb effort without testing the project's central claim.

For the next strategic milestone, prefer a minimal capability demonstration built from off-the-shelf components over further expansion of the self-hosted universe.
