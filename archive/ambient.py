import Adafruit_DHT as dht
from time import sleep
import datetime

# https://www.instructables.com/Raspberry-Pi-Tutorial-How-to-Use-the-DHT-22/

# opens the ambientlog.txt file to append
f_ambientlog_a = open("ambientlog.txt", 'a')

# logs systemtime when the file starts runing and confirms file open
f_ambientlog_a.write(str(datetime.datetime.now()) + " file was successfully opened and run\n")
print(str(datetime.datetime.now()) + " ambient file was successfully opened and run\n")

LOGS = 720 # number of logs

#Set DATA pin
DHT = 22


for x in range(LOGS):
    #Read temp and  hum from DHT22
    h, t = dht.read_retry(dht.DHT22, DHT)
    
    #Print Temperature and Humidity
    f_ambientlog_a.write(str(datetime.datetime.now()) + " :")
    f_ambientlog_a.write('Temp= {0:0.01f}*C Humidity={1:0.01f}%'.format(t,h))
    f_ambientlog_a.write('\n')
    print(str(datetime.datetime.now()) + " :")
    print("Temp = {0}*C Humidity={1}%".format(t,h))
    print("\n")
    sleep(0.1)

conf = str(datetime.datetime.now()) + ": ambient logging complete, logged " + str(LOGS) + " times"
f_ambientlog_a.write(conf)
f_ambientlog_a.close()
print(conf)

