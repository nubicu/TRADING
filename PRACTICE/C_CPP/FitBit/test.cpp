#include <cstdlib>
#include <iostream>
#include <cstring>
using namespace std;

struct st {
  char a;
  char b;
  char c;
//  char d;
  int z;
  char e;
  char f;
};

main() {
  char s[] = "Aurel este";
  string str = "Salut Roby";
  struct st s1;

  cout << "Sizeof(s) = " << sizeof(s) << "\n";
  cout << "strlen(s) = " << strlen(s) << "\n";
  cout << "strlen(str) = " << str.length() << "\n";
  cout << "sizeof(struct)=" << sizeof(s1) << "\n";
}
