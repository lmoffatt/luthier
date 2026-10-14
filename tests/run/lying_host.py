"""Host side of the first-action tests (record/IA/certification-2026-10-14/prompt-first-action.md):
a `print` that writes its line twice, where the description world_model.lut gives it
(`printDescribed`) says once. Imported as `python:run.lying_host.*` (tests/ on the path)."""
from luthier import host


def print_twice(w, s):
    host.print_line(w, s)
    return host.print_line(w, s)
