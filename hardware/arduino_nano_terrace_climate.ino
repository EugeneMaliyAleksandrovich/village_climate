#include <DHT11.h>
#include <LiquidCrystal_I2C.h>

// ===== НАСТРОЙКИ =====
#define PIN_PROBE 2

// ===== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ =====
DHT11 dht11(PIN_PROBE);

int temperature = 0;
int humidity = 0;

unsigned long lastSendTime = 0;
const unsigned long sendInterval = 2000;

// Sensor calibration. Start with 0 for each.
const int HumidityCorrection = 0;
const int CelsiusTemperatureCorrection = 0;

LiquidCrystal_I2C lcd(0x27,16,2);  // Устанавливаем дисплей (адрес дисплея на шине I2C, ширина дисплея, количество строк)

// ===== ФУНКЦИЯ setup() - ВЫПОЛНЯЕТСЯ 1 РАЗ =====
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  lcd.init();
  lcd.backlight();// Включаем подсветку дисплея 
  lcd.print("t: ");
  lcd.setCursor(8, 0);
  lcd.print("h: ");
  
  Serial.println("Nano started");
}

void printInfo(int temperature, int humidity) {
  
  lcd.setCursor(0, 0);
  lcd.print("t: ");
  lcd.print(temperature);
  lcd.print(" C");
  lcd.setCursor(8, 0);
  lcd.print("h: ");
  lcd.print(humidity);
  lcd.print(" %");
}

// ===== ФУНКЦИЯ loop() - ВЫПОЛНЯЕТСЯ БЕСКОНЕЧНО =====
void loop() {
  
  // Выполнять процедуру раз в секунду
  if (millis() - lastSendTime < sendInterval) {
    return;
  }
  
  int result = dht11.readTemperatureHumidity(temperature, humidity);
  if (result == 0) {
      temperature += CelsiusTemperatureCorrection;
      humidity += HumidityCorrection;
  } else {
      // Print error message based on the error code.
      Serial.println(DHT11::getErrorString(result));
      return;
  }

  printInfo(temperature, humidity);

  // Отправить данные на Wifi-модуль
  String data = "T:" + String(temperature) + " H:" + String(humidity);
  Serial.println(data);

  lastSendTime = millis();
}

