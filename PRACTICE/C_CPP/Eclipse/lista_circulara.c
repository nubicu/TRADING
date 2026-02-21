#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

struct El{
	int data;
	struct El *suc;
};

void inserare(struct El **cap, int val)
{
	struct El *p;
	p = (struct El*)malloc(sizeof(struct El));
	if(*cap == NULL)
	{
		p->data = val;
		p->suc = NULL;
		*cap = p;
	}
	else
	{
		p->data = val;
		p->suc = *cap;
		*cap = p;
	}
}

void afisare(struct El *cap)
{
	struct El *p = cap;

	if(cap == NULL)
		return;
	do
	{
		printf("%d ", p->data);
		p = p->suc;
	} while(p);

	printf("\n");
}

bool isCircular(struct El *cap)
{
	struct El *node;
	bool result;
	// An empty linked list is circular
  if (cap == NULL)
     result = true;
  // Next of head
  node = cap->suc;
  // This loop would stop in both cases (1) If Circular (2) Not circular
  while (node != NULL && node != cap)
     node = node->suc;
  // If loop stopped because of circular condition
  result = (node == cap);

	return result;
}

void invers(struct El ** cap)
{
	struct El *prev = 0, *current = *cap, *next = (*cap)->suc;

	// if list is empty
  if (*cap == NULL)
      return;
	do
	{
		next = current->suc;
		current->suc = prev;
		prev = current;
		current = next;
	} while(current != (*cap));

	// adjutsing the links so as to make the
  // last node point to the first node
  (*cap)->suc = prev;
  *cap = prev;
	printf("Gata invers\n");
}

void top(struct El *cap)
{
	printf("%d ", cap->data);
}

void parcurge(struct El *cap)
{
	struct El *p=cap;
	if(cap == NULL)
		printf("\n");
	else
	{
		printf("%d ",p->data);
		parcurge(p->suc);
		printf("%d ",p->data);
	}
}


int main(int argc, char* argv[])
{
	struct El *p, *r;
	p = NULL;
	int val;
	int opt;
	int n=0;
	printf("\nIntroduceti valoarea 0 pentru a termina editarea listei\n");
	printf("\nval=");
	scanf("%d",&val);
	while(val)
	{
		n++;
		inserare(&p,val);
		printf("val=");
		scanf("%d",&val);
	}
	afisare(p);
	do{
		printf("\n\t\tMENIU:\n");
		printf("\n\t0--parcurgere dus-intors");
		printf("\n\t1--are bucle?");
		printf("\n\t2--inversa");
		printf("\n\t3--exit");
		do{
			printf("\nIntroducetzi optiunea opt=");
			scanf("%d",&opt);
		}while(opt!=0 && opt!=1 && opt!=2 && opt!=3);
		switch(opt)
		{
			case 0:
				{
					parcurge(p);
					break;
				}
			case 1:
				{
					if(isCircular(p))
						printf("Circular list");
					else
						printf("Normal list");
					break;
				}
			case 2:
				{
					printf("Capul contine: ");
					top(p);
					invers(&p);
					printf("\nLista inversata: ");
				  afisare(p);
					break;
				}
			case 3:
				{
					printf("\nIesire");
					break;
				}
		}
	} while(opt != 3);
	return 0;
  }
