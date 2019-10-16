#ifndef UTIL_H
#define UTIL_H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void initR(int** arr, int n) {
  srand(time(0));
  *arr = (int*)malloc(n*sizeof(int));
  int i;
  for (i = 0; i < n; i++)
    (*arr)[i] = rand() % 100;
}

void init2dR(int*** arr, int n) {
  srand(time(0));
  *arr = (int**)malloc(n*sizeof(int*));
  int i, j;
  for (i = 0; i < n; i++) {
    (*arr)[i] = (int*)malloc(n*sizeof(int));
    for (j = 0; j < n; j++)
      (*arr)[i][j] = rand() % 100;
  }
}

void initZ(int** arr, int n) {
  *arr = (int*)malloc(n*sizeof(int));
  int i;
  for (i = 0; i < n; i++)
    (*arr)[i] = 0;
}

void init2dZ(int*** arr, int n) {
  *arr = (int**)malloc(n*sizeof(int*));
  int i, j;
  for (i = 0; i < n; i++) {
    (*arr)[i] = (int*)malloc(n*sizeof(int));
    for (j = 0; j < n; j++)
      (*arr)[i][j] = 0;
  }
}

void disp(int* arr, int n) {
  int i;
  for (i = 0; i < n; i++)
    printf("%2d ", arr[i]);
  printf("\n");
}

void disp2d(int** arr, int n) {
  int i, j;
  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++)
      printf("%2d ", arr[i][j]);
    printf("\n");
  }
}

int min(int a, int b) {
  return a < b ? a : b;
}

int max(int a, int b) {
  return a > b ? a : b;
}

#endif