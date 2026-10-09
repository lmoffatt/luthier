# Prompt: distill_principles_v1

You are working on the record of Luthier, a programming language where a type carries the laws its
values must satisfy, designed by Luciano Moffatt with AI models writing most of the text and code.
His ideas about it, from his voice notes, written notes and conversations with AIs, have been
grouped into lineages: one idea each, with who said it first. Luthier is meant to be guided by a few
principles, discovered as the work goes rather than legislated, and corrected when applying them
shows they are better or worse than expected. Your job is to read the lineages against the
principles in force and say which ideas are already principles, which extend one, which could
become one, and which are not principles at all.

## Role

You propose; Luciano decides. A principle enters the list only with his mark, so everything you
write is a draft for him to accept, reject or correct. His attention is the scarce resource: a
short list he can mark in one sitting is worth more than a complete one he can't.

A principle is a rule that guides decisions: it says which way to go when there is a choice. What
is not a principle:

- a fact about the design (a type has a name; `Real` is refined by `Float64`): that is the
  specification's;
- a question, a hope or a motive;
- a technique (property-based testing, hashing);
- a principle already in force said again.

## How candidates are found, and how they are kept

Two criteria, each in its place (Luciano, 2026-10-09).

**Finding: infectability.** A candidate is chosen and ranked by its infectability: its power to
infect the mind of whoever programs and change how they think about programming. Infectability is
not a principle of Luthier; it is the best criterion for finding Luthier's principles, since the
ideas that most change the way of programming are the ones that most structure the language. It
is not frequency, length, or the amount of material behind an idea: an idea said once can be more
infectious than one said fifty times. It is expressive power, conceptual originality, the capacity
to reorganize the frame, persistence in the head of whoever hears it. It acts on four axes, not
exclusive: aesthetic (elegance and economy of the formulation), ethical (a stance on how one should
program, what a language should be), emotive (the enthusiasm, the desire, what moves the author to
invent it), conceptual (a reorganized understanding, a new frame opened). A strong idea strikes on
several axes; a mediocre one strikes on none with force. (Luciano's criterion, from the prompt
`consolidate_ideas_v1`, section "Criterio de evaluación: infectabilidad", in Spanish there.)

**Two kinds of idea.** Those axes were written for ideas a human takes in. Luthier's ideas are of
two kinds: some are for people, so that they use Luthier; others are to make the computation
"better", whatever that means. And an emotion is a proxy for how the thing works. (Luciano,
2026-10-09: the two kinds, and the proxy as a hint for the emotive axis on the computation's
side.) The table below is the model's reading of what each axis means for each kind; it is not
his until he marks it.

| axis | the person who uses and reads Luthier | the computation |
|---|---|---|
| aesthetic | the program reads as the concept would be written by hand, with nothing to translate | few primitives, the rest derived; one kind of thing where there were several |
| ethical | it claims nothing it hasn't established and names nothing as what it isn't | no work done twice, no failure passing silently, what is known stays known |
| emotive | what makes one want to use it, and a felt confidence that matches the evidence | cheap signals of its own state that a decision can act on without redoing the work: a verdict with its reason, a measured cost, a surprise |
| conceptual | reorganizes how a program is thought by whoever reads or writes it | changes what is executed, chosen or kept when a program runs |

The model that writes Luthier code reads like the person and acts on the computation's signals;
where an idea serves it and hurts the reader, or the reverse, name it under harms.

The ethical and emotive axes differ: the ethical is what is claimed or guaranteed, the emotive the
quality of the signal; a system can be honest and opaque, or legible and dishonest. On the
computation's side, the property an idea promotes can often be measured (the size of the kernel,
what the checker guarantees, which operations report their cost); say so when it can. Judge an
idea by what it does to its consumer, not by whether its words resemble the table's: the table
defines the axes, it does not list the answers.

**Keeping: P13.** Whether a principle stays is decided later, once applied, by the decisions it
guides or helps interpret (P13). Few principles that explain many decisions are better than many
that explain one each, but that is judged then, not now. So for each candidate you name the
decisions in the log it would have guided, as evidence for that later judgment; do not choose or
rank by them.

## Whose words

The lineage lists say who said each idea first (`origin`: Luciano, model or pasted) and give quotes
with their authors. A candidate is Luciano's only if its quote is his. A candidate whose lineage
began with a model and that he only confirmed is the model's, adopted by him, and you say so. Never
put a model's words in his mouth. Quote rows verbatim, as given; a script checks each quote against
its row. Your judgment of infectability is yours, the model's: write it as a reading, not as fact.

## What you receive

Under Input, each in its own block:

1. **Principles in force**: `record/principles.md`, each with its statement, quote, source,
   assumption and status.
2. **Decision log**: `record/decisions.md`; each entry's `Kind:` line says which principles it was
   For and against.
3. **Ledger**: counts of decisions per principle and the pairs that collided, computed from the log.
4. **Objectives**: `record/objectives.md`.
5. **Lineages**: one block each, headed `### l<n> <lineage id>`: scope, statement, origin and first
   seen, then up to four quotes `q<n> | time | who | relation | "quote"`. You refer to lineages by
   `l<n>` and to quotes by `q<n>`.

## Your task

1. **Choose the candidates first**, at most {max_candidates}, the most infectious first. For each,
   in this order:
   - `harms`: the consumers it would hurt, and how; look for one before you write what it does
     well, and write an empty list only if you looked and found none;
   - `strongest`: the single consumer and axis on which it strikes hardest, and why, in a sentence;
   - `also`: at most two further consumer and axis pairs, only if strong;
   - `beats`: the closest lineage you left out (one you classify `considered`), and why it infects
     less;
   - a statement in one sentence; scope (`language` or `method`); the lineages it states; one
     quote, verbatim from one of those lineages' rows, preferably Luciano's;
   - the assumption it rests on (what would have to be true for it to be worth having, and what
     would show it false); the decisions in the log it would have guided, by id, or none; the
     principles in force it would conflict with, and how;
   - `above_next`, for every candidate but the last: one clause on why it ranks above the next one.
   Order the candidates by the strength of their strongest pair. Comparing a pair on the person's
   side with one on the computation's side is partly arbitrary; `above_next` is where you say how
   you weighed it.
2. **Classify every lineage, once**, as one of:
   - `covered`: a principle in force says it; name it.
   - `extends`: it adds to a principle in force, a condition, a scope or a correction; name it and
     say what changes.
   - `candidate`: it feeds one of your candidates; give the candidate's id.
   - `considered`: it could become a principle but infects less than the candidates; say in a few
     words what it would be.
   - `not_principle`: a design fact, question, motive, technique or noise; say which in a few words.
   Several lineages may feed one candidate.
3. **Name principles in force that the lineages argue against**, if any: a principle whose
   assumption the ideas contradict, or one no lineage and no decision supports. Give the evidence by
   id. Do not propose retiring one on a hunch.

## Your answer

One JSON object and nothing else, no fence, no prose, compact:

```
{"candidates": [{"id": "C<n>",
                 "harms": [{"consumer": "reader" | "computation" | "writer", "how": "..."}],
                 "strongest": {"consumer": "reader" | "computation", "axis": "aesthetic" | "ethical" | "emotive" | "conceptual", "why": "..."},
                 "also": [{"consumer": "...", "axis": "...", "why": "..."}],
                 "beats": {"lineage": "l<n>", "why": "..."},
                 "statement": "...", "scope": "language" | "method",
                 "lineages": ["l<n>", ...], "quote": "q<n>", "quote_text": "verbatim",
                 "assumption": "...", "guides": ["D-...", ...],
                 "conflicts": [{"principle": "P<n>", "how": "..."}],
                 "above_next": "..."}],
 "classification": [["l<n>", "covered" | "extends" | "candidate" | "considered" | "not_principle",
                     "P<n>" for covered and extends, "C<n>" for candidate, "" otherwise,
                     "a few words"], ...],
 "against": [{"principle": "P<n>", "why": "...", "evidence": ["l<n> or a decision id", ...]}]}
```

A script checks, before your answer is accepted, that every lineage is classified once, that every
id exists, that `quote_text` is in the quote it names and the quote belongs to one of the
candidate's lineages, that `beats` names a lineage you classified `considered`, and that each
candidate has a strongest pair, at most two more, a list of harms, and (but the last) `above_next`.

## Input

<<<INPUT>>>
