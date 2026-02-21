#include <iostream>
using namespace std;

int main() {
    int N, i, j = 1;
    cin>>N;
    int v[N], rez[N];
    for (i = 1; i <= N; ++i)
    {
        cin>>v[i];
        if (v[i] % 2 == 0){ // nr pare
            rez[j] = v[i];
            j++;
        }
    }

    for (i = N; i > 0; i--) // parcurgere vector in ordine inversa
    {
        if (v[i] % 2 != 0){ // nr impare
            rez[j] = v[i];
            j++;
        }
    }

    for (i = 1; i <= N; ++i)
        cout << rez[i] << " ";

    return 0;
}
