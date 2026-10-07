GÖREV: Eski hikâye kancalarını gözden geçir; yalnız ZAYIF olanları yeniden yaz.
Önce /home/user/wort/hikaye/TALIMAT.md dosyasını oku: biçim ve kurallar oradaki gibi (bütün heceler, sesi çok yakın Türkçe kelimeler, anlam hikâyede BÜYÜK HARFLE, somut, artikel eylemi YOK, yazı/söz ile anlam vermek YOK, anlam kopmasın, 2-3 cümle olabilir).
GİRDİ (eski satırlar): {IN}
İKİNCİ, DAHA KATI TUR. Kullanıcının yakaladığı kötü örnek:
  KÖTÜ: der Liegestütz = LİG + EŞ + TÜTSÜ | ŞINAV | Süper LİG finalinde EŞin elinde TÜTSÜ yakıp seni ŞINAV çekmeye zorluyor... (EŞ sese uymuyor, anlamsız ara parça; TÜTSÜ ile şınav arasında bağ yok; hikâye kısa ve saçma)
  İYİ:  der Liegestütz = LİGE + ŞUT | ŞINAV | Süper LİGE yeni transfer oldun; hoca kaçırdığın her ŞUT için seni çimlere yatırıp ŞINAV çektiriyor. Burnun çimlere gömülüyor, kolların yanıyor, tribünler sayıyor: doksan sekiz, doksan dokuz, yüz!
Ayrıca ZAYIF: sese uymayan ya da hikâyede işlevi olmayan dolgu parça (EŞ, FİLAN gibi), ses kelimesi ile anlam arasında mantıklı neden-sonuç bağı yoksa, olaylar birbirinden kopuksa, hikâye sahneyi kuramayacak kadar kısaysa.
Bir satır ZAYIF sayılır eğer: yalnız ilk hece karşılanmış ya da hece açıkta; ses benzerliği zorlama/uzak; ses kelimesi bilinmeyen bir sözcük; anlam hikâyede yok ya da kopuk; tabela/yazı/bağırma ile anlatılmış; soyut; sonu artikel eylemi (patlama/alev/cam) ile bitiyor ve gerisi de zayıf.
İyi satırlara DOKUNMA, yazma. Yalnız zayıfların yeni hâlini aynı biçimde ({anahtar} :: ...) üret.
KAYIT: Yeni satırları 10'arlık gruplar hâlinde tek Bash komutuyla ekle ve kaydet:
  cd /home/user/wort && cat >> {OUT} <<'SON'
  ...satırlar...
  SON
  flock .git/hikaye.lock sh -c 'git add {OUT} && git commit -q -m "Hikâye kancaları: eski zayıflar yenilendi" -- {OUT} && git push -q origin claude/adoring-brahmagupta-szc9qd' || true
Write aracını kullanma, doğrulama betiği yazma, başka iş yapma. Son mesajın yalnız: "bitti <yenilenen sayısı>/<incelenen sayısı>".
