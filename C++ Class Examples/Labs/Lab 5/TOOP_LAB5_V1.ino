#include "Arduino.h"

void handleButtons() {
  Lcd.locate(0, 0);

  if (ReadSwitch(SW_1)) {
    Lcd.print("Switch 1 is being held!");
  } else if (ReadSwitch(SW_2)) {
    Lcd.print("Switch 2 is being held!");
  } else if (ReadSwitch(SW_3)) {
    Lcd.print("Switch 3 is being held!");
  } else if (ReadSwitch(SW_4)) {
    Lcd.print("Switch 4 is being held!");
  } else {
    Lcd.print("No switches are being held!");
  }

  delay(1000);
  Lcd.clear();
}

void setup() {
  InitEmoro();
  Lcd.init();
  if (!SW_AVAILABLE) {
    Lcd.print("Error initializing the switches!");
  }
}

void loop() {
  handleButtons();
}
