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
#include <string.h>
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
   int valeur_max_pixel;
   void* struct_pixels_p;

};

// Structure des pixels PPM
struct PPM_pixel{

   short unsigned int* R;
   short unsigned int* G;
   short unsigned int* B;
   // Seulement si limté à 65536 valeurs, là ou la sepc officielle limite à 256 valeurs https://en.wikipedia.org/wiki/Netpbm

};

//  Structure des pixels PGM
struct PGM_pixel{

   unsigned char* pixels;
   // Seulement si limté à 256 valeurs, là ou la sepc officielle limite à 65536 valeurs https://en.wikipedia.org/wiki/Netpbm

};

//  Structure des pixels PBM
struct PBM_pixel{

   unsigned char* pixels;
   // 8 bits pour stocker 1 bit -> sous-optimal mais type binaire n'existe pas 

};


int load_pnm(PNM **image, char* filename) {
   // Vérification des préconditions

   if(image == NULL || filename == NULL){
      return -2;
   }

   PNM image_charge;
   *image = &image_charge;

   char *extension_fichier;
   extension_fichier = strchr(filename, '.');

   FILE* fichier = fopen(filename, "r");

   //Vérification de la bonne ouverture du fichier

   if(fichier == NULL){
      return -1;
   }

   // Analyse de l'en-tête
   int status = 0;
   char* ligne_s;

   while(status < 3){
      lire_ligne(&ligne_s,fichier);
      if((ligne_s[0] != '#') == 1){
         if(status == 0){
            if(creer_formatage(ligne_s, &image_charge) != 0){
               printf("%s \n", "Erreur lors de l'enregistrement du formatage renseigné dans le fichier.");
               return -3;
            }
            if((test_formatage(&image_charge,extension_fichier)) != 0){
               printf("%s \n", "Format du fichier différent du format renseigné dans le fichier.");
               return -3;
            }
         }
         else if(status == 1){
            if(creer_taille(ligne_s,&image_charge) != 0){
               printf("%s \n", "Erreur lors de l'enregistrement de la taille de l'image renseignée dans le fichier.");
               return -3;
            }
            if(image_charge.formatage == 1)
               status = 3;
         }
         else if(status == 2){
            if(creer_taille_max(ligne_s,&image_charge) != 0){
               printf("%s \n", "Erreur lors de l'enregistrement de la taille maximale d'un pixel renseignée dans le fichier.");
               return -3;
            }
            if(image_charge.formatage == 1){
               image_charge.valeur_max_pixel = -1;
            }
            if(verification_taille_max(&image_charge) != 0){
               printf("%s \n","Taille maximale renseignée dans le fichier à une mauvaise valeur.");
               return -3;
            }
         }
         status += 1;
      }
      free(ligne_s);
   }
   printf("%d      -> Format \n", image_charge.formatage);
   printf("%d , %d -> Taille \n", image_charge.taille_fichier.colonnes,image_charge.taille_fichier.lignes);
   printf("%d      -> Valeur Max \n", image_charge.valeur_max_pixel);

   if(enregistrement_data(&image_charge,fichier) != 0){
      printf("%s \n", "Problème lors de la lecture des données.");
      return -3;
   }


   fclose(fichier);

   return 0;
}

int write_pnm(PNM *image, char* filename) {

   if(image == NULL || filename == NULL)
      return -1;

   return 0;
}

void test_extension(char* format, char* nom_fichier){

   char *extension_fichier;
   extension_fichier = strchr(nom_fichier, '.');

   // Test de l'extension du nom du fichier

   if(nom_fichier == NULL || (strcmp(extension_fichier,".pbm") != 0 && strcmp(extension_fichier,".pgm") != 0 && strcmp(extension_fichier,".ppm") != 0)){
      printf("%s \n", "Mauvaise extension du fichier renseigné.");
      return;
   };

   // Test de correspondance entre l'extension renseignée et celle du nom du fichier

   if(strcmp(format,"PBM") == 0 && strcmp(extension_fichier, ".pbm") != 0){
      printf("%s \n", "hello");
      return;
   }
   else if(strcmp(format,"PGM") == 0 && strcmp(extension_fichier, ".pgm") != 0){
      return;
   }
   else if(strcmp(format,"PPM") == 0 && strcmp(extension_fichier, ".ppm") != 0){
      return;
   }

   return;
}

int lire_ligne(char** ligne_s_p, FILE* filehandle){
   if (ligne_s_p == NULL || filehandle == NULL)
      return -1;
   *ligne_s_p = malloc(sizeof(char)*4000);
   if (fgets(*ligne_s_p,4000,filehandle)){
      return -2;
   }
   printf("%s \n", *ligne_s_p);

   return 0;
}

int creer_formatage(char* ligne_s, PNM* image_charge){
   if(ligne_s == NULL || image_charge == NULL)
      return -1;
   
   int format;

   if(sscanf(ligne_s,"P%d",&format) != 1)
      return -2;
   if(format < 1 || format > 3)
      return -3;
   image_charge->formatage = format;
   if(format == 1){
      image_charge->struct_pixels_p = malloc(sizeof(PBM));
   }
   else if(format == 2)
      image_charge->struct_pixels_p = malloc(sizeof(PGM));
   else
      image_charge->struct_pixels_p = malloc(sizeof(PPM));

   return 0;
}

int creer_taille(char* ligne_s, PNM* image_charge){
   if(ligne_s == NULL || image_charge == NULL)
      return -1;

   int colonnes ,lignes;

   if(sscanf(ligne_s, "%d %d",&colonnes,&lignes) != 2)
      return -2;

   image_charge->taille_fichier.colonnes = colonnes;
   image_charge->taille_fichier.lignes = lignes;
   
   if(image_charge->formatage == 1){
      PBM* sp = (PBM*)image_charge->struct_pixels_p;
      sp->pixels = malloc(colonnes*lignes*sizeof(unsigned char));
   }
   else if(image_charge->formatage == 2){
      PGM* sp = (PGM*)image_charge->struct_pixels_p;
      sp->pixels = malloc(sizeof(unsigned char) * lignes * colonnes);
   }
   else{
      PPM* sp = (PPM*)image_charge->struct_pixels_p;
      sp->R = malloc(sizeof(short unsigned int) * lignes * colonnes);
      sp->G = malloc(sizeof(short unsigned int) * lignes * colonnes);
      sp->B = malloc(sizeof(short unsigned int) * lignes * colonnes);
   }

   return 0;
}

int creer_taille_max(char* ligne_s, PNM* image_charge){
   if(ligne_s == NULL || image_charge == NULL)
      return -1;

   int taille_max;
   
   if(sscanf(ligne_s,"%d",&taille_max) != 1)
      return -2;

   if(taille_max < 0)
      return -3;
   else
      image_charge->valeur_max_pixel = taille_max;

   return 0;
}

int test_formatage(PNM* image_charge, char* extension){
   if((image_charge->formatage == 1) && (strcmp(extension,".pbm") != 0)){
      return -1;
   }
   else if((image_charge->formatage == 2) && (strcmp(extension,".pgm") != 0)){
      return -1;
   }
   else if((image_charge->formatage == 3) && (strcmp(extension,".ppm") != 0)){
      return -1;
   }

   return 0;

}

int verification_taille_max(PNM* image_charge){
   if(image_charge == NULL)
      return -1;

   int format = image_charge->formatage;
   int taille_max = image_charge->valeur_max_pixel;

   if(format == 2 && (taille_max < 0 || taille_max > 256)){
      return -2;
   }
   else if(format == 3 &&  (taille_max < 0 || taille_max > 35536)){
      return -2;
   }

   return 0;
}

int enregistrement_data(PNM* image_charge,FILE* fichier){
   if(image_charge == NULL || fichier == NULL)
      return -1;
   
   int format = image_charge->formatage;

   int i = 0, j = 0, lignes, colonnes, offset = 0;
   lignes = image_charge->taille_fichier.lignes;
   colonnes = image_charge->taille_fichier.colonnes;

   if (format == 1 || format == 2){
      for(i=0;i<lignes;i++){
         for(j=0;j<colonnes;j++){
            unsigned char pixel = pixel_PBM_PGM(fichier);
            if(pixel != (unsigned char)-1){
               if(image_charge->formatage == 1){
                  PBM* sp = (PBM*)image_charge->struct_pixels_p;
                  sp->pixels[offset] = pixel;
               }
               else if(image_charge->formatage == 2){
                  PGM* sp = (PGM*)image_charge->struct_pixels_p;
                  sp->pixels[offset] = pixel;
               }
               offset += 1;
            }else{
               return -3;
            }
         }
      }

   }
   else if(format == 3){
      for(i=0;i<colonnes;i++){
         for(j=0;j<lignes;j++){
            short unsigned int pixel = pixel_PPM(fichier);
            if(pixel != (short unsigned int)-1){
               PPM* sp = (PPM*)image_charge->struct_pixels_p;
               sp->R[offset] = pixel;

            }else{
               return -3;
            }

            pixel = pixel_PPM(fichier);
            if(pixel != (short unsigned int)-1){
               PPM* sp = (PPM*)image_charge->struct_pixels_p;
               sp->G[offset] = pixel;
            }else{
               return -3;
            }

            pixel = pixel_PPM(fichier);
            if(pixel != (short unsigned int)-1){
               PPM* sp = (PPM*)image_charge->struct_pixels_p;
               sp->B[offset] = pixel;
            }else{
               return -3;
            }

            offset += 1;
         }
      }
   }
   printf("%d \n",offset);
   printf("%d \n",(colonnes * lignes));

   return 0;
}

unsigned char pixel_PBM_PGM(FILE* fichier){
   unsigned int pixel_u;
   if(fscanf(fichier,"%u ",&pixel_u) !=1)
      return (unsigned char)-1;

   return (unsigned char) pixel_u;
}

short unsigned int pixel_PPM(FILE* fichier){
   unsigned int pixel_u;
   if(fscanf(fichier,"%u ", &pixel_u) != 1)
      return (short unsigned int)-1;
   
   return (short unsigned int)pixel_u;
}
