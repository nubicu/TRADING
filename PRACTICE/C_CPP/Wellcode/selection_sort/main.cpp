#include <iostream>
using namespace std;

int main() {
    int N, v[100], i, j, aux, nr_intersch = 0;
    cin>>N;
    for (i = 1; i <= N; ++i) // Citim sirul
        cin>>v[i];
    for (i = 1; i < N; ++i)
        for (j = i + 1; j <= N; ++j) // Cautam elemente mai mici decat v[i]
            if (v[i] > v[j]) { // Am gasit un element mai mic
                // Punem valoarea din v[j] in v[i] si din v[i] in v[j]
                aux = v[i];
                v[i] = v[j];
                v[j] = aux;
                nr_intersch++;
            }
    for (i = 1; i <= N; ++i) // Afisam sirul
        cout<<v[i]<<' ' ;

    cout << endl << "Numar interschimbari = " << nr_intersch << endl;
    return 0;
}
