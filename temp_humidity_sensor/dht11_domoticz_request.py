import time
import board
import adafruit_dht
import requests
import datetime

# Initial the dht device, with data pin connected to (GPIO 27):
DHT_DEVICE = adafruit_dht.DHT11(board.D27)

# Domoticz server
SERVER="192.168.100.202:8080"
# DHT IDX FOR DOMOTICZ REQUEST
DHTIDX="1"
DATE_TIME_STRING = str(datetime.datetime.now())

def send_data_to_server(temperature_c, humidity):
       formated_temperature_c = "{:.1f}".format(temperature_c)
       print(DATE_TIME_STRING + " : ", formated_temperature_c, " - ", humidity)
       URL = ("http://" + SERVER + "/json.htm?type=command&c=getauth&param=udevice&idx=" +
              DHTIDX + "&nvalue=0&svalue=" + str(formated_temperature_c) + ";" + str(humidity) + ";2")
       print(DATE_TIME_STRING + " : " + "Sending request with url ", URL)

       r = requests.get(url = URL) 

       data = r.json()
       print(data)

# try to get data 20 times
for x in range(20):
       try:
 
              temperature_c = DHT_DEVICE.temperature
              temperature_f = temperature_c * (9 / 5) + 32
              humidity = DHT_DEVICE.humidity
              print(DATE_TIME_STRING + " : " + "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))
              
              send_data_to_server(temperature_c, humidity)
              break
       except Exception as error:
              # Errors happen fairly often, DHT's are hard to read, just keep going 
              print(DATE_TIME_STRING + " : " + error.args[0])
              time.sleep(5)
              pass