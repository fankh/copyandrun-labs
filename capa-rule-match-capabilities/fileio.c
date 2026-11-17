/* 시험 프로그램 (b): 파일을 읽고 다른 파일에 쓴다. 실행하지 않고 분석만 한다. */
#include <stdio.h>
#include <string.h>

int main(void) {
    char buf[256];
    FILE *in = fopen("input.txt", "rb");
    if (!in) return 1;
    size_t n = fread(buf, 1, sizeof(buf), in);
    fclose(in);

    FILE *out = fopen("output.txt", "wb");
    if (!out) return 2;
    fwrite(buf, 1, n, out);
    fclose(out);
    return 0;
}
