"""The host's renderer, the model of plot.lth's `Drawing` and `Renderer` (plot_model.lut).

Derivation: brief record/IA/plots-2026-10-15/prompt-host.md (step 2 of
record/plan/plots/plan-plots-2026-10-14-execution.md), on plot.lth at c6febf0 (the canvas) and
plot_model.lut at bc25d58. Drawn with matplotlib: the Agg canvas for PNG, the SVG backend for
SVG, both on a `matplotlib.figure.Figure` (never pyplot's global state).

What crosses (run.py's bridge, plot_model.lut's header): a `Plot` is a record (a dict with
attributes); a table is tables.py's `Table` or the record `tables.as_table` reads; a mapping a
list of pairs; a geometry, a scale, limits and coordinates the pair `(label, value)`; `facet`
`host.NOTHING` or `host.Just(column)` (None is read as nothing too, for callers in Python).

How each law of plot.lth is met:
- `wellFormed` (§4): `check` evaluates its fifteen laws here, with `aes_of` ggplot's inheritance
  as `aesOf` states it, and `image` refuses a plot that breaks one, naming the law.
- `LimitsContainTheData`: the axes are drawn exactly at `resolvedLimits` (`resolved_limits`
  here), autoscale off, no margins.
- `ImageOfTheValue`, `rendersTheSame`: no timestamp (`metadata={'Date': None}`), a fixed
  `svg.hashsalt`, `rcdefaults` inside an `rc_context`, one bundled font (DejaVu Sans), text drawn
  as paths in SVG; nothing read from the clock or the environment.
- `RowOrderInvariant`: every geometry draws its rows sorted by their mapped values (`lines` by
  group, colour, then x); colour levels, legend entries and facet panels in sorted order.
- `LayerOrderInvariant` (rasters): layer i is drawn at z-order 2 + i, so the layers are drawn in
  list order, a later one over an earlier one, and nothing else depends on that order.
- `ImageSeesTheTitle`: the title is drawn always (`suptitle`), even when empty.
- `FormatByExtension`: `format_of` reads the PNG signature or an SVG root.
- `FileExistsAfter`: `render` writes the bytes whose reading is `image(plot, ext)`.

The content as a string (plot.lth §5, [proposed] there: one character per byte): `image` reads
the bytes as `host.text_of_bytes` does, the reading `observe` and `read_file` share, so that
world.lth's `agreement` compares like with like. That is UTF-8 when the bytes are valid UTF-8
and Latin-1 (one character per byte) otherwise: a PNG is never valid UTF-8 (its second byte of
signature, 0x89 first, cannot start a UTF-8 sequence), so a PNG is one character per byte; an
SVG is text, and read as text, which coincides with one character per byte while its content is
ASCII (a title outside ASCII is where the two readings differ; this module keeps the host's).
"""
from __future__ import annotations

import io
import math
from contextlib import contextmanager

from . import host, tables

try:
    import matplotlib
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.backends.backend_svg import FigureCanvasSVG
    from matplotlib.collections import LineCollection
    from matplotlib.figure import Figure
    from matplotlib.patches import Ellipse, Patch
except ImportError:  # pragma: no cover - matplotlib is installed where this was written
    matplotlib = None

FORMATS = ("png", "svg")
KNOWN_AESTHETICS = ("x", "y", "xend", "yend", "xerr", "yerr", "colour", "size", "group", "label")
NUMERIC_AESTHETICS = ("x", "y", "xend", "yend", "xerr", "yerr", "size")
NEEDS = {"points": ("x", "y"), "lines": ("x", "y"), "errorbars": ("x", "y", "yerr"),
         "ellipses": ("x", "y", "xerr", "yerr"), "texts": ("x", "y", "label"),
         "segments": ("x", "y", "xend", "yend"), "ablines": ()}
MAY_DRAW = {"points": ("colour", "size"), "lines": ("colour", "group"), "errorbars": ("xerr", "colour"),
            "ellipses": ("colour",), "texts": ("colour",), "segments": ("colour",), "ablines": ()}

# the renderer's fixed settings: what would otherwise come from the user's matplotlibrc or the
# clock. [proposed] The font is matplotlib's bundled DejaVu Sans, so no system font is looked up.
FIXED_RC = {"svg.hashsalt": "luthier", "svg.fonttype": "path", "font.family": "DejaVu Sans",
            "axes.xmargin": 0.0, "axes.ymargin": 0.0}
# [proposed] what an unmapped colour draws in (ggplot's default for points, lines and text)
UNMAPPED_COLOUR = "black"


class NotWellFormed(ValueError):
    """A plot that breaks a law of plot.lth §4; `law` is its name."""
    def __init__(self, law):
        self.law = law
        super().__init__(f"the plot is not well formed: {law} (plot.lth §4)")


def version():
    """The drawing library's version, for the run's record (plot.lth §5: the renderer's version is
    its routes' identity with the version of the library the host reports)."""
    return f"matplotlib {matplotlib.__version__}" if matplotlib is not None else "none"


# ------------------------------------------------------------------ reading what crosses

def _field(x, name):
    return x[name] if isinstance(x, dict) else getattr(x, name)


def _maybe(m):
    if m is None or m is host.NOTHING:
        return None
    return m.value if isinstance(m, host.Just) else m


def _sum(x):
    """A labeled sum as `(label, value)`."""
    label, value = x
    return label, value


class _Plot:
    """The plot as this module reads it: its parts in Python's terms, the tables as tables.Table."""
    def __init__(self, p):
        cv = _field(p, "canvas")
        self.width, self.height, self.dpi = (float(_field(cv, k)) for k in ("width", "height", "dpi"))
        self.tables = [(n, tables.as_table(t)) for n, t in _field(p, "tables")]
        self.mapping = [tuple(m) for m in _field(p, "mapping")]
        self.layers = []
        for layer in _field(p, "layers"):
            label, params = _sum(_field(layer, "geom"))
            self.layers.append({"geom": label, "params": params, "mapping": [tuple(m) for m in _field(layer, "mapping")],
                                "table": _field(layer, "table")})
        self.scales = [(a, _sum(s)) for a, s in _field(p, "scales")]
        self.coord = _sum(_field(p, "coord"))[0]
        self.facet = _maybe(_field(p, "facet"))
        lab = _field(p, "labels")
        self.title, self.xlab, self.ylab = (_field(lab, k) for k in ("title", "x", "y"))


def _lookup(pairs, key):
    for k, v in pairs:
        if k == key:
            return v
    return None


def _p(params, name):
    return float(_field(params, name))


# ------------------------------------------------------------------ plot.lth §3, reading a plot

def draws(geom):
    return NEEDS[geom] + MAY_DRAW[geom]


def aes_of(p, layer, a):
    """plot.lth `aesOf`: the layer's own mapping first, then the plot's, the plot's only for an
    aesthetic the layer's geometry draws (ggplot's inheritance)."""
    c = _lookup(layer["mapping"], a)
    if c is not None:
        return c
    return _lookup(p.mapping, a) if a in draws(layer["geom"]) else None


def _table(p, name):
    return _lookup(p.tables, name)


def _kind(t, c):
    return dict(t.columns).get(c)


def _num(t, c, r):
    """`numOf`: the cell as a number when its column is one."""
    if c is None or _kind(t, c) not in ("float", "int"):
        return None
    return float(t.rows[r][t.index(c)])


def _reach(layer):
    if layer["geom"] == "errorbars":
        return 1.0
    if layer["geom"] == "ellipses":
        return _p(layer["params"], "level")
    return 0.0


def _union(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return (min(a[0], b[0]), max(a[1], b[1]))


_END = {"x": "xend", "y": "yend"}
_ERR = {"x": "xerr", "y": "yerr"}


def _row_range(p, layer, t, a, r):
    end = _num(t, aes_of(p, layer, _END.get(a, "")), r)
    out = None if end is None else (end, end)
    v = _num(t, aes_of(p, layer, a), r)
    if v is None:
        return _union(out, None)
    e = _num(t, aes_of(p, layer, _ERR.get(a, "")), r)
    if e is None:
        return _union(out, (v, v))
    k = _reach(layer)
    return _union(out, _union((v - k * e, v - k * e), (v + k * e, v + k * e)))


def layer_range(p, layer, a):
    t = _table(p, layer["table"])
    if t is None:
        return None
    out = None
    for r in range(t.nRows):
        out = _union(out, _row_range(p, layer, t, a, r))
    return out


def data_range(p, a):
    out = None
    for layer in p.layers:
        out = _union(out, layer_range(p, layer, a))
    return out


def _limits_from(is_log, limits, d):
    label, value = limits
    if label == "stated":
        return (_p(value, "lo"), _p(value, "hi"))
    if d is None:
        return None
    e = _p(value, "expand")
    if is_log:
        return (d[0] / e, d[1] * e)
    return (d[0] - e * (d[1] - d[0]), d[1] + e * (d[1] - d[0]))


def resolved_limits(p, a):
    """plot.lth `resolvedLimits`: where the host draws an aesthetic, never limits of its own."""
    s = _lookup(p.scales, a)
    if s is None or s[0] == "palette":
        return None
    return _limits_from(s[0] == "log", s[1], data_range(p, a))


def _cell_key(t, c, r):
    """A cell as (kind, value), the identity `sameCell` compares."""
    return (_kind(t, c), t.rows[r][t.index(c)])


def _sort_key(v):
    """Sorted levels: numbers before strings, each in its natural order."""
    return (1, v, 0.0) if isinstance(v, str) else (0, "", float(v))


# ------------------------------------------------------------------ plot.lth §4, the laws

def _aesthetics_known(p):
    return all(a in KNOWN_AESTHETICS for a, _ in p.mapping) and \
        all(a in KNOWN_AESTHETICS for layer in p.layers for a, _ in layer["mapping"])


def _scale_kind(p, a):
    s = _lookup(p.scales, a)
    return "" if s is None else s[0]


def _palette_length(p):
    s = _lookup(p.scales, "colour")
    return len(s[1]) if s is not None and s[0] == "palette" else 0


def _column_fits(p, layer, a):
    c = aes_of(p, layer, a)
    if c is None:
        return True
    t = _table(p, layer["table"])
    if t is None:
        return False
    return _kind(t, c) in ("float", "int") if a in NUMERIC_AESTHETICS else c in t.names


def _geom_positive(layer):
    g, ps = layer["geom"], layer["params"]
    names = {"points": ("size",), "lines": ("width",), "errorbars": ("width",), "ellipses": ("level", "width"),
             "texts": ("size",), "segments": ("width",), "ablines": ("width",)}[g]
    return all(_p(ps, n) > 0.0 for n in names)


def _limits_well_formed(is_log, limits):
    label, value = limits
    if label == "stated":
        lo, hi = _p(value, "lo"), _p(value, "hi")
        return lo < hi and (not is_log or lo > 0.0)
    e = _p(value, "expand")
    return e >= 1.0 if is_log else e >= 0.0


def _scale_well_formed(s):
    if s[0] == "palette":
        return len(s[1]) > 0
    return _limits_well_formed(s[0] == "log", s[1])


def _limits_contain(p, a, limits):
    if limits[0] == "stated":
        return True
    g, d = resolved_limits(p, a), data_range(p, a)
    return g is not None and g[0] < g[1] and d is not None and g[0] <= d[0] and d[1] <= g[1]


def _levels(t, c):
    return len({_cell_key(t, c, r) for r in range(t.nRows)})


def _maps_colour(p):
    return any(aes_of(p, layer, "colour") is not None for layer in p.layers)


LAWS = (
    ("CanvasPositive", lambda p: p.width > 0.0 and p.height > 0.0 and p.dpi > 0.0),
    ("AestheticsKnown", _aesthetics_known),
    ("TablesNamedOnce", lambda p: len({n for n, _ in p.tables}) == len(p.tables)),
    ("LayersNameTheirTables", lambda p: all(not NEEDS[l["geom"]] or _table(p, l["table"]) is not None for l in p.layers)),
    ("LayerMapsWhatItDraws", lambda p: all(a in draws(l["geom"]) for l in p.layers for a, _ in l["mapping"])),
    ("NeedsMapped", lambda p: all(aes_of(p, l, a) is not None for l in p.layers for a in NEEDS[l["geom"]])),
    ("AestheticsAreColumns", lambda p: all(_column_fits(p, l, a) for l in p.layers for a in draws(l["geom"]))),
    ("GeometryParametersPositive", lambda p: all(_geom_positive(l) for l in p.layers)),
    ("ScalesStated", lambda p: (not p.layers or (_lookup(p.scales, "x") is not None and _lookup(p.scales, "y") is not None))
     and (not _maps_colour(p) or _lookup(p.scales, "colour") is not None)),
    ("ScalesFitTheirAesthetics", lambda p: all((a == "colour") == (s[0] == "palette") and a in ("x", "y", "colour")
                                               for a, s in p.scales)),
    ("ScaleLimitsWellFormed", lambda p: all(_scale_well_formed(s) for _, s in p.scales)),
    ("LimitsContainTheData", lambda p: all(s[0] == "palette" or _limits_contain(p, a, s[1]) for a, s in p.scales)),
    ("LogScaleOnPositiveData", lambda p: all(s[0] != "log" or (lambda d: d is None or d[0] > 0.0)(data_range(p, a))
                                             for a, s in p.scales)),
    ("PaletteCoversLevels", lambda p: all(
        aes_of(p, l, "colour") is None or _table(p, l["table"]) is None
        or _levels(_table(p, l["table"]), aes_of(p, l, "colour")) <= _palette_length(p) for l in p.layers)),
    ("FacetIsAColumn", lambda p: p.facet is None or any(
        _table(p, l["table"]) is not None and p.facet in _table(p, l["table"]).names for l in p.layers)),
    ("CoordFitsScales", lambda p: p.coord == "cartesian" or _scale_kind(p, "x") == _scale_kind(p, "y")),
)


def check(plot):
    """The first law of plot.lth §4 the plot breaks, in the order `wellFormed` conjoins them, or
    None. Evaluated as `wellFormed` is, left to right and stopping at the first that fails: a later
    law may read what an earlier one guards (a colour column that is a column of its table)."""
    p = plot if isinstance(plot, _Plot) else _Plot(plot)
    return next((name for name, law in LAWS if not law(p)), None)


# ------------------------------------------------------------------ drawing

@contextmanager
def _settings():
    with matplotlib.rc_context():
        matplotlib.rcdefaults()
        matplotlib.rcParams.update(FIXED_RC)
        yield


def _show(v):
    if isinstance(v, str):
        return v
    if isinstance(v, float):
        return repr(v)
    return str(v)


class _Colours:
    """The palette assigned to the sorted levels of the colour columns of every layer that maps
    colour. [proposed] One assignment over all layers, so a level has one colour in every layer;
    the law `PaletteCoversLevels` counts levels per layer, so a palette shorter than the union of
    levels repeats colours (taken modulo its length)."""
    def __init__(self, p):
        levels = set()
        columns = set()
        for layer in p.layers:
            c, t = aes_of(p, layer, "colour"), _table(p, layer["table"])
            if c is not None and t is not None:
                columns.add(c)
                levels.update(t.rows[r][t.index(c)] for r in range(t.nRows))
        self.levels = sorted(levels, key=_sort_key)
        self.title = ", ".join(sorted(columns))
        s = _lookup(p.scales, "colour")
        self.palette = list(s[1]) if s is not None and s[0] == "palette" else []
        self.index = {v: k for k, v in enumerate(self.levels)}

    def of(self, value):
        if value is None or not self.palette:
            return UNMAPPED_COLOUR
        return self.palette[self.index[value] % len(self.palette)]


def _rows(p, layer, t, level):
    """The rows a panel draws of a layer's table: all, or those at the facet's level when the table
    has the facet's column (a table without it is drawn in every panel)."""
    rows = range(t.nRows)
    if p.facet is not None and level is not None and p.facet in t.names:
        k = t.index(p.facet)
        rows = [r for r in rows if t.rows[r][k] == level]
    return list(rows)


def _value(p, layer, t, a, r):
    c = aes_of(p, layer, a)
    return None if c is None else t.rows[r][t.index(c)]


def _canonical(p, layer, t, rows, order):
    """The rows sorted by their mapped values, aesthetics in `order` (plot.lth §5: the image does not
    depend on the order of the rows)."""
    def key(r):
        return tuple(_sort_key(v) if v is not None else (-1, "", 0.0)
                     for v in (_value(p, layer, t, a, r) for a in order))
    return sorted(rows, key=key)


def _draw_layer(ax, p, layer, z, colours, level):
    g, ps = layer["geom"], layer["params"]
    if g == "ablines":
        _draw_abline(ax, p, ps, z)
        return
    t = _table(p, layer["table"])
    rows = _rows(p, layer, t, level)
    num = lambda a, r: _num(t, aes_of(p, layer, a), r)
    colour = lambda r: colours.of(_value(p, layer, t, "colour", r))
    if g == "points":
        rows = _canonical(p, layer, t, rows, ("x", "y", "colour", "size"))
        size = _p(ps, "size")
        sizes = [(num("size", r) if aes_of(p, layer, "size") else size) ** 2 for r in rows]
        ax.scatter([num("x", r) for r in rows], [num("y", r) for r in rows], s=sizes,
                   c=[colour(r) for r in rows], marker="o", linewidths=0, zorder=z)
    elif g == "lines":
        rows = _canonical(p, layer, t, rows, ("group", "colour", "x", "y"))
        groups = {}
        for r in rows:
            groups.setdefault((_value(p, layer, t, "group", r), _value(p, layer, t, "colour", r)), []).append(r)
        for (_, col), rs in groups.items():  # in sorted order: rows were sorted by group, colour
            ax.plot([num("x", r) for r in rs], [num("y", r) for r in rs], color=colours.of(col),
                    linewidth=_p(ps, "width"), zorder=z)
    elif g in ("errorbars", "segments"):
        rows = _canonical(p, layer, t, rows, ("x", "y", "xend", "yend", "xerr", "yerr", "colour"))
        segs, cols = [], []
        for r in rows:
            x, y = num("x", r), num("y", r)
            if g == "segments":
                segs.append([(x, y), (num("xend", r), num("yend", r))])
                cols.append(colour(r))
                continue
            e = num("yerr", r)
            segs.append([(x, y - e), (x, y + e)])
            cols.append(colour(r))
            if aes_of(p, layer, "xerr") is not None:
                e = num("xerr", r)
                segs.append([(x - e, y), (x + e, y)])
                cols.append(colour(r))
        ax.add_collection(LineCollection(segs, colors=cols, linewidths=_p(ps, "width"), zorder=z), autolim=False)
    elif g == "ellipses":
        rows = _canonical(p, layer, t, rows, ("x", "y", "xerr", "yerr", "colour"))
        k = _p(ps, "level")
        for r in rows:
            ax.add_patch(Ellipse((num("x", r), num("y", r)), 2 * k * num("xerr", r), 2 * k * num("yerr", r),
                                 fill=False, edgecolor=colour(r), linewidth=_p(ps, "width"), zorder=z))
    elif g == "texts":
        rows = _canonical(p, layer, t, rows, ("x", "y", "label", "colour"))
        for r in rows:
            ax.text(num("x", r), num("y", r), _show(_value(p, layer, t, "label", r)), fontsize=_p(ps, "size"),
                    color=colour(r), ha="center", va="center", zorder=z, clip_on=True)
    else:
        raise ValueError(f"unknown geometry {g}")


def _draw_abline(ax, p, ps, z):
    """y = intercept + slope x across the panel's x limits; on a log axis, sampled at one point per
    pixel column of the canvas (no constant of its own)."""
    a, b = _p(ps, "intercept"), _p(ps, "slope")
    lo, hi = ax.get_xlim()
    if ax.get_xscale() == "linear" and ax.get_yscale() == "linear":
        xs = [lo, hi]
    else:
        n = max(2, int(math.ceil(p.width * p.dpi)) + 1)
        if ax.get_xscale() == "log":
            xs = [lo * (hi / lo) ** (k / (n - 1)) for k in range(n)]
        else:
            xs = [lo + (hi - lo) * k / (n - 1) for k in range(n)]
    ys = [a + b * x for x in xs]
    if ax.get_yscale() == "log":
        pts = [(x, y) for x, y in zip(xs, ys) if y > 0.0]
        xs, ys = [x for x, _ in pts], [y for _, y in pts]
    ax.plot(xs, ys, color=UNMAPPED_COLOUR, linewidth=_p(ps, "width"), zorder=z)


def _facet_levels(p):
    if p.facet is None:
        return [None]
    levels = set()
    for name, t in p.tables:
        if p.facet in t.names and any(l["table"] == name for l in p.layers):
            k = t.index(p.facet)
            levels.update(row[k] for row in t.rows)
    return sorted(levels, key=_sort_key)


def _figure(p):
    fig = Figure(figsize=(p.width, p.height), dpi=p.dpi, layout="constrained")
    levels = _facet_levels(p)
    ncol = int(math.ceil(math.sqrt(len(levels))))
    nrow = int(math.ceil(len(levels) / ncol))
    axes = fig.subplots(nrow, ncol, squeeze=False, sharex=True, sharey=True)
    colours = _Colours(p)
    xlim, ylim = resolved_limits(p, "x"), resolved_limits(p, "y")
    for k, ax in enumerate(axes.flat):
        if k >= len(levels):
            ax.set_axis_off()
            continue
        level = levels[k]
        ax.set_autoscale_on(False)
        ax.margins(0.0)
        if _scale_kind(p, "x") == "log":
            ax.set_xscale("log")
        if _scale_kind(p, "y") == "log":
            ax.set_yscale("log")
        if xlim is not None:
            ax.set_xlim(*xlim)
        if ylim is not None:
            ax.set_ylim(*ylim)
        if p.coord == "equal":
            ax.set_aspect("equal", adjustable="box")
        if level is not None:
            ax.set_title(_show(level))
        for i, layer in enumerate(p.layers):
            _draw_layer(ax, p, layer, 2 + i, colours, level)
        ax.set_autoscale_on(False)
    fig.supxlabel(p.xlab)
    fig.supylabel(p.ylab)
    fig.suptitle(p.title)  # always drawn (ImageSeesTheTitle)
    if colours.levels and colours.palette:
        handles = [Patch(color=colours.of(v), label=_show(v)) for v in colours.levels]
        fig.legend(handles=handles, title=colours.title, loc="outside right upper")
    return fig


def image_bytes(plot, ext):
    """The file's bytes: the plot drawn in the format `ext`; a plot that breaks a law of plot.lth §4
    is refused with the law's name."""
    if matplotlib is None:
        raise RuntimeError("matplotlib is not installed")
    if ext not in FORMATS:
        raise ValueError(f"the renderer writes {', '.join(FORMATS)}, not {ext!r}")
    p = _Plot(plot)
    broken = check(p)
    if broken is not None:
        raise NotWellFormed(broken)
    with _settings():
        fig = _figure(p)
        canvas = (FigureCanvasAgg if ext == "png" else FigureCanvasSVG)(fig)
        buf = io.BytesIO()
        metadata = {"Software": None} if ext == "png" else {"Date": None}
        fig.savefig(buf, format=ext, dpi=p.dpi, metadata=metadata)
        del canvas
    return buf.getvalue()


def image(plot, ext):
    """plot_model.lut `image`: `Plot -> String -> String`, the file's content as the host reads a
    file (`host.text_of_bytes`)."""
    return host.text_of_bytes(image_bytes(plot, ext))


def format_of(content):
    """plot_model.lut `formatOf`: "png" for the PNG signature, "svg" for a document whose root is
    an `svg` element (after an XML declaration, comments and a doctype), "" otherwise."""
    if content.startswith("\x89PNG\r\n\x1a\n"):
        return "png"
    s = content.lstrip()
    while True:
        if s.startswith("<?"):
            end = s.find("?>")
        elif s.startswith("<!--"):
            end = s.find("-->")
        elif s.startswith("<!"):
            end = s.find(">")
        else:
            break
        if end < 0:
            return ""
        s = s[s.index(">", end) + 1:].lstrip()
    if s.startswith("<svg") and len(s) > 4 and (s[4].isspace() or s[4] in ">/"):
        return "svg"
    return ""


def extension(path):
    """What follows the path's last ".", "" when its last part has none."""
    name = path.replace("\\", "/").rsplit("/", 1)[-1]
    return name.rsplit(".", 1)[1] if "." in name else ""


def render(w, plot, path):
    """plot_model.lut `render`: `W -> Plot -> String -> W * Unit`, the bytes whose reading is
    `image(plot, ext)` written at `path`, `ext` the path's extension; a path whose extension is not
    among the formats is refused, and nothing is written."""
    ext = extension(path)
    if ext not in FORMATS:
        raise ValueError(f"the renderer writes {', '.join(FORMATS)}; the path {path!r} has extension {ext!r}")
    data = image_bytes(plot, ext)
    with open(path, "wb") as f:
        f.write(data)
    return w, None
