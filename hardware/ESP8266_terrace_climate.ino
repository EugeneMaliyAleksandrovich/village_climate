#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

// Конфигурация Wi-Fi
const char* ssid = "Имя точки доступа";
const char* password = "Пароль точки доступа";

// Глобальные переменные
float lastTemp = 0;
float lastHum = 0;
unsigned long lastReadTime = 0;

// Настройки статического IP
IPAddress local_IP(192, 168, 1, 98);    // Какой IP хотим дать ESP
IPAddress gateway(192, 168, 1, 254);       // IP твоего роутера (шлюз)
IPAddress subnet(255, 255, 255, 0);      // Маска подсети (обычно такая)

// Создаем сервер
ESP8266WebServer server(80);

void setup() {
  Serial.begin(9600);          // Для связи с Nano
  Serial.println("ESP8266 starting...");
  
  // Сначала конфигурируем статический IP
  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("STA Failed to configure");
  }

  // Подключаемся к Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("\nWiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  // Настраиваем маршруты веб-сервера
  server.on("/data", handleDataRequest);
  server.on("/", handleRootPage);
  server.onNotFound([]() {
    server.send(404, "text/plain", "404: Not Found");
  });
  
  // ЗАПУСКАЕМ СЕРВЕР (ОДИН РАЗ!)
  server.begin();
  Serial.println("HTTP server started!");
}

void loop() {
  // 1. Принимаем данные с Nano
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    
    // Парсим строку "T:23.5 H:60.2"
    if (data.startsWith("T:")) {
      sscanf(data.c_str(), "T:%f H:%f", &lastTemp, &lastHum);
    }
  }

  // 2. Обслуживаем веб-сервер (ЭТО ГЛАВНОЕ!)
  server.handleClient();
  
  // 3. Другие задачи (например, мигание LED, если нужно)
  // НИКАКИХ delay() !!!
}

void handleDataRequest() {
  String json = "{";
  json += "\"temperature\":" + String(lastTemp) + ",";
  json += "\"humidity\":" + String(lastHum);
  json += "}";
  
  server.send(200, "application/json", json);
}

// ----- ОБРАБОТЧИК ДЛЯ КОРНЕВОЙ СТРАНИЦЫ (опционально) -----
void handleRootPage() {
  String html = "<html><body>";
  html += "<h1>Meteo Station</h1>";
  html += "<p>Temperature: " + String(lastTemp) + " C</p>";
  html += "<p>Humidity: " + String(lastHum) + " %</p>";
  html += "<button onclick='updateData()'>Update</button>";
  html += "<script>";
  html += "function updateData() {";
  html += "  fetch('/data').then(r=>r.json()).then(d=>{";
  html += "    document.querySelector('p').innerHTML='Temp: '+d.temperature+' C';";
  html += "  });";
  html += "}";
  html += "</script></body></html>";
  
  server.send(200, "text/html", html);
}