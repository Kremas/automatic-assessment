#include "calc.h"
#include <stdlib.h>
#include <string.h>

int add(int a, int b) {
    return a + b;
}

int sub(int a, int b) {
    return a - b;
}

int mul(int a, int b) {
    return a * b;
}

float divide(int a, int b) {
    return (float) a / b;
}

int max(int a, int b) {
    return (a > b) ? a : b;
}

char* concat(const char* a, const char* b) {
    char* result = malloc(strlen(a) + strlen(b) + 1);
    strcpy(result, a);
    strcat(result, b);
    return result;
}
