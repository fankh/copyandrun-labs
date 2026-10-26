import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

ALLOWED_READ_DIRS = [os.path.realpath("workspace/allowed")]
ALLOWED_WRITE_DIRS = [os.path.realpath("workspace/output")]
MAX_FILE_SIZE = 512 * 1024


def vuln_read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    except OSError as e:
        return f"오류: {e}"


def vuln_write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"저장 완료: {path}"


def check_path(path, allowed_dirs, action):
    real = os.path.realpath(path)
    if not any(real == d or real.startswith(d + os.sep) for d in allowed_dirs):
        raise PermissionError(f"{action} 허용되지 않은 경로: {path}")
    return real


def secure_read(path):
    try:
        real = check_path(path, ALLOWED_READ_DIRS, "읽기")
        if os.path.getsize(real) > MAX_FILE_SIZE:
            return "파일이 너무 큽니다"
        with open(real, encoding="utf-8") as f:
            return f.read().strip()
    except PermissionError as e:
        return f"[차단] {e}"
    except OSError as e:
        return f"오류: {e}"


def secure_write(path, content):
    try:
        real = check_path(path, ALLOWED_WRITE_DIRS, "쓰기")
        with open(real, "w", encoding="utf-8") as f:
            f.write(content)
        return f"저장 완료: {os.path.relpath(real)}"
    except PermissionError as e:
        return f"[차단] {e}"
    except OSError as e:
        return f"오류: {e}"


CASES = [
    ("read", "workspace/allowed/readme.txt", None),
    ("read", "workspace/forbidden/secret.txt", None),
    ("read", "workspace/allowed/../forbidden/secret.txt", None),
    ("write", "workspace/output/result.txt", "정상 출력"),
    ("write", "workspace/forbidden/evil.txt", "덮어쓰기 시도"),
]

if __name__ == "__main__":
    for op, path, content in CASES:
        print(f"[{op}] {path}")
        if op == "read":
            print("  취약:", vuln_read(path))
            print("  보안:", secure_read(path))
        else:
            print("  취약:", vuln_write(path, content))
            print("  보안:", secure_write(path, content))
