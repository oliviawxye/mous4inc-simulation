import Adafruit_BMP.BMP085 as BMP085 # Imports the BMP library
import datetime
import time
import os.path

# https://thepihut.com/blogs/raspberry-pi-tutorials/18025084-sensors-pressure-temperature-and-altitude-with-the-bmp180#:~:text=The%20BMP180%20is%20an%20i2c,a%20lot%20of%20different%20devices.

# PATH
PATH_HOME = '/home/pi/Desktop/parallel/'

# opens the pressurelog.txt file to append
f_pressurelog_a = open(PATH_HOME + "pressurelog.txt", 'a')

# logs systemtime when the file starts running and confirms file open
f_pressurelog_a.write(str(datetime.datetime.now()) + " file was successfully opened and run\n")
print(str(datetime.datetime.now()) + " pressure file was successfully opened and run\n")

LOGS =  7200 # number of logs

sensor = BMP085.BMP085()

for x in range(LOGS):
    temperature = sensor.read_temperature()
    pressure = sensor.read_pressure()
    f_pressurelog_a.write("\n" + str(datetime.datetime.now()) + ":")
    f_pressurelog_a.write("Temp = {0:0.2f} *C".format(temperature))
    f_pressurelog_a.write("Pressure = {0:0.2f} Pa".format(pressure))
    print("\n" + str(datetime.datetime.now()) + ":")
    print("Temp = {0:0.2f} *C".format(temperature))
    print("Pressure = {0:0.2f} Pa".format(pressure))
    time.sleep(1)
    if os.path.exists(PATH_HOME + "shutdown.txt"):
        break

conf = str(datetime.datetime.now()) + ": pressure logging complete, logged " + str(x) + " times"
f_pressurelog_a.write(conf)
f_pressurelog_a.close()
print(conf)
