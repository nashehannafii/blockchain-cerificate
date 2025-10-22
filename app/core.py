import hashlib
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
import pickle
import os

from app.models import Block, Transaction, StudentDegree
from app.utils import calculate_hash, validate_nim, validate_gpa


class UniversityBlockchain:
    def __init__(self, difficulty: int = 3):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        self.data_file = "data/blockchain_data.pkl"
        self._initialize_blockchain()

    def _initialize_blockchain(self):
        """Initialize blockchain dengan genesis block atau load dari file"""
        if os.path.exists(self.data_file):
            self.load_blockchain()
        else:
            self.chain = [self._create_genesis_block()]
            self.save_blockchain()

    def _create_genesis_block(self) -> Block:
        """Membuat genesis block"""
        genesis_transaction = Transaction(
            transaction_type="system",
            student_nim="GENESIS",
            student_name="System",
            degree="Genesis Block",
            major="System",
            gpa="0.0",
            graduation_date=datetime.now().strftime("%Y-%m-%d"),
            document_hash="0" * 64,
            issuer="System",
            timestamp=datetime.now()
        )
        
        return Block(
            index=0,
            transactions=[genesis_transaction],
            timestamp=datetime.now(),
            previous_hash="0" * 64
        )

    def add_degree_transaction(self, student_data: Dict) -> str:
        """Menambahkan transaksi ijazah baru"""
        try:
            # Validasi data
            if not validate_nim(student_data["nim"]):
                raise ValueError("NIM tidak valid")
            
            if not validate_gpa(student_data["gpa"]):
                raise ValueError("GPA tidak valid")

            # Hitung hash dokumen
            document_hash = calculate_hash(
                f"{student_data['nim']}"
                f"{student_data['name']}"
                f"{student_data['degree']}"
                f"{student_data['major']}"
                f"{student_data['gpa']}"
                f"{student_data['graduation_date']}"
            )

            # Buat transaksi
            transaction = Transaction(
                transaction_type="degree_issuance",
                student_nim=student_data["nim"],
                student_name=student_data["name"],
                degree=student_data["degree"],
                major=student_data["major"],
                gpa=student_data["gpa"],
                graduation_date=student_data["graduation_date"],
                document_hash=document_hash,
                issuer=student_data.get("issuer", "University Registrar"),
                timestamp=datetime.now()
            )

            self.pending_transactions.append(transaction)
            # Persist pending transactions so they survive separate CLI runs
            try:
                self.save_blockchain()
            except Exception:
                # Non-fatal: transaction was added in-memory
                pass

            print(f"✅ Transaksi ijazah untuk {student_data['name']} berhasil ditambahkan ke pending transactions")
            return transaction.transaction_id
        except Exception as e:
            print(f"❌ Error menambahkan transaksi: {e}")
            return ""

    def add_bulk_transactions(self, students: List[Dict]) -> List[str]:
        """Tambahkan banyak transaksi sekaligus dari list of student data dicts.

        Returns list of transaction IDs for added transactions.
        """
        tx_ids: List[str] = []
        for student in students:
            try:
                tx_id = self.add_degree_transaction(student)
                if tx_id:
                    tx_ids.append(tx_id)
            except Exception as e:
                # Continue on error for other records, but report
                print(f"❌ Error adding student {student.get('nim') or student.get('name')}: {e}")
        # save_blockchain is already called by add_degree_transaction
        return tx_ids

    def mine_pending_transactions(self) -> bool:
        """Menambang blok baru dengan transaksi pending"""
        if not self.pending_transactions:
            print("❌ Tidak ada transaksi pending untuk ditambang")
            return False

        print(f"⛏️  Menambang blok baru dengan {len(self.pending_transactions)} transaksi...")
        
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions.copy(),
            timestamp=datetime.now(),
            previous_hash=self.get_latest_block().hash
        )

        # Mining process dengan progress indicator
        print("Mining in progress", end="")
        start_time = time.time()
        
        while new_block.hash[:self.difficulty] != "0" * self.difficulty:
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()
            if new_block.nonce % 1000 == 0:
                print(".", end="", flush=True)

        mining_time = time.time() - start_time
        print(f"\n✅ Blok #{new_block.index} berhasil ditambang!")
        print(f"⏱️  Waktu mining: {mining_time:.2f} detik")
        print(f"🔗 Hash: {new_block.hash}")
        print(f"🔢 Nonce: {new_block.nonce}")

        self.chain.append(new_block)
        self.pending_transactions = []
        self.save_blockchain()
        
        return True

    def verify_degree(self, document_hash: str, student_nim: str) -> Dict:
        """Memverifikasi keaslian ijazah"""
        for block in self.chain:
            for transaction in block.transactions:
                if (transaction.transaction_type == "degree_issuance" and
                    transaction.student_nim == student_nim and
                    transaction.document_hash == document_hash):
                    
                    return {
                        "verified": True,
                        "block_index": block.index,
                        "transaction_data": transaction.to_dict(),
                        "block_hash": block.hash,
                        "timestamp": block.timestamp.isoformat()
                    }
        
        return {"verified": False, "message": "Ijazah tidak ditemukan dalam blockchain"}

    def get_student_degrees(self, student_nim: str) -> List[Dict]:
        """Mendapatkan semua ijazah seorang mahasiswa"""
        degrees = []
        for block in self.chain:
            for transaction in block.transactions:
                if (transaction.transaction_type == "degree_issuance" and 
                    transaction.student_nim == student_nim):
                    degrees.append({
                        "block_index": block.index,
                        "degree_data": transaction.to_dict(),
                        "block_timestamp": block.timestamp.isoformat()
                    })
        return degrees

    def get_blockchain_info(self) -> Dict:
        """Mendapatkan informasi blockchain"""
        total_transactions = sum(len(block.transactions) for block in self.chain)
        degree_transactions = sum(
            1 for block in self.chain 
            for tx in block.transactions 
            if tx.transaction_type == "degree_issuance"
        )
        
        return {
            "total_blocks": len(self.chain),
            "total_transactions": total_transactions,
            "degree_transactions": degree_transactions,
            "pending_transactions": len(self.pending_transactions),
            "difficulty": self.difficulty,
            "chain_hash": self.get_latest_block().hash
        }

    def get_latest_block(self) -> Block:
        """Mendapatkan blok terakhir"""
        return self.chain[-1]

    def is_chain_valid(self) -> bool:
        """Memvalidasi integritas seluruh blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Cek hash blok saat ini
            if current_block.hash != current_block.calculate_hash():
                print(f"❌ Hash blok {current_block.index} tidak valid!")
                return False

            # Cek koneksi dengan blok sebelumnya
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ Hash sebelumnya pada blok {current_block.index} tidak valid!")
                return False

            # Cek proof-of-work
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                print(f"❌ Proof-of-work blok {current_block.index} tidak valid!")
                return False

        print("✅ Blockchain valid dan aman!")
        return True

    def save_blockchain(self):
        """Menyimpan blockchain ke file"""
        os.makedirs("data", exist_ok=True)
        # Store both chain and pending transactions for full persistence
        payload = {
            "chain": self.chain,
            "pending_transactions": self.pending_transactions,
        }
        with open(self.data_file, "wb") as f:
            pickle.dump(payload, f)

    def load_blockchain(self):
        """Load blockchain dari file"""
        try:
            with open(self.data_file, "rb") as f:
                data = pickle.load(f)

            # Backwards compatibility: older files may contain only the chain list
            if isinstance(data, dict) and "chain" in data:
                self.chain = data.get("chain", [self._create_genesis_block()])
                self.pending_transactions = data.get("pending_transactions", [])
            elif isinstance(data, list):
                self.chain = data
                self.pending_transactions = []
            else:
                # Unknown format: recreate genesis
                self.chain = [self._create_genesis_block()]
                self.pending_transactions = []

            print(f"✅ Blockchain loaded: {len(self.chain)} blocks")
        except Exception as e:
            print(f"❌ Error loading blockchain: {e}")
            self.chain = [self._create_genesis_block()]
            self.pending_transactions = []

    def display_chain(self, detailed: bool = False):
        """Menampilkan isi blockchain"""
        from tabulate import tabulate
        
        if not detailed:
            # Tampilan ringkas
            table_data = []
            for block in self.chain:
                degree_txs = sum(1 for tx in block.transactions if tx.transaction_type == "degree_issuance")
                table_data.append([
                    block.index,
                    block.timestamp.strftime("%Y-%m-%d %H:%M"),
                    len(block.transactions),
                    degree_txs,
                    block.hash[:16] + "...",
                    block.previous_hash[:16] + "..."
                ])
            
            headers = ["Block", "Timestamp", "Total TX", "Degree TX", "Hash", "Previous Hash"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        else:
            # Tampilan detail
            for block in self.chain:
                print(f"\n{'='*60}")
                print(f"📦 BLOK #{block.index}")
                print(f"{'='*60}")
                print(f"🕐 Timestamp: {block.timestamp}")
                print(f"🔗 Hash: {block.hash}")
                print(f"🔗 Previous Hash: {block.previous_hash}")
                print(f"🔢 Nonce: {block.nonce}")
                print(f"📋 Jumlah Transaksi: {len(block.transactions)}")
                
                for i, tx in enumerate(block.transactions):
                    if tx.transaction_type == "degree_issuance":
                        print(f"\n  📝 Transaksi #{i+1} - Ijazah")
                        print(f"     👨‍🎓 NIM: {tx.student_nim}")
                        print(f"     🧑 Nama: {tx.student_name}")
                        print(f"     🎓 Gelar: {tx.degree}")
                        print(f"     📚 Jurusan: {tx.major}")
                        print(f"     📊 GPA: {tx.gpa}")
                        print(f"     🏅 Penerbit: {tx.issuer}")
                        print(f"     🔐 Document Hash: {tx.document_hash[:16]}...")
                    else:
                        print(f"\n  ⚙️  Transaksi #{i+1} - System")
                
                print(f"{'='*60}")