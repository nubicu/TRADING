#include <cmath>
#include <iostream>

constexpr unsigned long long fib(const int i)
{
  constexpr auto sqrt_5 = std::sqrt(5);

  if (i == 0) return 0;
  if (i == 1) return 1;

  return static_cast<unsigned long long>((std::pow(1 + sqrt_5, i) - std::pow(1 - sqrt_5, i)) / (std::pow(2, i) * sqrt_5));
}

int main()
{
  std::cout << fib(93) << '\n'; // This is the last value in the Fibonacci that fits in an unsigned long long
}
