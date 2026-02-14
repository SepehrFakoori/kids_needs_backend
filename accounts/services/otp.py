import hashlib
import secrets
import hmac
from datetime import datetime, timedelta


class OTPService:
    def __init__(self, ttl_minutes: int = 2):
        self.ttl_minutes = ttl_minutes

    def generate_code(self) -> str:
        return f"{secrets.randbelow(10 ** 6):06d}"

    def generate_salt(self) -> str:
        return secrets.token_hex(16)

    def hash_code(self, code: str, salt: str) -> str:
        raw = f"{code}:{salt}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def expires_at(self) -> datetime:
        return datetime.utcnow() + timedelta(minutes=self.ttl_minutes)

    def verify_code(self, code: str, salt: str, code_hash: str) -> bool:
        new_hash = self.hash_code(code=code, salt=salt)
        return hmac.compare_digest(new_hash, code_hash)
