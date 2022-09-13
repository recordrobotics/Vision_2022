# imports
import cv3 as cv
import numpy as np

# initialization
cap = cv.VideoCapture("""PLACEHOLDER - camera output could go here?""")
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # capture individual frames
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Operations on the frame
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()