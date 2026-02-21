#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

#define MAX_NAME 256
#define TABLE_SIZE 10

typedef struct pers{
  char name[MAX_NAME];
  int age;
  struct pers *next;
} person;

person *hash_table[TABLE_SIZE];

unsigned int hash(char *name) {
  int length = strnlen(name, MAX_NAME);
  unsigned int hash_value = 0;

  for(int i = 0; i < length; i++) {
    hash_value += name[i];
    hash_value = (hash_value * name[i]) % TABLE_SIZE;
  }
  return hash_value;
}

void init_hash_table() {
  for(int i = 0; i < TABLE_SIZE; i++) {
    hash_table[i] = NULL;
  }
  // table is empty
}

void print_table() {
  printf("Start\n");
  for (int i = 0; i < TABLE_SIZE; i++) {
    if(hash_table[i] == NULL) {
      printf("\t%i\t---\n", i);
    } else {
      printf("\t%i\t ", i);
      person *tmp = hash_table[i];
      while(tmp != NULL) {
        printf("%s - ", tmp->name);
        tmp = tmp->next;
      }
      printf("\n");
    }
  }
  printf("End\n");
}

bool hash_table_insert(person *p) {
  if (p == NULL) return false;
  int index = hash(p->name);
  p->next = hash_table[index];
  hash_table[index] = p;
  return true;
}

person *hash_table_lookup(char *name) {
  int index = hash(name);
  person *tmp = hash_table[index];
  while(tmp != NULL && strncmp(hash_table[index]->name, name, TABLE_SIZE) != 0) {
    tmp = tmp->next;
  }
  return tmp;
}

person *hash_table_delete(char * name) {
  int index = hash(name);
  person *tmp = hash_table[index];
  person *prev = NULL;
  while(tmp != NULL && strncmp(hash_table[index]->name, name, TABLE_SIZE) == 0) {
    prev = tmp;
    tmp = tmp->next;
  }
  if(tmp == NULL) return NULL;
  if(prev == NULL) {
    // delete insert_at_head
    hash_table[index] = tmp->next;
  } else {
    prev->next = tmp->next;
  }
  return tmp;
}

int main() {
  init_hash_table();

  person jacob = {.name="Jacob", .age=25};
  person kate = {.name="Kate", .age=27};
  person roby = {.name="Roby", .age=34};
  person sara = {.name="Sara", .age=15};
  person edna = {.name="Edna", .age=17};
  person eliza = {.name="Eliza", .age=19};
  person maren = {.name="Maren", .age=23};
  person jane = {.name="Jane", .age=21};

  hash_table_insert(&jacob);
  hash_table_insert(&kate);
  hash_table_insert(&roby);
  hash_table_insert(&sara);
  hash_table_insert(&edna);
  hash_table_insert(&maren);
  hash_table_insert(&eliza);
  hash_table_insert(&jane);

  print_table();

  person *tmp = hash_table_lookup("Roby");
  if (tmp == NULL) {
    printf("Not found!\n");
  } else {
    printf("Found %s.\n", tmp->name);
  }

  tmp = hash_table_lookup("George");
  if (tmp == NULL) {
    printf("Not found!\n");
  } else {
    printf("Found %s.\n", tmp->name);
  }

  hash_table_delete("Kate");
  print_table();

  return 0;
}
