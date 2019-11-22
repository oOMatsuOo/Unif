#include "/home/kieranvm/Documents/Unif/Projet de progra/labo/util/util.h"

int main (){
   int **matrice ;
   int n ;

   printf("Entrez une valeur pour n :\n");
   scanf("%d", &n);

   remplir_matrice_zeros(&matrice, n);

   // AJOUTER VOTRE CODE ICI

    int compteur = 1, carre_actuel = 1,x = 0, y = 0, i = 1, carre_parfait = 0;

    y = n / 2 - 1;

    if(n%2 == 0){
        x = -1 + n/2;
    }else{
        x = n / 2;
    }

    printf("X  : %d",x);
    printf("Y  : %d\n",y);

    while (compteur <= n*n){
        //matrice[1] = compteur;
        //printf("matrice  : %d ",matrice[y][x]);
        printf("compteur : %d | ",compteur);

        for(i = 1; i <= n; i++){
            if (compteur / i == i && compteur % i == 0){
                carre_parfait = 1;
                i = n + 1;
                printf("%d",i);
            }else
                carre_parfait = 0;
        }

        if(carre_parfait ){
            carre_actuel += 1;
        }
        if (carre_actuel % 2 == 0){
            x += 1;
            if(compteur < (carre_actuel * carre_actuel) - (carre_actuel - 1)){
                y += 1;
            }else{
                x -= 1;
            }
        }else{
            x -= 1;
            if(compteur < (carre_actuel * carre_actuel) - (carre_actuel - 1)){
                y -= 1;
            }else{
                x += 1;
            }
        }
        printf("x  : %d | y  : %d | ",x,y);
        if (carre_parfait){
            printf("Carré Parfait !\n");
        }else
            printf("\n");

        compteur += 1;
    }



   // Affiche le tableau
   afficher_matrice(matrice , n);

   return 0;
}// fin programme
