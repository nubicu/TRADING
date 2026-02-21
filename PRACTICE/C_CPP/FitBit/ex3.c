//During development you discover that we need a generic map-like data structure. We would like to optimize for good insertion and access times. Since this is needed on an embedded system, the amount of memory available is fairly limited. Therefore, we would like it to behave like a cache when reaching a total number of entries given at initialization time (this is the maximum size).

//Define the needed C structures, then write the initialization, insertion and extraction functions.

#define MAXSIZE 10

struct h {
    int val;
    struct h* next;
}

struct hash {
    unsigned int hashcode;
    struct h *head;
}

struct hash ht[MAXSIZE];

void insertion(int val) {
    unsigned int hc = getHash(val);
    int ht_size = sizeof(ht) / sizeof(ht[0]);
    if(ht_size >= MAXSIZE) {
        extract();
    }
    struct h* tmp = malloc(sizeof(struct h));
    tmp->val = val;
    tmp->next = ht[hc].head;
    ht[hc].head = tmp;
}
