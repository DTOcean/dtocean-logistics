# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 10:09:15 2016

@author: BTeillant
"""


def indices(a, func):
    """
    indices returns the indices of a vector "a" that satisfy the
    conditional function "func"
    """

    return [i for (i, val) in enumerate(a) if func(val)]
