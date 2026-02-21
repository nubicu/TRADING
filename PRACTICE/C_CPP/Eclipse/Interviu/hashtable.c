#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

#define MAX_NAME 256
#define TABLE_SIZE 10
#define DELETED_NODE (person*)(0xFFFFFFFFFFFFFFFFUL)

typedef struct {
  char name[MAX_NAME];
  int age;
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
    } else if(hash_table[i] == DELETED_NODE){
      printf("\t%i\t---<deleted>\n", i);
    } else {
      printf("\t%i\t%s\n", i, hash_table[i]->name);
    }
  }
  printf("End\n");
}

bool hash_table_insert(person *p) {
  if (p == NULL) return false;
  int index = hash(p->name);
  for(int i=0; i< TABLE_SIZE; i++) {
    int try = (i+index)%TABLE_SIZE;
    if(hash_table[try] == NULL ||
      hash_table[try] == DELETED_NODE) {
      hash_table[try] = p;
      return true;
    }
  }
  return false;
}

person *hash_table_lookup(char *name) {
  int index = hash(name);
  for(int i=0; i< TABLE_SIZE; i++) {
    int try = (index + i) % TABLE_SIZE;
    if(hash_table[try] == NULL) {
      return false;
    }
    if(hash_table[try] == DELETED_NODE) continue;
    if(strncmp(hash_table[try]->name, name, TABLE_SIZE) == 0) {
      return hash_table[try];
    }
  }
  return NULL;
}

person *hash_table_delete(char * name) {
  int index = hash(name);
  for(int i=0; i< TABLE_SIZE; i++) {
    int try = (index + i) % TABLE_SIZE;
    if(hash_table[try] == NULL) {
      return false;
    }
    if(hash_table[try] == DELETED_NODE) continue;
    if(strncmp(hash_table[try]->name, name, TABLE_SIZE) == 0) {
        person *tmp = hash_table[try];
        hash_table[try] = NULL;
      return tmp;
    }
  }
  return NULL;
}

int main() {
  init_hash_table();
  //print_table();

  person jacob ={.name="Jacob", .age=25};
  person kate ={.name="Kate", .age=27};
  person roby ={.name="Roby", .age=34};
  person sara ={.name="Sara", .age=15};
  person edna ={.name="Edna", .age=17};
  person eliza ={.name="Eliza", .age=19};
  person maren ={.name="Maren", .age=23};
  person jane ={.name="Jane", .age=21};


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
