from pathlib import Path
from cryptography.fernet import Fernet


class Encoder:


    def genkey(self):
        user_key = Fernet.generate_key()
        return user_key


    def encrypt(self, text, key):
        Fernet.generate_key()
        cipher = Fernet(key)
        return cipher.encrypt(text.encode()).decode()
      

    def decrypt(self, encrypted_text, key):
        cipeher = Fernet(key)
        decrypted_text = cipeher.decrypt(encrypted_text.encode())
        return decrypted_text.decode()
    



    def encrypt_file(self, file_path: str, key: bytes) -> str:
        cipher = Fernet(key)
        file = Path(file_path)

        # читаємо вміст файлу як байти
        data = file.read_bytes()

        # шифруємо
        encrypted = cipher.encrypt(data)

        # створюємо новий файл
        encrypted_path = file.with_suffix(file.suffix + ".enc")
        encrypted_path.write_bytes(encrypted)

        return str(encrypted_path)

    # 📂 Розшифрування файлу
    def decrypt_file(self, file_path: str, key: bytes) -> str:
        cipher = Fernet(key)
        file = Path(file_path)

        # читаємо зашифрований файл
        encrypted_data = file.read_bytes()

        # розшифровуємо
        decrypted = cipher.decrypt(encrypted_data)

        # видаляємо ".enc" або додаємо "_decrypted"
        if file.suffix == ".enc":
            output_path = file.with_name(file.stem)
        else:
            output_path = file.with_name(file.name + "_decrypted")

        output_path.write_bytes(decrypted)
        return str(output_path)
