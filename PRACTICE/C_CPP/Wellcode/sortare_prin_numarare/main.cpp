#include <iostream>
using namespace std;

int main()
{
  int N, v[100001], fr[100];
  cin>>N;
  // Initializam intai fiecare pozitie din vectorul de frecventa cu 0
  for (int i = 1; i < 100; ++i)
    fr[i] = 0;
  for (int i = 1; i <= N; ++i) {
    cin>>v[i];
    ++fr[v[i]];// crestem frecventa elementului v[i]
  }

  for (int i = 1; i < 100; ++i)
    for (int j = 1; j <= fr[i]; ++j)
      cout<<i<<' ';
  return 0;
}
