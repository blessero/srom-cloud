// make_template.jsx — builds the clean SROM template (IDML) from a vol. 18 article file.
// Run by indesign_check.py --template OUT.idml (arguments: sourceIdml setupJsx outIdml outPdf report).
// Keeps the page, margins, masters and the threaded text frame of the source; everything else is rebuilt or cleaned:
// styles (srom_style_setup.jsx: purge + house style v3), placeholder text, running heads in Pagina/Folio, page
// numbering from 1, unused swatches, imported numbering lists, links, hyperlinks, bookmarks, conditions, XML tags,
// empty layers, 0 pt strokes that carry a colour. Report: every change.
//@target indesign
var A = arguments, LOG = [], doc, res, i, j, k, it, n;
function log(s) { LOG.push(s); }
function tryRemove(coll, keep, what) {
  var c = 0, x;
  for (x = coll.length - 1; x >= 0; x--) {
    try { if (keep && keep(coll[x])) { continue; } coll[x].remove(); c++; } catch (e) {}
  }
  if (c) { log("   removed " + c + " " + what); }
}
function ps(name) { var a = doc.allParagraphStyles, x; for (x = 0; x < a.length; x++) { if (a[x].name === name) { return a[x]; } } throw new Error("no style " + name); }

app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;
doc = app.open(new File(A[0]), false);
var SROM_TARGET_DOC = doc, SROM_REPORT = A[4] + ".setup.txt";
res = $.evalFile(new File(A[1]));
log("SROM template v3 from " + File(A[0]).name + " — styles: " + res);
app.scriptPreferences.measurementUnit = MeasurementUnits.POINTS;

// pages: an opening page and one spread
var main = null, best = 0;
for (i = 0; i < doc.stories.length; i++) { if (doc.stories[i].length > best) { best = doc.stories[i].length; main = doc.stories[i]; } }
var mainId = main.id;                       // stories[i] is addressed by position: hold the article story by its id
n = doc.pages.length;
for (i = doc.pages.length - 1; i >= 3; i--) { doc.pages[i].remove(); }
log("   pages " + n + " → " + doc.pages.length);
main = doc.stories.itemByID(mainId);
for (i = 0; i < doc.pages.length; i++) {
  var items = doc.pages[i].pageItems.everyItem().getElements();   // resolved types (TextFrame, Rectangle …)
  for (j = items.length - 1; j >= 0; j--) {
    it = items[j];
    if (it.constructor.name === "TextFrame" && it.parentStory.id === mainId) { continue; }
    log("   removed from p. " + doc.pages[i].name + ": " + it.constructor.name); it.remove();
  }
}
try { doc.sections[0].continueNumbering = false; doc.sections[0].pageNumberStart = 1; log("   page numbering starts at 1"); } catch (e0) { log("   ! section: " + e0); }

// placeholder text: every paragraph in its style, one footnote
var P = [["Autor", "Imię Nazwisko"], ["Afiliacja", "Afiliacja"], ["Tytuł", "Tytuł artykułu"], ["Śródtytuł", "Śródtytuł"],
         ["Tekst BEZ WCIĘCIA", "Pierwszy akapit po śródtytule. Tekst artykułu wpływa tu z pliku DOCX: zaznacz ramkę, menu Plik, polecenie Umieść, opcje importu „SROM – pandoc” (references/indesign.md)."],
         ["Tekst", "Kolejny akapit, z wcięciem 4 mm."]];
main.contents = "";
for (i = 0; i < P.length; i++) { main.insertionPoints[-1].contents = P[i][1] + (i < P.length - 1 ? "\r" : ""); }
for (i = 0; i < P.length; i++) { main.paragraphs[i].appliedParagraphStyle = ps(P[i][0]); main.paragraphs[i].clearOverrides(OverrideType.ALL); }
var fn = main.paragraphs[4].insertionPoints[-2].footnotes.add(); fn.insertionPoints[-1].contents = "Przypis: 9/10,8 pt, numer w indeksie górnym, po nim kropka i półfiret.";
log("   placeholder text in the article frame (" + P.length + " paragraphs, 1 footnote)");

// masters: running heads and page numbers in their styles, placeholder text
for (i = 0; i < doc.masterSpreads.length; i++) {
  var m = doc.masterSpreads[i];
  for (j = 0; j < m.textFrames.length; j++) {
    var tf = m.textFrames[j], txt;
    try { txt = String(tf.texts[0].contents); if (!tf.paragraphs.length) { continue; } }
    catch (eF) { continue; }                          // a frame without valid text (an empty threaded master frame)
    // frames above the type area are running heads: text → Pagina, the page-number frames (the marker is no text) → Folio
    var top = tf.geometricBounds[0] < tf.parentPage.marginPreferences.top;
    if (!top) { continue; }
    var isNum = !/[A-Za-zÀ-ž]/.test(txt);
    if (!isNum) {
      if (/Studia Romologica/.test(txt)) { tf.contents = "Studia Romologica 19/2026"; }
      else { tf.contents = "Imię Nazwisko – Tytuł skrócony"; }
      tf.paragraphs[0].appliedParagraphStyle = ps("Pagina"); tf.paragraphs[0].clearOverrides(OverrideType.ALL);
      log("   master " + m.name + ": running head „" + tf.contents + "” in Pagina");
    } else if (isNum) {
      for (k = 0; k < tf.paragraphs.length; k++) { tf.paragraphs[k].appliedParagraphStyle = ps("Folio"); tf.paragraphs[k].clearOverrides(OverrideType.ALL); }
      log("   master " + m.name + ": page number in Folio");
    }
  }
}

// junk
log("   clean-up:");
var keepSw = {"None": 1, "Paper": 1, "Black": 1, "Registration": 1};
tryRemove(doc.unusedSwatches, function (s) { return keepSw[s.name] === 1 || s.name === ""; }, "unused swatches");
tryRemove(doc.numberingLists, function (l) { return l.name.charAt(0) === "["; }, "numbering lists (Word import)");
tryRemove(doc.hyperlinks, null, "hyperlinks");
tryRemove(doc.hyperlinkTextDestinations, null, "hyperlink destinations");
tryRemove(doc.hyperlinkURLDestinations, null, "URL destinations");
tryRemove(doc.bookmarks, null, "bookmarks");
tryRemove(doc.conditions, null, "conditions");
try { doc.xmlElements[0].xmlElements.everyItem().untag(); } catch (e1) {}
tryRemove(doc.xmlTags, function (t) { return t.name === "Root"; }, "XML tags");
tryRemove(doc.tableStyles, function (t) { return t.name.charAt(0) === "["; }, "table styles");
tryRemove(doc.cellStyles, function (t) { return t.name.charAt(0) === "["; }, "cell styles");
for (i = doc.layers.length - 1; i >= 0 && doc.layers.length > 1; i--) {
  if (doc.layers[i].allPageItems.length === 0) { log("   removed empty layer " + doc.layers[i].name); doc.layers[i].remove(); }
}
var all = doc.allPageItems, hair = 0;          // allPageItems returns resolved types
for (i = 0; i < all.length; i++) {
  try { if (all[i].strokeWeight === 0 && all[i].strokeColor.name !== "None") { all[i].strokeColor = "None"; hair++; } } catch (e2) {}
}
if (hair) { log("   " + hair + " page item(s) with a 0 pt stroke in colour → stroke None (could print as a hairline)"); }
var left = [];
if (main.overflows) { left.push("article frame overset"); }
if (doc.links.length) { left.push(doc.links.length + " links"); }
doc.exportFile(ExportFormat.INDESIGN_MARKUP, new File(A[2]));
if (A[3]) { app.pdfExportPreferences.pageRange = PageRange.ALL_PAGES; doc.exportFile(ExportFormat.PDF_TYPE, new File(A[3]), false); }
log("   written " + File(A[2]).name);
log(left.length ? "RESULT: check — " + left.join(", ") : "RESULT: OK");
doc.close(SaveOptions.NO);
var f = new File(A[4]); f.encoding = "UTF-8"; f.open("w"); f.write(LOG.join("\n")); f.close();
app.scriptPreferences.userInteractionLevel = UserInteractionLevels.INTERACT_WITH_ALL;
LOG[LOG.length - 1];
