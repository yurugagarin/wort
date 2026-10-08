# Denetim · KONULAR (gramer konuları): yaşam döngüsü ve durum gösterimi

Test ortamı: Playwright, saat sabitlenip gün atlatıldı. Betikler `scratchpad/v22/konu/` altında:
- `lib.js`: ortak yardımcılar (gün atlatma, aşamayı doğru/yanlış cevaplarla bitirme, Konular/Bugün/konu sayfası okuma)
- `akis1.js` → `akis1.out`: g1 (Perfekt) baştan sona: Anla → Tanı (önce başarısız, sonra geçer) → Kur → ertesi gün Üret → 1., 2. (önce başarısız) ve 3. tekrar (başarısız)
- `akis2.js` → `akis2.out`: paralel konular, gfocus, başarısız tekrardan sonraki öneri, Üret'i yeniden yapma, yanlışları tekrar, Anla eşiği, "Zaten biliyorum"
- `akis3.js` → `akis3.out`, `akis3c.js`: serbest alıştırma, tekrar sonrası "yanlışları tekrar", aynı gün ikinci tekrar, aynı gün vadesi gelen iki konu
- `akis4.js` → `akis4.out`: oturmuş konuda aşamayı yeniden yapma (puan), gecikmiş tekrarın gösterimi
- `veri_tara.js` → `veri_tara.out`, `syn_tara.js`, `ty_tara.js`, `ty_bak.js`, `ty_g32.js`: veri taraması (G/GS/GX/GX2/GW/PR/GL)
- İç fonksiyonlara erişmek için `konu/inst/index.html` kullanıldı: base kopyasının aynısı, tek fark `window.__I={...}` dışa aktarma satırı (8771 portunda sunuldu; yeniden çalıştırmak için: `cd konu/inst && nohup python3 -m http.server 8771 &`, sonra `NODE_PATH=$(npm root -g) node akis1.js`). Davranış base ile aynı.

Doğrulanmış yaşam döngüsü (g1, akis1.out):
| Gün | Olay | stg/rv/due | tstat | % | Konular satırı | Bugün "Konu" |
|---|---|---|---|---|---|---|
| 8 Eki | başlangıç | – | sırada | 0 | başlanmadı | Aşama 1 · Anla · 0/10 |
| 8 Eki | Anla 3/3 | anla | çalışılıyor | 10 | 1/4 aşama · sıradaki: Tanı | Tamam · bir aşama bitti 25/25 |
| 8 Eki | Tanı 5/8 (eşik altı) | anla | çalışılıyor | 10 | 1/4 · sıradaki: Tanı | (Anla'dan) Tamam |
| 8 Eki | Tanı 8/8, Kur 8/8 | anla,tani,kur | çalışılıyor | 55 | 3/4 aşama · yarın | Tamam |
| 9 Eki | Üret | +uret, due 10 Eki | çalışılıyor | 70 | 4/4 aşama · yarın | Tamam |
| 10 Eki | Tekrar 1 8/8 | rv=[10], due 13 | çalışılıyor | 85 | 4/4 aşama · 13 Eki | Tamam |
| 13 Eki | Tekrar 5/8 (başarısız) | due 14 | çalışılıyor | 85 | 4/4 aşama · yarın | Bugünlük aşama yok · 8/10 → 20/25 |
| 14 Eki | Tekrar 2 8/8 | rv=[10,14], due 21 | OTURDU | 100 | oturdu · tekrar 21 Eki | Tamam |
| 21 Eki | Tekrar 3 4/8 (başarısız) | due 22 | **OTURDU** | **100** | oturdu · tekrar 22 Eki | 20/25 |

Konular sekmesi, konu sayfası ve Bugün tek konu yürürken birbiriyle tutarlı. Sorunlar başarısız tekrarda, paralel konularda, gfocus'ta ve "yeniden yap" yollarında çıkıyor (aşağıda).

---
## [ÖNEM: yüksek] Başarısız tekrardan sonra konu yine "oturdu · %100 · Pekiştir ✓" görünüyor
- Kullanıcı ne görüyor: Perfekt 2 tekrarla oturdu. 7 gün sonraki tekrarda 4/8 aldı ("Bu sefer %80 olmadı"). Konu sayfasında hâlâ "A2.1 · OTURDU", "%100", yeşil, "Pekiştir ✓ · 2 tekrar yapıldı". Konular listesi "oturdu · tekrar 22 Eki", A2.1 bandı "1/13 oturdu". Konuyu unuttuğu hiçbir yerde görünmüyor. Kaç kez başarısız olursa olsun durum değişmiyor.
- Tekrar: `akis1.js`, 21 Eki adımı (`akis1.out` "G14 rv3 başarısız sonrası"): `tstat:"ok", pct:100, rv:[10 Eki,14 Eki], due:22 Eki`, konu sayfası "OTURDU %100 … Pekiştir · 2 tekrar yapıldı ✓".
- Kök neden: `tstat` (satır 5674) yalnız `stgAll && nRv>=2` sayıyor ve son sonucun başarısız olduğunu bilmiyor. `tprog` (5668–5673) en çok 2 tekrar sayıyor. `stagePath` (6105) `nr>=2 → ✓` gösteriyor. `lessonEnd` (6257) başarısız tekrarda yalnız `x.due=addD(t,1)` yazıyor; başarısızlığın izi kalmıyor. `S.gdone` de (6258) kalıyor.
- Düzeltme: başarısızlıkta işaret bırak, örneğin `else{x.due=addD(t,1);x.lapse=t;}`, başarılı tekrarda `delete x.lapse`. `tstat`: `if(x.lapse&&!x.known)return 'wip'`. Ayrıca `liSub`/`pTopic` için "son tekrar başarısız (21 Eki) · yarın yeniden" metni ekle; bant sayacı ve `pace` de buna uysun.

## [ÖNEM: yüksek] "Bugün bunu çalış" (gfocus) konusu bitince başlık hiç başlanmamış konuya geçiyor ve onu "Tamam" gösteriyor
- Kullanıcı ne görüyor: Perfekt'te "Bugün bunu çalış"a bastı, ertesi gün Üret'i yaptı. Bugün sekmesinin başlığı ve teması birden **"Modalverben im Präteritum"** oluyor. Görev satırı "Konu: Modalverben im Präteritum · Tamam · bir aşama bitti 25/25" diyor, oysa bu konu %0 ve "başlanmadı". Konular sekmesindeki "Bugünün konusu" kartı da Modalverben'i (%0, başlanmadı, "Aşama 1 · Anla") gösteriyor. Aynı ekranda Perfekt satırında hâlâ "bugün" etiketi var, Perfekt'in sayfasında da "✓ Bugünün konusu" yazıyor. Bu, kullanıcının bildirdiği şikâyetin aynısı ama başka bir tetikleyiciyle.
- Tekrar: `akis2.js` S2: 8 Eki'de g1 için Anla/Tanı/Kur yapılır, g1 sayfasında `gfocus` seçilir. 9 Eki'de g1 Üret yapılır. Çıktı: `Konular Bugünün konusu: … Modalverben im Präteritum %0 · başlanmadı …`, `g1 satırı: "Perfekt 4/4 aşama · yarın bugün %70"`, `Bugün: {"tema":"Modalverben im Präteritum","gram":"Konu: Modalverben im Präteritum Tamam · bir aşama bitti 25/25"}`.
- Kök neden: `todayTopic` (5710–5715). gfocus dalı, konunun yapılacak işi varken (`nextAct(S.gfocus).k`) onu döndürüyor ama `d.gt`'yi yazmıyor. Konu bugünlük bitince (`k` null) bu dal atlanıyor. O gün `d.gt` hiç yazılmadığı için `pickTopic()` yeni bir konu seçiyor. `taskDefs` ise puanı gün sayacından (`d.gs`) aldığı için yeni başlık "Tamam" görünüyor. `topicLi` (5904–5908) "bugün" etiketini `S.gfocus===id` ile ayrıca koyuyor.
- Düzeltme: gfocus dalında `d.gt=S.gfocus` yaz. Koşulu `nextAct(S.gfocus).k || (d.gt===S.gfocus && d.gtDone)` yap. "bugün" etiketini `todayTopic()[0]===id` ile göster. Genel olarak `taskDefs` "Konu" görevi, başlıktaki konuya bakmalı ya da başlığı o gün aşaması yapılan konuya çevirmeli (ORTAK'taki bilinen kök neden).

## [ÖNEM: yüksek] (Bilinen kök neden, ek tetikleyiciler doğrulandı) Başka konunun aşaması, günün konusunu "Tamam" gösteriyor
- Kullanıcı ne görüyor: 9 Eki'de günün konusu Perfekt (sıradaki iş Üret). Konular > "Yarım kalanlar"dan Modalverben'in Tanı aşamasını yapınca Bugün "Konu: Perfekt · Tamam · bir aşama bitti 25/25" diyor. Perfekt'in Üret'i ise hâlâ yapılmamış (`nextAct=uret`). 8 Eki'de Konular'daki "Yanında yeni bir konu" kartından başlanan konu için de aynısı oluyor. Gün içinde "Bugün bunu çalış" ile konu değiştirilirse yeni başlık da hemen "Tamam" görünüyor.
- Tekrar: `akis2.js` S1 (`S1 g2 Tanı sonrası Bugün: {"tema":"Perfekt","gram":"Konu: Perfekt Tamam · bir aşama bitti 25/25"}` ve `S1 g1 durum … next:{"k":"uret"}`).
- Kök neden: `taskDefs` (5793–5801), `frac` (3342 `gram:d.gs?1:…`). `d.gs` ve `d.g` gün sayacı, konuya bağlı değil. `lessonEnd` (6256) ve `usave` (6912) hangi konu olursa olsun `d.gs=1` yazıyor.
- Düzeltme: `d.gs` yerine `d.gsk={g1:1,g2:1}` gibi konu bazlı kayıt tut. Görev satırını "Konu: Perfekt · Üret bekliyor · (Modalverben Tanı bitti, puan alındı)" biçiminde yaz ya da başlığı o gün aşaması biten konuya çevir.

## [ÖNEM: yüksek] Yazarak (Kur/tekrar) sorulan bazı boşluklarda doğru cevap ancak tahminle bulunabiliyor; g32'nin bütün soruları böyle
- Kullanıcı ne görüyor: Kur aşamasında "BOŞLUĞA YAZ · Ich frage den ___." Türkçe karşılık yok, parantez ipucu yok. Beklenen cevap "Kollegen" ("İpucu": `K·······`). g41: "Er kommt heute nicht, denn ___." → beklenen "er hat Fieber" (`e· h·· F·····`). Kullanıcı "ich bin krank" yazarsa yanlış sayılıyor. g44: "Ich gebe ___." → "es ihm". Kur'un eşiği %70 (8 sorudan 6). 4 yazma sorusunun en az 2'si tahminle tutmazsa aşama geçilemiyor. Kullanıcı neyi yanlış yaptığını anlayamıyor.
- Tekrar: `ty_g32.js` (g32, g44 ve g41 için Kur ekranını ve ipucunu basar). `ty_tara.js` adayları listeler. Elle süzülmüş, içerik kelimesi tahmin gerektiren sorular:
  - g32 n-Deklination: GX[0–7] ve GX2[0–3], yani 12/12 (Kollegen, Studenten, Nachbarn, Kunden, Journalisten, Junge, Namen, Touristen, Herrn, Präsidenten, Dieb, Kollegen)
  - g41: GX[3] "ich bin krank", GX[7] "wir gehen trotzdem", GX2[3] "er hat Fieber"
  - g44: GX[0] "dem Kellner", GX[1] "meiner Schwester eine Uhr", GX[2] "es ihm", GX[3] "mir den Weg", GX2[2] "unserem Trainer"
  - g46 GX[7] "Mechaniker werden", g30 GX[6] "üben" (her fiil uyar)
  - Aynı verinin başka yerlerinde doğru örnek var: g44 GX[6] "Ich kaufe ___ ein Eis. (mein Sohn)" ve GX2[0] "(die Gäste)" parantezli. Kuralı bu sorular bozuyor.
- Kök neden: `tItems` (6160–6176) her GX/GX2 öğesini `ty` (yazma) olarak da kullanabiliyor. `tyBody` (6225) yalnız soru cümlesini gösteriyor, ne Türkçe karşılık ne kelime ipucu var. Veride bu öğelerin parantez ipucu eksik.
- Düzeltme: veride parantez ipucu ekle ("Ich frage den ___. (der Kollege)", "…, denn ___. (ich / krank sein)"). Ya da öğeye "yalnız şıklı" bayrağı koy (9. alan `mc`) ve `tItems`'ta `ty` için bu öğeleri atla. Bir başka yol: `tyBody`'de Türkçe çeviri göster.

## [ÖNEM: orta] Üret'i "Yeniden yap"mak vadesi gelen tekrarı yarına atıyor; oturmuş konuda bir aşamayı yeniden yapmak da günün Konu puanını veriyor
- Kullanıcı ne görüyor: Tekrar günü (10 Eki) konu sayfasında Üret'in yanındaki "Yeniden yap"a basıp cümle yazınca tekrar düğmesi kayboluyor. Ekranda "tekrar yarın açılır" yazıyor. Bu her gün yapılırsa tekrar hiç gelmez. 26 gün gecikmiş bir tekrar da aynı yolla yarına kayıyor. Ayrıca oturmuş Perfekt'te Kur'u yeniden yapınca Bugün'de "Konu: Modalverben im Präteritum · Tamam · bir aşama bitti 25/25" çıkıyor, oysa Modalverben'e hiç dokunulmadı.
- Tekrar: `akis2.js` S4: `G3 önce: due 2026-10-10 tdue true next {"k":"rv"}` → Üret yeniden → `due 2026-10-11 tdue false … tekrar yarın açılır`. 20 Eki'de: `due 2026-10-11 tdue true` → Üret yeniden → `due 2026-10-21`. Puan: `akis4.js` (`Kur yeniden sonrası: dgs 1 … "Konu: Modalverben im Präteritum Tamam · bir aşama bitti 25/25"`).
- Kök neden: `ACT.usave` (6908–6912) `if(!x.due||x.due<=t)x.due=addD(t,1)` her kayıtta çalışıyor ve ayrıca `d.gs=1` yazıyor. `lessonEnd` (6256) aşama daha önce geçilmiş olsa bile `day().gs=1` yazıyor.
- Düzeltme: `if(!x.stg.uret){x.stg.uret=t;if(!x.due)x.due=addD(t,1);}` yap; yeniden yapmada `due`'ya dokunma. `day().gs=1` yalnız aşama ilk kez geçildiğinde (`!x.stg[k]` iken) ya da tekrarda yazılsın.

## [ÖNEM: orta] Tekrar başarısız olunca Bugün, yarım kalmış konu dururken yepyeni bir konu öneriyor
- Kullanıcı ne görüyor: Perfekt tekrarı %80'in altında kaldı. Bugün'deki "Sıradaki adım" kartı başlıkta "Konu: Perfekt — Bu konunun bugünlük işi bitti … Puan için yeni bir konuya başla" yazıyor, düğmesi "Yeni konu: Nebensätze: weil, dass, wenn". Oysa Modalverben Tanı'da yarım duruyor (Konular'da "Yarım kalanlar" kartında). Konular aynı anda hem "Yanında yeni bir konu" hem "Yarım kalanlar" kartını gösteriyor. Sonuç: kullanıcı 3. ve 4. konuya başlamaya itiliyor, yarım konu bekliyor. Bu da "aynı anda 2–3 konu" kuralına aykırı.
- Tekrar: `akis2.js` S3: `S3 sıradaki adım düğmesi: <button … data-id="g3" data-s="anla">Yeni konu: Nebensätze: weil, dass, wenn</button>` ve `S3 Konular kartları: […"YANINDA YENİ BİR KONU · A2.1","YARIM KALANLAR · DEVAM EDEBİLİRSİN"] | g2: "1/4 aşama · sıradaki: Tanı"`.
- Kök neden: `nextHtml` (5815–5823) ve `taskDefs` `need` metni (5802) `newTopic()` (5679) kullanıyor. Bu fonksiyon yalnız "sırada" konulara bakıyor; işi açık yarım konuları ve `pickTopic`'teki `active<3` sınırını yok sayıyor. `vKonular` (5921–5922) "Yanında yeni bir konu" kartını yarım konu olsa da gösteriyor.
- Düzeltme: önce `G.filter(g=>g[0]!==tp[0]&&tstat(g[0])==='wip'&&nextAct(g[0]).k)[0]` önerilsin (düğme: "Devam: Modalverben · Tanı"). Yeni konu yalnız yarım konu yoksa ve aktif konu sayısı 3'ten azsa önerilsin. Kart metni de "Puan için yarım kalan konuna devam et" olsun.

## [ÖNEM: orta] "Bugün bunu çalış" aslında kalıcı; günler sonra da "✓ Bugünün konusu" yazıyor
- Kullanıcı ne görüyor: 8 Eki'de Perfekt için "Bugün bunu çalış"a bastı ("Bugünün konusu: Perfekt" bildirimi çıktı). 20 Eki'de Perfekt sayfasında hâlâ "✓ Bugünün konusu" yazıyor, listede "bugün" etiketi duruyor. Konunun yapılacak işi olduğu her gün diğer bütün konuların (vadesi gelen tekrarlar dahil) önüne geçiyor. Kullanıcı bunun kalıcı bir sabitleme olduğunu bilemiyor.
- Tekrar: `akis2.js` S2: `S2 12 gün sonra gfocus hâlâ: "g1"`, `g1 sayfası düğme: ['✓ Bugünün konusu']`.
- Kök neden: `ACT.gfocus` (6922) tarihsiz `S.gfocus` yazıyor. `todayTopic` (5711) bunu her gün okuyor. Gün değişince temizleyen bir kod yok.
- Düzeltme: `S.gfocus={id,d:today()}` sakla ve yalnız `d===today()` iken uygula. Kalıcı sabitleme isteniyorsa adı "Bu konuya odaklan (kapatana kadar)" olsun ve konu oturunca otomatik kalksın.

## [ÖNEM: orta] "Yanlışları tekrar" sonrası "Çok iyi." deniyor ama geçilemeyen aşama için yol gösterilmiyor
- Kullanıcı ne görüyor: Tanı'da 4/8 aldı (geçemedi), "Yanlış yaptığım 4 soruyu tekrar et"e bastı ve 4/4 yaptı. Bitiş ekranında "YANLIŞLARI TEKRAR BİTTİ · 4/4 · Çok iyi." yazıyor, vurgulu (lime) düğme "Bitti". "Aşamayı yeniden dene" düğmesi yok. Tanı'nın hâlâ geçilmediğini yalnız aşama listesindeki boş "2" dairesi gösteriyor. Kullanıcı aşamayı geçtiğini sanabilir. Başarısız tekrardan sonraki "yanlışları tekrar"da da aynı "Çok iyi." çıkıyor (`akis3.out`).
- Tekrar: `akis2.js` S5: `S5 retry sonu: 4/4 … YANLIŞLARI TEKRAR BİTTİ | 4 / 4 | Çok iyi. | … 2 | Tanı | 8 şıklı soru… | Konuya dön | Bitti`, `stg` değişmedi: `{"anla":…}`.
- Kök neden: `lessonEnd` 6265 (`k==='retry'` için yalnız "Çok iyi"/"Yanlışlarına bir göz at") ve 6272 (`a.k&&k!=='free'&&k!=='retry'` olduğundan devam düğmesi gizli; 6276'da "Bitti" lime).
- Düzeltme: `retry` ve `free` için `a.k` varsa "Tanı hâlâ geçilmedi (%75 gerekli) · şimdi aşamayı yeniden dene" mesajı ve `ACTB[a.k]` düğmesi göster; o durumda "Bitti" vurgulu olmasın.

## [ÖNEM: orta] Konu sayfası "ne zaman ne yaptım / ne zaman ne yapacağım" sorusuna cevap vermiyor (tasarım bulgusu)
- Kullanıcı ne görüyor: Konu sayfasında her aşama için yalnız **ilk** geçiş tarihi var ("tamam · 8 Eki"). Pekiştir'de "2 tekrar yapıldı" ve sıradaki tekrar tarihi yazıyor. Görünmeyenler: tekrarların hangi günler yapıldığı, kaç doğruyla geçildiği, başarısız denemeler (13 Eki'deki 5/8 ve 21 Eki'deki 4/8 hiçbir yerde yok), Tanı'nın ilk denemede kalındığı, yeniden yapılan aşamalar, serbest alıştırmalar. Gelecek de görünmüyor: yalnız bir sonraki tarih var. Oturduktan sonra 14/30/60 gün aralıklı tekrarların süreceği ve konunun ne zaman "tamamen bitmiş" sayılacağı yazmıyor. "Notum" sekmesinde yalnız Üret metinleri tarihleriyle duruyor.
- Tekrar: `akis1.out` son konu sayfası ("Pekiştir · 2 tekrar yapıldı · sıradaki tekrar: 22 Eki"). Kayıtta yalnız `rv:["2026-10-10","2026-10-14"]` var; başarısız tekrarlar ve puanlar saklanmıyor. `S.at['g:g1']` toplam doğru/yanlış sayısını tutuyor ama yalnız Rapor'da (8047–8049) kullanılıyor.
- Kök neden: veri yok. `lessonEnd` (6250–6260) sonuç kaydetmiyor (`X.ok/n` atılıyor), `x.stg[k]` yalnız ilk tarih, `x.rv` yalnız başarılı tarihler. `pTopic` (6117–6150) ve `stagePath` (6096–6108) geçmiş bölümü çizmiyor.
- Düzeltme: `lessonEnd` ve `usave` içinde `x.h.push({d:t,k:k,ok:X.ok,n:n,p:X.pass?1:0})` (son ~30 kayıt) tut. Konu sayfasına "Geçmiş" (tarih · aşama · 6/8 · geçti/kaldı) ve "Plan" (sıradaki tekrar 21 Eki, sonra ~4 Kas, ~4 Ara…) bölümleri ekle. Aşama satırında "2. denemede · 8 Eki" gibi kısa özet göster.

## [ÖNEM: orta] "Zaten biliyorum" işaretleri "haftada biten konu" temposunu ve bitiş tahminlerini şişiriyor; geri alınca gerçek oturma tarihi siliniyor
- Kullanıcı ne görüyor: İlk gün 8 konuyu "Zaten biliyorum" diye işaretledi. İlerleme > "Ne zaman?" kartında "2 · haftada biten konu (son 4 hafta)", "A2 konuları bu hızla biter: 10 Ara", "B1 sonu: 18 Şub" çıkıyor; hiçbir konu çalışılmadığı halde. Ayrıca tekrarla gerçekten oturmuş Perfekt'te "Zaten biliyorum"u açıp kapatınca konu "oturdu" kalıyor ama oturma tarihi (gdone) siliniyor. Haftalık "oturan konu" sayısından ve tempodan düşüyor.
- Tekrar: `akis2.js` S7 (`NE ZAMAN? | 10 Ara | … | 2 | haftada biten konu`) ve S7b (`tstat ok gdone undefined`).
- Kök neden: `ACT.gknown` (6923) işaretlemede `S.gdone[id]=today()` yazıyor, kaldırmada koşulsuz `delete S.gdone[id]` yapıyor. `pace` (5751–5754) ve `weekStats` (6012) `S.gdone`'u sayıyor.
- Düzeltme: "biliyorum" için `S.gdone` yazma (ya da `pace`'te `gx[id].known` olanları atla). Kaldırırken `x.known=false` yaptıktan sonra `if(tstat(id)!=='ok')delete S.gdone[id]`.

## [ÖNEM: düşük] Anla aşaması 0/3 ile de "tamam" sayılıyor ve günün Konu puanını (25) veriyor
- Kullanıcı ne görüyor: 3 kontrol sorusunun üçü de yanlış: "AŞAMA 1 · ANLA BİTTİ · 0 / 3 · Kuralı gördün. Şimdi tanıma alıştırması". Anla ✓, %10, Bugün "Konu … Tamam · bir aşama bitti 25/25".
- Tekrar: `akis2.js` S6 (`S6 Anla 0/3 sonu: 0/3 … ANLA BİTTİ`).
- Kök neden: `lessonEnd` 6253 `X.pass=k==='anla'||acc>=…`.
- Düzeltme: Anla için en az 2/3 iste ya da 0–1/3'te "Özeti bir kez daha oku" uyarısı göster; puanı yine verecekse bile mesajı sonuca göre değiştir.

## [ÖNEM: düşük] Gecikmiş tekrar listede geçmiş bir tarihle "oturdu · tekrar 20 Eki" yazıyor
- Kullanıcı ne görüyor: 15 Kasım'da Perfekt satırında "oturdu · tekrar 20 Eki" ve %100 yazıyor. Tekrarın 26 gün geciktiği yazmıyor; yalnız küçük bir "tekrar" etiketi var.
- Tekrar: `akis4.js` (`15 Kas (gecikmiş): liSub oturdu · tekrar 20 Eki`).
- Kök neden: `liSub` (6113) `x.due` tarihini geçmiş mi diye bakmadan yazıyor.
- Düzeltme: `tdue(id)` iken "oturdu · tekrar bekliyor (N gün gecikti)".

## [ÖNEM: düşük] Tekrar takvimi metinleri gerçek aralıkla uyuşmuyor; "Uygulama o gün hatırlatacak" sözü karşılıksız
- Kullanıcı ne görüyor: Pekiştir açıklaması "1, 3 ve 7 gün sonra. 2 başarılı tekrar = konu oturdu". Konu notu da "sonra 1, 3 ve 7 gün arayla tekrar" diyor. Gerçekte Üret'ten 1 gün sonra 1. tekrar, 3 gün sonra 2. tekrar geliyor ve konu bu noktada oturuyor (7 günlük tekrar oturduktan sonra). Ardından 14, 30, 60, 60… gün arayla tekrar sonsuza kadar sürüyor; bu hiçbir yerde açıklanmıyor ("arada bir yine sorulacak" dışında). Bitiş ekranlarındaki "Uygulama o gün hatırlatacak" bildirimi için kodda bildirim yok (`Notification` kullanılmıyor); konu ancak uygulama açılınca Bugün'de çıkıyor.
- Tekrar: `akis1.out` (13 Eki: 2. tekrar, oturdu; due 21 Eki = +7), `RVI=[3,7,14,30,60]` (5659), `usave` due +1.
- Kök neden: `STDESC.rv` (6091), `pTopic` notu (6130), `lessonEnd` 6273 metni.
- Düzeltme: "Üret'ten 1 gün sonra ve ondan 3 gün sonra tekrar; ikisi de %80 ise oturdu. Sonra 7, 14, 30, 60 günde bir kısa kontrol." "Hatırlatacak" yerine "o gün Bugün sayfasında çıkacak".

## [ÖNEM: düşük] Aynı bilgi üç ayrı biçimde ve "ne yarın?" belirsizliği
- Kullanıcı ne görüyor: Konular satırında "3/4 aşama · yarın" ve "4/4 aşama · yarın" yazıyor; yarın neyin olacağı yazmıyor. Aynı konu için başlık kartı "Üret aşaması yarın açılır", aşama listesi "yarın açılır" diyor. Tekrarda üç farklı biçim var: liste "4/4 aşama · 13 Eki", başlık "tekrar 2 gün sonra açılır", aşama listesi "sıradaki tekrar: 13 Eki". Konular kartında cümle küçük harfle başlıyor: "Bugünlük tamam. tekrar yarın açılır."
- Tekrar: `akis1.out` (8 Eki kur sonrası, 11 Eki).
- Kök neden: `liSub` (6110–6115, `a.wait` dalında aşama adı yok), `nextReview` (5716–5721), `stagePath` (6106), `vKonular` 5918.
- Düzeltme: tek bir biçimlendirici kullan, örneğin `whenTxt(id)` → "Üret · yarın (9 Eki)" / "Tekrar · 3 gün sonra (13 Eki)". Her yerde onu çağır ve cümle başını büyük harf yap.

## [ÖNEM: düşük] "40 konu" metinleri eskimiş (konu sayısı 46)
- Kullanıcı ne görüyor: Konular > "Konular arası bağlantılar" açılınca "40 konu aslında 9 temel mantığın çeşitlemesi". Seviye testi girişinde "Gramer · 40 konu, her birinden 1 soru" yazıyor; test aslında 46 gramer sorusu soruyor (`G.map`).
- Tekrar: `veri_tara.out` (`hubsCard: … 40 konu aslında…`, `Konu sayısı 46`).
- Kök neden: `hubsCard` (8206), test girişi (6752; sorular 6746'da `G.map`).
- Düzeltme: sabit yerine `G.length` yaz.

## [ÖNEM: düşük] Vadesi gelen ikinci konu Bugün'de sayfanın en altında kalıyor; "Konu" görevi ise "Tamam" görünüyor
- Kullanıcı ne görüyor: 10 Eki'de Perfekt ve Modalverben'in tekrarı aynı gün geliyor. Bugün'ün başlığı ve "Konu" görevi Perfekt. Modalverben yalnız sayfanın en altındaki "Tekrar zamanı gelen konular" kartında (hata haritasının da altında). Perfekt'in tekrarı bitince "Konu: Perfekt · Tamam 25/25" ve "Sıradaki adım" kelimeye geçiyor. İkinci tekrar hiçbir görevde ya da sayaçta geçmiyor.
- Tekrar: `akis3c.js` (`… Puan nasıl hesaplanır? | … | TEKRAR ZAMANI GELEN KONULAR | Modalverben im Präteritum | 4/4 aşama · sıradaki: tekrar | tekrar | %70`, sayfanın en sonu).
- Kök neden: `vBugun` (5851–5852) kartı en sona ekliyor. `taskDefs` "Konu" görevi tek konuya bakıyor.
- Düzeltme: "Konu" görevinin altına "+1 tekrar daha bekliyor: Modalverben" satırı ekle ya da kartı "Sıradaki adım"ın hemen altına taşı.

---
## Veri taraması özeti (g41–g46 dahil 46 konu) · `veri_tara.js`, `syn_tara.js`, `sz_tara.js`, `ty_tara.js`
- 46 konunun hepsinde G (özet ve 6 örnek cümle), GS, GX (8) + GX2 (4) = 12 boşluk sorusu, GW, PR ve GL (hub, kopru, hatirla, mantik, adim, tr, neden, karis, kanca, ileri) var. Boş alan yok.
- Bütün GX/GX2 öğelerinde tek `___` var. Doğru cevap ve iki yanlış şık dolu ve birbirinden farklı; `norm` sonrası da çakışmıyor. Açıklama ve yanlış şık notları dolu. `mcItem` ile üretilen mc/hc öğelerinde doğru cevap şıklarda var. "Hangisi doğru?" iki farklı cümle üretiyor. Tek sayıda `*` yok. Konu içinde aynı soru iki kez yok.
- Bütün örnek cümlelerdeki alternatif sıra kodları (`szDecode`) çözülüyor, `prepSatz` hatasız. Tekrar eden kelimeler (ich … ich) küçük harf anahtarla doğru karşılaştırılıyor.
- GL bağlantıları (`kopru.to`, `ileri.to`, `hub`) hepsi çözülüyor. Her konu en az bir bağlantı ailesinde (HUB).
- Eşanlamlı şık çakışması (deshalb/deswegen/darum, trotzdem/dennoch vb.) bulunmadı.
- Küçük notlar (bulgu değil): GW kelime sayısı g28'de 3, g22, g26 ve g37'de 4. Bazı GL.adim adımları bir öncekinin devamı değil (g12, g32, g34, g38, g40, g42–g46); bu adımlarda bütün satır "yeni" diye vurgulanıyor, hata değil. GL'siz Anla yolundaki "Sonra 4 kısa soru" metni (6195) ölü kod, çünkü her konunun GL'si var.
- Tek gerçek veri sorunu yukarıdaki "yazarak sorulan, tahmin gerektiren boşluklar" bulgusu.

## Doğrulanan ve sorunsuz olanlar
- Tek konu yürürken Konular satırı, "Bugünün konusu" kartı, konu sayfası, aşama listesi ve Bugün "Konu" görevi her adımda aynı aşamayı ve aynı yüzdeyi gösteriyor (10 → 30 → 55 → 70 → 85 → 100). Ayrıntı için baştaki tablo.
- Eşik altı Tanı/Kur'da aşama işaretlenmiyor. "Geçmek için %75 lazım…" mesajı, "Aşamayı yeniden dene" ve "Yanlış yaptığım N soruyu tekrar et" düğmeleri anlaşılır. Başarısız tekrarda `due=yarın` oluyor ve `rv` değişmiyor.
- Aynı gün ikinci tekrar ve vadesinden önce tekrar arayüzden mümkün değil. Tekrar geçildikten sonra Konular, Bugün ve konu sayfasında `data-s="rv"` düğmesi kalmıyor; yalnız "Alıştırma / Yine de alıştırma yap · aşamaya sayılmaz" var (`akis3.out`).
- Serbest alıştırma ve "Yanlışları tekrar" `stg`, `rv`, `due` ve `gdone`'a dokunmuyor. Yalnız `x.m` (soru bilinirliği), `x.last`, `d.g` (günlük Konu soru sayacı) ve `S.al/S.at/S.wl` kayıtları artıyor (`akis3.out`: free sonrası `rv`/`due` aynı, `dg` 8 → 16).
- Kur geçilince 3 "gs:" cümle kartı +2 gün vadeyle kelime tekrarına ekleniyor ("Konu cümlesi · Perfekt" etiketiyle).
- Sayfa hatası (pageerror) hiçbir akışta yok.
