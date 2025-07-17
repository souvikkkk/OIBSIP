# client/security.py

from cryptography.fernet import Fernet

# Replace this key with a secure, generated one and keep it the same across all clients
KEY = b'jWQLEELP8r5ff4fEtH8kFpiMN2GBqyiECr-MI0T-i5Y='  # 32-byte base64 key

cipher = Fernet(KEY)

def encrypt_message(message: str) -> str:
    return cipher.encrypt(message.encode()).decode()

def decrypt_message(token: str) -> str:
    try:
        return cipher.decrypt(token.encode()).decode()
    except Exception as e:
        print("[DECRYPTION ERROR]", e)
        return "[ENCRYPTED MESSAGE ERROR]"
