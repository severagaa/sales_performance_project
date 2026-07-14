# Portfolio Project: Nusantara Retail Sales & Customer Analytics

Proyek ini adalah analisis transaksional bisnis retail multi-channel di Indonesia bernama **Nusantara Retail Group (NRG)**. Fokus utama proyek ini adalah mengidentifikasi performa penjualan regional, menganalisis perilaku belanja musiman (Lebaran Seasonality), mengevaluasi popularitas metode pembayaran e-wallet, dan melakukan segmentasi pelanggan menggunakan analisis **RFM (Recency, Frequency, Monetary)** untuk menyusun strategi pemasaran terarah.

---

## 📌 1. Ringkasan Eksekutif (Executive Summary)
Nusantara Retail Group (NRG) merupakan perusahaan retail yang beroperasi di 7 wilayah Indonesia dengan 4 kategori produk utama: *Groceries*, *Electronics*, *Fashion*, dan *Home Living*. Untuk menyusun strategi pemasaran dan perencanaan inventaris di semester kedua 2026, tim Data Analyst mengaudit data transaksi dari Januari - Juni 2026.

**Hasil Utama Analisis:**
1. **Pola Musiman Belanja**: Terjadi lonjakan penjualan signifikan pada bulan **Februari dan Maret 2026** (Ramadhan dan menjelang Lebaran), diikuti penurunan tajam di bulan April (efek setelah lebaran/post-holiday slump).
2. **Preferensi Pembayaran**: E-wallet (GoPay, OVO, ShopeePay) memegang porsi sangat besar dalam total volume transaksi, menunjukkan penetrasi digital payment yang sukses di Indonesia.
3. **Analisis Pelanggan RFM**: Mayoritas pendapatan disokong oleh segmen kecil pelanggan loyal (*Champions*). Namun, terdapat **25.5% pelanggan hilang (*Hibernating*)** dan **14.1% pelanggan terancam hilang (*At Risk*)** yang membutuhkan tindakan penyelamatan segera.

---

## 📁 2. Struktur Proyek
```text
sales_performance_project/
│
├── data/
│   ├── customer_data.csv               # Data profil demografis pelanggan
│   ├── retail_sales_transactions.csv   # Data transaksi penjualan rupiah
│   └── rfm_results.csv                 # Output hasil segmentasi RFM
│
├── scripts/
│   ├── generate_sales_data.py          # Skrip pembuat data transaksional
│   └── analyze_sales.py                # Skrip pengolahan data dan analisis RFM
│
├── visualizations/
│   ├── monthly_sales_performance.png   # Grafik tren pendapatan bulanan
│   ├── sales_by_region_channel.png     # Grafik kontribusi daerah & channel
│   ├── payment_method_distribution.png # Grafik metode pembayaran terpopuler
│   ├── rfm_customer_segments.png       # Grafik klasifikasi segmen pelanggan
│   └── portfolio_banner.png            # Cover visual portofolio proyek
│
└── README.md                           # Dokumentasi ini
```

---

## 📈 3. Visualisasi Hasil & Analisis Grafik

### A. Tren Penjualan Bulanan
Grafik ini melacak total omset penjualan bulanan dari Januari hingga Juni 2026.

* **Analisis**:
  * Penjualan melonjak tajam mulai Februari (**Rp 745,8 Juta**) dan memuncak di Maret (**Rp 913,3 Juta**). Hal ini bertepatan dengan musim belanja Ramadhan dan Lebaran di Indonesia.
  * Bulan April mengalami penurunan drastis ke **Rp 621,4 Juta** karena siklus konsumsi yang menurun pasca-Hari Raya.

---

### B. Kontribusi Wilayah & Saluran Penjualan (Offline vs Online)
Grafik ini membandingkan total penjualan di 7 wilayah operasional, dipecah berdasarkan saluran pembelian.

* **Analisis**:
  * **Jabodetabek** adalah kontributor utama pendapatan dengan total omset mencapai **Rp 1,87 Miliar**, diikuti Jawa Barat (**Rp 837 Juta**) dan Jawa Timur (**Rp 529 Juta**).
  * Penjualan toko fisik (*Offline*) mendominasi di seluruh wilayah (~55% - 60%), namun wilayah Jawa Barat dan Jabodetabek memiliki adopsi belanja *Online* yang cukup tinggi (~40%).

---

### C. Metode Pembayaran Terpopuler
Grafik horizontal ini menunjukkan distribusi nilai transaksi berdasarkan metode pembayaran yang digunakan pelanggan.

* **Analisis**:
  * Metode pembayaran **Cash** masih memimpin dengan total **Rp 1,31 Miliar**, karena tingginya transaksi belanja offline di supermarket.
  * Namun, **GoPay** berada di posisi kedua dengan kontribusi luar biasa sebesar **Rp 1,15 Miliar**, disusul **Transfer BCA** (Rp 604 Juta) dan **OVO** (Rp 592 Juta). Ini menandakan integrasi pembayaran non-tunai (Qris/E-wallet) sangat diterima oleh pelanggan Nusantara Retail Group.

---

### D. Segmentasi Pelanggan RFM
Pelanggan diklasifikasikan menggunakan kuantil dari nilai Recency (R), Frequency (F), dan Monetary (M).

* **Analisis**:
  * **Hibernating (255 pelanggan)**: Segmen terbesar. Mereka adalah pelanggan yang sudah lama tidak belanja dan frekuensinya sedikit. Perlu dianalisis apakah ada kendala layanan atau kompetitor baru.
  * **Champions (246 pelanggan)**: Kontributor finansial terbesar bagi perusahaan. Mereka baru saja belanja, sangat sering belanja, dan berbelanja dalam jumlah besar.
  * **At Risk (141 pelanggan)**: Pelanggan yang dulu sering belanja banyak, namun sudah cukup lama tidak kembali. Ini adalah target utama kampanye re-aktivasi.

---

## 📝 4. Kesimpulan & Rekomendasi Bisnis
Berdasarkan hasil temuan analisis di atas, berikut adalah rekomendasi taktis bagi Nusantara Retail Group:

1. **Strategi Stok Musiman Lebaran**: Tim logistik dan pengadaan harus mempersiapkan peningkatan stok barang (khususnya kategori *Groceries* dan *Fashion*) sebesar 1.5x lebih awal (mulai awal Januari) guna menghindari kekosongan stok (*out-of-stock*) saat puncak belanja Ramadhan di bulan Februari/Maret.
2. **Kampanye Re-Engagement Segment "At Risk"**: Lakukan promosi khusus melalui email marketing atau push notification dengan voucher "We Miss You" berupa potongan harga 20% untuk menarik kembali 141 pelanggan di segmen *At Risk* sebelum mereka beralih ke kompetitor.
3. **Kemitraan Strategis Gopay/OVO**: Karena GoPay dan OVO merupakan metode pembayaran digital terpopuler, jalankan program *exclusive cashback* bersama GoTo/OVO di akhir pekan untuk meningkatkan volume transaksi di aplikasi online.
4. **Ekspansi Digital Regional**: Meskipun toko offline mendominasi wilayah luar Jawa (Kalimantan, Sulawesi), terdapat potensi pasar online yang belum tergarap optimal. Lakukan promosi digital tertarget di daerah-daerah tersebut dengan menawarkan subsidi ongkos kirim (ongkir).
