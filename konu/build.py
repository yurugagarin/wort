#!/usr/bin/env python3
"""Soru bankası derleyici: konu/sorular/gN.txt → index.html içindeki <script id="qbank"> bloğu.

Satır biçimi (alanlar | ile ayrılır; # ile başlayan ve boş satırlar atlanır):
  Y|boşluklu cümle ___ (ipucu)|cevap|başka doğru cevaplar a/b|açıklama          boşluğa yaz
  S|boşluklu cümle ___|doğru|yanlış1|yanlış2|açıklama                            şıklı boşluk
  H|hatalı cümle|düzeltilmiş cümle|başka doğru biçimler a/b|açıklama              hata bul
  H|doğru cümle|=|açıklama                                                       hata yok
  D|yönerge|kaynak cümle|hedef cümle|başka doğru biçimler a/b|açıklama            dönüştür
  C|Türkçe cümle|Almanca cümle|başka doğru çeviriler a/b|açıklama                 çevir
  K|Almanca cümle|Türkçesi|başka doğru sıralar a/b                                cümle kur
  O|Almanca parça|Türkçesi|soru~doğru~yanlış1~yanlış2|soru~doğru~yanlış1~yanlış2  okuma parçası
Açıklamalarda *…* Almanca biçimi kalın gösterir. Soru anahtarı içerikten türetilir (q + 7 hane)."""
import hashlib, json, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'konu' / 'sorular'
HTML = ROOT / 'index.html'
NEED = {'Y': 2, 'S': 4, 'H': 2, 'D': 3, 'C': 2, 'K': 2, 'O': 3}

def key(t, f):
    return 'q' + hashlib.sha1((t + '|' + f[0] + '|' + (f[1] if len(f) > 1 else '')).encode()).hexdigest()[:7]

def norm(s):
    s = s.lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    return re.sub(r'\s+', ' ', re.sub(r'[.,!?;:"\'„“()]', '', s)).strip()

def check(tid, n, t, f, errs):
    w = lambda m: errs.append(f'{tid}:{n}: {t}: {m}')
    if t in ('Y', 'S') and f[0].count('___') != 1: w('tam bir ___ olmalı')
    if t == 'S' and len({norm(x) for x in f[1:4]}) < 3: w('şıklar farklı olmalı')
    if t == 'H' and f[1] != '=' and norm(f[0]) == norm(f[1]): w('düzeltilmiş cümle aynı')
    if t == 'D' and norm(f[1]) == norm(f[2]): w('hedef kaynakla aynı')
    if t == 'K' and not re.search(r'[.!?]$', f[0]): w('cümle noktalama ile bitmeli')
    if t == 'O':
        for q in f[2:]:
            p = q.split('~')
            if len(p) < 3: w('okuma sorusu soru~doğru~yanlış biçiminde olmalı')
            elif len({norm(x) for x in p[1:]}) < len(p) - 1: w('okuma şıkları farklı olmalı')

def build():
    bank, errs, stats = {}, [], {}
    for fp in sorted(SRC.glob('g*.txt'), key=lambda p: int(re.sub(r'\D', '', p.stem) or 0)):
        tid = fp.stem
        items, seen = [], set()
        for n, line in enumerate(fp.read_text(encoding='utf-8').splitlines(), 1):
            line = line.strip()
            if not line or line.startswith('#'): continue
            parts = [x.strip() for x in line.split('|')]
            t, f = parts[0], parts[1:]
            if t not in NEED: errs.append(f'{tid}:{n}: bilinmeyen tür {t}'); continue
            if len(f) < NEED[t]: errs.append(f'{tid}:{n}: {t}: alan eksik'); continue
            check(tid, n, t, f, errs)
            k = key(t, f)
            if k in seen: errs.append(f'{tid}:{n}: aynı soru iki kez'); continue
            seen.add(k)
            items.append({'t': t, 'k': k, 'f': f})
        bank[tid] = items
        st = {}
        for it in items: st[it['t']] = st.get(it['t'], 0) + 1
        stats[tid] = st
    return bank, errs, stats

def main():
    bank, errs, stats = build()
    for tid, st in stats.items():
        print(tid, sum(st.values()), ' '.join(f'{k}{v}' for k, v in sorted(st.items())))
    if errs:
        print('\n'.join(errs)); sys.exit(1)
    data = json.dumps(bank, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    html = HTML.read_text(encoding='utf-8')
    block = '<script type="application/json" id="qbank">' + data + '</script>\n'
    m = re.search(r'<script type="application/json" id="qbank">.*?</script>\n', html, re.S)
    if m: html = html[:m.start()] + block + html[m.end():]
    else:
        i = html.index('<script>\n(function(){')
        html = html[:i] + block + html[i:]
    HTML.write_text(html, encoding='utf-8')
    print('yazıldı:', sum(len(v) for v in bank.values()), 'satır')

if __name__ == '__main__':
    main()
