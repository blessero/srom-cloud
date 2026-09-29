# Gates: 1.3.5c Training corpus, batch 3 (Urbanek's review of Gawin)

Opened 29.09.2026 14:18 [general]. One text arrived in `training/` during leaf 1.3.2: B. Urbanek's review of M. Gawin, *Rasa
i nowoczesność. Historia polskiego ruchu eugenicznego (1880–1952)* (2003), „Medycyna Nowożytna” 11/1 (2004). Harvest
per schema § Admission: no row passes (period eugenics vocabulary is decided per case), so the register gets a cluster.

- [x] G1: registered (key, bibliographic line) and hashed; all hashes match (10 files: the Kubica DOCX left the folder, its conversion stays)
  CHECK: cd training && shasum -a 256 -c manifest.sha256 | grep -c ': OK$' && grep -c '^urbanek' sources.tsv
  EXPECT: /^10\n1$/m

- [x] G2: register cluster B10 (eugenics) cites [urbanek] and every quoted form is in the text
  CHECK: python3 -c "import re;t=open('tlumacz-rasa.md').read();b=t.split('### B10',1)[1].split('\n## ',1)[0];s=open('training/Bozena_Urbanek_Recenzja_Magdalena_Gawin_Rasa_i_nowoczesnosc.md').read();q=[x for x in re.findall(r'„([^”]+)” \[urbanek\]',b)];print('B10 forms found: %d/%d'%(sum(x in s for x in q),len(q)))"
  EXPECT: /^B10 forms found: ([1-9]\d*)\/\1$/m

- [x] G3: termbase checks still green; committed
  CHECK: ~/.venvs/srom/bin/python tlumacz-check_tb.py --evidence | tail -1 && git log -1 --format=%s
  EXPECT: /candidate rows: \d+, each with a verified training quote\n.*1\.3\.5c/m
