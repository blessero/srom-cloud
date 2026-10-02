// srom_zakladki.jsx — PDF bookmarks from the headings (MB, 02.10.2026: Google Scholar's viewer guessed the outline
// and missed "Wstęp"). General script, any SROM document. Run once the text is final, before the PDF export;
// running it again replaces the bookmarks it made before (and only those). One undo step.
//   Tytuł            -> top level (the article; a whole volume gets one entry per article)
//   Śródtytuł        -> under the article's title (top level if there is no title)
//   Śródtytuł MAŁE   -> under the heading before it
// PDF export: tick "Bookmarks" (General > Include) in the export dialog / preset, or they are not written.
//@target indesign

var LEVEL = {"Tytuł": 0, "Śródtytuł": 1, "Śródtytuł MAŁE": 2};
var PREFIX = "srom-zakladka ";              // names of the text anchors this script creates

function clean(s) {
  s = String(s).replace(new RegExp("[\\r\\n\\t\\u2028\\u2029]+", "g"), " ").replace(/\s+/g, " ").replace(/^\s+|\s+$/g, "");
  return s.length > 120 ? s.substr(0, 117) + "…" : s;
}

function headings(doc) {
  // every heading paragraph with its page position, in reading order (page, then top to bottom)
  var out = [], s, i, p, nm, f, pg;
  for (s = 0; s < doc.stories.length; s++) {
    var ps = doc.stories[s].paragraphs;
    for (i = 0; i < ps.length; i++) {
      p = ps[i]; nm = p.appliedParagraphStyle.name;
      if (!LEVEL.hasOwnProperty(nm) || clean(p.contents) === "") { continue; }
      f = p.parentTextFrames;
      if (!f || !f.length || !f[0].parentPage) { continue; }            // overset or pasteboard: no page to link to
      pg = f[0].parentPage;
      out.push({p: p, level: LEVEL[nm], page: pg.documentOffset, y: p.baseline, name: clean(p.contents)});
    }
  }
  out.sort(function (a, b) { return a.page !== b.page ? a.page - b.page : a.y - b.y; });
  return out;
}

function removeOld(doc) {
  var i, n = 0, d = doc.hyperlinkTextDestinations;
  for (i = doc.bookmarks.length - 1; i >= 0; i--) {
    try { if (doc.bookmarks[i].destination.name.indexOf(PREFIX) === 0) { doc.bookmarks[i].remove(); n++; } } catch (e) {}
  }
  for (i = d.length - 1; i >= 0; i--) { if (d[i].name.indexOf(PREFIX) === 0) { d[i].remove(); } }
  return n;
}

function build(doc, hs) {
  var i, h, dest, bm, parent = [null, null, null], made = 0;
  for (i = 0; i < hs.length; i++) {
    h = hs[i];
    dest = doc.hyperlinkTextDestinations.add(h.p.insertionPoints[0], {name: PREFIX + (i + 1)});
    var lvl = h.level, up = null, k;
    for (k = lvl - 1; k >= 0; k--) { if (parent[k]) { up = parent[k]; break; } }
    bm = up ? up.bookmarks.add(dest) : doc.bookmarks.add(dest);
    bm.name = h.name;
    parent[lvl] = bm;
    for (k = lvl + 1; k < 3; k++) { parent[k] = null; }
    made++;
  }
  return made;
}

function main() {
  var doc = (typeof SROM_DOC !== "undefined") ? SROM_DOC : (app.documents.length ? app.activeDocument : null);
  if (!doc) { alert("SROM bookmarks: no document open."); return "no document"; }
  var hs = headings(doc), out = [], old = 0, made = 0;
  app.doScript(function () { old = removeOld(doc); made = build(doc, hs); },
               ScriptLanguage.JAVASCRIPT, undefined, UndoModes.ENTIRE_SCRIPT, "SROM bookmarks");
  out.push("SROM bookmarks — " + doc.name);
  out.push("bookmarks made: " + made + (old ? " (" + old + " old ones replaced)" : ""));
  var i, pad = ["", "   ", "      "];
  for (i = 0; i < hs.length; i++) { out.push(pad[hs[i].level] + hs[i].name + "  (p. " + (hs[i].page + 1) + ")"); }
  if (!made) { out.push("!! no heading on a page: nothing to bookmark (styles Tytuł / Śródtytuł / Śródtytuł MAŁE)"); }
  out.push("Export the PDF with General > Include > Bookmarks ticked.");
  var r = out.join("\r");
  if (typeof SROM_DOC === "undefined") { alert(r); }
  return r;
}

main();
