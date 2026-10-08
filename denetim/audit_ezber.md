# Denetim: Ezber · İlerleme · Defter · Kalıplar · Ayarlar · mergeS
Betikler: scratchpad/v22/ezber/ (lib.js + t*.js). Çalıştırma: `NODE_PATH=$(npm root -g) node tX.js`
Satır numaraları: scratchpad/v22/base/index.html

## [ÖNEM: yüksek] Bugün'deki "Ezber: X" başlığı, gerçekte çalışılan tabloyu değil günün seçilmiş tablosunu gösteriyor; başka tablo çalışınca X "Tamam" görünüyor
- Kullanıcı ne görüyor: 13 Eki'de Bugün'de görev "Ezber: Ayrılan ve ayrılmayan ön ekler · Tamam · 1 tablo çalışması · 25/25". Oysa o gün yalnız "sein ve haben" tablosu test edildi; "ön ekler" tablosuna hiç dokunulmadı (Ezber sekmesinde hâlâ %0). Perfekt/Modalverben şikâyetinin birebir ezber karşılığı: başlıktaki tablo bitmiş gibi görünüyor.
- Tekrar: `ezber/t1_ezdays.js` → 2026-10-13 satırı: `ezd=prefix … test sein ve haben … Bugün ez: Ezber: Ayrılan ve ayrılmayan ön ekler | Tamam · 1 tablo çalışması | 25/25`.
- Kök neden: `taskDefs` (satır 5804) başlığı `ezToday()` (d.ezd, satır 7237-7243) ile yazıyor; puan ise `frac().ez` (satır 3343) gün sayaçları `d.ezt/d.ez` ile hesaplanıyor; bu sayaçlar hangi tabloda çalışıldığını tutmuyor (`ezRecord` 7289, `ezEnd` 7312, `ezFillCheck` 7433).
- Düzeltme: gün içinde çalışılan tabloları kaydet (`d.ezl=[tid,…]` → `ezEnd`/`ezFillCheck`'te push). Başlık: tamamlandıysa "Ezber: <çalışılan tablo(lar)> · Tamam", değilse "Ezber: <ezToday>". Ya da çalışılan ilk tabloyu `d.ezd`'ye yaz (`if(!d.ezdDone){d.ezd=tid;d.ezdDone=1}`).

## [ÖNEM: yüksek] Ezber tablosu birkaç dakikada "oturdu" (%100) sayılıyor: aynı oturumda iki test yeter
- Kullanıcı ne görüyor: "sein ve haben" tablosunu üst üste iki kez test ediyor (12/12, 12/12, toplam ~2 dk) → tablo %100, "12 / 12 hücre oturdu", Ezber yolunda "1/12 tablo oturdu", yeşil nokta. Hiç ara verilmeden "oturdu" etiketi kazanılıyor; İlerleme'deki ezber yüzdesi ve sınav tahmini (Sprechen %20 ezber) de buna göre yükseliyor.
- Tekrar: `ezber/t1_ezdays.js` → "ez state after 2 tests … cells2: 12, cellsTot: 12", tablo sayfası "%100 … 12 / 12 hücre oturdu". `levels().e1` 0 → 0.083.
- Kök neden: `ezMark` (7288) hücre serisini her doğru cevapta +1 yapıyor, aynı gün/aynı dakika ayrımı yok; `ezProg` (7231) "seri ≥ 2"yi oturdu sayıyor. `ezPick` (7277) en düşük serili hücreleri seçtiği için ≤12 hücreli tablolarda ikinci test bütün hücreleri tekrar sorar. Aynı durum "Boş tabloyu doldur" ile de var (iki kez doldur → %100).
- Düzeltme: hücre serisini günde en fazla bir kez artır (`e.cd={k:tarih}`; `if(ok&&e.cd[k]===today())return;`) ya da "oturdu" için ikinci doğrunun farklı bir günde olmasını şart koş.

## [ÖNEM: orta] Test bitince "12/12 Harika" ama tablo %0 ya da %50 görünüyor; ne zaman tekrar edileceği söylenmiyor
- Kullanıcı ne görüyor: İlk testte 12/12 → sonuç ekranı "Harika. Bir sonraki tekrar daha ileri bir günde." ve hemen altındaki tablo satırı "%0". Bir gün sonra yarıyı bilemeyip ertesi gün 12/12 yapınca yine "Harika" + "%50". "Daha ileri bir gün" hangi gün? Söylenmiyor (tarih yalnız tablo sayfasında `ezStatus`). "Oturdu"nun ne demek olduğu (hücre başına art arda 2 doğru) hiçbir yerde yazmıyor.
- Tekrar: `ezber/t1_ezdays.js` → "Test1 sonu ekranı … 12 / 12 Harika … sein ve haben … %0"; 2026-10-11 "12 / 12 Harika … %50".
- Kök neden: `ezEnd` (7305-7322) mesajı tarih içermiyor; `ezLi` yüzdesi `ezProg` (seri≥2) — testin yüzdesiyle farklı ölçü.
- Düzeltme: `ezEnd`'de tablo başına "Sıradaki tekrar: <trShort(e.due)> · X/Y hücre oturdu (bir hücre 2 farklı testte doğru olunca oturur)" satırı. %80 altı için de tarihi yaz.

## [ÖNEM: orta] Vakti gelmeden yapılan testler tekrar aralığını büyütüyor: 5 gün üst üste test → 30 gün sonraya atlıyor
- Kullanıcı ne görüyor: Tablo 14 Eki'de tekrar edilecekken 12, 13, 14 Eki'de "Test et"e basınca her seferinde aralık büyüyor: 12 Eki → 19 Eki, 13 Eki → 27 Eki, 14 Eki → 13 Kas. Ardışık günlerde "tıkıştırma" uzun süreli tekrar sayılıyor; tablo bir ay hiç sorulmuyor.
- Tekrar: `ezber/t1_ezdays.js` → 2026-10-12/13/14 satırları (`n:3 due 10-19`, `n:4 due 10-27`, `n:5 due 11-13`).
- Kök neden: `ezSchedule` (7299-7303): `acc>=.8` ise `e.n++` (gün farklıysa) — `e.due` henüz gelmemiş olsa bile. Başarısız testte `e.n` hiç düşmüyor (10-10: 6/12 → n=1 kalıyor, sonraki başarı yine n+1).
- Düzeltme: `if(!e.due||e.due<=t){e.n++…}` (vadesinden önceki test aralığı uzatmasın; yalnız `best`/hücreler güncellensin). Başarısızlıkta `e.n=Math.max(0,e.n-1)` ya da 1'e indir.

## [ÖNEM: kritik] Yeni kullanıcının ilk günü ertesi açılışta geriye dönük değişiyor: takvimde 100 → 65; seviye testi sonucu ve "Zaten biliyorum" işaretleri siliniyor
- Kullanıcı ne görüyor: Uygulamayı ilk kez kurduğu gün seviye testi yapıyor ("A2 %30"), bir konuyu "Zaten biliyorum" diye işaretliyor, bütün görevleri bitirip Bugün'de **100/100** görüyor; takvimde de 100. Ertesi sabah açınca: İlerleme takviminde o gün **65**, "A2 tamamlandı" %30 → **%1** (test sonucu `vest` silindi), "biliyorum" işareti ve `gdone` kaydı yok. Hiçbir açıklama yok; "dün yaptığım iş kayboldu" hissi.
- Tekrar: `ezber/t4_fresh.js`. Çıktı: `Gün1 Bugün puanı: 100 … Kayıttaki göç bayrakları: { scv: undefined, rk1: undefined, rk2: undefined, gs1: undefined } … Gün1 takvim: 100` → ertesi gün `9 Eki kaydı: {… "sc0":65 …}`, `Gün2 takvim: 65`, `A2: 1, vest: 'null', g5: undefined, gdone: '{}'`.
- Kök neden: `blank()` (satır 3122-3126) göç bayraklarını (`scv`, `rk1`, `rk2`, `gs1`) içermiyor; `migrate()` boş durumda (`if(!s…)return blank();` 3129) bayrak koymadan dönüyor. Kayıt bayraksız saklanıyor ve sonraki `load()`'da eski kullanıcılar için yazılmış göçler yeni kullanıcıya uygulanıyor: 3141-3147 (`scv!==8`: geçmiş günler ESKİ formülle `sc0` olarak dondurulur — ezber puanı yok, konu 15, "h" alanı artık hiç dolmuyor), 3153-3156 (`rk2`: `known`, `base`, `vest` silinir, `last`'ı olmayan konu kayıtları silinir), 3157-3159 (`rk1`: `known` + `gdone` silinir), 3150-3151 (`gs1`). Aynı bayraksız kayıt senkronla buluta giderse `mergeS` içindeki `migrate(cp(R))` (8319) öteki cihazda da eski `sc0`'ları `mergeDay` ile (x==null → R değeri) yerel günlere taşır.
- Düzeltme: `blank()`'e `scv:8,rk1:1,rk2:1,gs1:1` ekle (bundan sonra eklenecek her göç bayrağı da blank()'e girmeli). Ayrıca `migrate` sonunda bayraklar değiştiyse hemen `saveLocal()`.

## [ÖNEM: yüksek] İki cihazda aynı anda eklenen notlar ve kendi kelimeler birleşince biri kayboluyor; bir cihazda not silmek ötekinin farklı notunu da siliyor
- Kullanıcı ne görüyor: Telefonda Defter'e "Toplantıyı yarına erteleyebilir miyiz?" notu ve "Wiederholung" kelimesini, bilgisayarda (senkron gelmeden) "Faturayı e-postayla gönderir misiniz?" notu ve "Hantel" kelimesini ekliyor. Eşitlemeden sonra her iki cihazda da yalnız biri kalıyor (not da kelime de kartı da). Telefonda kendi notunu silince bilgisayardaki başka bir not da siliniyor.
- Tekrar: `ezber/t3_merge.js` → `A notes [n1:Toplantı…] mine [m:2:Wiederholung]`, `B notes [n1:Faturayı…] mine [m:2:Hantel]`, `1) MERGE notes [n1:Faturayı…] mine [m:2:Hantel] srs m: [m:2]`; `2) A, n1 notunu sildi; B tarafında birleşince B notları: [] tomb {n1:1}`.
- Kök neden: Kimlikler cihaza özgü sayaçtan: `ACT.nsave` 'n'+(++S.seq) (satır 7193), `awsave` / `ACT.ncard` 'm:'+(++S.seq) (6967, 7202). İki cihazın `seq`'i aynı yerden artar → aynı kimlik. `unionId` (8317) kimliğe göre tekilleştiriyor, `srs` (8330) kimliğe göre üzerine yazıyor, `tomb` (8340) kimliğe göre siliyor.
- Düzeltme: not ve kendi kelime kimliklerini `uid('n')` / `uid('m:')` ile üret (S.qn ve S.wl zaten `uid` kullanıyor, 7927). Eski kayıtlar için birleşmede aynı kimlik + farklı içerik görülürse birini yeniden adlandır.

## [ÖNEM: yüksek] Kaldırılan "Zaten biliyorum" işareti öteki cihazdan geri geliyor; işaret kaldırılsa bile "biten konu" kaydı (gdone) geri dönüyor
- Kullanıcı ne görüyor: Konuyu yanlışlıkla "Zaten biliyorum" yapıp telefonda geri alıyor. Bilgisayar daha sonra başka bir iş yaptıysa (ör. not ekledi) eşitlemeden sonra işaret iki cihazda da yeniden "✓ Biliyorum". Telefon daha yeniyse işaret kalkık kalıyor ama konu "biten konu" olarak sayılmaya devam ediyor: İlerleme → "Ne zaman?" kartı "0,3 haftada biten konu" ve bir bitiş tarihi gösteriyor, oysa konu "sırada" (tstat=next) ve hiç çalışılmadı.
- Tekrar: `ezber/t3_merge.js` bölüm 3 → `merge(C yerel, D bulut): known= true`, `merge(D yerel, C bulut): known= true`, `C daha yeni iken merge(C, D): known= false gdone= 2026-10-09`, `İlerleme "Ne zaman?": … 0,3 haftada biten konu`, `g5 tstat= next`.
- Kök neden: `mergeGx` (8305-8316) konu nesnesini bütün olarak "S.mt'si daha yeni olan cihazdan" alıyor (`m=cp(bNewer?b:a)`); `known`'ın kendi zaman damgası yok. `mergeS` 8332: `gdone` için yalnız ekleme var (`if(!M.gdone[id]||…)M.gdone[id]=R.gdone[id]`), silme taşınmıyor (yalnız `rs` için temizleniyor, 8334).
- Düzeltme: `gknown`'da `x.kt=Date.now()` yaz; `mergeGx`'te `known`'ı `kt`'si büyük olandan al. `gdone`'u birleştirdikten sonra `for(id in M.gdone)if(!tstatOf(M.gx[id]||{}))delete M.gdone[id];`.

## [ÖNEM: orta] Aynı gün iki cihazda yazılan cümleler birleşince birinin yazdıkları siliniyor; sayaçlar toplanmıyor (puan şişmiyor ama düşük kalıyor)
- Kullanıcı ne görüyor: Telefonda Yazma görevine 2 cümle, bilgisayarda 1 cümle yazıyor (toplam 3). Eşitlemeden sonra yalnız uzun olan metin kalıyor; bilgisayardaki "Am Abend rufe ich meine Mutter an." kayboluyor ve Yazma 13/20'de kalıyor. Aynı şekilde iki cihazda yapılan 12+12 ezber cevabı 12, iki tablo testi 1 sayılıyor.
- Tekrar: `ezber/t3_merge.js` bölüm 4 → `E gün … sch:"Ich gehe … Gemüse."`, `F gün … sch:"Am Abend rufe ich meine Mutter an."`, `MERGE gün … sch:"Ich gehe … Gemüse."` · `puan E/F/M: [38, 32, 38]`.
- Kök neden: `mergeDay` (8296-8303): sayılar `Math.max`, metin "uzun olan kazanır". Soru: Math.max puanı şişiriyor mu? → Hayır; şişirme bulunmadı, tersine iki cihazdaki iş toplanmıyor (eksik sayım) ve metin kaybı var.
- Düzeltme: `sch` için satır birleşimi (`x.split('\n')` ∪ `y.split('\n')`, sırayı koru). Sayaçlar için cihaz başına alt sayaç (`d.ezc={devA:12,devB:12}` → toplam) ya da en azından `sch` kaybını önle.

## [ÖNEM: orta] Aynı ezber tablosu iki cihazda çalışılınca hücre sonuçlarının biri tamamen atılıyor ve iki cihaz hiç uzlaşmıyor
- Kullanıcı ne görüyor: "Modalverben" tablosunda bilgisayarda 24, telefonda 12 hücreyi doğru bildi (birleşimi 31 hücre). Birleşince telefon kendi 12'sinde, bilgisayar kendi 24'ünde kalıyor; her eşitlemede ikisi de kendi hâlini buluta yazıyor (birbirini ezip duruyor).
- Tekrar: `ezber/t3_merge.js` bölüm 5 → `G1: 24 n 1 | G2: 12 n 1`, `merge sonrası doğru hücre: 12 / 24 (iki cihazın birleşimi olmalıydı: 31)`.
- Kök neden: `mergeS` 8336: tablo kaydı bütün olarak seçiliyor (`n` büyük olan, eşitse `last` büyük olan, o da eşitse yerel L) — hücre (`e.c`) birleşimi yok, eşitlikte belirleyici bir kural yok.
- Düzeltme: `e.c` hücre bazında birleştir (her hücre için daha yeni olanı; hücreye tarih eklemek gerekir) ya da en azından `Math.max`; `n/due/best/last` için ayrı ayrı max/later. Eşitlikte deterministik seçim (ör. `stable()` karşılaştırması).

## [ÖNEM: yüksek] "Ne zaman?" tahmini yılsız tarih gösteriyor ve "Zaten biliyorum" işaretlerini biten konu sayıyor
- Kullanıcı ne görüyor: Hiç ders yapmadan bir konuyu "Zaten biliyorum" yapınca İlerleme → Ne zaman? kartı: "**8 Eyl** A2 konuları bu hızla biter · **22 Mar** B1 sonu · 0,3 haftada biten konu". 8 Eyl aslında 8 Eylül **2028**, 22 Mar ise **2030** (bugün 9 Eki 2026); yıl yazmadığı için "8 Eyl" geçmiş bir tarih, "22 Mar" önümüzdeki bahar gibi okunuyor. 4 konuyu "biliyorum" yapınca "1 haftada biten konu", "12 Mar / 30 Tem" (2027) ve "Bu hafta: 4 oturan konu" çıkıyor — oysa bu hafta hiçbir konu çalışılmadı.
- Tekrar: `ezber/t6_tahmin.js` → `1 "biliyorum" sonrası: NE ZAMAN? 8 Eyl A2 … 22 Mar B1 … 0,3 haftada biten konu`, `4 "biliyorum" sonrası: … 12 Mar … 30 Tem … 1 haftada biten konu … 4 oturan konu`.
- Kök neden: `vIlerleme` (6027-6035) tarihleri `trShort` (gün+ay, yılsız; 3105) ile yazıyor. `pace()` (5751-5754) ve `weekStats` (6012 `r.g`) `S.gdone`'u sayıyor; `gknown` (6923) "biliyorum" işaretinde de `gdone`'a bugünün tarihini yazıyor.
- Düzeltme: tahmin tarihleri `trDate` (yıllı) ya da "≈ 23 ay sonra" biçiminde. `gknown` `gdone` yazmasın (ya da `pace`/`weekStats` `known` olanları atlasın: `if(!gpeek(id).known)`), "biliyorum" ayrı bir satırda gösterilsin.

## [ÖNEM: yüksek] Takvimde bir güne dokununca hiçbir şey olmuyor; "ne zaman ne yaptım" sorusu İlerleme'den cevaplanamıyor (tasarım)
- Kullanıcı ne görüyor: Puan takviminde yalnız sayı (100, 25, 30, –) var. 5 Eki'ye dokununca hiçbir şey açılmıyor; o gün hangi konunun hangi aşaması, hangi ezber tablosu, kaç kart, hangi cümleler yapıldı görülemiyor. "Bu hafta" kartı yalnız toplamlar veriyor; ezber tablosu adı, konu adı hiçbir yerde gün gün geçmiyor. Rapor (Claude metni) da gün listesi vermiyor (yalnız yazılar).
- Tekrar: `ezber/t5_ilerleme.js` → `Takvim hücresine dokunma: sayfa açıldı mı? false | hücre: <div class="c" style="…">100</div>` (data-act yok).
- Kök neden: `vIlerleme` takvim döngüsü (6048-6055) düz `<div>` üretiyor; gün ayrıntısı sayfası yok. Veri kısmen var ama dağınık: `S.days[k]` (w, g, gs, gt, ez, ezt, ezd, sch), `S.al[k]` (gün × bölüm cevap/doğru sayısı, `logAns` 7929), `gx[id].stg` (aşama tarihleri), `gx[id].rv` (tekrar tarihleri). Ezber için yalnız `S.ez[id].last` tutuluyor — hangi gün hangi tablo çalışıldı geçmişi YOK; `d.gt/d.ezd` ise "günün önerisi", çalışılanı değil (bkz. Perfekt/Modalverben şikâyeti).
- Düzeltme: (1) Gün kaydına olay listesi: `d.log.push({t:'ez',id,ok,n})`, `{t:'stg',id,k}`, `{t:'rv',id}`, `{t:'w',n}` (`ezEnd`, `ezFillCheck`, aşama geçişi, `grade`). (2) Takvim hücresine `data-act="dayv" data-k="YYYY-MM-DD"` → tam sayfa "9 Ekim Cuma · 100 puan": Kelime 10/10 kart · Konu: Perfekt — Aşama 2 Tanı geçildi (%88) · Ezber: sein ve haben testi 12/12 · Yazma: 3 cümle (metin). (3) Gelecek için aynı sayfada "Sırada": tekrar tarihi gelen konu/tablo listesi (gx.due, ez.due) — "ne zaman ne yapacağım" sorusu da şu an hiçbir ekranda toplu yok (ezber tekrar tarihleri yalnız her tablonun kendi sayfasında).

## [ÖNEM: orta] Sınav tahmini (Hören) hâlâ kaldırılmış Diktat'a dayanıyor: "0 diktat cümlesinden", Hören en fazla 80 olabilir
- Kullanıcı ne görüyor: İlerleme → "Sınava bugün girsem?" Hören satırı "kelime, gramer ve **0 diktat cümlesinden**". Diktat'a giden hiçbir düğme yok (6 sekme + Ayarlar/Kalıplar/Rapor tarandı: 0). Hören'in %20'si hiçbir zaman dolmayacak bir sayaca bağlı: her şeyi %100 bilen biri bile Hören 80 görür; geçme sınırı 60 olduğu için "en zayıf modül" sürekli Hören görünür. Aynı sayı Rapor metnine de gidiyor ("Sınav tahmini … Hören").
- Tekrar: `ezber/t5_ilerleme.js` → `Hören 0 / 100 kelime, gramer ve 0 diktat cümlesinden`, `Diktat düğmesi bulunan ekranlar: []`. Kod: `data-act="diktat"` yalnız Diktat sayfasının kendi "Yeniden" düğmesinde (7490).
- Kök neden: `exam()` 5744: `.2*Math.min(1,P.dk/300)`; `practice()` 5735-5739 `d.dk` topluyor; `d.dk` yalnız `ACT.dkcheck` (6902) ile artıyor.
- Düzeltme: Hören'i `100*(.6*v+.4*g)` (ya da dinlemeye dayalı başka bir gerçek ölçü: kelime tekrarındaki "listen" kartlarının doğruluğu `S.al[*].w`) yap, açıklamayı "kelime ve gramerden" olarak değiştir; `practice().dk`'yı kaldır. Diktat kodu (`dkItems`…`startDikt` 7469-7514, ACT.diktat/dk* 6899-6905) ölü kod — ya geri getirilsin ya silinsin.

## [ÖNEM: düşük] "Bu hafta" kartı Pazartesi sabahı "0 ortalama puan · geçen haftaya göre -22" diyor; "90+ gün / minimum gün" kesir gibi okunuyor
- Kullanıcı ne görüyor: Yeni haftanın ilk saatinde, daha hiçbir şey yapmadan "0 ortalama puan · geçen haftaya göre -22". Ayrıca "0 / 0 · 90+ gün / minimum gün" ifadesi "0'dan 0'ı" gibi okunuyor (aslında iki ayrı sayı). "tekrar edilen kart" sayısına ilk kez gösterilen yeni kelimeler de giriyor (`introDone` d.w'yi artırıyor, 3274).
- Tekrar: `ezber/t5_ilerleme.js` (12 Eki 08:00) → `BU HAFTA · 12 EKİ – 18 EKİ 0 ortalama puan · geçen haftaya göre -22 … 0 / 0 90+ gün / minimum gün`.
- Kök neden: `weekStats` (6008-6014) bugünü (henüz bitmemiş gün) ortalamaya katıyor; etiket 6059-6063.
- Düzeltme: ortalamaya bugünü yalnız puanı >0 ise ya da gün bittiyse kat; karşılaştırmayı "geçen haftanın aynı günlerine göre" yap. "90+ gün: 2 · minimum gün: 1" diye iki ayrı kutu. "tekrar edilen kart" → "çalışılan kart".

## [ÖNEM: düşük] Rapor metninde bölüm numaraları atlıyor (1, 2, 4, 5, 6, 7, 8, 10)
- Kullanıcı ne görüyor: Claude'a giden raporda "## 3" ve "## 9" yok; düzen hastası kullanıcıya eksik bölüm varmış gibi görünür.
- Tekrar: `ezber/t5_ilerleme.js` → `Rapor ## başlıkları: ## 1 … ## 2 … ## 4 … ## 10`.
- Kök neden: `rpText` (8021-8099) silinen bölümlerden sonra numaralar güncellenmemiş; `var nh=…` (8069) hesaplanıp kullanılmıyor.
- Düzeltme: başlıkları sayaçla üret (`var sec=0;function H(t){o.push('## '+(++sec)+'. '+t);}`), `nh` satırını sil.

## [ÖNEM: yüksek] Kelime tekrarı açıkken senkron gelirse "Devam" düğmesi çalışmıyor (sayfa hatası)
- Kullanıcı ne görüyor: Telefonda kelime tekrarı yaparken başka uygulamaya geçip dönüyor (ya da 2 dk'lık otomatik eşitleme çalışıyor) ve bilgisayarda o gün bir şey değişmişse: ekrandaki kartta "Devam"a / "Doğru tahmin → devam"a basınca hiçbir şey olmuyor; kart aynı kalıyor. Kapatıp yeniden açmak gerekiyor.
- Tekrar: `ezber/t9_sync.js` (GitHub API `page.route` ile taklit edildi; uzak kayıtta yeni bir not var). Kart cevaplandıktan sonra `synow` → `sync sonrası W.q: null X: review` → `rvok` → `PAGEERROR TypeError: Cannot read properties of null (reading 'shift')`.
- Kök neden: `sync()` 8367: birleşme bir şey değiştirdiyse koşulsuz `W.q=null` yapıyor; açık `review` sayfası `W.q`'yu kullanmaya devam ediyor (`rvAdvance` 6666, `ACT.rvok` 6843, `pReview` 6578 `q.length`). Tetikleyiciler: `visibilitychange` (8426), 2 dk aralık (8425), `online`.
- Düzeltme: `if(!(X&&X.kind==='review'))W.q=null; else W.stale=1;` ve review kapanınca/bitince `W.stale` ise kuyruğu yeniden kur; ya da `rvAdvance`/`pReview` başında `if(!W.q)buildQueue();`.

## [ÖNEM: orta] Bir cihazda "Tüm verileri sil" / "Yedek yükle" yapılırsa, öteki cihaz o arada bir şey kaydettiyse eski veriler her iki cihaza geri geliyor
- Kullanıcı ne görüyor: Telefonda bütün verileri silip temiz başlıyor. Dizüstü (açık sekme/çevrimdışı) sıfırlamadan sonra herhangi bir kayıt yaptıysa, eşitlemeden sonra eski kelimeler, ezber tabloları ve günler telefona da geri geliyor. Yedekten geri yüklemede de aynı.
- Tekrar: `ezber/t10_resetghost.js` → `phone: srs 0, ez 0, days 0` (sıfırlanmış) → `phoneAfter: srs 4, ez 1, days 1`.
- Kök neden: `mergeS` 8321-8322: uzak `rz` yalnız `R.rz > L.mt-1` ise uygulanıyor; değilse normal birleşme yapılıp `M.rz=max` ile sıfırlama "tüketilmiş" sayılıyor, eski veriler korunarak buluta yazılıyor.
- Düzeltme: `R.rz>L.rz` ise her durumda `R`'yi temel al; L'den yalnız `mt>R.rz` olan değişiklikleri (zaman damgalı alanlar: srs.u, hk.u, qn/wl/notes d) taşı. En basit: `R.rz>(L.rz||0)` → `return R` ve kullanıcıya "öteki cihazda veriler sıfırlandı" uyarısı.

## [ÖNEM: orta] "Bu konuyu baştan al" öteki cihazdaki sonraki çalışmayı siliyor
- Kullanıcı ne görüyor: Telefonda Perfekt'i "baştan al"dı; dizüstünde (henüz eşitlenmemiş) Perfekt Anla+Tanı'yı yeniden geçti. Eşitlemeden sonra iki aşama da yok.
- Tekrar: `ezber/t11_mergeday.js` → `g1_after: {"m":{},"stg":{},"rv":[],"w":[],"rs":1000}` (B'nin 2000'deki anla/tani kaybolur).
- Kök neden: `mergeGx` 8307: `rs` farklıysa büyük `rs`'li nesne bütünüyle kazanıyor; diğer taraftaki `rs`'den sonraki aşama tarihleri (`stg[k]` ≥ reset günü) atılıyor.
- Düzeltme: `rs` kazanan nesneye, diğer taraftan `stg[k]`/`rv` tarihlerinden reset anından sonra olanları ekle (aşama tarihine saat yoksa `last>=resetGünü` koşuluyla).

## [ÖNEM: düşük] İki cihazın günlük konu/ezber seçimi birleşince alfabetik küçük olan kazanıyor (g10 > g2'yi ezer)
- Kullanıcı ne görüyor: Bugün başlığı gün ortasında başka bir konuya/tabloya dönebiliyor; seçilen, kullanıcının çalıştığı değil, kimliği alfabetik olarak önce gelen ("g10" < "g2", "art" < "seinhaben").
- Tekrar: `ezber/t11_mergeday.js` → `{ ezd: 'art', gt: 'g10' }` (A: seinhaben/g2, B: art/g10).
- Kök neden: `mergeDay` 8302: `(k==='ezd'||k==='gt')?(x<y?x:y)`.
- Düzeltme: günün ilk seçim zamanını sakla (`d.gtT`) ve önce seçileni koru; ya da çalışılan tablo/konu kaydı (bkz. ilk bulgu) varsa onu başlığa yaz.

## [ÖNEM: orta] Kısmi "Boş tabloyu doldur" oturmuş tabloyu sıfırlıyor ve tekrarını yarına çekiyor
- Kullanıcı ne görüyor: "Belirli artikel" %100 oturmuş, sıradaki tekrar 20 Eki. Sadece ilk satırı (3 hücre) doldurup "Kontrol et"e basınca sonuç "3 / 12", tablo **%25**'e düşüyor, tekrar **15 Eki**'ye (yarın) çekiliyor. Boş bıraktığı 9 hücre "bilmiyorum" sayıldı ama ekran bunu önceden söylemiyor (yalnız "Bilmediğin hücreyi boş bırak").
- Tekrar: `ezber/t2_ezfill.js` → `10-13 test sonrası {n:3, due:'2026-10-20', cells2:12}` → `kısmi doldurma sonrası {n:3, due:'2026-10-15', cells2:3, cells … "1-0":0 …}`.
- Kök neden: `ezFillCheck` 7427-7434: boş hücre için de `ezMark(...,false)` (seriyi 0'a çeker); `per=[ok,cells.length]` ile `ezSchedule` boşları da payda sayıp <%80 → `due=yarın`.
- Düzeltme: boş hücreleri işaretleme/paydaya katma (yalnız doldurulanları değerlendir) ya da "Kontrol et"ten önce "9 hücre boş: bilmiyorum sayılacak" uyarısı göster; tablo vadesi gelmemişse kısmi doldurma `due`'yu öne çekmesin.

## [ÖNEM: orta] "Oturdu" üç ekranda üç farklı anlamda; ezber için tanımı hiç yazmıyor
- Kullanıcı ne görüyor: Kelimeler: "oturdu = tekrar aralığı 21 günü geçti" (açıklanmış). Konular: "oturdu = 5 aşama + 2 tekrar". Ezber: "%100 oturdu / 1/12 tablo oturdu" — bir hücreyi art arda 2 kez doğru bilmek (aynı dakikada bile) ve hücrelerin %80'i; bu tanım arayüzde yok. Test sonucu "12/12 Harika" iken tablo %0 görünmesinin sebebi de bu.
- Tekrar: `ezber/t1_ezdays.js`, `ezber/t8_kalipacts.js` (kural tablosu: "6 / 6 Harika … Fiil 2. sırada %0").
- Kök neden: `ezProg` 7231 (seri≥2), `ezLi` 7435-7439, `vEzber` 7450 ("tablo oturdu"), `pEz` 7385 "hücre oturdu"; açıklama metni (`pEz` notu 7399) tanım vermiyor.
- Düzeltme: Ezber'de "oturdu" yerine "ezberlendi" ve tanımı ekrana yaz ("bir hücre iki ayrı günde doğru bilinince ezberlenmiş sayılır"); test sonucunda "%0 → bu test 12 hücrenin ilk doğrusu; yarınki testte doğru bilirsen ezberlenir" gibi açıklama.

