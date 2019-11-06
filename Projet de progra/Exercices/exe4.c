#include <stdio.h>

int main(){
    int i = 0, n = 0, f = 1;

    printf("Entrez une valeur : ");
    scanf("%d", &n);

    if(n > 1){
        for(i = 1; i <= n; i++){
            f *= i;
        }
    }

    printf("La factorielle de %d est : %d\n", n, f);
}