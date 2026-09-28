> **ZASTĄPIONY 26.09.2026.** Tekst przyjęty do Kanonu v1.6 jako § 12.2 (skill srom-kanon, `references/kanon-redakcyjny.md`) — rozstrzyga tamten tekst. Ten plik zachowany jako zapis historyczny.

# STUDIA ROMOLOGICA – KANON EDYTORSKI

## Projekt § 12.2. Artykuły tłumaczone (do wersji 1.6)

**Status: projekt rozstrzygnięty przez redaktora prowadzącego (25.09.2026), do włączenia do kanonu.** Znak ▲ oznaczał kwestię otwartą; wszystkie zostały rozstrzygnięte.

Umiejscowienie: po § 12.1. Zmiany wynikowe: § 1 pkt 8 i 9 (wyjątki), § 4.2 (wyłączenie formuły `[tłum. własne]`), § 6.3 (odstępstwo dla tekstu przekładu), § 11 (nowy skrót), § 17 (wpis 1.6).

---

### 12.2.1. Zakres i pierwszeństwo

Paragraf dotyczy artykułów publikowanych w przekładzie na język polski z oryginału anglojęzycznego (w rekordzie: `is_translation` = `TAK`); przekłady z innych języków wymagają osobnej regulacji metadanych (§ 12.2.2). Pozostałe paragrafy kanonu stosuje się bez zmian, o ile niniejszy nie stanowi inaczej; w razie kolizji rozstrzyga § 12.2. § 12.1 nie stosuje się: wersją angielską artykułu tłumaczonego jest jego pierwodruk.

### 12.2.2. Metadane

- Tytuł angielski, abstrakt angielski i angielskie słowa kluczowe – **w brzmieniu oryginału**, bez zmian i bez przekładu zwrotnego. Wyjątek od § 1 pkt 8: przekładem jest abstrakt polski, nie angielski. Przekład zwrotny wprowadziłby do rekordu deponowanego drugą, rozbieżną wersję angielską.
- Oryginał bez abstraktu lub słów kluczowych – sporządza je tłumacz, w wersji polskiej i angielskiej; wersję angielską zatwierdza autor.
- Abstrakt oryginału dłuższy niż 1000 znaków (§ 1 pkt 7) – abstrakt polski skraca redakcja, abstrakt angielski pozostaje w brzmieniu oryginału; rozbieżność długości jest dopuszczalna.
- Tytuł polski – przekład tytułu oryginału, z zachowaniem podziału na tytuł i podtytuł.
- Słowa kluczowe pochodzą zawsze od autora. Polskie – przekład angielskich; nazwy grup w formie wzorcowej (§ 6.3). Angielskie – autorskie, bez zmian (odstępstwo od § 1 pkt 9). Wątpliwości co do pisowni rozstrzyga się w toku pracy, z wpisem do rejestru decyzji.
- Rekord: pola `original_title`, `original_source`, `original_doi` wypełnione. Relację `isTranslationOf` generuje moduł deponowania, gdy znany jest DOI oryginału.

### 12.2.3. Nota o przekładzie i wskazanie tłumacza

- Tłumacz – w nagłówku artykułu, pod afiliacją autora: `Tłumaczenie: Imię Nazwisko`; ponadto w nocie o przekładzie.
- **Nota o przekładzie jest obowiązkowa**: jawność pierwodruku wyklucza zarzut publikacji zdublowanej. Przypis do tytułu, oznaczony gwiazdką (§ 7.1). Zawiera, w tej kolejności:
  1. opis pierwodruku według § 7.2, z DOI;
  2. licencję pierwodruku z adresem jej tekstu albo podstawę zgody na przekład; przy licencjach Creative Commons – wskazanie, że przekład stanowi zmianę utworu, oraz nota o prawach autorskich pierwodruku, jeżeli ją zawiera (wymogi licencji);
  3. tłumacza;
  4. zakres ingerencji (§ 12.2.8), jeżeli wystąpiły;
  5. formułę o cytatach (§ 12.2.4 d).

Wzór:
> \* Pierwodruk: I. Nazwisko, *Tytuł oryginału*, „Czasopismo”, rrrr, t. nn, nr nn, s. aa–bb, DOI: 10.nnnn/nnnn. © I. Nazwisko. Tekst opublikowany na licencji CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); niniejszy przekład stanowi zmianę utworu w rozumieniu licencji. Tłumaczenie: Imię Nazwisko. Cytaty ze źródeł obcojęzycznych, o ile nie wskazano inaczej, w przekładzie tłumacza artykułu.

### 12.2.4. Cytaty

| Sytuacja | Postępowanie |
|---|---|
| a) Dzieło cytowane przez autora ma wydanie polskie | Cytat według wydania polskiego, ze stroną tego wydania; przypis odsyła do wydania polskiego (§ 4.3); odesłanie autora do oryginału zachowuje się w tym samym przypisie po średniku. Kilka przekładów polskich – najnowsze wydanie naukowe, chyba że starsze jest merytorycznie lepsze (decyzja redakcji, wpis do rejestru decyzji). Przekład własny zamiast wydania polskiego – wyłącznie gdy wydanie nie oddaje brzmienia istotnego dla wywodu; decyzja redakcji, przypis tłumacza podaje powód. |
| b) Źródło pierwotnie polskie, przytoczone przez autora po angielsku | Przywraca się brzmienie oryginału; przypis wskazuje źródło polskie; odesłanie autora zachowuje się po średniku, poprzedzone formułą `autor cytuje za:`. |
| c) Źródło w innym języku, przytoczone przez autora w przekładzie angielskim | Przekład z oryginału, jeżeli jest dostępny; w przeciwnym razie z przekładu autora, z adnotacją w przypisie `tłum. z przekładu angielskiego autora`. Materiał terenowy (wypowiedzi rozmówców w przekładzie autora) – jedna formuła w nocie zamiast adnotacji przy każdym cytacie. |
| d) Źródło anglojęzyczne bez wydania polskiego | Przekład tłumacza artykułu, bez adnotacji przy cytacie – obejmuje go formuła noty (§ 12.2.3). Formuły `[tłum. własne]` (§ 4.2) w przekładzie się nie stosuje: byłaby dwuznaczna. |
| e) Poezja, pieśń, przysłowie | Jak a–c. Brzmienie oryginału (np. romskie), jeżeli przytacza je autor, pozostaje tam, gdzie umieścił je autor. |

Nieodnalezienie miejsca w wydaniu polskim albo niedostępność oryginału – pozycja w wykazie pytań. Tekstu nie oddaje się do składu z cytatem przełożonym tymczasowo i nieoznaczonym (§ 0, zasada integralności danych).

Bibliografia (§ 9) obejmuje wydanie polskie, z którego pochodzą cytaty w sytuacji a, oraz – skoro odesłanie autora zostaje zachowane – oryginał.

### 12.2.5. Terminologia

- Terminy i pojęcia – w formie z bazy terminologicznej redakcji. Pozycje o statusie HOUSE, w tym **wszystkie rozstrzygnięcia tomu 18/2025**, obowiązują bez wyjątku.
- Pierwsze wystąpienie – forma polska, po niej oryginał kursywą w nawiasie okrągłym, w pisowni źródła (§ 4.3). Gdy forma polska jest tożsama z oryginałem (z dokładnością do polskiej końcówki fleksyjnej), nawiasu się nie stawia.
- W cytatach z wydań polskich (§ 12.2.4 a) terminologia wydania pozostaje bez zmian, także gdy różni się od formy HOUSE; rozbieżność istotną dla wywodu objaśnia przypis tłumacza.
- Neologizm autorski – jak wyżej; w razie potrzeby przypis tłumacza objaśniający przekład (§ 12.2.7).
- Pojęcie nieobecne w bazie – kwestia otwarta, rozstrzygana przez redaktora prowadzącego przed oddaniem przekładu, według reguły zapisanej w schemacie bazy. Zmiana formy HOUSE – wyłącznie jego decyzją, z wpisem do rejestru decyzji; obowiązuje od kolejnego tomu (§ 17).

### 12.2.6. Nazwy grup

- W przekładzie nazwy grup mają formę wzorcową z kartoteki (§ 6.3), bez formy oryginału w nawiasie (odstępstwo od § 6.3, który dla tekstu artykułu przewiduje formę autorską). Kartotekę uzupełnia się w toku pracy: forma dotąd nieustalona – kwestia do rozstrzygnięcia przed oddaniem przekładu.
- Wyjątek: autoetnonim albo forma, której brzmienie autor czyni przedmiotem analizy – pozostaje w brzmieniu oryginału, pismem prostym (§ 6.2).
- Ang. Gypsy – przekład według funkcji w tekście: kategoria źródłowa lub opis historyczny – `Cyganie` (§ 6.1 b); autoidentyfikacja – `Cyganie` (§ 6.1 c); w cytacie – odpowiednik oddający rejestr oryginału, bez łagodzenia (§ 6.1 a). Przypis wyjaśniający przy pierwszym wystąpieniu – jak w § 6.1. Pierwsze wystąpienie w każdej funkcji – w wykazie pytań.
- Wybór terminu przez autora jest respektowany: każdy termin źródła ma własny odpowiednik polski i nie zastępuje się jednego drugim (Gypsy nie staje się „Romowie”, Roma nie staje się „Cyganie”). Ang. Gypsy jako świadomie użyty termin samego autora – `Cyganie`, z przypisem wyjaśniającym przy pierwszym wystąpieniu (§ 6.1); jeżeli autor sam objaśnia swój wybór, przypis tłumacza może do tego objaśnienia odesłać.

### 12.2.7. Przypisy tłumacza

- Przypisy nieautorskie (przypis tytułowy, przypisy tłumacza i redakcji) – odrębny ciąg, oznaczony gwiazdkami (*, **, ***), liczony od nowa na każdej stronie; na pierwszej stronie pierwszą gwiazdkę ma przypis tytułowy (§ 7.1). Przypis tłumacza kończy formuła `– przyp. tłum.`, przypis redakcji – `– przyp. red.` Wyjątek od § 7.1 (numeracja ciągła dotyczy przypisów autora).
- Uzupełnienie w przypisie autora – w nawiasie kwadratowym, zakończone tą samą formułą, np. `[zob. też wydanie polskie: …, s. 45 – przyp. tłum.]`.
- W tekście głównym tłumacz nie wprowadza ingerencji w nawiasie kwadratowym: nawias kwadratowy w cytacie należy do autora (§ 4.1). Uzupełnienia w tekście głównym – wyłącznie te, które przewiduje § 4.3 (oryginał terminu, przekład tytułu, objaśnienie instytucji, przekład nazwy aktu prawnego), w nawiasie okrągłym, przy pierwszym wystąpieniu.
- § 11 uzupełnia się o skróty `przyp. tłum.` – przypis tłumacza, `przyp. red.` – przypis redakcji.

### 12.2.8. Ingerencje w treść oryginału

- Tłumacz nie poprawia oryginału bez uzgodnienia. Błędy rzeczowe, błędne daty, nazwiska, odesłania i opisy bibliograficzne trafiają do wykazu pytań.
- Poprawki uzgodnione z autorem wprowadza się bez oznaczania w tekście; nota o przekładzie odnotowuje, że przekład je uwzględnia. Poprawka istotna dla treści – komentarz (przypis tłumacza) uzgodniony z autorem.
- Oczywiste omyłki pisarskie (literówka w nazwisku, przestawione cyfry numeru strony) – po sprawdzeniu w źródle poprawia się bez uzgadniania; każda poprawka trafia do wykazu pytań jako informacja.
- Brak odpowiedzi autora – przekład zgodny z oryginałem; o przypisie tłumacza sygnalizującym problem decyduje redaktor prowadzący.
- Skróty i pominięcia (np. ilustracji z przyczyn licencyjnych) – wyłącznie za zgodą autora i z informacją w nocie.

---

### Projekt wpisu do § 17

| Wersja | Zmiana |
|---|---|
| 1.6 | § 12.2 Artykuły tłumaczone: metadane oryginału (wyjątki od § 1 pkt 8 i 9); § 12.1 nie dla przekładów; nota o przekładzie i wskazanie tłumacza; cytaty w pięciu sytuacjach; terminologia z bazy redakcji, rozstrzygnięcia tomu 18/2025 wiążące; nazwy grup w przekładzie (odstępstwo od § 6.3); przypisy nieautorskie (odrębny ciąg z gwiazdkami, wyjątek od § 7.1); ingerencje; bibliografia przy cytatach z wydań polskich. § 4.2: formuła `[tłum. własne]` nie w przekładach. § 11: `przyp. tłum.`, `przyp. red.` |

### Kwestie otwarte (▲) – zestawienie

Brak. Wszystkie punkty pierwotnego zestawienia rozstrzygnął redaktor prowadzący 25.09.2026; rozstrzygnięcia wpisano do tekstu powyżej. Przed włączeniem do kanonu: sprawdzić numerację paragrafów i numer wersji wobec aktualnego pełnego tekstu kanonu.
