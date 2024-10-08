import datetime

import jwt
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError

from ..configs import settings
from ..settings import TOKEN_EXPIRATION_TIME, TOKEN_ALGORITHM

passw_hasher = CryptContext(schemes=["bcrypt", "pbkdf2_sha256"], deprecated="auto")


def hash_passord(password: str):
    return passw_hasher.hash(password)


def verify_password(password, hash):
    return passw_hasher.verify(password, hash)


def create_user_token(user_id: str):
    secret = settings.secret_key
    expiration_datetime = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=TOKEN_EXPIRATION_TIME)
    payload = {"sub": user_id, "exp": expiration_datetime}
    return jwt.encode(payload, secret, algorithm=TOKEN_ALGORITHM)


def validate_user_token(token: str):
    """Check token validity and return the user id or None"""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[TOKEN_ALGORITHM]
        )
        return payload.get('sub')
    except InvalidTokenError:
        return None