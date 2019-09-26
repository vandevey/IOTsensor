# See https://docs.pycom.io for more information regarding library specifics
import os
print(os.listdir())
import machine
import sys
import pycom
sys.path.append('/flash/DIM_PyCom_0X/')
sys.path.append('/flash/DIM_PyCom_0X/lib/')
#print(sys.path)
#print(sys.modules)
from pysense import Pysense

# seule la librairie pour la température est importée pour ce modèle
from SI7006A20 import SI7006A20
import ujson

#from wifi import WiFi
from network import WLAN
from mqtt import MQTTClient
import time
print('Imports ok')

wlan = WLAN(mode=WLAN.STA)

ssid='floki_guest'
pwd='#!F10ki_Gu357#1909'

IBMorgID='209kxe' # Identifiant de l'instance 'IoT PLatform' sur 6 caractères
deviceType='MicroPy' # Nom du 'Device Type' défini dans le IoT Platform
deviceID='001' # ID du device (4 dernieres caractères du SSID)
deviceToken='8IFLMGx1_9f?lnA6r-' # Token (mot de passe) défini pour le device dans le Iot Platform

#IBMorgID='514y4j' # Identifiant de l'instance 'IoT PLatform' sur 6 caractèrejys
#deviceType='PyCom' # Nom du 'Device Type' défini dans le IoT Platform
#deviceID='sdbd' # ID du device (4 dernieres caractères du SSID)
#deviceToken='gVVxAcc!tzALKKGHjn' # Token (mot de passe) défini pour le device dans le Iot Platform

print ('Start initializing')

py = Pysense()
si = SI7006A20(py)

#wifi = WiFi()

#print("Temperature: {} deg C and Relative Humidity: {} %RH"\
#      "".format(si.temperature(), si.humidity()))
#print("Dew point: {} deg C".format(si.dew_point()))

#WiFi.connectwifi(ssid,pwd)
wlan.connect(ssid, auth=(WLAN.WPA2, pwd), timeout=5000)
while not wlan.isconnected():
    machine.idle() # save power while waiting
    time.sleep(1)
print('WLAN connection succeeded!')

device="d:{}:{}:{}".format(IBMorgID, deviceType, deviceID)
print(device)
address="{}.messaging.internetofthings.ibmcloud.com".format(IBMorgID)
print(address)
print("Connecting to IBM IoT cloud platform...")
client = MQTTClient(device, address, user="use-token-auth",
                    password=deviceToken, port=8883, ssl=True)
try:
    rc=client.connect()
    if rc>0:
        print("Error connecting to IBM with result code: {}".format(rc))
        sys.exit(0)
    else:
        print("Connection to IBM with result code: {}".format(rc))
        temp = 0
        humid = 0
        sleep = 0
        SLEEP_1 = 1
        SLEEP_30 = 30
        ecartMax = 0.5
        while True:
            pycom.heartbeat(False)
            if si.temperature()<20 or si.temperature()>35:
                pycom.rgbled(0xFF0000)  # Red
            elif si.humidity() < 30 or si.humidity() > 50:
                pycom.rgbled(0xFF0000) # Red
            else:
                pycom.rgbled(0x00FF00)  # Green

            print("Sending")
            msg={}

            sleep = SLEEP_30
            if temp + ecartMax > si.temperature() or temp - ecartMax < si.temperature() or humid + ecartMax > si.humidity() or humid - ecartMax < si.humidity():
                msg['temp'] = si.temperature()
                msg['hum']=si.humidity()
                mqttMsg=ujson.dumps(msg)

            #mqttMsg = '{"temp":' + str(si.temperature())
            #mqttMsg = mqttMsg + '}'

                topic="iot-2/evt/data/fmt/json"
                print(mqttMsg)

                temp = si.temperature()
                humid = si.humidity()
                sleep = SLEEP_1
                client.publish(topic=topic, msg=mqttMsg)

            time.sleep(sleep)
except Exception as e:
    print(e.args)
    print(type(e))
print('Exiting...')
