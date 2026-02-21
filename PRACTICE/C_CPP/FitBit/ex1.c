#include <assert.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Complete the 'reorder' function below.

void reorder(int *number_sequence, size_t count)
{
    int countZeros = 0, i = 0;

    for(i = count-1; i >= 0; i--) {
        if(number_sequence[i] == 0) {
            countZeros++;
        } else {
            number_sequence[i + countZeros] = number_sequence[i];
        }
    }
    for(i = 0; i < countZeros; i++){
        number_sequence[i] = 0;
    }
}

void read_sequence(FILE* f, int **number_sequence, size_t *count)
{
    if (f == NULL || number_sequence == NULL || count == NULL)
    {
        return;
    }

    fscanf(f, "%d", count);
    *number_sequence = (int*) malloc(*count * sizeof (int));
    if (*number_sequence == NULL)
    {
        return;
    }

    int *elem = *number_sequence;
    for (int i = 0; i < *count; i++)
    {
        fscanf(f, "%d", elem);
        elem++;
    }

    return;
}

void write_sequence(FILE* f, int *number_sequence, size_t count)
{
    if (number_sequence == NULL || count == 0 || f == NULL)
    {
        return;
    }
    for (int i = 0; i < count; i++)
    {
        fprintf(f, "%d ", number_sequence[i]);
    }
}
int main()
{
    int *number_sequence = NULL;
    size_t count = 0;
    read_sequence(stdin, &number_sequence, &count);
    reorder(number_sequence, count);
    write_sequence(stdout, number_sequence, count);
    return 0;
}
