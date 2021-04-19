import cv2
import numpy as np
from settings.setting import API_IMG_PATH

class Contour(object):
    def __init__(self, ImageName):
        self.ImageName = ImageName
        self.ImagePath = "{}/{}.jpg".format(API_IMG_PATH,ImageName)
        self.img = cv2.imread(self.ImagePath)

    # 某些论文中提及的简单方式提取，也可使用别的优化
    def cutSkin(self):
        lower = np.array([0, 133, 77], np.uint8)
        upper = np.array([255, 173, 127], np.uint8)

        ycrcb = cv2.cvtColor(self.img, cv2.COLOR_BGR2YCR_CB)
        mask = cv2.inRange(ycrcb, lower, upper)
        kernel = np.ones((57, 57), np.uint8)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        skin = cv2.bitwise_and(self.img, self.img, mask=opening)
        cv2.imwrite("{}/{}_skin.jpg".format(API_IMG_PATH,self.ImageName), skin)
        return skin, opening

    def drawContour(self):
        skin, opening = self.cutSkin()
        skinc = skin.copy()
        _, black_and_white = cv2.threshold(opening, 127, 255, 0)
        contours, _ = cv2.findContours(black_and_white, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        length = len(contours)
        maxArea = -1
        final_Contour = np.zeros(self.img.shape, np.uint8)
        if length > 0:
            ci = 0
            for i in range(length):
                temp = contours[i]
                area = cv2.contourArea(temp)
                if area > maxArea:
                    maxArea = area
                    ci = i
            largest_contour = contours[ci]
            contour = cv2.drawContours(final_Contour, [largest_contour], 0, (0, 255, 0), 3)
            cv2.imwrite("{}/{}_contour.jpg".format(API_IMG_PATH,self.ImageName), final_Contour)
            contourSkin = cv2.drawContours(skin, [largest_contour], 0, (0, 255, 0), 3)
            cv2.imwrite("{}/{}_contour_skin.jpg".format(API_IMG_PATH,self.ImageName), skin)
            return largest_contour, skinc, contour, contourSkin


if __name__ == '__main__':
    c = Contour("cqh_test")
    c.drawContour()
