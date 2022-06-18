#include <iostream>
#include <string>

using namespace std;

class Rectangle {
public:
  Rectangle() : length(5), width(5), area(5 * 5) {
    numInstances++;
    cout << "There is (are) " << numInstances << " instance(s) of rectangle\n";
  }
  Rectangle(const int& length_, const int& width_) : length(length_), width(width_), area(length_* width_) {
    numInstances++;
    cout << "There is (are) " << numInstances << " instance(s) of rectangle\n";
  }

public:
  void printInfo() {
    cout << "We are a rectangle of length " << length << ", width " << width << ", and area " << area << ".\n";
  }

protected:
  int length, width, area;
public:
  static int numInstances;
};

int Rectangle::numInstances = 0;

class Square : public Rectangle {
public:
  Square() : Rectangle() {}
  Square(const int& size) : Rectangle(size, size) {}

public:
  void printInfo() {
    cout << "We are a square with length " << length << ", and area " << area << ".\n";
  }
};

int main() {
  cout << "3/c Hopley Yeaton\n";
  cout << "TOOP HW6\n";

  Rectangle rect;
  Rectangle rect2(5, 10);
  Square square;
  Square square2(10);

  rect.printInfo();
  rect2.printInfo();
  square.printInfo();
  square2.printInfo();
}
