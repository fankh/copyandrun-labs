import hashlib
import subprocess


def ping(host):
    return subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True)


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()
