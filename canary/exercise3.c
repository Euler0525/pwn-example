#include<stdio.h>
#include<string.h>

void System() {
    system("/bin/sh");
}

void init() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
}

void GoLiangXiang() {
    char book[100];
    for (int i = 0; i < 2; i++) {
        read(0, book, 0x200);
        printf(book);
    }
}

int main() {
    init();
    GoLiangXiang();
    return 0;
}

