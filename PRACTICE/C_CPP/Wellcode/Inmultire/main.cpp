#include <iostream>
using namespace std;

int cifreImpare(unsigned int n)
{
    int c, n_invers = 0, contor = 0; //Declaram variabilele
    //Facem un contor sa numaram cate cifre impare are numarul nostru
    while(n)
    {
        c = n % 10; //Aflam in "c" cifra curenta
        if(c % 2 == 0) //Daca aceasta este para, formam inversul numarului
            n_invers = n_invers * 10 + c;
        else //Daca aceasta este impara o adaugam la contor
            contor++; //Crestem contorul cu o unitate
        n = n / 10; //Stergem ultima cifra din numar
    }
    if(contor == 0 || n_invers == 0) //Daca nu avem cifre impare returnam -1
        return -1;
    while(n_invers) //Acum intoarcem numarul nostru, la forma lui initiala
    {
        c = n_invers % 10;
        n = n * 10 + c;
        n_invers = n_invers / 10;
    }
    return n;
}

int main()
{
    int a,b,i;
    cin >> a >> b;

    for (i=1;i<b;i++)
    {
        cout << a*i << " ";
    }
    cout << a*i;

    return 0;
}
