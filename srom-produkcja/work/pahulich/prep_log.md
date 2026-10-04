# prep.py — changes to the extraction

- 'religiopolitical' -> 'religio-political': PDF 'religio-|political' at a line end; hyphen kept (check against Wynter 2003, 309 — query)
- 'statedefined' -> 'state-defined': PDF 'state-|defined' at a line end; 'statedefined' is no word
- '*Ibid.,*' -> '*Ibid.*,' ×8: comma set roman
- 'Mróz 2015*,* 17, 58' -> 'Mróz 2015, 17, 58': comma in italics (PDF)
- '[Dissertation on the Gipseys]*,*' -> '[Dissertation on the Gipseys],': comma in italics (PDF)
- ' (for similar inquiry, see Parvulescu and Boatcă 2022)' -> '[^m1]' + [^m1]: 'For similar inquiry, see Parvulescu and Boatcă 2022.': prose inside the parenthesis: the whole of it becomes the note (Kanon § 7.1)
- 'Ella Shohat and Robert Stam (2012)' -> 'Ella Shohat and Robert Stam[^m2]' + [^m2]: 'Shohat and Stam 2012.': narrative citation with first names: marker after the names (§ 7.1)
- ' (see also Thomas 2018 on Soviet politics of sedentarization of nomads in Central Asia)' -> '[^m3]' + [^m3]: '[Zob. też @thomas2018] on Soviet politics of sedentarization of nomads in Central Asia.': prose inside the parenthesis: the whole of it becomes the note; keyed by hand (the lead-in is followed by prose)
- 'the creation of other racial states” (*Ibid.*, 155)' -> 'the creation of other racial states” (Shohat and Stam 2012, 155)': Ibid. = Shohat and Stam (2012), named just before it (a hand-made note, which the scan does not track)
- '(*Ibid.*; Mróz 2015)' -> '(Červinski 2008; Mróz 2015)': Ibid. = the work cited just before it in the paragraph, (Červinski 2008)
- 'dainty” (viii)' -> 'dainty” (1807, viii)': page only: the work cited in the same sentence, Grellmann (1807)
- 'nationality” (74)' -> 'nationality” (1931, 74)': page only: the work cited in the same sentence, Barannikov (1931)
- 'internal affairs (1992, 81; Crowe 2007, 109).' -> 'internal affairs (1992, 81); Crowe 2007, 109. <!-- DO SPRAWDZENIA: „1992, 81” – rok i strona bez nazwiska autora; zapewne Fraser 1992 (pytanie do autora, pahulich_queries.md) -->': note 2: '1992, 81' has no author in the source — left as written, flagged; Crowe keyed
- 'Jenkins and Leroy (2021)' -> 'Jenkins and Leroy (2021)<!-- DO SPRAWDZENIA: Jenkins, Leroy 2021 – brak w bibliografii autora (pytanie do autora) -->': work not in the author's list — left as written, flagged
- '## Acknowledgments' section (end) -> ::: przypis-tytulowy at the top (Kanon § 7.1)
