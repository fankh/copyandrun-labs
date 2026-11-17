/* 분석용 시험 프로그램입니다. 실행해도 화면에 한 줄 출력하는 일만 합니다.
   아래 분기는 argc가 3일 때(프로그램 이름 포함 인자 3개)만 도달하며, 내용은 모두 무해한 호출입니다. */
#include <windows.h>
#include <wininet.h>
#include <stdio.h>

static void probe_calls(void)
{
    /* 존재하지 않는 시험용 파일을 읽기 모드로 여는 호출 */
    HANDLE h = CreateFileA("C:\\no_such_dir\\demo.txt", GENERIC_READ, 0, NULL,
                           OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (h != INVALID_HANDLE_VALUE) CloseHandle(h);

    /* 계산기가 아니라 빈 문자열 명령 */
    WinExec("", SW_HIDE);

    /* 인터넷 세션 핸들만 열고 바로 닫음. 접속은 하지 않음 */
    HINTERNET s = InternetOpenA("demo-agent", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (s) InternetCloseHandle(s);
}

int main(int argc, char **argv)
{
    (void)argv;
    if (argc == 3) {
        probe_calls();
    }
    printf("hello from demo\n");
    return 0;
}
