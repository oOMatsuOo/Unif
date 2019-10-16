#include <stdio.h>

int main(){

    int a = 0, b = 0, c = 0;

    printf("Entrer deux nombres : \n");
  
    scanf("%d", &a);
    scanf("%d", &b);

    c = a;

    if(c < b)
        c = b;
    
    printf("Le plus grand de vos deux nombres est : %d \n", c);
}