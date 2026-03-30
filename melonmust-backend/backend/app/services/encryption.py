from cryptography.fernet import Fernet
from app.core.config import settings

fernet = Fernet(settings.SECRET_KEY.encode())

def encrypt(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()

