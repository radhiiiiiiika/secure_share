from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

KEY = b'This_is_a_16byte'  # 16 byte key

def encrypt_file(file_path, output_path):
    cipher = AES.new(KEY, AES.MODE_EAX)
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    ciphertext, tag = cipher.encrypt_and_digest(data)
    
    with open(output_path, 'wb') as f:
        f.write(cipher.nonce)
        f.write(tag)
        f.write(ciphertext)

def decrypt_file(file_path, output_path):
    with open(file_path, 'rb') as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()
    
    cipher = AES.new(KEY, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    
    with open(output_path, 'wb') as f:
        f.write(data)