"""Host side of the first-action tests (record/IA/certification-2026-10-14/prompt-first-action.md):
a `print` that writes its line twice, where the description world_model.lut gives it
(`printDescribed`) says once. Imported as `python:run.lying_host.*` (tests/ on the path)."""
from luthier import host


def print_twice(w, s):
    host.print_line(w, s)
    return host.print_line(w, s)


def read_and_print(w, path):
    """A `readFile` that also prints a line: its case agrees with the console's description at the
    place it declares (the path), and changes the standard output, which it does not declare
    (world.lth's `HostChangesOnlyDeclared`; record/IA/layer-3-review-2026-10-15/prompt-run-host.md)."""
    host.print_line(w, "noise")
    return host.read_file(w, path)
