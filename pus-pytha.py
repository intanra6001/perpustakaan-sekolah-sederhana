import json

DATA_FILE = "data.json"
RIWAYAT_FILE = "riwayat.json"


try:
    with open(DATA_FILE, "r") as f:
        pass
except FileNotFoundError:
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

try:
    with open(RIWAYAT_FILE, "r") as f:
        pass
except FileNotFoundError:
    with open(RIWAYAT_FILE, "w") as f:
        json.dump([], f)


def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_riwayat():
    with open(RIWAYAT_FILE, "r") as f:
        return json.load(f)

def save_riwayat(data):
    with open(RIWAYAT_FILE, "w") as f:
        json.dump(data, f, indent=4)

def garis():
    print("-" * 50)


def tambah_buku():
    print("\n--- Tambah Buku Baru ---")
    judul = input("Judul: ")
    penulis = input("Penulis: ")
    tahun = input("Tahun: ")
    data = load_data()
    data.append({
        "judul": judul,
        "penulis": penulis,
        "tahun": tahun,
        "status": "TERSEDIA",
        "peminjam": "-"
    })
    save_data(data)
    print(f"Buku '{judul}' berhasil ditambahkan!\n")

def daftar_buku():
    data = load_data()
    if not data:
        print("\nBelum ada buku.\n")
        return
    print("\n=== DAFTAR BUKU ===")
    garis()
    for i, b in enumerate(data, start=1):
        info = f"{i}. {b['judul']} - {b['penulis']} ({b['tahun']}) | {b['status']}"
        if b['peminjam'] != "-":
            info += f" | Peminjam: {b['peminjam']}"
        print(info)
    garis()

def hapus_buku():
    data = load_data()
    daftar_buku()
    if not data: return
    try:
        pilih = int(input("Nomor buku yang dihapus: "))
        if 1 <= pilih <= len(data):
            judul = data[pilih-1]["judul"]
            del data[pilih-1]
            save_data(data)
            print(f"🗑Buku '{judul}' dihapus.\n")
        else:
            print("Nomor tidak valid.")
    except ValueError:
        print("Input harus angka.")


def pinjam_buku():
    data = load_data()
    daftar_buku()
    if not data: return
    try:
        pilih = int(input("Nomor buku yang ingin dipinjam: "))
        if 1 <= pilih <= len(data):
            buku = data[pilih-1]
            if buku["status"] == "TERSEDIA":
                nama = input("Nama peminjam: ")
                buku["status"] = "DIPINJAM"
                buku["peminjam"] = nama
                save_data(data)
                riw = load_riwayat()
                riw.append({"aksi": "Pinjam", "judul": buku["judul"], "peminjam": nama})
                save_riwayat(riw)
                print(f"Buku '{buku['judul']}' dipinjam oleh {nama}.")
            else:
                print(f"Buku sedang dipinjam oleh {buku['peminjam']}.")
    except ValueError:
        print("Input harus angka.")

def kembalikan_buku():
    data = load_data()
    daftar_buku()
    if not data: return
    try:
        pilih = int(input("Nomor buku yang dikembalikan: "))
        if 1 <= pilih <= len(data):
            buku = data[pilih-1]
            if buku["status"] == "DIPINJAM":
                nama = input("Nama peminjam: ")
                if nama.lower() == buku["peminjam"].lower():
                    buku["status"] = "TERSEDIA"
                    buku["peminjam"] = "-"
                    save_data(data)
                    riw = load_riwayat()
                    riw.append({"aksi": "Kembalikan", "judul": buku["judul"], "peminjam": nama})
                    save_riwayat(riw)
                    print(f"Buku '{buku['judul']}' telah dikembalikan.")
                else:
                    print("Nama peminjam tidak cocok.")
            else:
                print("Buku belum dipinjam.")
    except ValueError:
        print("Input harus angka.")


def cari_buku():
    data = load_data()
    kata = input("Cari judul atau penulis: ").lower()
    hasil = [b for b in data if kata in b["judul"].lower() or kata in b["penulis"].lower()]
    if hasil:
        print("\nHasil Pencarian:")
        garis()
        for b in hasil:
            print(f"{b['judul']} - {b['penulis']} ({b['tahun']}) | {b['status']}")
    else:
        print("Tidak ditemukan.")

def laporan():
    riw = load_riwayat()
    if not riw:
        print("Belum ada aktivitas.")
        return
    print("\n=== LAPORAN AKTIVITAS ===")
    garis()
    for i, r in enumerate(riw, start=1):
        print(f"{i}. {r['aksi']} - {r['judul']} oleh {r['peminjam']}")
    garis()


def menu_admin():
    while True:
        print("""
╔════════════════════════════╗
║       MENU ADMIN           ║
╚════════════════════════════╝
1. Tambah Buku
2. Hapus Buku
3. Daftar Buku
4. Cari Buku
5. Laporan Aktivitas
6. Logout
""")
        p = input("Pilih: ")
        if p == "1": tambah_buku()
        elif p == "2": hapus_buku()
        elif p == "3": daftar_buku()
        elif p == "4": cari_buku()
        elif p == "5": laporan()
        elif p == "6": break
        else: print("Pilihan tidak valid.")

def menu_user():
    while True:
        print("""
        
╔════════════════════════════╗
║       MENU USER            ║
╚════════════════════════════╝
1. Daftar Buku
2. Pinjam Buku
3. Kembalikan Buku
4. Cari Buku
5. Keluar
""")
        p = input("Pilih: ")
        if p == "1": daftar_buku()
        elif p == "2": pinjam_buku()
        elif p == "3": kembalikan_buku()
        elif p == "4": cari_buku()
        elif p == "5": break
        else: print("Pilihan tidak valid.")

def menu_awal():
    while True:
        print("""
╔═══════════════════════════════════════════════════════╗
║                   PUS-PYTHA                           ║
║ (Perpustakaan Sekolah Sederhana – Python Application) ║
║               by Tim AREK_SIJA 2025                   ║
╚═══════════════════════════════════════════════════════╝
1. Login Admin
2. Masuk Sebagai User
3. Keluar
""")
        p = input("Pilih: ")
        if p == "1":
            user = input("Username: ")
            pw = input("Password: ")
            if user == "admin" and pw == "123":
                print("Login berhasil!")
                menu_admin()
            else:
                print("Login gagal.")
        elif p == "2": menu_user()
        elif p == "3":
            print("Terima kasih sudah menggunakan sistem perpustakaan!")
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    print("Selamat datang di PUS-PYTHA (Perpustakaan Sekolah Sederhana – Python Application)!")
    menu_awal()