import serial
import RPI.GPIO as GPIO
import pynmea2
GPIO.setmode(GPIO.BOARD)

def gps():
    gpsSerial = serial.Serial('/dev/ttyAMC0',9600)
    dataout = pynmea2.NMEAStreamReader()
    newdata = gpsSerial.readline()
    if newdata[0:6] == "$GPRMC":
        newmsg = pynmea2.parse(newdata)
        lat = newmsg.latitude
        lng = newmsg.longitute
        
        