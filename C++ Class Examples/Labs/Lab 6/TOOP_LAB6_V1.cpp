#include <iostream>
#include <string>

using namespace std;

class Robot {
public:
  // Default Constructor
  Robot() {
    name = "Iron Giant";
    height = 15;
  }
  // Parameterized Constructor 
  Robot(string name_) {
    name = name_;
  }

public:
  // method dance
  void dance() {
    cout << name << " does the Robot\n";
  }
  // method getInfo
  void printInfo() {
    cout << name << " is a " << height << " meter tall robot\n";
  }

private:
  string name;
  int height;
};

int main() {
  cout << "TOOP Lab 6 (Last Lab!)\n";

  Robot ironGiant;
  ironGiant.dance();
  ironGiant.printInfo();
}
