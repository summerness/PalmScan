import numpy as np


def compute_crossing_number(values):
    return np.count_nonzero(values < np.roll(values, -1))

if __name__ == '__main__':
    a = [1, 0, 1, 0, 1, 0,1, 0, 1]  #十字

    b = [0, 0, 0, 0, 1, 0,1, 0, 1] #分叉
    c  = [1, 0, 1,0, 1, 0,0, 0, 0]

    print(compute_crossing_number(b))