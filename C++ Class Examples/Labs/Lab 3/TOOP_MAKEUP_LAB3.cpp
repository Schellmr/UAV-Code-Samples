#include <iostream>

// Define a function called isEvenlyDivisible.
// It will take a divisor and dividend
// It will return true if the divisor can evenly divide the dividend, false otherwise.
bool isEvenlyDivisible(int divisor, int dividend) {
  return (divisor % dividend == 0) ? true : false;
}

// Define a function called isPrime.
// It will take a single positive number.
// It will return true if the given number is prime, false otherwise.
// Consider that a prime number divided by any natural number will have a nonzero remainder.
// Call isEvenlyDivisible in this method.
bool isPrime(int num) {
  bool isPrime = true;
  std::cout << "going from 1 to " << num << std::endl;
  for (int j = 2; j < num && isPrime; j++) {
    std::cout << "\ttesting " << j << " and " << num << std::endl;
    isPrime = !isEvenlyDivisible(num, j);
    std::cout << "\tIt was " << ((!isPrime) ? "divisible" : "not divisible") << std::endl;
  }

  return isPrime;
}

// Define a function that takes a positive integer "a" and returns the number of primes between 1 and a.
// Call isPrime in this method.
// return -1 on invalid input (negative number, for example)
int numPrimes(int a) {
  if (a < 1) {
    return -1;
  }

  int numPrimes = 0;
  for (int i = 1; i <= a; i++) {
    if (isPrime(i)) {
      numPrimes++;
    }
  }

  return numPrimes;
}

int main() {
    std::cout << "Enter a positive number: ";
    int a;
    std::cin >> a;

    std::cout << "Number of Primes between 1 and " << a << " is " << numPrimes(a) << std::endl;
}
