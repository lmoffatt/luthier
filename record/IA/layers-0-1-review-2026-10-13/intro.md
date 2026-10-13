# Review of layers 0 and 1 of Luthier: three prompts for external models

Written 2026-10-13 by Claude Opus 5.5 for Luciano, who sends each prompt, with its bundle, to the
same four models (GPT, DeepSeek, Claude, Kimi); the replies go to `A/`, `B/`, `C/`, one file per
model (`<model>.md`), unedited (P3). Agreed with the coordinating session (plan from zero, Z9: one
external round per layer). Three small prompts rather than one large, since web models answer
small bites better (his lesson of 2026-10-13). The bundles are frozen by `freeze.py` once every
file parses.

The common opening, at the head of each prompt:

> You are reviewing theory files written in Luthier, a language whose interpreter is being rebuilt
> from its own theories: a type is a theory (a structure with laws), a value of it is a model, and
> the language certifies models against their theories by testing. A theory file (`.lth`) declares
> a record type of operations, states its laws as Bool-valued definitions over a model (`(m : T)`),
> and defines the theory as their conjunction (`T := Law1 & Law2`); a model file (`.lut`) holds
> values of theories. Every constructor of a `data` must have a law stating its role (principle
> L2.7: a definition is a concept; distinct constructors and accessors state no role). A law
> quantifies over the subtype it means rather than over an implication whose premise random cases
> rarely meet. The files parse with the project's parser; nothing yet type-checks or certifies
> them, so you are the first check of their meaning. Grammar files were reviewed in earlier rounds
> and are not in scope. Do not reopen a decision listed in `decisions-cited.md` unless a file
> contradicts it; where you disagree with the specification itself, say so as a separate item.
