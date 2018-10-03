"""
from __future__ import division
from datetime import datetime 

import cv2
import csv
import os
import glob
import time
import random
import threading
import numpy as np
import sys
camera = cv2.VideoCapture(1)
try:
    while True:
        return_value,image = camera.read()
        #print(return_value)
        #image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        cv2.imshow('image',image)
        if cv2.waitKey(1)& 0xFF == ord('s'):
            cv2.imwrite('test.jpg',image)
            break
except:
    print ("Unexpected error:", sys.exc_info()[0])
    raise

camera.release()
cv2.destroyAllWindows()
"""
import numpy as np
import cv2

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720);
test = cap.get(cv2.CAP_PROP_FPS);
print (test)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("test.jpg", frame)
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()