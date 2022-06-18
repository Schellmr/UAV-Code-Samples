#include <iostream> // for console io
#include <string> // for access to strings
#include <fstream> // for file io

using namespace std; // using the standard namespace

/*
LAB #1
TOOP Fall 2021
*/
int main() { // define our entry point
    std::cout << "Hello, TOOP! Welcome to the First Lab!\n"; // print a nice welcome message

    int x = 10; // declare and initialize x to the value of 10
    int y = 3; // declare and initialize y to the value 3
    double z = 10.2; // declare and initialize z to the value 10.2

    cout << "y + x = " << (y + x) << std::endl; // print y + x = ...

    string name; // declare a string name
    int age; // declare an int age

    cout << "Please enter your first name: "; // request the user's first name
    cin >> name; // input the first name into the name variable
    cout << "Please enter your age: "; // request the user's age
    cin >> age; // input the user's age into the age variable

    // print the user's name and age
    cout << "You are " << name << ", and you are " << age << endl;

    ofstream outfile; // create an output file stream called myfile
    outfile.open("lab1.txt", ios::app); // open lab1.txt (in local directory) in append mode (ios::app)
    outfile << name << " used our program!"; // input the user's name
    outfile.close();

    string contents; // declare a string called contents
    ifstream infile; // create an input file stream
    infile.open("lab1.txt"); // open the output file
    getline(infile, contents); // read the first line
    cout << contents << endl; // print the first line

    x = z; // BONUS: what is the value of x after this command is run?
    x %= y; // BONUS: what is the value of x after this command is run?
}