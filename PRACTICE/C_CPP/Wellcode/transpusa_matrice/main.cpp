#include <iostream>
#include <fstream>
using namespace std;

int main() {
  int linii, coloane, mat[35][35];
  int linii_transpusa, coloane_transpusa, transpusa[35][35];
  int i,j;
  ifstream fin("di_transpusa_matrice.txt");
  ofstream fout("do_transpusa_matrice.txt");
  // Citire
  fin>>linii>>coloane;
  for (i = 1; i <= linii; ++i)
    for (j = 1; j <= coloane; ++j)
      fin>>mat[i][j];
  // Calculare transpusa
  linii_transpusa = coloane;
  coloane_transpusa = linii;
  for (i = 1; i <= linii; ++i)
    for (j = 1; j <= coloane; ++j) {
      // linia i devine coloana i, coloana j devine linia j
      // asta inseamna ca elementul care a fost pe linia i, coloana j
      // va ajunge pe coloana i, linia j
      transpusa[j][i] = mat[i][j];
    }
  for (i = 1; i <= linii_transpusa; ++i) {
    for (j = 1; j <= coloane_transpusa; ++j)
      fout<<transpusa[i][j]<<" ";
    fout<<"\n";
  }
  return 0;
}
