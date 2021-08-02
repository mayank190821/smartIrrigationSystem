#include<SoftwareSerial.h>

//Serial communication to the gps module
#define gpsBaud 9600
#define rx 3
#define tx 4
SoftwareSerial ss(tx,rx);
void setup() {
  Serial.begin(gpsBaud);
  ss.begin(gpsBaud);
}

void loop() {
  while(ss.available()>0){
    byte gpsData = ss.read();
    ss.write(gpsData);
  }
  delay(1000);

}
