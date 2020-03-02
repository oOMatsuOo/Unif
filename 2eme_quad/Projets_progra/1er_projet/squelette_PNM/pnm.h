/**
 * pnm.h
 * 
 * Ce fichier contient les déclarations de types et les prototypes
 * des fonctions pour la manipulation d'images PNM.
 * 
 * @author: Van Muysewinkel Kieran S181530
 * @date: 20/02/2020
 * @projet: INFO0030 Projet 1
 */

/*
 * Include guard (pour éviter les problèmes d'inclusions multiplies
 * Bonne pratique: toujours encadrer un header avec un include guard
 */
#ifndef __PNM__
#define __PNM__

/**
 * Déclaration du type opaque PNM
 *
 */
typedef struct PNM_t PNM;
typedef struct PBM_pixel PBM;
typedef struct PPM_pixel PPM;
typedef struct PGM_pixel PGM;
typedef struct taille Taille;


/**
 * load_pnm
 *
 * Charge une image PNM depuis un fichier.
 *
 * @param image l'adresse d'un pointeur sur PNM à laquelle écrire l'adresse
 *              de l'image chargée.
 * @param filename le chemin vers le fichier contenant l'image.
 *
 * @pre: image != NULL, filename != NULL
 * @post: image pointe vers l'image chargée depuis le fichier.
 *
 * @return:
 *     0 Succès
 *    -1 Erreur à l'allocation de mémoire
 *    -2 Nom du fichier malformé
 *    -3 Contenu du fichier malformé
 *
 */
int load_pnm(PNM **image, char* filename);

/**
 * write_pnm
 *
 * Sauvegarde une image PNM dans un fichier.
 *
 * @param image un pointeur sur PNM.
 * @param filename le chemin vers le fichier de destination.
 *
 * @pre: image != NULL, filename != NULL
 * @post: le fichier filename contient l'image PNM image.
 *
 * @return:
 *     0 Succès
 *    -1 Nom du fichier malformé
 *    -2 Erreur lors de la manipulation du fichier
 *
 */
int write_pnm(PNM *image, char* filename);

/**
 * test_extension
 * 
 * Vérifie si le nom de l'extension est bien un nom attendu
 * 
 * @param nom_fichier nom du fichier passé en paramètre
 * @param format format du fichier à vérifier
 * 
 * @pre: nom_fichier != NULL && format != NULL
 * @post: retourne 0 si le format renseigné est le même que celui du fichier
 * 
 * @return:
 *      0 Succès
 *      -1 Mauvais arguments
 *      -2 Mauvaise extension du fichier renseignée
 */

int test_extension(char* format, char* nom_fichier);

/**
 * nom_fichier_retour
 * 
 * Stocke le nom du fichier output en fonction du format du fichier
 * 
 * @param  image  Pointeur vers une structure PNM
 * @param  output pointeur vers un pointeur de char, destiné à recevoir le nom du fichier output
 * 
 * @pre: image != NULL && format != NULL
 * @post: le non nom du fichier output est renseingé dans l'output
 * 
 * @return:
 *      0 Succès
 *      -1 Mauvais arguments
 */

int nom_fichier_retour(PNM* image,char** output);

#endif // __PNM__

