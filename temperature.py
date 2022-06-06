import datetime
import glob
import time

LOGS = 720 # number of logs

# code from: circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file,'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while len(lines) == 0 or len(lines[0].strip()) < 3 or lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

# opens the temperaturelog.txt file to append
f_temperaturelog_a = open("temperaturelog.txt", "a")

# logs systemtime when the file starts running and confirms file open
f_temperaturelog_a.write(str(datetime.datetime.now()) + " file was successfully opened and run\n")
print(str(datetime.datetime.now()) + " temperature file was successfully opened and run\n")

# logs systemtime and temperature every ~2-3 seconds when time.sleep(0.2) in read_temp() and time.sleep(1) in for loop
for x in range(LOGS):
    #print(str(datetime.datetime.now()) + "; ")
    c, f = read_temp()
    print(str(datetime.datetime.now()) + ": ")
    f_temperaturelog_a.write(str(datetime.datetime.now()) + ": ")
    f_temperaturelog_a.write("Touch temperature: {0}*C {1}*F".format(c,f))
    f_temperaturelog_a.write("\n")
    print("Touch temperature: {0}*C {1}*F".format(c,f))
    print("\n")
    time.sleep(1)

conf = str(datetime.datetime.now()) + ": temperature logging complete, logged " + str(LOGS) + " times"
f_temperaturelog_a.write(conf)
f_temperaturelog_a.close()
print(conf)
