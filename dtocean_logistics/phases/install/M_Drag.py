# -*- coding: utf-8 -*-

#    Copyright (C) 2016 Boris Teillant, Paulo Chainho, Pedro Vicente
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

from .classes import DefPhase, LogPhase


def init_m_drag_phase(log_op, vessels, equipments, foundation):

    phase = {}
    if len(foundation) > 0:
        # save outputs required inside short named variables
        found_db = foundation
        drag_db = found_db[found_db['type [-]'] == 'drag-embedment anchor']
    
        # initialize logistic phase
        phase = LogPhase(113, "Installation of mooring systems with drag-embedment anchors")
    
        ''' Deploy drag-embedment anchor installation strategy'''
    
        # initialize strategy
        phase.op_ve[0] = DefPhase(0, 'Deploy drag-embedment anchor')
    
        # define vessel and equipment combinations suited for this strategy
        phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['AHTS'])],
                                            'equipment': [(1, equipments['rov'], 0)]}
    
        phase.op_ve[0].ve_combination[1] = {'vessel': [(1, vessels['Multicat'])],
                                            'equipment': [(1, equipments['rov'], 0)]}
    
        # define initial mobilization and onshore preparation tasks
        phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                      log_op["AssPort"],
                                      log_op["VessPrep_drag"]]
    
        # iterate over the list of elements to be installed.
        # each element is associated with a customized operation sequence depending on it's characteristics
        for index, row in drag_db.iterrows():
    
            # initialize an empty operation sequence list for the 'index' element
            phase.op_ve[0].op_seq_sea[index] = []
    
            phase.op_ve[0].op_seq_sea[index].extend([ log_op["SeafloorEquipPrep"],
                                                      log_op["DragEmbed"],
                                                      log_op["PreLay"] ])

            # transportation operations
            phase.op_ve[0].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])

        # define final demobilization tasks
        phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    return phase
