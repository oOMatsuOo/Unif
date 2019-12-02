#include <stdio.h>

int est_premier(unsigned int x){
    unsigned int est_premier = 1, i = 2;

    for(i = 2; i < x; i++){
        if((x % i) == 0){
            est_premier = 0;
            i = x;
        };
    };

    return est_premier;
}

int sont_jumeaux(unsigned int p, unsigned int n){
    unsigned int reponse = 0, difference = 0;

    difference = p - n;

    if(difference == 2 && est_premier(p) && est_premier(n)){
        reponse = 1;
    };

    return reponse;
}

void affiche_jumeaux(unsigned int x){
    unsigned int jum1 = 2, jum2 = 2, i = 2, premier = 0;

    for(i = 2; i <= x; i++){

        if(est_premier(i)){
            jum2 = i;
            premier = 1;
        };
        
        if(sont_jumeaux(jum2,jum1))
            printf("%d %d\n",jum1,jum2);

        if(premier == 1)
            jum1 = jum2;

        premier = 0;
    };

}



int main(){
    unsigned int nombre;

    printf("Entrez un nombre : \n");
    scanf("%d", &nombre);

    affiche_jumeaux(nombre);

}