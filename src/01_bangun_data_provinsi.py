"""Menggabungkan semua tabel BPS tingkat provinsi (2022) menjadi satu tabel 34 provinsi.
Jalankan:  python 01_bangun_data_provinsi.py   (ubah FOLDER sesuai lokasi file)"""
import pandas as pd, numpy as np, glob, re

FOLDER = "/mnt/user-data/uploads"          # <- ganti: folder tempat semua file xlsx

def cari(kata):                              # cari file berdasarkan potongan nama
    hasil = [f for f in glob.glob(f"{FOLDER}/*{kata}*.xlsx")]
    assert len(hasil) == 1, f"'{kata}' cocok dengan {len(hasil)} file"
    return hasil[0]

def norm(s):                                 # samakan penulisan nama provinsi
    s = str(s).strip().upper()
    s = re.sub(r"^\d+\.\s*", "", s)
    s = s.replace("KEP. ", "KEPULAUAN ").replace("D I YOGYAKARTA", "DI YOGYAKARTA")
    return s

def angka(x):
    if isinstance(x, str):
        x = x.strip().replace(",", ".")
        if x in ("-", ""): return np.nan
    return pd.to_numeric(x, errors="coerce")

def dua_kolom(kata, kol=1):                  # tabel format: nama | nilai 2022
    d = pd.read_excel(cari(kata), header=None)
    d = d.iloc[3:, [0, kol]].copy()
    d.columns = ["prov", "nilai"]
    d["prov"] = d["prov"].map(norm)
    d["nilai"] = d["nilai"].map(angka)
    return d.dropna(subset=["nilai"]).drop_duplicates("prov").set_index("prov")["nilai"]

# --- kerangka: 34 provinsi dari matriks migrasi + migrasi neto hasil kodemu
neto = pd.read_csv(cari_csv := glob.glob(f"{FOLDER}/*migrasi_neto*.csv")[0], index_col=0)["migrasi_neto"]
neto.index = [norm(i) for i in neto.index]
df = pd.DataFrame(index=neto.index); df.index.name = "provinsi"
df["migrasi_neto"] = neto

# --- tabel dua kolom
df["miskin_p0"]     = dua_kolom("Persentase_Penduduk_Miskin__P0")   # baris provinsi ada di tabel kab/kota
df["rata_lama_sek"] = dua_kolom("Rata-Rata_Lama_Sekolah")
df["uhh"]           = dua_kolom("Umur_Harapan_Hidup_Saat_Lahir")
df["pengeluaran"]   = dua_kolom("Pengeluaran_per_Kapita")
df["sanitasi"]      = dua_kolom("Sanitasi_Layak")
df["air_minum"]     = dua_kolom("Air_Minum_Layak")
df["ipm"]           = dua_kolom("Indeks_Pembangunan_Manusia")

# --- Gini: kolom Perkotaan+Perdesaan, Semester 1 (Maret) = kolom ke-7
g = pd.read_excel(cari("Gini_Ratio"), header=None).iloc[5:, [0, 7]]
g.columns = ["prov", "v"]; g["prov"] = g["prov"].map(norm); g["v"] = g["v"].map(angka)
df["gini_maret"] = g.dropna().drop_duplicates("prov").set_index("prov")["v"]

# --- TPT dan TPAK (Agustus)
t = pd.read_excel(cari("Tingkat_Pengangguran"), header=0)
t["prov"] = t.iloc[:, 0].map(norm)
t = t.drop_duplicates("prov").set_index("prov")
df["tpt_agustus"]  = t.iloc[:, 2].map(angka)
df["tpak_agustus"] = t.iloc[:, 4].map(angka)

# --- penduduk dan kepadatan
p = pd.read_excel(cari("Penduduk__Laju"), header=0)
p["prov"] = p.iloc[:, 0].map(norm); p = p.drop_duplicates("prov").set_index("prov")
df["penduduk_ribu"]   = p.iloc[:, 1].map(angka)
df["kepadatan"]       = p.iloc[:, 4].map(angka)

# IPM tabel ini memakai batas 38 provinsi: nilai Papua & Papua Barat bukan batas lama (34 provinsi) -> dikosongkan
df.loc[["PAPUA", "PAPUA BARAT"], "ipm"] = np.nan

df["neto_per_1000"] = df["migrasi_neto"] / df["penduduk_ribu"]     # migrasi neto per 1.000 penduduk
df["ln_kepadatan"]  = np.log(df["kepadatan"])

df.to_csv("data_provinsi_2022.csv")
print(df.shape); print(df.isna().sum()[lambda s: s > 0])
print(df.describe().T[["count", "min", "max"]].round(2).to_string())
