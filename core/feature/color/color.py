import numpy as np
import cv2
from core.tools import showImage
class ColorFeature(object):

    def __init__(self, mainP, imageName):
        self.mainP = mainP
        self.ImageName = imageName

    def GetColor(self):
        # B, G, R = cv2.split(self.mainP)
        # b = B.ravel()[np.flatnonzero(B)]
        # g = G.ravel()[np.flatnonzero(G)]
        # r = R.ravel()[np.flatnonzero(R)]
        # b_max = max(b)
        # b_min = min(b)
        # r_max = max(r)
        # r_min = min(r)
        # g_max = max(g)
        # g_min = min(g)
        # average_b = sum(b) / len(b) / (b_max-b_min)
        # average_r = sum(r) / len(r) / (r_max-r_min)
        # average_g = sum(g) / len(g) / (g_max - g_min)
        # print(average_b,average_g,average_r)
        hsv = cv2.cvtColor(self.mainP, cv2.COLOR_RGB2HSV)
        gray = cv2.cvtColor(self.mainP, cv2.COLOR_BGR2GRAY)
        H, S, V = cv2.split(hsv)
        h = H.ravel()[np.flatnonzero(H)]
        s = S.ravel()[np.flatnonzero(S)]
        g = gray.ravel()[np.flatnonzero(gray)]
        s_max = max(s)
        s_min = min(s)
        h_max = max(h)
        h_min = min(h)
        g_max = max(g)
        g_min = min(g)
        average_h = sum(h) / len(h) /(h_max-h_min)
        average_s = sum(s) / len(s) /(s_max-s_min)
        average_g = sum(g) / len(g) / (g_max - g_min)
        if average_h < 0.2:
            average_h = average_h+0.2
        if average_h > 0.8:
            average_h = average_h - 0.6

        self.color = (average_h,average_s,average_g)

    def toVote(self,r,v,z):
        i = 1
        for each in v:
            f = i * z
            k = each[0]
            count = r.get(k)
            if count == None:
                r[k] = f
            else:
                r[k] = r.get(k) + f
            i += 1

        return r


    def getVote(self):
        fcmM ={
            1:[0.6556,0.9756,0.3997],
            2:[0.5865,0.5449,0.6891],
            3:[0.6169,0.6955,0.4473],
            4:[0.3629,0.3245,0.4633],
            5:[0.4766,0.5323,0.4657],
            6:[0.0667,0.1263,0.5668],
            7:[0.6544,0.8310,0.4011],
        }
        hm = {}
        sm = {}
        gm = {}
        for k, each in fcmM.items():
            hm[k] = abs(self.color[0] - each[0])
            sm[k] = abs(self.color[1] - each[1])
            gm[k] = abs(self.color[2] - each[2])
        hs = sorted(hm.items(), key=lambda item: item[1])
        ss = sorted(sm.items(), key=lambda item: item[1])
        ms = sorted(gm.items(), key=lambda item: item[1])









if __name__ == '__main__':
    userName = "cqh_test"
    ImagePath = "../../../image/{}".format(userName + "_roi_main_out.jpg")
    img = cv2.imread(ImagePath)
    t = ColorFeature(img, userName)
    t.GetColor()
    t.vote()
