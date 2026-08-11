async function ozetGetir() {
    const yanit = await fetch("/api/ozet");
    const veri = await yanit.json();
    console.log(veri.ortalama_fiyat);
}