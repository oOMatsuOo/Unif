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

int verification_taille_max(PNM* image);

int load_data(PNM* image,FILE* fichier);

int scan_pixel(FILE* fichier);

int load_header(PNM* image,FILE* fichier,int extension_fichier);

int load_formatage(PNM* image,FILE* fichier);

int load_taille_image(PNM* image,FILE* fichier);

int load_taille_pixel_max(PNM* image,FILE* fichier);

int skip_commentaires(FILE* fichier);

int test_pixel(int pixel,PNM* image);

int write_header(PNM *image,FILE *fichier);

int write_data(PNM *image,FILE *fichier);

int nom_fichier_retour(PNM* image,char** output);

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

   *image = malloc(sizeof(PNM));

   char *extension_fichier;
   extension_fichier = strchr(filename, '.');

   while(extension_fichier[1] == '/'){
      extension_fichier = strchr(&extension_fichier[2],'.');
   }

   int format_attendu;

   if(strcmp(extension_fichier,".pbm") == 0){
      format_attendu = 1;
   }
   else if(strcmp(extension_fichier,".pgm") == 0){
      format_attendu = 2;
   }
   else{
      format_attendu = 3;
   }

   FILE* fichier = fopen(filename, "r");

   //Vérification de la bonne ouverture du fichier

   if(fichier == NULL){
      return -1;
   }

   // Analyse de l'en-tête

   if(load_header(*image,fichier,format_attendu) <0){
      printf("Problème lors de l'enregistrement du header \n");
      return -3;
   }

   if(load_data(*image,fichier) != 0){
      printf("%s \n", "Problème lors de la lecture des données.");
      return -3;
   }


   fclose(fichier);

   return 0;
}

int write_pnm(PNM *image, char* filename) {

   if(image == NULL || filename == NULL)
      return -1;
   
   FILE *fichier = fopen(filename,"w");
   if(fichier == NULL)
      return -1;
      
   if(write_header(image,fichier) != 0){
      return -2;
   };

   if(write_data(image,fichier) != 0){
      return -3;
   };

   fclose(fichier);
   return 0;
}

int test_extension(char* format, char* nom_fichier){

   char *extension_fichier;
   extension_fichier = strchr(nom_fichier, '.');
   if(extension_fichier[1] == '/'){
      extension_fichier = strchr(&extension_fichier[2],'.');
   }
   if(extension_fichier == NULL || format == NULL){
      printf("Mauvais arguments\n");
      return -1;
   }

   // Test de l'extension du nom du fichier

   if(nom_fichier == NULL || (strcmp(extension_fichier,".pbm") != 0 && strcmp(extension_fichier,".pgm") != 0 && strcmp(extension_fichier,".ppm") != 0)){
      printf("%s \n", "Mauvaise extension du fichier renseignée. \n");
      return -2;
   };

   // Test de correspondance entre l'extension renseignée et celle du nom du fichier

   if(strcmp(format,"PBM") == 0 && strcmp(extension_fichier, ".pbm") != 0){
      return 0;
   }
   else if(strcmp(format,"PGM") == 0 && strcmp(extension_fichier, ".pgm") != 0){
      return 0;
   }
   else if(strcmp(format,"PPM") == 0 && strcmp(extension_fichier, ".ppm") != 0){
      return 0;
   }

   return 0;
}

int verification_taille_max(PNM* image){
   if(image == NULL)
      return -1;

   int format = image->formatage;
   int taille_max = image->valeur_max_pixel;

   if(format == 2 && (taille_max < 0 || taille_max > 256)){
      return -2;
   }
   else if(format == 3 &&  (taille_max < 0 || taille_max > 35536)){
      return -2;
   }

   return 0;
}

int load_data(PNM* image,FILE* fichier){
   if(image == NULL || fichier == NULL)
      return -1;
   
   int format = image->formatage;

   int i = 0, j = 0, lignes, colonnes, offset = 0;
   lignes = image->taille_fichier.lignes;
   colonnes = image->taille_fichier.colonnes;

   if (format == 1 || format == 2){
      for(i=0;i<lignes;i++){
         for(j=0;j<colonnes;j++){
            if(skip_commentaires(fichier) < 0){
               return -1;
            }
            int pixel = scan_pixel(fichier);
            if(test_pixel(pixel,image) != 0){
               return -4;
            }
            if(image->formatage == 1){
               PBM* sp = (PBM*)image->struct_pixels_p;
               sp->pixels[offset] = (unsigned char)pixel;
            }
            else if(image->formatage == 2){
               PGM* sp = (PGM*)image->struct_pixels_p;
               sp->pixels[offset] = (unsigned char)pixel;
            }
            offset += 1;
         }
      }

   }
   else if(format == 3){
      for(i=0;i<colonnes;i++){
         for(j=0;j<lignes;j++){
            int pixel = scan_pixel(fichier);
            if(pixel != -1){
               PPM* sp = (PPM*)image->struct_pixels_p;
               sp->R[offset] = (short unsigned int)pixel;

            }else{
               return -3;
            }

            pixel = scan_pixel(fichier);
            if(pixel != -1){
               PPM* sp = (PPM*)image->struct_pixels_p;
               sp->G[offset] = (short unsigned int)pixel;
            }else{
               return -3;
            }

            pixel = scan_pixel(fichier);
            if(pixel != -1){
               PPM* sp = (PPM*)image->struct_pixels_p;
               sp->B[offset] = (short unsigned int)pixel;
            }else{
               return -3;
            }

            offset += 1;
         }
      }
   }
   if(offset != (colonnes * lignes)){
      printf("Problème non détecté lors de la lecture du fichier \n");
      return -1;
   }

   return 0;
}

int scan_pixel(FILE* fichier){
   unsigned int pixel_u;
   if(fscanf(fichier,"%u%*[ \n]",&pixel_u) !=1)
      return -1;

   return (int)pixel_u;
}

int load_header(PNM* image,FILE* fichier,int extension_fichier){
   if(load_formatage(image, fichier) != 0){
      printf("Problème lors de la lecture du formatage. \n");
      return -1;
   }

   int nombre_magique = image->formatage;

   if(nombre_magique < 1 || nombre_magique > 3){
      printf("Mauvaise valeur du nombre magique \n");
      return -3;
   }

   if(extension_fichier != nombre_magique){
      printf("Le nombre magique ne correspond pas au format du fichier \n");
      return -4;
   }

   if(nombre_magique == 1)
      image->struct_pixels_p = malloc(sizeof(PBM));
   else if(nombre_magique == 2)
      image->struct_pixels_p = malloc(sizeof(PGM));
   else
      image->struct_pixels_p = malloc(sizeof(PPM));

   if(load_taille_image(image, fichier) != 0){
      printf("Problème lors de la lecture de la taille de l'image. \n");
      return -1;
   }
   if(image->formatage != 1){
      if(load_taille_pixel_max(image, fichier) != 0){
         printf("Problème lors de la lecture de la taille max d'un pixel. \n");
         return -1;
      }
   }

   return 0;
}

int load_formatage(PNM* image,FILE* fichier){
   if(skip_commentaires(fichier) < 0){
      printf("Problèmes lors de la lecture d'un commentaire dans le load_formatage \n");
      return -1;
   }

   if((fscanf(fichier, "P%d %*[\n]",&image->formatage)) != 1){
      return -1;
   }

   return 0;
}

int load_taille_image(PNM* image,FILE* fichier){
   if(skip_commentaires(fichier) < 0){
      printf("Problèmes lors de la lecture d'un commentaire dans le load_taille_pixel \n");
      return -1;
   }

   if(fscanf(fichier,"%d %d %*[\n]",&image->taille_fichier.colonnes,&image->taille_fichier.lignes) != 2){
      return -1;
   }

   int lignes, colonnes;
   colonnes = image->taille_fichier.colonnes;
   lignes = image->taille_fichier.lignes;

   if(image->formatage == 1){
      PBM* sp = (PBM*)image->struct_pixels_p;
      sp->pixels = malloc(colonnes*lignes*sizeof(unsigned char));
   }
   else if(image->formatage == 2){
      PGM* sp = (PGM*)image->struct_pixels_p;
      sp->pixels = malloc(sizeof(unsigned char) * lignes * colonnes);
   }
   else{
      PPM* sp = (PPM*)image->struct_pixels_p;
      sp->R = malloc(sizeof(short unsigned int) * lignes * colonnes);
      sp->G = malloc(sizeof(short unsigned int) * lignes * colonnes);
      sp->B = malloc(sizeof(short unsigned int) * lignes * colonnes);
   }

   return 0;
}

int load_taille_pixel_max(PNM* image,FILE* fichier){
   if(skip_commentaires(fichier) < 0){
      printf("Problèmes lors de la lecture d'un commentaire dans le load_taille_pixel_max \n");
      return -1;
   }

   if(fscanf(fichier,"%d %*[\n]",&image->valeur_max_pixel) != 1){
      return -1;
   }

   if(verification_taille_max(image) != 0){
      printf("La taille maximale n'est pas autorisée \n");
      return -1;
   }

   return 0;
}

int skip_commentaires(FILE* fichier){
   int comment_flag = 1;
   do {
      int ch = fgetc(fichier);
      if(ch < 0){
         if(ch == EOF){
            printf("Fin prématurée du fichier\n");
            return -1;
         }else{
            printf("Problème lors de la lecture du premier caractère de la ligne \n");
            return -1;
         }
      }
      if((char)ch == '#'){
         if(fscanf(fichier,"%*[^\n]%*[\n]") < 0){
            printf("Problème lors de la lecture d'une ligne de commentaire");
            return -2;
         };
      }
      else{
         if(ungetc(ch,fichier) < 0){
            printf("Problème lors de la fin de skip comment");
            return -4;
         }
         comment_flag = 0;
      }
   } while (comment_flag);

   return 0;
}

int test_pixel(int pixel,PNM* image){

   int format = image->formatage, taille_max = image->valeur_max_pixel;

   if(format == 1 && pixel > 1){
      printf("Un pixel a une valeur suppérieure à la valeur max.\n");
      return -1;
   }
   else if(format != 1 && pixel > taille_max){
      printf("Un pixel a une valeur suppérieure à la valeur max.\n");
      return -1;
   }

   if(pixel < 0){
      printf("Erreur système lors de la lecture d'un pixel\n");
      return -2;
   }

   
   return 0;
}

int write_header(PNM *image,FILE *fichier){
   fprintf(fichier,"P%d\n",image->formatage);
   fprintf(fichier,"%d %d\n",image->taille_fichier.colonnes,image->taille_fichier.lignes);
   if(image->formatage != 1)
      fprintf(fichier,"%d\n",image->valeur_max_pixel);

   return 0;
}

int write_data(PNM *image,FILE *fichier){

   int colonnes = image->taille_fichier.colonnes, lignes = image->taille_fichier.lignes, i = 0, j = 0, format = image->formatage, offset = 0;

   if(format == 1){
      PBM* sp = (PBM*)image->struct_pixels_p;
      for(i=0;i<lignes;i++){
         for(j=0;j<colonnes;j++){
            fprintf(fichier,"%u ",sp->pixels[offset]);
            offset += 1;
         }
         fprintf(fichier,"\n");
      }
   }
   else if(format == 2){
      PGM* sp = (PGM*)image->struct_pixels_p;
      for(i=0;i<lignes;i++){
         for(j=0;j<colonnes;j++){
            fprintf(fichier,"%u ",sp->pixels[offset]);
            offset += 1;
         }
         fprintf(fichier,"\n");
      }
   }
   else if(format == 3){
      PPM* sp = (PPM*)image->struct_pixels_p;
      for(i=0;i<lignes;i++){
         for(j=0;j<colonnes;j++){
            fprintf(fichier,"%u %u %u ",sp->R[offset],sp->G[offset],sp->B[offset]);
            offset += 1;
         }
         fprintf(fichier,"\n");
      }
   }

   return 0;
}

int nom_fichier_retour(PNM* image,char** output){
   if(image == NULL){
      return -1;
   }

   if(image->formatage == 1){
      *output = "output.pbm";
   }
   else if(image->formatage == 2){
      *output = "output.pgm";
   }
   else if(image->formatage == 3){
      *output = "output.ppm";
   }

   return 0;
}
