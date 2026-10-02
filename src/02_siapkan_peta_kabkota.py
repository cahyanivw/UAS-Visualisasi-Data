"""Menggabungkan batas kab/kota (GADM) dengan tabel BPS (kemiskinan 2022), menyederhanakan bentuk,
lalu menyimpan satu GeoJSON ringan untuk web.   Jalankan: python 02_siapkan_peta_kabkota.py"""
import pandas as pd, json, glob, re
from shapely.geometry import shape, mapping

FOLDER = "/mnt/user-data/uploads"
TOL    = 0.008          # tingkat penyederhanaan bentuk (derajat, ~900 m); makin besar makin ringan

def key(s): return re.sub(r"[^A-Z0-9]", "", str(s).upper())

def baca_bps(kata, kolom):
    d = pd.read_excel(glob.glob(f"{FOLDER}/*{kata}*")[0], header=None).iloc[3:, :2]
    d.columns = ["nama", kolom]; rows = []; prov = None
    for n, v in zip(d.nama.astype(str).str.strip(), d[kolom]):
        if n.isupper(): prov = n; continue            # baris huruf kapital = provinsi
        v = pd.to_numeric(str(v).replace(",", "."), errors="coerce")
        rows.append((prov, n, v))
    return pd.DataFrame(rows, columns=["provinsi", "nama", kolom])

bps = baca_bps("Persentase_Penduduk_Miskin__P0", "p0_persen") \
        .merge(baca_bps("Jumlah_Penduduk_Miskin", "miskin_ribu"), on=["provinsi", "nama"])
bps["key"] = bps.nama.map(key)

# nama di GADM yang berbeda penulisannya dengan BPS
ALIAS = {"Pakpak Barat": "Pakpak Bharat", "Pontianak": "Mempawah",          # kab. Pontianak (kode 6104) kini bernama Mempawah
         "Tanjung Jabung B": "Tanjung Jabung Barat", "Tanjung Jabung T": "Tanjung Jabung Timur",
         "Tarakan": "Kota Tarakan"}
g = json.load(open(f"{FOLDER}/Indonesia.json"))
fitur = []
for f in g["features"]:
    p = f["properties"]
    if p["TYPE_2"] == "Water Body" or p["NAME_2"] in ("Danau Limboto",): continue   # buang danau/waduk
    nm = p["NAME_2"]
    if p["TYPE_2"] == "Kota" and not nm.startswith("Kota "): nm = "Kota " + nm
    nm = ALIAS.get(nm, ALIAS.get(p["NAME_2"], nm)) if p["NAME_2"] != "Pontianak" or p["CC_2"] == "6104" else nm
    f["_key"] = key(nm); f["_kode"] = p["CC_2"]; fitur.append(f)

peta = {f["_key"]: f for f in fitur}
keluar, tanpa_peta = [], []
for r in bps.itertuples():
    f = peta.get(r.key)
    if f is None: tanpa_peta.append((r.provinsi, r.nama)); continue
    geom = shape(f["geometry"]).simplify(TOL, preserve_topology=True)
    if geom.is_empty: continue
    keluar.append({"type": "Feature",
        "properties": {"nama": r.nama, "provinsi": r.provinsi.title(), "kode_gadm": f["_kode"],
                       "p0_persen": r.p0_persen, "miskin_ribu": r.miskin_ribu},
        "geometry": json.loads(json.dumps(mapping(geom), separators=(",", ":")))})

def bulatkan(c):                      # 3 desimal (~110 m) cukup untuk peta nasional
    return round(c, 3) if isinstance(c, float) else [bulatkan(x) for x in c]
for f in keluar: f["geometry"]["coordinates"] = bulatkan(f["geometry"]["coordinates"])

json.dump({"type": "FeatureCollection", "features": keluar}, open("kabkota_2022.geojson", "w"), separators=(",", ":"))
pd.DataFrame(tanpa_peta, columns=["provinsi", "kab_kota"]).to_csv("kabkota_tanpa_peta.csv", index=False)
print("Tergambar:", len(keluar), "dari", len(bps), "| Tanpa batas peta:", len(tanpa_peta))
for t in tanpa_peta: print("  -", t)
