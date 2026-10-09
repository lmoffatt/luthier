"""scripts/scrub_private.py replaces private words in place, consistently, and leaves other text alone."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_scrub(tmp_path):
    words = tmp_path / "w.private"
    words.write_text("secretword\n")
    a = tmp_path / "a.json"
    a.write_text('{"id": "L-apply-to-secretword", "text": "SecretWord and secretwords"}\n')
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "scrub_private.py"), str(a), "--words", str(words)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert a.read_text() == '{"id": "L-apply-to-[private word]", "text": "[private word] and secretwords"}\n'
    assert "2 replaced" in r.stdout
