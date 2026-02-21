#include <iostream>
using namespace std;

int main() {
    int x, inv_x = 0;
    cin >> x;
    while(x>0)
    {
        inv_x = inv_x * 10 + x % 10;
        x /= 10;
    }
    cout<<inv_x;
    return 0;
}
