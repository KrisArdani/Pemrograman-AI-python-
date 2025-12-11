import datetime

# --- DATA MENU (Daftar Harga) ---
MENU = {
    1: {"nama": "Jus kelapa", "harga": 6000},
    2: {"nama": "Es teh anget", "harga": 30000},
    3: {"nama": "Jahe susu", "harga": 25000},
    4: {"nama": "Es Dawet", "harga": 15000}
}

# --- INISIALISASI VARIABEL ---
keranjang_belanja = [] # List untuk menyimpan semua item yang dipesan
tanggal_pembelian = datetime.date.today().strftime("%d %B %Y")

# --- FUNGSI UNTUK MENGHITUNG TOTAL BELANJA ---
def hitung_total(keranjang):
    """Menghitung total harga dan total kuantitas dari keranjang belanja."""
    total_harga = sum(item['subtotal'] for item in keranjang)
    total_qty = sum(item['jumlah'] for item in keranjang)
    return total_harga, total_qty

# --- HEADER PROGRAM ---
print("YOMIE COFFE")
nama_pelanggan = input("Nama Pelanggan: ")
tanggal_input = input(f"Tanggal Pembelian (Kosongkan untuk hari ini, {tanggal_pembelian}): ")
if tanggal_input.strip() != "":
    tanggal_pembelian = tanggal_input

print(f"Nama Pelanggan   : {nama_pelanggan.capitalize()}")
print(f"Tanggal Pembelian: {tanggal_pembelian}")
print("=============================")

# --- TAMPILKAN MENU ---
print("=====MENU=====")
for no, item in MENU.items():
    harga_formatted = f"Rp.{item['harga']:,}"
    print(f"{no}. {item['nama']:<20} {harga_formatted.replace(',', '.')}")
print("==============\n")

# --- FUNGSI TAMBAH BARANG ---
def tambah_barang():
    while True:
        try:
            no_menu = int(input("Masukkan Menu Pesanan (Nomor Menu): "))
            if no_menu not in MENU:
                print("❌ Nomor menu tidak valid. Silakan masukkan nomor 1 sampai 4.")
                continue

            jumlah = int(input("Masukkan Jumlah Pembelian: "))
            if jumlah <= 0:
                print("❌ Jumlah harus lebih dari nol.")
                continue

            item_dipilih = MENU[no_menu]
            subtotal = item_dipilih["harga"] * jumlah
            
            # Tambahkan ke keranjang
            keranjang_belanja.append({
                "no_menu": no_menu,
                "nama": item_dipilih["nama"],
                "harga": item_dipilih["harga"],
                "jumlah": jumlah,
                "subtotal": subtotal
            })
            print(f"-> Berhasil Menambah {jumlah} {item_dipilih['nama']}.")
            break
            
        except ValueError:
            print("❌ Input tidak valid. Masukkan angka.")

# --- FUNGSI KURANG BARANG ---
def kurang_barang():
    if not keranjang_belanja:
        print("Keranjang kosong. Tidak ada yang bisa dikurangi.")
        return

    print("\n--- DAFTAR PESANAN SAAT INI ---")
    for i, item in enumerate(keranjang_belanja):
        print(f"[{i+1}] {item['nama']} x{item['jumlah']} (Rp.{item['subtotal']:,}.00)")
    print("--------------------------------")
    
    try:
        indeks = int(input("Masukkan Nomor Urut Pesanan yang ingin DIKURANGI/DIHAPUS (contoh: 1): ")) - 1
        
        if 0 <= indeks < len(keranjang_belanja):
            item_untuk_kurang = keranjang_belanja[indeks]
            qty_lama = item_untuk_kurang['jumlah']
            print(f"Anda memilih: {item_untuk_kurang['nama']} (Qty saat ini: {qty_lama})")
            
            qty_kurang = int(input("Masukkan jumlah yang ingin dikurangi: "))
            
            if qty_kurang <= 0 or qty_kurang > qty_lama:
                print("❌ Jumlah pengurangan tidak valid.")
                return
            
            qty_baru = qty_lama - qty_kurang
            
            if qty_baru == 0:
                # Hapus item jika kuantitas menjadi 0
                keranjang_belanja.pop(indeks)
                print(f"-> Item {item_untuk_kurang['nama']} berhasil DIHAPUS dari pesanan.")
            else:
                # Update kuantitas dan subtotal
                keranjang_belanja[indeks]['jumlah'] = qty_baru
                keranjang_belanja[indeks]['subtotal'] = qty_baru * keranjang_belanja[indeks]['harga']
                print(f"-> Kuantitas {item_untuk_kurang['nama']} diubah menjadi {qty_baru}.")
        else:
            print("❌ Nomor urut pesanan tidak valid.")

    except ValueError:
        print("❌ Input harus berupa angka.")


# --- PROSES PEMESANAN UTAMA ---
print("\n--- Mulai Memesan ---")
# Pesanan pertama harus selalu 'tambah'
tambah_barang() 

while True:
    pilihan = input("\nApakah ada yang ingin ditambahkan/dikurangi? (tambah/kurang/tidak tambah): ").lower()
    
    if pilihan == 'tambah':
        tambah_barang()
    elif pilihan == 'kurang':
        kurang_barang()
    elif pilihan == 'tidak tambah':
        break
    else:
        print("⚠️ Pilihan tidak dikenal. Masukkan 'tambah', 'kurang', atau 'tidak tambah'.")

# --- TAMPILAN AKHIR (Final Output) ---
total_pembayaran, total_pesanan_qty = hitung_total(keranjang_belanja)

print("\n=============================")
print("          REKAP PESANAN         ")
print("=============================")

if not keranjang_belanja:
    print("KERANJANG KOSONG.")
else:
    for item in keranjang_belanja:
        print(f"- {item['nama']:<20} x{item['jumlah']} (Rp.{item['subtotal']:,}.00)")

print("-----------------------------")
print(f"Total Pesanan  : {total_pesanan_qty}")
print(f"Total Pembayaran: Rp.{total_pembayaran:,.0f}".replace(',', '.'))
print("=============================")