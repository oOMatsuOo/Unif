#include <stdio.h>

int main(){

    int n = 100, i = 0, j = i, carre = 1, pal = 0;

    while(i<n){
        carre = i * i;
        pal = 0;
        for(j = carre;j>0;){
            pal *= 10;
            pal += (j % 10);
            j -= (j%10);
            j /= 10;
        }

        if(carre == pal){
            printf("%d\n", carre);
        }
        i++;
    }

}