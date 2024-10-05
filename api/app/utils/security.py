from passlib.hash import pbkdf2_sha256


def hash_passord(password: str):
    return pbkdf2_sha256.hash(password)

def verify_password(password, hash):
    return pbkdf2_sha256.verify(password, hash)