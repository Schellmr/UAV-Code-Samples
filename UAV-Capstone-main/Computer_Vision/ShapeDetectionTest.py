import cv2
import numpy as np
#from picamera import PiCamera


def nothing(x):
    # any operation
    pass


cap = cv2.VideoCapture(0)
# -1 on RaspberryPi

font = cv2.FONT_HERSHEY_COMPLEX


while True:

    _, frame = cap.read()
    cv2.normalize(frame, frame, 65, 190, cv2.NORM_MINMAX)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 75, 40), (180, 255, 255))
    mask_3d = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
    blurred_frame = cv2.GaussianBlur(frame, (25, 25), 0)
    frame = np.where(mask_3d == (255, 255, 255), frame, blurred_frame)

    lower_red = np.array([000, 66, 134])
    upper_red = np.array([180, 255, 243])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)

    # Contours detection
    if int(cv2.__version__[0]) > 3:
        # Opencv 4.x.x
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        # Opencv 3.x.x
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        M = cv2.moments(cnt) #calculates the centroid of the box around object (lines 60-62 & 66)
        cX = int((M["m10"] + .001)/ (M["m00"] + .001))
        cY = int((M["m01"] + .001)/ (M["m00"] + .001))

        if area > 400:
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
            cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(frame, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            if len(approx) == 3:
                cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
            elif len(approx) == 4:
                cv2.putText(frame, "Rectangle", (x, y), font, 1, (0, 0, 0))
            elif 7 < len(approx):
                cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
