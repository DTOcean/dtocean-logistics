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


def init_devices_phase(log_op, vessels, equipments, device, layout):

    # save outputs required inside short named variables
    dev_type = device['type [-]'].ix[0]
    assembly_strategy = device['assembly strategy [-]'].ix[0]  # unused!
    trans_methd = device['transportation method [-]'].ix[0]
    loadout_methd = device['load out [-]'].ix[0]
    hydro_db = layout

    # initialize logistic phase
    phase = LogPhase(121, "Installation of devices")

    ''' On-deck Transportation Strategy '''

    # initialize strategy
    phase.op_ve[0] = DefPhase(1, 'On-deck transportation')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[0].ve_combination[0] = {'vessel': [ (1, vessels['Crane Vessel']), (1, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    phase.op_ve[0].ve_combination[1] = {'vessel': [ (1, vessels['JUP Vessel']), (1, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    phase.op_ve[0].ve_combination[2] = {'vessel': [ (1, vessels['CSV']), (2, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    phase.op_ve[0].ve_combination[3] = {'vessel': [ (1, vessels['Fit for Purpose']), (2, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    phase.op_ve[0].ve_combination[4] = {'vessel': [ (1, vessels['Crane Barge']), (1, vessels['Tugboat']), (1, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    phase.op_ve[0].ve_combination[5] = {'vessel': [ (1, vessels['JUP Barge']), (1, vessels['Tugboat']), (1, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                  log_op["DevAssPort"]]
    # check the transportation method
    # (1st branch in the decision making tree)
    if trans_methd == 'deck':
        # check the device loadout strategy
        # (2nd branch in the decision making tree)
        if loadout_methd == 'lift away':
            phase.op_ve[0].op_seq_prep.extend([log_op["LoadOut_Lift"]])

        elif loadout_methd == 'skidded':
            phase.op_ve[0].op_seq_prep.extend([log_op["LoadOut_Skidded"]])

    elif trans_methd == 'tow':
        # check the device loadout strategy
        # (2nd branch in the decision making tree)
        if loadout_methd == 'lift away':
            phase.op_ve[0].op_seq_prep.extend([log_op["LoadOut_Lift"]])

        elif loadout_methd == 'skidded' or dev_type == 'trailer':
            phase.op_ve[0].op_seq_prep.extend([log_op["LoadOut_Skidded"]])

        elif loadout_methd == 'float away':
            phase.op_ve[0].op_seq_prep.extend([log_op["LoadOut_Float"]])


    # iterate over the list of elements to be installed.
    # each element is associated with a customized operation sequence depending on it's characteristics,.
    for index, row in hydro_db.iterrows():

        # transportation operations
        phase.op_ve[0].op_seq_sea[index] = [ log_op["VesPos"] ]

        # device installation operations
        if dev_type == 'float WEC' or dev_type == 'float TEC':

            phase.op_ve[0].op_seq_sea[index].extend([log_op["PosFLTdev"]])

        elif dev_type == 'fixed WEC' or dev_type == 'fixed TEC':

             phase.op_ve[0].op_seq_sea[index].extend([log_op["PosBFdev"]])

        # transportation operations
        phase.op_ve[0].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])

    # define final demobilization tasks
    phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    ''' Tow Transportation Strategy '''

    # initialize strategy
    phase.op_ve[1] = DefPhase(1, 'Towing transportation')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[1].ve_combination[0] = {'vessel': [(1, vessels['AHTS']), (1, vessels['Multicat'])],
                                        'equipment': [(1, equipments['rov'], 0) ]}

    phase.op_ve[1].ve_combination[1] = {'vessel': [(1, vessels['Fit for Purpose']), (1, vessels['Multicat'])],
                                        'equipment': [(1, equipments['rov'], 0) ]}

    phase.op_ve[1].ve_combination[2] = {'vessel': [(1, vessels['Tugboat']), (1, vessels['Multicat'])], # TUGBOAT CANNOT BE CHARACTERIZED AS BOTH INSTALLATION AND SUPPORT VESSEL IN THE FEASIBILITY FUNCTIONS
                                        'equipment': [(1, equipments['rov'], 0) ]}

    # define initial mobilization and onshore tasks
    phase.op_ve[1].op_seq_prep = [log_op["Mob"],
                                  log_op["DevAssPort"]]
    if trans_methd == 'deck':

        if loadout_methd == 'lift away':
            phase.op_ve[1].op_seq_prep.extend([log_op["LoadOut_Lift"]])

        elif loadout_methd == 'skidded':
            phase.op_ve[1].op_seq_prep.extend([log_op["LoadOut_Skidded"]])


    elif trans_methd == 'tow':

        if loadout_methd == 'lift away':
            phase.op_ve[1].op_seq_prep.extend([log_op["LoadOut_Lift"]])

        elif loadout_methd == 'skidded' or dev_type == 'trailer':
            phase.op_ve[1].op_seq_prep.extend([log_op["LoadOut_Skidded"]])

        elif loadout_methd == 'float away':
            phase.op_ve[1].op_seq_prep.extend([log_op["LoadOut_Float"]])

    # iterate over the list of elements to be installed.
    # each element is associated with a customized operation sequence depending on it's characteristics,.
    for index, row in hydro_db.iterrows():

        # transportation operations
        phase.op_ve[1].op_seq_sea[index] = [ log_op["VesPos"] ]

        # device installation operations
        if dev_type == 'float WEC' or dev_type == 'float TEC':
            phase.op_ve[1].op_seq_sea[index].extend([log_op["PosFLTdev"]])

        elif dev_type == 'fixed WEC' or dev_type == 'fixed TEC':
             phase.op_ve[1].op_seq_sea[index].extend([log_op["PosBFdev"]])

        # transportation operations
        phase.op_ve[1].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])
    # define final demobilization tasks
    phase.op_ve[1].op_seq_demob = [ log_op["Demob"] ]

    ''' Selection of suitable strategies '''

    # delete the strategies that are not applicable for the scenario
    # so they're not tested in the performance functions
    if trans_methd == 'tow':
        phase.op_ve[0] = phase.op_ve[1]
        del phase.op_ve[1]

    elif trans_methd == 'deck':
        del phase.op_ve[1]

    return phase
