import cv2
from core.contour.contour import Contour
from core.tools import *
import numpy as np


class ROI(object):
    def __init__(self, contour, skin, contourSkin):
        self.contour = contour
        self.contourSkin = contourSkin
        self.skin = skin

    def calK(self, p0, p1):
        if p0[0] == p1[0]:
            return 2
        if abs(p0[1] - p1[1]) < 20:
            return 0
        k = (p1[1] - p0[1]) / (p1[0] - p0[0])
        return k

    def roi(self, contour, userName):
        global ImagePath
        ImagePath = "../../image/{}.jpg".format(userName)
        global UserName
        UserName = ImagePath.replace(".jpg", "").replace(".jpeg", "").replace(".png", "")
        points = []
        img_rows, img_cols, _ = self.contour.shape
        hull = cv2.convexHull(contour, returnPoints=False)
        defects = cv2.convexityDefects(contour, hull)  # 返回的前三个值是点在轮廓中的索引
        defects = defects[:, 0, :]
        temp = sorted(defects, key=lambda entity: entity[3], reverse=True)
        for i in range(4):
            s, e, f, d = temp[i]
            far = tuple(contour[f][0])
            number = f
            while self.calK(contour[number - 1, 0], contour[number, 0]) < 1:
                number -= 3
            right = number
            number = f
            while self.calK(contour[number, 0], contour[number + 1, 0]) < 1:
                number += 3
            left = number
            points.append(tuple(contour[left, 0]))
            points.append(tuple(contour[right, 0]))
            cv2.circle(self.contour, far, 5, [0, 0, 255], -1)
            cv2.circle(self.contourSkin, tuple(contour[left][0]), 5, [255, 255, 255], -1)
            cv2.circle(self.contourSkin, tuple(contour[right][0]), 5, [0, 255, 255], -1)
        cv2.imwrite("{0}_contour_anchor.jpg".format(UserName), contourSkin)
        self.points = sorted(points, key=lambda x: x[0])

    def roi_main(self, contours):
        x_min = self.points[0][0]
        y_min = self.points[0][1]
        x_max = self.points[0][0]
        y_max = self.points[0][1]
        for each in self.points:
            y = each[1]
            x = each[0]
            if y <= y_min:
                y_min = y
            if x <= x_min:
                x_min = x
            if x >= x_max:
                x_max = x
            if y >= y_max:
                y_max = y
        for each in contours:
            x = each[0][0]
            y = each[0][1]
            if x <= x_min + 3 and x >= x_min - 3 and y >= y_max:
                y_max = y
            if y >= y_min - 3 and y <= y_min + 3 and x >= x_max:
                x_max = x
        top_left = (x_min, y_min)
        bottom_right = (x_max, y_max)
        cv2.rectangle(self.contourSkin, top_left, bottom_right, (255, 255, 0), 3)
        cv2.imwrite("{0}_roi_main.jpg".format(UserName), self.contourSkin)
        out = self.skin.copy()[top_left[1]:bottom_right[1],top_left[0]:bottom_right[0],:]
        cv2.imwrite("{0}_roi_main_out.jpg".format(UserName), out)

    def roi_10(self):
        x_min = self.points[2][0]
        y_min = self.points[2][1]



if __name__ == '__main__':
    userName = "cqh_test"
    c = Contour(userName)
    ct, skin, contour, contourSkin = c.drawContour()
    r = ROI(contour, skin, contourSkin)
    r.roi(ct, userName)
    r.roi_main(ct)
