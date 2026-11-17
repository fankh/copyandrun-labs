/* 문자열 추출 시험용 프로그램. 네트워크 접속이나 파일 쓰기를 하지 않고 화면에 글자만 출력한다.
   이 글에서는 컴파일만 하고 실행하지 않는다. */
#include <stdio.h>
#include <string.h>
#include <wchar.h>

/* 1. 평문 문자열 */
static const char *PLAIN_URL = "http://plain.example.com/update/check";
static const char *PLAIN_PATH = "C:\\Users\\alice\\AppData\\Roaming\\DemoAgent\\config.dat";
static const char *PLAIN_KEY = "Software\\DemoCorp\\Agent\\Settings";

/* 2. UTF-16LE 로 저장되는 문자열 */
static const wchar_t *WIDE_LOG = L"C:\\Temp\\demo-agent.log";

/* 3. 인코딩한 문자열: XOR 키 0x5A 와 base64 */
static const unsigned char XOR_DATA[] = {
    0x32, 0x2e, 0x2e, 0x2a, 0x60, 0x75, 0x75, 0x22, 0x35, 0x28, 0x74, 0x3f,
    0x22, 0x3b, 0x37, 0x2a, 0x36, 0x3f, 0x74, 0x39, 0x35, 0x37, 0x75, 0x3b
};
static const char *B64_DATA = "aHR0cDovL2I2NC5leGFtcGxlLmNvbS9j";

static void xor_decode(const unsigned char *in, int n, char *out) {
    for (int i = 0; i < n; i++) out[i] = (char)(in[i] ^ 0x5A);
    out[n] = '\0';
}

static int b64_value(char c) {
    const char *t = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    const char *p = strchr(t, c);
    return p ? (int)(p - t) : -1;
}

static void b64_decode(const char *in, char *out) {
    int n = 0, bits = 0, acc = 0;
    for (; *in && *in != '='; in++) {
        acc = (acc << 6) | b64_value(*in);
        bits += 6;
        if (bits >= 8) { bits -= 8; out[n++] = (char)((acc >> bits) & 0xFF); }
    }
    out[n] = '\0';
}

int main(void) {
    char xor_out[64], b64_out[64];

    /* 4. 실행 중에 한 글자씩 조립하는 문자열(스택 문자열) */
    char stack_url[32];
    stack_url[0] = 'h'; stack_url[1] = 't'; stack_url[2] = 't'; stack_url[3] = 'p';
    stack_url[4] = ':'; stack_url[5] = '/'; stack_url[6] = '/';
    stack_url[7] = 's'; stack_url[8] = 't'; stack_url[9] = 'a'; stack_url[10] = 'c';
    stack_url[11] = 'k'; stack_url[12] = '.'; stack_url[13] = 'e'; stack_url[14] = 'x';
    stack_url[15] = 'a'; stack_url[16] = 'm'; stack_url[17] = 'p'; stack_url[18] = 'l';
    stack_url[19] = 'e'; stack_url[20] = '.'; stack_url[21] = 'c'; stack_url[22] = 'o';
    stack_url[23] = 'm'; stack_url[24] = '/'; stack_url[25] = 'b'; stack_url[26] = '\0';

    xor_decode(XOR_DATA, (int)sizeof(XOR_DATA), xor_out);
    b64_decode(B64_DATA, b64_out);

    printf("%s\n%s\n%s\n", PLAIN_URL, PLAIN_PATH, PLAIN_KEY);
    wprintf(L"%ls\n", WIDE_LOG);
    printf("%s\n%s\n%s\n", xor_out, b64_out, stack_url);
    return 0;
}
