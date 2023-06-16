# Imports
import hashlib


def sha256(string: str, seed: str) -> str:
    """Hashes a given input with the SHA256 function"""
    return hashlib.sha256((string+seed).encode()).hexdigest()
