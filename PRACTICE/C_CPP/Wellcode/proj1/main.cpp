#include <iostream>
using namespace std;

int main()
{
    int a,b,c;
    cin>>a>>b>>c;
    if (a*a+b*b == c*c) // PITAGORA
        cout<<"DA";
    else
        cout<<"NU";

    return 0;
}

/*
    int a=2,b,c;
    a++;
    cout<<"a="<<a<<endl;
    b=a++;
    cout<<"a="<<a<<" b="<<b<<endl;
    c=a++;
    cout<<"a="<<a<<" b="<<b<<" c="<<c<<endl;
*/

// cout<<(a-b)*(a-b)*(a-b);
