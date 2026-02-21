#include <pthread.h>
#include <stdio.h>

/* parameter structure for every thread */
struct cont {
	char character; /* printed character */
	int number;     /* how many times */
};

/* the function performed by every thread */
void* print_character(void *params)
{
	struct cont *p = (struct cont *) params;
	int i;

	for (i = 0; i < p->number; i++)
		printf("%c", p->character);
	printf("\n");

	return NULL;
}

int main()
{
	pthread_t fir1, fir2;
	struct cont fir1_args, fir2_args;

	/* create one thread that will print 'x' 11 times */
	fir1_args.character = 'x';
	fir1_args.number = 5;
	if (pthread_create(&fir1, NULL, &print_character, &fir1_args)) {
		perror("pthread_create");
		return 1;
	}

	/* create one thread that will print 'y' 13 times */
	fir2_args.character = 'y';
	fir2_args.number = 13;
	if (pthread_create(&fir2, NULL, &print_character, &fir2_args)) {
		perror("pthread_create");
		return 1;
	}

	/* wait for completion */
	if (pthread_join(fir1, NULL))
		perror("pthread_join");
	if (pthread_join(fir2, NULL))
		perror("pthread_join");

	return 0;
}
