import os

# --- 1. DATA PRODUK (MIRIP DENGAN KONSEP 'LIST' DI VIDEO) ---
# Menggunakan dictionary untuk menyimpan data produk secara terstruktur
DATA_PRODUK = {
    "PRIA": {
        1: {"nama": "Jas Formal", "harga": 650000, "ukuran": ["S", "M", "L", "XL"]},
        2: {"nama": "Kemeja Batik", "harga": 250000, "ukuran": ["S", "M", "L", "XL"]},
        3: {"nama": "Kaos Polo", "harga": 180000, "ukuran": ["M", "L", "XL"]},
        4: {"nama": "Celana Chino", "harga": 300000, "ukuran": ["28", "30", "32", "34"]},
    },
    "WANITA": {
        1: {"nama": "Dress Pesta", "harga": 750000, "ukuran": ["S", "M", "L"]},
        2: {"nama": "Blouse Kerja", "harga": 220000, "ukuran": ["S", "M", "L", "XL"]},
        3: {"nama": "Rok Plisket", "harga": 190000, "ukuran": ["S", "M", "L"]},
        4: {"nama": "Kardigan", "harga": 350000, "ukuran": ["All Size"]},
    },
}

# --- 2. FUNGSI UNTUK TAMPILAN (REPRESENTASI FUNGSI DEF) ---

def format_rupiah(angka):
    """Fungsi untuk memformat angka menjadi string Rupiah."""
    return f"Rp {angka:,.0f}".replace(",", ".")

def tampilkan_list_baju(gender):
    """Menampilkan daftar baju berdasarkan gender."""
    print("\n" + "="*50)
    print(f"|{'DAFTAR BAJU ' + gender:^48}|")
    print("="*50)
    print("| No | Nama Produk        | Harga Satuan | Ukuran Tersedia |")
    print("="*50)
    
    produk = DATA_PRODUK.get(gender)
    if produk:
        for no, item in produk.items():
            nama = item['nama'].ljust(18)
            harga = format_rupiah(item['harga']).ljust(12)
            ukuran = ", ".join(item['ukuran']).ljust(15)
            print(f"| {no:<2} | {nama} | {harga} | {ukuran} |")
    
    print("="*50)

def cetak_struk(pembeli, total_belanja, total_akhir, diskon_rp, keranjang, uang_bayar, uang_kembali):
    """Mencetak struk pembayaran seperti di demonstrasi video."""
    os.system('cls' if os.name == 'nt' else 'clear') # Membersihkan layar
    print("="*60)
    print(f"{'PROGRAM TOKO BAJU SEDERHANA':^60}")
    print("="*60)
    print(f"Nama Pembeli : {pembeli['nama']}")
    print(f"No. Telepon  : {pembeli['telepon']}")
    print("-" * 60)
    print(f"| {'Nama Baju':<20} | {'Ukuran':<7} | {'Qty':<3} | {'Harga Satuan':<12} | {'Subtotal':<12} |")
    print("-" * 60)

    for item in keranjang:
        nama = item['nama'].ljust(20)
        ukuran = item['ukuran'].ljust(7)
        qty = str(item['jumlah']).ljust(3)
        harga_satuan = format_rupiah(item['harga']).ljust(12)
        subtotal = format_rupiah(item['subtotal']).ljust(12)
        print(f"| {nama} | {ukuran} | {qty} | {harga_satuan} | {subtotal} |")

    print("-" * 60)
    print(f"{'TOTAL BELANJA':<45}: {format_rupiah(total_belanja):>12}")

    if diskon_rp > 0:
        print(f"{'SELAMAT! ANDA MENDAPATKAN DISKON 25%':<45}")
        print(f"{'DISKON':<45}: -{format_rupiah(diskon_rp):>12}")

    print(f"{'TOTAL AKHIR':<45}: {format_rupiah(total_akhir):>12}")
    print("-" * 60)
    print(f"{'UANG BAYAR':<45}: {format_rupiah(uang_bayar):>12}")
    print(f"{'KEMBALIAN':<45}: {format_rupiah(uang_kembali):>12}")
    print("=" * 60)
    print(f"{'TERIMA KASIH SUDAH BERBELANJA':^60}")
    print("=" * 60)

# --- 3. FUNGSI INTI PROGRAM (LOGIKA TRANSAKSI) ---

def mulai_transaksi():
    """Mengelola proses pembelian dari awal hingga akhir."""
    keranjang = []
    total_belanja = 0

    print("\n--- PROGRAM PENJUALAN TOKO BAJU ---")
    
    # 3.1. Input Data Pembeli
    try:
        nama = input("Masukkan Nama Lengkap Anda: ")
        telepon = input("Masukkan Nomor Telepon: ")
        
        while True:
            gender = input("Pilih Jenis Kelamin (Pria/Wanita): ").strip().upper()
            if gender in ["PRIA", "WANITA"]:
                break
            else:
                print("Pilihan tidak valid. Harap masukkan 'Pria' atau 'Wanita'.")
        
        pembeli = {"nama": nama, "telepon": telepon, "gender": gender}

    except Exception:
        print("Input tidak valid. Membatalkan transaksi.")
        return

    # 3.2. Proses Pembelian (Perulangan/Looping)
    counter = 1
    maks_beli = 10 # Batasan maksimal pembelian, sesuai demo
    
    while counter <= maks_beli:
        tampilkan_list_baju(pembeli['gender'])
        
        print(f"\nPembelian ke-{counter} (Maks. {maks_beli} item)")

        # 3.2.1. Pilih Produk (Percabangan If/Else)
        while True:
            try:
                pilihan_no = int(input("Masukkan No. Baju yang dipilih (atau 0 untuk selesai): "))
                if pilihan_no == 0:
                    break
                
                produk_pilihan = DATA_PRODUK[pembeli['gender']].get(pilihan_no)
                if produk_pilihan:
                    break
                else:
                    print("Nomor baju tidak ditemukan. Coba lagi.")
                    
            except ValueError:
                print("Input harus berupa angka. Coba lagi.")
        
        if pilihan_no == 0:
            if not keranjang:
                print("Transaksi dibatalkan. Keranjang kosong.")
                return
            else:
                break # Keluar dari perulangan pembelian

        # 3.2.2. Pilih Ukuran
        list_ukuran = produk_pilihan['ukuran']
        while True:
            print(f"Ukuran tersedia: {', '.join(list_ukuran)}")
            ukuran = input(f"Masukkan ukuran ({'/'.join(list_ukuran)}): ").strip().upper()
            if ukuran in list_ukuran:
                break
            else:
                print(f"Ukuran '{ukuran}' tidak tersedia untuk produk ini.")
        
        # 3.2.3. Input Jumlah Beli
        while True:
            try:
                jumlah_beli = int(input("Masukkan Jumlah Beli: "))
                if jumlah_beli > 0:
                    break
                else:
                    print("Jumlah harus lebih dari 0.")
            except ValueError:
                print("Input harus berupa angka.")

        # 3.2.4. Hitung Subtotal dan Simpan ke Keranjang
        harga_satuan = produk_pilihan['harga']
        subtotal = harga_satuan * jumlah_beli
        total_belanja += subtotal
        
        keranjang.append({
            "nama": produk_pilihan['nama'],
            "ukuran": ukuran,
            "harga": harga_satuan,
            "jumlah": jumlah_beli,
            "subtotal": subtotal
        })

        counter += 1
        
        # 3.2.5. Tanya Belanja Lagi (Perulangan Lanjutan)
        if counter <= maks_beli:
            while True:
                lanjut = input("Apakah Anda ingin belanja lagi? (ya/tidak): ").strip().lower()
                if lanjut == 'tidak':
                    break # Keluar dari perulangan pembelian (break)
                elif lanjut == 'ya':
                    break # Lanjut ke iterasi berikutnya
                else:
                    print("Pilihan tidak valid. Masukkan 'ya' atau 'tidak'.")
            
            if lanjut == 'tidak':
                break # Break dari perulangan utama

    # 3.3. Perhitungan Diskon dan Total Akhir (Percabangan If/Else)
    DISKON_MIN_TOTAL = 500000
    DISKON_PERSEN = 0.25
    diskon_rp = 0
    total_akhir = total_belanja

    if total_belanja >= DISKON_MIN_TOTAL: # Kondisi diskon seperti di [00:13:03]
        diskon_rp = int(total_belanja * DISKON_PERSEN)
        total_akhir = total_belanja - diskon_rp
        print("\nSELAMAT! Anda mendapatkan Diskon 25%!")
    
    print("-" * 40)
    print(f"Total Belanja Anda: {format_rupiah(total_belanja)}")
    if diskon_rp > 0:
        print(f"Diskon (25%): -{format_rupiah(diskon_rp)}")
    print(f"TOTAL YANG HARUS DIBAYAR: {format_rupiah(total_akhir)}")
    print("-" * 40)

    # 3.4. Proses Pembayaran
    while True:
        try:
            uang_bayar = int(input("Masukkan Uang Pembayaran: "))
            if uang_bayar >= total_akhir:
                uang_kembali = uang_bayar - total_akhir
                break
            else:
                print(f"Uang pembayaran kurang. Kurang {format_rupiah(total_akhir - uang_bayar)}.")
        except ValueError:
            print("Input harus berupa angka.")

    # 3.5. Pencetakan Struk
    cetak_struk(pembeli, total_belanja, total_akhir, diskon_rp, keranjang, uang_bayar, uang_kembali)


# --- 4. FUNGSI MENU UTAMA (ENHANCEMENT/PENAMBAHAN LENGKAP) ---

def tampilkan_menu_utama():
    """Menampilkan menu lengkap aplikasi."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*40)
        print(f"{'APLIKASI TOKO BAJU PYTHON':^40}")
        print("="*40)
        print("Pilih Opsi:")
        print("1. Mulai Transaksi Baru")
        print("2. Lihat Daftar Harga Baju Pria")
        print("3. Lihat Daftar Harga Baju Wanita")
        print("4. Keluar dari Program")
        print("="*40)

        pilihan = input("Masukkan Pilihan (1-4): ").strip()

        if pilihan == '1':
            mulai_transaksi()
            input("\nTekan ENTER untuk kembali ke Menu Utama...")
        elif pilihan == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            tampilkan_list_baju("PRIA")
            input("\nTekan ENTER untuk kembali ke Menu Utama...")
        elif pilihan == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            tampilkan_list_baju("WANITA")
            input("\nTekan ENTER untuk kembali ke Menu Utama...")
        elif pilihan == '4':
            print("Terima kasih telah menggunakan program ini. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("\nTekan ENTER untuk melanjutkan...")

# --- 5. EKSEKUSI PROGRAM ---

if __name__ == "__main__":
    tampilkan_menu_utama()