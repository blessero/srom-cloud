// args: mode(new|open) input setupJsx report dump pdf("" = none)
#target indesign
#include "dumplib.jsxinc"
var A = arguments, doc, res;
app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;
doc = A[0] === "new" ? app.documents.add(false) : app.open(new File(A[1]), false);
var SROM_TARGET_DOC = doc, SROM_REPORT = A[3];
try { res = A[2] ? $.evalFile(new File(A[2])) : "no setup"; } catch (e) { res = "SETUP ERROR " + e + " line " + e.line; }
try { dumpDoc(doc, A[4]); } catch (e2) { res += " | DUMP ERROR " + e2; }
if (A[5]) { try { doc.exportFile(ExportFormat.PDF_TYPE, new File(A[5]), false); } catch (e3) { res += " | PDF ERROR " + e3; } }
doc.close(SaveOptions.NO);
app.scriptPreferences.userInteractionLevel = UserInteractionLevels.INTERACT_WITH_ALL;
res;
