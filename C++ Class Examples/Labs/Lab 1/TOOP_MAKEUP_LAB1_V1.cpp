#include <iostream> // import this for console io
#include <string> // import this for access to strings
#include <fstream> // import this for file io

using namespace std; // using the standard namespace

/*
MAKEUP-LAB #1
TOOP Fall 2021
*/
int main() { // define our entry point
    std::cout << "Hello, TOOP! Welcome to the First Make-Up Lab!\n"; // print a nice welcome message

    int x = 20; // declare and initialize x to the value of 20
    int y = 2; // declare and initialize y to the value 2
    double z = 20.24; // declare and initialize z to the value 20.24

    cout << "y - x = " << (y - x) << std::endl; // print y - x = ...

    string last_name; // declare a string last name
    int months_age; // declare an int months_age

    cout << "Please enter your last name: "; // request the user's last name
    cin >> last_name; // input the last name into the last_name variable
    cout << "Please enter your age in years: "; // request the user's age in years
    cin >> 12 * months_age; // input the user's age in months into the months_age variable

    // print the user's last name and age in months
    cout << "Your last name is " << last_name << ", and you are at least " << months_age << " months old." << endl;

    ofstream outfile; // create an output file stream called myfile
    outfile.open("makeup-lab1.txt", ios::app); // open makeup-lab1.txt (in local directory) in append mode (ios::app)
    outfile << name << " used our program!"; // input the user's name
    outfile.close(); // close the file

    string contents; // declare a string called contents
    ifstream infile; // create an input file stream
    infile.open("makeup-lab1.txt"); // open the output file
    getline(infile, contents); // read the second line (hint, you may call getline twice!). 
							   // You may assume makeup-lab1.txt has more than one line.
	getline(infile, contents);
    cout << contents << endl; // print the second line
}