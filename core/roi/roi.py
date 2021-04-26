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

    def roi(self, contour, imageName, fullPath):
        global ImagePath
        ImagePath = "{}/{}.jpg".format(fullPath, imageName)
        global ImgSavePath
        ImgSavePath = ImagePath.replace(".jpg", "")
        points = []
        # img_rows, img_cols, _ = self.contour.shape
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
        cv2.imwrite("{0}_contour_anchor.jpg".format(ImgSavePath), contourSkin)
        self.points = points
        x = []
        y = []
        for each in self.points:
            y.append(each[1])
            x.append(each[0])
        self.x = sorted(x)
        self.y = sorted(y)

    def roi_main(self, contours):
        yy = sorted(self.y, reverse=True)
        x_min = min(self.x)
        x_max = max(self.x)
        y_min = yy[3]
        y_max = max(self.y)
        for each in contours:
            x = each[0][0]
            y = each[0][1]
            if x <= x_min + 3 and x >= x_min - 3 and y >= y_max:
                y_max = y
        top_left = (x_min, y_min)
        bottom_right = (x_max, y_max)
        scp = self.contourSkin.copy()
        cv2.rectangle(scp, top_left, bottom_right, (255, 255, 0), 3)
        cv2.imwrite("{0}_roi_main.jpg".format(ImgSavePath), scp)
        out = self.skin.copy()[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0], :]
        cv2.imwrite("{0}_roi_main_out.jpg".format(ImgSavePath), out)
        self.main_point = [top_left, bottom_right]
        return out

    def roi_thenar(self):
        top_left = (min(self.x) + 7, max(self.y) + 7)
        bottom_right = (
            int((self.main_point[1][0] - self.main_point[0][0]) / 2) + self.main_point[0][0], self.main_point[1][1])
        scp = self.contourSkin.copy()
        cv2.rectangle(scp, top_left, bottom_right, (0, 255, 0), 3)
        cv2.imwrite("{0}_roi_thenar.jpg".format(ImgSavePath), scp)
        out = self.skin.copy()[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0], :]
        cv2.imwrite("{0}_roi_thenar_out.jpg".format(ImgSavePath), out)
        return out

    def roi_5(self):
        p1 = p2 = (0, 0)
        for each in self.points:
            if each[0] == self.x[3]:
                p1 = each
            if each[0] == self.x[4]:
                p2 = each
        y = int((self.main_point[1][1] - self.main_point[0][1]) / 2 + self.main_point[0][1])
        center_x = ((self.main_point[1][0] - self.main_point[0][0]) / 2 + self.main_point[0][0])
        x1 = int(center_x * 0.875)
        x2 = int(center_x * 1.125)
        p3 = (x1, y)
        p4 = (x2, y)
        p = np.array([p1, p2, p4, p3], np.int32)
        scp = self.contourSkin.copy()
        cv2.polylines(scp, [p], True, (0, 255, 255), 3)
        cv2.imwrite("{0}_roi_5.jpg".format(ImgSavePath), scp)
        # mask = np.zeros(self.skin.copy().shape, dtype=np.uint8)
        # mask2 = cv2.fillPoly(mask, [p], (255, 255, 255))
        # out = cv2.bitwise_and(self.skin.copy(), mask2)
        xp = []
        yp = []
        for each in [p1, p2, p4, p3]:
            xp.append(each[0])
            yp.append(each[1])
        out1 = self.skin.copy()[min(yp):max(yp), min(xp):max(xp), :]
        cv2.imwrite("{0}_roi_5_out.jpg".format(ImgSavePath), out1)
        return out1

    def roi_small_thenar(self):
        x = 0
        y = 0
        for each in self.points:
            if each[0] == self.x[4]:
                x = each[0]
            if each[0] == self.x[1]:
                y = each[1]

        # center_y = ((self.main_point[1][1] - self.main_point[0][1]) / 2 + self.main_point[0][1])
        p1 = (x, y)
        p2 = (self.main_point[1][0], y)

        p3 = self.main_point[1]
        y = self.main_point[1][1]
        center_x = ((self.main_point[1][0] - self.main_point[0][0]) / 2 + self.main_point[0][0])
        p4 = (center_x, y)
        p = np.array([p1, p2, p3, p4], np.int32)
        scp = self.contourSkin.copy()
        cv2.polylines(scp, [p], True, (0, 255, 255), 3)
        cv2.imwrite("{0}_roi_small_thenar.jpg".format(ImgSavePath), scp)
        # mask = np.zeros(self.skin.copy().shape, dtype=np.uint8)
        # mask2 = cv2.fillPoly(mask, [p], (255, 255, 255))
        # out = cv2.bitwise_and(self.skin.copy(), mask2)
        xp = []
        yp = []
        for each in [p1, p2, p4, p3]:
            xp.append(int(each[0]))
            yp.append(int(each[1]))
        out1 = self.skin.copy()[min(yp):max(yp), min(xp):max(xp), :]
        cv2.imwrite("{0}_roi_small_thenar_out.jpg".format(ImgSavePath), out1)
        return out1

    def roi_7(self):
        y_min = 0
        y_max = 0
        for each in self.points:
            if each[0] == self.x[1]:
                y_max = each[1]
            if each[0] == self.x[6]:
                y_min = each[1]
        top_left = (self.x[5], y_min)
        bottom_right = (self.x[6], y_max)
        scp = self.contourSkin.copy()
        cv2.rectangle(scp, top_left, bottom_right, (255, 255, 0), 3)
        cv2.imwrite("{0}_roi_7.jpg".format(ImgSavePath), scp)
        out = self.skin.copy()[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0], :]
        cv2.imwrite("{0}_roi_7_out.jpg".format(ImgSavePath), out)
        self.main_point = [top_left, bottom_right]
        return out

    def roi9(self):
        pass

    def roi10(self):
        pass

    def roi_10(self):
        x_min = self.points[2][0]
        y_min = self.points[2][1]

# if __name__ == '__main__':
#     userName = "cqh_test"
#     c = Contour(userName)
#     ct, skin, contour, contourSkin = c.drawContour()
#     r = ROI(contour, skin, contourSkin)
#     r.roi(ct, userName)
#     r.roi_main(ct)
#     r.roi_thenar()
#     r.roi_small_thenar()
#     r.roi_5()
#     r.roi_7()
