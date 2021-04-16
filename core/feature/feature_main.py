from core.tools import *
import numpy as np

class MainFeature(object):
    def __init__(self,roi_main):
        self.roi_main = roi_main

    def getMainLine(self):
        roi_main_gray = cv2.cvtColor(self.roi_main, cv2.COLOR_BGR2GRAY)
        th2 = cv2.adaptiveThreshold(roi_main_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV, 11, 2)
        kernel = np.ones((2, 2), np.uint8)
        opening = cv2.morphologyEx(th2, cv2.MORPH_OPEN, kernel)
        skeleton = cv2.ximgproc.thinning(opening, thinningType=cv2.ximgproc.THINNING_GUOHALL)
        all_8_neighborhoods = [np.array([int(d) for d in f'{x:08b}'])[::-1] for x in range(256)]
        cn_lut = np.array([self.compute_crossing_number(x) for x in all_8_neighborhoods]).astype(np.uint8)
        skeleton01 = np.where(skeleton != 0, 1, 0).astype(np.uint8)
        cn_filter = np.array([[1, 2, 4],
                              [128, 0, 8],
                              [64, 32, 16]])
        cn_values = cv2.filter2D(skeleton01, -1, cn_filter, borderType=cv2.BORDER_CONSTANT)
        cn = cv2.LUT(cn_values, cn_lut)
        cn[skeleton == 0] = 0
        minutiae = [(x, y) for y, x in zip(*np.where(np.isin(cn, [ 3])))]
        # print(minutiae)
        for x,y in minutiae:
            cv2.drawMarker(self.roi_main, (x, y), (255,0,0), cv2.MARKER_CROSS, 8)
        showImage(self.roi_main)


        # kernel = np.ones((5, 5), np.uint8)
        # opening = cv2.morphologyEx(th2, cv2.MORPH_OPEN, kernel)
        # showImage(opening)
        # minLineLength = 50
        # maxLineGap = 5
        #
        #
        #
        # lines = cv2.HoughLinesP(th2, 1, np.pi / 180, 100, minLineLength, maxLineGap)
        # for each in lines:
        #     for x1, y1, x2, y2 in each:
        #         cv2.line(self.roi_main, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # showImage(self.roi_main)

        # th3 = cv2.adaptiveThreshold(roi_main_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 11, 2)
        # kernel = np.ones((3, 3), np.uint8)
        # showImage(th2)
        # closing = cv2.morphologyEx(th2, cv2.MORPH_CLOSE, kernel)
        # gradient = cv2.morphologyEx(th2, cv2.MORPH_GRADIENT, kernel)
        # showImage(gradient)
        # showImage(closing)
        # showImage(th3)
        # roi_main_blurred = cv2.blur(roi_main_gray, (1, 1))
        # _,thresh1=cv2.threshold(roi_main_blurred,90,255,cv2.THRESH_BINARY)
        # showImage(thresh1)




    def compute_crossing_number(self,values):
        return np.count_nonzero(values < np.roll(values, -1))

    def cross(self):
        pass









if __name__ == '__main__':
    userName = "cqh_test"
    ImagePath = "../../image/{}".format(userName + "_roi_main_out.jpg")
    img = cv2.imread(ImagePath)
    mf = MainFeature(img)
    mf.getMainLine()
    # mf.cross()
