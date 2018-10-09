# -*- coding: utf-8 -*-

#    Copyright (C) 2016 Adam Collin
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
Created on Mon Sep 19 15:45:22 2016

.. moduleauthor:: Adam Collin <adam.collin@ieee.org>
.. moduleauthor:: Mathew Topper <mathew.topper@dataonlygreater.com>
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
