# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 10:10:16 2016

@author: BTeillant
"""
import numpy as np


def nan2zero(a):
    """
    nan2zero returns a list of size (x,1) replacing any float('nan') by zero
    """
    return [0 if np.isnan(i) else i for i in a]
