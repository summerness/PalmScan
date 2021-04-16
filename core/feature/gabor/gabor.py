import numpy as np
import cv2
import math
from core.tools import showImage
_sigma_conv = (3.0/2.0)/((6*math.log(10))**0.5)
def _gabor_sigma(ridge_period):
    return _sigma_conv * ridge_period

def _gabor_size(ridge_period):
    p = int(round(ridge_period * 2 + 1))
    if p % 2 == 0:
        p += 1
    return (p, p)

def gabor_kernel(period, orientation):
    f = cv2.getGaborKernel(_gabor_size(period), _gabor_sigma(period), np.pi/2 - orientation, period, gamma = 1, psi = 0)
    f /= f.sum()
    f -= f.mean()
    return f


def Gabor(directs):
    ridge_period = 7
    directsP = []
    for each in directs:
        directsP.append(np.pi/each)
    gabor_bank = []
    for each in directsP:
        gabor_bank.append(gabor_kernel(ridge_period,each))
    return gabor_bank


if __name__ == '__main__':
    gabor_banks = Gabor([1, 2, 3, 4])
    showImage(gabor_banks[2])