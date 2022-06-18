#include <iostream>

using namespace std;

int sum(int a, int b) {
  return a + b;
}
int sum(int a, int b, int c) {
  return a + b + c;
}
long power(int a, int b) {
  int sum = 1;
  for (int i = 0; i < b; i++) {
    sum *= a;
  }
  return sum;
}
void doubleNumber(int& a) {
  a *= 2;
}

int main() {
    cout << "3/c Hopley Yeaton\n";
    cout << "TOOP HW3\n\n";

    while (true) {
      int userInput;
      cout << "1. Sum two numbers\n";
      cout << "2. Sum three numbers\n";
      cout << "3. Raise a number to a certain power\n";
      cout << "4. Double a given number\n";
      cout << "5. Print info\n";
      cout << "6. Quit\n";
      cout << "Please enter your choice: ";
      cin >> userInput;

      int a, b, c;
      switch (userInput) {
      case 1:
        cout << "Enter the first number: ";
        cin >> a;
        cout << "Enter the second number: ";
        cin >> b;

        cout << a << " + " << b << " = " << sum(a, b) << "\n\n";
        break;
      case 2:
        cout << "Enter the first number: ";
        cin >> a;
        cout << "Enter the second number: ";
        cin >> b;
        cout << "Enter the third number: ";
        cin >> c;

        cout << a << " + " << b << " + " << c << " = " << sum(a, b, c) << "\n\n";
        break;
      case 3:
        cout << "Enter the first number: ";
        cin >> a;
        cout << "Enter the second number: ";
        cin >> b;

        cout << a << " ^ " << b << " = " << power(a, b) << "\n\n";
        break;
      case 4:
        cout << "Enter a number to double: ";
        cin >> a;

        doubleNumber(a);

        cout << "a doubled is " << a << "\n\n";
        break;
      case 5:
        cout << "3/c Hopley Yeaton\n";
        cout << "TOOP Fall 1776\n";
        cout << "Homework 3: Functions\n\n";
        break;
      case 6:
        return 0;
        break;
      default:
        cout << "Valid input are 1-6. Please try again!\n\n";
        std::cin.clear();
        std::cin.ignore(10000, '\n');
      }
    }
}
