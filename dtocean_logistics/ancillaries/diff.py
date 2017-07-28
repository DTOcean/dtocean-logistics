# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 10:10:16 2016

@author: BTeillant
"""

def differences(a):
    """
    differences returns a list of size (x,1) containing the difference of the 
    elements x+1 and elements x of a list "" 
    """
    return [j - i for i, j in zip(a[:-1], a[1:])]
