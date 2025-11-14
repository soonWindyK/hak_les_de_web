import hashlib

def hash_pass(password):
    hasher = hashlib.sha256()
    hasher.update(password.encode('utf-8'))
    hashed_value = hasher.hexdigest()
    return hashed_value