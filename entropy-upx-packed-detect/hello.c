/* 시험용 무해한 프로그램: 문자열 표를 만들어 합계만 출력합니다. 실행하지 않고 분석 도구로 열기만 합니다. */
#include <stdio.h>
#include <string.h>

static const char *NOTES[] = {
    "alpha: this is a harmless sample used for entropy comparison.",
    "bravo: it only prints a checksum of a small text table.",
    "charlie: nothing is written to disk and no network is used.",
    "delta: the strings are plain English so they compress well.",
    "echo: packers shrink such text and raise the entropy.",
};

static unsigned int checksum(const char *s) {
    unsigned int h = 5381;
    while (*s) h = h * 33 + (unsigned char)*s++;
    return h;
}

int main(void) {
    unsigned int total = 0;
    for (int round = 0; round < 3; round++)
        for (size_t i = 0; i < sizeof(NOTES) / sizeof(NOTES[0]); i++)
            total += checksum(NOTES[i]) + (unsigned int)strlen(NOTES[i]);
    printf("checksum=%u\n", total);
    return 0;
}
