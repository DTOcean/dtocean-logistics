# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 10:22:21 2016

@author: BTeillant
"""

from geopy.distance import great_circle
import utm


def distance(UTM_ini, UTM_fin):
    """
    distance returns the calculated distance (in kms) between two points
    defined in the UTM coordinate system
    """

    UTM_ini_x = UTM_ini[0]
    UTM_ini_y = UTM_ini[1]
    UTM_ini_zone = UTM_ini[2]

    UTM_fin_x = UTM_fin[0]
    UTM_fin_y = UTM_fin[1]
    UTM_fin_zone = UTM_fin[2]

    [LAT_INI, LONG_INI] = utm.to_latlon(UTM_ini_x, UTM_ini_y, int(UTM_ini_zone[0:2]), str(UTM_ini_zone[3]))  # to get dd.dd from utm
    [LAT_FIN, LONG_FIN] = utm.to_latlon(UTM_fin_x, UTM_fin_y, int(UTM_fin_zone[0:2]), str(UTM_fin_zone[3]))  # to get dd.dd from utm

    point_i = (LAT_INI, LONG_INI)
    point_f = (LAT_FIN, LONG_FIN)

    distance = great_circle(point_i, point_f).kilometers # gives you a distance (in kms) between two coordinate in dd.dd

    return distance