import hashlib
import os
import subprocess

import requests
from flask import request

from helpers import run_shell


def find_user(db, name):
    return db.execute(f"SELECT * FROM users WHERE name = '{name}'").fetchall()


def find_order(db, order_id):
    return db.execute("SELECT * FROM orders WHERE id = " + order_id).fetchall()


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def fetch_report(url):
    return requests.get(url, verify=False, timeout=5).text


def ping():
    host = request.args.get("host")
    return os.system("ping -c 1 " + host)


def backup(path):
    return subprocess.run(f"tar czf /tmp/backup.tgz {path}", shell=True)


def cleanup(cmd):
    return run_shell(cmd)
