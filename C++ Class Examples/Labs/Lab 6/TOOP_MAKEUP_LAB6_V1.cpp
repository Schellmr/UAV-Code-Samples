#include <iostream>
#include <string>
#include <stdlib.h>

using namespace std;

class CAcademicCourse {
public:
  // Default Constructor
  CAcademicCourse() {
    name = "Signals, Systems, and Transforms";
    credits = 4;
  }
  // Parameterized Constructor 
  CAcademicCourse(string name_, double credits_) {
    name = name_;
    credits = credits_;
  }

public:
  // method dance
  void doExamination() {
    cout << name << " issues an exam...\n";
    double averageGrade = rand() % 15 + 70;
    cout << "The average grade was " << averageGrade << '\n';
  }
  // method getInfo
  void printInfo() {
    cout << name << " is a " << credits << " credit course\n";
  }

protected:
  string name;
  double credits;
};

class CTOOP : public CAcademicCourse {
public:
  CTOOP() : CAcademicCourse("Transition to Object Oriented Programming", 2) {}

public:
  void doExamination() {
    cout << name << " issues a lab...\n";
    double averageGrade = rand() % 15 + 85;
    cout << "The average grade was " << averageGrade << '\n';
  }
};

int main() {
  cout << "TOOP Makeup Lab 6 (Last Lab!)\n";

  CAcademicCourse SST;
  CTOOP TOOP;

  SST.printInfo();
  SST.doExamination();

  TOOP.printInfo();
  TOOP.doExamination();
}
