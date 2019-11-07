#include <stdio.h>

int main(){
    const unsigned int MAX = 5;
    int brut[MAX];
    int compress[MAX];

    int i = 0, val = 0;
    printf("Entrez les valeurs : \n");
    for(i = 0; i<MAX; i++){
        
        scanf("%d", &val);
        brut[i] = val;

    }
    for(i = 0 ; i<MAX; i++){
        val = brut[i];
        printf("%d", val);
    }
}