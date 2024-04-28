from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import hashlib

org_aes_key = b"SRAXCAV"
iv = b"adegasfeqfkddsge"


def encrypt_data(plain_text_before_padding):
    aes_key = org_aes_key + b'\x00' * 9

    padder = padding.PKCS7(128).padder()
    plain_text_bytes = padder.update(plain_text_before_padding.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_string = encryptor.update(plain_text_bytes) + encryptor.finalize()

    hash_map = hashlib.new('md5', encrypted_string).hexdigest()
    encoded_final_value = base64.standard_b64encode(iv + hash_map.encode() + encrypted_string).decode()

    return encoded_final_value


def decrypt_data(encoded_final_value):
    if not encoded_final_value:
        return encoded_final_value

    aes_key = org_aes_key + b'\x00' * 9

    try:
        encrypted_bytes = base64.standard_b64decode(encoded_final_value)
    except:
        return encoded_final_value

    actual_encrypted_str = encrypted_bytes[48:]

    decrypted_final_string = decrypt_cbc(actual_encrypted_str, aes_key, iv)

    try:
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_final_string_unpadded = unpadder.update(decrypted_final_string) + unpadder.finalize()
    except ValueError as e:
        raise ValueError("Invalid padding bytes. Decryption failed.") from e

    return decrypted_final_string_unpadded.decode()


def decrypt_cbc(cipher_text, enc_key, iv):
    cipher = Cipher(algorithms.AES(enc_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(cipher_text) + decryptor.finalize()