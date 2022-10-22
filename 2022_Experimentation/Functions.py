import cv2 as cv
import numpy as np
import math


imgs = [cv.imread("blue_ball.jpg")]
cv.MergeExposures

#print(imgs[0].shape)
for i in range(len(imgs)):
    imgs[i] = cv.resize(imgs[i], (256, 144))

focalLength = 0
diagpx = 0
hpx = 0
diagFOV = 68.5
horizontalFOV = math.degrees(math.atan(math.tan(math.radians(diagFOV/2)) * (imgs[0].shape[1]/math.sqrt(imgs[0].shape[0]** 2 + imgs[0].shape[1]**2)) * 2))
#print(horizontalFOV, "HorizontalFOV")
ballWidth = 9.5
goalWidth = 39.25

def maskBalls(image):
    image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    #image = cv.GaussianBlur(image, (5,5), 0)
    #define colors
    upperLimit = np.array([255,100,100])
    lowerLimit = np.array([50,0,0])

    mask = cv.inRange(image.copy(), lowerLimit, upperLimit)

    return mask

def findCircle(image):
    #find circles in the masked image, return a center and a radius
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.medianBlur(image, 19)
    #DO NOT CHANGE VALUES OF CIRCLE TRANSFOR    M. Param1 = 28, Param2 = 30
    circles = cv.HoughCircles(image, cv.HOUGH_GRADIENT, 1, 100, param1=28, param2=30, minRadius=0, maxRadius=0) 
    return circles

def findDistance(width, focal, perWidth):
    return (width * focal) / perWidth

def calibrateBall(image, dist):
    global focalLength
    masked = maskBalls(image)
    
    #The below line originally began with _, which I deleted, causing the value error to disappear.
    contours, hierarchy = cv.findContours(masked, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    myContour = max(contours, key=cv.contourArea)

    M = cv.moments(myContour, True)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    
    area = cv.contourArea(myContour)
    diameter = math.sqrt(area/math.pi)*2

    focalLength = (diameter * dist)/ballWidth

def setDegPx(image):
    global diagpx
    global hpx

    width = image.shape[1]
    height = image.shape[0]
    diag = math.sqrt(width**2 + height**2)
    #print("diag", diag)

    diagpx = diagFOV/diag
    hpx = horizontalFOV/width

def findAngle(point, image):
    center = [image.shape[0]/2, image.shape[1]/2]
    return (center[1] - point[0])*hpx

def distanceToBall(image):
    masked = maskBalls(image)
    masked = cv.bitwise_and(image, image, mask = masked)

    circle = findCircle(masked)
    
    i = 0
    max = circle[i][0][2]**2 * math.pi

    for c in range(len(circle)):
        if circle[c][0][2]**2 * math.pi > max:
            max = circle[c][0][2]**2 * math.pi
        i = c
    
    try:
        radius = circle[i][0][2]
    except:
        return None
    center = (circle[i][0][0], circle[0][0][1])
    cv.circle(image, (center[0], center[1]), 3, (255, 0, 0), 3)
    
    
    
    print(center)

    #calculate angles and distances
    angle = findAngle(center, image)
    xDist = findDistance(ballWidth, focalLength, 2 * radius)
    distance = xDist / (math.cos(math.radians(angle)))

    return distance, angle

def calibrateGoal(image, distance):
    global focalLength
    masked = maskGoal(image)
    rect = findGoal(masked)

    focalLength = (rect[2] * distance)/goalWidth

def maskGoal(image):
    image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    upperLimit = np.array([90, 255, 255])
    lowerLimit = np.array([70, 120, 120])

    mask = cv.inRange(image.copy(), lowerLimit, upperLimit)

    return mask

def findGoal(mask):
    contours = cv.findContours(cv.Canny(mask.copy(), 30, 200), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)[1]
    contours = max(contours, key = cv.contourArea)
    rect = cv.boundingRect(contours)

    return rect

def distanceToGoal(image):
    mask = maskGoal(image)
    rect = findGoal(mask)

    distance = findDistance(goalWidth, focalLength, rect[2])

    contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)[1]
    myContour = max(contours, key=cv.contourArea)

    M = cv.moments(myContour, True)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    angle = findAngle(center, image)
    print(center)
    
    cv.circle(image, center, 3, (0, 0, 255), 6)
    cv.drawContours(image, [myContour], -1, (255, 0, 0), 1)
    '''
    cv.imshow("goal", image)
    cv.waitKey(0)
    cv.destroyAllWindows()
    '''
    distance = distance / (math.cos(math.radians(angle)))
    
    return distance, angle, center, [myContour]

def momentsBall(image):
    binImg = maskBalls(image)
    print(image.shape, "ImgShape")

    contours, hierarchy = cv.findContours(binImg, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    myContour = min(contours, key = contourCenter)

    M = cv.moments(myContour, True)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    print(center)
    
    area = cv.contourArea(myContour)
    print(area)
    
    #debuging output, do not run on RPi
    cv.circle(image, center, 3, (0, 0, 255), 3)
    cv.drawContours(image, [myContour], 0, (0, 255, 0), 3)
    cv.line(image, (128, 0), (128, 144), (255, 0, 0), 3)
    '''
    cv.imshow("potatoe", image)
    cv.waitKey(0)
    cv.destroyAllWindows()
    '''
    angle = findAngle(center, image)

    pxWidth = math.sqrt(area/math.pi)*2
    dist = findDistance(ballWidth, focalLength, pxWidth)
    dist = dist / math.cos(math.radians(angle))

    return dist, angle

def contourCenter(contour):
    width = 256

    M = cv.moments(contour, True)

    try:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print("HURRAH!")
    except:
        return math.inf
    
    if cv.contourArea(contour) < 1000:
        return math.inf

    return abs((width/2) - cx)

setDegPx(imgs[0])
calibrateBall(imgs[0], 36)

print(distanceToBall(imgs[0]))
