#all imports go here
import cv2 as cv
import sys
import numpy as np

#identifying cv version, needed for tracker type
(major_ver, minor_ver, subminor_ver) = (cv.__version__).split('.')
 
#choosing tracker types
if __name__ == '__main__' :

    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[7]
 
    if int(minor_ver) < 3:
        tracker = cv.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv.TrackerBoosting_create()
        elif tracker_type == 'MIL':
            tracker = cv.TrackerMIL_create()
        elif tracker_type == 'KCF':
            tracker = cv.TrackerKCF_create()
        elif tracker_type == 'TLD':
            tracker = cv.TrackerTLD_create()
        elif tracker_type == 'MEDIANFLOW':
            tracker = cv.TrackerMedianFlow_create()
        elif tracker_type == 'GOTURN':
             tracker = cv.TrackerGOTURN_create()
        elif tracker_type == 'MOSSE':
            tracker = cv.TrackerMOSSE_create()
        elif tracker_type == "CSRT":
            tracker = cv.TrackerCSRT_create()

#capture video
video = cv.VideoCapture(0)
#0 should be replaced with a file name if a saved video is used.

# Exit if video not opened.
if not video.isOpened():
  print("Could not open video")
  sys.exit()

# Read first frame.
ok, frame = video.read()
if not ok:
  print ('Cannot read video file')
  sys.exit()

#create an initial bounding box. The box should be around the object being tracked.
#The current values are placeholders
#bbox = (100, 200, 300, 400)
bbox = cv.selectROI(frame, False)

# Initialize tracker with first frame and bounding box
ok = tracker.init(frame, bbox)

while True:
     # Read a new frame
     ok, frame = video.read()
     if not ok:
         break
      
     # Start timer
     timer = cv.getTickCount()

     # Update tracker
     ok, bbox = tracker.update(frame)

     # Calculate Frames per second (FPS)
     fps = cv.getTickFrequency() / (cv.getTickCount() - timer);

     # Draw bounding box
     if ok:
         # Tracking success
         p1 = (int(bbox[0]), int(bbox[1]))
         p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
         cv.rectangle(frame, p1, p2, (255,0,0), 2, 1)
     else :
         # Tracking failure
         cv.putText(frame, "Tracking failure detected", (100,80), cv.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

     # Display tracker type on frame
     cv.putText(frame, tracker_type + " Tracker", (100,20), cv.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
  
     # Display FPS on frame
     cv.putText(frame, "FPS : " + str(int(fps)), (100,50), cv.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
     # Display result
     cv.imshow("Tracking", frame)

     # Exit if ESC pressed
     if cv.waitKey(1) & 0xFF == ord('q'): # if press SPACE bar
         break

video.release()
cv.destroyAllWindows()