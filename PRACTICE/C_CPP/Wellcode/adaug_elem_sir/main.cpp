#include <iostream>
using namespace std;

int main() {
    int N, i;
    cin>>N;
    int v[N];
    for (i = 1; i <= N; ++i) // Citim sirul
        cin>>v[i];
    int x,p; // Numarul si pozitia pe care sa fie inserat
    cin>>x>>p;
    ++N; // Crestem lungimea sirului
    for (i = N; i > p; --i) // Mutam elementele cu o pozitie la dreapta
        v[i]=v[i-1];
    v[p]=x;
    for (i = 1; i <= N; ++i) // Afisam sirul
        cout<<v[i]<<' ';
    return 0;
}
