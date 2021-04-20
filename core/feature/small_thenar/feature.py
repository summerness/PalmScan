from core.tools import *
import numpy as np
from settings.setting import API_IMG_PATH
from core.feature.gabor.gabor import Gabor

class SmallThenarFeature(object):
    def __init__(self,sthenar,imageName):
        self.sthenar = sthenar
        self.ImageName = imageName

    def pre_image(self):
        roi_main_gray = cv2.cvtColor(self.sthenar, cv2.COLOR_BGR2GRAY)
        th2 = cv2.adaptiveThreshold(roi_main_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(th2, cv2.MORPH_CLOSE, kernel)
        # rows, cols= closing.shape
        # M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 25, 1)
        # dst = cv2.warpAffine(closing, M, (rows, rows))
        # grad_x = cv2.Sobel(dst, cv2.CV_8U, 1, 0, ksize=3)
        # gradx = cv2.convertScaleAbs(grad_x)
        nccomps = cv2.connectedComponentsWithStats(closing)
        stats = nccomps[2]
        for istat in stats:
            if istat[4] < 300:
                cv2.rectangle(closing, tuple(istat[0:2]), tuple(istat[0:2] + istat[2:4]), 0, thickness=-1)

        img_line = cv2.ximgproc.thinning(closing, thinningType=cv2.ximgproc.THINNING_GUOHALL)
        contours, _ = cv2.findContours(img_line, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        f_c = []
        mask = np.zeros(img_line.shape, np.uint8)
        for each in contours:
            p1 = (-1,-1)
            p2 = (-1,-1)

            for index,each_c in enumerate(each):
                if index == 0:
                    p1 = each_c[0]
                    p2 = each_c[0]
                    continue
                if each_c[0][1] > p1[1]:
                    p1 = each_c[0]
                if each_c[0][1] < p2[1]:
                    p2 = each_c[0]
            if p1[0] - p2[0] < 0:
                f_c.append(each)
        for each in f_c :
            mask = cv2.drawContours(mask, [each], 0, (255, 255, 255), 2)
        img_line = cv2.ximgproc.thinning(mask, thinningType=cv2.ximgproc.THINNING_GUOHALL)
        contours, _ = cv2.findContours(img_line, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for  each in contours:
            cv2.drawContours(self.sthenar, [each], 0, (111, 255, 0), 3)
        self.pre_image = self.sthenar






if __name__ == '__main__':
    userName = "cqh_test"
    ImagePath = "../../../image/{}".format(userName + "_roi_small_thenar_out.jpg")
    img = cv2.imread(ImagePath)
    t = SmallThenarFeature(img, userName)
    t.pre_image()






