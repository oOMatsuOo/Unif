#ifndef RPG_H
#define RPG_H

#define MAX_NAME 64
#define MAX_SLOTS 8

typedef struct materia_t{
  char name[MAX_NAME];
  int str, mag;
}Materia;

typedef struct weapon_t{
  char name[MAX_NAME];
  int str, dex, mag;
  int slots;
}Weapon;

typedef struct armor_t{
  char name[MAX_NAME];
  int vit, sp, luck;
  int slots;  
}Armor;

typedef struct character_t{
  char name[MAX_NAME];
  Weapon *weapon;
  Armor *armor;
  Materia *mat_w[MAX_SLOTS];
  Materia *mat_a[MAX_SLOTS];
  int str, dex, mag, vit, sp, luck;
}Character;

#endif
