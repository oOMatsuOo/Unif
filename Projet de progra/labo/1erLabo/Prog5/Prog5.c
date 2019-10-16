#include <stdio.h>

int main(){

    int a = 7, m = 1, n = 0;

    while(m <= 30){
        n = a * m;
        printf("%d\n",n);
        m ++;
    }
}