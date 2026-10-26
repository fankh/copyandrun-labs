import hashlib

DB_PASSWORD = "Sup3rS3cret!"
SECRET_TOKEN = "tok_FAKE_0123456789abcdef"

users = {}


def open_db(host, password="Sup3rS3cret!"):
    return {"host": host, "password": password}


def sign_up(name, password):
    users[name] = hashlib.md5(password.encode()).hexdigest()


def log_in(name, password):
    return users.get(name) == hashlib.md5(password.encode()).hexdigest()


db = open_db("db.example.test", password="Sup3rS3cret!")
