#include <iostream>
using namespace std;

int main()
{
  int N, v[100001];
  cin>>N;
  for (int i = 1; i <= N; ++i)
    cin>>v[i];

  // Variabila sortat ne spune daca am gasit elemente in ordine descrescatoare
  // la pasul curent. Daca am gasit, atunci va mai trebui sa parcurgem sirul o
  // data si sa vedem daca mai exista si alte elemente in ordine descrescatoare
  // Initializam sortat cu 0 pentru ca inca nu am facut nici o cautare, deci nu
  // stim daca sirul este sortat
  int sortat = 0, aux, test=1, nr_intersch = 0;
  while (sortat == 0) {
        test++;
    // vom initializa sortat cu 0 cand gasim numere in ordine descrescatoare, in
    // cazul in care nu gasim, inseamna ca sirul este sortat si putem sa ne oprim
    sortat = 1;
    for (int i = 1; i < N; ++i)
      if (v[i] > v[i + 1]) {
        sortat = 0;
        // interschimbam pe v[i] cu v[i + 1]
        aux = v[i];
        v[i] = v[i + 1];
        v[i + 1] = aux;
        nr_intersch++;
      }
  }
  for (int i = 1; i <= N; ++i)
    cout<<v[i]<<' ';
  cout <<endl<<"nr test="<<test<<" nr interschimbari="<<nr_intersch<<endl;
  return 0;
}
