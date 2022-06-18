from cv2 import cv2
import cv2.aruco as aruco

dictionary = aruco.Dictionary_get(aruco.DICT_4X4_50)
marker = aruco.drawMarker(dictionary=dictionary, id=21, sidePixels=800, borderBits=1)

image = cv2.cvtColor(marker, cv2.COLOR_GRAY2BGR)

cv2.imwrite("marker.png", image)