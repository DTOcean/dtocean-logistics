# -*- coding: utf-8 -*-

#    Copyright (C) 2016 Boris Teillant, Paulo Chainho
#    Copyright (C) 2019 Mathew Topper
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
This module governs the definition of the logistic phases. The functions included
are responsible to initialize and characterize the logistic phases both of the
installation and O&M modules. The functions return a class of each logistic phase
characterized in terms of operations sequence and vessel & equipment combination.

BETA VERSION NOTES: In this version, only two logistic phases were characterized,
one related to Moorings and Foundation Installation: Driven Pile, and another
related to Operation and Maintenance: Offshore Inspection.

.. moduleauthor:: Boris Teillant <boris.teillant@wavec.org>
.. moduleauthor:: Paulo Chainho <paulo@wavec.org>
.. moduleauthor:: Mathew Topper <mathew.topper@dataonlygreater.com>
"""

from .LpM1 import initialize_LpM1_phase
from .LpM2 import initialize_LpM2_phase
from .LpM3 import initialize_LpM3_phase
from .LpM4 import initialize_LpM4_phase
from .LpM5 import initialize_LpM5_phase
from .LpM6 import initialize_LpM6_phase
from .LpM7 import initialize_LpM7_phase
from .LpM8 import initialize_LpM8_phase


LOGPHASE_CONFIG_MAP = {'LpM1': initialize_LpM1_phase,
                       'LpM2': initialize_LpM2_phase,
                       'LpM3': initialize_LpM3_phase,
                       'LpM4': initialize_LpM4_phase,
                       'LpM5': initialize_LpM5_phase,
                       'LpM6': initialize_LpM6_phase,
                       'LpM7': initialize_LpM7_phase,
                       'LpM8': initialize_LpM8_phase
                       }


def logPhase_om_init(log_phase_id, log_op, vessels, equipments, om):
    """This function initializes and characterizes all logistic phases associated
    with the installation module. The first step uses LogPhase class to initialize
    each class with a key ID and description, the second step uses the DefPhase
    class to characterize each phase with a set of operation sequences and vessel
    and equipment combinations.
    Explanation of the key ID numbering system implemented:
     1st digit: 1 = Installation;
                9 = O&M
     2nd digit: 0 = Electrical infrastructure;
                1 = Moorings and foundations;
                2 = Wave and Tidal devices;
     3rd digit: component/sub-system type - differ depending on the logistic phase
     4th digit: method (level 1) - differ depending on the logistic phase
     5th digit: sub-method (level 2) - differ depending on the logistic phase
    
    Parameters
    ----------
    log_phase_id: 
        the required log phase
    log_op : dict
     dictionnary containing all classes defining the individual logistic operations
    vessels : DataFrame
     Panda table containing the vessel database
    equipments : DataFrame
     Panda table containing the equipment database
    
    Returns
    -------
    logPhase_om : dict
     dictionnary containing all classes defining the logistic phases for operation and maintenance
    """
    
    # Returns a configured LogPhase class
    log_phase_configurator = LOGPHASE_CONFIG_MAP[log_phase_id]
    log_phase = log_phase_configurator(log_op, vessels, equipments, om)
    
    return log_phase
