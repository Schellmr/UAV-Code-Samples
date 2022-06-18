#include <iostream> // For console IO
#include <string> // for to_string

using namespace std; // using the standard namespace (std::)

class CPlayingCard {
public:
  CPlayingCard();
  CPlayingCard(const string& suit, const int& value);

public:
  friend ostream& operator<<(ostream&, const CPlayingCard&);

private:
  string suit;
  int value;
};

// Write a default constructor and a parametrized constructor consistent with the headers provided
// in the class definition. You need no further code; however, there are questions on the next page.
CPlayingCard::CPlayingCard() {
  this->suit = "Spades";
  this->value = 13;
}

CPlayingCard::CPlayingCard(const string& suit, const int& value) {
  this->suit = suit;
  this->value = value;
}

ostream& operator<<(ostream& stream, const CPlayingCard& card) {
  string value = "";
  if (card.value <= 9) {
    value = to_string(card.value + 1);
  } else {
    string faces[] = {"Jack", "Queen", "King", "Ace"};
    value = faces[card.value - 10];
  }

  return stream << value << " of " << card.suit;
}

int main() {
  CPlayingCard deck[52];
  string suits[] = { "Spades", "Diamonds", "Hearts", "Clubs" };
  for (int i = 0; i < 52; i++) {
    deck[i] = CPlayingCard(suits[(int) floor(i / 13)], i % 13);
    cout << deck[i] << endl;
  }

  return 0;
}
