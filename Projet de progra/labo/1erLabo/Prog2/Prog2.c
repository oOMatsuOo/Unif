#include <stdio.h>

int main(){

    int a = 0, b = 0, s = 0, p = 0;

    printf("Entrer deux nombre : \n");
  
    scanf("%d", &a);
    scanf("%d", &b);

    s = a + b;
    p = a * b;

    printf("Le produit est : %d\n", p);
    printf("La somme est : %d\n", s);

}