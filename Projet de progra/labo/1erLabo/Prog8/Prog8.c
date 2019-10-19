#include <stdio.h>

int main(){

    int a = 1;

    while(a != 0){

        int b = 0, c = 1, d = 0, i = 0, j = 0, f = 0;

        printf("Voulez-vous :\n 1 - Déterminer si une année est bisexstille ou non\n 2 - Décomposez un entier en puissance de 2\n 3 - Calculer la racine carrée d'un nombre\n 0 - Quitter\n");

        scanf("%d", &a);

        if(a == 1){
            printf("\nEntrer une année : ");
            scanf("%d", &b);

            if(b%4 == 0){
                if(b%100 == 0){
                    if(b%400 == 0){
                        printf("\n%d est une année bisexstille.\n \n", b);
                    }else{
                        printf("\n%d n'est pas une année bisexstille.\n \n", b);
                    };
                }else{
                    printf("\n%d est une année bisexstille.\n \n", b);
                };
            }else{
                printf("\n%d n'est pas une année bisexstille.\n \n", b);
            };
        }else if(a == 2){
            printf("\nEntrer un entier : ");
            scanf("%d", &b);

            printf("\nLes puissances de 2 qui composent %d sont : \n", b);
            d = b;

            while(d > 0){
                f = 0;
                c = 1;
                for(i=d; i>1; ){
                    f++;
                    i = i / 2;
                }
                for(j=f; j>0; j--){
                    c *= 2;
                }
                printf("%d\n", c);

                d -= c;

                if(d == 0)
                    printf("\n");

            };
        }else if(a == 3){
            float carre1 = 0, carre2 = 0, m = 0, k = 0, o = 0, limite = 20, x = 1;
            int entier = 0;

            printf("\nEntrer un entier : ");
            scanf("%d", &entier);

            printf("\nLa racine carrée de %d, au centième près est : ", entier);

            // Premier carré parfait inférieure à N 

            for(m = entier; m > 0; m--){
                for(k = m ; k > 0 ; k--){ 
                    if(k * k == m){ 
                        carre1 = k;
                        m = 0;
                        k = 0;
                    }
                }; 
            }; 

            carre2 = carre1 + 1;

            for(o = 0; o < limite; o++){
                x = carre1 + ((carre2 - carre1) / 2);

                if((x * x) < entier){
                    carre1 = x;
                }else if((x * x) >= entier){
                    carre2 = x;
                }
            }
            printf("%f\n", x);
            printf("\n");
        }      
    }
}