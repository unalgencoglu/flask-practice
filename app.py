from flask import Flask, request, redirect, url_for, jsonify, render_template

app = Flask(__name__)
print(">>> DOSYA:", __file__)

URUNLER = [
    {"id": 1, "ad": "Klavye", "fiyat": 450, "kategori": "aksesuar"},
    {"id": 2, "ad": "Monitör", "fiyat": 3200, "kategori": "ekran"},
    {"id": 3, "ad": "Mouse", "fiyat": 280, "kategori": "aksesuar"},
    {"id": 4, "ad": "Kulaklık", "fiyat": 890, "kategori": "aksesuar"},
]

@app.route("/")
def anasayfa():
    return render_template("index.html", baslik="Ürün Paneli", urunler=URUNLER)

@app.route("/hakkinda")
def hakkinda():
    return "Bu bir Flask denemesi"

@app.route("/iletisim")
def iletisim():
    return "<ul> <li>Telefon numarası ...</li> <li>Eposta ....</li> </ul>"

@app.route("/toplam")
def toplam():
    a = 5
    b = 3
    top = a + b
    return f"{a} + {b} = {top}"

@app.route("/kullanici/<isim>")
def kullanici(isim):
    return f"<h2>Profil: {isim}</h2>"

@app.route("/kare/<int:sayi>")
def kare(sayi):
    return f"{sayi}'nin karesi: {sayi ** 2}"

@app.route("/selam/<isim>")
def selam(isim): 
    return f"<h1>{isim.replace('i', 'İ').upper()}</h1>"

@app.route("/bolme/<int:a>/<int:b>")
def bolme(a, b):
    if b == 0:
        return "payda 0 olamaz"
    
    sonuc = a / b
    return f"{a} / {b} = {sonuc}"

@app.route("/kayit", methods=["GET", "POST"])
def kayit():
    if request.method == "POST":
        ad = request.form.get("ad")
        return f"<h2>Kayıt alındı: {ad}</h2>"
    
    return """
        <form method="POST">
            <input type="text" name="ad" placeholder="Adınız">
            <button type="submit">Gönder</button>
        </form>
    """

@app.route("/hesap",methods=["GET", "POST"])
def hesap():
    if request.method == "POST":
        sayi1 = int(request.form.get("sayi1"))
        sayi2 = int(request.form.get("sayi2"))
        sonuc = sayi1 + sayi2
        return redirect(url_for("sonuc", deger=sonuc))
    
    return """
        <form method="POST">
            <input type="number" name="sayi1" placeholder="Toplanacak ilk sayıyı giriniz">
            <input type="number" name="sayi2" placeholder="Toplanacak ikinci sayıyı giriniz">
            <button type="submit">Hesapla</button>
        </form>
    """
    
@app.route("/sonuc/<int:deger>")
def sonuc(deger):
    return f"<h2>Sonuç: {deger}</h2>"

@app.route("/api/kullanici")
def api_kullanici():
    return jsonify({"ad": "Ali", "Yaş": 25})

@app.route("/api/ara")
def ara():
    kelime = request.args.get("q")
    limit = request.args.get("limit", 10, type=int)
    return jsonify({"aranan": kelime, "limit": limit})

@app.route("/api/urunler")
def api_urunler():
    kategori = request.args.get("kategori")
    max_fiyat = request.args.get("max", type=int)
    
    sonuc = URUNLER
    if kategori:
        sonuc = [u for u in sonuc if u["kategori"] == kategori]
    if max_fiyat:
        sonuc = [u for u in sonuc if u["fiyat"] <= max_fiyat]
        
    return jsonify({"adet": len(sonuc), "urunler": sonuc})

@app.route("/api/urun/<int:id>")
def urun(id):
    for u in URUNLER:
        if u["id"] == id:
            return jsonify(u)
    
    return jsonify({"hata": "Ürün bulunamadı"}), 404

@app.route("/api/ozet")
def ozet():
    fiyatlar = [u["fiyat"] for u in URUNLER]
    urun_adedi = len(fiyatlar)
    ortalama_fiyat = round(sum(fiyatlar) / len(fiyatlar), 2)
    
    return jsonify({"toplam_urun": urun_adedi, "ortalama_fiyat": ortalama_fiyat})

@app.route("/panel")
def panel():    
    return render_template("panel-js.html", baslik="Ürün Paneli", urunler=URUNLER)

if __name__ == "__main__":
    app.run(debug=True)