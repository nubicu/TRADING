// C program for linked list implementation of stack
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>

// A structure to represent a stack
struct Element {
    int data;
    struct Element* next;
};

struct Element* newNode(int data)
{
    struct Element* stackNode = (struct Element*)malloc(sizeof(struct Element));
    stackNode->data = data;
    stackNode->next = NULL;
    return stackNode;
}

int isEmpty(struct Element* root)
{
    return !root;
}

void push(struct Element** root, int data)
{
    struct Element* stackNode = newNode(data);
    stackNode->next = *root;
    *root = stackNode;
    printf("%d pushed to stack\n", data);
}

int pop(struct Element** root)
{
    int popped;
    struct Element* temp;

    if (isEmpty(*root))
        return INT_MIN;
    temp = *root;
    *root = (*root)->next;
    popped = temp->data;
    free(temp);

    return popped;
}

int peek(struct Element* root)
{
    if (isEmpty(root))
        return INT_MIN;
    return root->data;
}

int main()
{
    struct Element* root = NULL;

    push(&root, 10);
    push(&root, 20);
    push(&root, 30);

    printf("%d popped from stack\n", pop(&root));

    printf("Top element is %d\n", peek(root));

    return 0;
}
