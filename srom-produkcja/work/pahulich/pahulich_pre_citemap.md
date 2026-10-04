# cite_map report

| # | where | original | status | key(s) | becomes |
|---|---|---|---|---|---|
| 1 | line 7 | `(Demeter et al. 2000; Crowe 2007; Law and Kovats 2018; Kóczé 2020)` | **OK** | demeter2000, crowe2007, law2018, kocze2020 | `[^c1]` + `[^c1]: [@demeter2000; @crowe2007; @law2018; @kocze2020].` |
| 2 | line 7 | `(Matache 2016)` | **OK** | matache2016 | `[^c2]` + `[^c2]: [@matache2016].` |
| 3 | line 7 | `(Taba 2021)` | **OK** | taba2021 | `[^c3]` + `[^c3]: [@taba2021].` |
| 4 | line 11 | `(Césaire 2000)` | **OK** | cesaire2000 | `[^c4]` + `[^c4]: [@cesaire2000].` |
| 5 | line 19 (note m1) | `see Parvulescu and Boatcă 2022` | **IN-NOTE** | parvulescu2022 | `[zob. @parvulescu2022]` |
| 6 | line 23 | `Fraser (1992)` | **OK** | fraser1992 | `Fraser[^c5]` + `[^c5]: [@fraser1992].` |
| 7 | line 23 | `(2018, 78)` | **YEAR-ONLY** | law2018 | `[^c6]` + `[^c6]: [@law2018, s. 78]. (author named earlier in the paragraph)` |
| 8 | line 23 | `(quoted in Shahar 2007, 5)` | **OK** | shahar2007 | `[^c7]` + `[^c7]: [Cyt. za @shahar2007, s. 5].` |
| 9 | line 23 | `(quoted in Fraser 1992, 67)` | **OK** | fraser1992 | `[^c8]` + `[^c8]: [Cyt. za @fraser1992, s. 67].` |
| 10 | line 23 | `(Fraser 1992)` | **OK** | fraser1992 | `[^c9]` + `[^c9]: [@fraser1992].` |
| 11 | line 23 | `(Demeter et al. 2000, 31–32)` | **OK** | demeter2000 | `[^c10]` + `[^c10]: [@demeter2000, s. 31–32].` |
| 12 | line 23 | `Said (1978)` | **OK** | said1978 | `Said[^c11]` + `[^c11]: [@said1978].` |
| 13 | line 25 | `Robinson’s (2000)` | **OK** | robinson2000 | `Robinson’s[^c12]` + `[^c12]: [@robinson2000].` |
| 14 | line 25 | `(*Ibid.*, 2, 21)` | **PAGE-ONLY** | robinson2000 | `[^c13]` + `[^c13]: [@robinson2000, s. 2, 21]. (the work cited just before it)` |
| 15 | line 25 | `(*Ibid.*, 67)` | **PAGE-ONLY** | robinson2000 | `[^c14]` + `[^c14]: [@robinson2000, s. 67]. (the work cited just before it)` |
| 16 | line 27 | `(Wynter 2003; Shohat and Stam 2012; Baker 2018)` | **OK** | wynter2003, shohat2012, baker2018 | `[^c15]` + `[^c15]: [@wynter2003; @shohat2012; @baker2018].` |
| 17 | line 27 | `(Shohat and Stam 2012, 155)` | **OK** | shohat2012 | `[^c16]` + `[^c16]: [@shohat2012, s. 155].` |
| 18 | line 29 (note m2) | `Shohat and Stam 2012` | **IN-NOTE** | shohat2012 | `[@shohat2012]` |
| 19 | line 31 | `Wynter (2003)` | **OK** | wynter2003 | `Wynter[^c17]` + `[^c17]: [@wynter2003].` |
| 20 | line 31 | `(*Ibid.*, 309)` | **PAGE-ONLY** | wynter2003 | `[^c18]` + `[^c18]: [@wynter2003, s. 309]. (the work cited just before it)` |
| 21 | line 31 | `(*Ibid.*)` | **PAGE-ONLY** | wynter2003 | `[^c19]` + `[^c19]: [@wynter2003]. (the work cited just before it)` |
| 22 | line 31 | `(*Ibid*.)` | **PAGE-ONLY** | wynter2003 | `[^c20]` + `[^c20]: [@wynter2003]. (the work cited just before it)` |
| 23 | line 33 | `(2012, 37–38)` | **YEAR-ONLY** | law2012 | `[^c21]` + `[^c21]: [@law2012, s. 37–38]. (author named earlier in the paragraph)` |
| 24 | line 33 | `(quoted in Fraser 1992, 85)` | **OK** | fraser1992 | `[^c22]` + `[^c22]: [Cyt. za @fraser1992, s. 85].` |
| 25 | line 35 | `Fraser (1992)` | **OK** | fraser1992 | `Fraser[^c23]` + `[^c23]: [@fraser1992].` |
| 26 | line 35 | `(Fraser 1992; Crowe 2007)` | **OK** | fraser1992, crowe2007 | `[^c24]` + `[^c24]: [@fraser1992; @crowe2007].` |
| 27 | line 35 | `(Fraser 1992, 100)` | **OK** | fraser1992 | `[^c25]` + `[^c25]: [@fraser1992, s. 100].` |
| 28 | line 37 | `(Fraser 1992, 130)` | **OK** | fraser1992 | `[^c26]` + `[^c26]: [@fraser1992, s. 130].` |
| 29 | line 37 | `Confederation (1510)` | **NOT-CITED?** | — | `unchanged` + `name not in refs.json — left unchanged; if it IS a citation, add the work to refs.json` |
| 30 | line 37 | `England (1530)` | **NOT-CITED?** | — | `unchanged` + `name not in refs.json — left unchanged; if it IS a citation, add the work to refs.json` |
| 31 | line 37 | `France (1539)` | **NOT-CITED?** | — | `unchanged` + `name not in refs.json — left unchanged; if it IS a citation, add the work to refs.json` |
| 32 | line 37 | `(Crowe 2007, 34)` | **OK** | crowe2007 | `[^c27]` + `[^c27]: [@crowe2007, s. 34].` |
| 33 | line 37 | `(Mróz 2015, 96)` | **OK** | mroz2015 | `[^c28]` + `[^c28]: [@mroz2015, s. 96].` |
| 34 | line 37 | `(Law and Kovats 2018, 78–80)` | **OK** | law2018 | `[^c29]` + `[^c29]: [@law2018, s. 78–80].` |
| 35 | line 37 | `(*Ibid.*, 80)` | **PAGE-ONLY** | law2018 | `[^c30]` + `[^c30]: [@law2018, s. 80]. (the work cited just before it)` |
| 36 | line 39 | `(Crowe 2007)` | **OK** | crowe2007 | `[^c31]` + `[^c31]: [@crowe2007].` |
| 37 | line 39 | `(Mróz 2015)` | **OK** | mroz2015 | `[^c32]` + `[^c32]: [@mroz2015].` |
| 38 | line 39 | `(Červinski 2008)` | **OK** | chervinski2008 | `[^c33]` + `[^c33]: [@chervinski2008].` |
| 39 | line 39 | `(Hancock 1987; Gheorghe 1991; Achim 2004; Matache 2020)` | **OK** | hancock1987, gheorghe1991, achim2004, matache2020 | `[^c34]` + `[^c34]: [@hancock1987; @gheorghe1991; @achim2004; @matache2020].` |
| 40 | line 39 | `(Fraser 1992; Achim 2004)` | **OK** | fraser1992, achim2004 | `[^c35]` + `[^c35]: [@fraser1992; @achim2004].` |
| 41 | line 39 | `(Crowe 2007, 118)` | **OK** | crowe2007 | `[^c36]` + `[^c36]: [@crowe2007, s. 118].` |
| 42 | line 41 (note 2) | `(1992, 81)` | **YEAR-ONLY?** | — | `unchanged` + `year without a name: no single work of that year by an author named earlier in the note — left unchanged` |
| 43 | line 41 (note 2) | `Crowe 2007, 109` | **IN-NOTE** | crowe2007 | `[@crowe2007, s. 109]` |
| 44 | line 43 | `(Crowe 2007)` | **OK** | crowe2007 | `[^c37]` + `[^c37]: [@crowe2007].` |
| 45 | line 43 | `(*Ibid.*, 72–73)` | **PAGE-ONLY** | crowe2007 | `[^c38]` + `[^c38]: [@crowe2007, s. 72–73]. (the work cited just before it)` |
| 46 | line 43 | `(Horváthová 1964, 375–376; Demeter et al. 2000, 49)` | **OK** | horvathova1964, demeter2000 | `[^c39]` + `[^c39]: [@horvathova1964, s. 375–376; @demeter2000, s. 49].` |
| 47 | line 45 | `Mróz (2015)` | **OK** | mroz2015 | `Mróz[^c40]` + `[^c40]: [@mroz2015].` |
| 48 | line 45 | `(Fraser 1992; Zinevych 2001; Mróz 2015)` | **OK** | fraser1992, zinevych2001, mroz2015 | `[^c41]` + `[^c41]: [@fraser1992; @zinevych2001; @mroz2015].` |
| 49 | line 45 | `(Mróz 2015, 118–119)` | **OK** | mroz2015 | `[^c42]` + `[^c42]: [@mroz2015, s. 118–119].` |
| 50 | line 45 | `(Byelikov 2003; Mróz 2015, 17, 58)` | **OK** | bielikov2003, mroz2015 | `[^c43]` + `[^c43]: [@bielikov2003; @mroz2015, s. 17, 58].` |
| 51 | line 47 | `(Červinski 2008)` | **OK** | chervinski2008 | `[^c44]` + `[^c44]: [@chervinski2008].` |
| 52 | line 47 | `Litva (1588)` | **NOT-CITED?** | — | `unchanged` + `name not in refs.json — left unchanged; if it IS a citation, add the work to refs.json` |
| 53 | line 47 | `(Červinski 2008; Mróz 2015)` | **OK** | chervinski2008, mroz2015 | `[^c45]` + `[^c45]: [@chervinski2008; @mroz2015].` |
| 54 | line 47 | `(Byelikov 2003; Mróz 2015)` | **OK** | bielikov2003, mroz2015 | `[^c46]` + `[^c46]: [@bielikov2003; @mroz2015].` |
| 55 | line 47 | `(Mróz 2015, 161)` | **OK** | mroz2015 | `[^c47]` + `[^c47]: [@mroz2015, s. 161].` |
| 56 | line 47 | `(*Ibid.*, 254–255)` | **PAGE-ONLY** | mroz2015 | `[^c48]` + `[^c48]: [@mroz2015, s. 254–255]. (the work cited just before it)` |
| 57 | line 49 | `(Law and Kovats 2018, 81)` | **OK** | law2018 | `[^c49]` + `[^c49]: [@law2018, s. 81].` |
| 58 | line 49 | `(Demeter et al. 2000; Zinevych 2001; Mróz 2015)` | **OK** | demeter2000, zinevych2001, mroz2015 | `[^c50]` + `[^c50]: [@demeter2000; @zinevych2001; @mroz2015].` |
| 59 | line 49 | `(Byelikov 2003)` | **OK** | bielikov2003 | `[^c51]` + `[^c51]: [@bielikov2003].` |
| 60 | line 49 | `(Zelenchuk 1979, 213)` | **OK** | zelenchuk1979 | `[^c52]` + `[^c52]: [@zelenchuk1979, s. 213].` |
| 61 | line 49 | `(Demeter et al. 2000, 186; Shaidurov 2018, 204)` | **OK** | demeter2000, shaidurov2018 | `[^c53]` + `[^c53]: [@demeter2000, s. 186; @shaidurov2018, s. 204].` |
| 62 | line 51 | `(Zinevych 2001, 44)` | **OK** | zinevych2001 | `[^c54]` + `[^c54]: [@zinevych2001, s. 44].` |
| 63 | line 51 | `(Kistyakovskiy 1879, 820; see also Zinevych 2001; Byelikov 2008)` | **OK** | kistiakovskii1879, zinevych2001, bielikov2008 | `[^c55]` + `[^c55]: [@kistiakovskii1879, s. 820; zob. też @zinevych2001; @bielikov2008].` |
| 64 | line 51 | `(Zinevych 2001; Shaidurov 2018)` | **OK** | zinevych2001, shaidurov2018 | `[^c56]` + `[^c56]: [@zinevych2001; @shaidurov2018].` |
| 65 | line 51 | `(Smirnova-Seslavinskaya 2021, 85)` | **OK** | smirnovaseslavinskaya2021 | `[^c57]` + `[^c57]: [@smirnovaseslavinskaya2021, s. 85].` |
| 66 | line 53 | `(Zelenchuk 1979; Achim 2004; Byelikov 2008)` | **OK** | zelenchuk1979, achim2004, bielikov2008 | `[^c58]` + `[^c58]: [@zelenchuk1979; @achim2004; @bielikov2008].` |
| 67 | line 53 | `(Zelenchuk 1979, 213–216)` | **OK** | zelenchuk1979 | `[^c59]` + `[^c59]: [@zelenchuk1979, s. 213–216].` |
| 68 | line 55 | `(Byelikov 2003, 87)` | **OK** | bielikov2003 | `[^c60]` + `[^c60]: [@bielikov2003, s. 87].` |
| 69 | line 55 | `(Zinevych 2001, 48)` | **OK** | zinevych2001 | `[^c61]` + `[^c61]: [@zinevych2001, s. 48].` |
| 70 | line 57 | `(Crowe 2007)` | **OK** | crowe2007 | `[^c62]` + `[^c62]: [@crowe2007].` |
| 71 | line 61 | `(Willems 1997; Shmidt and Jaworsky 2020)` | **OK** | willems1997, shmidt2020 | `[^c63]` + `[^c63]: [@willems1997; @shmidt2020].` |
| 72 | line 61 | `(Willems 1997)` | **OK** | willems1997 | `[^c64]` + `[^c64]: [@willems1997].` |
| 73 | line 65 | `(Kirey and Serdyuk 1984, 113–114)` | **OK** | kirei1984 | `[^c65]` + `[^c65]: [@kirei1984, s. 113–114].` |
| 74 | line 65 | `(*Ibid.*, 118)` | **PAGE-ONLY** | kirei1984 | `[^c66]` + `[^c66]: [@kirei1984, s. 118]. (the work cited just before it)` |
| 75 | line 65 | `(Willems 1997, 44)` | **OK** | willems1997 | `[^c67]` + `[^c67]: [@willems1997, s. 44].` |
| 76 | line 67 | `(Shmidt and Jaworsky 2020, 57)` | **OK** | shmidt2020 | `[^c68]` + `[^c68]: [@shmidt2020, s. 57].` |
| 77 | line 67 | `(Willems 1997, 24)` | **OK** | willems1997 | `[^c69]` + `[^c69]: [@willems1997, s. 24].` |
| 78 | line 69 | `(2008, 183)` | **YEAR-ONLY** | hancock2008 | `[^c70]` + `[^c70]: [@hancock2008, s. 183]. (author named earlier in the paragraph)` |
| 79 | line 71 | `(2015, 11)` | **YEAR-ONLY** | mroz2015 | `[^c71]` + `[^c71]: [@mroz2015, s. 11]. (author named earlier in the paragraph)` |
| 80 | line 73 | `Roma, Grellmann (1807)` | **TRIMMED** | grellmann1807 | `Roma, Grellmann[^c72]` + `[^c72]: [@grellmann1807].` |
| 81 | line 73 | `(Willems 1997, 24)` | **OK** | willems1997 | `[^c73]` + `[^c73]: [@willems1997, s. 24].` |
| 82 | line 73 | `(*Ibid.*, 63–65)` | **PAGE-ONLY** | willems1997 | `[^c74]` + `[^c74]: [@willems1997, s. 63–65]. (the work cited just before it)` |
| 83 | line 75 | `(Fraser 1992; Shahar 2007)` | **OK** | fraser1992, shahar2007 | `[^c75]` + `[^c75]: [@fraser1992; @shahar2007].` |
| 84 | line 77 | `Wynter (2003)` | **OK** | wynter2003 | `Wynter[^c76]` + `[^c76]: [@wynter2003].` |
| 85 | line 79 | `(Wynter 2003, 265)` | **OK** | wynter2003 | `[^c77]` + `[^c77]: [@wynter2003, s. 265].` |
| 86 | line 81 | `(*Ibid.*, 266)` | **PAGE-ONLY** | wynter2003 | `[^c78]` + `[^c78]: [@wynter2003, s. 266]. (the work cited just before it)` |
| 87 | line 85 | `(Shahar 2007, 7)` | **OK** | shahar2007 | `[^c79]` + `[^c79]: [@shahar2007, s. 7].` |
| 88 | line 85 | `(cited in Lewy 2000, 2; see also Fernández 2021)` | **OK** | lewy2000, fernandez2021 | `[^c80]` + `[^c80]: [Cyt. za @lewy2000, s. 2; zob. też @fernandez2021].` |
| 89 | line 85 | `(1883, 140–142)` | **YEAR-ONLY** | dal1883 | `[^c81]` + `[^c81]: [@dal1883, s. 140–142]. (author named earlier in the paragraph)` |
| 90 | line 87 | `Likewise, Grellmann (1807)` | **TRIMMED** | grellmann1807 | `Likewise, Grellmann[^c82]` + `[^c82]: [@grellmann1807].` |
| 91 | line 87 | `(1807, viii)` | **YEAR-ONLY** | grellmann1807 | `[^c83]` + `[^c83]: [@grellmann1807, s. viii]. (author named earlier in the paragraph)` |
| 92 | line 87 | `(*Ibid*.)` | **PAGE-ONLY** | grellmann1807 | `[^c84]` + `[^c84]: [@grellmann1807]. (the work cited just before it)` |
| 93 | line 87 | `(Clark 2004, 231)` | **OK** | clark2004 | `[^c85]` + `[^c85]: [@clark2004, s. 231].` |
| 94 | line 89 | `(1807, i)` | **YEAR-ONLY** | grellmann1807 | `[^c86]` + `[^c86]: [@grellmann1807, s. i]. (author named earlier in the paragraph)` |
| 95 | line 91 | `(1807, 6)` | **YEAR-ONLY** | grellmann1807 | `[^c87]` + `[^c87]: [@grellmann1807, s. 6]. (author named earlier in the paragraph)` |
| 96 | line 91 | `(*Ibid.*, 13)` | **PAGE-ONLY** | grellmann1807 | `[^c88]` + `[^c88]: [@grellmann1807, s. 13]. (the work cited just before it)` |
| 97 | line 93 | `(1807, 89)` | **YEAR-ONLY** | grellmann1807 | `[^c89]` + `[^c89]: [@grellmann1807, s. 89]. (author named earlier in the paragraph)` |
| 98 | line 93 | `(*Ibid.*, 72–73)` | **PAGE-ONLY** | grellmann1807 | `[^c90]` + `[^c90]: [@grellmann1807, s. 72–73]. (the work cited just before it)` |
| 99 | line 93 | `(*Ibid.*, 25)` | **PAGE-ONLY** | grellmann1807 | `[^c91]` + `[^c91]: [@grellmann1807, s. 25]. (the work cited just before it)` |
| 100 | line 97 | `Wippermann (1997)` | **OK** | wippermann1997 | `Wippermann[^c92]` + `[^c92]: [@wippermann1997].` |
| 101 | line 101 | `(2019, 119)` | **YEAR-ONLY** | law2019 | `[^c93]` + `[^c93]: [@law2019, s. 119]. (author named earlier in the paragraph)` |
| 102 | line 103 | `Melamed (2015)` | **OK** | melamed2015 | `Melamed[^c94]` + `[^c94]: [@melamed2015].` |
| 103 | line 103 | `(2015, 28)` | **YEAR-ONLY** | vincze2015 | `[^c95]` + `[^c95]: [@vincze2015, s. 28]. (author named earlier in the paragraph)` |
| 104 | line 105 | `Robinson (2000)` | **OK** | robinson2000 | `Robinson[^c96]` + `[^c96]: [@robinson2000].` |
| 105 | line 105 | `(*Ibid.*, 27)` | **PAGE-ONLY** | robinson2000 | `[^c97]` + `[^c97]: [@robinson2000, s. 27]. (the work cited just before it)` |
| 106 | line 107 | `Jenkins and Leroy (2021)` | **NOT-CITED?** | — | `unchanged` + `name not in refs.json — left unchanged; if it IS a citation, add the work to refs.json` |
| 107 | line 109 | `(2000, 67)` | **YEAR-ONLY** | robinson2000 | `[^c98]` + `[^c98]: [@robinson2000, s. 67]. (author named earlier in the paragraph)` |
| 108 | line 109 | `(*Ibid.*, 42)` | **PAGE-ONLY** | robinson2000 | `[^c99]` + `[^c99]: [@robinson2000, s. 42]. (the work cited just before it)` |
| 109 | line 111 | `(see Melamed 2015)` | **OK** | melamed2015 | `[^c100]` + `[^c100]: [Zob. @melamed2015].` |
| 110 | line 111 | `(Grellmann 1807)` | **OK** | grellmann1807 | `[^c101]` + `[^c101]: [@grellmann1807].` |
| 111 | line 111 | `(Willems 1997; Lucassen 1998)` | **OK** | willems1997, lucassen1998 | `[^c102]` + `[^c102]: [@willems1997; @lucassen1998].` |
| 112 | line 113 | `Federici (2004)` | **OK** | federici2004 | `Federici[^c103]` + `[^c103]: [@federici2004].` |
| 113 | line 113 | `(*Ibid.*, 46)` | **PAGE-ONLY** | federici2004 | `[^c104]` + `[^c104]: [@federici2004, s. 46]. (the work cited just before it)` |
| 114 | line 115 | `(Federici 2004, 45)` | **OK** | federici2004 | `[^c105]` + `[^c105]: [@federici2004, s. 45].` |
| 115 | line 115 | `(*Ibid.*, 49)` | **PAGE-ONLY** | federici2004 | `[^c106]` + `[^c106]: [@federici2004, s. 49]. (the work cited just before it)` |
| 116 | line 115 | `(*Ibid.*, 64)` | **PAGE-ONLY** | federici2004 | `[^c107]` + `[^c107]: [@federici2004, s. 64]. (the work cited just before it)` |
| 117 | line 115 | `(*Ibid.*)` | **PAGE-ONLY** | federici2004 | `[^c108]` + `[^c108]: [@federici2004]. (the work cited just before it)` |
| 118 | line 117 | `(Federici 2004, 69–70; see also Acton 1974)` | **OK** | federici2004, acton1974 | `[^c109]` + `[^c109]: [@federici2004, s. 69–70; zob. też @acton1974].` |
| 119 | line 119 | `(Lucassen 2008, 430)` | **OK** | lucassen2008 | `[^c110]` + `[^c110]: [@lucassen2008, s. 430].` |
| 120 | line 119 | `(Willems 1997, 8)` | **OK** | willems1997 | `[^c111]` + `[^c111]: [@willems1997, s. 8].` |
| 121 | line 119 | `(2015, 81)` | **YEAR-ONLY** | melamed2015 | `[^c112]` + `[^c112]: [@melamed2015, s. 81]. (author named earlier in the paragraph)` |
| 122 | line 119 | `(Robinson 2000; Federici 2004)` | **OK** | robinson2000, federici2004 | `[^c113]` + `[^c113]: [@robinson2000; @federici2004].` |
| 123 | line 121 | `(Lucassen 2008)` | **OK** | lucassen2008 | `[^c114]` + `[^c114]: [@lucassen2008].` |
| 124 | line 121 | `(1997, 8–9)` | **YEAR-ONLY** | willems1997 | `[^c115]` + `[^c115]: [@willems1997, s. 8–9]. (author named earlier in the paragraph)` |
| 125 | line 121 | `(*Ibid.*, 14–15)` | **PAGE-ONLY** | willems1997 | `[^c116]` + `[^c116]: [@willems1997, s. 14–15]. (the work cited just before it)` |
| 126 | line 121 | `(Willems 1997; Lucassen 1998)` | **OK** | willems1997, lucassen1998 | `[^c117]` + `[^c117]: [@willems1997; @lucassen1998].` |
| 127 | line 121 | `(Zinevych 2001; Mróz 2015)` | **OK** | zinevych2001, mroz2015 | `[^c118]` + `[^c118]: [@zinevych2001; @mroz2015].` |
| 128 | line 121 | `(Mróz 2015, 128)` | **OK** | mroz2015 | `[^c119]` + `[^c119]: [@mroz2015, s. 128].` |
| 129 | line 123 | `(quoted in Mróz 2015, 129)` | **OK** | mroz2015 | `[^c120]` + `[^c120]: [Cyt. za @mroz2015, s. 129].` |
| 130 | line 123 | `(1544)` | **YEAR-ONLY?** | — | `unchanged` + `year without a name: no single work of that year by an author named earlier in the paragraph — left unchanged` |
| 131 | line 123 | `(Mróz 2015, 131)` | **OK** | mroz2015 | `[^c121]` + `[^c121]: [@mroz2015, s. 131].` |
| 132 | line 123 | `(quoted in Mróz 2015, 131–132)` | **OK** | mroz2015 | `[^c122]` + `[^c122]: [Cyt. za @mroz2015, s. 131–132].` |
| 133 | line 125 | `(Mróz 2015, 233–234)` | **OK** | mroz2015 | `[^c123]` + `[^c123]: [@mroz2015, s. 233–234].` |
| 134 | line 129 | `(Willems 1997, 22–23)` | **OK** | willems1997 | `[^c124]` + `[^c124]: [@willems1997, s. 22–23].` |
| 135 | line 129 | `(*Ibid*., 8)` | **PAGE-ONLY** | willems1997 | `[^c125]` + `[^c125]: [@willems1997, s. 8]. (the work cited just before it)` |
| 136 | line 129 | `(1807, 108)` | **YEAR-ONLY** | grellmann1807 | `[^c126]` + `[^c126]: [@grellmann1807, s. 108]. (author named earlier in the paragraph)` |
| 137 | line 129 | `(*Ibid.*, 26, 85)` | **PAGE-ONLY** | grellmann1807 | `[^c127]` + `[^c127]: [@grellmann1807, s. 26, 85]. (the work cited just before it)` |
| 138 | line 131 | `(1807, 87)` | **YEAR-ONLY** | grellmann1807 | `[^c128]` + `[^c128]: [@grellmann1807, s. 87]. (author named earlier in the paragraph)` |
| 139 | line 131 | `(*Ibid.*, 69–70)` | **PAGE-ONLY** | grellmann1807 | `[^c129]` + `[^c129]: [@grellmann1807, s. 69–70]. (the work cited just before it)` |
| 140 | line 133 | `(Smirnova-Seslavinskaya 2021, 91)` | **OK** | smirnovaseslavinskaya2021 | `[^c130]` + `[^c130]: [@smirnovaseslavinskaya2021, s. 91].` |
| 141 | line 133 | `(O’Keeffe 2014)` | **OK** | okeeffe2014 | `[^c131]` + `[^c131]: [@okeeffe2014].` |
| 142 | line 135 | `(O’Keeffe 2014, 125)` | **OK** | okeeffe2014 | `[^c132]` + `[^c132]: [@okeeffe2014, s. 125].` |
| 143 | line 135 | `(Holler 2015, 84)` | **OK** | holler2015 | `[^c133]` + `[^c133]: [@holler2015, s. 84].` |
| 144 | line 135 | `Barannikov (1931)` | **OK** | barannikov1931 | `Barannikov[^c134]` + `[^c134]: [@barannikov1931].` |
| 145 | line 135 | `(1931, 74)` | **YEAR-ONLY** | barannikov1931 | `[^c135]` + `[^c135]: [@barannikov1931, s. 74]. (author named earlier in the paragraph)` |
| 146 | line 135 | `(O’Keeffe 2014, 126)` | **OK** | okeeffe2014 | `[^c136]` + `[^c136]: [@okeeffe2014, s. 126].` |
| 147 | line 135 | `(Zinevych 2001; Byelikov 2008)` | **OK** | zinevych2001, bielikov2008 | `[^c137]` + `[^c137]: [@zinevych2001; @bielikov2008].` |
| 148 | line 143 | `(Marsh 2008)` | **OK** | marsh2008 | `[^c138]` + `[^c138]: [@marsh2008].` |
| 149 | line 143 | `(Césaire 2000)` | **OK** | cesaire2000 | `[^c139]` + `[^c139]: [@cesaire2000].` |

Totals: IN-NOTE 3, NOT-CITED? 5, OK 95, PAGE-ONLY 25, TRIMMED 2, YEAR-ONLY 17, YEAR-ONLY? 2
