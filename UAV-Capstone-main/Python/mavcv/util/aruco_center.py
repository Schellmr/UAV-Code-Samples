import cv2.aruco as aruco
import cv2
import numpy


class FindAruco:

    def __init__(self):
        self.dictionary = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.parameters = aruco.DetectorParameters_create()

    def is_aruco(self, image):
        marker_corners, marker_ids, _ = aruco.detectMarkers(image=image, dictionary=self.dictionary,
                                                            parameters=self.parameters)
        if marker_ids is None:
            return False

        self.corners = marker_corners
        self.ids = marker_ids

        for i in range(len(self.ids)):
            if self.ids[i] == 10:
                c = self.corners[i][0]
                self.cX = c[:, 0].mean()
                self.cY = c[:, 1].mean()
                return True

        return False

    def return_center(self):
        return int(self.cX), int(self.cY)
