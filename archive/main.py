#!/usr/bin/python

""" 
Z Porter
NanoRacks LLC
Version 2.0
Last updated: 2-11-19
"""

# flight event codes to start each process
FLIGHT_EVENT_RESET_FILES = 'A'
FLIGHT_EVENT_CAMERA = 'C'
FLIGHT_EVENT_MOTOR = 'D'
FLIGHT_EVENT_TEMPERATURE = 'F'
FLIGHT_EVENT_LEDS = 'C'
FLIGHT_EVENT_MISSION_END = 'M'
FLIGHT_EVENT_AMBIENT = 'F'
FLIGHT_EVENT_PRESSURE = 'F'

import time
import serial
from subprocess import Popen
import datetime

MAXBUFFER = 200
NUMDATAFIELDS = 21

# This is specific to the pi zero. Must have serial enabled and console over serial disabled.
PORTNAME = '/dev/ttyGS0'

BAUDRATE = 115200
TIMEOUT = 0.02

# Dictionary to hold all of the current flight information.
FLIGHT_DATA = {'flight_event': 0, 
                'exptime': 0,
                'altitude': 0,
                'gps_altitude': 0,
                'velocity': [0,0,0],
                'acc_magnitude': 0,
                'acceleration': [0,0,0],
                'attitude': [0,0,0],
                'angular_velocity': [0,0,0],
                'warnings': [0,0,0,0]}


""" parse_serial_packet """
# Parses the incoming serial packet and updates the flight data
def parse_serial_packet(incoming_data):
    # Remove leading or trailing white space and separate the fields.
    incoming_data = incoming_data.strip()
    fields = incoming_data.decode().split(',')

    # Ensure that the appropriate number of data fields are present.
    if len(fields) != NUMDATAFIELDS:
        return False
    else:
        index = 0
        for field in fields:
            if index == 0:
                FLIGHT_DATA['flight_event'] = field
            elif index == 1:
                FLIGHT_DATA['exptime'] = float(field)
            elif index == 2:
                FLIGHT_DATA['altitude'] = float(field)
            elif index == 3:
                FLIGHT_DATA['gps_altitude'] = float(field)
            elif index == 4:
                FLIGHT_DATA['velocity'][0] = float(field)
            elif index == 5:
                FLIGHT_DATA['velocity'][1] = float(field)
            elif index == 6:
                FLIGHT_DATA['velocity'][2] = float(field)
            elif index == 7:
                FLIGHT_DATA['acc_magnitude'] = float(field)
            elif index == 8:
                FLIGHT_DATA['acceleration'][0] = float(field)
            elif index == 9:
                FLIGHT_DATA['acceleration'][1] = float(field)
            elif index == 10:
                FLIGHT_DATA['acceleration'][2] = float(field)
            elif index == 11:
                FLIGHT_DATA['attitude'][0] = float(field)
            elif index == 12:
                FLIGHT_DATA['attitude'][1] = float(field)
            elif index == 13:
                FLIGHT_DATA['attitude'][2] = float(field)
            elif index == 14:
                FLIGHT_DATA['angular_velocity'][0] = float(field)
            elif index == 15:
                FLIGHT_DATA['angular_velocity'][1] = float(field)
            elif index == 16:
                FLIGHT_DATA['angular_velocity'][2] = float(field)
            elif index == 17:
                FLIGHT_DATA['warnings'][0] = int(field)
            elif index == 18:
                FLIGHT_DATA['warnings'][1] = int(field)
            elif index == 19:
                FLIGHT_DATA['warnings'][2] = int(field)
            elif index == 20:
                FLIGHT_DATA['warnings'][3] = int(field)
            index = index + 1
        return True


# Confirm file has started running successfully
def init_experiment():
    print("initializing experiment")    

# Opens mainlog.txt to overwrite previous information and append information
f_mainlog_a = open("mainlog.txt", "a")
f_mainlog_w = open("mainlog.txt", "w")

# Opens temperaturelog.txt to overwrite previous information and add text
f_temperaturelog_a = open("temperaturelog.txt", "a")
f_temperaturelog_w = open("temperaturelog.txt", "w")

# Opens ambientlog.txt to overwrite previous information and add text
f_ambientlog_a = open("ambientlog.txt", "a")
f_ambientlog_w = open("ambientlog.txt", "w")

# Opens pressurelog.txt to overwrite previous information and add text
f_pressurelog_a = open("pressurelog.txt", "a")
f_pressurelog_w = open("pressurelog.txt", "w")

""" reset_files """
def reset_files(telemetry):
    print_str = str(datetime.datetime.now()) + "; " + telemetry + "; reset file\n"
    global f_mainlog_w
    global f_temperaturelog_w
    global f_ambientlog_w
    global f_pressurelog_w
    f_mainlog_w.write(print_str)
    f_temperaturelog_w.write(print_str)
    f_ambientlog_w.write(print_str)
    f_pressurelog_w.write(print_str)

""" run_camera """
# log systemtime, telemetry, and camera on action to mainlog.txt
# call camera.py to run
def run_camera(telemetry):
    global f_mainlog_a
    f_mainlog_a.write(str(datetime.datetime.now()) + "; " + telemetry + "; camera on\n")
    print(str(datetime.datetime.now()) + "; " + telemetry + "; run_camera successful in main.py\n")
    Popen(['python3', 'camera.py'])

""" run_motor """
# log systemtime, telemetry, and motor on action to mainlog.txt
# call motor.py to run
def run_motor(telemetry):
    global f_mainlog_a
    f_mainlog_a.write(str(datetime.datetime.now()) + "; " + telemetry + "; motor on\n")
    print(str(datetime.datetime.now()) + "; " + telemetry + "; run_motor successful in main.py\n")
    Popen(['python3', 'motor.py'])

""" run_temperature """
# log systemtime, telemetry, and temperature on action to mainlog.txt
# log systemtime, and telemetry to temperaturelog.txt
# call temperature.py to run
def run_temperature(telemetry):
    global f_mainlog_a
    global f_temperaturelog_w
    f_mainlog_a.write(str(datetime.datetime.now()) + "; " + telemetry + "; temperature on\n")
    print(str(datetime.datetime.now()) + "; " + telemetry + "; run_temperature sucessful in main.py\n")
    f_temperaturelog_a.write(str(datetime.datetime.now()) + "; " + telemetry + "\n")
    Popen(['python3', 'temperature.py'])

""" run_leds """
# log systemtime, telemetry, and leds on action to mainlog.txt
# call leds.py to run
def run_leds(telemetry):
    global f_mainlog_a
    f_mainlog_a.write(str(datetime.datetime.now()) + "; " + telemetry + "; leds on\n")
    print(str(datetime.datetime.now()) + "; " + telemetry + "; run_leds successful in main.py\n")
    Popen(['python3', 'leds.py'])

""" run_ambient """
# log systemtime, telemetry, and ambient temp/humidity on action to mainlog.txt
# log systemtime, and telemetry to ambientlog.txt
# call ambient.py to run
def run_ambient(telemetry):
    global f_mainlog_a
    global f_ambientlog_w
    f_mainlog_a.write(str(datetime.datetime.now()) + "; " + telemetry + "; ambient on\n")
    print(str(datetime.datetime.now()) + "; " + telemetry + "; run_ambient successful in main.py\n")
    f_ambientlog_a.write(str(datetime.datetime.now()) + "; " + telemetry + "\n")
    Popen(['python3', 'ambient.py'])

""" run_pressure"""
# log systemtime, telemetry, and ambient temp/pressure on action to mainlog.txt
# log systemtime, and telemetry to pressurelog.txt
# call pressure.py to run
def run_pressure(telemetry):
    global f_mainlog_a
    global f_ambientlog_w
    f_mainlog_a.write(str(datetime.datetime.now()) + "; " + telemetry + "; pressure on\n")
    print(str(datetime.datetime.now()) + "; " + telemetry + "; run_pressure successful in main.py\n")
    f_pressurelog_a.write(str(datetime.datetime.now()) + "; " + telemetry + "\n")
    Popen(['python3', 'pressure.py'])

""" stop_log_files """
# close all files
def stop_log_files():
    global f_mainlog_a
    global f_mainlog_w
    global f_temperaturelog_a
    global f_temperaturelog_w
    global f_ambientlog_a
    global f_ambientlog_w
    global f_pressurelog_a
    global f_pressurelog_w
    f_mainlog_a.close()
    f_mainlog_w.close()
    f_temperaturelog_a.close()
    f_temperaturelog_w.close()
    f_ambientlog_a.close()
    f_ambientlog_w.close()
    f_pressurelog_a.close()
    f_pressurelog_w.close()

""" main """
def main():
    # Wait about 5 seconds before starting (probably unnecessary)
    time.sleep(5)

    # Initialize the experiment.
    init_experiment()

    # Open serial connection. 
    ser = serial.Serial(port=PORTNAME, baudrate=BAUDRATE, timeout=TIMEOUT)

    # set all function run variables to false
    has_files_reset = False
    has_camera_run = False
    has_motor_run = False
    has_temperature_run = False
    has_leds_run = False
    has_ambient_run = False
    has_pressure_run = False

    # Main loop to continuously read in incoming data and attempt to parse it.
    while True:
        # Check for any available data in the input serial buffer according to the polling rate.
        while ser.in_waiting == 0:
            time.sleep(0.01)

        # Read in up to the maximum size of data per line.
        data_in = ser.read(MAXBUFFER)
        
        # Check that some data was received.
        if (len(data_in) == 0):
            continue

        # Check that packet was well formatted.
        if not parse_serial_packet(data_in):
            continue

        # recompile a string with current flight telemetry data 
        telemetry = str(FLIGHT_DATA['flight_event']) + ","
        telemetry += str(FLIGHT_DATA['exptime']) + ","
        telemetry += str(FLIGHT_DATA['altitude']) + ","
        telemetry += str(FLIGHT_DATA['gps_altitude']) + ","
        telemetry += str(FLIGHT_DATA['velocity'][0]) + ","
        telemetry += str(FLIGHT_DATA['velocity'][1]) + ","
        telemetry += str(FLIGHT_DATA['velocity'][2]) + ","
        telemetry += str(FLIGHT_DATA['acc_magnitude']) + ","
        telemetry += str(FLIGHT_DATA['acceleration'][0]) + ","
        telemetry += str(FLIGHT_DATA['acceleration'][1]) + ","
        telemetry += str(FLIGHT_DATA['acceleration'][2]) + ","
        telemetry += str(FLIGHT_DATA['attitude'][0]) + ","
        telemetry += str(FLIGHT_DATA['attitude'][1]) + ","
        telemetry += str(FLIGHT_DATA['attitude'][2]) + ","
        telemetry += str(FLIGHT_DATA['angular_velocity'][0]) + ","
        telemetry += str(FLIGHT_DATA['angular_velocity'][1]) + ","
        telemetry += str(FLIGHT_DATA['angular_velocity'][2]) + ","
        telemetry += str(FLIGHT_DATA['warnings'][0]) + ","
        telemetry += str(FLIGHT_DATA['warnings'][1]) + ","
        telemetry += str(FLIGHT_DATA['warnings'][2]) + ","
        telemetry += str(FLIGHT_DATA['warnings'][3]) 
        #print(telemetry)

        if not has_files_reset:
            if (FLIGHT_DATA['flight_event'] == FLIGHT_EVENT_RESET_FILES):
                reset_files(telemetry)
                has_files_reset = True

        # checks if the camera has not run
            # true: check for flight event
                # true: call run_camera function
                # false: skip
            # false: skip
        if not has_camera_run:
            if (FLIGHT_DATA['flight_event'] == FLIGHT_EVENT_CAMERA): 
                run_camera(telemetry)
                has_camera_run = True
        
        # checks if the motor has not run
            # true: check for flight event
                # true: call run_motor function
                # false: skip
            # false: skip
        if not has_motor_run:
            if (FLIGHT_DATA['flight_event'] == FLIGHT_EVENT_MOTOR): 
                run_motor(telemetry)
                has_motor_run = True
         
        # checks if the temperature has not run
            # true: check for flight event
                # true: call run_temperature function
                # false: skip
            # false: skip
        if not has_temperature_run:
            if (FLIGHT_DATA['flight_event'] == FLIGHT_EVENT_TEMPERATURE): 
                #global f_temperaturelog_w.write(str(datetime.datetime.now()) + ": reset\n")
                run_temperature(telemetry)
                has_temperature_run = True

        # checks if the leds has not run
            # true: check for flight event
                # true: call run_leds function
                # false: skip
            # false: skip
        if not has_leds_run:
            if (FLIGHT_DATA['flight_event'] == FLIGHT_EVENT_LEDS): 
                run_leds(telemetry)
                has_leds_run = True

        # checks if ambient has not run
            # true: check for flight event
                # true: call run_ambient function
                # false: skip
            # false: skip
        if not has_ambient_run:
            if (FLIGHT_DATA['flight_event'] == FLIGHT_EVENT_AMBIENT):
                #global f_ambientlog_w.write(str(datetime.datetime.now()) + ": reset\n")
                run_ambient(telemetry)
                has_ambient_run = True

        # checks if pressure has not run
            # true: check for flight event
                # true: call run_pressure function
                # false: skip
            # false: skip
        if not has_pressure_run:
            if (FLIGHT_DATA['flight_event'] == FLIGHT_EVENT_PRESSURE):
                #global f_pressurelog_w.write(str(datetime.datetime.now()) + ": reset'n")
                run_pressure(telemetry)
                has_pressure_run = True

        # calls stop_log_files function if mission has ended
        if (FLIGHT_DATA['flight_event'] == FLIGHT_EVENT_MISSION_END): # M is mission end
            stop_log_files()


if __name__=="__main__":
    main()

