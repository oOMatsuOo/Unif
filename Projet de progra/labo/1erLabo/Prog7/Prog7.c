#include <stdio.h>

int main(){

    int a = 0, b = 0, c = 0, moyenne;

    do{
        printf("Entrer une note : \n");
        scanf("%d", &a);

        if(a != -1 ){

            b += a;
            c ++;
        }

    }while(a != -1);

    moyenne = b / c;

    printf("La moyenne de vos notes : %d\n", moyenne);
}
