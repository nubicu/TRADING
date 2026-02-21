#include <fstream>
using namespace std;

int main() {
  ifstream fin("date_intrare.txt");
  ofstream fout("date_iesire.txt");
  int a,b;
  fin>>a>>b;
  fout<<a+b;
  return 0;
}
