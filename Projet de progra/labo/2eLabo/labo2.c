#include "/home/kieranvm/Downloads/Unif/Projet de progra/labo/util/util.h"

int main(){
    int *vecteur;
    int n;
    int min;

    printf("Entrez une valeur pour n:\n");
    scanf("%d", &n);

    // Remplit le tableau avec des valeurs aléatoires
    initR(&vecteur, n);

    int i = 1, s = n;
    min = vecteur[0];

    while(i<s-1){
        if(vecteur[i]<min)
            min = vecteur[i];
        if(vecteur[s-1]<min)
            min = vecteur[s-1];
        i ++;
        -- s;
    }
    if (i==s-1){
        if(vecteur[i]<min)
            min = vecteur[i];
    }

    // Imprime sur la sortie standard le contenu du tableau
    disp(vecteur, n);
    printf("%d\n", min);

}