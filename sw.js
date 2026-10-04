/* WORT · service worker — şimdilik yalnız kurulum (ana ekrana ekleme) için.
   Bilerek "fetch" dinleyicisi YOK: sayfa önbelleğe alınmaz, her açılışta sunucudaki
   en güncel sürüm gelir. v3'te akşam bildirimi ("kartların bekliyor") buraya eklenecek. */
self.addEventListener('install', function () { self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });
