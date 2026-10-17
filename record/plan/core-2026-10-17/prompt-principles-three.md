# Brief: three clauses from this week's decisions into the principles record

Read `CLAUDE.md` first. Edit only `record/principles-language.md`; never `docs/principles.md` by
hand. Add each clause after the last clause of its principle, with its History line "2026-10-17:
clause N added, proposed (D-...)". Rewrap to 100 columns; change no other word.

1. After L3's last clause, as the next number:
   "Two types that differ only in the names of their fields or injections are distinct at the strict
   level, the hash, and equivalent by a named value, the renaming of their projections: an
   equivalence between types is a value with its laws, the two maps and their round trips, certified
   once, and certificates transport along it at its cost, nothing when it is exact (L6, L10.7)
   (D-2026-10-17-a). [proposed]"
2. After L8's last clause, as the next number:
   "The certified subtype from a law is the equalizer of the law and the constant `true`, the
   forgetful projection its universal arrow; so each construction of clause 5 is an instance of a
   structure of the core with its universal property (D-2026-10-17-g). [proposed]"
3. After L11's last clause, as the next number:
   "What has no feedback to check it is a root of trust: the system's delivery to the terminal, the
   file system, the interpreter, the floating-point hardware. The roots of trust are declared once
   per project and listed in every run's record; above them everything is checked: an action writes
   at once and fails when the system rejects what it writes, and a place is observed according to
   what it is, a file by re-reading it, a pipe by its own copy, a terminal by the bytes it accepted.
   Which kind of feedback each place has, and the grade an action there earns by it, is open
   (D-2026-10-16-n). [proposed]"

Then `python3 scripts/project_principles.py --write` and `--check`.
Accepted when `--check` prints ok and `git diff` touches only the two principles files and only
those three clauses and their History lines. Commit the record, then the projection, two-line
messages (subject, blank line, body) ending with "Co-Authored-By: Claude Sonnet 5.5
<noreply@anthropic.com>"; stage by path; other agents commit at the same time (retry on
.git/index.lock). Final message: the clause numbers given, the hashes, the --check output.
