#include <stdio.h>
#include <stdlib.h>

typedef struct node {
  int value;
  struct node* next;
} node_t;

void printList(node_t *head) {
  node_t *temp = head;
  while (temp != NULL) {
    printf("%d->", temp->value);
    temp = temp->next;
  }
  printf("NULL\n");
}

node_t *create_new_node(int value) {
  node_t *result = malloc(sizeof(node_t));
  result->value = value;
  result->next = NULL;
  return result;
}

void insert_at_head(node_t **head, node_t *node_to_insert) {
  node_to_insert->next = *head;
  *head = node_to_insert;
}

void insert_after_node(node_t *node_to_insert_after, node_t *newnode) {
  newnode->next = node_to_insert_after->next;
  node_to_insert_after->next = newnode;
}

node_t *find_node(node_t *head, int value) {
  node_t *tmp = head;
  while(tmp != NULL) {
    if(tmp->value == value) return tmp;
    tmp = tmp->next;
  }

  return NULL;
}

void reverse_list(node_t **head) {
  node_t *prev = NULL, *current = (*head), *urm = (*head)->next;

  if((*head) == NULL) return;

  do {
    current->next = prev;
    prev = current;
    current = urm;
    urm = current->next;
  } while (urm != NULL);

  current->next = prev;
  (*head) = current;
}

int main() {
  node_t *head = NULL;
  node_t *tmp;
  int find_value;

  for(int i = 0; i < 25; i++) {
    tmp = create_new_node(i);
    insert_at_head(&head, tmp);
  }

  find_value = 50;
  tmp = find_node(head, find_value);
  if(tmp == NULL) {
    printf("Node with value %d was not found!\n", find_value);
  }
  else {
    printf("Found node with value %d\n", tmp->value);
    insert_after_node(tmp, create_new_node(75));
  }

  printf("\nLista inainte de inversare:\n");
  printList(head);

  reverse_list(&head);
  printf("\nLista dupa inversare:\n");
  printList(head);

  free(tmp);
  free(head);

  return 0;
}
