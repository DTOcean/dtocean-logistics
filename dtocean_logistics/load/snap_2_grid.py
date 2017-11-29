# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 15:45:22 2016

@author: topper, acollin
"""

from scipy import spatial
import numpy as np


class SnapToGrid(object):
    
    def __init__(self, grid_points):
        
        self._grid = np.array(grid_points[['x coord [m]', 'y coord [m]']])
        self._tree = spatial.cKDTree(self._grid)
        
        return
    
    def __call__(self, point):
        
        closest_idx = self._tree.query(np.array(point))[1]

        new_coords = self._grid[closest_idx].tolist()
        new_coords = [float(i) for i in new_coords]
        
        return tuple(new_coords)
