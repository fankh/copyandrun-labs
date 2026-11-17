from evtx_tree import classify

# 직접 만든 시험 값입니다. 실제 로그가 아니라 규칙이 어떻게 판정하는지만 확인합니다.
CASES = [
    ("정상 경로 WINWORD 가 powershell 실행", r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE", r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"),
    ("정상 경로 EXCEL 이 메모장 실행", r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE", r"C:\Windows\System32\notepad.exe"),
    ("사용자 폴더의 WINWORD 가 cmd 실행", r"C:\Users\kim\AppData\Roaming\WINWORD.EXE", r"C:\Windows\System32\cmd.exe"),
    ("탐색기가 cmd 실행", r"C:\Windows\explorer.exe", r"C:\Windows\System32\cmd.exe"),
    ("정상 경로 OUTLOOK 이 rundll32 실행", r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE", r"C:\Windows\System32\rundll32.exe"),
]
for name, parent, child in CASES:
    print(name, "->", ", ".join(classify(parent, child)) or "표시 없음")
