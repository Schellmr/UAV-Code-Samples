
import cv2
import numpy as np

webcam = cv2.VideoCapture(0)

while(1):

    _, imageFrame = webcam.read()

    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    white_lower = np.array([200, 200, 200], np.uint8)
    white_upper = np.array([255, 255, 255], np.uint8)
    white_mask = cv2.inRange(hsvFrame, white_lower, white_upper)

    kernal = np.ones((5, 5), "uint8")

    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(imageFrame, imageFrame,
                              mask = red_mask)

    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(imageFrame, imageFrame,
                                mask = green_mask)

    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(imageFrame, imageFrame,
                               mask = blue_mask)

    white_mask = cv2.dilate(white_mask, kernal)
    res_white = cv2.bitwise_and(imageFrame, imageFrame,
                               mask = white_mask)

    contours, hierarchy = cv2.findContours(red_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            #gray_image = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY) # convert to grayscale for centroid
            #ret,thresh = cv2.threshold(gray_image,127,255,0) # convert to binary image
            #M = cv2.moments(thresh) # calculate moments of binary image
            #cX = int(M["m10"] / M["m00"]) # calculate x,y coordinate of center
            #cY = int(M["m01"] / M["m00"])
            imageFrame = cv2.rectangle(imageFrame, (x, y),
                                       (x + w, y + h),
                                       (0, 0, 255), 2)

            cv2.putText(imageFrame, "Red", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))

            #cv2.circle(imageFrame, (cX, cY), 5, (255, 255, 255), -1)

            print("Red")

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(green_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),
                                       (x + w, y + h),
                                       (0, 255, 0), 2)

            cv2.putText(imageFrame, "Green", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (0, 255, 0))

            print("Green")

    # Creating contour to track blue color
    contours, hierarchy = cv2.findContours(blue_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),
                                       (x + w, y + h),
                                       (255, 0, 0), 2)

            cv2.putText(imageFrame, "Blue", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (255, 0, 0))

            print("Blue")

    contours, hierarchy = cv2.findContours(white_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),
                                       (x + w, y + h),
                                       (255, 255, 255), 2)

            cv2.putText(imageFrame, "White", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (255, 255, 255))

    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
