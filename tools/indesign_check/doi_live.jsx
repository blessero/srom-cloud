// doi_live.jsx — for doi_check.py. args: template idml, docx, <stem>_doi.jsx, pdf out, report out.
// Places the DOCX into a hidden copy of the template (preset "SROM – pandoc" settings, pages added until nothing is
// overset), runs the DOI script twice (the second run must replace the first), exports the PDF, closes without saving.
#target indesign
var A = arguments, out = [], doc = null;
app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;
try {
  doc = app.open(new File(A[0]), false);
  var i, best = null, st;
  for (i = 0; i < doc.stories.length; i++) {
    st = doc.stories[i];
    if (!best || st.footnotes.length > best.footnotes.length || (st.footnotes.length === best.footnotes.length && st.textContainers.length > best.textContainers.length)) { best = st; }
  }
  var p = app.wordRTFImportPreferences;
  p.importFootnotes = true; p.importEndnotes = false; p.importTOC = false; p.importIndex = false; p.useTypographersQuotes = false;
  p.preserveGraphics = false; p.importUnusedStyles = false; p.preserveTrackChanges = false; p.removeFormatting = false;
  p.convertPageBreaks = ConvertPageBreaks.NONE;
  p.resolveParagraphStyleClash = ResolveStyleClash.RESOLVE_CLASH_USE_EXISTING; p.resolveCharacterStyleClash = ResolveStyleClash.RESOLVE_CLASH_USE_EXISTING;
  best.contents = "";
  best.insertionPoints[0].place(new File(A[1]), false);
  var fr = best.textContainers[best.textContainers.length - 1], n = 0, pg, b, m, l, r;
  while (best.overflows && n < 200) {
    pg = doc.pages.add(LocationOptions.AT_END); b = pg.bounds; m = pg.marginPreferences;
    l = pg.side === PageSideOptions.LEFT_HAND ? m.right : m.left; r = pg.side === PageSideOptions.LEFT_HAND ? m.left : m.right;
    var nf = pg.textFrames.add({geometricBounds: [b[0] + m.top, b[1] + l, b[2] - m.bottom, b[3] - r]});
    fr.nextTextFrame = nf; fr = nf; n++; best.recompose();
  }
  out.push("placed: " + best.footnotes.length + " footnotes, " + doc.pages.length + " pages, overset " + best.overflows);
  var SROM_DOC = doc, SROM_APPLY = true;
  out.push("RUN1 " + $.evalFile(new File(A[2])));
  out.push("RUN2 " + $.evalFile(new File(A[2])));
  out.push("COUNTS hyperlinks " + doc.hyperlinks.length + " sources " + doc.hyperlinkTextSources.length + " destinations " + doc.hyperlinkURLDestinations.length);
  app.pdfExportPreferences.pageRange = PageRange.ALL_PAGES;
  app.pdfExportPreferences.includeHyperlinks = true;
  doc.exportFile(ExportFormat.PDF_TYPE, new File(A[3]), false);
} catch (e) { out.push("ERROR " + e + " line " + e.line); }
if (doc) { doc.close(SaveOptions.NO); }
app.scriptPreferences.userInteractionLevel = UserInteractionLevels.INTERACT_WITH_ALL;
var f = new File(A[4]); f.encoding = "UTF-8"; f.open("w"); f.write(out.join("\n")); f.close();
"done";
