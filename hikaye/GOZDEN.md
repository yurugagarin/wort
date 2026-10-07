GÖREV: Eski hikâye kancalarını gözden geçir; yalnız ZAYIF olanları yeniden yaz.
Önce /home/user/wort/hikaye/TALIMAT.md dosyasını oku: biçim ve kurallar oradaki gibi (bütün heceler, sesi çok yakın Türkçe kelimeler, anlam hikâyede BÜYÜK HARFLE, somut, artikel eylemi YOK, yazı/söz ile anlam vermek YOK, anlam kopmasın, 2-3 cümle olabilir).
GİRDİ (eski satırlar): {IN}
Bir satır ZAYIF sayılır eğer: yalnız ilk hece karşılanmış ya da hece açıkta; ses benzerliği zorlama/uzak; ses kelimesi bilinmeyen bir sözcük; anlam hikâyede yok ya da kopuk; tabela/yazı/bağırma ile anlatılmış; soyut; sonu artikel eylemi (patlama/alev/cam) ile bitiyor ve gerisi de zayıf.
İyi satırlara DOKUNMA, yazma. Yalnız zayıfların yeni hâlini aynı biçimde ({anahtar} :: ...) üret.
KAYIT: Yeni satırları 10'arlık gruplar hâlinde tek Bash komutuyla ekle ve kaydet:
  cd /home/user/wort && cat >> {OUT} <<'SON'
  ...satırlar...
  SON
  flock .git/hikaye.lock sh -c 'git add {OUT} && git commit -q -m "Hikâye kancaları: eski zayıflar yenilendi" -- {OUT} && git push -q origin claude/adoring-brahmagupta-szc9qd' || true
Write aracını kullanma, doğrulama betiği yazma, başka iş yapma. Son mesajın yalnız: "bitti <yenilenen sayısı>/<incelenen sayısı>".
