#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

bool isPalindrome(const char word[], int length) {
  // YOUR CODE HERE
  for (int i = 0; i < length / 2; i++) {
    if (word[i] != word[length - 1 - i]) {
      return false;
    }
  }
  return true;
}

int main() {
    cout << "3/c Hopley Yeaton\n";
    cout << "TOOP HW4\n";

    bool quit = false;
    while (!quit) {
      string word;
      cout << "Please enter a word ('quit' to exit): ";
      getline(cin, word);

      // Transform, from the algorithm library, allows us to convert our
      // std::string into a lowercase version of the same string.
      transform(word.begin(), word.end(), word.begin(), ::tolower);

      if (!strcmp(word.c_str(), "quit")) {
        quit = true;
      } else {
        if (isPalindrome(word.c_str(), word.length())) {
          cout << "\"" << word << "\" is a palindrome!\n";
        } else {
          cout << "\"" << word << "\" is not a palindrome!\n";
        }
      }
    }

    int matrix[4][4] = {
      {1, 2, 3, 4},
      {0, 5, 6, 7},
      {0, 0, 8, 9},
      {0, 0, 0, 1}
    };

    for (int r = 0; r < 4; r++) {
      for (int c = r; c < 4; c++) {
        int temp = matrix[r][c];
        matrix[r][c] = 0;
        matrix[c][r] = temp;
      }
    }

    for (int r = 0; r < 4; r++) {
      for (int c = 0; c < 4; c++) {
        cout << matrix[r][c] << " ";
      }
      cout << "\n";
    }

    cout << "Have a nice day!\n";
    return 0;
}