#include <iostream>
using namespace std;

int main() {
    int N, v[100], i;
    cin>>N;
    for (i = 1; i <= N; ++i) // Citim sirul
        cin>>v[i];
    int p; // Pozitia de pe care vrem sa stergem
    cin>>p;
    for (i = p; i < N; ++i) // Mutam elementele cu o pozitie la stanga
        v[i]=v[i+1];
    --N; // Scadem lungimea sirului
    for (i = 1; i <= N; ++i) // Afisam sirul
        cout<<v[i]<<' ';
    return 0;
}
