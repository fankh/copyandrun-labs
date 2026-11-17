import hashlib
import os
import shlex
import subprocess

import requests
from flask import request

from helpers import safe_run


def find_user(db, name):
    return db.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()


def find_order(db, order_id):
    return db.execute("SELECT * FROM orders WHERE id = ?", (int(order_id),)).fetchall()


def hash_password(password, salt):
    return hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1).hex()


def fetch_report(url):
    return requests.get(url, timeout=5).text


def ping():
    host = request.args.get("host")
    return os.system("ping -c 1 " + shlex.quote(host))


def backup(path):
    return subprocess.run(["tar", "czf", "/tmp/backup.tgz", path], check=True)


def cleanup(cmd):
    return safe_run(cmd)
