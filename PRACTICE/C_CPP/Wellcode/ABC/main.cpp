#include <iostream>

using namespace std;

// Un numar natural se numeste ABC daca are exact a cifre, prima cifra este b si ultima cifra este c.
int main()
{
    int a,b,c,x, x_copy;
    int ult_cif, prima_cif, nr_cifre = 0;
    cin >> a >> b >> c >> x;
    x_copy = x;

    ult_cif = x % 10;

    while (x>0)
    {
        ++nr_cifre;
        prima_cif = x % 10;
        x /= 10;
    }

    if ((nr_cifre == a) && (ult_cif == c) && (prima_cif == b))
        cout << "DA";
    else
        cout << "NU";
    /*
    cout << "x = " << x_copy << endl;
    cout << "Ultima cifra a numarului este " << ult_cif << endl;
    cout << "Prima cifra a numarului este " << prima_cif << endl;
    cout << "Numarul de cifre este " << nr_cifre << endl;
    */
    return 0;
}
