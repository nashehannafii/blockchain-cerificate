# Blockchain Prototype System

This is a prototype digital degree (diploma) registry implemented as a simple blockchain. It demonstrates the flow of issuing, storing, and verifying degrees using a lightweight proof-of-work blockchain and a command line interface.

## Features

- ✅ Record and store issued degrees as transactions on the blockchain.
- 🔗 Simple mining (proof-of-work) to confirm transactions and add new blocks.
- 📱 Verify a degree using student ID (NIM) and a document hash.
- 🔍 Optional QR code generation for verification (requires `qrcode` and `Pillow`).
- 💻 Command Line Interface (CLI) for adding degrees (single or bulk), mining, verification, and viewing the chain.

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

## Project layout (directory tree)

```
blockcert/
├── app/
│   ├── __init__.py
│   ├── core.py            # blockchain core implementation
│   ├── models.py         # dataclasses for Block/Transaction
│   └── utils.py          # helpers (hash, QR generation, validation)
├── blockchain/
│   ├── __init__.py
│   ├── cli.py            # CLI wrapper
│   └── main.py           # demo entrypoint
├── data/                 # persisted blockchain and pending tx (pickle)
├── run                   # executable wrapper (./run)
├── run.py                # main runner
├── Makefile              # helper targets
└── README.md
```

## Sample output — `./run display`

Below is a sample of the `./run display` output (table view):

```
✅ Blockchain loaded: 3 blocks
📚 MENAMPILKAN BLOCKCHAIN
+---------+------------------+------------+-------------+---------------------+---------------------+
|   Block | Timestamp        |   Total TX |   Degree TX | Hash                | Previous Hash       |
+=========+==================+============+=============+=====================+=====================+
|       0 | 2025-10-23 04:35 |          1 |           0 | cea3cef99d642a53... | 0000000000000000... |
+---------+------------------+------------+-------------+---------------------+---------------------+
|       1 | 2025-10-23 04:46 |          2 |           2 | 000e11f48709c07e... | cea3cef99d642a53... |
+---------+------------------+------------+-------------+---------------------+---------------------+
|       2 | 2025-10-23 04:47 |          2 |           2 | 000134af701b0842... | 000e11f48709c07e... |
+---------+------------------+------------+-------------+---------------------+---------------------+
```


