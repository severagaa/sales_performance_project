import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Konfigurasi visualisasi premium
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16,
    'figure.dpi': 150
})

# Palette Warna Indonesia / Lokal yang hangat dan profesional
INDONESIA_PALETTE = ["#d62728", "#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd", "#8c564b", "#e377c2"]
PRIMARY_COLOR = "#d62728"  # Merah batik / merah bendera
SECONDARY_COLOR = "#1f77b4" # Biru laut

def format_rupiah(val, pos=None):
    """Format angka menjadi format Rupiah Indonesia yang bersih"""
    if val >= 1e9:
        return f"Rp {val*1e-9:.1f} Miliar"
    elif val >= 1e6:
        return f"Rp {val*1e-6:.1f} Juta"
    else:
        return f"Rp {val:,.0f}"

def analyze_monthly_performance(df_sales, output_dir):
    print("--- 1. Menganalisis Kinerja Penjualan Bulanan ---")
    df_sales['Date'] = pd.to_datetime(df_sales['Date'])
    df_sales['Month'] = df_sales['Date'].dt.to_period('M')
    
    # Agregasi penjualan bulanan
    monthly_sales = df_sales.groupby('Month')['TotalAmount'].sum().reset_index()
    monthly_sales['MonthStr'] = monthly_sales['Month'].astype(str)
    
    print("\nTabel Penjualan Bulanan (IDR):")
    for idx, row in monthly_sales.iterrows():
        print(f"{row['MonthStr']}: {format_rupiah(row['TotalAmount'])}")
        
    # 1. Grafik Tren Penjualan Bulanan (Line Chart dengan Marker)
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_sales['MonthStr'], monthly_sales['TotalAmount'], marker='o', color=PRIMARY_COLOR, linewidth=2.5, markersize=8)
    
    # Format sumbu Y menjadi Rupiah
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_rupiah))
    
    # Highlight bulan Ramadhan & Lebaran (Februari & Maret)
    plt.axvspan('2026-02', '2026-03', color='yellow', alpha=0.2, label='Ramadhan & Lebaran Season')
    
    # Tambahkan anotasi pada puncak penjualan
    peak_idx = monthly_sales['TotalAmount'].idxmax()
    peak_row = monthly_sales.loc[peak_idx]
    plt.annotate(
        f"Puncak Lebaran!\n{format_rupiah(peak_row['TotalAmount'])}",
        xy=(peak_row['MonthStr'], peak_row['TotalAmount']),
        xytext=(peak_row['MonthStr'], peak_row['TotalAmount'] * 0.85),
        arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=6),
        ha='center'
    )
    
    plt.title("Tren Pendapatan Bulanan Nusantara Retail Group (Jan - Jun 2026)")
    plt.xlabel("Bulan")
    plt.ylabel("Total Omset (IDR)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "monthly_sales_performance.png"), bbox_inches='tight')
    plt.close()
    print("Visualisasi 'monthly_sales_performance.png' berhasil disimpan.")

def analyze_regions_and_channels(df_sales, output_dir):
    print("\n--- 2. Menganalisis Penjualan Berdasarkan Wilayah & Saluran ---")
    
    # Agregasi Wilayah & Channel
    region_channel = df_sales.groupby(['Region', 'Channel'])['TotalAmount'].sum().unstack().fillna(0)
    region_channel['Total'] = region_channel['Online'] + region_channel['Offline']
    region_channel = region_channel.sort_values(by='Total', ascending=True) # untuk bar horizontal
    
    print("\nTabel Penjualan Wilayah (IDR):")
    print(region_channel.round(2))
    
    # 2. Grafik Kontribusi Penjualan per Wilayah (Horizontal Stacked Bar Chart)
    plt.figure(figsize=(11, 7))
    region_channel[['Offline', 'Online']].plot(kind='barh', stacked=True, color=['#7f7f7f', PRIMARY_COLOR], ax=plt.gca())
    
    ax = plt.gca()
    ax.xaxis.set_major_formatter(plt.FuncFormatter(format_rupiah))
    
    plt.title("Analisis Multi-Channel: Kontribusi Omset Offline vs Online per Wilayah")
    plt.xlabel("Total Penjualan (IDR)")
    plt.ylabel("Wilayah")
    plt.legend(title="Saluran Penjualan")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "sales_by_region_channel.png"), bbox_inches='tight')
    plt.close()
    print("Visualisasi 'sales_by_region_channel.png' berhasil disimpan.")

def analyze_payment_methods(df_sales, output_dir):
    print("\n--- 3. Menganalisis Distribusi Metode Pembayaran ---")
    
    pay_dist = df_sales.groupby('PaymentMethod').agg(
        TotalSpent=('TotalAmount', 'sum'),
        TransactionCount=('TransactionID', 'count')
    ).reset_index().sort_values(by='TotalSpent', ascending=False)
    
    print("\nTabel Penggunaan Metode Pembayaran:")
    print(pay_dist.round(2))
    
    # 3. Grafik Distribusi Metode Pembayaran (Bar Chart Horizontal)
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=pay_dist,
        x='TotalSpent',
        y='PaymentMethod',
        palette='Reds_r',
        hue='PaymentMethod',
        legend=False
    )
    
    ax = plt.gca()
    ax.xaxis.set_major_formatter(plt.FuncFormatter(format_rupiah))
    
    plt.title("Metode Pembayaran Terpopuler Berdasarkan Nilai Transaksi (IDR)")
    plt.xlabel("Total Nilai Transaksi")
    plt.ylabel("Metode Pembayaran")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "payment_method_distribution.png"), bbox_inches='tight')
    plt.close()
    print("Visualisasi 'payment_method_distribution.png' berhasil disimpan.")

def perform_rfm_segmentation(df_sales, output_dir):
    print("\n--- 4. Menganalisis Segmentasi Pelanggan (RFM Analysis) ---")
    df_sales['Date'] = pd.to_datetime(df_sales['Date'])
    
    # Batas tanggal referensi analisis (1 hari setelah tanggal terakhir di dataset)
    ref_date = df_sales['Date'].max() + pd.Timedelta(days=1)
    
    # Hitung Recency, Frequency, Monetary harian
    rfm = df_sales.groupby('CustomerID').agg({
        'Date': lambda x: (ref_date - x.max()).days, # Recency
        'TransactionID': 'count',                     # Frequency
        'TotalAmount': 'sum'                         # Monetary
    }).rename(columns={
        'Date': 'Recency',
        'TransactionID': 'Frequency',
        'TotalAmount': 'Monetary'
    })
    
    # Buat Skor RFM berdasarkan Kuantil (1-5)
    # Gunakan qcut. Jika data duplikat banyak, gunakan rank(method='first')
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]) # Recency lebih kecil lebih bagus
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    
    # Konversi tipe data skor ke integer
    rfm['R_Score'] = rfm['R_Score'].astype(int)
    rfm['F_Score'] = rfm['F_Score'].astype(int)
    rfm['M_Score'] = rfm['M_Score'].astype(int)
    
    # Klasifikasikan Segmen Pelanggan
    def define_segment(row):
        r = row['R_Score']
        f = row['F_Score']
        
        if r >= 4 and f >= 4:
            return "Champions (Loyal & Borong)"
        elif r >= 3 and f >= 3:
            return "Loyal Customers"
        elif r >= 4 and f <= 2:
            return "New / Recent Customers"
        elif r <= 2 and f >= 3:
            return "At Risk (Hampir Hilang)"
        elif r <= 2 and f <= 2:
            return "Hibernating (Hilang)"
        else:
            return "About to Sleep (Rata-rata)"
            
    rfm['Segment'] = rfm.apply(define_segment, axis=1)
    
    # Hitung statistik per segmen
    segment_stats = rfm.groupby('Segment').agg(
        Count=('Recency', 'count'),
        AvgRecency=('Recency', 'mean'),
        AvgFrequency=('Frequency', 'mean'),
        AvgMonetary=('Monetary', 'mean'),
        TotalMonetary=('Monetary', 'sum')
    ).reset_index().sort_values(by='Count', ascending=False)
    
    print("\nStatistik Segmen Pelanggan RFM:")
    print(segment_stats.round(2))
    
    # 4. Grafik Distribusi Segmen Pelanggan (Bar Chart Vertikal)
    plt.figure(figsize=(10, 6))
    bars = sns.barplot(
        data=segment_stats,
        x='Count',
        y='Segment',
        palette='RdYlGn_r',
        hue='Segment',
        legend=False
    )
    
    # Tambahkan angka di samping bar
    for p in bars.patches:
        width = p.get_width()
        plt.text(
            width + 5,
            p.get_y() + p.get_height() / 2,
            f"{int(width)} Pelanggan",
            ha='left', va='center', fontweight='bold', fontsize=9
        )
        
    plt.title("Segmentasi Pelanggan Berdasarkan Analisis RFM (Recency, Frequency, Monetary)")
    plt.xlabel("Jumlah Pelanggan")
    plt.ylabel("Segmen Pelanggan")
    plt.xlim(0, segment_stats['Count'].max() * 1.15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "rfm_customer_segments.png"), bbox_inches='tight')
    plt.close()
    print("Visualisasi 'rfm_customer_segments.png' berhasil disimpan.")
    
    # Simpan hasil rfm ke file csv untuk referensi portofolio tambahan
    rfm.to_csv(os.path.join(output_dir, "..", "data", "rfm_results.csv"))
    print("Hasil segmentasi RFM disimpan ke 'data/rfm_results.csv'.")

def main():
    base_dir = "d:/PORTOFOLIO/sales_performance_project"
    data_dir = os.path.join(base_dir, "data")
    vis_dir = os.path.join(base_dir, "visualizations")
    
    sales_file = os.path.join(data_dir, "retail_sales_transactions.csv")
    
    if not os.path.exists(sales_file):
        print("Dataset retail tidak ditemukan! Jalankan 'generate_sales_data.py' terlebih dahulu.")
        return
        
    df_sales = pd.read_csv(sales_file)
    
    analyze_monthly_performance(df_sales, vis_dir)
    analyze_regions_and_channels(df_sales, vis_dir)
    analyze_payment_methods(df_sales, vis_dir)
    perform_rfm_segmentation(df_sales, vis_dir)
    
    print("\nAnalisis Kinerja Penjualan Retail selesai.")

if __name__ == "__main__":
    main()
