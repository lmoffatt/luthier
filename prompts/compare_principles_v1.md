# Prompt: compare_principles_v1

You compare statements, as a careful reader would, and nothing else.

You receive three lists. List C holds candidate principles proposed for a programming language,
each with an id, a statement and the quote it rests on. Lists A and B hold other statements, each
with an id. For every candidate of C, say which items of A and which items of B it states.

A candidate states an item when someone who accepts the candidate thereby accepts that item: the
same content, possibly in other words, possibly narrower or broader as long as the core claim is
the same. Sharing a topic is not enough ("errors" and "errors should not pass silently" are not the
same claim). A candidate may state several items, of either list, or none.

Compare only the texts in front of you. Do not use what you may know about any language, its
designers or its history, and do not guess where the lists come from.

## Your answer

One JSON object and nothing else, no fence, no prose, compact:

```
{"judgments": [{"candidate": "C<n>",
                "A": [{"item": "<id>", "why": "a few words"}],
                "B": [{"item": "<id>", "why": "a few words"}]}]}
```

Every candidate of C appears once; every item id is one of its list. A script checks this.

## Input

<<<INPUT>>>
