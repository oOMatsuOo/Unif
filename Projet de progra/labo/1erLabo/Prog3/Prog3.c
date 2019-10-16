#include <stdio.h>

int main(){

    int a = 0, b = 0;

    printf("Entrer un nombre : \n");
  
    scanf("%d", &a);

    b = a % 2;

    if(b)
        printf("Votre nombre est impair.\n");
    else
        printf("Votre nombre est pair.\n");
}