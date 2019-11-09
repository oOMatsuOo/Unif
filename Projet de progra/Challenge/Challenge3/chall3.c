#include <stdio.h>

int main(){
    const unsigned int MAX = 30;
    int brut[MAX];
    int compress_tab[MAX];

    int i = 0, val = 0;
    printf("Entrez les valeurs : \n");
    for(i = 0; i<MAX-1; i++){
        
        scanf("%d", &val);
        brut[i] = val;

    }

    brut[MAX-1] = -1;

    for(i = 0 ; i<MAX; i++){
        val = brut[i];
        printf("%d", val);
    }
    printf("\n");

    int f = 0, k = 0, j = 0, compteur = 1;

    while(k < MAX){
        if(brut[k] == -1 && k == 0){
            compress_tab[j] = brut[k];
            k = MAX;
        }else if (brut[k] == -1){
            if(compteur == 1){
                compress_tab[j] = brut[f];
                compress_tab[j+1] = brut[k];
                k = MAX;
            }else{
                compress_tab[j] = compteur;
                compress_tab[j+1] = brut[f];
                compress_tab [j+2] = brut[k];
                k = MAX;
            }
        }else{
            k ++;
        }
        //printf("f : %d  k : %d  brut[f] : %d  brut[k] : %d  ", f, k, brut[f], brut[k]);

        if(brut[k] != -1){
            if(brut[f] == brut[k]){
                compteur ++;
                f ++;
            }else if(compteur == 1){
                compress_tab[j] = brut[f];
                j ++;
                f ++;
            }else{
                compress_tab[j] = compteur;
                compress_tab[j+1] = brut[f];
                j += 2;
                compteur = 1;
                f ++;
            }
        }
        //printf("compteur : %d  j : %d\n", compteur,j);
    }
    for(i = 0 ; i<MAX; i++){
        val = compress_tab[i];
        printf("%d", val);
    }

}