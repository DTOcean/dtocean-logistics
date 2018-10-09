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
Gravity.py contains the functions to initiallize the logistic phase: "gravity base foundation 
installation". This consists of:
    (1) Defining Vessels and Equipment combinations capable to carry out the logistic activities
    (2) Defining the list of operations required to conduct out the logistic activities

Parameters
----------
vessels (DataFrame): Panda table containing the vessel database

equipments (DataFrame): Panda table containing the equipment database

foundation (DataFrame): Panda table containing the foundations database


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


def init_gravity_phase(log_op, vessels, equipments, foundation):

    phase = {}
    if len(foundation) > 0:
        # save outputs required inside short named variables
        found_db = foundation
        gravity_db = found_db[found_db['type [-]'] == 'gravity foundation']
        gravity_db = gravity_db.append(found_db[found_db['type [-]'] == 'gravity anchor'])
        gravity_db = gravity_db.append(found_db[found_db['type [-]'] == 'shallow foundation'])
        gravity_db = gravity_db.append(found_db[found_db['type [-]'] == 'shallow anchor'])
    
        # initialize logistic phase
        phase = LogPhase(112, "Installation of gravity based foundations")
    
        '''On-deck Transportation Strategy'''
    
        # initialize strategy (all strategies will be individually assessed by the
        # performance functions, with the lowest costs on being choosen)
        phase.op_ve[0] = DefPhase(0, 'Gravity based anchor installation with on deck transportation')
    
        # define vessel and equipment combinations suited for this strategy
        phase.op_ve[0].ve_combination[0] = {'vessel': [ (1, vessels['Crane Vessel']), (1, vessels['Multicat']) ],
                                            'equipment': [ (1, equipments['rov'], 0) ]}
                                            
        phase.op_ve[0].ve_combination[1] = {'vessel': [ (1, vessels['Crane Barge']), (2, vessels['Tugboat']), (1, vessels['Multicat'])],
                                            'equipment': [ (1, equipments['rov'], 0) ]}

        phase.op_ve[0].ve_combination[2] = {'vessel': [ (1, vessels['JUP Vessel']), (1, vessels['Multicat']) ],
                                            'equipment': [ (1, equipments['rov'], 0) ]}
    
        phase.op_ve[0].ve_combination[3] = {'vessel': [ (1, vessels['JUP Barge']), (2, vessels['Tugboat']), (1, vessels['Multicat']) ],
                                            'equipment': [ (1, equipments['rov'], 0) ]}
                                            
        phase.op_ve[0].ve_combination[4] = {'vessel': [ (1, vessels['CSV']), (1, vessels['Multicat']) ],
                                            'equipment': [ (1, equipments['rov'], 0) ]}
    
 
        # define initial mobilization and onshore preparation tasks
        phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                      log_op["AssPort"],
                                      log_op["VessPrep_gravity"]]
    
        # iterate over the list of elements to be installed.
        # each element is associated with a customized operation sequence depending on it's characteristics,
        for index, row in gravity_db.iterrows():
    
            # initialize an empty operation sequence list for the 'index' element
            phase.op_ve[0].op_seq_sea[index] = []
    
            phase.op_ve[0].op_seq_sea[index].extend([ log_op["VesPos"],
                                                      log_op["GBSlow"] ])
    
            if gravity_db['type [-]'].ix[index] == 'gravity anchor' or gravity_db['type [-]'].ix[index] == 'shallow anchor':
                phase.op_ve[0].op_seq_sea[index].extend([ log_op["PreLay"] ])

            # transportation operations
            phase.op_ve[0].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])

        # define final demobilization tasks
        phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    return phase
