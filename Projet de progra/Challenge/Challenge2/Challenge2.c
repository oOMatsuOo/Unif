#include <stdio.h>

int main(){
    
    unsigned int V = 16, H = 20, k = 1, b = 1;
    char C1 = '&', C2 = ' ';

    while(k <= V){
        b = 1;
        while(b <= H){
            if(k <= V/2){
                if(b <= (H/2))
                    printf("%c", C1);
                else
                    printf("%c", C2);
                b ++;
            }else{
                if(b <= (H/2))
                    printf("%c", C2);
                else
                    printf("%c", C1);
                b ++;
            }
        }
        k ++;
        printf("\n");
    }
}