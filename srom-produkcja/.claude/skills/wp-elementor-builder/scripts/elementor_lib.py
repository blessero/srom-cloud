"""
elementor_lib.py — building blocks for generating Elementor JSON.

Import this into a project-specific generator rather than hand-writing JSON.
Everything here is globals-first and uses the verified dynamic-tag encoding.

    from elementor_lib import *

    COLORS = {"#211E1B": "ink", "#DF261E": "accent"}   # hex → global id
    set_color_map(COLORS)

    doc = document("Home", [
        band([heading("Title", "h1", font="primary", color="#211E1B")]),
    ])
"""
from __future__ import annotations
import itertools, json
from urllib.parse import quote

# ---------------------------------------------------------------- IDS
_counter = itertools.count(1)
def eid() -> str:
    """Deterministic 7-char id so re-runs diff cleanly."""
    return format(next(_counter) + 0x1000000, "x")[-7:]

# ---------------------------------------------------------------- PRIMITIVES
def px(n):  return {"unit": "px", "size": n, "sizes": []}
def pct(n): return {"unit": "%",  "size": n, "sizes": []}
def em(n):  return {"unit": "em", "size": n, "sizes": []}

def dim(t, r, b, l, unit="px", linked=False):
    return {"unit": unit, "top": str(t), "right": str(r),
            "bottom": str(b), "left": str(l), "isLinked": linked}

def gap(col, row, unit="px"):
    return {"unit": unit, "size": str(col), "column": str(col),
            "row": str(row), "isLinked": col == row}

def link(url, external=None):
    if external is None:
        external = not str(url).startswith("#")
    return {"url": url, "is_external": "on" if external else "",
            "nofollow": "", "custom_attributes": ""}

def fa_solid(name): return {"value": f"fas fa-{name}", "library": "fa-solid"}
def fa_brand(name): return {"value": f"fab fa-{name}", "library": "fa-brands"}

# ---------------------------------------------------------------- GLOBALS
_COLOR_MAP: dict[str, str] = {}

def set_color_map(mapping: dict[str, str]) -> None:
    """hex → global colour id. Lets call sites stay readable while emitting globals."""
    _COLOR_MAP.clear()
    _COLOR_MAP.update(mapping)

def gc(cid):  return f"globals/colors?id={cid}"
def gt(tid):  return f"globals/typography?id={tid}"

def cgid(color):
    """Resolve a hex (or a bare global id) to a global colour id, or None."""
    if not color:
        return None
    return _COLOR_MAP.get(color) if color.startswith("#") else color

def _cglobal(control, color):
    g = cgid(color)
    return {control: gc(g)} if g else {}

# ---------------------------------------------------------------- DYNAMIC TAGS
# elementor/core/dynamic-tags/manager.php
#   write: urlencode( wp_json_encode( $settings, JSON_FORCE_OBJECT ) )
#   read:  json_decode( urldecode( $settings ), true )
# Empty settings is %7B%7D. NEVER base64 (e30%3D) — it decodes to null → WP fatal.
def tag(name, settings=None) -> str:
    payload = json.dumps(settings, separators=(",", ":"), ensure_ascii=False) if settings else "{}"
    return f'[elementor-tag id="{eid()}" name="{name}" settings="{quote(payload, safe="")}"]'

def native(name):    return tag(name)                       # post-title, post-featured-image…
def cf(meta_key):    return tag("post-custom-field", {"key": meta_key})

# ---------------------------------------------------------------- ELEMENTS
def container(settings=None, elements=None, isInner=False, _id=None):
    s = {"content_width": "boxed"}
    if settings:
        s.update(settings)
    return {"id": _id or eid(), "elType": "container", "isInner": isInner,
            "settings": s, "elements": elements or []}

def widget(widget_type, settings=None, _id=None):
    return {"id": _id or eid(), "elType": "widget", "isInner": False,
            "settings": settings or {}, "elements": [], "widgetType": widget_type}

def _merge(s, globals_=None, dynamic=None):
    if globals_:
        s.setdefault("__globals__", {}).update(globals_)
    if dynamic:
        s.setdefault("__dynamic__", {}).update(dynamic)
    return s

# ---------------------------------------------------------------- LAYOUT
def row(children, gcol=40, grow=40, align="flex-start", wrap="wrap",
        justify=None, classes="", extra=None):
    s = {"content_width": "full", "flex_direction": "row",
         "flex_gap": gap(gcol, grow), "flex_wrap": wrap, "flex_align_items": align}
    if justify: s["flex_justify_content"] = justify
    if classes: s["css_classes"] = classes   # containers use the bare name; only widgets take _css_classes
    if extra:   s.update(extra)
    return container(s, children)

def col(children, width=None, grow=16, align=None, classes="", extra=None):
    s = {"content_width": "full", "flex_direction": "column", "flex_gap": gap(0, grow)}
    if width:   s["width"] = pct(width)
    if align:   s["flex_align_items"] = align
    if classes: s["css_classes"] = classes   # containers use the bare name; only widgets take _css_classes
    if extra:   s.update(extra)
    return container(s, children)

def band(children, bg=None, border=None, pad=(56, 20, 40, 20), _id=None,
         direction="column", gcol=40, grow=22):
    """Full-bleed outer + boxed inner.

    Required, not redundant: a boxed container's background/border stop at the
    boxed width, so the outer is the only way to run an edge-to-edge band or
    hairline rule while keeping content centred at the site width.
    direction="row" makes the boxed inner the flex row, avoiding a dead wrapper.
    """
    inner_s = {"content_width": "boxed", "flex_direction": direction,
               "padding": dim(0, pad[1], 0, pad[3])}
    inner_s["flex_gap"] = gap(gcol, grow) if direction == "row" else gap(0, grow)
    if direction == "row":
        inner_s["flex_wrap"] = "wrap"
        inner_s["flex_align_items"] = "flex-start"

    outer = {"content_width": "full", "flex_direction": "column",
             "padding": dim(pad[0], 0, pad[2], 0)}
    if bg:
        outer["background_background"] = "classic"
        _merge(outer, _cglobal("background_color", bg))
    if border:
        outer["border_border"] = "solid"
        outer["border_width"] = dim(0, 0, 1, 0)
        _merge(outer, _cglobal("border_color", border))
    if _id:
        outer["_element_id"] = _id
    return container(outer, [container(inner_s, children)])

# ---------------------------------------------------------------- WIDGETS
_TAG_FONT = {"h1": "primary", "h2": "secondary", "h3": "secondary"}

def heading(text_str, tag_="h2", font=None, color=None, classes="",
            bind=None, bind_link=None, extra=None):
    s = {"title": text_str, "header_size": tag_}
    g = {"typography_typography": gt(font or _TAG_FONT.get(tag_, "secondary"))}
    g.update(_cglobal("title_color", color))
    d = {}
    if bind:      d["title"] = bind
    if bind_link:
        s["link"] = link("#")
        d["link"] = bind_link
    _merge(s, g, d)
    if classes: s["_css_classes"] = classes
    if extra:   s.update(extra)
    return widget("heading", s)

def text(html, font=None, color=None, classes="", bind=None,
         tight=False, extra=None):
    """Omit font+color for body copy — it inherits the `text` global, which is
    exactly what a hand-built Elementor page looks like."""
    s = {"editor": html if str(html).startswith("<") else f"<p>{html}</p>"}
    g = {}
    if font:  g["typography_typography"] = gt(font)
    if color: g.update(_cglobal("text_color", color))
    _merge(s, g, {"editor": bind} if bind else None)
    if tight:   s["paragraph_spacing"] = px(0)   # kills the <p> bottom margin
    if classes: s["_css_classes"] = classes
    if extra:   s.update(extra)
    return widget("text-editor", s)

def button(text_str, url="#", style="primary", icon=None, font="primary",
           bg=None, fg="#FFFFFF", bind_url=None, classes="", extra=None):
    s = {"text": text_str, "link": link(url)}
    g = {"typography_typography": gt(font)}
    if icon:
        s["selected_icon"] = fa_solid(icon)
        s["icon_align"] = "right"
        s["icon_indent"] = px(8)
    if style == "primary":
        g.update(_cglobal("background_color", bg))
        s["button_text_color"] = fg
        s["border_radius"] = dim(50, 50, 50, 50, linked=True)
        s["text_padding"] = dim(12, 22, 12, 22)
    elif style == "ghost":
        s["background_color"] = "rgba(0,0,0,0)"
        g.update(_cglobal("button_text_color", bg))
        g.update(_cglobal("border_color", bg))
        s["border_border"] = "solid"
        s["border_width"] = dim(1, 1, 1, 1, linked=True)
    elif style == "textlink":
        s["background_color"] = "rgba(0,0,0,0)"
        g.update(_cglobal("button_text_color", bg))
        s["text_padding"] = dim(0, 0, 0, 0)
    _merge(s, g, {"link": bind_url} if bind_url else None)
    if classes: s["_css_classes"] = classes
    if extra:   s.update(extra)
    return widget("button", s)

def image(url="", alt="", classes="", bind=None, bind_link=None, extra=None):
    s = {"image": {"url": url, "id": "", "alt": alt, "source": "url"},
         "image_size": "full"}
    d = {}
    if bind:      d["image"] = bind
    if bind_link:
        s["link_to"] = "custom"
        s["link"] = link("#")
        d["link"] = bind_link
    _merge(s, None, d)
    if classes: s["_css_classes"] = classes
    if extra:   s.update(extra)
    return widget("image", s)

def divider(color=None, weight=1):
    s = {"weight": px(weight), "gap": px(15)}
    _merge(s, _cglobal("color", color))
    return widget("divider", s)

def nested_tabs(titles, panels, classes=""):
    """First tab is open on load. Panels are containers, matched by order.
    Keep settings minimal — cosmetic sub-controls are unverified; style the
    inner widgets via globals and .e-n-tab-title via CSS."""
    s = {"tabs": [{"_id": eid(), "tab_title": t} for t in titles]}
    if classes: s["_css_classes"] = classes
    w = widget("nested-tabs", s)
    w["elements"] = panels
    return w

def loop_grid(query_id, post_type, columns=1, classes="", extra=None):
    """template_id is EMPTY on purpose — the Loop Item's post id is assigned by
    the target DB on import, and a stale id makes Elementor fetch null → fatal.
    The user selects the template once. Pair with an elementor/query/<id> filter."""
    s = {"template_id": "", "query_post_type": post_type,
         "query_query_id": query_id, "query_id": query_id,
         "columns": str(columns), "columns_mobile": "1"}
    if classes: s["_css_classes"] = classes
    if extra:   s.update(extra)
    return widget("loop-grid", s)

# ---------------------------------------------------------------- DOCUMENT
def document(title, content, dtype="page", page_settings=None):
    """`content` takes several top-level containers — don't add a root wrapper."""
    return {"version": "0.4", "title": title, "type": dtype,
            "content": content if isinstance(content, list) else [content],
            "page_settings": page_settings or {}, "metadata": {}}

def write(path, doc):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
