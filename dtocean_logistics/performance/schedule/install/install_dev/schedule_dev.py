# -*- coding: utf-8 -*-

#    Copyright (C) 2016 Boris Teillant, Paulo Chainho
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
This module is responsible for the interphase relation between the different
logistic phases during installation. The inputs from the user and other DTOcean
packages build up unique projects which require specific installation sequences.
The functions in this module return the installation sequence required based on
some pre-defined cases (type of foundations, type of moorings, type of device,
type of electrical infranstrucutres).

BETA VERSION NOTES: the methodology was defined and implemented, should not
suffer major changes on the next version of the code. However the content (the
installation sequences) will be updated.

.. moduleauthor:: Boris Teillant <boris.teillant@wavec.org>
.. moduleauthor:: Paulo Chainho <paulo@wavec.org>
"""

from .schedule_dev_tow import sched_dev_tow
from .schedule_dev_deck import sched_dev_deck

import logging
module_logger = logging.getLogger(__name__)

def sched_dev(seq, ind_sol, install, log_phase, site, entry_point, device, sub_device,
              layout, sched_sol):
    """sched_dev determines the duration of each individual logistic operations
    for the installtion of ocean energy devices following a common methodology:
        - the time value duration can be extracted from a direct average
        default value
        - the time value duration can result from a specialized function
        - the time value duration can be derived from other sources, mostly by
        making use of values available in the database or provided from the
        end-user
    Parameters
    ----------
    seq: integer
     index of the operation sequencing strategy under consideration
    ind_sol: integer
     index representing the feasible logistic solution under consideration
    log_phase: class
     class containing all data relevant to the characterization of the feasible
     logistic solutions
    user_inputs : dict
     dictionnary containing all required inputs to WP5 coming from WP1/end-user.
    ...

    Returns
    -------
    sched_sol : dict
     ...
    """

    """
    Time assessment for the installation of ocean energy devices
    """
#    """
#    On-deck device transportation
#    """
    if log_phase.op_ve[seq].description == 'On-deck transportation':
        sched_sol = sched_dev_deck(seq, ind_sol, install, log_phase, site, entry_point,
                                   device, sub_device, layout, sched_sol)
#    """
#    Towing device transportation
#    """
    elif log_phase.op_ve[seq].description == 'Towing transportation':
        sched_sol = sched_dev_tow(seq, ind_sol, install, log_phase, site, entry_point,
                                   device, sub_device, layout, sched_sol)          
    else:
        
        msg = ("Unknow device transportation method: {}. Only 'On-deck "
               "transportation' or 'Towing transportation' accepted.".format(
               log_phase.op_ve[seq].description))
        module_logger.warning(msg)

    return sched_sol
