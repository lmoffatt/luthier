# Prompt: adopt_method_v1

You are setting up the working method for one of Luciano Moffatt's projects. He built the method for
luthier and sonolocalización; take from it what serves this project, and nothing else.

## What to read

Pin the version first: `git -C /home/lmoffatt/Projects/luthier rev-parse --short HEAD`, called
`<commit>` below, and read with `git -C /home/lmoffatt/Projects/luthier show <commit>:<path>`.

- `CLAUDE.md`: the working rules and the principles in force.
- `docs/principles.md`: each principle with Luciano's words and its assumption.
- `docs/decisions.md`: why each rule exists.

Read `docs/working-method.md` only for a rule you need to understand better. It is long and full of
the specifics of luthier and sonolocalización.

## Steps

1. **The objectives.** Find what this project is for, in Luciano's own words: his notes, transcripts
   of his voice notes, his turns in chats; summaries written by models only point you to them. Draft
   at most five objectives, each a line with a verbatim quote and its source. If his words don't
   say, ask him in one question. Everything below is judged against them, by P4 (decisions follow
   guiding principles toward the objectives of the project).
2. **Take, adapt or leave out.** For each principle and each rule of `CLAUDE.md`, decide which, with
   a reason in one line, judged by the objectives, P8 (no more bureaucracy than it pays for) and P12
   (Luciano's attention is the scarce resource). Likely specific to luthier: P10 (the invariant of
   a type) and the language's own checks. The chat exports to a public GitHub never apply to work
   for a client.
3. **Start small.** The core is: commit before every change; a document for Luciano is committed
   before he annotates it, then his annotations are committed verbatim; questions to him come as
   bites he can answer after reading a screen; at the end of each task, list the decisions you took
   on your own. Any other mechanism comes in only after a real case it would have caught
   (D-2026-10-06-s in luthier's log).
4. **Write**, in this project, committing each file before Luciano reads it:
   - `CLAUDE.md`: the rules and the principles in force, with no meta-information.
   - `docs/decisions.md`: a first entry "Adopted the working method from luthier@<commit>", listing
     what was taken, adapted and left out, one line each with its reason.
   - `docs/objectives.md`: the draft of step 1.
5. **Report to Luciano**, in Spanish, only what needs him: the objectives to mark, and the choices
   of step 2 whose implications go beyond this project, as bites (ok, no, or a correction). Then a
   short list of what you left out: comparing what each project keeps is how the universal part of
   the method will be found.

## Rules

- Luciano's words are quoted verbatim, typos kept, with their source.
- If the project is work for a client or with coauthors, nothing of it leaves its folder: no
  exports, no citations into luthier or anywhere public.
- Files in English; chat with Luciano in Spanish.
