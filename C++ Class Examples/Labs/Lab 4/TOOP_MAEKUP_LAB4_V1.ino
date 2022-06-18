#include "Arduino.h"

float msButtonHeldStart = -1;
int switchHeld = -1;

void handleButtons() {
  Lcd.locate(0, 0);
  if (SW_AVAILABLE) {
    if (ReadSwitch(SW_1)) {
      Lcd.print("Switch 1 is being held!");

      Lcd.locate(1, 0);
      if (switchHeld == 1) {
        Lcd.print("Held for: ");
        Lcd.print(millis() - msButtonHeldStart);
      } else {
        msButtonHeldStart = millis();
        switchHeld = 1;
      }
    } else if (ReadSwitch(SW_2)) {
      Lcd.print("Switch 2 is being held!");

      Lcd.locate(1, 0);
      if (switchHeld == 2) {
        Lcd.print("Held for: ");
        Lcd.print(millis() - msButtonHeldStart);
      } else {
        msButtonHeldStart = millis();
        switchHeld = 2;
      }
    } else if (ReadSwitch(SW_3)) {
      Lcd.print("Switch 3 is being held!");

      Lcd.locate(1, 0);
      if (switchHeld == 2) {
        Lcd.print("Held for: ");
        Lcd.print(millis() - msButtonHeldStart);
      } else {
        msButtonHeldStart = millis();
        switchHeld = 2;
      }
    } else if (ReadSwitch(SW_4)) {
      Lcd.print("Switch 4 is being held!");

      Lcd.locate(1, 0);
      if (switchHeld == 2) {
        Lcd.print("Held for: ");
        Lcd.print(millis() - msButtonHeldStart);
      } else {
        msButtonHeldStart = millis();
        switchHeld = 2;
      }
    } else {
      Lcd.print("No switches are being held!");
      switchHeld = -1;
    }
  } else {
    Lcd.print("Error initializing the switches!");
  }
  delay(1000);
  Lcd.clear();
}

void setup() {
  InitEmoro();
  Lcd.init();
}


void loop() {
  handleButtons();
}
