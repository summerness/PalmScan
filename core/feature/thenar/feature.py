from core.tools import *
import numpy as np


class ThenarFeature(object):
    def __init__(self,thenar,full_path,file_name):
        self.thenar = thenar
        self.FullPath = full_path
        self.imgName = file_name


    def compute_crossing_number(self,values):
        return np.count_nonzero(values < np.roll(values, -1))

    def pre_image(self):
        roi_main_gray = cv2.cvtColor(self.thenar, cv2.COLOR_BGR2GRAY)
        th2 = cv2.adaptiveThreshold(roi_main_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(th2, cv2.MORPH_CLOSE, kernel)

        nccomps = cv2.connectedComponentsWithStats(closing)
        stats = nccomps[2]
        maxistat = -1
        istatt = []
        for istat in stats:
            if maxistat < istat[4]:
                maxistat = istat[4]
                istatt = istat

            if istat[4] < 200:
                cv2.rectangle(closing, tuple(istat[0:2]), tuple(istat[0:2] + istat[2:4]), 0, thickness=-1)

        skeleton = cv2.ximgproc.thinning(closing, thinningType=cv2.ximgproc.THINNING_GUOHALL)


        self.pre_themar = skeleton


    def draw_cross(self):
        all_8_neighborhoods = [np.array([int(d) for d in f'{x:08b}'])[::-1] for x in range(256)]
        cn_lut = np.array([self.compute_crossing_number(x) for x in all_8_neighborhoods]).astype(np.uint8)
        skeleton01 = np.where(self.pre_themar != 0, 1, 0).astype(np.uint8)
        cn_filter = np.array([[1, 2, 4],
                              [128, 0, 8],
                              [64, 32, 16]])
        cn_values = cv2.filter2D(skeleton01, -1, cn_filter, borderType=cv2.BORDER_CONSTANT)
        cn = cv2.LUT(cn_values, cn_lut)
        cn[self.pre_themar == 0] = 0
        minutiae = [(x, y) for y, x in zip(*np.where(np.isin(cn, [3])))]
        thenar = self.thenar.copy()
        for x, y in minutiae:
            cv2.drawMarker(thenar, (x, y), (0, 255, 0), cv2.MARKER_CROSS, 8)
        cv2.imwrite("{}/{}_thenar_draw.jpg".format(self.FullPath,self.imgName), thenar)
        return len(minutiae)







if __name__ == '__main__':
    userName = "cqh_test"
    ImagePath = "../../../image/{}".format(userName + "_roi_thenar_out.jpg")
    img = cv2.imread(ImagePath)
    t = ThenarFeature(img,userName)
    t.pre_image()
    t.draw_cross()














