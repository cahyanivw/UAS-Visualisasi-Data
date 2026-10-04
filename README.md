# Webstory Visualisasi Data BPS 2022

## Ke mana orang pindah, dan siapa yang tertinggal?

Webstory interaktif ini menyajikan eksplorasi data **Badan Pusat Statistik (BPS) tahun 2022** untuk melihat pola migrasi antarprovinsi serta keterkaitannya dengan kondisi sosial ekonomi wilayah di Indonesia.

Proyek ini dibuat untuk memenuhi **UAS Mata Kuliah Visualisasi Data dan Informasi**.

---

## Webstory

**Website:**  
https://cahyanivw.github.io/UAS-Visualisasi-Data/

Website dapat diakses secara publik tanpa login maupun instalasi aplikasi.

---

## Tujuan

Webstory ini bertujuan untuk:

1. Mengeksplorasi pola migrasi risen antarprovinsi di Indonesia.
2. Mengidentifikasi provinsi dengan migrasi neto masuk dan keluar yang menonjol.
3. Menganalisis struktur jaringan migrasi antarprovinsi.
4. Mengidentifikasi komunitas dalam jaringan migrasi menggunakan algoritma Louvain.
5. Membandingkan karakteristik sosial ekonomi antarprovinsi menggunakan analisis multivariat.
6. Menampilkan distribusi kemiskinan kabupaten/kota secara geospasial.

---

## Topik Visualisasi

Webstory mengintegrasikan empat topik visualisasi:

### 1. Flow / Movement

Pola perpindahan penduduk divisualisasikan menggunakan:

- Sankey diagram
- Matriks asal–tujuan (OD matrix)

Volume migrasi ditunjukkan melalui ketebalan aliran dan intensitas warna.

### 2. Network

Jaringan migrasi antarprovinsi divisualisasikan menggunakan force-directed graph.

Analisis jaringan mencakup:

- PageRank
- Betweenness centrality
- Community detection menggunakan algoritma Louvain
- Filter bobot edge
- Highlight tetangga saat node dipilih/di-hover

### 3. Geospatial

Distribusi kemiskinan divisualisasikan menggunakan:

- Choropleth map berdasarkan persentase penduduk miskin
- Proportional symbol berdasarkan jumlah penduduk miskin

Peta dilengkapi dengan tooltip, legenda, zoom, pan, dan kontrol layer.

### 4. Multivariate

Karakteristik sosial ekonomi 34 provinsi dianalisis menggunakan 11 variabel numerik.

Teknik yang digunakan meliputi:

- Principal Component Analysis (PCA)
- Hierarchical clustering
- Clustered heatmap
- Parallel coordinates
- Brushing dan linking antarvisualisasi

---

## Struktur Repository

```text
UAS-Visualisasi-Data/
│
├── data/
│   ├── raw/
│   └── clean/
│
├── docs/
│   ├── data/
│   │   └── kabkota_2022.geojson
│   └── index.html
│
├── src/
│   ├── 01_bangun_data_provinsi.py
│   ├── 02_siapkan_peta_kabkota.py
│   └── 03_analisis.py
│
├── web_data/
│
├── README.md
├── SUMBER_DATA.md
└── .gitignore
