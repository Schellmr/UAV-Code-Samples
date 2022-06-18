#include <iostream> // For console IO

int main() { // Entry point definition
  // Implement Division by Repeated Subraction
  // Define two integers and assign them with user input.

  int a, b; // integer a and b which we will use to calculate a/b
  std::cout << "Hello, TOOP! Welcome to Make-Up Lab 2." << std::endl; // nice introductory message

  std::cout << "Enter a positive integer 'a': "; // request integer a
  std::cin >> a;

  std::cout << "Enter another positive integer 'b': "; // request integer b
  std::cin >> b;

  int quotient = 0; // sum begins at 0

  /* Write the following Code:
   * If a and b are both greater than 0 and a > b, calculate a/b via repeated division
   * Note that you will complete a number of iterations and return a quotient as well as a remainder.
   * Your output should be similar to the following format: 3 remainder 3.
   * Else, print an error message.
   */

  if (a > 0 && b > 0 && a > b) {
    while (a - b >= 0) {
      std::cout << a << std::endl;
      a -= b;
      quotient++;
    }
  } else {
    std::cout << "Error: Invalid Input!" << std::endl;
    return 0;
  }

  std::cout << quotient << " remainder " << a << std::endl;
}
