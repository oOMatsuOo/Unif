#include <stdio.h>

int main(){

    unsigned int a = 1, b = 1, c = 1;

    printf("Entrer un nombre : \n");
  
    scanf("%d", &a);

    while (b <= a)
    {
        c = c * b;
        b ++;
    }
    printf("La !%d est : %d\n", a, c);

}