# Reference for the control on Haskell

What the filter should find, from Hudak, Hughes, Peyton Jones and Wadler, "A History of Haskell:
Being Lazy With Class", HOPL III, 2007, doi:10.1145/1238844.1238856; line numbers are of
`sources/history_flow.txt` (pinned in `../README.md`). Never shown to the filter.

Section 3, "Goals, principles, and processes" ("In this section we reflect on the principles that
underlay our thinking, the big choices that we made, and processes that led to them", line 578):

- H1 Haskell is lazy (3.1, line 579): "Laziness was undoubtedly the single theme that united the various groups that contributed to Haskell's design."
- H2 Haskell is pure (3.2, line 610): "Haskell is, therefore, a pure language"; "laziness kept us pure" (line 637).
- H3 Haskell has type classes (3.3, line 639): overloading, "now regarded as Haskell's most distinctive characteristic".
- H4 Haskell has no formal semantics (3.4, line 722): "One of our explicit goals was to produce a language that had a formally defined type system and semantics."
- H5 Haskell is a committee language (3.5, line 720).
- H6 Haskell is a big language (3.6, line 781): "the competition between beauty and utility"; "we passionately wanted to design a simple, elegant language", and "we also really wanted Haskell to be a useful language".
- H7 Haskell and Haskell 98 (3.7, line 817): "The goal of using Haskell for research demands evolution, while using the language for teaching and applications requires stability."

The committee's goals, section 2.3 (lines 324 to 333), left out of the corpus:

- C1 It should be suitable for teaching, research, and applications, including building large systems.
- C2 It should be completely described via the publication of a formal syntax and semantics.
- C3 It should be freely available.
- C4 It should be usable as a basis for further language research.
- C5 It should be based on ideas that enjoy a wide consensus.
- C6 It should reduce unnecessary diversity in functional programming languages.
