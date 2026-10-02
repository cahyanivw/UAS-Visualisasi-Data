# Sumber Data

Seluruh data utama bersumber dari **Badan Pusat Statistik (BPS)**. Tahun data seragam: **2022**.
Tanggal akses diisi sesuai hari saat tabel diunduh.

## Tabel BPS

| No | Judul tabel | Tahun | Dipakai untuk | URL | Tanggal akses |
|----|-------------|-------|---------------|-----|---------------|
| 1 | Arus Migrasi Risen Antar Provinsi | 2022 | Aliran, jaringan, migrasi neto | https://sensus.bps.go.id/topik/tabular/sp2022/170/0/0 | 2 Oktober 2026 |
| 2 | Persentase Penduduk Miskin (P0) Menurut Kabupaten/Kota (Persen) | 2022 | Peta kab/kota; persentase miskin provinsi | https://www.bps.go.id/id/statistics-table/2/NjIxIzI=/persentase-penduduk-miskin-p0-menurut-kabupaten-kota.html | 2 Oktober 2026 |
| 3 | Jumlah Penduduk Miskin (Ribu Jiwa) Menurut Kabupaten/Kota | 2022 | Peta proportional symbol | https://www.bps.go.id/id/statistics-table/2/NjE5IzI=/jumlah-penduduk-miskin--ribu-jiwa--menurut-kabupaten-kota-.html | 2 Oktober 2026 |
| 4 | Tingkat Pengangguran Terbuka (TPT) dan Tingkat Partisipasi Angkatan Kerja (TPAK) Menurut Provinsi | 2022 | Multivariat (TPT dan TPAK, Agustus) | https://www.bps.go.id/id/statistics-table/3/V2pOVWJWcHJURGg0U2pONFJYaExhVXB0TUhacVFUMDkjMyMwMDAw/tingkat-pengangguran-terbuka--tpt--dan-tingkat-partisipasi-angkatan-kerja--tpak--menurut-provinsi.html?year=2022 | 2 Oktober 2026 |
| 5 | Rata-Rata Lama Sekolah Penduduk Umur 15 Tahun ke Atas Menurut Provinsi | 2022 | Multivariat | https://www.bps.go.id/id/statistics-table/2/MTQyOSMy/rata-rata-lama-sekolah-penduduk-umur-15-tahun-ke-atas-menurut-provinsi.html | 2 Oktober 2026 |
| 6 | [Metode Baru] Umur Harapan Hidup Saat Lahir (UHH) Hasil Long Form SP2020 (Tahun) | 2022 | Multivariat | https://www.bps.go.id/id/statistics-table/2/MjIwNiMy/-metode-baru--umur-harapan-hidup-saat-lahir--uhh--hasil-long-form-sp2020--tahun-.html | 2 Oktober 2026 |
| 7 | [Metode Baru] Pengeluaran per Kapita Disesuaikan (Ribu Rupiah/Orang/Tahun) | 2022 | Multivariat | https://www.bps.go.id/id/statistics-table/2/NDE2IzI=/-metode-baru--pengeluaran-per-kapita-disesuaikan--ribu-rupiah-orang-tahun-.html | 2 Oktober 2026 |
| 8 | Persentase Rumah Tangga menurut Provinsi dan Memiliki Akses terhadap Sanitasi Layak (Persen) | 2022 | Multivariat | https://www.bps.go.id/id/statistics-table/2/ODQ3IzI=/persentase-rumah-tangga-menurut-provinsi-dan-memiliki-akses-terhadap-sanitasi-layak--persen-.html | 2 Oktober 2026 |
| 9 | Persentase Rumah Tangga yang Memiliki Akses terhadap Sumber Air Minum Layak Menurut Provinsi (Persen) | 2022 | Multivariat | https://www.bps.go.id/id/statistics-table/2/ODQ1IzI=/persentase-rumah-tangga-yang-memiliki-akses-terhadap-sumber-air-minum-layak-menurut-provinsi--persen-.html | 2 Oktober 2026 |
| 10 | Gini Ratio Menurut Provinsi dan Daerah | 2022 | Multivariat (Maret, Perkotaan+Perdesaan) | https://www.bps.go.id/id/statistics-table/2/OTgjMg==/gini-ratio-menurut-provinsi-dan-daerah.html | 2 Oktober 2026 |
| 11 | Penduduk, Laju Pertumbuhan Penduduk, Distribusi Persentase Penduduk, Kepadatan Penduduk, Rasio Jenis Kelamin Penduduk Menurut Provinsi | 2022 | Multivariat (kepadatan); penyebut migrasi neto | https://www.bps.go.id/id/statistics-table/3/V1ZSbFRUY3lTbFpEYTNsVWNGcDZjek53YkhsNFFUMDkjMyMwMDAw/jumlah-penduduk--laju-pertumbuhan-penduduk--distribusi-persentase-penduduk--kepadatan-penduduk--rasio-jenis-kelamin-penduduk-menurut-provinsi.html?year=2022 | 2 Oktober 2026 |
| 12 | [Metode Baru] Indeks Pembangunan Manusia (IPM) menurut Provinsi (Umur Harapan Hidup Hasil Long Form SP2020) | 2022 | Warna/label saja (bukan input PCA) | https://www.bps.go.id/id/statistics-table/2/MjIwNyMy/-metode-baru--indeks-pembangunan-manusia--ipm--menurut-provinsi--umur-harapan-hidup-hasil-long-form-sp2020-.html | 2 Oktober 2026 |

## Data pendukung (non-BPS)

| Data | Sumber | Lisensi |
|------|--------|---------|
| Batas provinsi (GeoJSON) | Badan Informasi Geospasial (BIG), melalui repositori `ardian28/GeoJson-Indonesia-38-Provinsi` | MIT |
| Batas kab/kota (GeoJSON) | GADM v4.0 (gadm.org), lewat repositori `mahendrayudha/indonesia-geojson` | Cek ketentuan di gadm.org |

## Data turunan (dihitung sendiri)

- **Migrasi neto** = migrasi masuk − migrasi keluar antarprovinsi (tanpa migrasi dalam provinsi dan tanpa "Luar negeri"), dari tabel No. 1.
- **Migrasi neto per 1.000 penduduk** = migrasi neto / jumlah penduduk (ribu), penyebut dari tabel No. 11.
- **ln kepadatan** = logaritma natural kepadatan penduduk, dari tabel No. 11.

## Catatan batas wilayah

Tabel No. 2-5, 6-7, 11 memakai batas 34 provinsi (Papua dan Papua Barat belum dipecah), sama dengan matriks migrasi. Tabel No. 12 (IPM) memakai batas 38 provinsi, sehingga nilai IPM Papua dan Papua Barat dikosongkan.

## Format teks "Sumber" untuk setiap visualisasi

> Sumber: BPS (judul tabel, 2022). Diolah penulis.
