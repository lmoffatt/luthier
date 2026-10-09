---
note: 2018-05-12_the-origins-of-pgen.md
note_dir: texts
note_sha256: 51b28594332ab29e9c4499f8b9e3b8cd9d8b6418a75e36e2755bc47cfdde6230
title: "The origins of pgen"
author: Guido van Rossum
created: 2018-05-12T09:37:00
ideas: 16
quotes_found: 15/16
generated_by: extract_ideas_text_v1
prompt_sha256: a5a7292ce238a474d4418f49c9719fcbd32470c331074c03c54a0a5c46cd899f
mode: editor
prompt_vars: language=Python; designers=Guido van Rossum
agent: claude-code
model: opus
effort: low
---

## Ideas

### two-pgens-c-and-python
- **What**: There are two parser generators for Python, the original written in C and a later rewrite in Python living under lib2to3/pgen2, both written by the author.
- **Quote**: "There are actually two pgens. The original, in C, and a rewrite in Python, under lib2to3/pgen2." (line 4)
- **Also at**: line 6

### pgen-first-code-for-python
- **What**: The original pgen was the first code written for Python, though the lexer had to come first because pgen and Python share a lexer.
- **Quote**: "The original was actually the first code I wrote for Python. Although technically I had to write the lexer first (pgen and Python share their lexer, pgen just doesn't have any uses for most tokens)." (line 6)

### why-own-parser-generator
- **What**: The author wrote his own parser generator because the available options were sparse (Yacc, or hand-written parsers) and he disliked Yacc, finding it hard to reason about the limits of an LALR(1) grammar.
- **Quote**: "The reason for writing my own parser generator was that at the time the landscape of parser generators ... was pretty sparse ... I had used Yacc in college ... but for some reason I didn't like it much; IIRC I found it hard to reason about what the limitations on an LALR(1) grammar would be." (line 8)

### regex-instead-of-bnf
- **What**: Building on LL(1) parser-generation and the Dragon book's regex-to-DFA technique, he wanted to try one improvement: using regular expressions instead of the standard BNF format, and from combining these pgen was born.
- **Quote**: "I had one improvement over that that I wanted to try out: using regular expressions (sort of) instead of the standard BNF format. The Dragon book had also taught me how to turn regular expressions into DFAs, so I combined all that and pgen was born." (line 8)

### avoided-advanced-techniques
- **What**: He did not use more advanced parsing techniques, being unfamiliar with them or judging them too inefficient, as he believes most parser workers did then.
- **Quote**: "I was not familiar with more advanced techniques, or I deemed them too inefficient." (line 10)

### no-generator-for-lexer
- **What**: He chose not to use a generator for the lexer: he thought less of Lex than of Yacc (the Lex he knew would segfault on tokens longer than 255 bytes), and figured indentation would be hard to teach a lexer generator.
- **Quote**: "For the lexer I decided I would not use a generator ... the version of Lex that I was familiar with would just segfault when trying to scan a token longer than 255 bytes (really!). Also I figured that indentation would be hard to teach to a lexer generator." (line 12)

### pgen2-origin-at-elemental
- **What**: pgen2 arose at a startup (Elemental Security) where, tasked to design a custom security-assertion language, he designed something vaguely like Python, implemented in Python, and rewrote pgen's exact algorithm in Python using tokenize.py as the lexer.
- **Quote**: "I decided to design something vaguely like Python, implemented in Python, and decided that I wanted to reuse pgen, but with a backend in Python, using tokenize.py as the lexer. So I just rewrote the exact algorithm from pgen in Python" (line 14)

### pgen2-reused-for-2to3
- **What**: Because pgen2's input format was identical to the original pgen, it was easy to generate a Python parser by feeding it the Grammar file, and the open-sourced tooling was later used for 2to3.
- **Quote**: "it made sense to use those tools for 2to3. (It was easy to generate a Python parser with it because the input format was identical to the original pgen -- I just had to feed the Grammar file into the tool. :-)" (line 14)

### regex-to-resolve-conflicts
- **What**: Looking back, he may have seen the regex approach as a new way of addressing grammar conflicts without adding helper rules, e.g. rewriting left-factoring (A -> X | X Y Z becoming A -> X B; B -> Y Z | empty) instead as A -> X [Y Z].
- **Quote**: "I may have seen this as a new (to me) way of addressing the various conflicts that may occur without adding helper rules. E.g. what that page calls left-factoring ... I would rewrite instead as A -> X [Y Z]." (line 19)
- **Open**: He does not quite recall why he did it this way ("I don't quite recall why I did things this way", line 18).

### parsing-engine-and-empty-productions
- **What**: He believes the parsing engine still works with parsing tables derived from such rules through the regex -> NFA -> DFA transformation, with a requirement of no empty productions.
- **Quote**: "the parsing engine ... still works with parsing tables derived from such rules through the regex -> NFA -> DFA transformation; I think the requirement not to have any empty productions was required here." (line 23)
- **Open**: Stated with "I think", as a recollection.

### variable-number-of-children
- **What**: Another idea was that parse-tree nodes have a variable number of children (e.g. A -> X [Y Z] yields a node with 1 or 3 children), with a simple check in the code generator to tell which alternative was parsed.
- **Quote**: "the parse tree nodes produced by the parsing engine would have a variable number of children ... A simple check in the code generator would then be needed to determine which alternative the parser had encountered." (line 28)
- **Open**: This "has turned out to be a double-edged sword" (line 34), later requiring a parse-tree-to-AST step driven by a separate generator to simplify the byte code generator.

### regex-for-readability
- **What**: The reason he used regular expressions was probably to make the grammar easier to read: after resolving conflicts with rewrites the grammar was not easy to read, and regex avoided helper rules with awkward names, with [optional] and repeated* parts closer to how he thinks about a language's syntax.
- **Quote**: "the reason I used regular expressions was probably to make the grammar easier to read ... no helper rules with awkward names, and [optional] parts or repeated* parts are closer to how I think about a typical language's syntax." (line 38)
- **Also at**: line 41 (Zen of Python reference)

### power-unchanged-ll1
- **What**: The regex notation did not change the parsing power beyond LL(1), nor reduce it; by "regular expressions" he meant the EBNF conventions, noting EBNF may not have been a well-defined notation at the time.
- **Quote**: "It certainly did not change the power beyond LL(1), nor did it reduce the power. And yes by "regular expressions" I meant the EBNF conventions -- I'm not sure that at the time "EBNF" was a well-defined notation" (line 44)

### ebnf-to-bnf-not-improvement
- **What**: Converting EBNF to BNF and working from there would cause awkward extra parse-tree node types, so he does not think that would have been an improvement.
- **Quote**: "Converting EBNF to BNF and taking it from there would cause awkward extra parse tree node types, so I don't think that would have been an improvement." (line 49)

### would-choose-more-powerful-engine
- **What**: Doing it over, he might choose a more powerful parsing engine such as LALR(1)/Yacc/Bison, since several grammar areas need more power than LL(1), e.g. keyword args where 'arg: [NAME =] expr' is not valid because NAME is in the FIRST-set of expr; LALR(1) can handle it, but keyword args came years later and he did not want to redo the parser then.
- **Quote**: "If I had to do it all over again I might opt for a more powerful parsing engine, perhaps a version of LALR(1) ... the rule 'arg: [NAME =] expr' is not a valid rule, since NAME occurs in the FIRST-set of expr and the algorithm doesn't handle that. IIRC LALR(1) can handle it. But keyword args were several years in the future ... and I didn't want to redo the parser at that point." (line 53)

### python38-drops-c-pgen
- **What**: Python 3.8 will drop the C version of pgen in favor of a tweaked version of pgen2.
- **Quote**: "UPDATE March 2019: Python 3.8 will drop the C version of pgen, in favor of a tweaked version of pgen2." (line 63)
