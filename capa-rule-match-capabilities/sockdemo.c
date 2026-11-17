/* 시험 프로그램 (c): 소켓 연결 코드가 들어 있다.
 * 명령줄 인자가 정확히 99개일 때만 연결 함수를 부르므로 보통은 도달하지 않는다.
 * 주소는 127.0.0.1 이다. 실행하지 않고 분석만 한다. */
#include <winsock2.h>
#include <ws2tcpip.h>
#include <string.h>

static int try_connect(void) {
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) return -1;
    SOCKET s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (s == INVALID_SOCKET) return -2;
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(9);
    addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    int rc = connect(s, (struct sockaddr *)&addr, sizeof(addr));
    if (rc == 0) send(s, "hello", 5, 0);
    closesocket(s);
    WSACleanup();
    return rc;
}

int main(int argc, char **argv) {
    (void)argv;
    if (argc == 99) return try_connect();
    return 0;
}
