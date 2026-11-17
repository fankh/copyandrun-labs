# 이미 내려받아 둔 로컬 모델에게 한 줄을 설명시키고 답을 그대로 출력합니다.
# 사용법: python -X utf8 ask_ai.py qwen2.5:3b samples/sample2.txt
# Ollama 가 든 컨테이너 이름은 환경 변수 OLLAMA_CONTAINER 로 지정합니다(기본값 ollama).
import os, re, subprocess, sys

model, path = sys.argv[1], sys.argv[2]
container = os.environ.get("OLLAMA_CONTAINER", "ollama")
code = open(path, encoding="utf-8").read().strip()
prompt = "다음 PowerShell 한 줄이 하는 일을 한국어로 세 문장 이내로 설명하세요.\n\n" + code
p = subprocess.run(["docker", "exec", "-i", container, "ollama", "run", "--nowordwrap", model],
                   input=prompt, capture_output=True, text=True, encoding="utf-8")
out = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", p.stdout)   # 화면 제어 문자 제거
out = re.sub(r"[⠀-⣿]", "", out)                # 진행 표시 점자 문자 제거
print(out.strip())
