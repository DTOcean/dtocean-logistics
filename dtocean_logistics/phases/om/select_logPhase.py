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

import logging

module_logger = logging.getLogger(__name__)


def logPhase_select(OM_outputs):
    
    # obtain first maintenance id of the OM_outputs dataframe
    df_index = OM_outputs.index.values
    om_id = OM_outputs['ID [-]'].ix[df_index[0]]
    
    # check if only one id type is being called
    if not all(OM_outputs['ID [-]'] == om_id):
        
        msg = ("OM maintenance id - more than one id type supplied.")
        raise ValueError(msg)
        
    if om_id == 'Insp1' or om_id == 'MoS1' or om_id == 'Insp2' or om_id == 'MoS2':
        log_phase_id = 'LpM1'
    
    elif om_id == 'Insp3' or om_id == 'MoS3':
          log_phase_id = 'LpM2'
    
    elif om_id == 'Insp4' or om_id == 'Insp5' or om_id == 'MoS4':
          log_phase_id = 'LpM3'
    
    elif om_id == 'MoS5' or om_id == 'MoS6':
          log_phase_id = 'LpM4'
    
    elif om_id == 'MoS7' or om_id == 'MoS8':
          log_phase_id = 'LpM5'
    
    elif om_id == 'RtP1' or om_id == 'RtP2':
          log_phase_id = 'LpM6'
    
    elif om_id == 'RtP3' or om_id == 'RtP4':
          log_phase_id = 'LpM7'
    
    elif om_id == 'RtP5' or om_id == 'RtP6':
          log_phase_id = 'LpM8'
    
    else:
        
        allowed_phases = ['Insp1','Insp2','Insp3','Insp4',
                          'MoS1', 'MoS2', 'MoS3', 'MoS4', 'MoS5', 'MoS6',
                          'MoS7', 'MoS8',
                          'RtP1', 'RtP2', 'RtP3', 'RtP4', 'RtP5', 'RtP6']
        allowed_phases_str = ", ".join(allowed_phases)
        
        msg = ("OM maintenance id {} not supported. Allowed ids are: "
               "{}.".format(om_id, allowed_phases_str))
        raise ValueError(msg)
    
    return log_phase_id
