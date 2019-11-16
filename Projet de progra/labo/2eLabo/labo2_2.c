#include "/home/kieranvm/Downloads/Unif/Projet de progra/labo/util/util.h"

int main(){
    int *vecteur;
    int n;
    int max1,max2;

    printf("Entrez une valeur pour n:\n");
    scanf("%d", &n);

    // Remplit le tableau avec des valeurs aléatoires
    initR(&vecteur, n);

    int i = 0, s = n, diff_somme = 0, val_intermediaire = 0;
    max1 = vecteur[0];
    max2 = vecteur[0];

    if(n>1){
        max1 = vecteur[0];
        max2 = vecteur[1];

        if(max2 > max1){
            val_intermediaire = max1;
            max1 = max2;
            max2 = val_intermediaire;
        }
    }

    while(i<s-1){
        if(vecteur[i]>=max1)
            max1 = vecteur[i];
        else if(vecteur[i]>max2)
            max2 = vecteur[i];
        if(vecteur[s-1]>=max1)
            max1 = vecteur[s-1];
        else if(vecteur[s-1]>max2)
            max2 = vecteur[s-1];
        i ++;
        -- s;
    }
    if (i==s-1){
        if(vecteur[i]>max1)
            max1 = vecteur[i];
        else if(vecteur[i]>max2)
            max2 = vecteur[i];
    }

    // Imprime sur la sortie standard le contenu du tableau
    disp(vecteur, n);
    printf("%d\n", max1);
    printf("%d\n", max2);
    diff_somme = max1 - max2;
    printf("%d\n",  diff_somme);


}