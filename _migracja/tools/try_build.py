import json,subprocess,tempfile,os,glob,re,sys
src, refsfiles, groups = sys.argv[1], sys.argv[2].split(","), json.loads(sys.argv[3])
P=os.path.abspath("build/srom-cowork/plugin/srom/skills")
refs=[r for f in refsfiles for r in json.load(open(f,encoding="utf-8"))]
B=open(src,encoding="utf-8").read().split("\n\n")
for s in groups:
    T=tempfile.mkdtemp(); os.makedirs(f"{T}/input")
    r0=subprocess.run(["python3","tools/excerpt.py",src,f"{T}/input/x.md"]+[str(i) for i in s],capture_output=True,text=True)
    if r0.returncode: print(s,"EXCERPT ERR",r0.stderr[-100:]); continue
    keys=set(r0.stdout.split())
    json.dump([r for r in refs if r["id"] in keys],open(f"{T}/input/refs.json","w",encoding="utf-8"),ensure_ascii=False)
    r=subprocess.run([os.path.expanduser("~/.venvs/srom/bin/python"),f"{P}/srom-produkcja/scripts/build.py","input/x.md","--refs","input/refs.json","--out","e"],cwd=T,capture_output=True,text=True)
    g=glob.glob(f"{T}/e/*_report.md"); rep=open(g[0],encoding="utf-8").read() if g else r.stderr[-150:]
    ib=re.search(r"Ibidem notes to check after layout: (\d+)",rep); fn=re.search(r"footnotes: (\d+)",rep)
    err=rep.split("## Errors")[1].split("\n##")[0].strip()[:120].replace("\n"," / ") if "## Errors" in rep else ""
    print(s, "PASS" if "RESULT: PASS" in rep else "FAIL", "fn",fn and fn.group(1),"ibid",ib and ib.group(1),"keys",len(keys), err, T)
