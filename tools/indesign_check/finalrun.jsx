// finalrun.jsx — setup + final pass on a copy (indesign_check.py). args: idml setupJsx finalJsx mode report pdf
//@target indesign
var A = arguments, res = "", t0 = new Date().getTime();
app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;
var doc = app.open(new File(A[0]), false);
var SROM_TARGET_DOC = doc, SROM_REPORT = A[4] + ".setup.txt", SROM_MODE = A[3];
try { res = $.evalFile(new File(A[1])); } catch (e) { res = "SETUP ERROR " + e + " line " + e.line; }
SROM_REPORT = A[4];
try { res += " | " + $.evalFile(new File(A[2])); } catch (e2) { res += " | FINAL ERROR " + e2 + " line " + e2.line; }
if (A[5]) { try { doc.exportFile(ExportFormat.PDF_TYPE, new File(A[5]), false); } catch (e3) { res += " | PDF " + e3; } }
doc.close(SaveOptions.NO);
app.scriptPreferences.userInteractionLevel = UserInteractionLevels.INTERACT_WITH_ALL;
res + " | " + Math.round((new Date().getTime() - t0) / 1000) + " s";
