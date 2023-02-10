import socket
import sys
import os
import numpy as np
import pdb
import cv2
import io
import time
import traceback
import psutil
import signal
import serial
import subprocess as sp
from Image import *
from Utils import *
import picamera
from picamera import PiCamera
from picamera.array import PiRGBArray
from control_motores import *

font = cv2.FONT_HERSHEY_SIMPLEX
direction = 0
Images=[]
N_SLICES = 4
(w, h) = (630,230)
bytesPerFrame = w * h
fps = 30 # setting to 250 will request the maximum framerate possible
lateral_search = 20 # number of pixels to search the line border
start_height = h - 5
Speed =40
count = 0;
#MotorsSetup()
BaseSpeed(Speed)
for q in range(N_SLICES):
    Images.append(Image())

    
#videoCmd = "raspividyuv -w "+str(w)+" -h "+str(h)+" --output - --timeout 0 --framerate "+str(fps)+" --luma --nopreview"
#videoCmd = videoCmd.split() # Popen requires that each parameter is a separate string

#cameraProcess = sp.Popen(videoCmd, stdout=sp.PIPE) # start the camera
# this closes the camera process in case the python scripts exits unexpectedly

# wait for the first frame and discard it (only done to measure time more accurately)
#rawStream = cameraProcess.stdout.read(bytesPerFrame)
camera = PiCamera()
camera.resolution = (640,240)
camera.framerate = 40
camera.awb_mode = 'auto'
camera.exposure_mode = 'auto'
camera.image_denoise = True
camera.image_effect = 'colorbalance'
camera.image_effect_params = (1, 2, 1, 1)
rawCapture = picamera.array.PiRGBArray(camera)
rawCapture.truncate(0)
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
location = ""
s = 0
def cleanup_finish():
    MotorsStop()
    sys.exit(0)

def signal_handler(sig, frame):
        print('Stop Everything!')
        cleanup_finish()
        sys.exit(0)
        
while True:
    #cameraProcess.stdout.flush()
    if arduino.in_waiting >0:
        #MotorsSetup()
        continue
    #camera.capture(rawCapture, format="bgr")
    try:
        while True:
            #data = cameraProcess.stdout
            for data in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                #array = np.frombuffer(cameraProcess.stdout.read(bytesPerFrame), dtype=np.uint8)
                #img = cv2.imdecode(array, 1)
                img = data.array
                rawCapture.truncate(0)
                if arduino.in_waiting > 0:
                    MotorsSetup()
                    location = arduino.readline().decode("utf-8")
                    print(str(location))
                    print(type(location))
                    try:
                        s = int(location)
                    except ValueError:
                        pass
                    print(s)
                    print(type(s))
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
                    # Blur using 3 * 3 kernel.
                gray_blurred = cv2.blur(gray, (3, 3))
                #detected_circles = cv2.HoughCircles(gray_blurred, 
                    #cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                    #param2 = 30, minRadius = 38, maxRadius = 45)
            
                direction = 0
                img = RemoveBackground(img,True)
                if img is not None:
                    t1 = time.clock()
                    SlicePart(img, Images, N_SLICES)
                    for i in range(N_SLICES):
                        direction += Images[i].dir
                        #print(direction)
                        
                    Direction(int(direction)/4)
                    
                      
                    # Apply Hough transform on the blurred image.
                    detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.3,100)
                    
                    if detected_circles is not None:
                        # Convert the circle parameters a, b and r to integers.
                        detected_circles = np.round(detected_circles[0, :]).astype("int")
                        for (x,y,r) in detected_circles:
                        
                            cv2.circle(img, (x,y),r,(0,255,0),2)
                            if x > 0 and y >0 and r>0:
                                count = count + 1
                                temp = count
                                print(count)
                                if count == 4:
                                    MotorsPause()
                                    
                                    count = 0
                                    break
                                if count == s:
                                    MotorsPause()
                                    time.sleep(10)
                                    MotorsSetup()
                                    BaseSpeed(Speed)
                                    s= 0
                            

                   
                    fm = RepackImages(Images)
                    t2 = time.clock()
                    print(str((t2-t1)*1000))
                    cv2.imshow("Vision Race", fm)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        cleanup_finish()
                        break
                elif img < 10:
                   cleanup_finish()
                 
    except Exception as erro:
        exctype, value = sys.exc_info()[:2]
        print(exctype, value)
        print(traceback.format_exc())
        print(erro)
    finally:
        # Clean up the connection
        MotorsStop()
        cv2.destroyAllWindows()
        #connection.close()
        
        


