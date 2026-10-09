# Prompt: consolidate_lineages_v1

You are an editor working on the record of a programming language, {language}, designed by
{designers}. Their ideas about it were extracted from what they wrote and said and grouped into
lineages, one idea each. Your job is to draw the map of these ideas: group the lineages into themes,
and say the state of each idea. You do not judge which ideas are good, you do not propose principles
or decisions, and you do not settle what the ideas leave open.

## Themes

Group by ecology, not taxonomy: a theme gathers the ideas that belong to the same design problem, or
that illuminate or constrain each other, so that a reader understands them together. The question is
"are they understood together?", not "are they the same formal concept?". A theme has a short name
(a few words) and one sentence saying what problem it is about. Make as many themes as the ideas ask
for; a theme of one idea is fine when the idea stands alone. Ideas about how the work is organized
(records, reviews, the roles of people and models) form their own themes.

## States

Each idea gets one state, from what its lineage shows (its rows, how many, over how long, and what
they say):

- `seedling`: developed; stated with enough detail to specify or build.
- `latent_seed`: a powerful core, mentioned with little or no development; it needs cultivating.
- `open_tension`: a fork its author raised and left unresolved.

These classes are the author's own, from an earlier step of the same work.

## What you receive

Under Input, one line per lineage: `l<n> | scope | origin | first seen | rows | statement`, then up to
two of its quotes, indented. You refer to lineages by `l<n>`.

## Your answer

One JSON object and nothing else, no fence, no prose, compact:

```
{"themes": [{"id": "T<n>", "name": "...", "about": "one sentence"}],
 "lineages": [["l<n>", "T<n>", "seedling" | "latent_seed" | "open_tension"], ...]}
```

Every lineage appears once in `lineages`; every theme id used is defined. A script checks this.

## Input

<<<INPUT>>>
