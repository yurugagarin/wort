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

## v6

**Konu dersleri bağlantı kurarak öğretiyor.**

- **Ders sekmesi ve adım adım "Anla"**: her konu bildiğin bir şeyden başlar (köprü + hatırlama sorusu), hangi "büyük fikrin" parçası olduğunu gösterir, mantığını anlatır, bir Türkçe cümleden Almancasını adım adım kurar, Türkçe ile kıyaslar, "neden?" sorularıyla düşündürür, sık karıştırılanları ayırır, hafıza kancası verir ve ileride nerede karşına çıkacağını söyler. 40 konunun hepsi.
- **Bağlantı haritası**: 40 konu 9 büyük fikre bağlı (cümle mengenesi, yan cümlede fiil sona, bağlaç aileleri, hâller, sıfat ekleri, zaman çizgisi, Konjunktiv II, zu + mastar, fiil + edat). Her ailede konular ve ezber tabloları bir arada.
- **Daha az test**: Tanı 8, Kur 4 + 4, Pekiştir 8 soru.

**Hata koçu** (çevrimdışı):

- Yanlış cevapta hatanın türünü bulur (hâl seçimi, artikel cinsi, haben/sein, fiil eki, Umlaut ve Konjunktiv II, Partizip, zaman, zu, kelime sırası, yan cümlede fiil, bağlaç seçimi, karşılaştırma) ve ne yaptığını, neden olmadığını, nasıl düşünmen gerektiğini, neyle karıştırdığını ve neyi çalışman gerektiğini söyler.
- **Hata haritası**: hataların türlere göre birikir; Bugün'de "odak noktan", İlerleme'de son 14 günün özeti.
- **Yazı kontrolü**: Üret ve Schreiben'de yazdığın cümlelerde tipik hataları arar (fiil 2. sırada, yan cümlede fiil sonda, haben/sein, edattan sonra hâl, koymak/durmak fiilleri, özne-fiil uyumu, modal + mastar, isimlerde büyük harf).

## v7

- **Konuya geri dön**: konu sayfasında tamamlanmış her aşamanın yanında "Yeniden yap" var; "Bu konuyu baştan al" ile aşamalar sıfırlanır (yazdıkların ve notun kalır). "Biliyorum" diye işaretli konularda da aşamalar görünür.
- **Masaüstü**: geniş ekranda sol kenar çubuğu, iki-üç sütunlu düzen, geniş ders sayfası ve klavye kısayolları (1–4 şık seç, Enter devam, Esc kapat). Chrome/Edge'de "Uygulamayı yükle" ile ayrı bir masaüstü uygulaması olarak açılır. Aynı adres olduğu için her güncelleme iki cihazda da görünür.
- **Cihazlar arası senkron**: Ayarlar → "Cihazlar arası senkron". GitHub'da yalnız *gist* izinli bir anahtar oluşturulur, iki cihaza da yapıştırılır. Veriler hesabındaki gizli bir gist'te durur; her açılışta, değişiklikten birkaç saniye sonra ve açıkken 2 dakikada bir kayıpsız birleştirilerek eşitlenir.

## v8

- **Puan dökümü**: Bugün ekranında her görevin puanı (alınan / en fazla), ne yapıldığı ve **ne eksik kaldığı** ("Eksik: 4 kart", "Aşamayı bitir ya da 6 soru") ve kalan puanlar. "Puan nasıl hesaplanır?" açıklaması. Yeni dağılım: Kelime 30 · Konu 25 · Ezber 25 · Yazma 20.
- **Dakika girme kaldırıldı**: Hören, Sprechen ve Lesen dakika kayıtları yok. Yerine gerçek alıştırmalar: **Diktat** (cümle Almanca okunur, duyduğunu yazarsın, kelime kelime kontrol) ve kartlarda, örneklerde, kalıplarda 🔊 telaffuz.
- **Sorular denetlendi**: bütün konu soruları, ezber tabloları ve 2323 kelime tek tek kontrol edildi ve bağımsız ikinci bir kontrolden geçti. Birden fazla doğru şık kalmadı; yazarak cevapta eşdeğer doğrular kabul ediliyor; her yanlış şık için "neden yanlış" açıklaması var.
- **Cümle kurma**: bir cümlenin bütün doğru sıraları kabul ediliyor ve gösteriliyor ("Benimki de doğru" kalktı).
- **Ezber köşesi**: şıklar yalnız aynı türden hücrelerden (ek sorusunda ekler, fiil sorusunda o fiilin biçimleri). Her tabloda **hafıza teknikleri** (kısaltma, ritim, imge, hafıza sarayı, desen, Türkçe köprü …), **ritimle dinle** (satır satır, tekrar için aralıklı), **desenleri göster** (değişen ekler renkli), **boş tabloyu doldur** (ezberden yazma). Bugünün ezberi ve ezber yolu.
- **Masaüstü**: kenar çubuğunda Araçlar (Bağlantı haritası, Hata haritam, Diktat, Kalıplar, Ayarlar); puan kartı iki sütun; geniş tablolar tam tablo olarak.

## v9 · Rapor

- **? düğmesi:** Her sayfanın sağ üstünde. Bir soruda kafan karışınca bas, ne anlamadığını yaz. Not, o anki soruyla (seçenekler, senin cevabın, doğru cevap) birlikte saklanır.
- **Her cevap kaydedilir:** Günlük ve konu/tablo bazında doğru-yanlış sayıları; yanlışların ayrıntısı (son 800).
- **Rapor sayfası** (İlerleme sekmesi ya da masaüstünde Araçlar → Rapor · Claude): Son rapordan beri / 7 gün / 30 gün / tümü. "Raporu kopyala" ile claude.ai'ye yapıştırılacak metin hazırlanır. Metnin başında Claude'a ne yapacağı yazar: hata kalıpları, notlarına cevap, öncelikler, 7 günlük plan, alıştırma.
- Notlar ve cevap kayıtları senkronla iki cihazda birleşir.

## v10 · Kelime öğrenme yeniden

- **Önce tahmin:** Yeni kelime örnek cümlenin içinde gelir; anlamını 4 şıktan tahmin edersin, sonra kart açılır. İlk gerçek soru oturumun sonunda gelir.
- **Zorluk basamakları:** Türkçe → Almanca seç · artikeliyle yaz · cümlede boşluk doldur · sonra yaz/boşluk karışık. Doğru: bir basamak yukarı; artikel ya da yazım hatası: aynı basamak; yanlış: bir basamak aşağı. "Doğru hatırladın mı?" kaldırıldı.
- **Bağlantılar:** Kartta parçalar (Kühl + Schrank, ab- + fahren), birlikte kullanıldığı kalıplar ve kelime ailesi.
- **Hafıza kancası:** Her kartta 🪝 düğmesi: çevrimdışı ipuçları, "Claude'a kanca ürettir" (istek kopyalanır, claude.ai açılır) ve kendi kancan. Kanca kelime her geldiğinde görünür. 3 kez kaçan kelimede kanca kutusu kendiliğinden açılır.
- **Zor kelimeler kartı** (Kelime sekmesi): kancasız zor kelimeler için toplu istek; Claude'un `kelime :: kanca` cevabı yapıştırılınca kancalar kelimelere dağıtılır. Raporda da aynı istek var.
- **Yeni kelime sırası:** Başlangıç destesi (spor, mutfak…) kaldırıldı; önce A1, sonra A2, sonra B1.
- İsteğe bağlı: iyi bilinen kelimeyle kendi cümleni yaz, Yazma görevine eklenir.

## v11 · Araştırmaya göre kelime ezberi

- **FSRS-5 zamanlama:** SM-2 yerine açık kaynak FSRS (700+ milyon tekrardan öğrenilmiş varsayılan ağırlıklar). Her kartın kararlılığı ve zorluğu tutulur; tekrar, hatırlama ihtimali %90'a düştüğünde gelir. Eski kartlar ilk tekrarlarında kendiliğinden taşınır.
- **Dinleyerek tanıma:** İleri basamakta kelime sesli okunur, anlamını seçersin (Hören için de).
- **Kelimenin tamamı:** İleri basamakta isimlerde çoğul (die Tische), fiillerde Perfekt (ist gegangen) sorulur; yardımcı fiil hatası hata haritasına gider.
- **Farklı bağlamlar:** Boşluk sorusunda kelime kendi örneği dışında konu, kalıp ve ezber cümlelerinde de karşına çıkar.
- **Sesli söyle:** Kart açılınca ve cevaptan sonra kelime otomatik seslendirilir (ses ve hız değişir); Ayarlar'dan kapatılabilir.
- **Benzerlik karışması:** Aynı gün aynı kümeden (renkler, günler, aylar, sayılar, aile…) ya da aynı anlamdan iki yeni kelime gelmez.
- **Artikel imgesi:** der patlar, die alev alır, das cam gibi kırılır (renklerle birlikte).

## v12 · Hikâye kancası (Melik Duyar yöntemi)

- Her kelime kartında ikinci hafıza kancası: **📖 Hikâye kancası**. İki kural: 1) Almanca kelimenin okunuşuna benzeyen Türkçe kelime (ses benzeri), 2) onu anlamla birleştiren absürt, abartılı, somut, hareketli bir sahne. İsimlerde sahne artikel eylemiyle biter (der → mavi patlar, die → kırmızı alev alır, das → yeşil cam gibi kırılır).
- Havuzdaki kelimelerin hazır hikâyeleri `hikaye.json` dosyasında; ilk gerektiğinde bir kez indirilir.
- Yeni kelime tanıtılırken ve yanlış cevaptan sonra hikâye kendiliğinden açılır; "Kancam bu olsun" ile kalıcı kancan yapılır.
- Hazır hikâyesi olmayan kelimelerde (kendi eklediklerin, konu kelimeleri) "Claude'a hikâye yazdır" aynı kurallarla istek hazırlar.
