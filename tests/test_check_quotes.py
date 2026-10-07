"""scripts/check_quotes.py on records, a git repository and a transcript of its own (step 4.1 of
record/plan-working-method-execution-2026-10-06.md)."""
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_quotes.py"

NOTES = """\
# Notes

The token is here.
The idea is that the human
signature has to be distinctive.
ok
Él dijo: comiteamos antes de aplicar un cambio.
true
"""

SESSION = "abcdef12-3456-7890-abcd-ef1234567890"
TRANSCRIPT = [
    {"type": "user", "message": {"role": "user", "content": "hola, empecemos"}},
    {"type": "assistant", "message": {"content": [
        {"type": "thinking", "thinking": "es un si"},
        {"type": "text", "text": "Una respuesta del modelo."}]}},
    {"type": "attachment", "attachment": {"type": "queued_command", "prompt": [
        {"type": "text", "text": "es un si. \nAsceleremos que estamos estaticos."}]}},
    {"type": "user", "message": {"content": [
        {"type": "tool_result", "tool_use_id": "x", "content": "es un si"}]}},
]


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=test", "-c", "user.email=test@example.com",
         "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", *args],
        check=True, capture_output=True, text=True).stdout.strip()


def make_repo(path: Path, files: dict[str, str]) -> str:
    """A git repository at path holding files, and the short hash of its one commit."""
    path.mkdir(parents=True)
    git(path, "init", "-q")
    for name, text in files.items():
        (path / name).parent.mkdir(parents=True, exist_ok=True)
        (path / name).write_text(text, encoding="utf-8")
    git(path, "add", "-A")
    git(path, "commit", "-q", "-m", "notes")
    return git(path, "rev-parse", "--short=7", "HEAD")


def setup(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    return repo, make_repo(repo, {"docs/notes.md": NOTES})


def run(tmp_path: Path, record: str, *args: str) -> subprocess.CompletedProcess:
    (tmp_path / "decisions.md").write_text(record, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), "decisions.md", "--transcripts", str(tmp_path / "projects"),
         *args],
        capture_output=True, text=True, cwd=tmp_path)


def entry(quote: str, source: str, author: str = "Luciano") -> str:
    return ("# Decisions\n\n```\n"
            "D-2026-10-06-a  A decision.\n"
            f"Author:     {author}\n"
            f"Quote:      {quote}\n"
            f"Source:     {source}\n"
            "Status:     current\n"
            "```\n")


def check(tmp_path: Path, quote: str, line: str) -> subprocess.CompletedProcess:
    repo, commit = setup(tmp_path)
    return run(tmp_path, entry(quote, f"luthier@{commit}:docs/notes.md:{line}"),
               "--repo-root", f"luthier={repo}")


def test_right_quote_passes(tmp_path):
    r = check(tmp_path, '"signature has to be distinctive." (line 5)', "5")
    assert (r.returncode, r.stdout, r.stderr) == (0, "", "")


def test_quote_one_line_late_fails(tmp_path):
    r = check(tmp_path, '"signature has to be distinctive."', "6")
    assert r.returncode == 1
    assert r.stdout.startswith("decisions.md:4: quote: D-2026-10-06-a: quote ")
    assert "it starts at line 5" in r.stdout


def test_quote_spanning_two_lines_passes(tmp_path):
    r = check(tmp_path, '"The idea is that the human signature has\n'
                        '            to be distinctive."', "4")
    assert (r.returncode, r.stdout) == (0, "")


def test_one_word_quote_at_wrong_line_fails(tmp_path):
    # "ok" is line 6, within the 30 lines after line 5, but doesn't start in line 5.
    r = check(tmp_path, '"ok"', "5")
    assert r.returncode == 1 and "it starts at line 6" in r.stdout


def test_one_word_quote_inside_a_word_fails(tmp_path):
    # Line 3 holds "token", which contains "ok".
    r = check(tmp_path, '"ok"', "3")
    assert r.returncode == 1 and "it starts at line 6" in r.stdout


def test_one_changed_character_fails(tmp_path):
    assert check(tmp_path / "right", '"Él dijo: comiteamos"', "7").returncode == 0
    wrongs = ('"El dijo: comiteamos"', '"Él dijo: Comiteamos"', '"Él dijo: comitiamos"')
    for k, wrong in enumerate(wrongs):
        r = check(tmp_path / f"wrong{k}", wrong, "7")
        assert r.returncode == 1 and "nor anywhere else in that file" in r.stdout, wrong


def test_quotes_pair_with_sources_in_order(tmp_path):
    repo, commit = setup(tmp_path)
    src = f"luthier@{commit}:docs/notes.md"
    quotes = '"ok"\n            "true"'
    roots = ("--repo-root", f"luthier={repo}")

    r = run(tmp_path, entry(quotes, f"{src}:6\n            {src}:8"), *roots)
    assert (r.returncode, r.stdout) == (0, "")

    r = run(tmp_path, entry(quotes, f"{src}:8\n            {src}:6"), *roots)
    assert r.returncode == 1
    assert r.stdout.count("quote: D-2026-10-06-a: quote ") == 2
    assert 'quote 1 of 2 "ok"' in r.stdout and 'quote 2 of 2 "true"' in r.stdout

    # One source for several quotes: each quote starts in the lines it names.
    r = run(tmp_path, entry(quotes, f"{src}:6-8"), *roots)
    assert (r.returncode, r.stdout) == (0, "")

    r = run(tmp_path, entry(quotes + '\n            "ok"', f"{src}:6\n            {src}:8"), *roots)
    assert r.returncode == 1 and "3 quotes and 2 sources" in r.stdout


def test_missing_repository_warns(tmp_path):
    r = run(tmp_path, entry('"ok"', "sonolocalizacion@abcdef1:docs/notes.md:6"),
            "--repo-root", f"sonolocalizacion={tmp_path / 'absent'}")
    assert (r.returncode, r.stdout) == (0, "")
    assert r.stderr.startswith("decisions.md:4: warning: D-2026-10-06-a: repository "
                               "sonolocalizacion not on disk")


def test_unknown_commit_and_path_fail(tmp_path):
    repo, commit = setup(tmp_path)
    r = run(tmp_path, entry('"ok"', "luthier@abcdef1:docs/notes.md:6"), "--repo-root",
            f"luthier={repo}")
    assert r.returncode == 1 and "commit abcdef1 not found" in r.stdout
    r = run(tmp_path, entry('"ok"', f"luthier@{commit}:docs/other.md:6"), "--repo-root",
            f"luthier={repo}")
    assert r.returncode == 1 and "docs/other.md is not a file" in r.stdout


def test_absolute_repository_path_with_spaces(tmp_path):
    repo = tmp_path / "a repo@home"
    commit = make_repo(repo, {"Lucianos notes/his notes.md": NOTES})
    r = run(tmp_path, entry('"true"', f"{repo}@{commit}:Lucianos notes/his notes.md:8"))
    assert (r.returncode, r.stdout, r.stderr) == (0, "", "")


def test_chat_source(tmp_path):
    project = tmp_path / "projects" / "-home-someone-project"
    project.mkdir(parents=True)
    (project / f"{SESSION}.jsonl").write_text(
        "".join(json.dumps(o, ensure_ascii=False) + "\n" for o in TRANSCRIPT), encoding="utf-8")

    def chat(quote: str, line: str) -> subprocess.CompletedProcess:
        return run(tmp_path, entry(quote, f"chat:{SESSION[:8]}:{line}"))

    assert chat('"es un si. Asceleremos que estamos estaticos."', "3").returncode == 0
    assert chat('"Una respuesta del modelo."', "2").returncode == 0
    assert chat('"hola, empecemos"', "1").returncode == 0
    r = chat('"Asceleremos que estamos estaticos."', "2")
    assert r.returncode == 1 and "it starts at line 3" in r.stdout
    # Thinking and tool results are not text of the conversation.
    r = chat('"es un si"', "4")
    assert r.returncode == 1 and "line 4 has no text; it starts at line 3" in r.stdout
    r = chat('"es un si"', "2")
    assert r.returncode == 1 and "it starts at line 3" in r.stdout

    r = run(tmp_path, entry('"ok"', "chat:00000000:1"))
    assert (r.returncode, r.stdout) == (0, "")
    assert "warning: D-2026-10-06-a: no transcript 00000000*.jsonl" in r.stderr


def test_which_entries_need_a_quote(tmp_path):
    repo, commit = setup(tmp_path)
    record = f"""\
```
D-2026-10-06-a  By Luciano, with no quote.
Author:     Luciano for the axis; the model for the scheme

D-2026-10-06-b  By the model, with no quote.
Author:     the model

D-2026-10-06-c  A quote with no source.
Author:     the model
Quote:      "ok"

D-2026-10-06-d  A source outside the grammar.
Author:     the model
Quote:      "ok"
Source:     docs/notes.md:6

P1  A principle with no quote and no word of why.
Source:     luthier@{commit}:docs/notes.md:6
Status:     current

P2  A principle whose source is still to be found,
                in a statement of two lines.
Status:     current since 2026-10-05; source to
            pin: his words are in a session
```
"""
    r = run(tmp_path, record, "--repo-root", f"luthier={repo}")
    assert r.returncode == 1
    assert r.stdout.splitlines() == [
        "decisions.md:2: quote: D-2026-10-06-a: a decision whose Author mentions Luciano has Quote",
        "decisions.md:8: quote: D-2026-10-06-c: has Quote but no Source",
        "decisions.md:12: quote: D-2026-10-06-d: Source: not in the grammar <repo>@<commit>:<path>:"
        "<line> or chat:<session8>:<line>, with <a>-<b> for a range: docs/notes.md:6",
        'decisions.md:17: quote: P1: a principle has Quote, unless its Status says "source to pin"',
    ]
    assert r.stderr == "decisions.md:21: warning: P2: no Quote; its Status says source to pin\n"


def test_missing_default_record_warns(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    r = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(empty)],
                       capture_output=True, text=True, cwd=tmp_path)
    assert (r.returncode, r.stdout) == (0, "")
    assert r.stderr.count("warning: no record here") == 2


# ---------------------------------------------------------------- found by the adversarial check

def write_transcript(tmp_path: Path, objects: list[dict], folder: str = "-home-someone-project"
                     ) -> Path:
    project = tmp_path / "projects" / folder
    project.mkdir(parents=True, exist_ok=True)
    path = project / f"{SESSION}.jsonl"
    path.write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in objects),
                    encoding="utf-8")
    return path


MESSAGES = [
    {"type": "user", "message": {"role": "user", "content": "hacé la separación"}},
    {"type": "assistant", "message": {"content": [{"type": "text", "text": "ok, la hago ahora."}]}},
    {"type": "attachment", "attachment": {"type": "queued_command", "prompt": [
        {"type": "text", "text": "quizas lo mejor sea un directorio"}]}},
    {"type": "attachment", "attachment": {"type": "queued_command",
                                          "prompt": "porque es mala idea"}},
]


def test_chat_quote_lies_within_one_message(tmp_path):
    # Joined, Luciano's message and the model's reply read "hacé la separación ok, la hago":
    # a quote stitched across them is not his.
    write_transcript(tmp_path, MESSAGES)

    def chat(quote: str, line: str) -> subprocess.CompletedProcess:
        return run(tmp_path, entry(quote, f"chat:{SESSION[:8]}:{line}"))

    assert chat('"hacé la separación"', "1").returncode == 0
    r = chat('"hacé la separación ok, la hago"', "1")
    assert r.returncode == 1 and "it runs across messages, from line 1" in r.stdout
    assert chat('"un directorio porque es mala"', "3").returncode == 1
    assert chat('"quizas lo mejor"', "1-3").returncode == 0
    assert chat('"quizas lo mejor"', "1-2").returncode == 1


def test_composed_and_decomposed_accents_are_the_same_text(tmp_path):
    import unicodedata
    repo = tmp_path / "repo"
    commit = make_repo(repo, {"nfd.md": unicodedata.normalize("NFD", "Él dijo: café con leche\n")})
    roots = ("--repo-root", f"luthier={repo}")
    # "é" as one character in the record, as "e" and an accent in the source.
    r = run(tmp_path, entry('"Él dijo: café con leche"', f"luthier@{commit}:nfd.md:1"), *roots)
    assert (r.returncode, r.stdout) == (0, "")
    # Without the accent the quote ends inside a word of the source.
    r = run(tmp_path, entry('"dijo: cafe"', f"luthier@{commit}:nfd.md:1"), *roots)
    assert r.returncode == 1


def test_an_indented_fence_in_a_quote_is_text(tmp_path):
    repo = tmp_path / "repo"
    commit = make_repo(repo, {"fence.md": "intro\n```\ncode here\n```\n",
                              "nofence.md": "intro\ncode here\n"})
    roots = ("--repo-root", f"luthier={repo}")
    quote = '"intro\n            ```\n            code here"'
    r = run(tmp_path, entry(quote, f"luthier@{commit}:fence.md:1"), *roots)
    assert (r.returncode, r.stdout) == (0, "")
    r = run(tmp_path, entry(quote, f"luthier@{commit}:nofence.md:1"), *roots)
    assert r.returncode == 1


def test_a_wrapped_line_may_start_with_a_quotation(tmp_path):
    repo = tmp_path / "repo"
    commit = make_repo(repo, {"q.md": 'the word "token" is here\na "b" c "d" e\na "b" X "d" e\n'})
    roots = ("--repo-root", f"luthier={repo}")
    src = f"luthier@{commit}:q.md"
    r = run(tmp_path, entry('"the word\n            "token" is here"', f"{src}:1"), *roots)
    assert (r.returncode, r.stdout) == (0, "")
    # Read as two quotes, 'a "b' and 'd" e', this one would be found at line 3 too.
    r = run(tmp_path, entry('"a "b" c\n            "d" e"', f"{src}:3"), *roots)
    assert r.returncode == 1
    r = run(tmp_path, entry('"a "b" c\n            "d" e"', f"{src}:2"), *roots)
    assert (r.returncode, r.stdout) == (0, "")
    # A closed quote, even with trailing text, still lets the next line start a quote.
    r = run(tmp_path, entry('"a "b" c" (line 2)\n            "the word"',
                            f"{src}:2\n            {src}:1"), *roots)
    assert (r.returncode, r.stdout) == (0, "")


def test_a_misspelt_repeated_or_missing_field_fails(tmp_path):
    record = """\
```
D-2026-10-06-a  A quote under a misspelt field would go unchecked.
Author:     the model
Qoute:      "ok"
Source:     docs/notes.md:6

D-2026-10-06-b  A second Author would be ignored.
Author:     the model
Author:     Luciano

D-2026-10-06-c  With no Author, nothing says whether a quote is needed.
Status:     current
```
"""
    r = run(tmp_path, record)
    assert r.returncode == 1
    assert r.stdout.splitlines() == [
        "decisions.md:2: quote: D-2026-10-06-a: Qoute: not a field of the record (the fields are "
        "Author, Quote, Source, Assumption, Kind, Principles, Status)",
        "decisions.md:7: quote: D-2026-10-06-b: Author: given twice",
        "decisions.md:11: quote: D-2026-10-06-c: a decision has Author, which says whether it "
        "needs a Quote",
    ]


def test_prose_that_starts_with_an_id_is_not_an_entry(tmp_path):
    repo, commit = setup(tmp_path)
    record = f"""\
# Principles

Two of them need their sources pinned:
P10 and P11, in force before the record began.
D-2026-10-06-h is a bundle, as the log says.

P3  An entry outside a fence is still an entry when it has fields.
Quote:      "ok"
Source:     luthier@{commit}:docs/notes.md:5
"""
    r = run(tmp_path, record, "--repo-root", f"luthier={repo}")
    assert r.returncode == 1
    assert len(r.stdout.splitlines()) == 1
    assert r.stdout.startswith("decisions.md:7: quote: P3: quote \"ok\" not at ")


def test_one_session_in_two_project_folders(tmp_path):
    write_transcript(tmp_path, MESSAGES, "-home-someone-project")
    copy = write_transcript(tmp_path, MESSAGES[:2], "-home-someone-moved")

    def chat() -> subprocess.CompletedProcess:
        return run(tmp_path, entry('"porque es mala idea"', f"chat:{SESSION[:8]}:4"))

    # One copy is the start of the other: the longer is read.
    assert (chat().returncode, chat().stdout) == (0, "")
    copy.write_text(json.dumps(MESSAGES[1]) + "\n", encoding="utf-8")
    r = chat()
    assert r.returncode == 1 and "the copies differ" in r.stdout


def test_bad_input_fails_cleanly(tmp_path):
    (tmp_path / "latin1.md").write_bytes("Él".encode("latin-1"))
    r = subprocess.run([sys.executable, str(SCRIPT), "latin1.md"], capture_output=True, text=True,
                       cwd=tmp_path)
    assert (r.returncode, r.stderr) == (1, "")
    assert r.stdout.startswith("latin1.md:0: quote: the record is not UTF-8")
    r = run(tmp_path, entry('"ok"', "chat:00000000:1"), "--context", "-1")
    assert r.returncode == 2 and "expected a whole number of lines" in r.stderr


def test_a_line_separator_inside_a_quote_is_whitespace(tmp_path):
    # U+2028 ends a line for str.splitlines, not for git: the record's lines are git's.
    repo = tmp_path / "repo"
    commit = make_repo(repo, {"s.md": "first second\n"})
    r = run(tmp_path, entry('"first second"', f"luthier@{commit}:s.md:1"),
            "--repo-root", f"luthier={repo}")
    assert (r.returncode, r.stdout) == (0, "")


def test_an_entry_with_a_misspelt_id_fails(tmp_path):
    # Not read as an entry, its Author would go unseen, and with it the need for a quote.
    record = """\
```
D-2026-10-06-A  An id with a capital letter.
Author:     Luciano
Status:     current
```
"""
    r = run(tmp_path, record)
    assert r.returncode == 1
    assert r.stdout.splitlines()[0].startswith("decisions.md:3: quote: Author: belongs to no entry")
