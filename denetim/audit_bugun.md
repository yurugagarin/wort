# Denetim · BUGÜN sekmesi ve GÜNLÜK PUAN

Donmuş kopya: scratchpad/v22/base/index.html (satır numaraları bu dosyaya göre).
Betikler: scratchpad/v22/bugun/ (lib.js ortak yardımcılar; t*.js senaryolar). Çalıştırma: `cd bugun && NODE_PATH=$(npm root -g) node tN.js`

Puanın kaynağı (kod: frac() 3338, MAX 3337):
| Görev | Puanı veren alan | Bu alanı artıran eylemler (hepsi, hangi konu/tablo olursa olsun) |
|---|---|---|
| Kelime 30 | d.w / d.wt | grade() 3286 (her cevap, YANLIŞ dahil, aynı kart tekrar gelince yine), introDone() 3275 (yeni kelime tanıtımı), "Zor kelimeler" turu (hardgo), "5 yeni kelime daha" |
| Konu 25 | d.gs=1 ya da d.g/10 | lessonEnd() 6256: HERHANGİ bir konunun anla/tani/kur/rv aşamasını geçmek → gs=1; usave 6912 (herhangi konunun Üret'i) → gs=1,g+=3; lessonRecord() 6188: her ders sorusu (Serbest alıştırma, Yanlışları tekrar, başka konular dahil) → g+1 |
| Ezber 25 | d.ezt ya da d.ez/12 | ezEnd() 7312: HERHANGİ tablo(lar)la ≥6 soruluk test → ezt+1; ezFillCheck() 7433: herhangi tablonun boş-tablo doldurması (≥6 hücre) → ezt+1; ezRecord() 7289 her ezber cevabı → ez+1 |
| Yazma 20 | sentN(d.sch) | Bugün'deki textarea (6990), Üret aşamasını kaydetmek (usave 6912, herhangi konu), kelime kartındaki "kendi cümleni yaz" (owsave 6860). Konu/dil kontrolü yok. |

ÖZET: 16 bulgu — 1 kritik, 7 yüksek (1 tasarım), 5 orta, 3 düşük (+ sorunsuz olanların kaydı en altta).

Başlıklar ise: Konu → todayTopic() (5710), Ezber → ezToday() (7237, d.ezd), Yazma → todayTopic(). Yani dört görevden üçünde başlıkta yazan şey ile puanı kazandıran şey bağımsız.

## [ÖNEM: kritik] Yeni kurulumda ikinci açılışta geçmiş günün puanı eski formülle "donduruluyor" (takvimde 100 → 55); "Zaten biliyorum" işaretleri ve seviye testi tahmini siliniyor
- Kullanıcı ne yaşıyor: Sıfırdan başlayan kullanıcı (Ayarlar > "Tüm verileri sil" de aynı yoldan geçer: `ACT.reset` → `S=blank()`; bu yol betikle denenmedi, kodla aynı) ilk gün 100/100 yapıyor; ertesi gün uygulamayı açınca İlerleme > Puan takviminde dünkü gün **55** görünüyor. Dün "Zaten biliyorum" dediği konu (ör. Verben mit Dativ) Konular'da yeniden "başlanmadı"; seviye testinden gelen kelime tahmini (S.vest) sıfırlanıyor.
- Tekrar üretme: `bugun/t9.js`. Gözlenen: G1 sonunda `d8` = {w:10,wt:10,gs:1,ezt:1,sch:3 cümle} ve halka 100. 2026-10-09 açılışında `S.days['2026-10-08'].sc0=55, mn0=0`; takvim "55"; `S.gx.g5` (known:true) silinmiş, `S.gdone={}`, `S.vest=null`. (Ayrıca `t8.js`: aynı akışta G1=100 → ertesi gün takvim 65.)
- Kök neden: `migrate()` (3125-3160) boş kayıtta `if(!s||typeof s!=='object')return blank();` ile erken dönüyor; `blank()` (3122) `scv/gs1/rk1/rk2` bayraklarını içermiyor. İkinci yüklemede bu bayraklar yok sayılıp tüm eski-sürüm göçleri çalışıyor: v8 dondurma (3143-3149) dünkü günü Konu 15 + "Hören 20" (d.h) + Yazma 20 + Kelime 30 eski formülüyle `sc0` olarak yazıyor ve `total()` (3348) artık hep sc0'ı döndürüyor; rk2/rk1 (3152-3159) `known`'ları ve `last`'ı olmayan gx kayıtlarını siliyor, `vest=null`.
- Düzeltme: `blank()` dönüşüne `scv:8,gs1:1,rk1:1,rk2:1` ekle (ya da migrate'in erken dönüşünü `s=blank()` yapıp bayrakları set ederek devam ettir). Zaten etkilenmiş kayıtlar için: `sc0` değeri yeni formülle (`parts`) hesaplanan değerden düşük olan ve `d.ezt`/`d.ez` alanı olan (eski sürümde olmayan alan) günlerde `sc0`/`mn0`'ı sil.

## [ÖNEM: yüksek] Konu görevi: başlıktaki konu ile puanı kazandıran konu bağımsız — başka konunun tekrarı / aşaması günün konusunu "Tamam" gösteriyor (kullanıcının örneği ve 4 benzeri)
- Kullanıcı ne görüyor: "Konu: Modalverben im Präteritum · Tamam · bir aşama bitti · 25/25". Oysa Modalverben'e hiç dokunulmadı; Konular sekmesi aynı anda "Bugünün konusu Modalverben · sıradaki: tekrar" diyor. Puanı Perfekt'in tekrarı kazandırdı ama Bugün'de Perfekt'in adı hiçbir yerde geçmiyor ("Tekrar zamanı gelen konular" kartından da Perfekt kayboluyor). Doğrulanan 4 yol:
  1. **Başka konunun Pekiştir tekrarı** (t2.js): g2 ve g1 vadesi gelmiş; günün konusu g2. "Tekrar zamanı gelen konular" kartındaki Perfekt'e dokun → Pekiştir 8/8 → Bugün: `Konu: Modalverben im Präteritum | Tamam · bir aşama bitti | 25/25`, `d.gs=1, d.gt='g2', gtDone` yok.
  2. **Serbest alıştırma / Yanlışları tekrar** (t3.js): oturmuş Perfekt'te "Karışık alıştırma" (4/8 doğru) → `Konu: Modalverben… | Aşama 1 · Anla · 8 / 10 soru | Eksik: Aşamayı bitir ya da 2 soru daha | 20/25`; ikinci alıştırma + "Yanlış yaptığım 4 soruyu tekrar et" → `Tamam · 20 soru | 25/25`. Modalverben hâlâ "başlanmadı". Yanlış cevaplar da soru sayılıyor.
  3. **"Sıradaki adım"ın kendi önerdiği yeni konu** (t7.js): Perfekt tekrarı 3/8 ile başarısız → kart "Yeni konu: Modalverben" öneriyor → Modalverben Anla geçilince Bugün: `Konu: Perfekt | Tamam · bir aşama bitti | 25/25`. Kullanıcı Perfekt tekrarını geçtiğini sanıyor; Konular'da Perfekt "tekrar yarın".
  4. **"Bugün bunu çalış" ile seçilen konu bitince başlık geri dönüyor** (t6.js): aşağıdaki ayrı bulguya bakın.
  5. Konular sekmesindeki "Yanında yeni bir konu" kartı (5923) "İki konu birlikte yürür, **ikisi de puana sayılır**" diyor; oysa Konu görevi tek bir `gs=1` ile 25'te tavan yapıyor, ikinci konu puana hiçbir şey eklemiyor ve Bugün'de adı geçmiyor (t2.js KONULAR çıktısında kart görünüyor).
- Kök neden: `frac()` 3338-3346 `gram: d.gs?1:min(1,d.g/10)` gün sayaçları; `lessonEnd()` 6256 `day().gs=1` konu kontrolü olmadan; `lessonRecord()` 6188 her soruda `d.g++` (free/retry/başka konu dahil); `usave` 6912. Başlık ise `taskDefs()` 5797 `'Konu: '+tp[2]` (todayTopic). `s` metni (5798) "Tamam · bir aşama bitti" hangi aşamanın/konunun bittiğini söylemiyor.
- Düzeltme: günlük kayıtta konu bazında iz tut: `lessonEnd` içinde `d.gl=(d.gl||[]); d.gl.push({id:id,k:k,pass:X.pass,n:n,ok:X.ok})`, `usave`'de de `{id,k:'uret'}`. `taskDefs` gram görevinde: başlık `Konu: <todayTopic>` kalsın ama `s` = bugün yapılanların listesi ("Perfekt · Pekiştir geçti 8/8"; "Modalverben · henüz yok"). Puanı ya (a) yalnız günün konusuna bağla (`d.gs` yerine `d.gsId===tp[0]`) ya da (b) başlığı puanı kazandıran konuya çevir ("Konu · Perfekt tekrarı ✓"); hangisi seçilirse seçilsin başlık ile puan aynı konuyu göstermeli. Serbest alıştırma/yanlışları tekrar soruları için ya sayma ya da `s`'de "8 soru (Perfekt, serbest alıştırma)" yaz.

## [ÖNEM: yüksek] "Bugün bunu çalış" ile seçilen konunun işi bitince Bugün başlığı gün ortasında hiç başlanmamış konuya dönüyor ve onu "Tamam" gösteriyor
- Kullanıcı ne görüyor: Sabah Bugün "Konu: Perfekt" diyor. Konular'da "Nebensätze"yi açıp "Bugün bunu çalış"a basıyor → başlık "Konu: Nebensätze…" ve Yazma başlığı da "Nebensätze" oluyor. Anla, Tanı, Kur'u geçiyor. Kur biter bitmez Bugün başlığı kendiliğinden **"Konu: Perfekt · Tamam · bir aşama bitti · 25/25"** ve "Yazma · 3 cümle · Perfekt" oluyor. Perfekt'e hiç dokunmadı (Konular: "Perfekt · başlanmadı"); Konular'ın "Bugünün konusu" kartı da Perfekt'e döndü. Gün içinde başlık iki kez değişti.
- Tekrar üretme: `bugun/t6.js`. Gözlenen satırlar: `1 g3 "Bugün bunu çalış": Konu: Nebensätze…`, `2 g3 kur geçti: Konu: Perfekt | Tamam · bir aşama bitti | 25/25 … gt=g1 gtDone=undefined gfocus=g3`.
- Kök neden: `todayTopic()` 5711: `if(S.gfocus&&GBY[S.gfocus]&&nextAct(S.gfocus).k)` — odak konusunun bugünlük işi bitince (Üret yarın açılır → `nextAct().k=null`) koşul düşüyor ve sabahki `d.gt` (g1) dönüyor. `lessonEnd()` 6259 `gtDone` yalnız `d.gt===id` iken yazılıyor; odak konusu için hiçbir iz yok.
- Düzeltme: `todayTopic()` içinde odak konusu seçildiğinde onu günün konusu olarak sabitle: `if(S.gfocus&&GBY[S.gfocus]){var d=day(); if(d.gt!==S.gfocus&&nextAct(S.gfocus).k){d.gt=S.gfocus;d.gtDone=0;save();}}` ve ardından normal `d.gt` yolunu kullan (gtDone sayesinde iş bitince de aynı başlık kalır). Ayrıca `gfocus` kalıcı bir ayar (ertesi gün de geçerli, t6 "3 ertesi gün" satırı) ama düğme "Bugün bunu çalış" diyor; ya etiketi "Bu konuya odaklan" yap ya da gfocus'u güne bağla.

## [ÖNEM: yüksek] Ezber görevi: başlıktaki tablo dışındaki herhangi bir tablo testi (başarısız olsa bile) "Ezber: <günün tablosu> · Tamam" yapıyor
- Kullanıcı ne görüyor: "Ezber: sein ve haben · Tamam · 1 tablo çalışması · 25/25". Oysa Ezber sekmesinden "Şimdiki zaman ekleri"ni test etti, 5/12 aldı (uygulama "%80 olmadı: yarın yeniden sorulacak" dedi). Ezber sekmesinin en üstünde hâlâ "BUGÜNÜN EZBERİ · sein ve haben · %0".
- Tekrar üretme: `bugun/t4.js` → `--- başka tablo testi (5/12 doğru) sonrası`: `ez: "Ezber: sein ve haben" | Tamam · 1 tablo çalışması | 25/25`, `d.ezt=1, d.ezd=seinhaben`.
- Kök neden: `frac()` 3343 `ez: d.ezt?1:…`; `ezEnd()` 7312 `d.ezt++` tablo kimliğine ve başarıya bakmıyor (`ezFillCheck()` 7433 aynı). Başlık `taskDefs()` 5803 `'Ezber: '+et.t` (`ezToday()`, `d.ezd`).
- Düzeltme: `ezEnd`/`ezFillCheck`'te çalışılan tablo kimliklerini güne yaz (`d.ezl=(d.ezl||[]).concat(Object.keys(X.per))` ve başarı oranı). `taskDefs` ez görevinde `s` = "Şimdiki zaman ekleri · test 5/12 (geçmedi)" gibi gerçekte yapılanı göstersin; başlıktaki tablo yapılmadıysa "Günün tablosu sein ve haben henüz çalışılmadı" ekle. İstenirse puanı `d.ezl` içinde `d.ezd` varsa tam ver.

## [ÖNEM: yüksek] Kelime görevi "kart" sayıyor ama aslında cevap sayıyor: yanlış cevaplarla "Tamam · 10 kart", seri korunuyor, kuyrukta 10 kart duruyor
- Kullanıcı ne görüyor: 10 kartlık günde her kartı yanlış cevaplıyor (kart kuyruğa geri dönüyor). 10 cevaptan sonra Bugün: "Kelime tekrarı · Tamam · 10 kart · 30/30", "Minimum gün tamam, seri güvende", "1 gün seri". Aynı anda Kelimeler sekmesi "10 kart seni bekliyor". 6 cevapta "6 / 10 kart · Eksik: 4 kart kaldı (~1 dk)" yazıyordu; gerçekte 10 kartın hiçbiri bitmemişti.
- Tekrar üretme: `bugun/t5.js` (newPerDay=0, 10 vadesi gelmiş kart; doReview(…, false)). Gözlenen: `w=10 wt=10`, `KELIMELER: … 10 kart seni bekliyor`, kuyruk uzunluğu 10.
- Kök neden: `grade()` 3286 `d.w=(d.w||0)+1` her cevapta (g=0 dahil, `s.d=t` ile kart bugün yeniden geliyor; `rvAdvance` 6665 requeue). `taskDefs()` 5795 bunu "kart" diye gösteriyor; `wordDone()` 3349 seriyi buna göre veriyor. Aynı sayaç "Zor kelimeler" turunda (hardgo) ve "5 yeni kelime daha"da (introDone 3275) da artıyor, yani vadesi gelen kartlar hiç açılmadan da 30 puan + seri alınabiliyor. Doğrulandı: `bugun/t10.js` — 10 vadesi gelmiş kart + 10 "zor kelime" (vadesi 20 Eki). Kelimeler > "Zor kelimeleri şimdi çalış · 10" bitirilince Bugün `Kelime tekrarı | Tamam · 10 kart | 30/30`, "1 gün seri"; vadesi gelmiş 10 kartın hiçbiri tekrar edilmedi. Aynı turun sonunda konsolda `TypeError: Cannot read properties of null (reading 'length')` atılıyor: `rvAdvance()` 6665-6668 `drawPage()` çağırınca `pReview()` 6581 `W.q=null` yapıyor, ardından 6668 `!W.q.length` patlıyor ("Kelime görevi tamam" bildirimi de bu yüzden hiç çıkmıyor).
- Düzeltme: günün kart kümesini sabitle (`ensureTarget`'ta `d.wq=[...id]`), puanı "bu kümeden bugün en az bir kez doğru cevaplanan/tanıtılan kart sayısı / d.wt" yap (`d.wd={id:1}`); en azından etiketi "10 / 10 cevap" yap ve kuyruk boşalmadan "Tamam" deme (`rem` = `W.q.length`).

## [ÖNEM: yüksek] Gece yarısı uygulama açıkken: Bugün ekranı eski günde donuyor; Yazma kutusuna dokunmak dünkü cümleleri yeni güne kopyalayıp 20 puan veriyor
- Kullanıcı ne görüyor: 23:58'de Yazma'ya 3 cümle yazdı (50 puan). 00:02'de ekran hâlâ "Donnerstag, 8. Oktober · 50" (sekme değiştirip dönmek de değiştirmiyor). Kutunun sonuna " Gut." ekleyince halka **20**'ye düşüyor ama tarih hâlâ "8. Oktober" yazıyor. Yeniden çizilince 9 Ekim'de "Yazma · Tamam · 3 cümle · 20/20" — yazılan cümleler dünkü cümleler.
- Tekrar üretme: `bugun/t11.js` (M1). Gözlenen: `'2026-10-09': {"sch":"Ich habe gestern gearbeitet. … Pizza gegessen. Gut."}`; ekranda tarih 8 Ekim, halka 20.
- Kök neden: (1) Gün değişimini yakalayan tek yer `visibilitychange` 7015 ve o da yalnız `W.day` doluysa (kelime tekrarı açılmışsa) çalışıyor; zamanlayıcı yok. (2) `input` işleyicisi 6990 `var d=day();d.sch=el.value` — textarea dünün `d.sch`'ıyla doluydu, `day()` artık yeni günü döndürüyor. (3) `refreshScore()` 5883 yeni günün puanını eski günün başlığına yazıyor.
- Düzeltme: `var RDAY=today()` tut; `render()`'da güncelle; `setInterval(function(){if(today()!==RDAY){W.q=null;if(!X)render();}},30000)` + `visibilitychange`'te `W.day` şartını kaldır. `input` (sch) işleyicisinde `if(today()!==RDAY){render();return;}` (eski metni yeni güne yazma).

## [ÖNEM: yüksek] Gece yarısını geçen ders: aşama yeni güne yazılıyor, yeni günün başlığı hiç dokunulmamış konuyu "Tamam" gösteriyor ve Üret bir gün kayıyor
- Kullanıcı ne görüyor: 23:5x'te Perfekt Anla+Tanı (8 Ekim: 55), Kur'a başladı, 00:03'te bitirdi. Bugün (9 Ekim): **"Konu: Modalverben im Präteritum · Tamam · bir aşama bitti · 25/25"**, Ezber başlığı da Modalverben'in tablosuna dönmüş. Modalverben'e dokunmadı. Perfekt'in Kur tarihi 9 Ekim olduğu için Üret "yarın" (10 Ekim) açılıyor; 9 Ekim'de Perfekt için yapılacak bir şey kalmıyor. Takvimde 9 Ekim gece 00:03'te 55.
- Tekrar üretme: `bugun/t11.js` (M2). Gözlenen: `'2026-10-09': {"g":4,"gs":1,"wt":0,"gt":"g2"}`, `g1.stg.kur="2026-10-09"`.
- Kök neden: `lessonEnd()` 6250-6260 her şeyi `today()`/`day()` ile ders BİTİŞ anına yazıyor; yeni günde `d.gt` henüz yok → `gtDone` yazılmıyor; ardından `todayTopic()` 5714 `pickTopic()` ile beklemedeki Perfekt'i atlayıp yeni konu seçiyor.
- Düzeltme: ders açılırken `o.day=today()` sakla; `lessonEnd`/`lessonRecord`/`ezEnd`/`ezRecord`'da `S.days[X.day]` kullan (dersin başladığı güne yaz) ve aşama tarihini `X.day` yap. Ayrıca `todayTopic()`'te yeni gün için `d.gt` seçerken "dün bugünkü konu olan ve dün aşama yapılan konu"yu (önceki günün `gt`'si, `nextAct` beklemede bile olsa) korumak başlık sürprizini önler.

## [ÖNEM: orta] Konu görevi Anla'nın 3 sorusuyla "Tamam" oluyor; Konular'ın "ilk gün Anla, Tanı, Kur" planıyla çelişiyor
- Kullanıcı ne görüyor: Perfekt'te Anla'yı (3 kontrol sorusu) bitirince Bugün "Konu: Perfekt · Tamam · bir aşama bitti · 25/25", "Eksik" satırı yok, "Sıradaki adım" Ezber'e geçiyor; Tanı'yı Bugün hiçbir yerde önermiyor. Konu sayfası ise "Bir konu yaklaşık 1 hafta sürer: ilk gün Anla, Tanı, Kur; ertesi gün Üret" diyor. Bugün'ü takip eden kullanıcı her gün tek aşama yapıp konuyu 1 hafta yerine ~2 haftaya yayıyor; Üret de buna göre kayıyor.
- Tekrar üretme: `bugun/t1.js` (`--- anla sonrası`: `gram: "Konu: Perfekt" | Tamam · bir aşama bitti | 25/25`, `d.g=3`). Ayrıca Anla giriş sayfası (lessonIntro 6195, GL olmayan konularda) "Sonra 4 kısa soru" derken düğme "Anladım · 3 kontrol sorusu" diyor; tItems 6164 3 soru veriyor.
- Kök neden: `lessonEnd()` 6256 `anla` geçişi de `gs=1`; `taskDefs()` 5799 `f.gram>=1` iken `need=''`.
- Düzeltme: `f.gram>=1` olsa bile `nextAct(tp).k` varsa `s`'ye "Sıradaki (isteğe bağlı): Aşama 2 · Tanı" ekle ve `nextHtml` bütün görevler bitince bu bonus adımı düğme olarak göstersin; ya da Anla'yı tek başına puanlama (Anla+Tanı birlikte = 25).

## [ÖNEM: orta] "Sıradaki adım: Yazmaya başla" düğmesi Yazma kutusu açıkken kutuyu kapatıyor
- Kullanıcı ne görüyor: Yazma görevini açıp 2 cümle yazdı; "Sıradaki adım · +7 puan · 1 cümle daha · Yazmaya başla"ya dokununca kutu kapanıyor (metin kaybolmuyor ama ekrandan gidiyor). Tekrar dokununca açılıyor.
- Tekrar üretme: `bugun/t12.js` → `görev satırına dokununca textarea: true`, `ardından "Yazmaya başla"ya dokununca textarea: false`, `2 cümleden sonra … açık mı: false`.
- Kök neden: `ACT.task` 6834-6841, satır 6839 `OPEN=OPEN===id?null:id` (aç/kapa); sıradaki-adım düğmesi aynı eylemi kullanıyor (nextHtml 5821 `data-act="task"`).
- Düzeltme: sıradaki-adım düğmesine `data-open="1"` ekle ve `ACT.task`'ta `OPEN=b.dataset.open?id:(OPEN===id?null:id)`; açınca textarea'ya odaklan.

## [ÖNEM: orta] Bütün görevler bitince "Sıradaki adım" kartı düğmesiz; "başka bir ezber tablosu çalış ya da yeni bir konuya başla" diyor ama hiçbir yere götürmüyor, yarını da söylemiyor
- Kullanıcı ne görüyor: 100/100'de kart: "BUGÜN · Bugünün planı tamam. Ausgezeichnet! · İstersen başka bir ezber tablosu çalış ya da yeni bir konuya başla." Dokunulacak öğe yok. Ayrıca günün konusunun bir sonraki aşaması (ör. Anla sonrası Tanı) açıkken bile yeni konu öneriyor.
- Tekrar üretme: `bugun/t7.js` (`--- yazma bitti` ve `--- yeniden render`: `SIRADAKI: [BUGÜN] … | btn=-`; nextC HTML'inde button yok).
- Kök neden: `nextHtml()` 5817 `if(!nx)return '<div …>…</div>'` düğmesiz sabit metin.
- Düzeltme: `nextAct(tp).k` varsa "Bonus: <ACTB>" düğmesi (`data-act="lesson"`), yoksa `newTopic()` için "Yeni konu" ve `ACT.tab ezber` düğmesi; altına "Yarın: ~N kart · <konu> <aşama> · <tablo> tekrarı" satırı (bkz. tasarım bulgusu).

## [ÖNEM: orta] Yazma görevi: başlık "Yazma · 3 cümle · <günün konusu>" ama içerik/konu/dil kontrolü yok; anlamsız Türkçe satırlar da 20 puan
- Kullanıcı ne görüyor: "Yazma · 3 cümle · Perfekt" altına `Ich esse gern Pizza. Das Wetter ist schön heute. Mein Hund heißt Max.` (Perfekt yok) → "Tamam · 3 cümle · 20/20". `bugün çok yoruldum ama. aaa bbb ccc. x y z` → yine 20/20. Başka bir konunun Üret aşamasını kaydetmek de (usave) metni buraya ekleyip 20 veriyor; başlık yine günün konusunu gösteriyor.
- Tekrar üretme: `bugun/t4.js` (`--- konu dışı 3 cümle sonrası`, `--- anlamsız 3 "cümle" sonrası`).
- Kök neden: `sentN()` 3331 yalnız "en az 3 harf dizisi" sayıyor (ASCII; Türkçe kelimeler parçalanıp yine sayılıyor); `taskDefs()` 5807 başlıkta `tp[2]`.
- Düzeltme: başlığı "Yazma · 3 Almanca cümle" yap, konu adını yalnız öneri olarak göster ("Önerilen konu: Perfekt"); `sentN`'de cümle başına en az 1 Almanca sözlük kelimesi (POOL/PK) ya da Türkçeye özgü harf (ç ğ ı ş) içermeme şartı koy; Üret'ten gelen metin için `s`'ye "(Perfekt · Üret'ten)" kaynağını yaz.

## [ÖNEM: orta] "Bugünün teması" kartı görevlerle tutarsız ve tekrarlı; "kelimeleri ekle" düğmesi ekranda kalıyor, ikinci dokunuşta "0 kelime eklendi"
- Kullanıcı ne görüyor:
  1. Kart "Dört adım aynı konunun etrafında: **Ezber bu konunun tablosundan (Ayrılan ve ayrılmayan ön ekler, Modalverben)**" diyor; aynı ekrandaki Ezber görevi "Ezber: sein ve haben" (vadesi gelen başka tablo). (`bugun/t8.js` "G6 açılış": tema Modalverben, `ez: "Ezber: sein ve haben"`.)
  2. Konu adı ekranda 4 kez geçiyor (tema başlığı, "Konu: …", "Yazma · 3 cümle · …", tema metni) ama puanı başka konular kazandırabiliyor (yukarıdaki bulgular) — kart "dört adım aynı konunun etrafında" diyerek yanlış güven veriyor.
  3. "Konunun 14 kelimesini kelime tekrarına ekle"ye dokununca bildirim "14 kelime eklendi" ama düğme yerinde kalıyor; tekrar dokununca "0 kelime kelime tekrarına eklendi". Eklenen 14 kelime Kelime görevinin hedefine girmiyor (görev "0 / 10 kart" kalıyor, Kelimeler sekmesi 24 kart bekliyor) ve "yeni kelime · önce tahmin et" tanıtımı olmadan doğrudan "Almancası hangisi?" diye soruluyor (`bugun/t15.js`: kuyruğun ilki `t:g1:3`, tip `tr2de`; `bugun/t16.js`).
- Kök neden: `vBugun()` 5839-5843 tema metni sabit; `ezToday()` 7239-7241 önce vadesi gelen tabloyu seçiyor. `ACT.gwadd` 6924 `drawPage()` çağırıyor; Bugün sekmesinde `X` boş olduğundan `drawPage()` 6075-6076 hiçbir şey yapmıyor (render yok). `ensureTarget()` 3325 hedefi gün başında sabitliyor; `gwadd` kartları `S.srs`'e `d=t` ile yazdığından `rvType()` onları "intro" saymıyor.
- Düzeltme: tema metnini görevlerden üret ("Ezber: <et.t> (vadesi geldiği için)" / "bu konunun tablosu"); ya da kartı kaldırıp konu adını yalnız Konu görevinde göster. `ACT.gwadd`'de `X?drawPage():render()`. gwadd kartlarını `S.srs`'e yazmak yerine kuyruğa "yeni" olarak (intro) ekle ya da `d.wt`'yi eklenen sayı kadar artır.

## [ÖNEM: düşük] "Tekrar zamanı gelen konular" kartı: satırda "tekrar" 3 kez, gecikme yok, puanla ilişkisi belirsiz
- Kullanıcı ne görüyor: "Modalverben im Präteritum · 4/4 aşama · sıradaki: tekrar · [tekrar] · %85". Kaç gündür beklediği (vadesi 2 gün önce geçmiş) yazmıyor. Kart günün planından ayrı duruyor; buradaki bir tekrar yapılınca puan "Konu: <günün konusu>" altına yazılıyor (yüksek önemli Konu bulgusu, yol 1) ve kart kayboluyor, yapılan iş Bugün'de iz bırakmıyor.
- Tekrar üretme: `bugun/t13.js` (CARD6), `bugun/t2.js`.
- Kök neden: `vBugun()` 5851-5852 `topicLi()` 5904 (Konular listesinin satırı aynen); `liSub()` 6110.
- Düzeltme: Bugün'e özel satır: "Modalverben · tekrar 2 gün gecikti · 8 soru" + "Bugün yapılan tekrarlar: Perfekt ✓ 8/8" alt listesi; birden çok konu bekliyorsa "Puan için biri yeter; diğerleri yarına kayabilir" notu.

## [ÖNEM: düşük] Hata haritası ve aylık deneme kartları doğru çalışıyor; yalnızca yer/öncelik sorunu
- Doğrulanan: Hata kartı son 14 günü doğru sayıyor (14 günden eski 9 hata dışarıda, "Son 14 günde 3 hata"); "Tümü" hata sayfasını, çipler ilgili tabloyu/konuyu açıyor. Aylık deneme kartı son ölçümden ≥30 gün sonra çıkıyor, deneme bitince kayboluyor (`bugun/t13.js`).
- Sorun: Aylık deneme kartı "Bugünün teması" ve "Sıradaki adım"ın ÜSTÜNDE çıkıyor; puana katkısı olmadığı yazmıyor. Hata haritası kartı İlerleme'deki "Hata haritam" kartının ilk satırının kopyası. Kök neden: `vBugun()` 5835 (deneme kartı sıralaması), 5849-5850.
- Düzeltme: deneme kartını "Sıradaki adım"ın altına al ve "puana girmez · ayda bir" etiketi ekle; hata kartını "Sıradaki adım" bitince (ya da 100/100 kartında) "bonus: Partizip biçimi tablosu" önerisi olarak birleştir.

## [ÖNEM: yüksek · TASARIM] Uygulamayı kapatıp açınca Bugün "ne yaptım / hangi konuda / ne kaldı / yarın ne var" sorularını cevaplamıyor
- Kullanıcı ne görüyor (`bugun/t14.js`, akşam yeniden açılış, tam ekran metni): "72/100 · Kelime 5/10 kart · **Konu: Modalverben · Tamam · bir aşama bitti** · **Ezber: Ayrılan ve ayrılmayan ön ekler · Tamam · 1 tablo çalışması** · Yazma 1/3 cümle". Gerçekte o gün: Modalverben'de Anla'yı yeniden yaptı + Pekiştir tekrarını 8/8 geçti (sonraki tekrar 15 Eki), **Modalverben** tablosunu 12/12 test etti (başlıktaki tablo değil), 5 kelime. Ekrandan bunların hiçbiri okunmuyor:
  - **Ne yaptım?** Hangi konu, hangi aşama, kaç doğru → yok ("bir aşama bitti"). Hangi tablo, kaç doğru → yok ("1 tablo çalışması"). Kaç kelime doğru/yanlış → yok (sayaç cevap sayıyor). Yazdığı cümle yalnız Yazma satırı açılınca görünüyor.
  - **Ne kaldı?** "Eksik:" satırları var (iyi), ama bir görev "Tamam" olunca günün konusunun açık bir sonraki aşaması (ör. Tanı) hiçbir yerde görünmüyor; Kelime'de kuyrukta kalan kartlar "Tamam"dan sonra görünmüyor.
  - **Yarın ne var?** Hiçbir şey. Veri hazır: yarın vadesi gelecek 5 kart, Modalverben tablosu yarın tekrar (`S.ez.modal.due=2026-10-09`), Perfekt başlıyor; Üret'i bekleyen konular "yarın açılır". Bu bilgi yalnız Konular sekmesinin "Bugünün konusu" kartında ("Bugünlük tamam. tekrar yarın açılır") ve tek tek konu sayfalarında var.
  - **Dün ne yaptım?** Bugün'den takvime/geçmişe bağlantı yok; İlerleme'deki takvim yalnız sayı gösteriyor, hücreye dokununca ayrıntı yok.
- Kök neden: gün kaydı (`S.days[t]`) yalnız sayaç tutuyor (w, g, gs, ez, ezt, sch); `lessonEnd()` 6250, `ezEnd()` 7305, `grade()` 3277 neyin yapıldığını güne yazmıyor; `vBugun()` 5828 yalnız `taskDefs()` sayaçlarını gösteriyor.
- Önerilen çözüm:
  1. Gün kaydına olay listesi: `d.log=[{t:'g',id,k,ok,n,pass},{t:'ez',ids,ok,n},{t:'w',ok,no},{t:'sch',src}]` (lessonEnd, usave, ezEnd, ezFillCheck, rvAdvance kuyruk boşalınca).
  2. Her görev satırının `t2`'si bu listeden: "Modalverben · Pekiştir 8/8 ✓ (sonraki 15 Eki)", "Modalverben tablosu 12/12 ✓ · sein ve haben: yapılmadı", "10 kart: 8 doğru, 2 yarına".
  3. Bugün'ün en altına "Yarın" kartı: `~N kart` (S.srs d≤yarın), konular (`nextAct().wait===yarın` + `x.due===yarın`), tablolar (`ez.due===yarın`). 100/100 kartının metnine de aynı özet.
  4. Takvim hücresine dokununca o günün `d.log` özetini açan küçük sayfa; Bugün başlığındaki tarihin yanına "‹ dün" bağlantısı.

## [ÖNEM: düşük] Günün ilk çiziminde seri rozeti ile "seri güvende" yazısı çelişebiliyor
- Kullanıcı ne görüyor: Kart olmayan günde (hedef 0) ilk açılışta "Minimum gün tamam, seri güvende" yazarken üst rozet "0 gün seri". Bir sonraki çizimde düzeliyor.
- Tekrar üretme: `bugun/t15.js` ilk satır (`wt=0`, `0 gün seri`, verdict "Minimum gün tamam, seri güvende").
- Kök neden: `render()` 5775-5776 `setStreak()`'i `vBugun()` → `ensureTarget()` (d.wt'yi yazan) ÇAĞRILMADAN önce çalıştırıyor.
- Düzeltme: `render()`'da `setStreak()`'i `$('main').innerHTML=…` satırından sonra çağır (ya da `ensureTarget()`'i render başında çağır).

## Doğrulanan ve sorunsuz olanlar (bulgu değil, kayıt için)
- Halka, "Bugünün puanı" kartındaki sayı, görev puanlarının toplamı ve "Kalan N puan" satırı her denenen durumda birbirini tutuyor (ör. 15+25+25+7=72, kalan 28). `refreshScore()` yazarken de aynı.
- Çok günlü akış (`bugun/t8.js`, 8→9→(10 atlandı)→11→12→13 Ekim): kelime hedefi her gün yeniden hesaplanıyor (10→20→23→25→25, tavan 25); günün konusu gün içinde sabit, Perfekt Anla/Tanı/Kur → ertesi gün Üret → vadesi gelince Pekiştir → geçince yeni konu (Modalverben) sırası doğru; seri atlanan günden sonra 0, kelime biten günden sonra 1; takvim 11 Ekim'i "minimum gün" (sarı) gösteriyor. Tek istisna yukarıdaki kritik `migrate` bulgusu (ilk günün puanı).
- "Sıradaki adım" düğmeleri: Kelime → kelime tekrarı; Konu → günün konusunun sıradaki aşaması (Anla/Tanı/Kur/Üret/Pekiştir) doğrudan açılıyor; konu beklemedeyse "Yeni konu: …" Anla'yı açıyor; Ezber → günün tablosunun sayfası (vadesi gelen ≥2 tablo varsa doğrudan karışık test); Yazma → Bugün içinde yazı kutusu. Tıklanınca her durumda bir şey oluyor (Yazma'daki aç/kapa sorunu hariç).
- Hata haritası kartı, "Tümü" ve çip bağlantıları; aylık deneme kartının çıkıp kaybolması doğru (`bugun/t13.js`).
