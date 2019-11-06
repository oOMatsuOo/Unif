#include <stdio.h>

int main(){
    int i = 0, n = 0, s = 0;

    printf("Entrez une valeur : ");
    scanf("%d", &n);

    for(i = 1; i <= n; i++){
        s += i*i*i;
    };

    printf("Le résulat : %d\n", s);
}