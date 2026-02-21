/* Write a function to move all 0 numbers to the beginning of an array, but not change the sequence of non-0 numbers. */

#include <stdio.h>
#include <stdlib.h>

#define ARR_LEN 12

void change(int * arr, int n)
{
  int *temp = (int*)malloc(n*sizeof(int));
  int j = 0, i = 0;

  for(j=0;j<n;j++)  {
    if(0 == arr[j]) {
      temp[i] = 0;
      i++;
    }
  }
  for(j=0;j<n;j++) {
    if(arr[j] != 0) {
      temp[i] = arr[j];
      i++;
    }
  }
  for(j=0; j<n; j++)
  {
    arr[j] = temp[j];
  }
}

void change2(int ** arr, int n)
{
  int *temp = (int*)malloc(n*sizeof(int));
  int j = 0, i = 0;

  for(j=0;j<n;j++)  {
    if(0 == (*arr)[j]) {
      temp[i] = 0;
      i++;
    }
  }
  for(j=0;j<n;j++) {
    if((*arr)[j] != 0) {
      temp[i] = (*arr)[j];
      i++;
    }
  }
  (*arr) = temp;
}

void print_array(int *arr, int n)
{
  int i = 0;
  for (i=0; i<n; i++) {
    printf("%d ", arr[i]);
  }
  printf("\n");
}

int main(void)
{
  int *a = calloc(ARR_LEN, sizeof(int));
  int i =0;

  for(i=0; i<ARR_LEN; i++)
  {
    scanf("%d", &a[i]);
  }

  printf("Initial array: ");
  print_array(a, ARR_LEN);

  //change(a, ARR_LEN);
  change2(&a, ARR_LEN);
  printf("Array after move: ");
  print_array(a, ARR_LEN);

  return 0;
}
