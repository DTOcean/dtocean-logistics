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
e_external.py contains the functions to initiallize the logistic phase: "external protection 
installation". This consists of:
    (1) Defining Vessels and Equipment combinations capable to carry out the logistic activities
    (2) Defining the list of operations required to conduct out the logistic activities

Parameters
----------
vessels (DataFrame): Panda table containing the vessel database

equipments (DataFrame): Panda table containing the equipment database

external protection (DataFrame): Panda table containing the external protection elements database


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
import numpy as np

def init_e_external(log_op, vessels, equipments, external_protection):

    phase ={}
    if len(external_protection)>0:
        # save outputs required inside short named variables
        external_db = external_protection
        
        mattress_db = external_db[external_db['protection type [-]'] == 'concrete matress']
        rockbag_db = external_db[external_db['protection type [-]'] == 'rock filter bag']

        nr_mattress = mattress_db['protection type [-]'].count()
        nr_rockbag = rockbag_db['protection type [-]'].count()

        # initialize logistic phase
        phase = LogPhase(102, "Installation of external cable protection")

        if not mattress_db.empty and rockbag_db.empty:
            equipment = [(1, equipments['rov'], 0), (nr_mattress, equipments['mattress'], 0)]
        if mattress_db.empty and not rockbag_db.empty:
            equipment = [(1, equipments['rov'], 0), (nr_rockbag, equipments['rock filter bags'], 0)]
        if not mattress_db.empty and not rockbag_db.empty:
            equipment = [(1, equipments['rov'], 0), (nr_mattress, equipments['mattress'], 0), (nr_rockbag, equipments['rock filter bags'], 0)]

        # initialize strategy (all strategies will be individually assessed by the
        # performance functions, with the lowest costs on being choosen)
        phase.op_ve[0] = DefPhase(1, 'Installation of external cable protection')

        # define vessel and equipment combinations suited for this strategy
        phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['Crane Vessel'])],
                                            'equipment': equipment}

        phase.op_ve[0].ve_combination[1] = {'vessel': [(1, vessels['Crane Barge']), (1, vessels['Tugboat'])],
                                            'equipment': equipment}

        phase.op_ve[0].ve_combination[2] = {'vessel': [(1, vessels['CSV'])],
                                            'equipment': equipment}

        # define initial mobilization and onshore preparation tasks
        phase.op_ve[0].op_seq_prep = [ log_op["Mob"],
                                       log_op["AssPort"],
                                       log_op["VessPrep_external"] ]

        # loop over the 'index' elements to install
        for index, row in external_db.iterrows():

            # define sea operations
            phase.op_ve[0].op_seq_sea[index] = [ log_op["VesPos"] ]

            # check the collection point type
            if external_db['protection type [-]'].ix[index] == 'concrete matress':

                phase.op_ve[0].op_seq_sea[index].extend([ log_op["Install_mattress"] ])
                phase.op_ve[0].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])

            if external_db['protection type [-]'].ix[index] == 'rock filter bag':

                phase.op_ve[0].op_seq_sea[index].extend([ log_op["Install_rockbag"] ])
                phase.op_ve[0].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])

        # define final demobilization tasks
        phase.op_ve[0].op_seq_demob = [ log_op["Demob"] ]

    return phase