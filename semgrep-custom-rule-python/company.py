# 규칙 시험 파일: semgrep --test 가 규칙 파일과 이름이 같은 이 파일을 읽는다.
# 주석 표시가 붙은 바로 다음 줄은 걸려야 하는 줄, ok 표시가 붙은 바로 다음 줄은 걸리면 안 되는 줄이다.
import hashlib
import os
import shlex
import subprocess

import requests
from flask import request

from helpers import run_shell


def sql(db, name, n):
    # ruleid: company-sql-string-built
    db.execute(f"SELECT * FROM t WHERE a = '{name}'")
    # ruleid: company-sql-string-built
    db.execute("SELECT * FROM t WHERE a = " + n)
    # ruleid: company-sql-string-built
    db.execute("SELECT * FROM t WHERE a = {}".format(n))
    # ok: company-sql-string-built
    db.execute("SELECT * FROM t WHERE a = ?", (name,))


def tls(url):
    # ruleid: company-tls-verify-false
    requests.get(url, verify=False)
    # ok: company-tls-verify-false
    requests.get(url, timeout=5)


def hashing(p):
    # ruleid: company-weak-password-hash
    hashlib.md5(p)
    # ruleid: company-weak-password-hash
    hashlib.sha1(p)
    # ok: company-weak-password-hash
    hashlib.sha256(p)


def taint():
    host = request.args.get("host")
    # ruleid: company-os-command-taint
    os.system("ping " + host)
    # ok: company-os-command-taint
    os.system("ping " + shlex.quote(host))
    # ok: company-os-command-taint
    os.system("ping 127.0.0.1")


def shell(path):
    # ruleid: company-subprocess-shell-true
    subprocess.run("ls " + path, shell=True)
    # ok: company-subprocess-shell-true
    subprocess.run(["ls", path])


def internal(cmd):
    # ruleid: company-no-run-shell
    run_shell(cmd)
    # ok: company-no-run-shell
    safe_run(cmd)
