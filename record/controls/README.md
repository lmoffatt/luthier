# Controls of the filter that finds principles

Draft 0, 2026-10-09. Written for Luciano and for the sessions that run or read the controls.

Why. The prompt that finds Luthier's candidate principles must not carry Luthier's ideas, or it
finds what it brings. Luciano asked for a control (2026-10-09, "hacé el control sobre python y
haskell"): run the same pipeline on the design writings of two other languages, with the passages
where their designers state their principles taken out, and see whether the filter finds those
principles, and whether ideas of Luthier slip into what it finds.

This file is written, and the two references committed, before any model reads the corpora.

## Corpora and references

| | corpus (what the filter reads) | reference (what it should find, never shown to it) |
|---|---|---|
| Python | Guido van Rossum, *The History of Python* (blog, 2009 to 2018), the 27 posts by him except "Python's Design Philosophy", "import this and The Zen of Python" and a notice of a translation | his "Python's Design Philosophy" (2009-01-13): 14 guidelines, a rule on punctuation, the Zen of Python as he quotes it, and four departures from ABC; `python/reference.md` |
| Haskell | Hudak, Hughes, Peyton Jones, Wadler, "A History of Haskell: Being Lazy With Class", HOPL III, 2007, doi:10.1145/1238844.1238856, sections 1, 2, 4 to 13, without the six goals of 2.3 | section 3, "Goals, principles, and processes" (3.1 to 3.7), and the six goals of 2.3; `haskell/reference.md` |

The sources are kept outside git (`*/sources/`, as in D-2026-10-09-a), pinned here by sha256:

| file | sha256 |
|---|---|
| `python/sources/feed.xml`, the blog's Atom feed, downloaded 2026-10-09 from `https://python-history.blogspot.com/feeds/posts/default?max-results=100` | 9a98249cfc9dcb4c3350f8f32ee902370e63290afb181f5bfed28fcbbe253edb |
| `haskell/sources/history.pdf`, downloaded 2026-10-09 from `https://www.microsoft.com/en-us/research/wp-content/uploads/2016/07/history.pdf` | 9fbda75d895eba8d2f9d56cf4db36dffe193919c716265a18003b43d13bc08ca |
| `haskell/sources/history_flow.txt`, `pdftotext history.pdf history_flow.txt` (pdftotext 26.07.0) | 37bb44345c9b8bd8ba9c9979b8b9bdd862a89fb3a52053fdaae3de9733759845 |

`scripts/prepare_control_corpus.py python|haskell` writes the corpus notes into `*/texts/`
(outside git); it prints the sha256 of each note.

## Protocol

Each corpus goes through the pipeline Luthier's ideas go through, with prompts that name the
language and its designers and nothing of Luthier:

1. extraction of ideas, one call per note (`extract_notes_ideas.py`, prompt `extract_ideas_text_v1`);
2. the timeline (`ideas_timeline.py`);
3. lineages (`link_ideas.py`, prompt `link_ideas_v2`);
4. the blind finding of candidates (`find_principles.py`, prompt `find_principles_v1`), which sees
   only the lineages and Luciano's criterion of infectability;
5. a judge (`compare_principles.py`, prompt `compare_principles_v1`) that maps each candidate to
   the items of the reference it states, to the items of Luthier it echoes (its principles P1 to
   P14 and features F1 to F16), or to neither, quoting both sides.

Read, decided before running:

- **Leakage**: a candidate that echoes a Luthier item and states no item of the reference. The
  filter passes if there is none.
- **Hits**: candidates that state an item of the reference. The filter passes if at least half
  of its candidates do. A reference has more items than the filter proposes candidates, so missed
  items are listed but not scored.
- An item of a reference that is also a Luthier item (Python's "errors should never pass silently")
  counts as a hit, not as leakage.
- The judge is a model too; its mappings come with quotes, and the report puts them in front of
  Luciano.

Limits known before running: Luthier's own lineages were made with `link_ideas_v1`, which names
Luthier; the controls use `link_ideas_v2`, which does not. The extraction prompt of the controls
differs from those used for Luthier's notes, voice notes and chats.

## Amendment, 2026-10-09, before any finding step ran

Luciano: "el problema es que cualquier agente va a saber qué es haskell y python". A model knows
both languages' principles from its training, so a hit may come from memory and not from the
corpus. Added, before the finding step ran on either corpus (the extraction of ideas was already
running; it reads the texts and does not judge principles):

- **A baseline from memory.** `compare_principles.py --recall`: the same model lists each
  language's principles with no text to read, and the judge scores that list against the same
  reference. A hit of the filter counts as coming from the corpus only if the baseline did not hit
  the same reference item.
- **A redacted run.** The finding step runs twice per language: as is, and with names replaced in
  what the model is shown (`--redact`): Python: `Python=L`, `Guido van Rossum=the designer`,
  `Guido=the designer`, `van Rossum=the designer`, `ABC=the predecessor`; Haskell: `Haskell=L`.
  Redaction is partial (a model can recognize Python from list comprehensions); a difference between
  the two runs measures how much the name drives the answer.
- **A language a model cannot know** is being looked for (released late 2025 or 2026, or obscure,
  with a principles statement separate from its other design writings, preferably not about
  verification or code written by models). If one is found, it gets the same protocol.

Leakage keeps its reading: a Luthier item a candidate states with no reference item behind it.

## Results, 2026-10-09

All runs with Claude Opus 5.5 at low effort; the files are under each control's folder.

| run | Python: hits | Python: leaks | Haskell: hits | Haskell: leaks |
|---|---|---|---|---|
| memory, no corpus (`--recall`) | 4/7 | 0 | 5/7 | 0 |
| find v1, as is | 2/7 | 0 | 3/7 | 0 |
| find v1, redacted | 3/7 | 0 | 3/7 | 0 |
| find v2, as is | 4/7 | 0 | 4/7 | 0 |
| find v2, redacted | 3/7 | 0 | 4/7 | 0 |

Read (the model's, for Luciano to weigh):

- No run brought Luthier's ideas: no candidate stated a Luthier item without a reference item.
- On Python the filter reads the corpus: its hits (G2, G9, G13, G14, Z8, Z10, Z12) are Guido's
  guidelines, which the memory baseline did not produce (it gave Z2, Z3, Z7, Z9, Z13). On Haskell
  every hit is also in memory (lazy, pure, type classes, consensus), so it tells nothing about the
  corpus.
- v1 returned single design decisions as principles (indentation, zero-based indexes, explicit
  self); v2, which asks for the road not taken, returns rules. Most of v2's misses are principles
  the designers state elsewhere and the references leave out (first-class everything, a value
  prints as an expression that reads back, effects as first-class values, notation that follows
  mathematics), so the hit rate understates the filter.
- Blind spot in every run: principles about the process and its tensions (Python's timesaving
  rules G1, G3 to G7: borrow ideas, don't fret about performance, good enough; Haskell's H4 to H7:
  a committee language, beauty against utility, evolution against stability) never came out. The
  filter finds principles about the artifact, not about how it is made.

## The naive run, 2026-10-10, written before it ran

Luciano, 2026-10-10, after reading the results above: "Quizas darle todas las ideas a un agente
naive y pedirle que extraiga de ahi las reglas y principios sea mejor que esta arquitectura
elaborada y pretendidamente precisa?" and, on the proposal to measure it, "Si correlo ahora".

What changes against find v2: the model sees every row of the timeline (date, who, the idea), not
the lineages; it is asked for "the rules and principles of this language", with no criterion of
infectability, no definition of a principle and no instruction to be blind
(`scripts/naive_principles.py`, prompt `naive_principles_v1`). What stays: the same timelines, the
same references, the same judge (`compare_principles_v1`), the same memory baseline, the same
redactions, opus at effort low, at most 7 candidates on the controls.

On Luthier, at most 10, as in the synthesis. There is no reference to score against, so the judge's
list A is the pipeline's ten candidates (`record/distillation/naive/reference.md`, S1 to S10) and
list B, as always, P1 to P14 and F1 to F16. Read there: how many naive candidates state a pipeline
candidate, and whether any states an item of P1 to P14, the principles about the process that no
run has found so far. The labels "hit" and "leak" of the judge's report mean, on Luthier, "states a
pipeline candidate" and "states a Luthier item and no pipeline candidate".

Read, decided before running, as numbers and without thresholds (D-2026-10-09-d): on each control,
hits of naive against hits of find v2 (as is and redacted) and against memory, and which reference
items naive hits that memory did not; whether any naive candidate states a process item (Python
G1, G3 to G7; Haskell H4 to H7).

### Results of the naive run, 2026-10-10

| run | Python: hits | Python: leaks | Haskell: hits | Haskell: leaks |
|---|---|---|---|---|
| memory, no corpus (`--recall`) | 4/7 | 0 | 5/7 | 0 |
| find v2, as is | 4/7 | 0 | 4/7 | 0 |
| find v2, "redacted" (names left in the prompt's first line) | 3/7 | 0 | 4/7 | 0 |
| naive, as is | 6/7 | 0 | 5/7 | 0 |
| naive, redacted (names out of the first line too) | 5/7 | 0 | 4/7 | 1 |

Each naive run was one call, accepted at the first attempt, in about four minutes.

Read (the model's, for Luciano to weigh):

- The naive run hits more on both controls and covers more of the reference: on Python 13 items
  as is and 13 redacted, against 7 for find v2; on Haskell 7 against 3.
- It finds principles about the process, which no earlier run found: on Python G6 and G7 (good
  enough, cut corners) and A4 (an evolutionary path with the users) as is, and also G1 (borrow
  ideas) and G4 (don't fret about performance) redacted; on Haskell H5 (a committee language) and
  H7 (stability against research) in both runs. The blind spot of find v1 and v2 came from their
  prompt (infectability, "a fact or a single decision is not a principle"), not from the corpora.
- The one leak (Haskell redacted, C5: algebraic data types and pattern matching are fundamental)
  is a design fact of Haskell that the reference does not list; the judge set it on F12 (`data`
  as initial algebras). It brings nothing of Luthier's.
- The naive candidates mix rules and design facts (Python: dynamic typing, indentation), what
  find v2 was written to avoid; the judge counts them as hits when the reference states them.
- On Luthier (`record/distillation/naive/`), 8 of the 10 naive candidates state a candidate of the
  pipeline, which covers 7 of the pipeline's 10. It misses S3 (the certified subtype from a
  predicate), S4 (the mathematical object as the type's invariant, which extends P10) and S7 (to
  express the invariances of the disciplines). It adds certificates by hash with a grade
  (C3), the forgetful functor that defines the language (C8, a candidate of the cutoff run of
  2026-10-09), groups of functions defined by coupled laws (C9), and Luthier as an orchestrator
  of other languages (C10). None states P1 to P13: the question asks for the principles of the
  language, and P1 to P13 are about how it is made.
