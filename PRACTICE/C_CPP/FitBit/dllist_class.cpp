#include <iostream>
#include <string>
#include <cstdlib>
using namespace std;

class dbinlob {
public:
  char info; // informatii
  dbinlob *urmator; // pointer spre obiectul urmator
  dbinlob *anterior; // pointer spre obiectul anterior
  dbinlob() {
    info = 0;
    urmator = NULL;
    anterior = NULL;
  }
  dbinlob(char c) {
    info = c;
    urmator = NULL;
    anterior = NULL;
  }
  dbinlob *daurmator() { return urmator; }
  dbinlob *daanterior() { return anterior; }
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

class dllist : public dbinlob {
  dbinlob *incep, *sfars;
public:
  dllist() { incep = sfars = NULL; }
  void memo(char c);
  void indep(dbinlob *ob); // scoate elementul
  void inceplist(); // afiseaza lista de la inceput spre sfarsit
  void sfarslist(); // afiseaza lista de la sfarsit spre inceput
  dbinlob *gaseste(char c); // returneaza pointer spre elementul cautat
  dbinlob *daincep() { return incep; }
  dbinlob *dasfars() { return sfars; }
};

// Adauga urmatoarea intrare
void dllist::memo(char c) {
  dbinlob *p;
  p = new dbinlob;
  if(!p) {
    cout << "Eroare de alocare!\n";
    exit(1);
  }
  p->info = c;

  if(incep == NULL) { //primul element din Lista
    sfars = incep = p;
  } else { // pune la sfarsit
      p->anterior = sfars;
      sfars->urmator = p;
      sfars = p;
  }
}

// Indeparteaza un element din lista si reactualizeaza pointerii incep si sfars
void dllist::indep(dbinlob *ob) {
  if(ob->anterior) { // nu este vorba de primul element
    ob->anterior->urmator = ob->urmator;
    if(ob->urmator) // nu este vorba de utlimul element
      ob->urmator->anterior = ob->anterior;
    else // Indeparteaza ultimul element
      sfars = ob->anterior; // reactualizeaza pointerul sfars
  } else { // indeparteaza primul element
      if(ob->urmator) { // lista nu e goala
        ob->urmator->anterior = NULL;
        incep = ob->urmator;
      } else // lista este goala acum
        incep = sfars = NULL;
  }
}

// Parcurge lista de la inceput la sfarsit
void dllist::inceplist() {
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

// Parcurge lista de la sfarsit catre inceput
void dllist::sfarslist() {
  dbinlob *temp;
  temp = sfars;
  do {
    cout << temp->info << " ";
    temp = temp->daanterior();
  } while (temp);
  cout << "\n";
}

// Gaseste un obiect pe baza informatiilor sale
dbinlob *dllist::gaseste(char c) {
  dbinlob *temp;
  temp = incep;
  while (temp) {
    if (c == temp->info) return temp; // gasit
    temp = temp->daurmator();
  }
  return NULL;
}

main() {
  dllist lista;
  char c;
  dbinlob *p;

  lista.memo('1');
  lista.memo('2');
  lista.memo('3');

  // foloseste functiile membre pt a afisa lista
  cout << "Iata lista de la inceput, apoi de la sfarsit:\n";
  lista.inceplist();
  lista.sfarslist();
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
  cout << "Iata lista de la inceput, apoi de la sfarsit\n";
  lista.inceplist();
  lista.sfarslist();
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

  // scoate ultimul element al listei
  cout << "Dupa indepartarea sfarsitului listei:\n";
  p = lista.dasfars();
  lista.indep(p);
  lista.inceplist();

  return 0;
}
