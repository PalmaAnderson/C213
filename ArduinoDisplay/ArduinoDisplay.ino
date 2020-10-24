#include <LiquidCrystal.h>
const int pin_RS = 8;
const int pin_EN = 9;
const int pin_d4 = 4;
const int pin_d5 = 5;
const int pin_d6 = 6;
const int pin_d7 = 7;
const int pin_BL = 10;
LiquidCrystal lcd(pin_RS, pin_EN, pin_d4, pin_d5, pin_d6, pin_d7);
int SetPoint;

void setup()
{
  Serial.begin(9600);S
  SetPoint = 50;

  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("ASM Control C213");
  lcd.setCursor(0, 1);
  lcd.print("SetPoint: 50");
}

void Block()
{
  lcd.setCursor(0, 0);
  lcd.print("> MAX SetPoint <");
  lcd.setCursor(0, 1);
  lcd.print("> Press Reset  <");
  while (1)
  {
  }
}

void loop()
{
  delay(100);
  int x;
  x = analogRead(0);
  lcd.setCursor(10, 1);
  if (x < 60)
  {
    SetPoint = SetPoint + 10;
    if (SetPoint > 100)
    {
      Block();
    }
    lcd.print(SetPoint);
    delay(250);
  }

  else if (x < 200)
  {
    lcd.print("UP    ");
  }
  else if (x < 400)
  {
    lcd.print("DW  ");
  }
  else if (x < 600)
  {
    SetPoint = SetPoint - 10;
    lcd.print(SetPoint);
    delay(250);
  }
  else if (x < 800)
  {
    Serial.println(SetPoint);
    delay(100);
    lcd.print("SENT ");
    delay(250);
    lcd.setCursor(10, 1);
    lcd.print("     ");
    lcd.setCursor(10, 1);
    lcd.print(SetPoint);
  }
  else
  {
    Serial.println(0);
  }
}
