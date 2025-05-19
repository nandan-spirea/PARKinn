#include <Arduino.h>

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// OLED display dimensions
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// OLED reset pin
#define OLED_RESET     -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Button pin definitions
#define BTN_CAR_PRESENT       13
#define BTN_CAR_NOT_PRESENT   12
#define BTN_OUT_OF_SERVICE    14
#define BTN_MAINTENANCE       27

// Output pin definitions
#define GREEN_LED 2
#define RED_LED 4
#define BUZZER 5
#define YELLOW_LED 15 // Optional

// 🔹 Function declarations
void clearOutputs();
void displayMessage(String msg);

void setup() {
  Serial.begin(115200);

  // Initialize OLED display
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("SSD1306 allocation failed");
    while (true);
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("System Initializing...");
  display.display();
  delay(2000);
  display.clearDisplay();

  // Set button pins as input
  pinMode(BTN_CAR_PRESENT, INPUT);
  pinMode(BTN_CAR_NOT_PRESENT, INPUT);
  pinMode(BTN_OUT_OF_SERVICE, INPUT);
  pinMode(BTN_MAINTENANCE, INPUT);

  // Set output pins
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);

  // Ensure all outputs are off at start
  clearOutputs();
}

void loop() {
  if (digitalRead(BTN_CAR_PRESENT) == HIGH) {
    clearOutputs();
    digitalWrite(GREEN_LED, HIGH);
    displayMessage("Car detected!\nPlate: KA03AB1234");
    Serial.println("Car present - plate: KA03AB1234");
    delay(2000);
  } else if (digitalRead(BTN_CAR_NOT_PRESENT) == HIGH) {
    clearOutputs();
    displayMessage("No vehicle detected");
    Serial.println("No car present");
    delay(2000);
  } else if (digitalRead(BTN_OUT_OF_SERVICE) == HIGH) {
    clearOutputs();
    digitalWrite(RED_LED, HIGH);
    digitalWrite(BUZZER, HIGH);
    displayMessage("ERROR: Out of Service!");
    Serial.println("Module out of service");
    delay(2000);
  } else if (digitalRead(BTN_MAINTENANCE) == HIGH) {
    clearOutputs();
    digitalWrite(YELLOW_LED, HIGH);
    displayMessage("Under Maintenance");
    Serial.println("Module under maintenance");
    delay(2000);
  }
}

void clearOutputs() {
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(RED_LED, LOW);
  digitalWrite(BUZZER, LOW);
  digitalWrite(YELLOW_LED, LOW);
}

void displayMessage(String msg) {
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println(msg);
  display.display();
}
