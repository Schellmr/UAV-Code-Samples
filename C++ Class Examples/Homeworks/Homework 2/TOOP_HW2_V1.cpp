#include <iostream>
#include <string>
#include <fstream>

int main() {
  std::cout << "3/c Hopley Yeaton" << std::endl;
  std::cout << "TOOP HW2" << std::endl;

  std::string input_filename, line;
  int age;

  std::cout << "Please enter your age: ";
  std::cin >> age;

  if (age < 18) {
    std::cout << (18 - age) << " years left until you can vote!" << std::endl;
  } else if (age < 21) {
    std::cout << "You can vote!" << std::endl;
  } else if (age < 30) {
    std::cout << "You can drink alcohol!" << std::endl;
  } else {
    std::cout << "You can run for senate!" << std::endl;
  }

  std::cin.clear();
  std::cin.ignore(10000, '\n');

  std::ifstream my_file;
  while (!my_file.is_open()) {
    std::cout << "Please enter a filename: ";
    std::getline(std::cin, input_filename);
    my_file.open(input_filename);
  }

  std::cout << "Input Filename: " << input_filename << std::endl;

  for (int i = 1; i <= 5; i++) {
    getline(my_file, line);
    std::cout << i << ": " << line << std::endl;
  }

  my_file.close();

  return 0;
}
