#include "painlessMesh.h"
#include<Arduino_JSON.h>
#include<ESP8266WiFi.h>
//Mesh Details
#define MESH_PREFIX "SMMesh" //name of mesh 
#define MESH_PASSWORD "123456789"
#define MESH_PORT 5555

int nodeNumber = 2;
String readings;
Scheduler userScheduler; // to control your personal talk
painlessMesh mesh;
//User stub

void sendMessage();
String getReadings();
float moisture();

Task taskSendMessage(TASK_SECOND *5,TASK_FOREVER,&sendMessage);

String getReadings(){
  JSONVar jsonReadings;
  jsonReadings ["node"] = nodeNumber;
  jsonReadings["moisture"]=moisture();
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
void setup() {
  Serial.begin(115200);
  pinMode(A0,INPUT);
  mesh.setDebugMsgTypes(ERROR|STARTUP);
  mesh.init(MESH_PREFIX,MESH_PASSWORD,&userScheduler,MESH_PORT);
  mesh.onReceive(&receivedCallback);
  mesh.onNewConnection(&newConnectionCallback);
  mesh.onNodeTimeAdjusted(&nodeTimeAdjustedCallback);
  mesh.onChangedConnections(&changedConnectionCallback);
  userScheduler.addTask(taskSendMessage);
  taskSendMessage.enable();
}
float moisture(){
  float moistureValue = analogRead(A0);
  moistureValue = map(moistureValue,1023,0,0,100);
  return moistureValue;
}
void loop(){
  moisture();
  mesh.update();
}
