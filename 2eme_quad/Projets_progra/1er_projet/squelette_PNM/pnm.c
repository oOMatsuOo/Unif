/**
 * pnm.c
 * 
 * Ce fichier contient les définitions de types et 
 * les fonctions de manipulation d'images PNM.
 * 
 * @author: Nom Prenom Matricule
 * @date: 
 * @projet: INFO0030 Projet 1
 */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "pnm.h"

#define MAX_CHAR 50

/**
 * Définition de la structure de la taille d'un fichier PNM
 * 
 */

struct taille{

   int colonnes;
   int lignes;

};

/**
 * Définition du type opaque PNM
 *
 */
struct PNM_t {

   int formatage;
   Taille taille_fichier;
   int** fichier_pnm;

};


int load_pnm(PNM **image, char* filename) {
   // Vérification des préconditions

   if(image == NULL || filename == NULL){
      return -2;
   }

   char *extension_fichier;
   extension_fichier = strchr(filename, '.');

   FILE* fichier = fopen(filename, "r");

   //Vérification de la bonne ouverture du fichier

   if(fichier == NULL){
      return -1;
   }

   int compteur = 0;
   char format[3];
   Taille taille_fichier;
   int taille_max_pixel = 1;

   // Format dans le fichier
   while(compteur == 0){
      char provisoir[3];
      fgets(provisoir,2,fichier);
      printf("%s", provisoir);
      compteur = 1;
   }



   /* Insérez le code ici */
   /**
    * Ouvrir le fichier fopen FILE* fopen(const char* nomDuFichier, const char* modeOuverture);
    * Vérifier si bonne ouverture (pointeur != NULL)
    * 
    * 
    * Terminer avec fclose int fclose(FILE* pointeurSurFichier);=)
    */

   fclose(fichier);

   return 0;
}

int write_pnm(PNM *image, char* filename) {

   /* Insérez le code ici */

   return 0;
}

int test_extension(char extension[4], char nom_fichier[40]){

   char *extension_fichier;
   extension_fichier = strchr(nom_fichier, '.');

   // Test de l'extension renseignée

   if(extension == NULL || (strcmp(extension,"PBM") != 0 && strcmp(extension,"PGM") != 0 && strcmp(extension,"PPM") != 0)){
      return -1;
   };

   // Test de l'extension du nom du fichier

   if(nom_fichier == NULL || (strcmp(extension_fichier,".pbm") != 0 && strcmp(extension_fichier,".pgm") != 0 && strcmp(extension_fichier,".ppm") != 0)){
      return -3;
   };

   // Test de correspondance entre l'extension renseignée et celle du nom du fichier

   if(strcmp(extension,"PBM") == 0 && strcmp(extension_fichier, ".pbm") != 0){
      printf("%s \n", "hello");
      return -2;
   }
   else if(strcmp(extension,"PGM") == 0 && strcmp(extension_fichier, ".pgm") != 0){
      return -2;
   }
   else if(strcmp(extension,"PPM") == 0 && strcmp(extension_fichier, ".ppm") != 0){
      return -2;
   }

   return 0;
}

