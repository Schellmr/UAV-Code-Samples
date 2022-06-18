#include <iostream>
#include <string>

using namespace std;

class Dog {
public:
  Dog();
  Dog(const int& age, const bool& sex, const string& breed, const string& name);

public:
  void bark();
  void sayHello(const Dog& other);
  string getInfo();

public:
  int age;
  bool sex;
  string breed, name;
};

Dog::Dog() {
  age = 7;
  sex = true;
  breed = "Golden Retriever";
  name = "Buck";
}

Dog::Dog(const int& age, const bool& sex, const string& breed, const string& name) {
  this->age = age;
  this->sex = sex;
  this->breed = breed;
  this->name = name;
}

void Dog::bark() {
  cout << "Woof!\n";
}

void Dog::sayHello(const Dog& other) {
  cout << name << " says hello to " << other.name << "\n";
}

string Dog::getInfo() {
  return name + " is a " + to_string(age) + " year old " + ((sex) ? "male" : "female") + " " + breed;
}

int main() {
    cout << "3/c Hopley Yeaton\n";
    cout << "TOOP HW5\n";

    Dog buck;
    Dog yourDog(10, 0, "Yorkshire Terrier", "Muffin");

    cout << buck.getInfo() << "\n";
    cout << yourDog.getInfo() << "\n";

    for (int i = 0; i < 10; i++) {
      yourDog.bark();
    }

    buck.sayHello(yourDog);
}
