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
