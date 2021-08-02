import serial
import RPI.GPIO as GPIO
import pynmea2
import Adafruit_DHT as dht
import http.client as client
from threading import Thread
import requests

webhost = 'http://dc.glaitm.org:7080/Thingworx'
app_key = '1102de3b-669e-440c-b85b-c2b09a5245ac'
thingname = 'team1_smart_irrigation_system'
prop_1 = "humidity"
prop_2 = "temperature"
prop_3 = "longitude"
prop_4 = "latitude"
prop_5 = "moisture"
GPIO.setmode(GPIO.BOARD)
global moisture
global humidity
global temp
global lat
global lng

def gps():
    gpsSerial = serial.Serial('/dev/ttyAMC0', 9600)
    dataout = pynmea2.NMEAStreamReader()
    newdata = gpsSerial.readline()
    if newdata[0:6] == "$GPRMC":
        newmsg = pynmea2.parse(newdata)
        lat = newmsg.latitude
        lng = newmsg.longitute


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


# Subscribing in on_connect() means that if we lose the connection and
client.subscribe("/esp8266/moisture")


def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) +
          "' on topic '" + message.topic)
    moisture = float(str(message.payload)[1:])


def mainMQtt():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect('localhost', 1883, 60)
    # Connect to the MQTT server and process messages in a background thread.
    mqtt_client.loop_start()


def gsmMOdule():
    class GSM_MODULE:
        def __init__(self, pino_pwr, pino_rst, pin, number, message):
                self.pino_pwr = pino_pwr
                self.pino_rst = pino_rst
                self.pin = str(pin)
                self.phone_number = str(number)
                self.text = message
                global last_received
                global end_tread
                last_received = ''
                end_tread = 1

        def init(self):  # pode ser usada fora da class
                self.power_gsm()

                self.ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=5)
                self.thread_serial = Thread(target=receiving, args=(self.ser,))
                self.thread_serial.start()

                error = self.init_gms()
                if error == 1:
                    self.reset_gsm()
                    error = self.init_gms()
                    if error == 1:
                        return 1;
                return 0;

        def init_gms(self):
            global last_received
            global end_tread
            self.ser.open()
            end_tread = 0
            time.sleep(1)
            self.ser.write('AT\r\n')
            time.sleep(1)

            # print '1-', last_received
            if last_received != 'OK\r\n':
                self.ser.close()
                return 1;

            self.ser.write('AT+CPIN="' + self.pin + '"\r\n')
            time.sleep(2)

            # print '2-',last_received
            if last_received != 'OK\r\n':
                self.ser.close()
                return 1;
            self.ser.close()￼

            return 0;

        def power_gsm(self):  # pode ser usada fora da class (com cuidado!)
                GPIO.setup(self.pino_pwr, GPIO.OUT)  # power
                GPIO.output(self.pino_pwr, 1)
                time.sleep(1)
                GPIO.output(self.pino_pwr, 0)
                time.sleep(3)

        def reset_gsm(self):  # pode ser usada fora da class
                global end_tread
                end_tread = 0
                self.thread_serial.join()
                GPIO.setup(self.pino_rst, GPIO.OUT)  # reset
                GPIO.output(self.pino_rst, 1)
                time.sleep(1)
                GPIO.output(self.pino_rst, 0)
                time.sleep(3)
                self.thread_serial = Thread(target=receiving, args=(self.ser,))
                self.thread_serial.start()

        def set_phone_number(self, number):  # pode ser usada fora da class
                self.phone_number = str(number)

        def set_text(self, message):  # pode ser usada fora da class
                self.text = message

        def send_sms(self):  # pode ser usada fora da class
                global last_received
                global end_tread
                end_tread = 1
                try:
                    self.thread_serial.start()
                except:
                    pass;
                self.ser.open()
                time.sleep(1)
                self.ser.write('AT+CMGF=1\r\n')
                time.sleep(1)
                # print '3-',last_received
                self.ser.write('''AT+CMGS="''' + self.phone_number + '''"\r\n''')
                time.sleep(1)
                for x in self.text:
                    self.ser.write(x + "\r\n")
                    time.sleep(1)
                self.ser.write('\x1A')
                time.sleep(3)
                # print '4-',last_received
                if last_received != 'OK\r\n':
                    end_tread = 0
                    self.ser.close()
                    return 1;
                end_tread = 0
                self.ser.close()
                return 0;

        def receiving(ser):
            global last_received
            global end_tread

            while end_tread:
                last_received = ser.readline()

        class GSM_MODULE:
            def __init__(self, pino_pwr, pino_rst, pin, number, message):
                self.pino_pwr = pino_pwr
                self.pino_rst = pino_rst
                self.pin = str(pin)
                self.phone_number = str(number)
                self.text = message
                global last_received
                global end_tread
                last_received = ''
                end_tread = 1

            def init(self):  # pode ser usada fora da class
                self.power_gsm()
                self.ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=5)
                self.thread_serial = Thread(target=receiving, args=(self.ser,))
                self.thread_serial.start()
                error = self.init_gms()
                if error == 1:
                    self.reset_gsm()
                    error = self.init_gms()
                    if error == 1:
                        return 1;
                return 0;

            def init_gms(self):
                global last_received
                global end_tread
                self.ser.open()
                end_tread = 0
                time.sleep(1)
                self.ser.write('AT\r\n')
                time.sleep(1)

                # print '1-', last_received
                if last_received != 'OK\r\n':
                    self.ser.close()
                    return 1;

                self.ser.write('AT+CPIN="' + self.pin + '"\r\n')
                time.sleep(2)

                # print '2-',last_received
                if last_received != 'OK\r\n':
                    self.ser.close()
                    return 1;
                self.ser.close()

                return 0;

            def power_gsm(self):  # pode ser usada fora da class (com cuidado!)
                GPIO.setup(self.pino_pwr, GPIO.OUT)  # power
                GPIO.output(self.pino_pwr, 1)
                time.sleep(1)
                GPIO.output(self.pino_pwr, 0)
                time.sleep(3)

            def reset_gsm(self):  # pode ser usada fora da class
                global end_tread
                end_tread = 0
                self.thread_serial.join()
                GPIO.setup(self.pino_rst, GPIO.OUT)  # reset
                GPIO.output(self.pino_rst, 1)
                time.sleep(1)
                GPIO.output(self.pino_rst, 0)
                time.sleep(3)
                self.thread_serial = Thread(target=receiving, args=(self.ser,))
                self.thread_serial.start()

            def set_phone_number(self, number):  # pode ser usada fora da class
                self.phone_number = str(number)

            def set_text(self, message):  # pode ser usada fora da class
                self.text = message

            def send_sms(self):  # pode ser usada fora da class
                global last_received
                global end_tread
                end_tread = 1
                try:
                    self.thread_serial.start()
                except:
                    pass;
                self.ser.open()
                time.sleep(1)
                self.ser.write('AT+CMGF=1\r\n')
                time.sleep(1)
                # print '3-',last_received
                self.ser.write('''AT+CMGS="''' + self.phone_number + '''"\r\n''')
                time.sleep(1)
                for x in self.text:
                    self.ser.write(x + "\r\n")
                    time.sleep(1)
                    self.ser.write('\x1A')
                    time.sleep(3)
                    # print '4-',last_received
                    if last_received != 'OK\r\n':
                        end_tread = 0
                        self.ser.close()
                        return 1;
                end_tread = 0
                self.ser.close()
                return 0;

            def receiving(ser):
                global last_received
                global end_tread

                while end_tread:
                    last_received = ser.readline()
def dhtValue():
    humidity,temp = dht.read_retry(dht.DHT22,4)
    


if __name__ == "__main__":
    while True:
        gsmModule()
        mainMQtt()
        gps()
        dhtValue()
        headers = {
            'Content-Type':'application/json',
            'appKey':app_key,
            }
        payload = {
            prop_1:humidity,
            prop_2:temp,
            prop_3:lng,
            prop_4:lat,
            prop_5:moisture,
            }
        
