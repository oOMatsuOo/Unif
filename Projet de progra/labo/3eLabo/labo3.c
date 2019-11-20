#include "/home/kieranvm/Downloads/Unif/Projet\ de\ progra/labo/util/util.h"
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

   // Imprime sur la sortie standard le contenu du tableau
   afficher_vecteur(vecteur , n);
   printf("%d %d\n", min , max);

   return 0;
}// fin programme