#define ENA 5   // Điều khiển tốc độ động cơ bên trái     GPIO5(D1)
#define ENB 4   // Điều khiển tốc độ động cơ bên phải    GPIO12(D6)
#define IN1 0   // L298N in1 Động cơ trái quay             GPIO4(D2)
#define IN2 2   // L298N in2 Động cơ trái quay ngược lại   GPIO0(D3)
#define IN3 12  // L298N in3 Động cơ phải quay            GPIO2(D4)
#define IN4 13  // L298N in4 Động cơ phải quay ngược lại GPIO14(D5),
#include <ESP8266WiFi.h>

WiFiClient client;
WiFiServer server(80);
int xMapped = map(10, 470, 0, 0, 100);
int tocdoxe1 = map(10,550, 0, 0, 255);/* WIFI settings */
int tocdoxe= tocdoxe1 - xMapped;
const char* ssid = "SEW";
const char* password = "Datyeuoanh";

// Set your Static IP address
IPAddress local_IP(192, 168, 1, 199);
// Set your Gateway IP address
IPAddress gateway(192, 168, 1, 1);

IPAddress subnet(255, 255, 0, 0);
IPAddress primaryDNS(8, 8, 8, 8);    // optional
IPAddress secondaryDNS(8, 8, 4, 4);  // optional

/* data received from application */
String data = "";
// int tocdoxe = 300;  // 400 - 1023.
/* define L298N or L293D motor control pins */

void setup() {
  /* initialize motor control pins as output */
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  Serial.begin(115200);
  connectWiFi();

  server.begin();
}

void loop() {
  /* If the server available, run the "checkClient" function */
  client = server.available();
  if (!client) return;
  data = checkClient();


  if (data == "toi")  moveForward();

  else if (data == "lui") moveBackward();

  else if (data == "trai") moveLeft();

  else if (data == "phai") moveRight();
  else if (data == "dung") stop();
}

/********************************************* Tiến tới *****************************************************/
void  moveForward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  //for (int tocdoxe1 = 50; tocdoxe1 <= 100; tocdoxe1 += 10) {
    analogWrite(ENA, tocdoxe1);
    analogWrite(ENB, tocdoxe1);
    //delay(00);
    //if (tocdoxe1 == 200) {
      //tocdoxe1 = 210;
      //break;
    //}
  //}
  printf(""+tocdoxe1);
}
/********************************** Lùi lại ******************************************/
void moveBackward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, HIGH);
  //for (int tocdoxe1 = 50; tocdoxe1 <= 100; tocdoxe1 += 10) {
    analogWrite(ENA, tocdoxe1);
    analogWrite(ENB, tocdoxe1);
    //delay(300);
    //if (tocdoxe1 == 200) {
      //tocdoxe1 = 210;
      //break;
    //}
 // }
}
/********************************** Dừng lại ******************************************/
void stop() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 0);
}
/********************************** Rẽ trái ******************************************/
void moveRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  //for (int tocdoxe1 = 50; tocdoxe1 <= 100; tocdoxe1 += 10) {
    analogWrite(ENA, tocdoxe1);
    analogWrite(ENB, tocdoxe1);
    //delay(300);
    //if (tocdoxe1 == 200) {
     //tocdoxe1 = 210;
      //break;
    //}
  //}
}
/********************************** Rẽ phải ******************************************/
void moveLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  //for (int tocdoxe1 = 50; tocdoxe1 <= 100; tocdoxe1 += 10) {
    analogWrite(ENA, tocdoxe1);
    analogWrite(ENB, tocdoxe1);
    //delay(300);
    //if (tocdoxe1 == 200) {
      //tocdoxe1 = 210;
      //break;
    //}
  //}
}
void callWheelChair() {
    digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}
void goBacktoParking() {
    digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}
String checkClient(void) {
  while (!client.available()) delay(1);
  String request = client.readStringUntil('\r');
  Serial.println(request);
  request.remove(0, 5);
  Serial.println(request);
  request.remove(request.length() - 9, 9);
  Serial.println(request);
  return request;
}
void connectWiFi() {
  Serial.println("Connecting to WIFI");
  WiFi.begin(ssid, password);
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
    Serial.println("STA Failed to configure");
  }
  while ((!(WiFi.status() == WL_CONNECTED))) {
    delay(300);
    Serial.print("..");
  }
  //Serial.print("Setting AP (Access Point)…");
  // Remove the password parameter, if you want the AP (Access Point) to be open
  //WiFi.softAP(ssid, password);

  //IPAddress IP = WiFi.softAPIP();
  //Serial.print("AP IP address: ");
  //Serial.println(IP);
  //Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("NodeMCU Local IP is : ");
  Serial.print((WiFi.localIP()));
}