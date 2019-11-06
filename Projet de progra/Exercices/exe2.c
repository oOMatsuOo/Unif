#include <stdio.h>

int main(){
    int a = 0, i = 0, b = 0, h = 0, d = 0;

    printf("Entrez une valeur pour le calcul de l'image : ");

    scanf("%d", &a);

    i = (2 * a + 3) * (3 * a * a + 2);

    printf("L'image de %d par la fonction est : %d\n", a, i);

    printf("Entrez les deux valeurs pour le calcul de la dérivée ( x et h) : ");

    scanf("%d", &b);
    scanf("%d", &h);

    d = ((2 * (b + h) + 3) * (3 * (b + h) * (b + h) + 2) - (2 * h + 3) * (3 * h * h + 2) ) / h;

    printf("L'image de %d par la fonction est : %d\n", b, d);

}