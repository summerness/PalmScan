
from core.tools import *
import numpy as np


class Roi5Feature(object):
    def __init__(self,roi5,full_path,file_name):
        self.roi5 = roi5
        self.FullPath = full_path
        self.imgName = file_name

    def compute_crossing_number(self, values):
        return np.count_nonzero(values < np.roll(values, -1))

    def pre_image(self):
        roi_main_gray = cv2.cvtColor(self.roi5, cv2.COLOR_BGR2GRAY)
        th2 = cv2.adaptiveThreshold(roi_main_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(th2, cv2.MORPH_CLOSE, kernel)
        grad_x = cv2.Sobel(closing, cv2.CV_8U, 1, 0, ksize=3)
        gradx = cv2.convertScaleAbs(grad_x)
        nccomps = cv2.connectedComponentsWithStats(gradx)
        stats = nccomps[2]
        for istat in stats:
            if istat[4] < 100:
                cv2.rectangle(grad_x, tuple(istat[0:2]), tuple(istat[0:2] + istat[2:4]), 0, thickness=-1)
        self.pre_image = grad_x

    def fix_line(self):
        img_line = cv2.ximgproc.thinning(self.pre_image, thinningType=cv2.ximgproc.THINNING_GUOHALL)
        all_8_neighborhoods = [np.array([int(d) for d in f'{x:08b}'])[::-1] for x in range(256)]
        cn_lut = np.array([self.compute_crossing_number(x) for x in all_8_neighborhoods]).astype(np.uint8)

        skeleton01 = np.where(img_line != 0, 1, 0).astype(np.uint8)
        cn = cv2.LUT(skeleton01, cn_lut)
        cn[img_line == 0] = 0
        minutiae = [(x, y) for y, x in zip(*np.where(np.isin(cn, [1, 3])))]

        for each in minutiae:
            for each1 in minutiae:
                if each == each1:
                    continue
                dx = each[0] - each1[0]
                dy = each[1] - each1[1]
                distance = dx * dx + dy * dy
                if distance < 10 * 10:
                    cv2.line(img_line, each, each1, (255, 255, 255), 1)
        self.fix_line_img = img_line


    def getLenAndDraw(self):
        contours, _ = cv2.findContours(self.fix_line_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        maxLen = -1
        ci_index = 0
        for index, each in enumerate(contours):
            perimeter = cv2.arcLength(each, True)
            if perimeter > maxLen:
                maxLen = perimeter
                ci_index = index

        if self.roi5.shape[0] *0.6 <= maxLen:
            cv2.drawContours(self.roi5, [contours[ci_index]], 0, (0, 255, 0), 3)
            cv2.imwrite("{}/{}_roi5_draw.jpg".format(self.FullPath, self.imgName), self.roi5)
            return True
        cv2.imwrite("{}/{}_roi5_draw.jpg".format(self.FullPath, self.imgName), self.roi5)
        return False



if __name__ == '__main__':
    userName = "wxf"
    ImagePath = "../../image/{}".format(userName + "_roi_5_out.jpg")
    img = cv2.imread(ImagePath)
    t = Roi5Feature(img,"../image", userName)
    t.pre_image()
    t.fix_line()
    t.getLenAndDraw()