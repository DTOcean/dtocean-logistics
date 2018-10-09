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

"""
e_dynamic.py contains the functions to initiallize the logistic phase: "dynamic cable 
installation". This consists of:
    (1) Defining Vessels and Equipment combinations capable to carry out the logistic activities
    (2) Defining the list of operations required to conduct out the logistic activities

Parameters
----------
vessels (DataFrame): Panda table containing the vessel database

equipments (DataFrame): Panda table containing the equipment database

dynamic_cable (DataFrame): Panda table containing the dynamic cables database

collection_point (DataFrame): Panda table containing the collection points database


Returns
-------

phase (class): contains the initialized characteristics of the logistic phase

See also: ...

                       DTOcean project
                    http://www.dtocean.eu

                   WavEC Offshore Renewables
                    http://www.wavec.org/en

.. moduleauthor:: Boris Teillant <boris.teillant@wavec.org>
.. moduleauthor:: Paulo Chainho <paulo@wavec.org>
.. moduleauthor:: Pedro Vicente <pedro.vicente@wavec.org>
"""

from .classes import DefPhase, LogPhase

import logging
module_logger = logging.getLogger(__name__)

def init_e_dynamic_phase(log_op, vessels, equipments, dynamic_cable,
                               collection_point):

    phase = {}
    if len(collection_point)>0:
        # save outputs required inside short named variables
        dynamic_db = dynamic_cable
        dynamic_db = dynamic_db[dynamic_db['upstream ei type [-]'] != 'hard-wired']
        cp_db = collection_point

        # initialize logistic phase
        phase = LogPhase(102, "Installation of dynamic cables")

        ''' Dynamic Cable Installation Strategy for all cable types '''

        # initialize strategy (all strategies will be individually assessed by the
        # performance functions, with the lowest costs on being choosen)
        phase.op_ve[0] = DefPhase(1, 'Installation of all dynamic cables')

        # define vessel and equipment combinations suited for this strategy
        phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['CLV']), (2, vessels['Multicat'])],
                                            'equipment': [(1, equipments['rov'], 0)]}

        phase.op_ve[0].ve_combination[1] = {'vessel': [(1, vessels['CLB']), (1, vessels['Tugboat']), (2, vessels['Multicat'])],
                                            'equipment': [(1, equipments['rov'], 0)]}

        # define initial mobilization and onshore preparation tasks
        phase.op_ve[0].op_seq_prep = [ log_op["Mob"],
                                       log_op["AssPort"],
                                       log_op["LoadCableFactory"] ]

        # iterate over the list of elements to be installed.
        # each element is associated with a customized operation sequence depending on it's characteristics.
        for index, row in dynamic_db.iterrows():

            # define sea operations
            phase.op_ve[0].op_seq_sea[index] = [ log_op["VesPos"] ]

            # condition check to obtain suitable operation sequence for the downstream termination
            if dynamic_db['downstream termination type [-]'].ix[index] == 'device':
                phase.op_ve[0].op_seq_sea[index].extend([ log_op["Lower_Cable_Seabed"] ])

            elif dynamic_db['downstream termination type [-]'].ix[index] == 'static cable':

                if dynamic_db['downstream ei type [-]'].ix[index] == 'wet-mate':
                    phase.op_ve[0].op_seq_sea[index].extend([ log_op["Wet_Connect"] ])

                elif dynamic_db['downstream ei type [-]'].ix[index] == 'dry-mate':
                    phase.op_ve[0].op_seq_sea[index].extend([ log_op["Lift_Cable_Seabed"],
                                                              log_op["Dry_Connect"],
                                                              log_op["Lower_Cable_Seabed"] ])

                elif dynamic_db['downstream ei type [-]'].ix[index] == 'splice':
                    phase.op_ve[0].op_seq_sea[index].extend([ log_op["Lift_Cable_Seabed"],
                                                              log_op["Splice_Connect"],
                                                              log_op["Lower_Cable_Seabed"] ])

            elif dynamic_db['downstream termination type [-]'].ix[index] == 'collection point':

                cp_id = dynamic_db['downstream termination id [-]'].ix[index]

                if cp_db['type [-]'].ix[cp_id] == 'seabed':

                    if dynamic_db['downstream ei type [-]'].ix[index] == 'dry-mate':
                        phase.op_ve[0].op_seq_sea[index].extend([ log_op["Lower_Cable_Seabed"] ])

                    elif dynamic_db['downstream ei type [-]'].ix[index] == 'wet-mate':
                        phase.op_ve[0].op_seq_sea[index].extend([ log_op["Wet_Connect"] ])

                elif cp_db['type [-]'].ix[cp_id] == 'seabed with pigtails':

                    if dynamic_db['downstream ei type [-]'].ix[index] == 'dry-mate':
                        phase.op_ve[0].op_seq_sea[index].extend([ log_op["Lift_Cable_Seabed"],
                                                                  log_op["Dry_Connect"],
                                                                  log_op["Lower_Cable_Seabed"] ])

                    elif dynamic_db['downstream ei type [-]'].ix[index] == 'splice':
                        phase.op_ve[0].op_seq_sea[index].extend([ log_op["Lift_Cable_Seabed"],
                                                                  log_op["Splice_Connect"],
                                                                  log_op["Lower_Cable_Seabed"] ])

                    elif dynamic_db['downstream ei type [-]'].ix[index] == 'wet-mate':
                        phase.op_ve[0].op_seq_sea[index].extend([ log_op["Wet_Connect"] ])

                elif cp_db['type [-]'].ix[cp_id] == 'surface piercing':
                    phase.op_ve[0].op_seq_sea[index].extend([ log_op["Jtube_Connect"] ])

            else:
                
                msg = ("Error in dynamic cable {}: "
                       "Downstream electrical interface type not "
                       "recognized or doesnt match with termination "
                       "type".format(index))

                module_logger.warning(msg)

            # include dynamic cable laying operation between terminations
            phase.op_ve[0].op_seq_sea[index].extend([ log_op["CableLay_Dyn"] ])

            # condition check to obtain suitable operation sequence for the upstream termination
            if dynamic_db['upstream termination type [-]'].ix[index] == 'device':
                phase.op_ve[0].op_seq_sea[index].extend([ log_op["Lower_Cable_Seabed"] ])

            elif dynamic_db['upstream termination type [-]'].ix[index] == 'collection point':

                cp_id = dynamic_db['upstream termination id [-]'].ix[index]

                if cp_db['type [-]'].ix[cp_id] == 'seabed' or \
                   cp_db['type [-]'].ix[cp_id] == 'seabed with pigtails':

                    if dynamic_db['upstream ei type [-]'].ix[index] == 'dry-mate':
                        phase.op_ve[0].op_seq_sea[index].extend([ log_op["Lower_Cable_Seabed"] ])

                    elif dynamic_db['upstream ei type [-]'].ix[index] == 'wet-mate':
                        phase.op_ve[0].op_seq_sea[index].extend([ log_op["Wet_Connect"] ])

                elif cp_db['type [-]'].ix[cp_id] == 'surface piercing':
                    phase.op_ve[0].op_seq_sea[index].extend([ log_op["Jtube_Connect"] ])
            else:
                
                msg = ("Error in dynamic cable {}: "
                       "Upstream electrical interface type not "
                       "recognized or doesnt match with termination "
                       "type".format(index))

                module_logger.warning(msg)

            phase.op_ve[0].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])
        # define final demobilization tasks
        phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    return phase
