# -*- coding: utf-8 -*-

#    Copyright (C) 2016 Boris Teillant
#    Copyright (C) 2017-2018 Mathew Topper
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Created on Wed Jan 27 10:10:16 2016

.. moduleauthor:: Boris Teillant <boris.teillant@wavec.org>
.. moduleauthor:: Mathew Topper <mathew.topper@dataonlygreater.com>
"""

import utm
import numpy as np
from geopy.distance import great_circle


def comp(list1, list2):
    """
    Compares the values of two lists and returns true if at least one value is
    found in both lists.
    """
    for val in list1:
        if val in list2:
            return True
    return False


def differences(a):
    """
    Returns a list of size (x,1) containing the difference of the elements x+1 
    and elements x of a list.
    """
    return [j - i for i, j in zip(a[:-1], a[1:])]


def distance(UTM_ini, UTM_fin):
    """
    Returns the calculated distance (in kms) between two points defined in the 
    UTM coordinate system.
    
    Parameters
    ----------
    UTM_ini : list
    initial UTM coordinates in x,y, zone format
    UTM_fin : list
    final UTM coordinates in x,y, zone format

    Returns
    -------
    dist : float
    direct geographical distance in kms between two UTM coordinates
    """
    
    UTM_ini_x = UTM_ini[0]
    UTM_ini_y = UTM_ini[1]
    UTM_ini_zone = UTM_ini[2]

    UTM_fin_x = UTM_fin[0]
    UTM_fin_y = UTM_fin[1]
    UTM_fin_zone = UTM_fin[2]
    
    # To get dd.dd from utm
    [LAT_INI, LONG_INI] = utm.to_latlon(UTM_ini_x,
                                        UTM_ini_y,
                                        int(UTM_ini_zone[0:2]),
                                        str(UTM_ini_zone[3]))
    
    # To get dd.dd from utm
    [LAT_FIN, LONG_FIN] = utm.to_latlon(UTM_fin_x,
                                        UTM_fin_y,
                                        int(UTM_fin_zone[0:2]),
                                        str(UTM_fin_zone[3]))

    point_i = (LAT_INI, LONG_INI)
    point_f = (LAT_FIN, LONG_FIN)
    
    # Gives you a distance (in kms) between two coordinate in dd.dd
    distance = great_circle(point_i, point_f).kilometers

    return distance


def indices(a, func):
    """
    Returns the indices of a vector "a" that satisfy the conditional function
    "func"
    """

    return [i for (i, val) in enumerate(a) if func(val)]


def nan2zero(a):
    """
    Returns a list of size (x,1) replacing any float('nan') by zero
    """
    return [0 if np.isnan(i) else i for i in a]
