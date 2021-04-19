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
    # showImage(thresh1)
    nccomps  = cv2.connectedComponentsWithStats(thresh1)
    stats = nccomps[2]
    for istat in stats:
        if istat[4] < 100:
            cv2.rectangle(grad_x, tuple(istat[0:2]), tuple(istat[0:2] + istat[2:4]), 0, thickness=-1)  # 26
    showImage(grad_x)
    kernel = np.ones((3, 3), np.uint8)
    cv2.morphologyEx(grad_x,  cv2.MORPH_CLOSE, kernel)
    # showImage(grad_x)
    fix_grad = fix(grad_x)
    getLen(fix_grad)

## 修复线条

def compute_crossing_number(values):
    return np.count_nonzero(values < np.roll(values, -1))

def  fix(img):
    img_line = cv2.ximgproc.thinning(img, thinningType=cv2.ximgproc.THINNING_GUOHALL)
    all_8_neighborhoods = [np.array([int(d) for d in f'{x:08b}'])[::-1] for x in range(256)]
    cn_lut = np.array([compute_crossing_number(x) for x in all_8_neighborhoods]).astype(np.uint8)

    skeleton01 = np.where(img_line != 0, 1, 0).astype(np.uint8)
    cn = cv2.LUT(skeleton01, cn_lut)
    cn[img_line == 0] = 0


    minutiae = [(x, y) for y, x in zip(*np.where(np.isin(cn, [1,3])))]
    print(minutiae)
    for x, y in minutiae:
        cv2.drawMarker(img, (x, y), (255, 0, 0), cv2.MARKER_CROSS, 8)

    showImage(img)
    for each in minutiae:
        for each1 in minutiae:
            if each == each1:
                continue
            dx = each[0] - each1[0]
            dy = each[1] - each1[1]
            distance = dx * dx + dy * dy
            if distance < 10*10 :
                cv2.line(img_line,each,each1,(255,255,0),5)

    showImage(img_line)
    return  img_line



def PreImage(img):
    roi_main_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th2 = cv2.adaptiveThreshold(roi_main_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(th2, cv2.MORPH_OPEN, kernel)
    # showImage(opening)
    #
    sobel_demo(opening)



def getLen(img):
    img_line = cv2.ximgproc.thinning(img, thinningType=cv2.ximgproc.THINNING_GUOHALL)
    contours, _ = cv2.findContours(img_line, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    maxLen = -1
    ci_index = 0
    for index, each in enumerate(contours) :
        perimeter = cv2.arcLength(each, True)
        if perimeter > maxLen:
            maxLen = perimeter
            ci_index = index

    userName = "cqh_test"
    ImagePath = "../../../image/{}".format(userName + "_roi_5_out.jpg")
    img1 = cv2.imread(ImagePath)

    contour = cv2.drawContours(img1, [contours[ci_index]], 0, (0, 255, 0), 3)




    showImage(img1)





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