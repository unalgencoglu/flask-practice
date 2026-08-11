async function urunleriGetir() {
    const kategori = document.getElementById("kategoriKutusu").value;
    const yanit = await fetch("/api/urunler?kategori=" + kategori);
    const veri = await yanit.json();
        
    const satirlar = veri.urunler.map(u => "<li>" + u.ad + " - " + u.fiyat + " TL</li>");
    document.getElementById("cikti").innerHTML = "<ul>" + satirlar.join("") + "</ul>";
}