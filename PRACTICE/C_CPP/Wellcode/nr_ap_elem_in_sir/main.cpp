#include <iostream>
using namespace std;

int main()
{
  int N, M, v[1001], AP[1001];
  cin>>N>>M;
  // Initializam cu 0 fiecare pozitie pentru a putea numara aparitiile
  for (int i = 1; i <= M; ++i)
    AP[i] = 0;

  for (int i = 1;i <= N; i++)
    cin>>v[i];
  // Actualizam sirul de aparitii
  for (int i = 1; i <= N; ++i)
    ++AP[v[i]];// Crestem numarul de aparitii ale elementului v[i]
  for (int i = 1; i <= M; ++i)
    cout<<"Elementul "<<i<<" apare de "<<AP[i]<<" ori\n";
  return 0;
}
