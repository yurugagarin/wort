# WORT

A2'den B1'e kişisel Almanca defteri. FORM ailesinden: aynı mimari, aynı tasarım dili.

- Tek dosya `index.html` (CSS ve JS içinde), derleme adımı ve kütüphane yok.
- iPhone'da ana ekrana eklenen PWA: `manifest.webmanifest`, `logo.svg`, `icon-180.png`, `sw.js` (yalnız kurulum için, önbellek yok).
- Veri cihazda: `localStorage`, tek anahtar `wort:v1`, sürümlü JSON. Ayarlar'dan JSON yedek dışa/içe aktarılır.
- GitHub Pages: `main` dalı, kök klasör.

## v1

- **Heute**: 0–100 günlük puan. Kelime tekrarı 30 · gramer 15 · Hören 20 (10 dk = tam) · Schreiben 20 (3 cümle = tam) · Sprechen 15. Kısmi puan var.
- **Seri ve minimum gün**: kelime görevi bitince gün seriye sayılır; yalnız kelime yapılan gün takvimde sarı görünür.
- **Wörter**: SM-2 benzeri aralıklı tekrar (Tekrar / Zor / Kolay), isimlerde önce artikel; artikel kuralı ve çoğul cevaptan sonra. Uygulamanın içinde A1–B1 arası ~2300 kelimelik havuz; her gün seçili seviyelerden karışık yeni kartlar. Kendi kelimeni ekleme, havuzda arama.
- **Übungen**: Artikel-Blitz (60 sn), Lücke (boşluk doldurma), Satzbau (karışık kelimelerden cümle).
- **Weg**: Menschen sırasına yakın A2.1 → B1.2 gramer haritası (40 konu, her biri anlatım + 6 cümle kurma alıştırması), dört beceri çubuğu, sınav geri sayımı.
- **Woche**: puan takvimi ve haftalık özet.

## v2

- Her gramer konusu için Türkçe özet (ne işe yarar, nasıl kurulur, dikkat, Türkçe ile karşılaştırma).
- Konu başına "Kurs notum" alanı ve "Bugün bunu çalış" düğmesi: kursta işlenen konu günün gramer görevi olur.

Sonraki sürümler: Claude ile yazma/konuşma düzeltmesi, ses kaydı arşivi, Almanca haftalık özet, bildirimler.

Kelime havuzu, Goethe listelerinin konu ve sıklık mantığına göre bu proje için hazırlandı; resmî listelerin kopyası değildir.

## v3

Uygulamanın omurgası artık konular.

- **Bugün**: tek "Sıradaki adım" düğmesi ve 5 adımlı günlük plan, günün kalıbı.
- **Konular**: A2.1 → B1.2 arası 40 konu. Her konu bir ders: Türkçe özet, konunun kelimeleri, 8 boşluk doldurma + cümle kurma, yüzde ilerleme. %80 = oturdu; sonra 2, 5, 12, 30 gün sonra tekrar.
- **Seviye testi**: 30 kelime + 40 gramer sorusu; bilinen konular %50'den başlar, bilinmeyenler öncelikli olur.
- **Kelimeler**: tam ekran kelime tekrarı (Türkçe karşılık büyük), Kalıplar (A1/A2/B1 hazır cümleler), Artikel-Blitz, Lücke, Satzbau.
- **Defter**: "bunu demek istedim / bunu duydum" notları; çevrimdışı ön analiz (hangi konu, senin seviyende mi, daha basit nasıl söylenir) ve Claude'a yapıştırmak için hazır mesaj.
- **İlerleme**: A2/B1 yüzdesi, bitiş tahmini, sınava bugün girsen modül tahmini, puan takvimi.
- Alt sayfalar yerine tam ekran sayfalar (sağa sola kayma giderildi).

## v5

**Konu dersleri derinleşti: her konu 5 aşama, günlere yayılır (~1 hafta).**

1. **Anla**: tam Türkçe özet, 6 örnek cümle, "kendine anlat" adımı, 4 "hangisi doğru?" sorusu.
2. **Tanı**: 12 şıklı boşluk doldurma (konu başına 12 soru), %75 ile geçilir.
3. **Kur**: 6 soruda cevabı yazarak verirsin (ä ö ü ß tuşları, ipucu), 6 cümleyi kendin kurarsın; %70 ile geçilir.
4. **Üret** (ertesi gün açılır): kendi hayatından en az 3 cümle, kontrol listesi, isteğe bağlı "Claude'a düzelttir" kopyası. Yazdıkların Schreiben görevine de sayılır.
5. **Pekiştir**: 1, 3, 7, 14, 30 gün arayla 12 soruluk karışık tekrar (2 soru önceki konulardan). 2 başarılı tekrar = konu oturdu.

Dayanak: geri çağırma pratiği ve aralıklı tekrar (Dunlosky vd. 2013), karışık çalışma, kendine açıklama, açık anlatım + önce tanıma sonra üretme (Norris & Ortega 2000; VanPatten).

**Ezber köşesi** (yeni sekme, konu derslerinden ayrı): A1 / A2 / B1 olarak ayrılmış 33 tablo (zamirler, artikeller, iyelik, Präsens, sein/haben, Modalverben, ön ekler, Wo/Wohin/Woher, edatlar, TeKaMoLo, bağlaçlar, Präteritum, Perfekt, sıfat ekleri, Genitiv, Relativpronomen, Konjunktiv II, Passiv …). Her tabloda ezber taktiği (DOGFU, „aus bei mit nach seit von zu“ şarkısı, m-r-m-n, be-emp-ent-er-ge-miss-ver-zer …), sesli dinleme, "Kapat ve hatırla", 12 soruluk test (bildiğin hücreler yazarak sorulur), hücre bazında ilerleme ve 1-3-7-14-30 gün aralıklı tekrar.
