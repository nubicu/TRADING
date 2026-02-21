#include <iostream>
using namespace std;
// Sortare crescator
int main() {
    int a,b,c;
    cin>>a>>b>>c;
    if (a < b) {
        if (b < c)
            cout<<a<<" "<<b<<" "<<c;
        else if (a < c)
            cout<<a<<" "<<c<<" "<<b;
        else
            cout<<c<<" "<<a<<" "<<b;
    }
    if (a >= b) {
        if (a < c)
            cout<<b<<" "<<a<<" "<<c;
        else if (b<c)
            cout<<b<<" "<<c<<" "<<a;
        else
            cout<<c<<" "<<b<<" "<<a;
    }
    return 0;
}
/*
a<b && b>c && a<c => a<c<b
a<b && b>c && c<a => c<a<b

b<a && a<c => b<a<c
a>b && a>c && c>b => b<c<a
a>b && a>c && b>c => c<b<a
*/
