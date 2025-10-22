# Blockchain Prototype System

Sistem pencatatan ijazah digital berbasis blockchain.

## Fitur

- ✅ Pencatatan ijazah digital yang aman
- 🔗 Blockchain dengan Proof-of-Work
- 📱 Verifikasi ijazah dengan QR Code
- 🔍 Validasi integritas blockchain
- 💻 Command Line Interface (CLI) dengan subcommands

## Instalasi

1. Clone atau download project ini

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Jalankan demo atau gunakan CLI

- Jalankan demo cepat (menampilkan alur contoh):
```bash
./run
```

- Untuk bantuan lengkap:
```bash
./run -help
# contoh: ./run -help
```

- Untuk daftar subcommands dan opsi tiap perintah:
```bash
./run <command> --help
# contoh: ./run add-degree --help
```

## Fitur impor massal (bulk JSON)

Tambahkan banyak transaksi dari file JSON yang berisi array objek mahasiswa.

Contoh format (`data/students.json`):

```json
[
	{"nim":"20210020","name":"Sari","degree":"Sarjana Biologi","major":"Biologi","gpa":"3.50","graduation_date":"2024-06-15"},
	{"nim":"20210021","name":"Dina","degree":"Sarjana Kimia","major":"Kimia","gpa":"3.60","graduation_date":"2024-06-15"}
]
```

Perintah untuk mengimpor:
```bash
./run add-bulk --file data/students.json
```

Setelah itu jalankan:
```bash
./run mine
```

## Penyimpanan & Persistensi

- Blockchain dan `pending_transactions` disimpan di `data/blockchain_data.pkl` menggunakan pickle. File ini menyimpan chain dan transaksi pending sehingga CLI yang dijalankan di proses berbeda akan melihat transaksi yang sama.
- Jika file pickle rusak/korup, aplikasi akan membuat genesis block baru (pesan error akan ditampilkan).

## Daftar Perintah (Command List)

Berikut daftar lengkap command / subcommand yang tersedia di prototipe ini beserta contoh penggunaan singkat:

- `./run` — Menjalankan demo singkat (tanpa argumen).

- `./run add-degree --nim <NIM> --name <NAME> --degree <DEGREE> --major <MAJOR> --gpa <GPA> --grad-date <YYYY-MM-DD>`
	- Tambah 1 transaksi ijazah ke pending.

- `./run add-bulk --file <PATH>`
	- Tambah banyak transaksi dari file JSON berisi array objek mahasiswa.

- `./run mine` — Menambang (mine) semua transaksi pending ke blok baru.

- `./run verify --nim <NIM> --hash <DOCUMENT_HASH>` — Verifikasi ijazah.

- `./run student-info --nim <NIM>` — Tampilkan semua ijazah untuk NIM.

- `./run info` — Tampilkan ringkasan blockchain (jumlah blok, transaksi, pending, difficulty).

- `./run validate` — Validasi integritas blockchain (cek hash dan proof-of-work).

- `./run display [--detailed]` — Tampilkan isi blockchain (opsional: `--detailed` untuk detail tiap transaksi).

- `./run generate-qr --nim <NIM>` — Generate QR verification image untuk NIM (menggunakan transaksi terakhir untuk NIM tersebut).

Makefile helper (di root):

- `make run` — Cetak petunjuk singkat.
- `make mine` — Shortcut untuk `./run mine`.
- `make display` — Shortcut untuk `./run display`.
- `make validate` — Shortcut untuk `./run validate`.
- `make add-degree NIM=... NAME='...' DEGREE='...' MAJOR='...' GPA='...' GRAD_DATE='...'` — Helper untuk menambahkan satu transaksi menggunakan variabel lingkungan.

Catatan:

- Pastikan dependencies sudah diinstall (`pip install -r requirements.txt`) untuk fitur optional seperti `tabulate` dan `qrcode`.
- Validasi input: `nim` harus numeric, `gpa` harus antara 0.0—4.0.
- Bulk import akan melaporkan error per-record jika ada yang invalid dan melanjutkan untuk record lain.
