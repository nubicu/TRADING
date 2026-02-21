#include <iostream>
using namespace std;

int main() {
  int n;
  cin>>n;
  int i = 1, copie, sum_cif;
  while (i <= n) {
    // ii facem o copie lui i pentru a nu pierde valoarea lui cand ii
    // calculam suma cifrelor
    copie = i;
    sum_cif = 0;
    // calculam suma cifrelor
    while (copie > 0) {
      sum_cif += copie % 10;
      copie /= 10;
    }
    if (sum_cif % 2 == 0)
      cout<<i<<' ';
    ++i;
  }
  return 0;
}
