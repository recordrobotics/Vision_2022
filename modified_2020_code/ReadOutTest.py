import numpy as np
import cv2 as cv
import Distance

image = cv.imread("OtherImgs\goodFrame1.png")

Distance.setDegPx(image)
dist, ang, cent, cont = Distance.distanceToGoal(image)

cv.circle(image, cent, 20, (0, 0, 255), 5)
cv.drawContours(image, cont, 0, (255, 0, 0), 3)

cv.line(image, (int(image.shape[1]/2), 0), (int(image.shape[1]/2), image.shape[0]), (0, 0, 255), 3, lineType=4)

cv.putText(image, "0.00deg", (5, 32), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, 8)
cv.putText(image, "0.00ft", (5, 64), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, 8)
cv.putText(image, "[MISS]", (5, 96), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, 8)

cv.imshow("R-RAAS", image)
cv.waitKey(0)
cv.destroyAllWindows()