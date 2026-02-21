#include <iostream>
using namespace std;

int main()
{
    int n, i = 0;
    cin >> n;
    int v[n];
    for (i = 1; i <= n; i++)
    {
        cin >> v[i];
        if(i%2 != 0)
            v[i] -= 1;
        else
            v[i] *= 2;
    }

    for (i = 1; i < n; i++)
        cout << v[i] << " ";
    cout << v[i];

    return 0;
}
