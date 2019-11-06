#include <stdio.h>

int main(){
    int f = 0, c = 0;

    printf("Entrez une valeur en Fahrenheit : ");

    scanf("%d", &f);

    c = 0.555556 * (f - 32);

    printf("Sa valeur en degré : %d\n", c);
}
