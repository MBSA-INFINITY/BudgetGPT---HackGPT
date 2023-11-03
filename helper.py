import hashlib
def hash_generator(text):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(text.encode('utf-8'))
    hashed_text = hash_algorithm.hexdigest()
    return hashed_text