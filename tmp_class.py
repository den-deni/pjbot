from cryptography.fernet import Fernet
from typing import Optional

class UserCryptoManager:
    """Клас для роботи з індивідуальними ключами користувачів у Telegram боті"""

    def __init__(self, key: Optional[bytes] = None):
        self._key: Optional[bytes] = None
        self._cipher: Optional[Fernet] = None

        if key:
            self.key = key  # використовуємо setter

    # === GETTER для ключа ===
    @property
    def key(self) -> Optional[bytes]:
        return self._key

    # === SETTER для ключа ===
    @key.setter
    def key(self, new_key: bytes):
        if not isinstance(new_key, bytes):
            raise TypeError("Ключ має бути типу bytes!")
        self._key = new_key
        self._cipher = Fernet(self._key)
        print("🔑 Ключ користувача встановлено або оновлено!")

    # === Генерація нового ключа ===
    @staticmethod
    def generate_key() -> bytes:
        return Fernet.generate_key()

    # === Шифрування тексту ===
    def encrypt(self, text: str) -> bytes:
        if not self._cipher:
            raise ValueError("Спочатку встанови ключ!")
        return self._cipher.encrypt(text.encode())

    # === Розшифрування тексту ===
    def decrypt(self, token: bytes) -> str:
        if not self._cipher:
            raise ValueError("Спочатку встанови ключ!")
        return self._cipher.decrypt(token).decode()


# b = UserCryptoManager(key=b'qSYkYI2eLCQ77FKonsz4Vmt3051saKlPRFxCxsLjWAk=')
# text = b.encrypt("hello world")
# print(text)

# d = b.decrypt(b'gAAAAABo9nbmFj-nUg5BEmgMkT-JTllBl1NPaF60GiP-KOXIKpJQbuVaJV0hQ241lpeoORn-lvtQiT2udAIHRsunsKLAtaeUcQ==')
# print(d)