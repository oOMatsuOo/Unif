#include <stdio.h>

int main(){
    int i = 0, n = 0, ui0 = 0, ui1 = 1, ui = 0;

    printf("Entrez une valeur : ");
    scanf("%d", &n);

    if(n >= 2){
        for(i = 2; i <= n; i++){
            ui = ui1 + ui0;
            ui0 = ui1;
            ui1 = ui;
            
        }
    }

    printf("La suite de Fibonacci pour n =  %d est : %d\n", n, ui);
}