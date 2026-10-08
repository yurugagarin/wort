# Denetim · KONULAR (gramer konuları): yaşam döngüsü ve durum gösterimi

Test ortamı: Playwright, saat sabitlenip gün atlatıldı. Betikler `scratchpad/v22/konu/` altında:
- `lib.js`: ortak yardımcılar (gün atlatma, aşamayı doğru/yanlış cevaplarla bitirme, Konular/Bugün/konu sayfası okuma)
- `akis1.js` → `akis1.out`: g1 (Perfekt) baştan sona: Anla → Tanı (önce başarısız, sonra geçer) → Kur → ertesi gün Üret → 1., 2. (önce başarısız) ve 3. tekrar (başarısız)
- `akis2.js` → `akis2.out`: paralel konular, gfocus, başarısız tekrardan sonraki öneri, Üret'i yeniden yapma, yanlışları tekrar, Anla eşiği, "Zaten biliyorum"
- `akis3.js` → `akis3.out`: serbest alıştırma, tekrar sonrası "yanlışları tekrar", aynı gün ikinci tekrar, aynı gün vadesi gelen iki konu
- `veri_tara.js` → `veri_tara.out`, `syn_tara.js`, `ty_tara.js`, `ty_bak.js`, `ty_g32.js`: veri taraması (G/GS/GX/GX2/GW/PR/GL)
- İç fonksiyonlara erişmek için `konu/inst/index.html` kullanıldı: base kopyasının aynısı, tek fark `window.__I={...}` dışa aktarma satırı (8771 portunda sunuldu). Davranış base ile aynı.

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
