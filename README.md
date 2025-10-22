# Blockchain Prototype System

Sistem pencatatan ijazah digital berbasis blockchain.

## Fitur

- ✅ Pencatatan ijazah digital yang aman
- 🔗 Blockchain dengan Proof-of-Work
- 📱 Verifikasi ijazah dengan QR Code
- 🔍 Validasi integritas blockchain
- 💻 Command Line Interface (CLI) dengan subcommands
# Prototype System

This is a prototype digital degree (diploma) registry implemented as a simple blockchain. It demonstrates the flow of issuing, storing, and verifying degrees using a lightweight proof-of-work blockchain and a command line interface.

## Features

- Record and store issued degrees as transactions on the blockchain.
- Simple mining (proof-of-work) to confirm transactions and add new blocks.
- Verify a degree using student ID (NIM) and a document hash.
- Optional QR code generation for verification (requires `qrcode` and `Pillow`).
- Command Line Interface (CLI) for adding degrees (single or bulk), mining, verification, and viewing the chain.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/nashehannafii/blockchain-cerificate.git
cd blockchain-cerificate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Make the run wrapper executable:

```bash
chmod +x run
```

## How to Use

Use the wrapper `./run` or call the script directly with `python3 run.py`.

Common commands:

- `./run` — Run a short demo (no arguments).
- `./run add-degree --nim <NIM> --name <NAME> --degree <DEGREE> --major <MAJOR> --gpa <GPA> --grad-date <YYYY-MM-DD>` — Add a single degree transaction (pending).
- `./run add-bulk --file <PATH>` — Add multiple degree transactions from a JSON file (array of student objects).
- `./run mine` — Mine pending transactions into a new block.
- `./run verify --nim <NIM> --hash <DOCUMENT_HASH>` — Verify a degree record.
- `./run student-info --nim <NIM>` — Show all degrees recorded for a student.
- `./run info` — Show blockchain summary (blocks, transactions, pending, difficulty).
- `./run validate` — Validate blockchain integrity (hashes and proof-of-work).
- `./run display [--detailed]` — Display the blockchain (use `--detailed` for per-transaction detail).
- `./run generate-qr --nim <NIM>` — Generate a verification QR code for a student's latest degree.

Notes:

- Data is persisted to `data/blockchain_data.pkl` using Python `pickle` and contains both the chain and the pending transactions. This allows separate CLI runs to see the same pending transactions.
- Optional packages for enhanced features: `tabulate`, `qrcode`, `Pillow`.
- For help on a specific command run: `./run <command> --help`.

