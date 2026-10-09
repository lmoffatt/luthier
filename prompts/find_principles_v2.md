# Prompt: find_principles_v2

You are reading the ideas of {designers} about a programming language, {language}. The ideas were
extracted from what they wrote and said and grouped into lineages: one idea each, with who said it
first and a few quotes. A language is meant to be guided by a few principles, discovered as the
work goes rather than legislated. Your job is to find, among these ideas, the ones that could be
its guiding principles.

You see only the lineages. You are not told what principles the language already has, and you
should not bring any from what you may know about it: judge only what the lineages say.

## What a principle is

A rule that guides decisions: it says which way to go when there is a choice, and so it names, at
least implicitly, the road not taken. "Prefer X to Y", "do X, not Y", "X even at the cost of Y".
A principle guides many decisions, not one: if a statement settles a single feature, it is a
decision, and the principle, if any, is the rule that decision followed. What is not a principle:

- a fact about the design or a single decision (blocks are marked by indentation; arrays start at
  zero; numbers have arbitrary size). When such a decision follows a rule the texts state or show,
  the rule is the candidate, not the decision ("notation follows the reader's common use, not the
  tradition of other languages");
- a question, a hope, a story or a motive;
- a technique (garbage collection, hashing, a parsing method);
- the same principle said again in other words (that is one lineage feeding another's candidate).

## The criterion: infectability

A candidate is chosen and ranked by its infectability: its power to infect the mind of whoever
programs and change how they think about programming. Infectability is not a principle of the
language; it is the best criterion for finding its principles, since the ideas that most change
the way of programming are the ones that most structure the language. It is not frequency, length,
or the amount of material behind an idea: an idea said once can be more infectious than one said
fifty times. It is expressive power, conceptual originality, the capacity to reorganize the frame,
persistence in the head of whoever hears it. It acts on four axes, not exclusive:

- aesthetic: elegance of the formulation, economy, beauty of the construction;
- ethical: a stance on how one should program, what a language should be;
- emotive: enthusiasm, desire, contact with what moves the author to invent it;
- conceptual: a reorganized structure of understanding, a new frame opened.

A strong idea strikes on several axes; a mediocre one strikes on none with force. A brief
formulation can be more infectious than a long text.

(This criterion is Luciano Moffatt's, written for another language; it is used here unchanged. Its
original, in Spanish: "Una idea se evalúa por su infectabilidad — su capacidad de infectar el
cerebro de quien programa y transformar su forma de pensar la programación. [...] No son criterios
de infectabilidad: frecuencia, longitud, cantidad de material asociado. Son criterios: potencia
expresiva, originalidad conceptual, capacidad de reorganizar el marco, persistencia en la cabeza
de quien la escucha. Cuatro ejes de fuerza (no exclusivos): Estética — elegancia de la
formulación, economía, belleza de la construcción. Ética — postura sobre cómo se debe programar /
qué debe ser un lenguaje. Emotiva — entusiasmo, deseo, contacto con lo que mueve al autor a
inventarlo. Conceptual — reorganización de la estructura de entendimiento, apertura de un marco
nuevo. Una idea fuerte pega en varios ejes; una mediocre no pega en ninguno con fuerza.")

## Whose words

Each lineage says who said its idea first (`origin`) and gives quotes with their authors. A
candidate is its designers' only if its quote is theirs. Quote rows verbatim, as given; a script
checks each quote against its row. Your judgment of infectability is yours: write it as a reading,
not as fact.

## What you receive

Under Input, the lineages, one block each, headed `### l<n> <lineage id>`: scope, statement,
origin and first seen, then up to four quotes `q<n> | time | who | relation | "quote"`. You refer
to lineages by `l<n>` and to quotes by `q<n>`.

## Your task

1. **Choose the candidates first**, at most {max_candidates}, the most infectious first. For each,
   in this order:
   - `harms`: what the idea would cost or whom it would hurt if it guided the language, in a few
     words each; look for one before you write what it does well, and write an empty list only if
     you looked and found none;
   - `strongest`: the single axis on which it strikes hardest, and why, in a sentence;
   - `also`: at most two further axes, only if strong, each with why;
   - `beats`: the closest lineage you left out (one you classify `considered`), and why it
     infects less;
   - a statement of the principle in one sentence, as a rule; `instead_of`: the alternative it
     rejects, the road not taken, in a few words; scope (`language`, `method` or `other`); the
     lineages it states; one quote, verbatim from one of those lineages' rows, preferably the
     designers';
   - `above_next`, for every candidate but the last: one clause on why it ranks above the next.
2. **Classify every lineage, once**: `candidate` (it feeds one of your candidates; give its id),
   `considered` (it could be a principle but infects less; say in a few words what it would be),
   or `not_principle` (a design fact, question, story, motive, technique or noise; say which).

## Your answer

One JSON object and nothing else, no fence, no prose, compact:

```
{"candidates": [{"id": "C<n>",
                 "harms": ["...", ...],
                 "strongest": {"axis": "aesthetic" | "ethical" | "emotive" | "conceptual", "why": "..."},
                 "also": [{"axis": "...", "why": "..."}],
                 "beats": {"lineage": "l<n>", "why": "..."},
                 "statement": "...", "instead_of": "...", "scope": "language" | "method" | "other",
                 "lineages": ["l<n>", ...], "quote": "q<n>", "quote_text": "verbatim",
                 "above_next": "..."}],
 "classification": [["l<n>", "candidate" | "considered" | "not_principle", "C<n>" for candidate or "",
                     "a few words"], ...]}
```

A script checks, before your answer is accepted, that every lineage is classified once, that every
id exists, that `quote_text` is in the quote it names and the quote belongs to one of the
candidate's lineages, that `beats` names a lineage you classified `considered`, and that each
candidate has a strongest axis, at most two more, a list of harms, the alternative it rejects, and
(but the last) `above_next`.

## Input

<<<INPUT>>>
