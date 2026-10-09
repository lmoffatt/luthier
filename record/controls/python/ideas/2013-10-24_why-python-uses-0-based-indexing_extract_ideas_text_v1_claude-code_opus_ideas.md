---
note: 2013-10-24_why-python-uses-0-based-indexing.md
note_dir: texts
note_sha256: bd01fba1b2c0c718b22ea169fdf0119f7203bd884d1c279cb5a5d348172c9559
title: "Why Python uses 0-based indexing"
author: Guido van Rossum
created: 2013-10-24T08:44:00
ideas: 10
quotes_found: 10/10
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### slice-notation-decided-indexing-base
- **What**: Van Rossum attributes his choice of Python's indexing base largely to how slice notation would work out; slicing was the deciding issue.
- **Quote**: "I think that one of the issues that helped me decide / was slice notation." (line 6)

### predecessors-pulled-both-ways
- **What**: Python's two main predecessors pulled in opposite directions on indexing: ABC used 1-based, C used 0-based; his earlier languages (Algol, Fortran, Pascal) used 1-based or variable-based.
- **Quote**: "ABC, one of Python's predecessors, / used 1-based indexing, while C, the other big influence, used 0-based." (line 3)
- **Also at**: lines 5

### common-slicing-use-cases
- **What**: He frames the decision around the two most common slicing use cases: getting the first n items and getting the next n items starting at i, the former being a special case of the latter.
- **Quote**: "most common use cases for slicing are \"get the first n items\" and \"get / the next n items starting at i\"" (line 10)

### avoid-plus-minus-one-compensations
- **What**: A criterion for a good notation is that these use cases be expressible without awkward +1 or -1 corrections.
- **Quote**: "It would be nice if both of these could be / expressed as without awkward +1 or -1 compensations." (line 12)

### zero-based-half-open-defaults-elegant
- **What**: The combination Python adopted, 0-based indexing with half-open intervals and suitable defaults, makes those use cases come out cleanly as a[:n] and a[i:i+n].
- **Quote**: "Using / 0-based indexing, half-open intervals, and suitable defaults (as Python / ended up having), they are beautiful: a[:n] and a[i:i+n]" (line 15)

### one-based-half-open-inelegant
- **What**: With 1-based indexing, half-open intervals are not elegant; getting the first n elements forces either closed intervals or a start-and-length slice notation.
- **Quote**: "Using half-open intervals just isn't very elegant when / combined with 1-based indexing." (line 23)

### closed-intervals-force-minus-one
- **What**: Under 1-based indexing with closed intervals, the n items starting at i require the awkward a[i:i+n-1].
- **Quote**: "Using closed intervals, you'd have to / write a[i:i+n-1] for the n items starting at i." (line 24)

### index-length-notation-as-abc-did
- **What**: An alternative he considered is a start-and-length (index:length) slice convention, which might suit 1-based indexing; ABC in fact did this with its own notation a@i|n.
- **Quote**: "So perhaps using the / slice length would be more elegant with 1-based indexing? ... And this is in fact what ABC did -- it used a different / notation so you could write a@i|n." (line 25)
- **Open**: He raises index:length as a possible improvement but does not resolve how it works for other use cases.

### fuzzy-memory-on-other-use-cases
- **What**: When pushing the index:length convention against other use cases his memory is uncertain, but he believes the elegance of half-open intervals swayed him.
- **Quote**: "TBH / this is where my memory gets fuzzy, but I think I was swayed by the / elegance of half-open intervals." (line 31)
- **Open**: He does not reconstruct the full comparison for other use cases.

### adjacency-invariant
- **What**: The decisive beauty is the invariant that for adjacent slices the first slice's end index equals the second slice's start index, illustrated by splitting a string at i and j into a[:i], a[i:j], a[j:].
- **Quote**: "the invariant that when two / slices are adjacent, the first slice's end index is the second slice's / start index is just too beautiful to ignore." (line 33)
- **Also at**: lines 35, 37
