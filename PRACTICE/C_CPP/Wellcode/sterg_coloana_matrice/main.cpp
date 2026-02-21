#include <iostream>
using namespace std;

int main() {
  int linii, coloane, sterg;
  int i,j;
  // Citire
  cin>>linii>>coloane>>sterg;
  int mat[linii+1][coloane+1];
  for (i = 1; i <= linii; ++i)
    for (j = 1; j <= coloane; ++j)
      cin>>mat[i][j];
  for (i = 1; i <= linii; ++i) {
    for (j = 1; j <= coloane; ++j)
        if (j!=sterg){
            cout<<mat[i][j]<<" ";
        }
    cout<<"\n";
  }
  return 0;
}
