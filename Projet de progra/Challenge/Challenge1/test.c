#include<stdio.h>

int main(){


    unsigned int pop_A = 1000000 , pop_B = 34, ans = 0;
    unsigned int sims_A = pop_A , sims_B = pop_B , annees = ans;
    int augmentation_A = 500000;
    float augmentation_B = 0.03;

    while(sims_B < sims_A){
        sims_A += augmentation_A;
        sims_B = sims_B + (sims_B * augmentation_B);
        annees ++;
    };

    printf("%u\n",annees);

    sims_A = pop_A;
    sims_B = pop_B;
    annees = ans;

    for( ; sims_B < sims_A; annees++){
        sims_A += augmentation_A;
        sims_B = sims_B + (sims_B * augmentation_B);
    };

    printf("%u\n", annees);

    sims_A = pop_A;
    sims_B = pop_B;
    annees = ans;

    do{
        sims_A += augmentation_A;
        sims_B = sims_B + (sims_B * augmentation_B);
        annees ++;
    }while(sims_B < sims_A);

    printf("%u\n", annees);
}