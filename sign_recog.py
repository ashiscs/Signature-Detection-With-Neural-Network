# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 23:38:20 2018
@author: Ashis Kumar Singh
"""

import socket
import cv2
import numpy
import os
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO

lcd = CharLCD(cols=16, rows=2, pin_rs=2, pin_rw=3, pin_e=4, pins_data=[5, 6, 7, 8], numbering_mode=GPIO.BCM)

GPIO.setwarnings(False)

#VIDEO_DIR = os.getcwd() + "/video/"
#IMAGE_DIR = os.getcwd() + "/img_output/"

#file_Name = VIDEO_DIR + "nano.mp4"

TCP_IP = '192.168.1.103'
TCP_PORT = 5001

print("Run")
#i=6
sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))
print("Socket create")

while(1):
    camera = PiCamera()
    camera.resolution = (1024, 512)
    camera.start_preview()
    camera.color_effects = (128,128)
    rawCapture = PiRGBArray(camera)
    time.sleep(0.1)
    camera.capture(rawCapture, format="bgr")
    #img_gray = cv2.cvtColor(rawCapture, cv2.COLOR_BGR2GRAY)
    image = rawCapture.array
    print("image capture")
    #capture = cv2.VideoCapture(file_Name)
    #ret, image = capture.read()
    #image = cv2.imread(IMAGE_DIR + "foo" + str(i) + ".jpg")

    #r = 600.0 / image.shape[1]
    #dim = (600, int(image.shape[0] * r))

    # perform the actual resizing of the image and show it
    #resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    result, imgencode = cv2.imencode('.jpg', image, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()

    sock.send( str(len(stringData)).ljust(16).encode())
    sock.send( stringData )
    str_msg = sock.recv(32).decode()
    print(str_msg)
    lcd.clear()
    lcd.cursor_pos = (0, 0) #line1
    lcd.write_string(str_msg)
    #lcd.cursor_pos = (0, 14)
    #lcd.write_string("%")
    #lcd.cursor_pos = (1, 3) #line2
    #lcd.write_string("confidence")
    #i -= 1
    #camera.stop_preview()
    camera.close()
    time.sleep(1)
    #lcd.clear()
    GPIO.setwarnings(False)
sock.close()
print("Socket close")
#decimg=cv2.imdecode(data,1)
#cv2.imshow('CLIENT',decimg)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
