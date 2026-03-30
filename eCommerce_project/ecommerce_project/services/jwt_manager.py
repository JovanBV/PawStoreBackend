import os
from dotenv import load_dotenv
from pathlib import Path
import jwt
import time

load_dotenv()

class JWTManager:
    def __init__(self):
        base_dir = Path(__file__).parent.parent.parent
        
        private_key_path = base_dir / "keys" / "private_key.pem"
        public_key_path = base_dir / "keys" / "public_key.pem"

        try:
            with open(private_key_path, "r") as f:
                self.private_key = f.read()
            with open(public_key_path, "r") as f:
                self.public_key = f.read()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"No se encontraron las claves JWT: {e}")

    def encode(self, data, exp_seconds=3600):
        try:
            payload = {
                "data": data,
                "iat": int(time.time()),
                "exp": int(time.time()) + exp_seconds
            }
            return jwt.encode(payload, self.private_key, algorithm="RS256")
        except Exception as e:
            raise ValueError(f"Unable to encode token: {e}")

    def decode(self, token):
        try:
            return jwt.decode(token, self.public_key, algorithms=["RS256"])
        except jwt.ExpiredSignatureError:
            raise ValueError("Expired token")