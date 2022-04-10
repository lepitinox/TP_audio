"""
#############################
#   MIDTREAD_DEQUANTIZER    #
#############################
Created on Fri Apr  2 11:10:49 2021

@author: boutin
"""
import numpy as np


def fuquant_inv(xq, r):
    if r == 0:
        return 0
    else:
        yq = np.round(xq)
        sign = -2 * (yq // (2 ** (r - 1))) + 1
        q = 2 / (2 ** r - 1)
        x = yq % (2 ** (r - 1))
        return sign * q * x
