#include <stdio.h>
#include <string.h>
#include <stdlib.h>
/* Exercitiu 1 : macrouri
#define MY_DIV(a, b, c)    ((a + (b) / (c))

int main(void) {
  int a = 13;
  int b = 17;
  int c = 4;

  unsigned int x = 2;
  int y = -10;

  (x + y > 0)?puts("greater than 0"):puts("less than 1");

  printf("%d\n", ( (a + (b) / (c + 1) ) ) );
  //printf("%d\n", MY_DIV(a, b, c+1));

	return 0;
}
*/
/* Exercitiu 2 : string
int main(int argc, char *argv[]) {
        char *buffer = (char*)malloc(16);
        char *p = (char*)malloc(sizeof(char));
        printf("Enter password: ");
        fgets(buffer, sizeof(buffer), stdin);
        if( (p=strchr(buffer, '\n')) != NULL )
            *p='\0';

        if (strcmp(buffer, "fitbit") == 0) {   // strcmp to be used; problem with assignment operator(should be equality operator)
                printf("CORRECT\n");
        } else {
                printf("WRONG\n");
        }

        free(buffer);
        free(p);
        return 0;
} */
/*
int main(){
  int i=2, j=3, res;
  printf("res = %u+++%u = ",i,j);
  res = i+++j;
  printf(" %u\n", res);

  return 0;
}
*/

#include <stdio.h>
#include <string.h>

int main () {
   const char src[50] = "http://www.tutorialspoint.com";
   char dest[50];

   strcpy(dest,"Heloooo!!");
   printf("Before memcpy dest = %s\n", dest);
   memcpy(dest, src, strlen(src)+1);
   printf("After memcpy dest = %s\n", dest);

   return(0);
}
