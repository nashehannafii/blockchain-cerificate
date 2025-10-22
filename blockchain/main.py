from app.core import UniversityBlockchain
from app.utils import format_student_data, generate_verification_qr


def demo_system():
    """Demo sistem blockchain universitas"""
    print("🎓 UNIVERSITY BLOCKCHAIN SYSTEM DEMO")
    print("=" * 50)
    
    # Inisialisasi blockchain
    blockchain = UniversityBlockchain(difficulty=2)
    
    # Data sample mahasiswa
    sample_students = [
        {
            "nim": "20210001",
            "name": "Anna Wijaya", 
            "degree": "Sarjana Komputer",
            "major": "Teknik Informatika",
            "gpa": "3.75",
            "graduation_date": "2024-06-15"
        },
        {
            "nim": "20210002",
            "name": "Budi Santoso",
            "degree": "Sarjana Ekonomi", 
            "major": "Manajemen",
            "gpa": "3.60",
            "graduation_date": "2024-06-15"
        },
        {
            "nim": "20210003",
            "name": "Citra Dewi",
            "degree": "Sarjana Hukum",
            "major": "Hukum Bisnis",
            "gpa": "3.80",
            "graduation_date": "2024-06-15"
        }
    ]
    
    # Tambahkan transaksi
    print("\n1. MENAMBAHKAN TRANSAKSI IJAZAH")
    for student in sample_students:
        tx_id = blockchain.add_degree_transaction(student)
        print(f"   ✅ {student['name']} - {student['degree']}")
    
    # Mine blok
    print(f"\n2. MINING BLOK (#{len(blockchain.chain)})")
    blockchain.mine_pending_transactions()
    
    # Verifikasi
    print(f"\n3. VERIFIKASI IJAZAH")
    test_student = sample_students[0]
    verification = blockchain.verify_degree(
        blockchain.pending_transactions[0].document_hash if blockchain.pending_transactions else "",
        test_student["nim"]
    )
    
    if verification["verified"]:
        print(f"   ✅ Ijazah {test_student['name']} terverifikasi!")
    else:
        print("   ℹ️  Butuh mining untuk verifikasi")
    
    # Info blockchain
    print(f"\n4. INFORMASI BLOCKCHAIN")
    info = blockchain.get_blockchain_info()
    print(f"   📦 Total Blok: {info['total_blocks']}")
    print(f"   📋 Total Transaksi: {info['total_transactions']}")
    print(f"   🎓 Transaksi Ijazah: {info['degree_transactions']}")
    
    print(f"\n🎉 Demo selesai! Gunakan CLI untuk operasi lebih lanjut.")


if __name__ == "__main__":
    demo_system()