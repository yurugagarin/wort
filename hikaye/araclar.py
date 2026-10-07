# Hikâye kancası hattı: kelime listesi, eksikleri bölme (todo), birleştirme (merge).
# Kullanım: python3 hikaye/araclar.py todo 6   |   python3 hikaye/araclar.py merge
import re,os,glob,json,sys
R=os.path.dirname(os.path.abspath(__file__))+'/'
W=os.path.dirname(R.rstrip('/'))+'/'
def pool():
    s=open(W+'index.html',encoding='utf-8').read()
    m=re.search(r'<script[^>]*id="pool"[^>]*>(.*?)</script>',s,re.S)
    seen=set();w=[]
    for l in m.group(1).split('\n'):
        f=l.strip().split('|')
        if len(f)<6 or f[0] not in('1','2','3'):continue
        k=(f[2]+' ' if f[2] else '')+f[3]
        if k in seen:continue
        seen.add(k);w.append((int(f[0]),k,f[5]))
    w.sort(key=lambda x:x[0]);return w
def parse():
    keys={k for _,k,_ in pool()};out={};bad=[]
    for f in sorted(glob.glob(R+'parca/*.txt')):
        for l in open(f,encoding='utf-8'):
            l=l.strip()
            if '::' not in l:continue
            k,v=l.split('::',1);k=k.strip().strip('`*- ')
            p=[x.strip() for x in v.split(' | ')]
            if k not in keys or len(p)!=3 or ' = ' not in p[0] or len(p[2])<25 or not p[1]:bad.append(l[:100]);continue
            syl,snd=p[0].split(' = ',1);out[k]=[syl.strip(),snd.strip(),p[1],p[2]]
    return out,bad
cmd=sys.argv[1] if len(sys.argv)>1 else 'merge'
if cmd=='todo':
    n=int(sys.argv[2]) if len(sys.argv)>2 else 6;minlv=int(sys.argv[3]) if len(sys.argv)>3 else 2
    done,_=parse();todo=[(l,k,t) for l,k,t in pool() if l>=minlv and k not in done]
    for f in glob.glob(R+'girdi/*.txt'):os.remove(f)
    size=(len(todo)+n-1)//n if todo else 0
    for i in range(n):
        part=todo[i*size:(i+1)*size]
        if part:open(R+'girdi/g%02d.txt'%(i+1),'w',encoding='utf-8').write('\n'.join(k+' = '+t for _,k,t in part)+'\n')
    print('kalan',len(todo),'grup basina',size)
else:
    cur=json.load(open(W+'hikaye.json',encoding='utf-8'))
    res={k:v for k,v in cur.items() if len(v)<4}  # eski biçim yalnız yedek
    new,bad=parse();res.update(new)
    json.dump(res,open(W+'hikaye.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
    print('yeni bicim',len(new),'toplam',len(res),'hatali',len(bad))
