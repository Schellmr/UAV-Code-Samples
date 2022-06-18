

class Center:

    def __init__(self, width, height):
        self.w = width
        self.h = height

    def find_center(self, roll, pitch):
        cX = int(self.w / 2 + roll * 293.71)
        cY = int(self.h / 2 + pitch * 305.63)

        if cX > 319:
            cX = 319

        if cX < 0:
            cX = 0

        if cY > 239:
            cY = 239

        if cY < 0:
            cY = 0

        return cX, cY
