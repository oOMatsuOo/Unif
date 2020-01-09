#include "chenil.h"

int charger_chiots(char *nom_fichier, Chien *chiots, unsigned short nb_chiots){

    assert(nom_fichier && chiots);
    FILE *chiotsfile;

    if ((chiotsfile = fopen(nom_fichier,"r")) == NULL){
        fclose(chiotsfile);
        return -1;
    }

    unsigned int compteur = 0;
    for(compteur = 0; compteur < nb_chiots; compteur++){

        fscanf(chiotsfile, " %64[^\n] %64[^\n] %64[^\n]",chiots[compteur].nom, &chiots[compteur].sexe, &chiots[compteur].vaccine);

    }

    return 1;
}

Chien *cree_chien(char *nom, char sexe, char vaccine){
    Chien *n_chien = malloc(sizeof(Chien) * 1);

    if((sexe != 'M' || sexe != 'F') || (vaccine != 0 || vaccine != 1) ){
        return NULL;
    }

    n_chien -> nom = nom;
    n_chien -> sexe = sexe;
    n_chien -> vaccine = vaccine;

    return n_chien;
}

Portee *cree_portee(char *nom_pere, char *nom_mere, unsigned short nb_chiots, char *nom_fichier, Date date_naissance){
    assert(nom_pere && nom_mere && nb_chiots > 0 && nom_fichier);
    
    Portee *actuelportee = malloc(sizeof(Chien) * 1);
    Chien *chiots_portee = malloc(sizeof(Chien) * nb_chiots);
    charger_chiots(nom_fichier, chiots_portee, nb_chiots);

    actuelportee -> pere = *nom_pere;
    actuelportee -> mere = *nom_mere;
    actuelportee -> chiots = chiots_portee;
    actuelportee -> nb_chiots = nb_chiots;
    actuelportee -> date_naissance = date_naissance;

    return actuelportee;
}

int main(){
    FILE *nom_chiens;
    FILE *chiots;

    if ((chiots = fopen("chiots.txt", "r")) == NULL){
        fclose(chiots);
        unsigned int test = 1;
        printf("%d \n", test);
        return 1;
    }

    unsigned int nombre_chiots = 0;
    char fichier_chiots;
    fichier_chiots = '1';

    fscanf(chiots, "%u\n", &nombre_chiots);
    fclose(chiots);

    if ((nom_chiens = fopen("nom_chien.txt", "r")) == NULL){
        fclose(nom_chiens);
        return 1;
    }

    unsigned int nombres_noms, compteur;

    fscanf(nom_chiens, "%u\n", &nombres_noms);
    char *tab_nom_chiens = malloc(sizeof(char[30]) * nombres_noms);

    for(compteur = 0; compteur < nombres_noms; compteur++){
        fscanf(nom_chiens, " %64[^\n]", &tab_nom_chiens[compteur]);
        printf("%s \n", &tab_nom_chiens[compteur]);
    }

    Chien *pere, *mere;
    pere = cree_chien(&tab_nom_chiens[2], 'M', '1');
    mere = cree_chien(&tab_nom_chiens[3], 'F', '1');

    Date *date = malloc(sizeof(Date) * 1);


    date -> jour = 3;
    date -> mois = 6;
    date -> annee = 2005;

    Portee *porte = malloc(sizeof(Portee) * 1);

    porte = cree_portee(pere -> nom, mere -> nom, nombre_chiots, &fichier_chiots, *date);

    printf("%s \n", &(*(porte -> pere) -> nom));

    fclose(nom_chiens);
    return 0;
}
