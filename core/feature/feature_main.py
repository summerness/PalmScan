from core.tools import *

class MainFeature(object):
    def __init__(self,roi_main):
        self.roi_main = roi_main

    def getMainLine(self):
        roi_main_gray = cv2.cvtColor(self.roi_main, cv2.COLOR_BGR2GRAY)
        roi_main_blurred = cv2.blur(roi_main_gray, (1, 1))



        _,thresh1=cv2.threshold(roi_main_blurred,90,255,cv2.THRESH_BINARY)
        showImage(thresh1)



if __name__ == '__main__':
    userName = "cqh_test"
    ImagePath = "../../image/{}".format(userName + "_roi_main_out.jpg")
    img = cv2.imread(ImagePath)
    mf = MainFeature(img)
    mf.getMainLine()