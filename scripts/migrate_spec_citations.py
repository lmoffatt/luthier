#!/usr/bin/env python3
"""Wave 1 of the specification: the citations of the old spec files (numbering of 2026-10-04,
in backticks: `05` R8, `04 §5`, `03`) moved to the chapters of docs/spec/ (`spec 4.R8`), in the
text the projection prints and in the documents that cite the spec. In the record, Quote, Source
and History keep the tags of their time (D-2026-10-12-v); only the other fields and the prose
outside (History:) paragraphs are moved. Mechanical, no model."""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SUBS = [
    (r"`05` R(\d+)", r"spec 4.R\1"), (r"`05 §3`", "spec 4 §4"), (r"`05 §7`", "spec 6"),
    (r"`05 §9`", "spec 5"), (r"`05`", "spec 4"),
    (r"`04 §5`", "spec 2 §4"), (r"`04` §7", "spec 8"), (r"`04 §7`", "spec 8"), (r"`04 §6`", "spec 3 §5"), (r"`04`", "spec 3"),
    (r"`03 §4`", "spec 12"), (r"`03`", "spec 12"),
    (r"`02 §9`", "spec 2 §8"), (r"`02 §1`", "spec 2 §1"), (r"`02 §8`", "spec 2 §8"), (r"`02`", "spec 2"),
    (r"`06 §8`", "spec 11"), (r"`06`", "spec 11"), (r"`08`", "spec 7"),
]
def remap(t):
    for a, b in SUBS:
        t = re.sub(a, b, t)
    return t
def record(path):
    out, field, in_fence, para_hist = [], None, False, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\s{0,3}```", line):
            in_fence = not in_fence; field = None; out.append(line); continue
        if in_fence:
            m = re.match(r"^(Quote|Source|History|[A-Z][a-z]+(?: on)?):", line)
            if m: field = m.group(1)
            elif not line.startswith(" "): field = None
            out.append(line if field in ("Quote", "Source", "History") else remap(line)); continue
        if not line.strip(): para_hist = False
        elif line.lstrip().startswith("(History:"): para_hist = True
        out.append(line if para_hist or line.startswith("|") else remap(line))
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
for name in sys.argv[1:]:
    p = ROOT / name
    record(p) if name.endswith("principles-language.md") else p.write_text(remap(p.read_text(encoding="utf-8")), encoding="utf-8")
