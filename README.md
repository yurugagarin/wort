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
