from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List
import hashlib
import uuid


@dataclass
class Transaction:
    transaction_type: str  # "degree_issuance" atau "system"
    student_nim: str
    student_name: str
    degree: str
    major: str
    gpa: str
    graduation_date: str
    document_hash: str
    issuer: str
    timestamp: datetime
    transaction_id: str = None
    
    def __post_init__(self):
        if self.transaction_id is None:
            self.transaction_id = str(uuid.uuid4())[:16]
    
    def calculate_hash(self):
        transaction_string = (
            f"{self.transaction_type}{self.student_nim}{self.student_name}"
            f"{self.degree}{self.major}{self.gpa}{self.graduation_date}"
            f"{self.document_hash}{self.issuer}{self.timestamp.isoformat()}"
        )
        return hashlib.sha256(transaction_string.encode()).hexdigest()
    
    def to_dict(self):
        return {
            **asdict(self),
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class Block:
    index: int
    transactions: List[Transaction]
    timestamp: datetime
    previous_hash: str
    nonce: int = 0
    hash: str = None
    
    def __post_init__(self):
        if self.hash is None:
            self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_string = (
            f"{self.index}"
            f"{''.join(tx.calculate_hash() for tx in self.transactions)}"
            f"{self.timestamp.isoformat()}"
            f"{self.previous_hash}"
            f"{self.nonce}"
        )
        return hashlib.sha256(block_string.encode()).hexdigest()


@dataclass
class StudentDegree:
    nim: str
    name: str
    degree: str
    major: str
    gpa: float
    graduation_date: str
    issue_date: str
    document_hash: str
    block_index: int
    transaction_id: str