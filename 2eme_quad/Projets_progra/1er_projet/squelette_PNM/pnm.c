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


/**
 * Définition du type opaque PNM
 *
 */
struct PNM_t {

   /* Insérez ici les champs de la structure PNM */

};


int load_pnm(PNM **image, char* filename) {

   /* Insérez le code ici */
   /**
    * Ouvrir le fichier fopen FILE* fopen(const char* nomDuFichier, const char* modeOuverture);
    * Vérifier si bonne ouverture (pointeur != NULL)
    * 
    * 
    * Terminer avec fclose int fclose(FILE* pointeurSurFichier);=)
    */

   return 0;
}

int write_pnm(PNM *image, char* filename) {

   /* Insérez le code ici */

   return 0;
}

