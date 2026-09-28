# Ndiaye, „Czarni Romowie” — przekład wstępny: arkusz uwag dla MB (28.09.2026)

Pliki: `ndiaye_pl.md` (tekst, 133 przypisy + 2 przypisy tłumacza + 1 przypis tytułowy: nota o przekładzie, potem podziękowania autorki – D12), `ndiaye_front_pl.md` (tytuł, abstrakt, słowa kluczowe), `ndiaye_refs_tlum.json` (2 wydania polskie dodane przez tłumacza), `ndiaye_pytania_tlum.csv` (14 pozycji). Word do pracy: `python3 $S/export_work.py work/ndiaye/ndiaye_pl.md -o ndiaye_robocza.docx`.

## 1. Do uzupełnienia przez MB — strony i brzmienie wydań polskich (znaczniki `DO SPRAWDZENIA` w tekście)

**Ta lista jest jedynym zabezpieczeniem.** Komentarze nie zatrzymują kompilacji (`handoff.md`: komentarze niczego nie blokują; `build.py` usuwa je z ostrzeżeniem i kończy się wynikiem PASS). W kopii roboczej Worda stają się komentarzami Worda, a po imporcie znikają z tekstu i zostają tylko w raporcie importu. Pozycja jest zamknięta dopiero wtedy, gdy MB ją rozstrzygnie: wtedy „otwarte” → „zamknięte dd.mm.rrrr (MB)”. Stan 28.09.2026: 7 otwartych.

- S1 [otwarte] – przyp. 44 i tekst przed nim: *Chory z urojenia*, intermedium I. Przekładu Boya nie ma w Wolnych Lekturach — w tekście **przekład roboczy z francuskiego**; podmienić na brzmienie Boya, dopisać wydanie i stronę.
- S2 [otwarte] – przyp. 49: *Szelmostwa Skapena*, akt III (Zerbineta): „bandy Cyganów, z tych, co to wałęsając się…” — strona.
- S3 [otwarte] – przyp. 50: akt I: „małe nieporozumienie”, „Bardzo się brzydko obszedł ze mną” — strona.
- S4 [otwarte] – przyp. 51: akt I: „trzy lata galer mniej czy więcej…” — strona.
- S5 [otwarte] – przyp. 68: akt III, scena z workiem: „Baczność! Oto znów jakaś podejrzana figura” — strona.
- S6 [otwarte] – przyp. 69: akt II, Skapen do Leandra: „nie ma pomiędzy nim a panem ani cienia podobieństwa…” — strona.
- S7 [otwarte] – przyp. 112 i tekst przed nim: C. P. Hong, *Pomniejsze uczucia*, tłum. A. Zano, Tajfuny 2024 — **brzmienie i strona** (w tekście przekład roboczy z angielskiego; oryginał s. 198).

Wydanie Boya: cytuję *Dzieła*, t. 6, Warszawa 1922 (podstawa tekstu Wolnych Lektur; tekst w `research/boy_skapen.txt`). Najnowsze wydanie naukowe to PIW 1988 (3 tomy). Jeśli strony z 1988 — zmienić wpis `molier1922` w `ndiaye_refs_tlum.json`. Cytaty S2–S6 sprawdziłem z tekstem Boya słowo w słowo.

## 2. Rozbieżności Boy – Molier, objaśnione przypisami tłumacza
- *Égyptiens* → u Boya zawsze „Cyganie”; wywód autorki opiera się na nazwie (przyp. tłum. *t1*).
- *bracelet* → u Boya „naszyjnik” (*t2*); w tekście autorki zostaje „bransoleta”.
- *qui a la mine d’un étranger* → u Boya „podejrzana figura” (dopisek w nawiasie w przyp. 68).
Brzmienie francuskie sprawdzone w wydaniu Louandre 1910 (fr.wikisource).

## 3. Zastosowane rozstrzygnięcia (D11) i moje wybory do potwierdzenia
- Tabela terminów (intake § 3) — wszystko jak w rekomendacji: czarni/biali małą literą, biała supremacja, studia nad czarnością (*Black studies*), matryca rasowa, zniewoleni/zniewolenie, Maurowie (z franc. *Mores*), Murzyn (z ang. *Blackamoor*, *negro*), urasowienie/urasawiać (HOUSE), krytyczne studia romskie, romolog/romologia.
- **Imiona postaci Moliera wg Boya** (Skapen, Leander, Zerbineta, Geront, Argant, Hiacynta, Sylwester, Karlo, Sganarel), oryginał w nawiasie przy pierwszym wystąpieniu; postaci Vallée, Ravenscrofta, M. W. — w oryginale (Hécate’a, Boristhène’a…).
- **Tytuły**: tytuły wydań polskich (Moliera, Szekspira, *Cyganiątko*, *Nowele przykładne*, *Formion* — ten ostatni potwierdzony we wstępie Boya). **Niepotwierdzone**: *Cyganiątko* jako tytuł *La gitanilla* w przekładzie z 1976 r.; *Opowieść etiopska* Heliodora (może *Etiopika*); moje przekłady tytułów w nawiasach (*Sielanka komiczna*, *Swat, czyli Rajfur*, obrazy: *Cyganka*, *Wróżka*).
- Śródtytuły ponumerowane (Kanon § 2; w oryginale bez numerów). Śródtytuł 4: „FIKCJE UCHODZENIA ZA BIAŁYCH…” — dodałem „za białych” (oryg. *Fictions of passing*); alternatywa: „FIKCJE *PASSINGU*…”.
- *race play* → „dramat rasowy”.
- Tytuły wierszy Scudéry’ego i Chevreau w cudzysłowie, jak u autorki (Kanon: kursywa? — do decyzji).
- W przyp. 66 (cytat z Taylor) ang. *Bohemian* → *Bohémien*.
- Elisa, *Old Goodwit’s niece* → „bratanica” (równie dobrze „siostrzenica”; sztuka nie mówi).
- **Odmiana nazwisk wg rodzaju, przyjętego z imion i informacji publicznych** (niepotwierdzone przez MB): Tracy C. Davis, Jessica Wolfe, Kim Coles, Karen Newman, Esther Crooks, Sydnee Wagner, Carol Mejia-LaPerle, M. A. Katritzky, Cynthia Damon, Becky Taylor, Susan Phillips, Erith Jaffe-Berg, Angéla Kóczé, Bridgette Baldwin, Margareta Matache, Tiffany Lethabo King, Lisa Lowe, Henriette Asséo, Annie Cathelin — kobiety; C. Riley Snorton, Nigel Smith, Dénètem Touam Bona („Touama Bony” — sprawdzić odmianę), Robin G. Kelley, Cedric Robinson, Mathieu Plésiat — mężczyźni.
- Poprawione omyłki autorki (zgłoszone w wykazie pytań jako informacja): *status* → „deklaracja” (1682, 2×); *cascabales* → *cascabeles*.

## 4. Otwarte poza przekładem
- Nazwy grup (D13, zastosowane 28.09.2026): Romni → Romka, Romnia → Romki; *gadjo* / *gadji* / *gadje* małą literą, kursywą przy pierwszym wystąpieniu, w pisowni autorki; wczesnonowożytni „Egipcjanie” w cudzysłowie. Przypis 1 zachowuje listę słów romskich autorki w oryginale.
- Nota o przekładzie: brak numeru zeszytu RQ 75 → `[BRAK nr]`.
- Słowa kluczowe angielskie — do zatwierdzenia przez autorkę.
- Ilustracje (3): pliki i zgody — etap 3 (srom-typeset).
