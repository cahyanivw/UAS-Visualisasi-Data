"""PCA + klaster (multivariat) dan graf migrasi (jaringan + aliran) -> JSON untuk web.
Jalankan setelah 01_bangun_data_provinsi.py:  python 03_analisis.py"""
import pandas as pd, numpy as np, json, re, glob, os
import networkx as nx
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from sklearn.metrics import silhouette_score

FOLDER = "/mnt/user-data/uploads"
OUT = "web_data"; os.makedirs(OUT, exist_ok=True)
df = pd.read_csv("data_provinsi_2022.csv", index_col=0)

PULAU = {  # kelompok pulau/wilayah untuk pengurutan dan warna
 "Sumatera": ["ACEH","SUMATERA UTARA","SUMATERA BARAT","RIAU","JAMBI","SUMATERA SELATAN","BENGKULU","LAMPUNG","KEPULAUAN BANGKA BELITUNG","KEPULAUAN RIAU"],
 "Jawa": ["DKI JAKARTA","JAWA BARAT","JAWA TENGAH","DI YOGYAKARTA","JAWA TIMUR","BANTEN"],
 "Bali & Nusa Tenggara": ["BALI","NUSA TENGGARA BARAT","NUSA TENGGARA TIMUR"],
 "Kalimantan": ["KALIMANTAN BARAT","KALIMANTAN TENGAH","KALIMANTAN SELATAN","KALIMANTAN TIMUR","KALIMANTAN UTARA"],
 "Sulawesi": ["SULAWESI UTARA","SULAWESI TENGAH","SULAWESI SELATAN","SULAWESI TENGGARA","GORONTALO","SULAWESI BARAT"],
 "Maluku & Papua": ["MALUKU","MALUKU UTARA","PAPUA BARAT","PAPUA"]}
pulau = {p: k for k, v in PULAU.items() for p in v}
assert set(pulau) == set(df.index), set(df.index) ^ set(pulau)
df["pulau"] = df.index.map(pulau)

# ---------------- 1) MULTIVARIAT: PCA + klaster ----------------
VAR = ["miskin_p0","tpt_agustus","tpak_agustus","rata_lama_sek","uhh","pengeluaran",
       "sanitasi","air_minum","gini_maret","ln_kepadatan","neto_per_1000"]
X = df[VAR].values.astype(float)
Z = (X - X.mean(0)) / X.std(0, ddof=0)                    # z-score
U, S, Vt = np.linalg.svd(Z, full_matrices=False)
var_ratio = S**2 / (S**2).sum()
scores = U * S                                            # skor PC tiap provinsi
loadings = Vt.T * S / np.sqrt(len(Z))                     # korelasi variabel-PC
# tanda PC1 diatur agar variabel kemiskinan bernilai positif (supaya mudah dibaca)
for k in range(Vt.shape[0]):
    if loadings[VAR.index("miskin_p0"), k] < 0 and k == 0:
        scores[:, k] *= -1; loadings[:, k] *= -1

Zl = linkage(Z, "ward")
sil = {k: round(silhouette_score(Z, fcluster(Zl, k, "maxclust")), 3) for k in range(2, 7)}
best = 3     # k=2 silhouette tertinggi (0,242) tetapi hanya memisahkan Jawa+Bali+Kepri dari sisanya; k=3 hampir setara (0,207) dan lebih informatif
klaster = fcluster(Zl, best, "maxclust")
dist_pc = np.sqrt((scores[:, :3] ** 2).sum(1))             # jarak ke pusat di ruang 3 PC pertama
order = dendrogram(Zl, no_plot=True)["leaves"]             # urutan baris heatmap terklaster

prov = []
for i, p in enumerate(df.index):
    d = {"provinsi": p.title().replace("Dki","DKI").replace("Di Yog","DI Yog"), "key": p, "pulau": df.pulau[p],
         "klaster": int(klaster[i]), "pc1": round(scores[i,0],3), "pc2": round(scores[i,1],3), "pc3": round(scores[i,2],3),
         "jarak_pusat": round(dist_pc[i],3), "ipm": None if pd.isna(df.ipm[p]) else df.ipm[p]}
    for v in VAR: d[v] = round(float(df[v][p]), 4)
    d["migrasi_neto"] = int(df.migrasi_neto[p]); d["penduduk_ribu"] = float(df.penduduk_ribu[p])
    d["z"] = {v: round(float(Z[i, j]), 3) for j, v in enumerate(VAR)}
    prov.append(d)
multi = {"variabel": VAR, "varians": [round(float(x),4) for x in var_ratio],
         "loading": {v: [round(float(loadings[j,k]),3) for k in range(4)] for j, v in enumerate(VAR)},
         "k_klaster": int(best), "urutan_heatmap": [df.index[i] for i in order], "provinsi": prov}
json.dump(multi, open(f"{OUT}/multivariat.json","w"), ensure_ascii=False, separators=(",",":"))

# ---------------- 2) JARINGAN + ALIRAN dari matriks migrasi ----------------
raw = pd.read_excel(glob.glob(f"{FOLDER}/*migrasi_2022.xlsx")[0], header=None)
h = raw.index[raw.iloc[:,0].astype(str).str.strip() == "Nama Provinsi"][0]
m = raw.iloc[h+1:, :].copy(); m.columns = [str(c).strip() for c in raw.iloc[h]]; m = m.set_index("Nama Provinsi")
nama = [str(s).strip().lower() for s in m.index]; stop = [i for i,s in enumerate(nama) if s in ("total","nan")]
if stop: m = m.iloc[:stop[0]]
m.index = [re.sub(r"^\d+\.\s*","",str(s)).strip().upper() for s in m.index]
M = m.drop(columns=["Total"]).map(lambda x: pd.to_numeric(str(x).replace(",","."), errors="coerce")).fillna(0)
luar_negeri = M["Luar negeri"]; P = M.drop(columns=["Luar negeri"]); P.columns = [c.upper() for c in P.columns]
assert list(P.index) == list(P.columns)
nodes = list(P.index)
edges = [(asal, tuj, float(P.loc[tuj, asal])) for tuj in nodes for asal in nodes if asal != tuj and P.loc[tuj, asal] > 0]
G = nx.DiGraph(); G.add_nodes_from(nodes); G.add_weighted_edges_from(edges)
U_ = nx.Graph()
for a, b, w in edges:
    U_.add_edge(a, b, weight=U_[a][b]["weight"] + w if U_.has_edge(a, b) else w)
for a, b, d in U_.edges(data=True): d["jarak"] = 1.0 / d["weight"]
btw = nx.betweenness_centrality(U_, weight="jarak", normalized=True)   # jalur terpendek berbobot (jarak = 1/volume)
pr = nx.pagerank(G, weight="weight")
komunitas = nx.community.louvain_communities(U_, weight="weight", seed=42, resolution=1.0)
kom = {n: i for i, c in enumerate(sorted(komunitas, key=lambda c: -len(c))) for n in c}
masuk  = {n: sum(w for a,b,w in edges if b == n) for n in nodes}
keluar = {n: sum(w for a,b,w in edges if a == n) for n in nodes}
jml_tetangga = {n: U_.degree(n) for n in nodes}
nodes_j = [{"id": n, "nama": n.title().replace("Dki","DKI").replace("Di Yog","DI Yog"), "pulau": pulau[n],
            "masuk": masuk[n], "keluar": keluar[n], "neto": masuk[n]-keluar[n],
            "derajat": jml_tetangga[n], "betweenness": round(btw[n],4), "pagerank": round(pr[n],4),
            "komunitas": kom[n], "dari_luar_negeri": float(luar_negeri[n])} for n in nodes]
json.dump({"nodes": nodes_j, "edges": [{"asal":a,"tujuan":b,"jumlah":w} for a,b,w in edges],
           "urutan_pulau": [n for k in PULAU for n in PULAU[k]]},
          open(f"{OUT}/jaringan.json","w"), ensure_ascii=False, separators=(",",":"))

# ---------------- ringkasan untuk dibaca manusia ----------------
print("PCA varians:", [f"{v*100:.1f}%" for v in var_ratio[:4]], "| kumulatif 3 PC:", f"{var_ratio[:3].sum()*100:.1f}%")
print("\nLoading PC1-PC3:"); print(pd.DataFrame({k:[multi['loading'][v][i] for v in VAR] for i,k in enumerate(['PC1','PC2','PC3'])}, index=VAR).to_string())
print("\nSilhouette per k:", sil, "| dipakai k =", best)
for k in sorted(set(klaster)): print(k, [df.index[i].title() for i in range(len(df)) if klaster[i]==k])
print("\nPencilan (jarak PC1-3 terbesar):", [(df.index[i].title(), round(dist_pc[i],2)) for i in np.argsort(-dist_pc)[:5]])
print("\nJaringan: node", G.number_of_nodes(), "edge", G.number_of_edges(), "| kepadatan", round(nx.density(G),3))
t = pd.DataFrame(nodes_j).set_index("nama")
print("Top betweenness:", t.betweenness.nlargest(5).round(3).to_dict())
print("Top masuk:", t.masuk.nlargest(5).to_dict()); print("Top keluar:", t.keluar.nlargest(5).to_dict())
for c in sorted(set(kom.values())): print("Komunitas", c, [n.title() for n in nodes if kom[n]==c])
