#include <iostream>
using namespace std;

int main()
{
    int n;
    cin >> n;
    if ( n % 2 == 0)
        cout << "fizz";
    if ( n % 3 == 0)
        cout << "buzz";
    return 0;
}
