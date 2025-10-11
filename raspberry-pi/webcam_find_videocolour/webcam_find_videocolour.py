import numpy as np
import cv2 as cv
from color_names import *

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0) # manual mode, still broken
cap.set(cv.CAP_PROP_SATURATION, 100) # dont wash colors we need em stronk
cap.set(cv.CAP_PROP_BRIGHTNESS, -50) # workaround for exposure bug
mid_w=int(cap.get(cv.CAP_PROP_FRAME_WIDTH)/2) # get middle of width
mid_h=int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)/2) # get middle of height

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    color = cv.cvtColor(frame, cv.COLOR_RGB2RGBA)
    # Display the resulting frame
    cv.imshow('frame', color)
    print(ColorNames.findNearestImageMagickColorName(frame[mid_h,mid_w][2],frame[mid_h,mid_w][1],frame[mid_h,mid_w][0]))
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
