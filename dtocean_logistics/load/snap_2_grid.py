# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 15:45:22 2016

@author: acollin
"""

from scipy import spatial
import numpy as np
import pandas as pd
import os
import time

def snap_to_grid(grid_points, point):
    
    '''Snap a point to the grid.
    
    Args:
        grid_points (DataFrame) [-]: DataFrame of site data.
        point (tuple) [m]: Point to be found.
    
    Attributes:
        grid (np.array) [m]: Filtered grid_points including only x and y
            coords.
        new_coords (list) [m]: x and y coords of closest grid point to values 
            defined by point.
        z (list) [m]: Add z value to each point.
        
    Returns:
        tuple () [m]: Tuple of new_coords.

    '''

    grid = np.array(grid_points[['x coord [m]','y coord [m]']])

    new_coords = grid[spatial.cKDTree(grid).query(np.array(point))[1]].tolist()

    new_coords = [float(i) for i in new_coords]
    
    return tuple(new_coords)

