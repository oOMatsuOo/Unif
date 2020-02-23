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

   char formatage[3];
   Taille taille_fichier;
   int taille_max_pixel;
   int** fichier_pnm;

};


int load_pnm(PNM **image, char* filename) {
   // Vérification des préconditions

   if(image == NULL || filename == NULL){
      return -2;
   }

   PNM image_charge;
   image = &image_charge;

   char *extension_fichier;
   extension_fichier = strchr(filename, '.');

   FILE* fichier = fopen(filename, "r");

   //Vérification de la bonne ouverture du fichier

   if(fichier == NULL){
      return -1;
   }

   // Analyse de l'en-tête
   int status = 0;
   char* ligne;

   while(status < 3){
      //lire_ligne(&ligne,fichier);
      ligne = malloc(sizeof(char)*1000);
      fgets(ligne,999,fichier);
      printf("%s", ligne);
      if((ligne[0] != '#') == 1){
         if(status == 0){
            if(creer_formatage(ligne,&image_charge) != 0){
               printf("%s \n", "Erreur lors de l'enregistrement du formatage renseigné dans le fichier.");
               return -3;
            }
         }
         else if(status == 1){
            if(creer_taille(ligne,&image_charge) != 0){
               printf("%s \n", "Erreur lors de l'enregistrement de la taille de l'image renseignée dans le fichier.");
               return -3;
            }
            if(image_charge.formatage == 'P1')
               status += 1;
         }
         else if(status == 2){
            if(creer_taille_max(ligne,&image_charge) != 0){
               printf("%s \n", "Erreur lors de l'enregistrement de la taille maximale d'un pixel renseignée dans le fichier.");
               return -3;
            }
         }
         status += 1;
      }
      free(ligne);
   }

   printf("%s      -> Format\n", image_charge.formatage);
   printf("%d , %d -> Taille\n", image_charge.taille_fichier.colonnes,image_charge.taille_fichier.lignes);
   printf("%d      -> Taille Max\n", image_charge.taille_max_pixel);






   // int compteur = 0;

   // // Format dans le fichier

   // while(compteur == 0){
   //    char provisoir[3];
   //    fgets(provisoir,3,fichier);
   //    if(provisoir[0] == 'P'){
   //       strcpy(image_charge.formatage,provisoir);
   //       compteur = 1;
   //    }
   // }

   // compteur = 0;

   // //Taille de l'image

   // while(compteur < 1 ){
   //    int colonnes = 0, lignes = 0;
   //    char taille[100];
   //    fgets(taille, 100, fichier);
   //    if(taille[0] != '\n' && taille[0] != '#'){
   //       printf("%s", taille);
   //       image_charge.taille_fichier.colonnes = atoi(taille);
   //       image_charge.taille_fichier.lignes = atoi(taille);
   //       compteur = 1;
   //    }
   // }

   // compteur = 0;

   // //Taille max d'un pixel

   // while(compteur < 1 ){
   //    int taille_max = 0;
   //    char taille[100];
   //    fgets(taille, 100, fichier);
   //    if(taille[0] != '\n' && taille[0] != '#'){
   //       printf("%s", taille);
   //       image_charge.taille_max_pixel = atoi(taille);
   //       compteur = 1;
   //    }
   // }


   // printf("%s  -> final \n", image_charge.formatage);
   // printf("%d  -> final \n",image_charge.taille_max_pixel);
   // printf("%d  -> final \n",image_charge.taille_fichier.colonnes);
   // printf("%d  -> final \n",image_charge.taille_fichier.lignes);



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

int test_extension(char* extension, char* nom_fichier){

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

int lire_ligne(char* ligne, FILE* filehandle){
   ligne = malloc(sizeof(char)*1000);
   fgets(ligne,1000,filehandle);
   printf("%s", ligne);

   // Truc avec %'\n'

   return 0;
}

int creer_formatage(char* ligne, PNM* image_charge){
   if(ligne == NULL || image_charge == NULL)
      return -1;
   
   char format[3];

   format[0] = ligne[0];
   format[1] = ligne[1];

   strcpy(image_charge->formatage, format);

   return 0;
}

int creer_taille(char* ligne, PNM* image_charge){
   if(ligne == NULL || image_charge == NULL)
      return -1;
   
   char colonnes[3],lignes[3] ;
   int i = 0, cmpt_col = 0, cmpt_lgn = 0;

   while(ligne[i] != ' '){
      colonnes[cmpt_col] = ligne[i];
      i += 1;
      cmpt_col += 1;
   }
   i += 1;
   printf("%d \n",i);
   printf("%s\n", colonnes);
   printf("%c \n",ligne[i]);

   while(ligne[i] != NULL){
      printf("%c \n",ligne[i]);
      lignes[cmpt_lgn] = ligne[i];
      printf("%s\n", lignes);
      i += 1;
      cmpt_lgn += 1;
   }

   printf("%s , %s \n", colonnes, lignes);
   image_charge->taille_fichier.colonnes = atoi(colonnes);
   image_charge->taille_fichier.lignes = atoi(lignes);
   
   return 0;
}

int creer_taille_max(char* ligne, PNM* image_charge){
   return 0;
}