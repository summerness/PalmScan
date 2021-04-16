import cv2
import numpy as np
from core.tools import showImage
from core.feature.gabor.gabor import Gabor



def scharr_demo(image):
    scharr_x = cv2.Scharr(image, cv2.CV_64F, 1, 0)
    scharrx = cv2.convertScaleAbs(scharr_x)
    scharr_y = cv2.Scharr(image, cv2.CV_64F, 0, 1)
    scharry = cv2.convertScaleAbs(scharr_y)
    # scharrxy = cv2.addWeighted(scharrx, 0.5, scharry, 0.5, 0)
    cv2.imshow("grad_x", scharrx)  # 将src图片放入该创建的窗口中
    cv2.waitKey(0)
    cv2.imshow("grad_y", scharry)  # 将src图片放入该创建的窗口中
    cv2.waitKey(0)
    # cv2.imshow("gradxy", scharrxy)  # 将src图片放入该创建的窗口中


def sobel_demo(image):
    grad_x = cv2.Sobel(image, cv2.CV_8U, 1, 0, ksize=3)
    gradx = cv2.convertScaleAbs(grad_x)
    # grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    # grady = cv2.convertScaleAbs(grad_y)
    # gradxy = cv2.addWeighted(gradx, 0.5, grady, 0.5, 0)
    cv2.imshow("grad_x", grad_x)  # 将src图片放入该创建的窗口中
    cv2.waitKey(0)

    # cv2.imshow("grad_y", grad_y)  # 将src图片放入该创建的窗口中
    # cv2.waitKey(0)
    # cv2.imshow("gradxy", gradxy)  # 将src图片放入该创建的窗口中
    # cv2.waitKey(0)
    # dst = cv2.bitwise_not(grad_x)
    # blur = cv2.blur(dst, (1, 1))
    _, thresh1 = cv2.threshold(grad_x, 127, 255, cv2.THRESH_BINARY)
    showImage(thresh1)
    nccomps  = cv2.connectedComponentsWithStats(thresh1)
    stats = nccomps[2]
    for istat in stats:
        if istat[4] < 100:
            cv2.rectangle(grad_x, tuple(istat[0:2]), tuple(istat[0:2] + istat[2:4]), 0, thickness=-1)  # 26





    showImage(grad_x)

def PreImage(img):
    roi_main_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th2 = cv2.adaptiveThreshold(roi_main_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    kernel = np.ones((2, 2), np.uint8)
    opening = cv2.morphologyEx(th2, cv2.MORPH_OPEN, kernel)
    showImage(opening)

    sobel_demo(opening)

    # scharr_demo(opening)

    # 提取垂直线  #效果不好
    # vline = cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(opening.shape[0]/16)), (-1, -1))
    # dst = cv2.morphologyEx(opening, cv2.MORPH_OPEN, vline)
    # dst = cv2.bitwise_not(dst)
    # showImage(dst)



    #gabor 可以只用做取交叉点
    # gabor_banks = Gabor([1,2])
    # all_filtered = np.array([cv2.filter2D(opening, cv2.CV_32F, f) for f in gabor_banks])
    # for index,each in enumerate(all_filtered) :
    #     if index == 0:
    #         img1 = each
    #     else:
    #         res = cv2.add(img1, each)
    #         img1 = res
    # showImage(img1)




if __name__ == '__main__':
    userName = "cqh_test"
    ImagePath = "../../../image/{}".format(userName + "_roi_5_out.jpg")
    img = cv2.imread(ImagePath)


    PreImage(img)