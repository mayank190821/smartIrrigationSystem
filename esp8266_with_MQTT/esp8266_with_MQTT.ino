#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "painlessMesh.h"
#include<Arduino_JSON.h>
#define MESH_PREFIX "SMMesh" //name of mesh 
#define MESH_PASSWORD "123456789"
#define MESH_PORT 5555

const char* ssid = "raspbpi";
const char* password = "123456789";

// Change the variable to your Raspberry Pi IP address, so it connects to your MQTT broker
const char* mqtt_server = "172.168.19.5"; // assuming ip address

// Initializes the espClient
WiFiClient espClient;
PubSubClient client(espClient);
long now = millis();
long lastMeasure = 0;
float moisture;

  int nodeNumber = 1;
  String readings;
  Scheduler userScheduler; // to control your personal talk
  painlessMesh mesh;
  //User stub

  void sendMessage();
  String getReadings();
 

  Task taskSendMessage(TASK_SECOND *5,TASK_FOREVER,&sendMessage);

  String getReadings(){
    JSONVar jsonReadings;
    jsonReadings ["received"] = "yes";
    readings = JSON.stringify(jsonReadings);
    return readings; 
  }
  void sendMessage () {
    String msg = getReadings();
    mesh.sendBroadcast(msg);
  }

  //Needed for painlessmesh library
  void receivedCallback(uint32_t from, String &msg){
    Serial.printf("Received from %u msg=%s\n",from,msg.c_str());
    JSONVar myObject = JSON.parse(msg.c_str());
    int node = myObject["node"];
    double moisture = myObject["moisture"];
    Serial.print("Node  ");
    Serial.println(node);
    Serial.print("moisture  ");
    Serial.println(moisture);
  }

  void newConnectionCallback(uint32_t nodeId){
    Serial.printf("New Connection, nodeID = %u\n",nodeId);
  }

  void changedConnectionCallback() {
    Serial.printf("Changed connections\n");
  }
  void nodeTimeAdjustedCallback(int32_t offset) {
    Serial.printf("Adjusted time %u. Offset = %d\n", mesh.getNodeTime(),offset);
  }




void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}
void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  
  Serial.println();
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");  
      client.subscribe("esp8266/4");
      client.subscribe("esp8266/5");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(15000);
    }
  }
}
void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  mesh.setDebugMsgTypes(ERROR|STARTUP);
  mesh.init(MESH_PREFIX,MESH_PASSWORD,&userScheduler,MESH_PORT);
  mesh.onReceive(&receivedCallback);
  mesh.onNewConnection(&newConnectionCallback);
  mesh.onNodeTimeAdjusted(&nodeTimeAdjustedCallback);
  mesh.onChangedConnections(&changedConnectionCallback);
  userScheduler.addTask(taskSendMessage);
  taskSendMessage.enable();
}
void loop() {
  mesh.update();
  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())

    client.connect("ESP8266Client");
    
  now = millis();
if (now - lastMeasure > 10000) {
    lastMeasure = now;
    if (isnan(moisture)) {
      Serial.println("Failed to read data!");
      return;
    }
    static char moistureValue[7];
    dtostrf(moisture, 6, 2, moistureValue);
    client.publish("/esp8266/moisture", moistureValue);
}
}
