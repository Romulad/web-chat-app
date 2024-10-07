from passlib.context import CryptContext

passw_hasher = CryptContext(schemes=["bcrypt", "pbkdf2_sha256"], deprecated="auto")


def hash_passord(password: str):
    return passw_hasher.hash(password)

def verify_password(password, hash):
    return passw_hasher.verify(password, hash)