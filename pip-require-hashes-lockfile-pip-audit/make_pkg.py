"""무해한 연습용 패키지의 휠(.whl)을 만든다.

사용법: python make_pkg.py 이름 버전 "출력할 문장" 출력폴더
같은 이름과 버전이라도 문장을 바꾸면 내용이 다른 휠이 만들어진다.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

name, version, message, out = sys.argv[1:5]

with tempfile.TemporaryDirectory() as tmp:
    src = Path(tmp)
    (src / name).mkdir()
    (src / name / "__init__.py").write_text(
        f'__version__ = "{version}"\n\n\ndef hello():\n    return "{message}"\n',
        encoding="utf-8",
    )
    (src / "pyproject.toml").write_text(
        '[build-system]\nrequires = ["setuptools"]\nbuild-backend = "setuptools.build_meta"\n\n'
        f'[project]\nname = "{name}"\nversion = "{version}"\n',
        encoding="utf-8",
    )
    Path(out).mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [sys.executable, "-m", "pip", "wheel", "--disable-pip-version-check", "--no-deps", "--no-build-isolation", "-q", "-w", out, str(src)],
        check=True,
    )
    shutil.rmtree(src / "build", ignore_errors=True)
print(sorted(p.name for p in Path(out).glob(f"{name}-{version}*.whl")))
