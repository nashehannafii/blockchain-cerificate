import hashlib
import qrcode
from PIL import Image
import json
from datetime import datetime


def calculate_hash(data: str) -> str:
    """Menghitung SHA-256 hash dari data"""
    return hashlib.sha256(data.encode()).hexdigest()


def validate_nim(nim: str) -> bool:
    """Validasi format NIM"""
    return nim.isdigit() and len(nim) >= 8


def validate_gpa(gpa: str) -> bool:
    """Validasi format GPA"""
    try:
        gpa_float = float(gpa)
        return 0.0 <= gpa_float <= 4.0
    except ValueError:
        return False


def generate_verification_qr(student_data: dict, verification_url: str = "http://verify.unida.gontor.ac.id/verify"):
    """Generate QR code untuk verifikasi ijazah"""
    qr_data = {
        "transaction_id": student_data.get("transaction_id"),
        "document_hash": student_data.get("document_hash"),
        "student_nim": student_data.get("nim"),
        "verification_url": verification_url,
        "timestamp": datetime.now().isoformat()
    }
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    filename = f"qr_verification_{student_data['nim']}.png"
    img.save(filename)
    
    print(f"✅ QR Code berhasil dibuat: {filename}")
    return filename


def format_student_data(nim: str, name: str, degree: str, major: str, gpa: str, graduation_date: str) -> dict:
    """Format data mahasiswa untuk transaksi"""
    return {
        "nim": nim,
        "name": name,
        "degree": degree,
        "major": major,
        "gpa": gpa,
        "graduation_date": graduation_date,
        "issuer": "University Registrar Office"
    }