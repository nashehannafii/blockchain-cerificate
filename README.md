# Blockchain Prototype System

Sistem pencatatan ijazah digital berbasis blockchain.

## Fitur

- ✅ Pencatatan ijazah digital yang aman
- 🔗 Blockchain dengan Proof-of-Work
- 📱 Verifikasi ijazah dengan QR Code
- 🔍 Validasi integritas blockchain
- 💻 Command Line Interface (CLI) dengan subcommands
# Prototype Sistem

Sistem pencatatan ijazah digital berbasis blockchain (prototype). Tujuan: menampilkan alur penerbitan, penyimpanan, dan verifikasi ijazah menggunakan struktur blockchain sederhana dengan proof-of-work.

## Fitur

- Pencatatan dan penyimpanan ijazah sebagai transaksi pada blockchain.
- Mining (proof-of-work) untuk mengonfirmasi transaksi dan menambah blok.
- Verifikasi ijazah berdasarkan NIM + document hash.
- Generasi QR code untuk verifikasi (opsional, memerlukan `qrcode`/`Pillow`).
- CLI untuk operasi: menambah transaksi (single/bulk), menambang, verifikasi, dan menampilkan blockchain.

## Cara Instalasi

1. Clone repository:

```bash
git clone https://github.com/nashehannafii/blockchain-cerificate.git
cd blockchain-cerificate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Pastikan file `run` executable (opsional):

```bash
chmod +x run
```

## Cara Penggunaan Fitur

Gunakan `./run <command>` (atau `python3 run.py <command>`). Ringkasan perintah utama:

- `./run` — Jalankan demo singkat (tanpa argumen).
- `./run add-degree --nim <NIM> --name <NAME> --degree <DEGREE> --major <MAJOR> --gpa <GPA> --grad-date <YYYY-MM-DD>` — Tambah satu transaksi ijazah (pending).
- `./run add-bulk --file <PATH>` — Tambah banyak transaksi dari file JSON (array objek mahasiswa).
- `./run mine` — Menambang semua transaksi pending menjadi blok baru.
- `./run verify --nim <NIM> --hash <DOCUMENT_HASH>` — Verifikasi ijazah.
- `./run student-info --nim <NIM>` — Tampilkan ijazah untuk NIM.
- `./run info` — Tampilkan ringkasan blockchain.
- `./run validate` — Validasi integritas blockchain.
- `./run display [--detailed]` — Tampilkan isi blockchain (opsional: `--detailed`).
- `./run generate-qr --nim <NIM>` — Generate QR verifikasi untuk NIM.

Catatan:

- Data disimpan di `data/blockchain_data.pkl` (pickle) dan mencakup chain serta pending transactions.
- Pastikan dependencies seperti `tabulate`, `qrcode`, dan `Pillow` terpasang jika ingin fitur terkait.
- Untuk bantuan tiap perintah gunakan: `./run <command> --help`.

