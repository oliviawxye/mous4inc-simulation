import datetime
import time
import RPi.GPIO as io

io.setmode(io.BCM)

led1 = 27
led2 = 23
led3 = 24
led4 = 5
led5 = 6
backlight1 = 13
backlight2 = 12

io.setup(led1, io.OUT)
io.setup(led2, io.OUT)
io.setup(led3, io.OUT)
io.setup(led4, io.OUT)
io.setup(led5, io.OUT)
io.setup(backlight1, io.OUT)
io.setup(backlight2, io.OUT)


io.output(led1, True)
io.output(led2, True)
io.output(led3, True)
io.output(led4, True)
io.output(led5, True)
io.output(backlight1, True)
io.output(backlight2, True)
time.sleep(720)
io.output(led1, False)
io.output(led2, False)
io.output(led3, False)
io.output(led4, False)
io.output(led5, False)
io.output(backlight1, False)
io.output(backlight2, False)

io.cleanup()

print(str(datetime.datetime.now()) + "leds file was successfully opened and run\n")

