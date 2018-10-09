# -*- coding: utf-8 -*-

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

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 16:35:02 2017

.. moduleauthor:: Mathew Topper <mathew.topper@dataonlygreater.com>
"""

import logging

# Start logging
module_logger = logging.getLogger(__name__)


def get_burial_equip(technique):
    
    stratMsg = ("Only simultaneous lay and burial strategy is "
                "supported by the tool. This is typically not "
                "compatible with the {} technique.")
    
    if technique == 'ploughing':
        burial_equip = 'plough'
        
    elif technique == 'jetting':
        burial_equip = 'jetter'
        
    elif technique == 'cutting':
        burial_equip = 'cutter'
        
        msg = stratMsg.format(technique)
        module_logger.info(msg)
        
    elif technique == 'dredging':
        burial_equip = 'dredge'
        
        msg = stratMsg.format(technique)
        module_logger.info(msg)
                       
    elif technique == 'no burial':
        burial_equip = None
        
    elif technique == 'no data':
        burial_equip = 'plough'
        
        msg = ("Not enough data to compute trenching techniques. "
               "A plough is assumed.")

        module_logger.warning(msg)

    else:
    
        msg = ("Export cable trenching technique not valid. "
               "A plough is assumed.")
        module_logger.warning(msg)
        
        burial_equip = 'plough'
        
    return burial_equip
