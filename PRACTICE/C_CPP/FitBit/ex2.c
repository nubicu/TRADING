//You need to transfer money from one bank account to another. Implement it in a thread safe manner.

struct account {
    int balance;
    int id;
    sem_t sem_ac;
}

void transfer(struct account *from, struct account *to,
                int amount) {
        if(from->id > to->id) {
            sem_wait(from->sem_ac);
            sem_wait(to->sem_ac);
            if (from->balance >= amount) {
                    from->balance -= amount;
                    to->balance += amount;
            }
            sem_post(from->sem_ac);
            sem_post(to->sem_ac);
        } else  if(to->id > from->id) {
            sem_wait(to->sem_ac);
            sem_wait(from->sem_ac);
            if (from->balance >= amount) {
                    from->balance -= amount;
                    to->balance += amount;
            }
            sem_post(from->sem_ac);
            sem_post(to->sem_ac);
        }
}


void thread1()
{
    transfer(a,b);
}
void thread2()
{
    transfer(b,a);
}
