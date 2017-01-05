# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 15:45:22 2016

@author: pvicente
"""

from scipy import spatial
import numpy as np
import pandas as pd
import os
import time


def find_index(site_x, site_y , x,y):

    xi=np.searchsorted(site_x,x)
    yi=np.searchsorted(site_y,y)

    return xi,yi

    grid = np.array(grid_points[['x','y']])

    new_coords = grid[spatial.cKDTree(grid).query(np.array(point))[1]].tolist()

    # and add z coord - I guess that you can add more features here as you need
    z = grid_points[(grid_points.x == new_coords[0]) & 
            (grid_points.y == new_coords[1])]['layer 1 start'].values[0]

    new_coords.append(z)
    new_coords = [float(i) for i in new_coords]
    
    return tuple(new_coords)

