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

#define USAGE printf("%s \n","Usage : ./pnm -f type_fichier nom_fichier_input nom_fichier_output");

int main(int argc, char *argv[]) {

   char *optstring = "f:";
   char *extension, *nom_fichier, *nom_fichier_write;
   int opt;

   while((opt = getopt(argc,argv,optstring)) != -1){
      switch (opt){
         case 'f':
            if((strcmp(optarg,"PBM") != 0) && (strcmp(optarg,"PPM") != 0) && (strcmp(optarg,"PGM") != 0)){
               printf("%s \n", "Mauvais format renseigné.");
               USAGE
               return -1;
            }
            else{
               extension = strdup(optarg);
            }
            break;
         default:
            USAGE
            return -1;
      }
   }

   if((argc - optind )!= 2){
      printf("%s \n","Nombre incorrect d'arguments.");
      USAGE
      return -1;
   }

   nom_fichier = strdup(argv[optind]);

   nom_fichier_write = strdup(argv[optind + 1]);

   test_extension(&extension[0],&nom_fichier[0]);

   PNM* image;

   printf("%d \n",load_pnm(&image,nom_fichier));

   printf("%d \n",write_pnm(image,nom_fichier_write));

   return 0;
}
