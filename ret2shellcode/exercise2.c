#include<stdio.h>
#include<string.h>

void GoLiangXiang() {
    char book[100] = { 0 };
    printf("Now you may have this: [%p]\n", book, 0, 0);
    read(0, book, 200);
    return;
}

int main() {
    GoLiangXiang();
    return 0;
}

