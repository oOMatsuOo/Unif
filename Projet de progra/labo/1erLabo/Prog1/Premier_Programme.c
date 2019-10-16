#include <stdio.h>

int main()
{
   int a = 0, i ;
  
   printf("Entrez un nombre entier : ");
  
   scanf("%d", &a);
     
   for(i = 0; i < a; i++){
  
     if(!(a%10))
        printf("%d! ", i);
     else if(!(a%5))
        printf("%d ", i);
      
   printf("\n");
  
   return 0;
   }
}
