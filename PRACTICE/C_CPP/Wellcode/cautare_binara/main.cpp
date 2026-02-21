#include <iostream>
using namespace std;

int main()
{
  int N, v[100001], x;
  cin>>N;
  for (int i = 1; i <= N; ++i)
    cin>>v[i];
  cin>>x;

  // Prima data cautam in tot sirul, de la pozitia 1 pana la N
  int st = 1, dr = N, m;
  // Cat timp subsecventa are mai mult de un element, o injumatatim alegand
  // fie jumatatea din stanga, fie cea din dreapta
  while (st < dr) {
    m = (st + dr) / 2;
    cout << "St=" << st << " m=" << m << " dr=" << dr << endl;
    if (v[m] < x)
      st = m + 1;
    else
      dr = m;
  }
  cout << "St=" << st << " m=" << m << " dr=" << dr << endl;
  // am ajuns la o subsecventa cu un singur element
  if (v[st] == x)
    cout << "x se gaseste in sir pe pozitia " << st;
  else
    cout<<"x nu se gaseste in sir ";
  return 0;
}
