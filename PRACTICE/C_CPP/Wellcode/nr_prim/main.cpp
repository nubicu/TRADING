#include <iostream>
#include <cmath>
using namespace std;

bool este_prim(int n)
{
    if (n < 2)
        return false;
    if (n == 2)
        return true;
    for(int i = 2; i <= sqrt(n); i++)
    {
        if (n % i == 0) // Daca N se divide la i
          return false; // Atunci N nu este prim
    }
    return true;
}

int invers(int x)
{
    int inv_x = 0;
    while(x>0)
    {
        inv_x = inv_x * 10 + x % 10;
        x /= 10;
    }
    return inv_x;
}

int main() {
  int N, inv_N;
  cin>>N;

  inv_N = invers(N);
  /*
  if (este_prim(inv_N))
    cout << inv_N << " este prim"<<endl;
  else
    cout << inv_N << " NU este prim"<<endl;
  if (este_prim(N))
    cout << N << " este prim" <<endl;
  else
    cout << N << " NU este prim"<<endl;
    */

  if ((este_prim(N) == true) && (este_prim(inv_N) == true))
    cout<<"DA"; // Numarul dat este prim
  else
    cout<<"NU"; // Numarul dat nu este prim

  return 0;
}
