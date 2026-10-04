import re,sys
txt=open(sys.argv[1],encoding='utf-8',errors='replace').read()
txt=re.sub(r'-\s*\n\s*','',txt); txt=re.sub(r'\s+',' ',txt)
for p in sys.argv[2:]:
    pat=''
    for ch in p:
        if ch in 'sf': pat+='[sfſ]'
        elif ch==' ': pat+=r'[\s,;.:]*'
        elif ch.isalpha(): pat+='['+ch.lower()+ch.upper()+']'
        else: pat+=re.escape(ch)
    ms=list(re.finditer(pat,txt))
    print('==',p,len(ms))
    for m in ms[:2]: print('   ',txt[max(0,m.start()-300):m.end()+300])
