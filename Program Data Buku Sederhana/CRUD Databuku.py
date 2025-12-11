# Nama File: program_data_buku.py

FILE_NAME = "data_buku.txt"

def show_menu():
    """Menampilkan menu utama program."""
    print("\n================================")
    print("📚 PROGRAM DATA BUKU SEDERHANA")
    print("================================")
    print("1. Masukkan Data Buku")
    print("2. Tampilkan Data Buku")
    print("3. Cari Buku")
    print("4. Edit Data Buku")
    print("5. Hapus Data Buku (Per Item)")
    print("6. Hapus Semua Data Buku")
    print("7. Keluar")
    print("================================")
    pilihan = input("Pilih Menu (1-7): ")
    return pilihan

def parse_line(line: str) -> dict:
    """Parse satu baris dari file menjadi dict {'judul','penulis','tahun'}.

    Backwards compatible: jika baris hanya berisi judul, maka penulis/tahun dikosongkan.
    """
    parts = [p.strip() for p in line.split('|')]
    if len(parts) == 1:
        return {'judul': parts[0], 'penulis': '', 'tahun': ''}
    # Jika ada lebih dari 3 bagian, gabungkan sisanya ke judul (defensive)
    if len(parts) >= 3:
        judul = parts[0]
        penulis = parts[1]
        tahun = parts[2]
    else:
        # len == 2
        judul, penulis = parts
        tahun = ''
    return {'judul': judul, 'penulis': penulis, 'tahun': tahun}


def format_line(item: dict) -> str:
    """Format dict menjadi string untuk disimpan di file: judul|penulis|tahun"""
    return f"{item.get('judul','').strip()}|{item.get('penulis','').strip()}|{item.get('tahun','').strip()}"


def get_data() -> list:
    """Baca semua data dari file, kembalikan list of dict."""
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            data = [parse_line(line.strip()) for line in f if line.strip()]
        return data
    except FileNotFoundError:
        return []


def write_all_data(data_list: list):
    """Tulis ulang seluruh daftar buku ke file (overwrite)."""
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        for item in data_list:
            f.write(format_line(item) + '\n')

def insert_data():
    """Memasukkan data buku baru."""
    while True:
        judul = input("Masukkan Judul Buku: ").strip()
        if not judul:
            print("Judul buku tidak boleh kosong.")
            continue

        penulis = input("Masukkan Nama Penulis (kosong jika tidak ada): ").strip()
        tahun = input("Masukkan Tahun Terbit (kosong jika tidak ada): ").strip()

        if tahun and not tahun.isdigit():
            print("Tahun harus berupa angka jika diisi. Batalkan input ini dan coba lagi.")
            continue

        item = {'judul': judul, 'penulis': penulis, 'tahun': tahun}
        try:
            with open(FILE_NAME, 'a', encoding='utf-8') as f:
                f.write(format_line(item) + '\n')
            print(f"Buku '{judul}' berhasil ditambahkan.")
        except Exception as e:
            print(f"Terjadi error saat menulis file: {e}")

        # Logika "Mau isi lagi?" sesuai video [00:04:42]
        isi_lagi = input("Mau isi lagi? (y/t): ").lower()
        if isi_lagi != 'y':
            break
    
    input("Tekan ENTER untuk kembali ke menu...")

def show_data():
    """Menampilkan semua data buku yang sudah tersimpan."""
    data_buku = get_data()
    print("\n================================")
    print("DATA BUKU")
    print("================================")
    
    if not data_buku:
        # Kondisi "Belum ada data buku yang masuk" [00:07:47]
        print("Belum ada data buku yang masuk.")
    else:
        # Mengurutkan data secara alfabetis berdasarkan judul
        data_buku.sort(key=lambda x: x.get('judul','').lower())
        for i, item in enumerate(data_buku, 1):
            judul = item.get('judul','')
            penulis = item.get('penulis','')
            tahun = item.get('tahun','')
            extra = ''
            if penulis and tahun:
                extra = f" — {penulis} ({tahun})"
            elif penulis:
                extra = f" — {penulis}"
            elif tahun:
                extra = f" — ({tahun})"
            print(f"{i}. {judul}{extra}")
    
    print("================================")
    input("Tekan ENTER untuk kembali ke menu...")

def search_data():
    """Mencari buku berdasarkan judul."""
    data_buku = get_data()
    if not data_buku:
        print("\nBelum ada data buku untuk dicari.")
        input("Tekan ENTER untuk kembali ke menu...")
        return
        
    search_term = input("Masukkan kata kunci pencarian (judul/penulis/tahun): ").strip().lower()
    found_items = []
    
    print("\n================================")
    print("HASIL PENCARIAN")
    print("================================")
    
    for item in data_buku:
        if (search_term in item.get('judul','').lower() or
            search_term in item.get('penulis','').lower() or
            search_term in item.get('tahun','').lower()):
            found_items.append(item)

    if found_items:
        for i, item in enumerate(found_items, 1):
            judul = item.get('judul','')
            penulis = item.get('penulis','')
            tahun = item.get('tahun','')
            extra = ''
            if penulis and tahun:
                extra = f" — {penulis} ({tahun})"
            elif penulis:
                extra = f" — {penulis}"
            elif tahun:
                extra = f" — ({tahun})"
            print(f"{i}. {judul}{extra}")
    else:
        print(f"Buku dengan kata kunci '{search_term}' tidak ditemukan.")
    
    input("Tekan ENTER untuk kembali ke menu...")

def edit_data():
    """Mengubah judul buku yang sudah ada."""
    data_buku = get_data()
    if not data_buku:
        print("\nBelum ada data buku untuk di-update.")
        input("Tekan ENTER untuk kembali ke menu...")
        return
    
    judul_lama = input("Masukkan judul buku yang ingin di-update: ").strip()
    
    try:
        index_to_edit = -1
        for i, item in enumerate(data_buku):
            if item.get('judul','') == judul_lama:
                index_to_edit = i
                break

        if index_to_edit == -1:
            print(f"Buku dengan judul '{judul_lama}' tidak ditemukan.")
            input("Tekan ENTER untuk kembali ke menu...")
            return

        current = data_buku[index_to_edit]
        print("Data saat ini:")
        print(f"Judul : {current.get('judul','')}")
        print(f"Penulis: {current.get('penulis','')}")
        print(f"Tahun : {current.get('tahun','')}")

        judul_baru = input("Masukkan judul baru (kosong = tidak diubah): ").strip()
        penulis_baru = input("Masukkan penulis baru (kosong = tidak diubah): ").strip()
        tahun_baru = input("Masukkan tahun baru (kosong = tidak diubah): ").strip()

        if tahun_baru and not tahun_baru.isdigit():
            print("Tahun harus berupa angka jika diisi. Pembatalan edit.")
            input("Tekan ENTER untuk kembali ke menu...")
            return

        if judul_baru:
            data_buku[index_to_edit]['judul'] = judul_baru
        if penulis_baru:
            data_buku[index_to_edit]['penulis'] = penulis_baru
        if tahun_baru:
            data_buku[index_to_edit]['tahun'] = tahun_baru

        write_all_data(data_buku)
        print(f"Buku '{judul_lama}' berhasil di-update.")

    except Exception as e:
        print(f"Terjadi error saat update data: {e}")
        
    input("Tekan ENTER untuk kembali ke menu...")

def delete_data():
    """Menghapus satu data buku."""
    data_buku = get_data()
    if not data_buku:
        print("\nBelum ada data buku untuk dihapus.")
        input("Tekan ENTER untuk kembali ke menu...")
        return
    
    judul_hapus = input("Masukkan judul buku yang ingin dihapus: ").strip()
    
    try:
        found_index = -1
        for i, item in enumerate(data_buku):
            if item.get('judul','') == judul_hapus:
                found_index = i
                break

        if found_index != -1:
            removed = data_buku.pop(found_index)
            write_all_data(data_buku)
            print(f"Buku '{removed.get('judul','')}' berhasil dihapus.")
        else:
            print(f"Buku dengan judul '{judul_hapus}' tidak ditemukan.")
            
    except Exception as e:
        print(f"Terjadi error saat menghapus data: {e}")
        
    input("Tekan ENTER untuk kembali ke menu...")

def delete_all():
    """Menghapus semua data buku."""
    # Konfirmasi penghapusan sesuai video [00:14:16]
    konfirmasi = input("Apakah Anda yakin akan menghapus semua data buku? (y/t): ").lower()
    if konfirmasi == 'y':
        try:
            # Buka file dalam mode 'w' (write), yang akan menimpa dan menghapus semua isi file
            with open(FILE_NAME, 'w') as f:
                f.write("")
            print("Data berhasil dihapus.")
        except Exception as e:
            print(f"Terjadi error saat menghapus semua data: {e}")
    else:
        print("Penghapusan dibatalkan.")
    
    input("Tekan ENTER untuk kembali ke menu...")


def main():
    """Fungsi utama untuk menjalankan program."""
    while True:
        pilihan = show_menu()
        
        if pilihan == '1':
            insert_data()
        elif pilihan == '2':
            show_data()
        elif pilihan == '3':
            search_data()
        elif pilihan == '4':
            edit_data()
        elif pilihan == '5':
            delete_data()
        elif pilihan == '6':
            delete_all()
        elif pilihan == '7':
            # Fungsi exit [00:15:37]
            print("Keluar dari program. Terima kasih!")
            break
        else:
            # Penanganan input salah [00:02:55]
            print("❌ Masukkan pilihan sesuai nomor menu yang tersedia (1-7).")
            input("Tekan ENTER untuk melanjutkan...")

# Panggil fungsi main agar program berjalan
if __name__ == "__main__":
    main()