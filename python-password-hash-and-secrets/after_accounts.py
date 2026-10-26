import os

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from dotenv import load_dotenv

load_dotenv()

ph = PasswordHasher()
DUMMY_HASH = ph.hash("not-a-real-password")
users = {}


def open_db(host, password):
    return {"host": host, "password": password}


def sign_up(name, password):
    users[name] = ph.hash(password)


def log_in(name, password):
    stored = users.get(name)
    try:
        ph.verify(stored or DUMMY_HASH, password)
    except (VerifyMismatchError, InvalidHashError):
        return False
    if stored is None:
        return False
    if ph.check_needs_rehash(stored):
        users[name] = ph.hash(password)
    return True


db = open_db("db.example.test", password=os.environ["DB_PASSWORD"])
