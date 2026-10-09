# Prompt: trace_rules_v1

You work on the record of a programming language, {language}, designed by {designers}. Below are two
lists: the rules of the language and of the way its work is done (normative statements of its
specification, sections of the specification, and decisions of its log), and the lineages of the
designers' ideas, one idea each. For each rule, say which lineages state it or motivate it: the ideas
the rule comes from. A rule may come from several ideas, from one, or from none (a rule invented in
the writing of the specification has no lineage behind it, and saying so is useful).

A lineage states a rule when accepting the idea commits one to the rule, or the rule is the idea made
precise; it motivates a rule when the rule exists to serve it. Sharing a topic is not enough. Name at
most five lineages per rule, the closest first. Judge from the texts in front of you only.

## Your answer

One JSON object and nothing else, no fence, no prose, compact:

```
{"traces": [["<rule id>", ["l<n>", ...]], ...]}
```

Every rule appears once; an empty list means no lineage. A script checks the ids.

## Input

<<<INPUT>>>
