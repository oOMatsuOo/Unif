#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

// Définition du type pour une Date
typedef struct{
    unsigned short jour;
    unsigned short mois;
    unsigned short annee;
}Date;

// Définition d'un chien
typedef struct{
    char *nom;
    char sexe;
    char vaccine;
}Chien;

// Définition d'une portée de chiens
typedef struct{
    Chien *pere;
    Chien *mere;
    Chien *chiots;
    unsigned short nb_chiots;
    Date date_naissance;
}Portee;

/*
 * @pré: {nom_fichier} valide, {chiots} est un tableau de chiens valide
 * 
 * @post : 1 si {chiots} a bien été rempli depuis le fichier dont le nom est
 * contenu dans {nom_fichier}.
 * -1 sinon.
 */
int charger_chiots(char *nom_fichier, Chien *chiots, unsigned short nb_chiots);

/*
 * Crée un chien ayant un nom, un sexe et une information quant à sa
 * vaccination.
 *
 * @pré: {nom} valide, {sexe} ∈ {'M','F'}, vacciné ∈ [0, 1]
 * @post: Un pointeur vers un chien valide.
 * NULL en cas d’erreur.
 */
Chien *cree_chien(char *nom, char sexe, char vaccine);

 /*
 * Crée une portée de chiots en fonction d’un père et d’une mère et charge,
 * depuis un fichier, les différents chiots.
 *
 * @pré: {nom_pere} est un nom de chien valide, {nom_mere} est un nom de chien
 * valide. Le père et la mère ont été vaccinés, {nb_chiots} > 0,
 * {nom_fichier} est valide.
 * @post: un pointeur vers une portée valide. Les chiots de la portée ont été
 * chargés depuis le fichier {nom_fichier}. NULL en cas d’erreur
 */
 Portee *cree_portee(char *nom_pere, char *nom_mere, unsigned short nb_chiots, char *nom_fichier, Date date_naissance);