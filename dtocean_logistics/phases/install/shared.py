# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 16:35:02 2017

@author: mtopper
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
