import sys

import pefile

# 분석 단서로 자주 거론되는 함수 이름과 그 의미. 이름만으로 악성을 판정하는 목록이 아닙니다.
CLUES = {
    "CreateFileA": "파일 열기 또는 만들기",
    "CreateFileW": "파일 열기 또는 만들기",
    "WinExec": "다른 프로그램 실행",
    "InternetOpenA": "인터넷 세션 열기(네트워크 사용 가능성)",
    "InternetOpenW": "인터넷 세션 열기(네트워크 사용 가능성)",
    "VirtualAlloc": "메모리 영역 할당",
    "CreateProcessA": "프로세스 생성",
}

pe = pefile.PE(sys.argv[1])
found = []
for entry in pe.DIRECTORY_ENTRY_IMPORT:
    for imp in entry.imports:
        if imp.name and imp.name.decode() in CLUES:
            found.append((entry.dll.decode(), imp.name.decode()))

for dll, fn in found:
    print(f"{dll:14} {fn:14} {CLUES[fn]}")
print("단서 함수 수:", len(found))
