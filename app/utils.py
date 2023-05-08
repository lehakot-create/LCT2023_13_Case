import hashlib
from config import SALT


def hash_password(password):
    key = hashlib.pbkdf2_hmac(hash_name='sha256',
                              password=password.encode('utf-8'),
                              salt=SALT.encode('utf-8'),
                              iterations=100000)
    return key.hex()
