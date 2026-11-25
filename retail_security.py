
from argon2 import PasswordHasher, Type
from argon2.exceptions import VerificationError, InvalidHashError

retail_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
    type=Type.ID
)


def hash_user_pwd(user_pwd):
    return retail_hasher.hash(user_pwd)


def verify_user_pwd(user_pwd, user_pwd_hash):
    try:
        return retail_hasher.verify(user_pwd_hash, user_pwd)
    except (VerificationError, InvalidHashError):
        return False
