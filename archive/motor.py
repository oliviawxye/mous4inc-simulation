import datetime
from gpiozero import Servo
import time

servoPIN =  17
servo = Servo(servoPIN)

print(str(datetime.datetime.now()) + "motor file was successfully opened and run\n")
servo.max()
time.sleep(90)
servo.min()
