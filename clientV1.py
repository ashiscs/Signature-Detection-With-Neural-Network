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
#from picamera import PiCamera

VIDEO_DIR = os.getcwd() + "/video/"
IMAGE_DIR = os.getcwd() + "/img_output/"

file_Name = VIDEO_DIR + "nano.mp4"

TCP_IP = 'localhost'
TCP_PORT = 5001

i=6
while(i):
    #camera = PiCamera()
    #camera.resolution = (256, 256)
    #camera.start_preview()
    #rawCapture = PiRGBArray(camera)
    #time.sleep(0.1)
    #camera.capture(rawCapture, format="bgr")
    #image = rawCapture.array
    
    sock = socket.socket()
    sock.connect((TCP_IP, TCP_PORT))
    #capture = cv2.VideoCapture(file_Name)
    #ret, image = capture.read()
    image = cv2.imread(IMAGE_DIR + "foo" + str(i) + ".jpg")

    r = 600.0 / image.shape[1]
    dim = (600, int(image.shape[0] * r))
     
    # perform the actual resizing of the image and show it
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    result, imgencode = cv2.imencode('.jpg', image, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()
    
    sock.send( str(len(stringData)).ljust(16).encode());
    sock.send( stringData );
    print(sock.recv(16).decode())
    sock.close()
    i -= 1
    time.sleep(2)
#decimg=cv2.imdecode(data,1)
#cv2.imshow('CLIENT',decimg)
#cv2.waitKey(0)
#cv2.destroyAllWindows() 
