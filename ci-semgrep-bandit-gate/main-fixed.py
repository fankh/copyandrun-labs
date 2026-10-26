import hashlib
import subprocess


def ping(host):
    return subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True)


def hash_password(password, salt):
    return hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1).hex()
