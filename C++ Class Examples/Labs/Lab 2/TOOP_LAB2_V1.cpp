#include <iostream> // For console IO

int main() { // Entry point definition
  // Define two integers, a and b. Initialize both variables with input from the user.
  // Define another integer called sum. Initialize this variable to 0.

  int a, b; // integer a and b which we will use to calculate a^b
  std::cout << "Hello, TOOP! Welcome to Lab 2." << std::endl; // nice introductory message

  std::cout << "Enter a positive integer 'a': "; // request integer a
  std::cin >> a;

  std::cout << "Enter another positive integer 'b': "; // request integer b
  std::cin >> b;

  int sum = 0; // sum begins at 0

  /* Write the following Code:
   * If a and b are both greater than 0, calculate a^b via repeated addition (see reference)
   * Else, print an error message.
   */

  if (a >= 0 && b >= 0) {
    for (int i = 0; i < b; i++) {
      sum += a;
    }
    std::cout << "a^b is: " << sum << std::endl; // print it nicely to the console
  } else {
    std::cout << "Error: Invalid Input!" << std::endl;
  }

  return 0;
}
