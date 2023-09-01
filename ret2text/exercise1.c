#include<stdio.h>

void System() {
    system("/bin/sh");
}

void GoLiangXiang() {
    char book[10] = { 0 };
    read(0, book, 100);
    return;
}

int main() {
    GoLiangXiang();
    return 0;
}
