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

int main()
{
    int x, ctr = 0, n = 1, nr_cautat = 1;
    cin >> x;

    while(ctr<x)
    {
        ++n;
        if (este_prim(n) == true)
        {
            ctr++;
            nr_cautat = n;
        }
    }
    cout << nr_cautat;
    return 0;
}
