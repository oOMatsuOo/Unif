#include "/home/kieranvm/Documents/Unif/Projet de progra/labo/util/util.h"
#include <stdio.h>

int main (){

   int *vecteur;
   int n;
   int min;
   int max;

   printf("Entrez une valeur pour n :\n");
   scanf("%d", &n);

   // Remplit le tableau avec des valeurs alé atoires
   remplir_vecteur(&vecteur , n);

   // AJOUTER VOTRE CODE ICI

   int k = n - 1, j = 0,compteur=0, max_comp = 0;
   min = 99;
   max = 0;

   for(j = 0; j + 1 < k; j++){
      if(vecteur[j] > vecteur[k]){
         if(vecteur[j] > max)
            max = vecteur[j];
         if(vecteur[k] < min)
            min = vecteur[k];
      }else{
         if(vecteur[j] < min)
            min = vecteur[j];
         if(vecteur[k] > max)
            max = vecteur[k];
      }
      k -= 1;
      compteur += 3;
   }

   if (k == j){
      if(vecteur[j] > vecteur[k]){
         if(vecteur[j] > max)
            max = vecteur[j];
         if(vecteur[k] < min)
            min = vecteur[k];
      }else{
         if(vecteur[j] < min)
            min = vecteur[j];
         if(vecteur[k] > max)
            max = vecteur[k];
      }
      compteur += 3;
   }

   max_comp = 3 * n / 2;
   compteur += 1;

   // Imprime sur la sortie standard le contenu du tableau
   afficher_vecteur(vecteur , n);
   printf("%d %d\n", min , max);

   printf("%d %d\n", max_comp, compteur);

   return 0;
}// fin programme