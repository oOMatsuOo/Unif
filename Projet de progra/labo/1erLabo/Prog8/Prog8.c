#include <stdio.h>

int main(){

    int a = 0, b = 0;
    float c = 0.5;

    printf("Voulez-vous :\n 1 - Déterminer si une année est bisexstille ou non\n 2 - Décomposez un entier en puissance de 2\n 3 - Calculer la racine carrée d'un nombre\n");

    scanf("%d", &a);

    if(a == 1){
        printf("Quelle est l'année ?\n");
        scanf("%d", &b);

        if(b%4 == 0){
            if(b%100 == 0){
                if(b%400 == 0){
                    printf("%d est une année bisexstille.\n", b);
                }else{
                    printf("%d n'est pas une année bisexstille.\n", b);
                };
            }else{
                printf("%d est une année bisexstille.\n", b);
            };
        };
    }else if(a == 2){
        printf("Quel est votre entier ?\n");
        scanf("%d", &b);

        while(b > 0){
            c = c * 2;

            printf("%f ", c);

            b -= c;
            
        };
    }else if(a == 3){

    }
}