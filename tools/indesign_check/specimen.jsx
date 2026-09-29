// args: setupJsx pdfOut
//@target indesign
var A = arguments;
app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;
var doc = app.documents.add(false);
app.scriptPreferences.measurementUnit = MeasurementUnits.POINTS;
doc.viewPreferences.horizontalMeasurementUnits = MeasurementUnits.POINTS; doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.POINTS;
doc.documentPreferences.facingPages = true; doc.documentPreferences.pageWidth = 467.716535433071; doc.documentPreferences.pageHeight = 666.141732283465;
doc.documentPreferences.pagesPerDocument = 3;
var SROM_TARGET_DOC = doc, SROM_REPORT = Folder.temp + "/srom_specimen_setup.txt";
var res = $.evalFile(new File(A[0]));
function ps(n) { var a = doc.allParagraphStyles, i; for (i = 0; i < a.length; i++) { if (a[i].name === n) { return a[i]; } } throw new Error("no style " + n); }
function cs(n) { return doc.characterStyles.itemByName(n); }
var pages = doc.pages, frames = [], i, pg, b;
for (i = 0; i < pages.length; i++) {
  pg = pages[i]; b = pg.side === PageSideOptions.LEFT_HAND ? [66.61, 48.19, 666.14 - 45.35, 467.72 - 62.36] : [66.61, 62.36, 666.14 - 45.35, 467.72 - 48.19];
  frames.push(pg.textFrames.add({geometricBounds: b}));
  if (i > 0) { frames[i - 1].nextTextFrame = frames[i]; }
}
var st = frames[0].parentStory;
// [style, text, [ [charStyle, substring], ... ], footnote]
var P = [
 ["Autor", "Anna Kowalska"], ["Afiliacja", "Uniwersytet Jagielloński"],
 ["Tytuł", "Tytuł artykułu, który zajmuje dwa wiersze i pokazuje interlinię 21,6 pt"],
 ["Śródtytuł", "Śródtytuł – wersalikami"],
 ["Tekst BEZ WCIĘCIA", "Pierwszy akapit po śródtytule zaczyna się bez wcięcia. W tekście pojawia się kursywa, np. tytuł książki Cyganie na polskich drogach, a po jednoliterowych spójnikach i przyimkach, jak w Tarnowie i Krakowie, nie łamie się wiersza.", [["Kursywa", "Cyganie na polskich drogach"]], "J. Ficowski, Cyganie na polskich drogach, Kraków 1985, s. 17."],
 ["Tekst", "Kolejny akapit ma wcięcie 4 mm. Tekst 10,5/13 pt na siatce bazowej 13,2945 pt, Cambria, justowanie z odstępami wyrazów 85–115%, liter od −3 do +1% i skalowaniem znaków 98–102%, jak w tomie 18. Liczby 13 000 i 45 % trzymają się razem, podobnie jak s. 15 i J. Ficowski.", [], "Tamże, s. 20–21. Drugi przypis sprawdza, jak wygląda przypis złożony w dwóch wierszach, 9/10,8 pt, bez siatki."],
 ["Cytat", "Cytat blokowy: 9 pt, wcięcie 1 cm, na siatce, te same ustawienia justowania co Tekst. Dłuższy cytat zajmuje kilka wierszy, żeby było widać, jak się składa w węższej kolumnie i czy nie ma dziur między wyrazami."],
 ["Tekst", "Po cytacie akapit wraca z wcięciem."],
 ["Śródtytuł MAŁE", "Śródtytuł małe – drugi stopień"],
 ["Tekst BEZ WCIĘCIA", "Wyliczenie – myślnik lub numer wpisany, tabulator na wcięciu wiszącym:"],
 ["Wyliczenie", "–\tpierwszy człon wyliczenia, na tyle długi, by przeszedł do drugiego wiersza i pokazał wcięcie wiszące;"],
 ["Wyliczenie", "–\tdrugi człon;"], ["Wyliczenie", "1.\tczłon numerowany;"], ["Wyliczenie", "2.\tdrugi numerowany."],
 ["Cytat", "Przewodniczący Coe: Na jakim statku pan przypłynął? – dialog w stylu Cytat, etykieta mówcy w stylu znakowym Pogrubienie.", [["Pogrubienie", "Przewodniczący Coe:"]]],
 ["Mówca", "Michał Garapich"], ["Afiliacja", "University of Roehampton"],
 ["Tekst BEZ WCIĘCIA", "Wypowiedź panelisty w transkrypcji, akapit bez wcięcia po nazwisku i afiliacji.*", [["Gwiazdka", "*"]]],
 ["Motto", "Fotografia uchodzi za niepodważalny dowód, że dana rzecz się wydarzyła (motto, kursywa, tytuł O fotografii prosto).", [["Proste", "O fotografii"]]],
 ["Motto ŹRÓDŁO", "Susan Sontag"],
 ["Cytat WIERSZ", "Pierwszy wers wiersza,\ndrugi wers, nieco dłuższy od pierwszego,\ntrzeci."],
 ["Tabela TYTUŁ", "Tabela 1. Tytuł tabeli"], ["Tabela TREŚĆ", "Treść komórki tabeli, 9/10,8, do lewej."],
 ["Podpis", "Podpis ilustracji, 9/10,8, justowany, ostatni wiersz do środka. Źródło: Wikimedia Commons."],
 ["Podpis LINIA", "Podpis z linią 0,4 pt pod spodem. Źródło: archiwum autora."],
 ["Przykład FORMA", "me\tdikhav\ttut"], ["Przykład GLOSA", "1SG.NOM\tsee-1SG\t2SG.ACC"], ["Przykład PRZEKŁAD", "‘widzę cię’"],
 ["Śródtytuł", "Bibliografia"], ["Śródtytuł MAŁE", "Opracowania"],
 ["Bibliografia", "Ficowski, Jerzy, Cyganie na polskich drogach, Wydawnictwo Literackie, Kraków 1985.", [["Kapitaliki", "Ficowski"], ["Kursywa", "Cyganie na polskich drogach"]]],
 ["Bibliografia", "Mróz, Lech, Dzieje Cyganów-Romów w Rzeczypospolitej XV–XVIII w., DiG, Warszawa 2001.", [["Kapitaliki", "Mróz"], ["Kursywa", "Dzieje Cyganów-Romów w Rzeczypospolitej XV–XVIII w."]]],
 ["Przypis GWIAZDKOWY", "* Przypis gwiazdkowy (nota tłumacza) – ten sam krój co Przypis, gwiazdka w indeksie górnym."],
 ["Tekst INICJAŁ", "Kolejna edycja Konferencji Taborowej – akapit otwierający z inicjałem na dwa wiersze, żeby było widać, jak siada na siatce."],
 ["Spis AUTOR", "Anna Kowalska"], ["Spis treści", "Tytuł artykułu w spisie treści\t7"], ["Spis JĘZYKI", "Title of the article in English"],
 ["Pagina", "Anna Kowalska – Tytuł artykułu"], ["Folio", "7"]
];
var k, j, p, fn, t, m, f;
for (k = 0; k < P.length; k++) {
  st.insertionPoints[-1].contents = P[k][1] + (k < P.length - 1 ? "\r" : "");
}
for (k = 0; k < P.length; k++) {
  p = st.paragraphs[k];
  p.appliedParagraphStyle = ps(P[k][0]);
  var runs = P[k][2] || [];
  for (j = 0; j < runs.length; j++) {
    f = p.contents.indexOf(runs[j][1]);
    if (f >= 0) { p.characters.itemByRange(f, f + runs[j][1].length - 1).appliedCharacterStyle = cs(runs[j][0]); }
  }
  if (P[k][3]) { fn = p.insertionPoints[-2].footnotes.add(); fn.insertionPoints[-1].contents = P[k][3]; }
}
doc.exportFile(ExportFormat.PDF_TYPE, new File(A[1]), false);
var ov = frames[frames.length - 1].overflows;
doc.close(SaveOptions.NO);
app.scriptPreferences.userInteractionLevel = UserInteractionLevels.INTERACT_WITH_ALL;
res + " | overset " + ov;
