#include <iostream>
#include <string>
#include <fstream>

int main() {
    std::cout << "Hello, TOOP!\n";

    std::string name;
    int age;
    double decimalAge;

    std::cout << "Please enter your name: ";
    std::getline(std::cin, name);
    std::cout << "Please enter your age in years: ";
    std::cin >> age;
    std::cout << "Please enter the number of months since your last birthday: ";
    std::cin >> decimalAge;
    decimalAge = age + decimalAge / 12;

    std::cout << "Your name is " << name << ", and you are " << decimalAge << " years old!" << std::endl;

    std::ofstream myfile;
    myfile.open("history.txt", std::ios::app);
    myfile << name << " : " << decimalAge << std::endl;
    myfile.close();

    return 0;
}
