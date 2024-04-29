import hashlib
import json
import random
import string
from datetime import datetime

from lib.aes.aes import decrypt_data
from lib.parser import get_keys_and_values


def get_body_by_plugin(response, plugin):
    return parse_plugin_data(get_raw_body(response, plugin))


def get_raw_body(response, plugin):
    return json.loads(response['originalRequest'].get('body', {}).get('raw', ''))


def parse_plugin_data(body):
    if body is not None:
        get_keys_and_values(body['payload'], body['source'])
        return body['payload']


""" plugin function """


def random_string(length):
    """Generate a random string of specified length."""
    # letters = string.ascii_letters + string.digits + string.punctuation
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(int(length)))


def checksum(items):
    return generate_checksum(items)


def generate_checksum(data):
    """Generate a SHA-256 checksum for the given data."""
    try:
        # Create a new SHA-256 hash object
        hash_object = hashlib.sha256()

        # Update the hash object with the data bytes
        hash_object.update(data.encode('utf-8'))

        # Get the digest (checksum) in bytes
        checksum_bytes = hash_object.digest()

        # Convert the bytes to hexadecimal representation
        checksum_hex = ''.join(format(byte, '02x') for byte in checksum_bytes)

        return checksum_hex
    except Exception as e:
        print("Error:", e)
        return None


def decrypt(arg):
    return decrypt_data(arg)


def today_date():
    return datetime.today().strftime('%Y-%m-%d')
