#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 18:43:32 2021
@author: boutin
"""
from typing import Union

import numpy as np


def quantif(x: Union[list, np.array], a, n):  # (input sig, full-scall value, Number of bites)
    x = np.float64(x)
    high = a
    low = -1 * a
    q = (high - low) / (2 ** n)
    Q = np.max(np.array(
        [np.min(np.array([np.floor((x - low) / q), np.ones_like(x) * (2 ** n - 1)]), axis=0), np.zeros_like(x)]),
        axis=0)
    low = low + q / 2
    Y = low + q * Q
    return Y, q, Q  # (quantization output, quant step, quantizd value (between 0 and 2^log2(N)-1))

#%%
