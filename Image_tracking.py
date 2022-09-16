# imports
import cv2 as cv
import numpy as np

# initialization
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Subtractor selection
selection = "MOG2"
if selection == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()

while True:
    # capture individual frames
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Operations on the frame
    mask = backSub.apply(frame)
    # Display the resulting frame
    cv.imshow('Frame', frame)
    cv.imshow("Mask", mask)
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
