#include <stdio.h>

int main(){
    
    const unsigned int N = 5;
    int n = 100, i = 0, j = 1, carre = 0, pal = 0, k = 0, compteur = 0;
    int carreV[N];

    while (i<n){
        carre = i * i;
        compteur = 0;

        printf("%d  %d ", carre,i);

        for(k = carre;k>0;){
            carreV[compteur] = (carre%10);
            k -= k%10;
            k /= 10;
            compteur ++;
        }

        pal = 0;

        for(j=N-1; j>0;){
            while(carreV[j] == 0){
                j--;
            }

            printf("%d  %d \n", carreV[pal], carreV[j]);
            if(carreV[pal] == carreV[j]){
                if(pal < j - 1 || pal < j - 2){
                    pal ++;
                    -- j;
                }else{
                    printf("OUIIIII %d\n", carre);
                    --j ;
                }
            }
        }        
        
    i++;
    }
}