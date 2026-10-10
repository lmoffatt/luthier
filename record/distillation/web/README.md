# The naive run on five web AIs, 2026-10-10

Luciano pasted `prompt_web_principles_v1.md` into five web chats and brought each answer back
unedited; the model files are verbatim his paste of each answer. The prompt asks the naive question
twice (the rules and principles of the language; of how it is built), at most 20 each, every item
citing the rows (`r<n>`) of `ideas.txt` it rests on (2,322 ideas from `record/ideas/timeline.jsonl`,
sha256 b18b5806955d; `ideas_redacted.txt` is the same file with Luthier=L, Luciano
Moffatt=the designer, sonolocalización=the application; the redaction is partial: 22 mentions such
as "PyLuthier" and "luthierize" survive, and gemini wrote "Luthier" from them).

| file | model, as Luciano reports it | read |
|---|---|---|
| `claude.md` | Claude (Fable, max effort) | redacted |
| `chatGPT.md` | ChatGPT (the best model of his plan) | named |
| `gemini.md` | Gemini (Pro, with thinking) | redacted |
| `deepseek.md` | DeepSeek (free, no options) | redacted |
| `grok.md` | Grok (free, no options) | redacted |

Which file each read is inferred from the answers ("Luciano" against "the designer"); the model
identities are Luciano's word (2026-10-10).

Mechanical check (every cited row looked up in the timeline; "first said by" against the earliest
cited row's author and date):

| answer | lines | unknown rows | first-said-by wrong | distinct rows cited |
|---|---|---|---|---|
| claude | 40 | 0 | 1 (a cited row has no date) | 395 |
| chatGPT | 40 | 0 | 0 | 185 |
| gemini | 40 | 0 | 0 | 206 |
| deepseek | 40 | 0 | 4 | 218 |
| grok | 40 | 0 | 3 | 182 |

The alignment of the five answers with the pipeline's candidates and the principles in force:
`alignment_2026-10-10.md`.
