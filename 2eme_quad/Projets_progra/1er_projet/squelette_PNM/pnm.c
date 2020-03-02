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

   *image = malloc(sizeof(PNM));

   char *extension_fichier;
   extension_fichier = strchr(filename, '.');
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
   int status = 0;
   char* ligne_s;

   if(load_header(*image,fichier,format_attendu) <0){
      printf("Problème lors de l'enregistrement du header \n");
      return -3;
   }

   printf("%d      -> Format \n", (*image)->formatage);
   printf("%d , %d -> Taille \n", (*image)->taille_fichier.colonnes, (*image)->taille_fichier.lignes);
   printf("%d      -> Valeur Max \n", (*image)->valeur_max_pixel);

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

int creer_formatage(char* ligne_s, PNM* image){
   if(ligne_s == NULL || image == NULL)
      return -1;
   
   int format;

   if(sscanf(ligne_s,"P%d",&format) != 1)
      return -2;
   if(format < 1 || format > 3)
      return -3;
   image->formatage = format;
   if(format == 1){
      image->struct_pixels_p = malloc(sizeof(PBM));
   }
   else if(format == 2)
      image->struct_pixels_p = malloc(sizeof(PGM));
   else
      image->struct_pixels_p = malloc(sizeof(PPM));

   return 0;
}

int creer_taille(char* ligne_s, PNM* image){
   if(ligne_s == NULL || image == NULL)
      return -1;

   int colonnes ,lignes;

   if(sscanf(ligne_s, "%d %d",&colonnes,&lignes) != 2)
      return -2;

   image->taille_fichier.colonnes = colonnes;
   image->taille_fichier.lignes = lignes;
   
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

int creer_taille_max(char* ligne_s, PNM* image){
   if(ligne_s == NULL || image == NULL)
      return -1;

   int taille_max;
   
   if(sscanf(ligne_s,"%d",&taille_max) != 1)
      return -2;

   if(taille_max < 0)
      return -3;
   else
      image->valeur_max_pixel = taille_max;

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
            int pixel = scan_pixel(fichier);
            if(pixel != -1){
               if(image->formatage == 1){
                  PBM* sp = (PBM*)image->struct_pixels_p;
                  sp->pixels[offset] = (unsigned char)pixel;
               }
               else if(image->formatage == 2){
                  PGM* sp = (PGM*)image->struct_pixels_p;
                  sp->pixels[offset] = (unsigned char)pixel;
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

   if((fscanf(fichier, "P%d%*[ \n]",&image->formatage)) != 1){
      return -1;
   }

   return 0;
}

int load_taille_image(PNM* image,FILE* fichier){
   if(skip_commentaires(fichier) < 0){
      printf("Problèmes lors de la lecture d'un commentaire dans le load_taille_pixel \n");
      return -1;
   }

   if(fscanf(fichier,"%d%*[ ]%d%*[ \n]",&image->taille_fichier.colonnes,&image->taille_fichier.lignes) != 2){
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

   if(fscanf(fichier,"%d%*[ \n]",&image->valeur_max_pixel) != 1){
      return -1;
   }

   return 0;
}

int skip_commentaires(FILE* fichier){
   int comment_flag = 1;
   do {
      int ch = fgetc(fichier);
      if(ch < 0){
         printf("Problème lors de la lecture du premier caractère de la ligne");
         return -1;
      }
      if((char)ch == '#'){
         if(fscanf(fichier,"%*[^\n]\n") < 0){
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
