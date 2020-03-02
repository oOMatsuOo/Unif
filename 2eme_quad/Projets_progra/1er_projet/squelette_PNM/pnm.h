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
 * @param extensionname le nom de l'extension passée en paramètre du main
 * 
 * @pre: extensionname != NULL
 * @post: extensionname appartient à {pbm; pgm, ppm}
 * 
 * @return:
 *      0 Succès
 *      -1 Extension renseignée non reconnue
 *      -2 Extension renseignée différente de celle du fichier
 *      -3 Extension du fichier non reconnue
 */

void test_extension(char* format, char* nom_fichier);

/**
 * Lire une ligne d'un fichier
 * 
 * Retourne un pointeur sur une liste de char, contenant la ligne lue
 * 
 * @param adresse du pointeur dans lequel stocker l'adresse de la liste et adresse du fichier à lire
 * 
 * @pre: pointeur != NULL et fichier != NULL
 * @post: pointeur pointe sur un tableau de char
 * 
 * @return:
 *      0 Succès
 *      -1 Mauvais pointeur
 *      -2 Problème lors de la lecture du fichier
 */

int lire_ligne(char** ligne_s_p, FILE* filehandle);

/**
 * Remplis le format d'un fichier PNM
 * 
 * Remplis le champs formatage de l'image
 * 
 * @param adresse de la ligne contenant les données et adresse de la structure PNM de l'image
 * 
 * @pre: ligne != NUL et image != NULL
 * @post: image.formatage à été remplis avec les bonnes donnée de la ligne
 * 
 * @return:
 *      0 Succès
 *      -1 Mauvais pointeur
 *      -2 Problème lors de la lecture de la ligne
 * 
 */

/**
TODO
 */
int load_data(PNM* image,FILE* fichier);

int verification_taille_max(PNM* image);

/**
 * Remplis la taille d'un fichier PNM
 * 
 * Remplis le champs taille 
 * 
 * @param adresse de la ligne contenant les données et adresse de la structure PNM de l'image
 * 
 * @pre: ligne != NUL et image != NULL
 * @post: image.taille à été remplis avec les bonnes donnée de la ligne
 * 
 * @return:
 *      0 Succès
 *      -1 Mauvais pointeur
 *      -2 Problème lors de la lecture de la ligne
 *      -3 Mauvais formatage du fichier
 * 
 */

int creer_taille(char* ligne_s, PNM* image);

/**
 * Remplis la taille_max d'un pixel d'un fichier PNM
 * 
 * Remplis le champs taille_max_pixel de l'image
 * 
 * @param adresse de la ligne contenant les données et adresse de la structure PNM de l'image
 * 
 * @pre: ligne != NUL et image != NULL
 * @post: image.taille_max_pixel à été remplis avec les bonnes donnée de la ligne
 * 
 * @return:
 *      0 Succès
 *      -1 Mauvais pointeur
 *      -2 Problème lors de la lecture de la ligne
 * 
 */

int creer_taille_max(char* ligne_s, PNM* image);

int scan_pixel(FILE* fichier);

int load_header(PNM* image,FILE* fichier,int extension_fichier);

int load_formatage(PNM* image,FILE* fichier);

int load_taille_image(PNM* image,FILE* fichier);

int load_taille_pixel_max(PNM* image,FILE* fichier);

int skip_commentaires(FILE* fichier);

int write_header(PNM *image,FILE *fichier);

int write_data(PNM *image,FILE *fichier);

#endif // __PNM__

