#include <iostream> // For console IO

using namespace std; // using the standard namespace (std::)

/*
This function returns a random integer between the lower (inclusive) and upper bounds (noninclusive) provided.
Upper must be greater than lower.
*/
int generateRandomInt(int lower, int upper) {
  return rand() % (upper - lower) + lower;
}

int main() {
  int ourArray[10][10]{};

  // fill ourArray based off of the following criteria:
  // if we are populating an odd row (1st, 3rd, etc.), fill the row with negative numbers.
  // if we are populating an even row, fill the row with positive multiples of two. Consider 0 to be even.
  // all numbers should have a maximum absolute value of 2024.
  for (int r = 0; r < 10; r++) {
    for (int c = 0; c < 10; c++) {
      if (r % 2) { // if r is odd
        ourArray[r][c] = generateRandomInt(-2024, 0); // generates a random integer between -2024 and -1.
      } else {
        ourArray[r][c] = 2 * generateRandomInt(0, 1012); // generates a random even integer between 0 and 2024.
      }
      cout << ourArray[r][c] << " ";
    }
    cout << '\n';
  }

  return 0;
}
