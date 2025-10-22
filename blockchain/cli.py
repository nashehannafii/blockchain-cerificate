import argparse
import sys
from datetime import datetime
import json

from app.core import UniversityBlockchain
from app.utils import generate_verification_qr, format_student_data


class BlockchainCLI:
    def __init__(self):
        self.blockchain = UniversityBlockchain()
    
    def run(self):
        """Menjalankan CLI"""
        parser = argparse.ArgumentParser(description="University Blockchain System")
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Add degree command
        add_parser = subparsers.add_parser("add-degree", help="Add a new degree transaction")
        add_parser.add_argument("--nim", required=True, help="Student NIM")
        add_parser.add_argument("--name", required=True, help="Student name")
        add_parser.add_argument("--degree", required=True, help="Degree title")
        add_parser.add_argument("--major", required=True, help="Major")
        add_parser.add_argument("--gpa", required=True, help="GPA")
        add_parser.add_argument("--grad-date", required=True, help="Graduation date (YYYY-MM-DD)")
        
        # Mine command
        subparsers.add_parser("mine", help="Mine pending transactions")
        
        # Verify command
        verify_parser = subparsers.add_parser("verify", help="Verify a degree")
        verify_parser.add_argument("--nim", required=True, help="Student NIM")
        verify_parser.add_argument("--hash", required=True, help="Document hash")
        
        # Student info command
        student_parser = subparsers.add_parser("student-info", help="Get student degrees")
        student_parser.add_argument("--nim", required=True, help="Student NIM")
        
        # Blockchain info command
        subparsers.add_parser("info", help="Show blockchain information")
        
        # Validate command
        subparsers.add_parser("validate", help="Validate blockchain integrity")
        
        # Display command
        display_parser = subparsers.add_parser("display", help="Display blockchain")
        display_parser.add_argument("--detailed", action="store_true", help="Show detailed view")
        
        # Generate QR command
        qr_parser = subparsers.add_parser("generate-qr", help="Generate verification QR code")
        qr_parser.add_argument("--nim", required=True, help="Student NIM")

        # Bulk add command
        bulk_parser = subparsers.add_parser("add-bulk", help="Add multiple degree transactions from a JSON file")
        bulk_parser.add_argument("--file", required=True, help="Path to JSON file containing an array of student objects")
        
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return
        
        try:
            if args.command == "add-degree":
                self.add_degree(args)
            elif args.command == "mine":
                self.mine_block()
            elif args.command == "verify":
                self.verify_degree(args)
            elif args.command == "student-info":
                self.get_student_info(args)
            elif args.command == "info":
                self.show_info()
            elif args.command == "validate":
                self.validate_chain()
            elif args.command == "display":
                self.display_chain(args.detailed)
            elif args.command == "generate-qr":
                self.generate_qr_code(args)
            elif args.command == "add-bulk":
                self.add_bulk(args)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def add_degree(self, args):
        """Menambahkan transaksi ijazah"""
        student_data = format_student_data(
            args.nim, args.name, args.degree, 
            args.major, args.gpa, args.grad_date
        )
        
        transaction_id = self.blockchain.add_degree_transaction(student_data)
        if transaction_id:
            print(f"✅ Transaksi berhasil ditambahkan!")
            print(f"📋 Transaction ID: {transaction_id}")
            print(f"⏳ Status: Pending (butuh mining)")
    
    def mine_block(self):
        """Menambang blok baru"""
        success = self.blockchain.mine_pending_transactions()
        if success:
            print("🎉 Mining selesai! Blockchain telah diperbarui.")
    
    def verify_degree(self, args):
        """Memverifikasi ijazah"""
        result = self.blockchain.verify_degree(args.hash, args.nim)
        
        if result["verified"]:
            print("✅ IJAZAH TERVERIFIKASI")
            print(f"📦 Tercatat di Blok: #{result['block_index']}")
            print(f"👨‍🎓 Nama: {result['transaction_data']['student_name']}")
            print(f"🎓 Gelar: {result['transaction_data']['degree']}")
            print(f"📚 Jurusan: {result['transaction_data']['major']}")
            print(f"🔗 Hash Blok: {result['block_hash'][:16]}...")
        else:
            print("❌ IJAZAH TIDAK TERVERIFIKASI")
            print(f"💡 Pesan: {result['message']}")
    
    def get_student_info(self, args):
        """Mendapatkan info mahasiswa"""
        degrees = self.blockchain.get_student_degrees(args.nim)
        
        if not degrees:
            print(f"❌ Tidak ditemukan ijazah untuk NIM {args.nim}")
            return
        
        print(f"📚 Daftar Ijazah untuk NIM {args.nim}:")
        for i, degree in enumerate(degrees, 1):
            data = degree['degree_data']
            print(f"\n{i}. {data['degree']} - {data['major']}")
            print(f"   📊 GPA: {data['gpa']}")
            print(f"   🎓 Tanggal Lulus: {data['graduation_date']}")
            print(f"   📦 Blok: #{degree['block_index']}")
            print(f"   🔐 Hash: {data['document_hash'][:16]}...")
    
    def show_info(self):
        """Menampilkan info blockchain"""
        info = self.blockchain.get_blockchain_info()
        
        print("📊 BLOCKCHAIN INFORMATION")
        print(f"📦 Total Blok: {info['total_blocks']}")
        print(f"📋 Total Transaksi: {info['total_transactions']}")
        print(f"🎓 Transaksi Ijazah: {info['degree_transactions']}")
        print(f"⏳ Pending Transactions: {info['pending_transactions']}")
        print(f"⚙️  Difficulty: {info['difficulty']}")
        print(f"🔗 Hash Terakhir: {info['chain_hash'][:16]}...")
    
    def validate_chain(self):
        """Validasi blockchain"""
        print("🔍 Memvalidasi blockchain...")
        is_valid = self.blockchain.is_chain_valid()
        
        if is_valid:
            print("✅ Blockchain valid dan aman!")
        else:
            print("❌ Blockchain tidak valid!")
    
    def display_chain(self, detailed=False):
        """Menampilkan blockchain"""
        print("📚 MENAMPILKAN BLOCKCHAIN")
        self.blockchain.display_chain(detailed)
    
    def generate_qr_code(self, args):
        """Generate QR code untuk verifikasi"""
        degrees = self.blockchain.get_student_degrees(args.nim)
        if not degrees:
            print(f"❌ Tidak ditemukan ijazah untuk NIM {args.nim}")
            return
        
        # Ambil ijazah terbaru
        latest_degree = degrees[-1]
        student_data = {
            "nim": args.nim,
            "transaction_id": latest_degree['degree_data']['transaction_id'],
            "document_hash": latest_degree['degree_data']['document_hash']
        }
        
        filename = generate_verification_qr(student_data)
        print(f"✅ QR Code untuk NIM {args.nim} berhasil dibuat: {filename}")

    def add_bulk(self, args):
        """Add many students from a JSON file."""
        file_path = args.file
        try:
            with open(file_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)

            if not isinstance(data, list):
                print("❌ File harus berisi array JSON dari objek mahasiswa")
                return

            tx_ids = self.blockchain.add_bulk_transactions(data)
            print(f"✅ Berhasil menambahkan {len(tx_ids)} transaksi (pending).")
        except FileNotFoundError:
            print(f"❌ File tidak ditemukan: {file_path}")
        except json.JSONDecodeError as e:
            print(f"❌ JSON tidak valid: {e}")
        except Exception as e:
            print(f"❌ Error saat menambahkan bulk: {e}")


def main():
    cli = BlockchainCLI()
    cli.run()


if __name__ == "__main__":
    main()