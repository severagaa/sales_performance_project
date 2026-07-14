import os
import csv
import random
from datetime import datetime, timedelta

def create_directory_structure():
    base_dir = "d:/PORTOFOLIO/sales_performance_project"
    dirs = [
        os.path.join(base_dir, "data"),
        os.path.join(base_dir, "scripts"),
        os.path.join(base_dir, "visualizations")
    ]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"Created directory: {d}")
    return base_dir

def generate_retail_data(base_dir):
    random.seed(42)
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 6, 30)
    delta = end_date - start_date
    days = delta.days + 1

    # Daftar Produk & Kategori
    products = {
        "Groceries": [
            ("Minyak Goreng 2L", 38000),
            ("Kopi Susu Aren 1L", 65000),
            ("Susu UHT Cokelat 1L", 18500),
            ("Indomie Goreng 1 Dus", 115000),
            ("Sirup Cocopandan", 22000),
            ("Beras Premium 5kg", 74000)
        ],
        "Electronics": [
            ("Blender Miyako", 280000),
            ("Kipas Angin Cosmos", 320000),
            ("Rice Cooker Yong Ma", 650000),
            ("Air Fryer Philips", 1200000),
            ("Smart TV Xiaomi 32\"", 1990000)
        ],
        "Fashion": [
            ("Kaos Polos Cotton", 85000),
            ("Kemeja Batik Pria", 180000),
            ("Gamis Muslimah Premium", 350000),
            ("Celana Chino Slimfit", 195000),
            ("Hijab Voal Square", 45000)
        ],
        "Home Living": [
            ("Sprei Microfiber King", 145000),
            ("Wajan Teflon Anti Lengket", 185000),
            ("Rak Sepatu Minimalis", 125000),
            ("Bantal Kepala Serat Silikon", 60000)
        ]
    }

    regions = ["Jabodetabek", "Jawa Barat", "Jawa Timur", "Jawa Tengah", "Sumatera", "Sulawesi", "Kalimantan"]
    region_weights = [0.45, 0.18, 0.12, 0.08, 0.08, 0.05, 0.04] # Jabodetabek paling tinggi
    
    payment_methods = ["GoPay", "OVO", "ShopeePay", "Transfer BCA", "Credit Card", "Cash"]
    
    # Generate 1000 Customer Profiles
    customers = []
    genders = ["Male", "Female"]
    age_groups = ["18-24", "25-34", "35-44", "45+"]
    
    cust_file_path = os.path.join(base_dir, "data", "customer_data.csv")
    with open(cust_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["CustomerID", "Gender", "AgeGroup", "JoinDate"])
        
        for c_id in range(1, 1001):
            cust_id = f"CUST-{c_id:04d}"
            gender = random.choice(genders)
            age = random.choices(age_groups, weights=[0.25, 0.45, 0.20, 0.10])[0] # 25-34 paling banyak
            join_offset = random.randint(0, 500)
            join_date = (start_date - timedelta(days=join_offset)).strftime("%Y-%m-%d")
            
            # Kita assign loyalitas bawaan agar clustering RFM terlihat rapi
            # 1: Champions, 2: Loyal, 3: Normal/At Risk, 4: Hibernating
            loyalty_class = random.choices([1, 2, 3, 4], weights=[0.10, 0.20, 0.50, 0.20])[0]
            
            customers.append({
                "id": cust_id,
                "loyalty": loyalty_class
            })
            writer.writerow([cust_id, gender, age, join_date])
            
    print(f"Customer profile data generated successfully: {cust_file_path}")

    # Generate Transactions
    tx_file_path = os.path.join(base_dir, "data", "retail_sales_transactions.csv")
    
    tx_counter = 10001
    
    with open(tx_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "TransactionID", "Date", "CustomerID", "ProductCategory", 
            "ProductName", "Quantity", "UnitPrice", "Discount", 
            "TotalAmount", "PaymentMethod", "Region", "Channel"
        ])
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            date_str = current_date.strftime("%Y-%m-%d")
            
            # Pola Ramadhan & Lebaran (18 Feb - 25 Maret 2026)
            is_ramadhan_lebaran = (
                (current_date.month == 2 and current_date.day >= 15) or
                (current_date.month == 3 and current_date.day <= 25)
            )
            
            # Tentukan jumlah transaksi hari ini
            if is_ramadhan_lebaran:
                # Spike 2.5x transaksi saat Lebaran season
                base_transactions = random.randint(60, 100)
            else:
                base_transactions = random.randint(25, 45)
                
            for _ in range(base_transactions):
                tx_id = f"TX-{tx_counter}"
                tx_counter += 1
                
                # Pilih customer berdasarkan class loyalitasnya
                # Pelanggan kelas 1 (Champions) & 2 (Loyal) lebih sering belanja
                active_customers = [c for c in customers if c["loyalty"] in [1, 2]]
                all_customers = customers
                
                # Tentukan customer untuk transaksi ini
                if random.random() < 0.40:
                    cust = random.choice(active_customers)
                else:
                    cust = random.choice(all_customers)
                
                cust_id = cust["id"]
                loyalty = cust["loyalty"]
                
                # Pilih Kategori & Produk
                # Saat Lebaran, Groceries (sirup, beras) dan Fashion (baju baru) naik drastis
                if is_ramadhan_lebaran:
                    category = random.choices(
                        ["Groceries", "Fashion", "Electronics", "Home Living"],
                        weights=[0.50, 0.35, 0.08, 0.07]
                    )[0]
                else:
                    category = random.choices(
                        ["Groceries", "Fashion", "Electronics", "Home Living"],
                        weights=[0.35, 0.25, 0.20, 0.20]
                    )[0]
                    
                prod_name, unit_price = random.choice(products[category])
                
                # Quantity
                # Champions beli lebih banyak
                if loyalty == 1:
                    qty = random.randint(2, 5)
                else:
                    qty = random.randint(1, 3)
                
                # Tambahan sirup & indomie saat lebaran biasanya dibeli karton/banyak
                if is_ramadhan_lebaran and prod_name in ["Sirup Cocopandan", "Indomie Goreng 1 Dus"]:
                    qty += random.randint(1, 3)
                    
                # Diskon
                discount = 0
                if is_ramadhan_lebaran:
                    # Promo Lebaran diskon lebih besar
                    if random.random() < 0.60:
                        discount = random.choice([5000, 10000, 15000, 20000])
                else:
                    if random.random() < 0.25:
                        discount = random.choice([2000, 5000, 10000])
                
                # Pastikan diskon tidak melebihi harga total
                subtotal = qty * unit_price
                discount = min(discount, int(subtotal * 0.3)) # maks diskon 30%
                
                total_amount = subtotal - discount
                
                # Region
                region = random.choices(regions, weights=region_weights)[0]
                
                # Channel & Payment Method
                # Online vs Offline
                channel = random.choices(["Online", "Offline"], weights=[0.40, 0.60])[0]
                
                if channel == "Online":
                    # E-wallet & BCA transfer dominan di Online
                    pay_method = random.choices(
                        ["GoPay", "OVO", "ShopeePay", "Transfer BCA", "Credit Card"],
                        weights=[0.35, 0.20, 0.25, 0.15, 0.05]
                    )[0]
                else:
                    # Cash & E-wallet qr dominan di Offline
                    pay_method = random.choices(
                        ["Cash", "GoPay", "OVO", "Transfer BCA", "Credit Card"],
                        weights=[0.50, 0.20, 0.10, 0.15, 0.05]
                    )[0]
                    
                writer.writerow([
                    tx_id, date_str, cust_id, category, 
                    prod_name, qty, unit_price, discount, 
                    total_amount, pay_method, region, channel
                ])
                
    print(f"Retail transactions generated successfully: {tx_file_path}")

if __name__ == "__main__":
    base_path = create_directory_structure()
    generate_retail_data(base_path)
    print("All fake retail data generation complete.")
