#include <iostream>

int main()
{
  int i = 4;
  auto l = [i]() mutable { return ++i; };

  std::cout << l() << '\n';

  return 0;
}
