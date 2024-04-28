from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

salt = b'H\x91\xab\xbe\xba\x02l\xc4=8\xc3\xc8\xea~e{'

def encrypt(data, password):
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CFB(salt), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(str(data).encode()) + encryptor.finalize()
    return b64encode(salt + encrypted_data).decode()

def derive_key(password, salt):
    return PBKDF2HMAC(
        salt=salt,
        length=32,
        iterations=100000,
        algorithm=hashes.SHA256(),
        backend=default_backend()
    ).derive(str(password).encode())

def decrypt(encrypted_data, password):
    encrypted_data = b64decode(str(encrypted_data).encode())
    salt = encrypted_data[:16]
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CFB(salt))
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data[16:]) + decryptor.finalize()
    return decrypted_data.decode()