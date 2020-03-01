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
#include <string.h>
#include <assert.h>
#include <unistd.h>
#include <ctype.h>
#include <getopt.h>

#include "pnm.h"


int main(int argc, char *argv[]) {

   char *optstring = "f:";
   char *extension, nom_fichier[40];
   int opt;

   while((opt = getopt(argc,argv,optstring)) != -1){
      switch (opt){
         case 'f':
            if((strcmp(optarg,"PBM") != 0) && (strcmp(optarg,"PPM") != 0) && (strcmp(optarg,"PGM") != 0)){
               printf("%s \n", "Mauvais format renseigné.");
               return -1;
            }
            else{
               extension = strdup(optarg);
            }
            break;
         default:
            printf("%s \n","Usage : ./pnm -f type_fichier nom_fichier");
            return -1;
      }
   }

   if((argc - optind )!= 1){
      printf("%s \n","Nombre incorrect d'arguments.");
      printf("%s \n","Usage : ./pnm -f type_fichier nom_fichier");
      return -1;
   }

   if (argv[3] != NULL){
      strcpy(nom_fichier, argv[3]);
   }

   test_extension(&extension[0],&nom_fichier[0]);

   PNM* image;

   printf("%d \n",load_pnm(&image,nom_fichier));

   printf("%d \n",write_pnm(image,nom_fichier));

   return 0;
}
