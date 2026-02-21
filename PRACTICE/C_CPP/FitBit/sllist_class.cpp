#include <iostream>
#include <string>
#include <cstdlib>
using namespace std;

class dbinlob {
public:
  char info; // informatii
  dbinlob *urmator; // pointer spre obiectul urmator
  dbinlob() {
    info = 0;
    urmator = NULL;
  }
  dbinlob(char c) {
    info = c;
    urmator = NULL;
  }
  dbinlob *daurmator() { return urmator; }
  void dainfo(char &c) { c = info; }
  void schimba(char c) { info = c; } // modifica un element

  // Supraincarca << pt obiecte de tip dbinlob
  friend ostream &operator<<(ostream &stream, dbinlob o) {
    stream << o.info << "\n";
    return stream;
  }

  // Supraincarca << pt pointeri spre obiecte de tip dbinlob
  friend ostream &operator<<(ostream &stream, dbinlob *o) {
    stream << o->info << "\n";
    return stream;
  }

  // Supraincarca >> pt referinte dbinlob
  friend istream &operator>>(istream &stream, dbinlob &o) {
    cout << "Introduceti infrmatiile: ";
    stream >> o.info;
    return stream;
  }
};

class sllist : public dbinlob {
  dbinlob *incep;
public:
  sllist() { incep = NULL; }
  void memo(char c);
  void indep(dbinlob *ob); // scoate elementul
  void inceplist(); // afiseaza lista de la inceput spre sfarsit
  dbinlob *gaseste(char c); // returneaza pointer spre elementul cautat
  dbinlob *daincep() { return incep; }
};

// Adauga urmatoarea intrare
void sllist::memo(char c) {
  dbinlob *p;
  p = new dbinlob;
  if(!p) {
    cout << "Eroare de alocare!\n";
    exit(1);
  }
  p->info = c;

  if(incep == NULL) { //primul element din Lista
    incep = p;
  } else { // pune la sfarsit
      p->urmator = incep;
      incep = p;
  }
}

// Indeparteaza un element din lista si reactualizeaza pointerii incep si sfars
void sllist::indep(dbinlob *ob) {
  dbinlob *temp;
  temp = incep;
  while (temp->urmator) {
    if (ob->info == temp->urmator->info) {
      // Sunt pe pozitia dinaintea elementului care trebuie eliminat
      // si nu este ultimul element din lista
      temp->urmator = ob->urmator;
      delete ob;
    }
    temp = temp->daurmator();
  }
}

// Parcurge lista de la inceput la sfarsit
void sllist::inceplist() {
  dbinlob *temp;
  temp = incep;

  if (!temp) {
    cout << "Lista este goala!\n";
    return;
  }

  do {
    cout << temp->info << " ";
    temp = temp->daurmator();
  } while (temp);
  cout << "\n";
}

// Gaseste un obiect pe baza informatiilor sale
dbinlob *sllist::gaseste(char c) {
  dbinlob *temp;
  temp = incep;
  while (temp) {
    if (c == temp->info) return temp; // gasit
    temp = temp->daurmator();
  }
  return NULL;
}

main() {
  sllist lista;
  char c;
  dbinlob *p;

  lista.memo('1');
  lista.memo('2');
  lista.memo('3');

  // foloseste functiile membre pt a afisa lista
  cout << "Iata lista de la inceput:\n";
  lista.inceplist();
  cout << "\n";

  // parcurge lista "manual"
  cout << "Parcurgere manuala a listei\n";
  p = lista.daincep();
  while(p) {
    p->dainfo(c);
    cout << c << " ";
    p = p->daurmator();
  }
  cout << "\n\n";

  // cauta un element
  cout << "Cauta elementul 2\n";
  p = lista.gaseste('2');
  if(p) {
    p->dainfo(c);
    cout << "Am gasit: " << c << "\n";
  }
  cout << "\n";


  // scoate un element
  p->dainfo(c);
  cout << "Scoate elementul " << c << "\n";
  lista.indep(p);
  cout << "Iata lista de la inceput \n";
  lista.inceplist();
  cout << "\n";

  // adauga o alta intrare
  cout << "Adauga un element\n";
  lista.memo('4');
  cout << "Iata lista de la inceput\n";
  lista.inceplist();
  cout <<"\n";

  // modifica informatiile
  p = lista.gaseste('1');
  if(!p) {
    cout << "Eroare! Elementul nu a fost gasit!\n";
    return 1; // eroare
  }

  p->dainfo(c);
  cout << "Modifica " << c << " in 5\n";
  p->schimba('5');
  cout << "Iata lista de la inceput:\n";
  lista.inceplist();
  cout <<"\n";

  // ilustreaza << si >>
  cin >> *p;
  cout << p;

  cout << "Iata lista de la inceput\n";
  lista.inceplist();
  cout << "\n";

  // scoate primul element al listei
  cout << "Dupa indepartarea inceputului listei:\n";
  p = lista.daincep();
  lista.indep(p);
  lista.inceplist();
  cout << "\n";

  return 0;
}
