#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 11:10:49 2021

@author: boutin
"""
import numpy as np


def fuquant(x, n):
    """
    quantificateur uniforme sur n bits
    saturation  +-1
    entrée: vecteur de reels
    sortie: vecteur d'entiers positifs"""

    if n > 0:
        pown = 2 ** (n - 1)
        xq = pown * (x < 0) + np.floor(pown * np.min([np.abs(x), 1 - 1e-10]))
    else:
        # xq = []
        xq = 0

    return xq
