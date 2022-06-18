import cv2.aruco as aruco


class ArucoFinder:

    def __init__(self):
        self.dictionary = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.parameters = aruco.DetectorParameters_create()
        self.cX = 0
        self.cY = 0

    def is_aruco(self, image):
        marker_corners, marker_ids, _ = aruco.detectMarkers(image=image, dictionary=self.dictionary,
                                                            parameters=self.parameters)
        if marker_ids is None:
            return False

        corners = marker_corners
        ids = marker_ids

        for i in range(len(ids)):
            if ids[i] == 45:
                c = corners[i][0]
                self.cX = c[:, 0].mean()
                self.cY = c[:, 1].mean()
                return True
            elif ids[i] == 10:
                c = corners[i][0]
                self.cX = c[:, 0].mean()
                self.cY = c[:, 1].mean()
                return True

        return False

    def return_center(self):
        return int(self.cX), int(self.cY)
