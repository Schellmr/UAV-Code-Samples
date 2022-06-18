#include <iostream> // For console IO

using namespace std; // using the standard namespace (std::)

// Define a function to greet the user. It won't return anything
void greet() {
  cout << "Hello! I am 2/c Jacob Schellman" << endl;
}

// Define a function that multiplies the arguments a and b and stores the result in c.
// a, b, and c are all integers. However, consider whether we want to pass by value or by reference.
void multiply(int a, int b, int& c) {
  c = a * b;
}

int main() {
  greet();
  int a, b, c;

  cout << "Enter a: ";
  cin >> a;
  cout << "Enter b: ";
  cin >> b;

  multiply(a, b, c);
  cout << "a * b = " << c << endl;
}
