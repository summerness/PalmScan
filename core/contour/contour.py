import cv2
import numpy as np



class Contour(object):
    def __init__(self,UserName):
        self.ImagePath = "../../image/{}.jpg".format(UserName)
        self.UserName = self.ImagePath.replace(".jpg","").replace(".jpeg","").replace(".png","")
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
        cv2.imwrite("{0}_skin.jpg".format(self.UserName), skin)
        return skin, opening

    def drawContour(self):
        skin,opening = self.cutSkin()
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
            contour = cv2.drawContours(final_Contour, [largest_contour], 0, (0, 255, 0), 10)
            cv2.imwrite("{0}_contour.jpg".format(self.UserName), final_Contour)
            contourSkin = cv2.drawContours(skin, [largest_contour], 0, (0, 255, 0), 10)
            cv2.imwrite("{0}_contour_skin.jpg".format(self.UserName), skin)
            return largest_contour, skin,contour,contourSkin



if __name__ == '__main__':
    c = Contour("cqh_test")
    c.drawContour()
