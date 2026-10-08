# Denetim · KELİME sekmesi ve aralıklı tekrar (SRS)

Betikler: `scratchpad/v22/kelime/` (lib.js ortak; çalıştırma: `NODE_PATH=$(npm root -g) node <betik>.js`).
Ana çıktılar: `sim5.stdout.txt` (6 gün), `backlog.out.txt` (8 gün, "Tamam"da bırakan kullanıcı), `focus.stdout.txt`, `judge.out.json`, `judge2.out.json`.
Satır numaraları donmuş kopyaya göre: `base/index.html`.

---

## [ÖNEM: yüksek] Zor kelime çipine dokununca sayfa çöküyor: kelime kartı açılmıyor, eski ekran kalıyor
- **Kullanıcı ne yaşıyor:** Kelime sekmesindeki "Zor kelimelerin" kutusunda bir kelimeye (ör. *der Bahnhof*) dokunuyor. Ya hiçbir şey değişmiyor ve bir önceki ekran ("nett" kartı ya da "Zor kelimeler bitti") duruyor, ya da kart açılıyor ama hikâye kısmı sonsuza kadar "Hikâye yükleniyor…" diyor. Kutudaki "Dokun: kartı ve hikâyesini gör" sözü tutmuyor.
- **Tekrar üretme:** `kelime/wcard.js`. (A) Hikâye dosyası daha inmemişken ilk çip: "📖 HİKÂYE KANCASI Hikâye yükleniyor…" 1,5 sn sonra da aynı. (B) İkinci çip (*der Bahnhof*): ekranda hâlâ **nett** kartı var, sayfa hatası `Maximum call stack size exceeded`. `focus.js` içinde de aynı: zor kelimeler oturumundan sonra çipe dokununca ekranda "Zor kelimeler bitti" kalıyor.
- **Kök neden:** `pWcard` (5983) her çizimde `hkyLoad(function(){ if(X.kind==='wcard') drawPage(); })` çağırıyor. `hkyLoad` (6512) hikâyeler zaten yüklüyse geri çağırmayı **hemen** çalıştırıyor → `drawPage` → `pWcard` → `hkyLoad` → … sonsuz özyineleme. İlk açılışta ise özyineleme `fetch().then` içinde oluyor ve `.catch` hatayı yutuyor, bu yüzden ekran "yükleniyor"da kalıyor.
- **Önerilen düzeltme:** `pWcard` içinde geri çağırmayı yalnız yükleme gerçekten bekleniyorsa ver: `if(!HKY) hkyLoad(function(){ if(X&&X.kind==='wcard') drawPage(); });`

## [ÖNEM: yüksek] "Bilmiyorum" ve yanlış cevaplar da puana sayılıyor: hiç doğru cevap vermeden 30/30 alınıyor ve seri sürüyor
- **Kullanıcı ne görüyor:** 2. gün her soruda "Bilmiyorum, göster"e (ya da yanlış şıkka) basınca Bugün sekmesi "Kelime tekrarı · Tamam · 19 kart · 30/30" diyor, seri "2 gün". Oysa **hiç doğru cevap yok** ve kuyrukta 18 kart duruyor. Normal günde de aynı sayaç şişiyor: 40 kartlık günde "Tamam · 53 kart". Buradaki "kart" aslında **cevap sayısı**. İlerleme sekmesindeki "tekrar edilen kart" da aynı sayıyı topluyor.
- **Tekrar üretme:** `kelime/focus.js` GÜN 2: `doğru cevap: 0 | bilemedim/yanlış: 18 | tanıtım: 1 | d.w 19 / d.wt 19 | toplam puan 30`, `kuyrukta kalan kart: 18`. `sim5.js` 2. gün: `d.w=27, d.wt=20`, Bugün "Tamam · 27 kart" (20 kart vardı).
- **Kök neden:** `grade()` (3277–3290) her cevapta `d.w++` yapıyor (3286): yanlış cevap, aynı kartın tekrar sorulması ve zor kelime oturumu dahil. `introDone` (3275) da sayıyor. `frac().wort = d.w/d.wt` (3341) ve `wordDone` (3349) bu sayıya bakıyor. Yanlış kart 3 kart sonra yine geldiği için (`rvAdvance` 6666), tek bir kartı sürekli bilemeyerek de hedefe ulaşılıyor.
- **Önerilen düzeltme:** Günün kart kümesini tut (`d.wd={id:1}`). Bir kart, o gün ilk kez doğru (ya da "near") cevaplandığında ya da tanıtıldığında bir kez sayılsın: `if(g>0&&!d.wd[id]){d.wd[id]=1;d.w=(d.w||0)+1;}`. Yanlış cevaplar ayrı sayaçta dursun (`d.wx`). Etiket "x / y kart" gerçekten kart sayısı olsun.

## [ÖNEM: yüksek] Bugün "0 / 25 kart" diyor, Kelime sekmesi "40 kart seni bekliyor". "Tamam" çıktığında 15–24 kart hâlâ bekliyor
- **Kullanıcı ne görüyor:** 3. günden sonra iki ekran farklı sayı veriyor: Bugün "0 / 25 kart", Kelime "30 / 32 / 40 / 47 kart seni bekliyor". 25. cevapta Bugün "Tamam · 30/30" diyor ama oturum sürüyor (ilerleme çubuğu 26/40…) ve kalan kartların "ekstra" olduğu hiçbir yerde söylenmiyor. "Tamam"da bırakan kullanıcının birikmiş işi her gün büyüyor, buna rağmen uygulama her gün 10 yeni kelime eklemeye devam ediyor.
- **Tekrar üretme:** `kelime/backlog.js` ("Tamam" görünce bırakan kullanıcı):
  `gün 3: d.wt=25 | 29 kart | kalan 6` · `gün 6: 38 kart | kalan 15` · `gün 8: d.wt=25 | 47 kart seni bekliyor | 25 cevapta "Tamam", kuyrukta kalan 24`. Vadesi gelenler 0→10→19→18→20→28→31→37 diye büyüyor.
  Gün ortasında yeniden yükleme (`sim5.js` 2. gün): Bugün "14 kart kaldı", Kelime "16 kart seni bekliyor".
- **Kök neden:** `ensureTarget` (3325–3328) hedefi `min(25, vadesi gelen + yeni)` ile sınırlıyor. `buildQueue` (5941–5948) ise vadesi gelenlerin **hepsini** ve `pickNew(newLeft())` sonucunu sınırsız kuyruğa koyuyor. Gün içinde eklenen kartlar (konu kelimeleri, kalıp, arama "+ ekle", kendi kelimen, defter) ve ayarlardan "günlük yeni kelime" değişikliği (`ACT.npd`, `W.q=null`) kuyruğu değiştiriyor ama `d.wt` sabit kalıyor (kodla doğrulandı). Yeni kelime sayısı birikmeye göre azaltılmıyor (`newLeft` 3296).
- **Önerilen düzeltme:** Tek kaynak olsun. Gün başında kuyruğu kur, `d.wt = q.length` yap (sınır gerekiyorsa kuyruğu da aynı sınırla kes), sonradan eklenen her kart için `d.wt++` yap. Birikme varsa yeni kelimeyi kıs: `newLeft = max(0, newPerDay - floor(due/10)*2)` gibi. Kelime başlığı ile Bugün aynı fonksiyondan okusun: "Bugün: 25 kart (17 tekrar + 8 yeni) · ekstra: 15".

## [ÖNEM: orta] Bugün'de bitmiş "Kelime tekrarı" satırına dokunmak sessizce 5 yeni kelime ekliyor
- **Kullanıcı ne yaşıyor:** Kelime görevi bitmiş ("Tamam · 10 kart"). Ne yaptığına bakmak için satıra dokununca bir özet görmüyor; doğrudan "11/15 · YENİ KELİME · ÖNCE TAHMİN ET" ekranı açılıyor. Kendisine sorulmadan 5 yeni kelime eklenmiş oluyor ve bu kelimeler yarının yükünü de artırıyor. Kelime sekmesinde artık "5 kart seni bekliyor" yazıyor.
- **Tekrar üretme:** `kelime/focus.js` GÜN 1: `npx (yok) → 5 | kuyruk 0 → 5`. 3. günde `act('review')` ile de aynısı oluyor (`sim5.js`: "review tekrar açılınca: 31/35 YENİ KELİME").
- **Kök neden:** `ACT.review` (6842): `if(!W.q.length) ACT.more();`. `ACT.task('wort')` doğrudan `ACT.review`'u çağırıyor.
- **Önerilen düzeltme:** Kuyruk boşsa `more` çağırma. `pReview`'in "Bugünlük tamam" ekranını (özetle birlikte, aşağıdaki tasarım bulgusuna bak) göster; yeni kelime yalnız "5 yeni kelime daha öğren" düğmesiyle eklensin.

## [ÖNEM: orta] Zor kelimeler: puana sayılıyor, günlük kuyruğu siliyor, yarıda kalınca Bugün'ün kelime görevi zor kelimeleri açıyor. Bunların hiçbiri söylenmiyor
- **Kullanıcı ne yaşıyor:** "Zor kelimeleri şimdi çalış · 4" düğmesine basıyor, 2 kart cevaplayıp çıkıyor. Kelime sekmesi artık "2 kart seni bekliyor · 2 tekrar · 0 yeni" diyor, oysa öncesinde 18 kart vardı. Bugün'deki "Kelime tekrarı"na dokununca günlük tekrar değil, kalan zor kelimeler açılıyor. Zor kelime cevapları günlük kelime puanına sayılıyor (d.w 19→21); günlük görev, zor kelimelerle doldurulabiliyor. Zor kelimeler bitince sayfa hatası çıkıyor.
- **Tekrar üretme:** `kelime/focus.js` ZOR KELİMELER bölümü: `zor kelimede 2 doğru cevap: d.w 19 → 21`; `yarıda bırakılınca Kelime başlığı: 2 kart seni bekliyor 2 tekrar · 0 yeni`; `Bugün > Kelime satırına dokununca açılan: … 3/4 … | W.hard= 1`. `kelime/misc.js`: `TypeError: Cannot read properties of null (reading 'length') at rvAdvance (6668)`.
- **Kök neden:** `ACT.hardgo` (6939) global `W`'yi zor kelime kuyruğuyla değiştiriyor. `wordsReady` (5792) ve `ACT.review` aynı `W`'yi kullanıyor. Cevaplar `rvGrade`→`grade` üzerinden `d.w++` yapıyor. Bitişte `pReview` `W.q=null` yapıyor (6580), `rvAdvance` 6668'de ise `W.q.length` okuyor.
- **Önerilen düzeltme:** Zor kelimeler için ayrı nesne kullan (`HW`) ya da `W`'yi yedekleyip bitişte geri koy. Zor kelime cevapları `d.w`'ye girmesin (ya da kutuda "günlük puana sayılır" yazsın). `rvAdvance`'te `if(W.q&&!W.q.length&&…)` kontrolü yapılsın.

## [ÖNEM: orta] Konu kelimeleri, kalıplar, defter ve arama ile eklenen kartlar tanıtılmadan aynı gün soruluyor ve "tekrar (daha önce öğrendiğin)" diye sayılıyor
- **Kullanıcı ne görüyor:** Bugün'de "Konunun 14 kelimesini kelime tekrarına ekle" diyor. Kelime sekmesi "41 kart seni bekliyor · **31 tekrar (daha önce öğrendiğin, tekrar zamanı gelen)** · 10 yeni" gösteriyor; 21'i hiç görülmemiş kart. Bu kartlar yeni kelime kartı (tanıtım, hikâye) gösterilmeden doğrudan "Almancası hangisi? gitmek (araçla)" diye soruluyor. Oysa aynı sekmede "ilk soru **yarın** gelir" yazıyor. Bugün'deki hedef değişmiyor (0/20).
- **Tekrar üretme:** `kelime/focus.js` GÜN 3: `eklemelerden sonra d.wt: 20 → 20`, Kelime "41 kart … 31 tekrar"; kart türleri `t:g1:* tr2de`, `k:* tr2de`, `m:2 tr2de`, ilk soru aynı gün.
- **Kök neden:** `gwadd` (6924), `ACT.kadd` (7209), `addcard` (6865), `awsave` (6969), `ncard` (7204) kartı `S.srs[id]={…,d:t}` ile hemen vadeli ve `nw` işaretsiz oluşturuyor. `rvType` (6399) `S.srs` kaydı olan kartı tanıtmıyor. `vKelimeler` (5952) "yeni"yi yalnız `!S.srs[id]` diye sayıyor. Ayrıca `nw` olmadığı için `grade` bu kartlarda `fsInit` (S=0,5) kullanıyor; tanıtılan kelimelerde başlangıç kararlılığı FSRS'in ilk değeri (1,18–3,17).
- **Önerilen düzeltme:** Eklenen kartları `S.srs`'e değil "bekleyen yeniler" listesine koy; tanıtım (`intro`) akışından geçsinler ve `introDone` ile ertesi güne vadelensinler. Ya da en azından `{d:addD(t,1),nw:1}` ile oluştur ve `d.wt`'yi güncelle.

## [ÖNEM: orta] Konu kelimelerinin yarısı havuzda zaten var: aynı kelime iki ayrı kart; Eşleştir'de doğru eşleşme yanlış sayılıyor
- **Kullanıcı ne görüyor:** "gehen", "essen", "trinken" hem havuzdan hem konudan ayrı kart olarak geliyor, aynı gün iki kez soruluyor ve sayaçları şişiriyor. Eşleştir'de sol sütunda iki "gehen", sağda "gitmek" ve "gitmek (yürüyerek)" var. Kullanıcı ilk "gehen"i "gitmek"le eşleştirince kırmızı yanıyor ve "ilk denemede doğru" sayısından düşüyor.
- **Tekrar üretme:** `kelime/dup.js`: `t: kart 379 | havuzda aynısı olan: 187`. Eşleştir: `aynı görünen eşleşmeyi seçince: {"bad":"r1","miss":{"0":1}}`, ekran "gehen essen trinken gehen essen | yemek yemek gitmek (yürüyerek) içmek gitmek yemek".
- **Kök neden:** `gwadd` (6924) havuzdaki aynı kelimeyi (`PK[deText]`) kontrol etmiyor. `matchRound` (5981) Almanca/Türkçe metne göre tekilleştirmiyor ve doğruluğu metne değil indekse göre ölçüyor (`mpick` 6941).
- **Önerilen düzeltme:** `gwadd`'da `PK[(a?a+' ':'')+w]` varsa `t:` yerine `p:` kimliğini ekle (zaten destede ise atla). `matchRound`'da `de` ve `tr` tekil olsun. `mpick` doğruluğu `P[sel].tr===P[i].tr` ile ölçsün.

## [ÖNEM: orta] Yazma sorusunda eş anlamlı ve "sich"siz cevap "Yanlış" sayılıyor ve kelimeyi "zor kelime"ye itiyor
- **Kullanıcı ne görüyor:** "Almancasını yaz: ödemek" sorusuna *bezahlen* yazıyor: "Yanlış · birazdan yine sorulacak · Doğrusu: zahlen". Kartta hangi eş anlamlının istendiğine dair hiçbir ipucu yok. Aynı şey *açmak* (öffnen/aufmachen), *başlamak* (beginnen/anfangen), *dinlenmek* (sich erholen/sich ausruhen) için de geçerli. Toplam **73** Türkçe anlam birden fazla Almanca karta karşılık geliyor. "dinlenmek"e *erholen* yazınca da "Yanlış" çıkıyor; 126 sich'li fiilde sich unutulunca bu "neredeyse" değil, tam yanlış sayılıyor. Her biri `lp`'yi artırıyor, yani kelimeyi "zor kelimeler"e itiyor.
- **Tekrar üretme:** `kelime/ui_judge.js`: `p:zahlen | bezahlen | "Yanlış … Doğrusu: zahlen" requeued:true lp:1`; `p:sich erholen | erholen | Yanlış`. `kelime/judge2.js`: 73 belirsiz anlam listesi (`judge2.out.json`), `sich fiilleri sich yazmadan: {"no":126}`.
- **Kök neden:** `rvJudge` (6429–6446) yalnız kartın kendi kelimesine bakıyor. `pReview` yazma sorusunda yalnız `c.tr`'yi gösteriyor (6632).
- **Önerilen düzeltme:** `rvJudge`'da `v`, `trSame(tr)` olan başka bir havuz kelimesine eşitse `{r:'near', m:'Bu da doğru; bu kartta istenen: *zahlen*'}` dön, `lp` artmasın. `sich` eksikse `near` + "sich'i unutma" mesajı ver. Belirsiz kartlarda soruya ipucu ekle (ilk harf ya da "z…").

## [ÖNEM: orta] Bazı konu kelimesi kartları yazarak çözülemiyor ya da yanlış anlam soruyor
- **Kullanıcı ne görüyor:**
  - "Almancasını yaz" sorusunda cevap *nicht nur …, sondern auch …*, *dieser / diese / dieses*, *der/die/das + Adjektiv*, *um … zu*, *zum + isim*, *je … desto*. Kullanıcı doğal biçimde (*nicht nur sondern auch*, *um zu*) yazınca "Yanlış" alıyor (23 kart). "…" ve "/" klavyede zor, "+ Adjektiv" gibi açıklama kelimesi de cevabın parçası gibi isteniyor.
  - Modal fiil kartları (Präteritum konusu): soru "-ebildi / zorundaydı / istedi" diyor ama istenen cevap *können / müssen / wollen*. Doğru Türkçe karşılık olan *konnte* yazılınca "Yanlış".
  - *das Datum*, *der Frau*, *der Kinder* kartlarında artikel kelimenin içinde ama soru "· artikeliyle" demiyor; *Datum* yazınca "Yanlış".
- **Tekrar üretme:** `kelime/judge2.js` ("NO" satırları, `t:g2` örnekleri), `kelime/tcards.js`.
- **Kök neden:** `card()` `t:` dalı (3188–3189) GW verisini olduğu gibi kullanıyor. `rvType` (6402) `isPhrase` kartlarını hep `write` sorusuna gönderiyor. `norm` (6221) "…", "/", "+" karakterlerini silmiyor.
- **Önerilen düzeltme:** Cevabında "…", "/" ya da "+" olan konu kartlarında yalnız seçmeli soru (`tr2de`) kullan, ya da `norm`'da bu karakterleri ve "isim/Adjektiv" yer tutucularını sil. `t:g2` için `tr`'yi mastara göre yaz ("-ebilmek" vb.) ya da `rvRight` olarak `f`'yi (konnte) iste. `t:` kartında `w` "der|die|das " ile başlıyorsa artikeli `a`'ya taşı.

## [ÖNEM: orta] Defter'den eklenen "duydum" kartı anlamsız soruluyor: "Almancası hangisi? Defterimden"
- **Kullanıcı ne görüyor:** Defter'de "Bunu duydum / gördüm" notunu kelime tekrarına ekliyor. Ertesi soru "KENDİ · DEFTER · Almancası hangisi? **Defterimden**" oluyor. Şıklar *neulich, vorgestern, gern* ve tek uzun cümle *Ich habe heute leider keine Zeit.*: doğru cevap düşünmeden bulunuyor. Sonraki aşamada "Almancasını yaz: Defterimden" sorusuna cevap verilemez.
- **Tekrar üretme:** `kelime/focus.js` GÜN 3: `m:2 tr2de :: … Almancası hangisi? Defterimden neulich vorgestern Ich habe heute leider keine Zeit. gern`.
- **Kök neden:** `ACT.ncard` (7203): `tr: … ||'Defterimden'`. `rvOpts` (6421–6427) cümle kartı için çeldiricileri havuzdaki tek kelimelerden seçiyor.
- **Önerilen düzeltme:** Karta çevirirken Türkçe anlamı zorunlu yap (boşsa sor). Cümle kartlarında (`/\s/.test(c.w)`) çeldiricileri diğer cümle kartlarından (KL, mine) seç.

## [ÖNEM: orta] Gece yarısını geçen oturum: kartlar ertesi güne yazılıyor, yeni günün hedefi düşük hesaplanıp hemen "Tamam" veriyor
- **Kullanıcı ne yaşıyor:** 23:58'de tekrara başlıyor, 00:02'de bitiriyor. Önceki gün 3/10 kalıyor (9 puan). Yeni gün, 6 kart beklemesine rağmen "Tamam · 7 kart 30/30" gösteriyor. Oturum sonu ekranı "Bugünlük tamam!" diyor; Kelime sekmesi ise "6 kart seni bekliyor".
- **Tekrar üretme:** `kelime/misc.js` (2): `d8:{w:3,wt:10}`, `d9:{w:7,np:7}` (wt yok), sonra Bugün "Tamam · 7 kart 30/30", Kelime "6 kart seni bekliyor 3 tekrar · 3 yeni".
- **Kök neden:** `pReview`/`rvok` gün değişimini (`W.day!==today()`) kontrol etmiyor. `introDone` (3272) `ensureTarget` çağırmadığı için yeni günün `d.wt`'si tanıtımlardan sonra, kalan kartlara göre hesaplanıyor (`d.w` > `d.wt`).
- **Önerilen düzeltme:** `introDone` başında `ensureTarget()` çağır. `rvok`/`rvnext`'te `if(W.day!==today()){buildQueue();toast('Yeni gün başladı');}` kontrolü yap. İsteğe bağlı: gece 03:00'e kadarki cevapları önceki güne yaz.

## [ÖNEM: orta] "Bunu zaten biliyorum · 30 gün sorma" aslında 16 gün sonra soruyor
- **Kullanıcı ne görüyor:** Düğme "30 gün sorma" diyor, kelime 16 gün sonra geri geliyor.
- **Tekrar üretme:** `kelime/focus.js` GÜN 1: `"Bunu zaten biliyorum · 30 gün sorma" → sonraki tekrar 2026-10-24 (aralık 16 gün)`.
- **Kök neden:** `ACT.rvknown` (6844) `grade(id,3)` çağırıyor; `fsNext` G=4'te S=FW[3]=15,69 veriyor, `fsIvl` sonucu 16 gün. Etiket eski SM-2 kuralından kalmış (`next()` 3245–3251 artık kullanılmıyor).
- **Önerilen düzeltme:** Etiketi "yaklaşık 2 hafta sorma" yap ya da `rvknown`'da `s.d=addD(t,30); s.i=30; s.fs=30` ayarla.

## [ÖNEM: orta] Hikâye kancası A1 kelimelerinin %97'sinde yok; hikâye dosyası geç gelirse "Hikâye yükleniyor…" yazısı kalıyor
- **Kullanıcı ne görüyor:** Kelime sekmesi "kartı ve hikâye kancasını görürsün" diyor. Yeni kelimeler önce A1'den geldiği için (`pickNew` seviyeye göre sıralıyor), ilk ~50 gün neredeyse her yeni kelimede "Bu kelimenin hazır hikâyesi henüz yok" çıkıyor. Yavaş bağlantıda kutu "Hikâye yükleniyor…"da kalıyor ve yükleme bitince de yenilenmiyor.
- **Tekrar üretme:** `kelime/storycov.js`: `A1: 545 kelimenin 18'inde hikâye`, A2 805/805, B1 973/973. `kelime/story.js`: 2,5 sn gecikmede `4000 ms sonra: Hikâye yükleniyor…`.
- **Kök neden:** `hikaye.json` içeriği. `pReview` (6588) `hkyLoad()`'u geri çağırma olmadan çağırıyor; `storyBox` (6522) yükleme bitince yeniden çizilmiyor.
- **Önerilen düzeltme:** A1 hikâyelerini tamamla ya da metni "hikâye varsa" diye yumuşat. 6588'de `hkyLoad(function(){ if(X&&X.kind==='review') drawPage(); })` kullan (önce `pWcard` döngüsünü düzelt).

## [ÖNEM: orta] Perfekt sorusu düzensiz fiillerde hiç gelmiyor (fahren, essen, sehen, sprechen, lesen, schlafen…)
- **Kullanıcı ne yaşıyor:** Perfekt kartı yalnız düzenli fiillerde çıkıyor. Ezberlenmesi en çok gereken 94 güçlü ya da düzensiz fiil hiç "Perfekt: yardımcı fiil + Partizip" diye sorulmuyor.
- **Tekrar üretme:** `kelime/judge.js`: `perf sorulmayan fiiller: 94 ["braten | brät · hat gebraten","fahren | fährt · ist gefahren","essen | isst · hat gegessen", …]`.
- **Kök neden:** `rvType` 6407: `/^(hat|ist) \S/.test(c.f)`. Bu fiillerde `f` "fährt · ist gefahren" biçiminde. `rvRight` (6647) ve `rvJudge` perf dalı da `c.f`'nin tamamını bekliyor.
- **Önerilen düzeltme:** `var pf=(c.f||'').match(/(hat|ist) [^·]+$/)` ile Perfekt kısmını ayır. `rvType`, `rvRight` ve `rvJudge` bu parçayı kullansın.

## [ÖNEM: düşük] "Artikel yanlış" kırmızı gösteriliyor ama kart geçmiş sayılıyor; büyük harf hiç denetlenmiyor
- **Kullanıcı ne görüyor:** *die Schlüssel* yazınca kırmızı "Artikel yanlış" çıkıyor, ama kart bugün tekrar gelmiyor ve 3 gün sonraya atılıyor. Artikelsiz yazmakla ("Neredeyse · doğru sayıldı") aynı işlem görüyor; ekranda bunun söylendiği bir yer yok. *der schluessel* (küçük harf) ise uyarısız "Richtig!" sayılıyor; isimlerin büyük harfle yazıldığı hiç hatırlatılmıyor.
- **Tekrar üretme:** `kelime/ui_judge.js`: `die Schlüssel → "Artikel yanlış…" requeued:false sonraki:2026-10-11`; `Schlüssel → "Neredeyse · doğru sayıldı" sonraki:2026-10-11`; `der schluessel → "Richtig!"`.
- **Kök neden:** `rvGrade` (6654): `res==='art'` için g=1 ve `W.cur.ok=true`. `rvFb` (6571–6575) başlığı ne olacağını söylemiyor. `norm` (6221) küçük harfe çeviriyor.
- **Önerilen düzeltme:** Yanlış artikel → kart 3 kart sonra yeniden sorulsun ya da başlık "Artikel yanlış · kelime doğru sayıldı, yarın yine sorulacak" olsun. İsim küçük harfle yazılmışsa `near` + "İsimler büyük harfle yazılır" mesajı ver.

## [ÖNEM: düşük] Konu kelimesi seçmeli sorularında şıklar farklı türden: cevap düşünmeden bulunuyor
- **Kullanıcı ne görüyor:** "Almancası hangisi? gitmek (araçla)" → şıklar *vielleicht, fahren, wer, demnächst*. Tek fiil doğru cevap.
- **Tekrar üretme:** `kelime/focus.js` GÜN 3: `t:g1:1 tr2de :: … vielleicht fahren wer demnächst`.
- **Kök neden:** `card()` `t:` kartlarına `p:'x'` veriyor, `rvOpts` (6422) çeldiricileri havuzdaki `p==='x'` (zarf/bağlaç) kelimelerden alıyor.
- **Önerilen düzeltme:** `t:` kartlarında çeldiricileri aynı konunun GW listesinden ya da havuzdaki aynı türden kelimeden (fiil→fiil) seç.

## [ÖNEM: düşük] Terim ve etiket tutarsızlıkları
- "öğreniliyor ›" düğmesi "**Öğrenilen** kelimeler" başlıklı listeyi açıyor (`pWlist` 5974); kullanıcı bunları "öğrenmişim" diye okuyabilir.
- Konu cümlesi (gs), kalıp (k) ve defter cümleleri "kelime" sayaçlarına ve "Kelime havuzu" dışındaki "tekrarı gelen" sayısına giriyor; liste satırında hangisinin ne olduğu yazmıyor.
- Tekrar bittiğinde "Tekrarı gelen" listesi "Bu listede **henüz** kelime yok" diyor; doğrusu "Bugün tekrar edilecek kelime kalmadı".
- Bitiş ekranı "27 cevap verdin" diyor, Bugün "Tamam · 27 kart", İlerleme "tekrar edilen kart": aynı sayı üç ayrı adla gösteriliyor ve hiçbiri kart sayısı değil (`sim5.js`).

## [ÖNEM: düşük] Oyun sonuçları: Eşleştir hiçbir yere kaydedilmiyor; Lücke ve Satzbau yalnız Rapor'a gidiyor ve kelime takvimine etki etmiyor
- **Kullanıcı ne görüyor:** Kutuda "Puana girmez, serbest pratik" yazıyor, bu doğru ve açık. Ama oyun sonu ekranları ("15 / 15", "10 / 10") sonucun nereye gittiğini söylemiyor. Lücke'de yanlış yapılan kelime tekrar takviminde öne alınmıyor. Eşleştir'in en iyi sonucu da tutulmuyor.
- **Tekrar üretme:** `kelime/focus.js` OYUNLAR: `S.al önce {"w":[31,31]}` → `sonra {"w":[31,31],"lk":[10,10],"sz":[8,8]}` (Eşleştir yok), `gün kaydı değişti mi: HAYIR`.
- **Kök neden:** `ACT.mpick` (6941) hiçbir şey kaydetmiyor. `ACT.upick`/`szCheck` yalnız `logAns` çağırıyor.
- **Önerilen düzeltme:** Sonuç ekranına "Puana ve tekrar takvimine girmez; yanlışlar Rapor'a eklendi" satırı ekle. İstenirse Lücke'deki yanlış kelimenin vadesini bugüne çek.

## [ÖNEM: orta · TASARIM] "Bugün ne yaptım, neyi yanlış yaptım, yarın ne var?" sorularının cevabı uygulamada yok
- **Kullanıcı ne yaşıyor:** Oturum sonu ekranında yalnız "Bugünlük tamam! 27 cevap verdin. Yarın tekrar zamanı gelenler burada olacak." yazıyor. Şunları görebileceği hiçbir ekran yok:
  - bugün **kaç farklı kart** çalıştığı (sayaç cevap sayısı),
  - bugün **hangi yeni kelimeleri** öğrendiği (liste yok),
  - bugün **hangilerini yanlış** yaptığı (yalnız Claude'a gidecek "Rapor önizlemesi" ham metninde ve 2+ kez unutulan "zor kelimeler"de var),
  - **yarın kaç kart** geleceği ("yarın" sözü yalnız "ilk soru yarın gelir" cümlesinde geçiyor),
  - bir cevaptan sonra kelimenin **ne zaman** tekrar geleceği (`ivl()` 3270 yazılmış ama hiç kullanılmıyor; aralık yalnız zor kelime kartında "sıradaki tekrar: 9 Eki" olarak görünüyor).

  Takvimdeki gün hücrelerine dokunulamıyor, yani geçmiş bir günde ne yapıldığı da görülemiyor.
- **Tekrar üretme:** `sim5.js` bitiş ekranları ve Kelime başlıkları. Kodda "yarın N kart" üreten bir yer yok (`grep yarın`).
- **Önerilen düzeltme:**
  - Bitiş ekranına özet ekle: "Bugün 32 kart · 10 yeni (liste) · 6 yanlış (liste, dokununca kart) · Yarın 14 kart, sonraki 7 günde 58".
  - Kelime sekmesi başlığına "Yarın: 14 kart" satırı ekle.
  - Cevap geri bildiriminde "Sonraki tekrar: 3 gün sonra" göster (`ivl(s.i)`).
  - Günlük kayda `d.wn` (yeni kimlikler) ve `d.wx` (yanlış kimlikler) dizileri ekle; İlerleme takviminde güne dokununca bu dizileri göster.

---

## Doğrulanan ve sorunsuz olanlar
- Yeni kelime tanıtıldığı gün sorulmuyor: 6 günlük simülasyonda aynı gün tanıtılıp sorulan kart çıkmadı (`sim5.js`).
- Gün içinde `d.wt` değişmiyor. Gece yarısı istisnası yukarıda.
- Yanlış kart 3 kart sonra yeniden geliyor; oturum kapanırsa kart bugün vadeli kalıyor ve yeniden açılınca kuyrukta. Seçmeli soruda cevap görüldüğü için kullanıcı döngüde takılmıyor; ancak tekrar sayısında sınır yok ve her tekrar puana sayılıyor (yukarıda).
- Yazılı cevap denetimi 2812 kartta sağlam:
  - write, cloze, plural ve perf türlerinde tam doğru cevap hiç yanlış sayılmıyor.
  - ae/oe/ue/ss, küçük harf ve "Der/Die/Das" kabul ediliyor.
  - Artikelsiz yazım "neredeyse" sayılıyor; tek harf hatası "neredeyse" sayılıyor (`judge.js`).
- Konu cümlesi (gs) kartları doğru sırayla kurulunca "Richtig" veriyor. Kalıp, defter ve konu kelimesi kartları çözülebiliyor (`focus.js`).
- "tekrarı gelen / öğreniliyor / oturdu" sayaçları açılan listelerin uzunluğuyla 8 gün boyunca aynı (`backlog.js`).
- Hep doğru cevapta aralıklar 1 → 3 → 9 → 25 gün: 4. başarılı tekrarda "oturdu". Sekmedeki "genelde 4-5 başarılı tekrar" açıklamasıyla uyumlu (`fsrs.js`).
- "5 yeni kelime daha öğren" puanı bozmuyor (hedef sabit, puan en fazla 30); yalnız yarının yükünü artırıyor.
