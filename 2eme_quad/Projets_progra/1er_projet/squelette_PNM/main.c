/**
 * main.c
 * 
 * Ce fichier contient la fonction main() du programme de manipulation
 * de fichiers pnm.
 *
 * @author: Nom Prenom Matricule
 * @date: 
 * @projet: INFO0030 Projet 1
 */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>
#include <ctype.h>
#include <getopt.h>

#include "pnm.h"


int main(int argc, char *argv[]) {

   char *optstring = "";

   char extension[4];
   char nom_fichier[40];

   strcpy(extension, argv[2]);
   strcpy(nom_fichier, argv[3]);

   printf("%s \n", extension);
   printf("%s \n", nom_fichier);

   int test_extension_retour;

   test_extension_retour = test_extension(extension,nom_fichier);

   if (test_extension_retour == -3){
      printf("%s \n", "Mauvaise extension du fichier renseigné.");
   }
   else if(test_extension_retour == -1){
      printf("%s \n", "Mauvaise extension renseignée.");
   }
   else if(test_extension_retour == -2){
      printf("%s \n", "L'extension du fichier est différente de celle renseignée.");
   }
   else{
      printf("%s \n","Le formatage est bon.");
   }

   return 0;
}

