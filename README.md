# flask-practice

Flask öğrenme sürecinde yazılmış alıştırma projesi. Temel rota tanımlamadan başlayıp JSON API, `fetch` ile asenkron veri çekme ve Jinja2 şablonlarına kadar ilerleyen bir çalışma.

## Kurulum

```bash
git clone <repo-url>
cd flask-practice

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

pip install flask
python app.py
```

Uygulama `http://127.0.0.1:5000` adresinde çalışır.

## Proje yapısı

```
flask-practice/
├── app.py                 # Tüm rotalar ve iş mantığı
├── templates/
│   ├── base.html          # Ortak iskelet (nav, head, bloklar)
│   ├── index.html         # Ürün listesi — sunucu tarafı render
│   ├── panel-js.html      # Ürün listesi — fetch ile istemci tarafı
│   └── ozet.html          # İstatistik sayfası
└── static/
    └── js.js              # fetch ile API çağıran fonksiyonlar
```

## Rotalar

### Sayfalar (HTML)

| Rota | Açıklama |
|---|---|
| `/` | Ürün listesi, Jinja2 döngüsü ile sunucuda üretilir |
| `/panel-js` | Aynı liste, `fetch` ile istemcide doldurulur |
| `/ozet` | Toplam ürün sayısı ve ortalama fiyat |

### API (JSON)

| Rota | Açıklama |
|---|---|
| `/api/urunler` | Tüm ürünler. `?kategori=` ve `?max=` ile filtrelenebilir |
| `/api/urun/<id>` | Tek ürün. Bulunamazsa 404 döner |
| `/api/ozet` | Özet istatistikler |
| `/api/ara` | `?q=` ve `?limit=` parametrelerini yansıtan örnek uç nokta |

### Alıştırma rotaları

`/hakkinda`, `/iletisim`, `/toplam`, `/kullanici/<isim>`, `/kare/<int:sayi>`, `/selam/<isim>`, `/bolme/<int:a>/<int:b>`, `/kayit`, `/hesap`, `/sonuc/<int:deger>`

## Kapsanan konular

**Rotalama**
- `@app.route` ile URL–fonksiyon eşleştirmesi
- Dinamik parametreler ve `<int:>`, `<float:>` gibi tip dönüştürücüler
- Dönüştürücülerin aynı zamanda filtre görevi görmesi (eşleşmeyen istek 404 alır)

**HTTP**
- GET / POST ayrımı, `request.form` ve `request.args`
- Durum kodları: 404 (adres yok), 405 (metod yanlış), 500 (kod çöktü)
- Post/Redirect/Get deseni — form tekrar gönderimini önlemek için
- Stateless mimari: sunucunun istekler arası hiçbir şey hatırlamaması

**JSON API**
- `jsonify` ile veri döndürme
- Sorgu parametreleriyle zincirleme filtreleme
- `return jsonify(...), 404` ile durum kodu belirtme

**JavaScript entegrasyonu**
- `fetch` + `async` / `await`
- `map` ve `join` ile diziden HTML üretme
- Sunucu tarafı render ile API + fetch yaklaşımlarının karşılaştırılması

**Jinja2**
- `{{ }}` çıktı, `{% %}` kontrol akışı
- Döngüler, koşullar, filtreler (`|length`, `|upper`)
- `{% extends %}` / `{% block %}` ile şablon kalıtımı
- Otomatik kaçış (XSS koruması)

## Süreçte karşılaşılan hatalar

Bu bölüm, çalışma sırasında gerçekten karşılaşılan ve teşhisi zaman alan durumları not eder.

**String / sayı karışması**
`request.form.get()` her zaman string döndürür. `"5" + "3"` çökmez, `"53"` verir. Hata fırlatmadığı için fark edilmesi zor. Dönüşüm veri sisteme girer girmez yapılmalı.

**`ERR_CACHE_MISS`**
POST sonucu sayfasında sert yenileme yapmak istek gövdesini boşaltır, `request.form` boş gelir. PRG deseni bu sorunu tamamen ortadan kaldırır.

**Sessiz `undefined`**
Python değişken adı JSON'a geçmez; JavaScript yalnızca sözlüğün anahtarını görür. Anahtar uyuşmazlığında JS hata vermez, `undefined` döner. Aynı şey Jinja'da boş çıktı olarak görünür.

**`len()` metod değildir**
`liste.len()` yerine `len(liste)`. `len`, `sum`, `int`, `round` yerleşik fonksiyonlardır; `.upper()` gibi metodlarla karıştırılmamalı.

**`type=int` hata fırlatmaz**
`request.args.get("max", type=int)` dönüşüm başarısız olursa varsayılana düşer. Geçersiz girdi 400 üretmez, sessizce filtresiz sonuç döner.

**Falsy değerler**
Python'da `""`, `0`, `[]` hepsi `False` sayılır. `if max_fiyat` yazarsan `max=0` filtresi sessizce yok sayılır; `is not None` kullanmak gerekir.

## Sonraki adımlar

- `try` / `except` ile hata yönetimi ve özel hata sayfaları
- `fetch` ile POST isteği gönderme
- Blueprint ile rotaları modüllere bölme
- Veritabanı entegrasyonu

## Notlar

`debug=True` yalnızca geliştirme içindir. Ayrıca reloader sadece Python dosyalarını izler — statik dosya ve şablon değişikliklerinde tarayıcıyı sert yenilemek (`Ctrl+Shift+R`) gerekebilir.
