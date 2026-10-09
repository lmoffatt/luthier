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
