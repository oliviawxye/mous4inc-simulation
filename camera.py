import datetime
import time
from picamera import PiCamera
import os.path

PATH_HOME = '/home/pi/Desktop/parallel/'
#TEST_NUM = 14
RES_WIDTH = 1280
RES_HEIGHT = 720
FPS = 24
FORMAT = "h264"
REC_TIME = 720
#TEST_NUM_FORMAT = str(TEST_NUM).zfill(3)
FILENAME = PATH_HOME + 'ppc-' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S-") + str(RES_WIDTH) + "w-" + str(RES_HEIGHT) + "h-" + str(FPS) + "fps-" + str(REC_TIME) + "s-test" +  "." + FORMAT 

# camera resolution and framerate
cam = PiCamera(resolution = [RES_WIDTH, RES_HEIGHT], framerate = FPS)


# confirm the file has successfully run 
print(str(datetime.datetime.now()) + "camera file was successfully opened and run\n")
time.sleep(5)
print(str(datetime.datetime.now()) + "start recording on camera.py\n")

# start recording
# file name needs to change to reflect width, height, framerate, length of recording, and test number each time
cam.start_recording(FILENAME, format=FORMAT)
#time.sleep(REC_TIME) # recording time

while True:
    if os.path.exists(PATH_HOME + "shutdown.txt"):
        break
    time.sleep(10)

cam.stop_recording()
cam.close()

# confirm the camera has stopped recording
print(str(datetime.datetime.now()) + "stop recording on camera.py\n")


