# -*- coding: utf-8 -*-
"""
Created on Thu May 26 13:16:55 2016

@author: BTeillant
"""


def comp(list1, list2):
    """
    compares the values of two lists and returns true if at least one value is
    found in both lists
    """
    for val in list1:
        if val in list2:
            return True
    return False