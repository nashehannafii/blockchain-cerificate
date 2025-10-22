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

## Makefile

Beberapa target berguna yang disediakan di `Makefile`:

- `make run` — cetak petunjuk singkat
- `make mine` — jalankan mining (sama dengan `./run mine`)
- `make display` — tampilkan blockchain
- `make validate` — validasi integritas
- `make add-degree` — helper untuk menambahkan ijazah via variabel (lihat Makefile)

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

## Skrip `update`

- Ada skrip `update` di root repo yang menjalankan `git add .`, `git commit -m "update"` dan `git push`. Jika tidak executable, ubah permission dan jalankan:
```bash
chmod +x update
./update
```

Perhatian: skrip ini melakukan commit dan push otomatis — pastikan perubahan sudah benar sebelum menjalankan.

## Rekomendasi pengembangan

- Ubah format penyimpanan dari pickle ke JSON/SQLite untuk ketahanan dan keterbacaan.
- Tambahkan opsi `--dry-run` pada `add-bulk` untuk validasi tanpa menyimpan.
- Tambahkan tes unit untuk save/load dan import massal.

Jika ingin, saya bisa menambahkan salah satu fitur di atas.