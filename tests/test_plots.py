"""plots.py, the renderer as the model of plot.lth's `Drawing` (record/IA/plots-2026-10-15/
prompt-host.md, item 2), on plot.lth at c6febf0. Each test names the law of plot.lth §5 or §4 it
holds the host to; the run of a `Plot` built in Luthier is tests/run/plot_two_tables.lut."""
from pathlib import Path
from types import SimpleNamespace

import pytest

from luthier import host, plots, tables
from test_run import command  # the run as a subprocess, its record removed

ROOT = Path(__file__).resolve().parents[1]

OBS = "x:float,y:float,g:str\n1.0,2.0,a\n2.0,3.5,b\n3.0,1.0,a\n4.0,2.5,b\n"
NOTES = "x:float,y:float,name:str\n1.5,3.0,first\n"


def table(text):
    return tables.parse(text)


def auto(e):
    return ("linear", ("auto", {"expand": e}))


def figure(obs=OBS, title="two tables", layers=None, canvas=(4.0, 3.0, 50.0), **parts):
    """A plot as it crosses the bridge: points coloured by g and a line over `obs`, a text over
    `notes`, linear scales with 5% expansion, a palette of two colours."""
    p = {"canvas": dict(zip(("width", "height", "dpi"), canvas)),
         "tables": [("obs", table(obs)), ("notes", table(NOTES))],
         "mapping": [("x", "x"), ("y", "y")],
         "layers": layers if layers is not None else [
             {"geom": ("points", {"size": 4.0}), "mapping": [("colour", "g")], "table": "obs"},
             {"geom": ("lines", {"width": 1.0}), "mapping": [], "table": "obs"},
             {"geom": ("texts", {"size": 8.0}), "mapping": [("label", "name")], "table": "notes"}],
         "scales": [("x", auto(0.05)), ("y", auto(0.05)), ("colour", ("palette", ["red", "blue"]))],
         "coord": ("cartesian", None), "facet": host.NOTHING,
         "labels": {"title": title, "x": "x", "y": "y"}}
    p.update(parts)
    return p


@pytest.mark.parametrize("ext", plots.FORMATS)
def test_two_renders_of_one_value_give_the_same_bytes(ext, tmp_path):
    # ImageOfTheValue (two plots that are samePlot, tables parsed twice) and rendersTheSame
    assert plots.image(figure(), ext) == plots.image(figure(), ext)
    plots.render(None, figure(), str(tmp_path / f"a.{ext}"))
    plots.render(None, figure(), str(tmp_path / f"b.{ext}"))
    assert (tmp_path / f"a.{ext}").read_bytes() == (tmp_path / f"b.{ext}").read_bytes()


def test_a_table_built_in_luthier_draws_as_the_parsed_one():
    # ImageOfTheValue across representations: the record tables.as_table reads, its cell giving
    # (label, value), is the same table as the parsed one, and draws the same bytes
    t = table(OBS)
    labels = {"int": "int", "float": "real", "str": "text"}
    built = SimpleNamespace(nRows=t.nRows, names=t.names, kinds=t.kinds,
                            cell=lambda c, r: (labels[t.kinds[t.index(c)]], t.rows[r][t.index(c)]) if c in t.names else None)
    p = figure()
    q = figure(tables=[("obs", built), ("notes", table(NOTES))])
    assert plots.image(p, "png") == plots.image(q, "png")


@pytest.mark.parametrize("ext", plots.FORMATS)
def test_a_permutation_of_the_rows_gives_the_same_bytes(ext):
    # RowOrderInvariant: every geometry draws its rows sorted (lines by group, colour, x)
    header, *rows = OBS.splitlines()
    permuted = "\n".join([header] + rows[::-1][1:] + rows[::-1][:1]) + "\n"
    assert permuted != OBS
    assert plots.image(figure(permuted), ext) == plots.image(figure(OBS), ext)


def test_swapping_two_layers_apart_gives_the_same_png():
    # LayerOrderInvariant, rasters only: the points of obs (x in 1..4) and the text of notes moved
    # to x = 9 are apart on x; the line across obs is dropped so that the two layers are adjacent
    notes = "x:float,y:float,name:str\n9.0,3.0,first\n"
    pts = {"geom": ("points", {"size": 4.0}), "mapping": [("colour", "g")], "table": "obs"}
    txt = {"geom": ("texts", {"size": 8.0}), "mapping": [("label", "name")], "table": "notes"}
    p = figure(layers=[pts, txt], tables=[("obs", table(OBS)), ("notes", table(notes))])
    q = figure(layers=[txt, pts], tables=[("obs", table(OBS)), ("notes", table(notes))])
    assert plots.image(p, "png") == plots.image(q, "png")
    # in an SVG the layers are elements in the order drawn: the bytes differ, not the picture
    assert plots.image(p, "svg") != plots.image(q, "svg")


@pytest.mark.parametrize("ext", plots.FORMATS)
def test_a_changed_title_changes_the_bytes(ext):
    # ImageSeesTheTitle, the negative control of the laws above
    assert plots.image(figure(title="two tables"), ext) != plots.image(figure(title="two tablez"), ext)
    assert plots.image(figure(title=""), ext) != plots.image(figure(title="t"), ext)


@pytest.mark.parametrize("ext", plots.FORMATS)
def test_the_format_is_the_extension(ext):
    # FormatByExtension
    assert plots.format_of(plots.image(figure(), ext)) == ext


def test_format_of_reads_only_the_signature_or_the_root():
    assert plots.format_of("") == ""
    assert plots.format_of("<html></html>") == ""
    assert plots.format_of("<svgx/>") == ""
    assert plots.format_of('<?xml version="1.0"?>\n<!-- c -->\n<!DOCTYPE svg>\n<svg xmlns="x"/>') == "svg"


@pytest.mark.parametrize("ext", plots.FORMATS)
def test_the_file_after_render_is_the_image_as_observe_reads_it(ext, tmp_path):
    # FileExistsAfter, and the reading `agreement` compares (host.observe, one character per byte
    # for a PNG)
    path = str(tmp_path / f"plot.{ext}")
    assert plots.render("w", figure(), path) == ("w", None)
    _, state = host.observe("w", [path])
    assert state["files"] == [(path, plots.image(figure(), ext))]
    _, read = host.read_file("w", path)
    assert read.value == plots.image(figure(), ext)


def test_render_refuses_an_extension_outside_the_formats(tmp_path):
    with pytest.raises(ValueError, match="png, svg"):
        plots.render(None, figure(), str(tmp_path / "plot.pdf"))
    with pytest.raises(ValueError):
        plots.render(None, figure(), str(tmp_path / "plot"))
    assert list(tmp_path.iterdir()) == []


def test_the_axes_are_at_the_resolved_limits():
    # LimitsContainTheData: the host draws at resolvedLimits, not limits of its own. obs spans
    # x 1..4 and notes x 1.5, so x is 1 - 0.15 .. 4 + 0.15; y is stated
    p = figure(scales=[("x", auto(0.05)), ("y", ("linear", ("stated", {"lo": 0.0, "hi": 10.0}))),
                       ("colour", ("palette", ["red", "blue"]))])
    with plots._settings():
        ax = plots._figure(plots._Plot(p)).axes[0]
        assert ax.get_xlim() == pytest.approx((0.85, 4.15)) and ax.get_ylim() == (0.0, 10.0)


@pytest.mark.parametrize("parts, law", [
    ({"canvas": (0.0, 3.0, 50.0)}, "CanvasPositive"),
    ({"mapping": [("x", "x"), ("yy", "y")]}, "AestheticsKnown"),
    ({"scales": [("x", auto(0.05)), ("colour", ("palette", ["red", "blue"]))]}, "ScalesStated"),
    ({"scales": [("x", auto(0.05)), ("y", auto(0.05)), ("colour", ("palette", ["red"]))]}, "PaletteCoversLevels"),
    ({"scales": [("x", auto(0.05)), ("y", ("log", ("auto", {"expand": 0.5}))),
                 ("colour", ("palette", ["red", "blue"]))]}, "ScaleLimitsWellFormed"),
    ({"facet": host.Just("nope")}, "FacetIsAColumn"),
])
def test_a_plot_not_well_formed_is_refused_with_the_law(parts, law):
    with pytest.raises(plots.NotWellFormed, match=law):
        plots.image(figure(**parts), "png")


def test_the_plots_mapping_reaches_only_what_a_layer_draws():
    # aesOf, ggplot's inheritance: the plot maps label to a column obs lacks; the points do not
    # draw label, so the plot is well formed; a text over obs inherits it and is refused
    mapping = [("x", "x"), ("y", "y"), ("label", "nope")]
    pts = {"geom": ("points", {"size": 4.0}), "mapping": [], "table": "obs"}
    assert plots.check(figure(mapping=mapping, layers=[pts], scales=[("x", auto(0.05)), ("y", auto(0.05))])) is None
    txt = {"geom": ("texts", {"size": 8.0}), "mapping": [], "table": "obs"}
    assert plots.check(figure(mapping=mapping, layers=[pts, txt],
                              scales=[("x", auto(0.05)), ("y", auto(0.05))])) == "AestheticsAreColumns"


def test_every_geometry_and_facets_draw():
    obs = "x:float,y:float,xe:float,ye:float,g:str,f:int\n1.0,2.0,0.1,0.2,a,0\n2.0,3.0,0.2,0.1,b,1\n3.0,1.5,0.1,0.1,a,1\n"
    layers = [
        {"geom": ("errorbars", {"width": 1.0}), "mapping": [("yerr", "ye"), ("xerr", "xe")], "table": "obs"},
        {"geom": ("ellipses", {"level": 2.0, "width": 1.0}), "mapping": [("xerr", "xe"), ("yerr", "ye")], "table": "obs"},
        {"geom": ("segments", {"width": 1.0}), "mapping": [("xend", "y"), ("yend", "x")], "table": "obs"},
        {"geom": ("ablines", {"intercept": 0.0, "slope": 1.0, "width": 0.5}), "mapping": [], "table": ""},
        {"geom": ("lines", {"width": 1.0}), "mapping": [("group", "g"), ("colour", "g")], "table": "obs"}]
    for coord, ys in (("cartesian", auto(0.05)), ("equal", auto(0.05))):
        p = figure(obs, layers=layers, facet=host.Just("f"), coord=(coord, None),
                   scales=[("x", auto(0.05)), ("y", ys), ("colour", ("palette", ["red", "blue"]))])
        assert plots.check(p) is None
        for ext in plots.FORMATS:
            assert plots.format_of(plots.image(p, ext)) == ext
    logs = figure(scales=[("x", ("log", ("auto", {"expand": 1.1}))), ("y", ("log", ("auto", {"expand": 1.1}))),
                          ("colour", ("palette", ["red", "blue"]))],
                  layers=figure()["layers"] + [layers[3]])
    assert plots.format_of(plots.image(logs, "png")) == "png"


def test_the_renderer_reports_its_version():
    assert plots.version().startswith("matplotlib ")


# ---------------------------------------------------------------- a Plot built in Luthier, run

def test_a_plot_of_two_tables_built_in_luthier_renders_through_luthier_run(tmp_path):
    # The run reads the stores of the files it loads (12.S17): the laws of matplotlibDrawing and
    # of files, certified by tests/tester/plot_laws.lut. What the program builds (a Plot of two
    # tables parsed by csv, the canvas, the layers' sums) crosses and draws what the host draws
    # from the same plot written in Python.
    obs = "x:float,y:float\n1.0,2.0\n2.0,3.5\n3.0,1.0\n"
    (tmp_path / "obs.csv").write_text(obs, encoding="utf-8")
    (tmp_path / "notes.csv").write_text(NOTES, encoding="utf-8")
    result = command(ROOT / "tests/run/plot_two_tables.lut", cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, "rendered\n", "")
    p = figure(obs, layers=[
        {"geom": ("points", {"size": 4.0}), "mapping": [], "table": "obs"},
        {"geom": ("lines", {"width": 1.0}), "mapping": [], "table": "obs"},
        {"geom": ("texts", {"size": 8.0}), "mapping": [("label", "name")], "table": "notes"}],
        scales=[("x", auto(0.05)), ("y", auto(0.05))])
    assert (tmp_path / "plot.png").read_bytes() == plots.image_bytes(p, "png")
    assert (tmp_path / "plot.svg").read_bytes() == plots.image_bytes(p, "svg")
