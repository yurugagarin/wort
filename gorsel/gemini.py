# Hikâye kancalarına karikatür: Gemini resim modeliyle tek resim üretir.
# Kullanım: GEMINI_API_KEY ortam değişkeni tanımlı olmalı.
#   python3 gorsel/gemini.py <cikti.png> "<ingilizce sahne tarifi>"
# Model GEMINI_IMAGE_MODEL ile değiştirilebilir; verilmezse sırayla denenir.
import base64, json, os, sys, urllib.request, urllib.error

STIL = ("Cartoon in the style of a German newspaper comic strip: hand-drawn black ink outlines, "
        "flat bright colors, funny exaggerated characters with big noses and expressive faces, simple background. "
        "Absolutely no text, no letters, no words, no logos in the image. Scene: ")
MODELLER = [m for m in [os.environ.get("GEMINI_IMAGE_MODEL"), "gemini-2.5-flash-image",
                        "gemini-2.5-flash-image-preview", "gemini-2.0-flash-preview-image-generation"] if m]

def uret(sahne, cikti):
    anahtar = os.environ.get("GEMINI_API_KEY")
    if not anahtar:
        sys.exit("GEMINI_API_KEY yok: ortam ayarlarına ekleyip yeni oturum aç.")
    govde = json.dumps({"contents": [{"parts": [{"text": STIL + sahne}]}],
                        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}).encode()
    for model in MODELLER:
        url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % model
        istek = urllib.request.Request(url, govde, {"Content-Type": "application/json", "x-goog-api-key": anahtar})
        try:
            cevap = json.load(urllib.request.urlopen(istek, timeout=180))
        except urllib.error.HTTPError as e:
            print(model, "->", e.code, e.read()[:300].decode("utf-8", "replace"))
            continue
        for aday in cevap.get("candidates", []):
            for parca in aday.get("content", {}).get("parts", []):
                veri = parca.get("inlineData") or parca.get("inline_data")
                if veri and veri.get("data"):
                    open(cikti, "wb").write(base64.b64decode(veri["data"]))
                    print(model, "-> kaydedildi:", cikti)
                    return True
        print(model, "-> resim dönmedi:", json.dumps(cevap)[:300])
    return False

if __name__ == "__main__":
    sys.exit(0 if uret(sys.argv[2], sys.argv[1]) else 1)
