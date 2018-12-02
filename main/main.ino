#include <RGBmatrixPanel.h>
#include "battlesnake.h"
#define CLK  8   // USE THIS ON ARDUINO UNO, ADAFRUIT METRO M0, etc.
#define OE   9
#define LAT 10
#define A   A0
#define B   A1
#define C   A2
#define D   A3
RGBmatrixPanel matrix(A, B, C, D, CLK, LAT, OE, false);
  
void setup() {
  matrix.begin();
  board_0(matrix);
  delay(3000);
}

void loop() {
  // Do nothing -- image doesn't change
}
