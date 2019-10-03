#include<stdio.h>

int main(){


    unsigned int pop_A = 0 , pop_B = 0, ans = 0;

    printf("Insérer la population A\n");
    scanf("%u",&pop_A);
    printf("Insérer la population B\n");
    scanf("%u",&pop_B);

    unsigned int population_alpha = pop_A , population_beta = pop_B , annees = ans;
    int augmentation_A = 500000;
    float augmentation_B = 0.03;

    while(population_beta <= population_alpha){
        population_alpha = population_alpha+ augmentation_A;
        population_beta = population_beta + (population_beta * augmentation_B);
        annees ++;
    };

    printf("%u\n",annees);

    population_alpha = pop_A;
    population_beta = pop_B;
    annees = ans;

    for( ; population_beta <= population_alpha; annees++){
        population_alpha = population_alpha + augmentation_A;
        population_beta = population_beta + (population_beta * augmentation_B);
    };

    printf("%u\n", annees);

    population_alpha = pop_A;
    population_beta = pop_B;
    annees = ans;

    do{
        if(population_beta <= population_alpha){
            population_alpha = population_alpha + augmentation_A;
            population_beta = population_beta + (population_beta * augmentation_B);
            annees ++;
        }
    }while(population_beta <= population_alpha);

    printf("%u\n", annees);
}