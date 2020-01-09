#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include "rpg.h"


int main(){

    FILE *armes;
    FILE *materia;
    FILE *armure;
    FILE *player;

    if ((armes = fopen("armor.dat","r")) == NULL)
    {
        fprintf(stderr,"Impossible d'ouvrir le fichier données en lecture\n");

        fclose(armes);

        exit(1);
    }

    if ((armure = fopen("weapon.dat","r")) == NULL)
    {
        fprintf(stderr,"Impossible d'ouvrir le fichier données en lecture\n");

        fclose(armes);
        fclose(armure);

        exit(1);
    }

    if ((materia = fopen("materia.dat","r")) == NULL)
    {
        fprintf(stderr,"Impossible d'ouvrir le fichier données en lecture\n");

        fclose(armes);
        fclose(materia);
        fclose(armure);

        exit(1);
    }

    unsigned int nombres_armes = 0, nombres_armure = 0, nombres_materia = 0;

    fscanf(armes, "%u\n", &nombres_armes);
    Weapon *tab_armes = malloc(sizeof(Weapon) * nombres_armes);

    fscanf(armure, "%u\n", &nombres_armure);
    Armor *tab_armure = malloc(sizeof(Armor) * nombres_armure);

    fscanf(materia, "%u\n", &nombres_materia);
    Materia *tab_materia = malloc(sizeof(Materia) * nombres_materia);

    unsigned int compteur = 0;

    for(compteur = 0; compteur < nombres_armes; compteur ++){

        fscanf(armes, " %64[^\n] %d %d %d\n%d", tab_armes[compteur].name , &tab_armes[compteur].str, &tab_armes[compteur].dex, &tab_armes[compteur].mag, &tab_armes[compteur].slots);
        printf("%s\n", tab_armes[compteur].name);

    }


    for(compteur = 0; compteur < nombres_armure; compteur ++){

        fscanf(armure, " %64[^\n] %d %d %d\n%d", tab_armure[compteur].name , &tab_armure[compteur].vit, &tab_armure[compteur].sp, &tab_armure[compteur].luck, &tab_armes[compteur].slots);
        printf("%s\n", tab_armure[compteur].name);

    }

    for(compteur = 0; compteur < nombres_materia; compteur ++){

        fscanf(materia, " %64[^\n] %d %d", tab_materia[compteur].name , &tab_materia[compteur].str, &tab_materia[compteur].mag);
        printf("%s\n", tab_materia[compteur].name);

    }

    if ((player = fopen("player.dat","r")) == NULL)
    {
        fprintf(stderr,"Impossible d'ouvrir le fichier données en lecture\n");

        fclose(armes);
        fclose(materia);
        fclose(armure);
        fclose(player);

        exit(1)
    }

    
    fclose(armes);
    fclose(materia);
    fclose(armure);

}