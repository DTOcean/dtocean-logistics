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

from .classes import DefPhase, LogPhase


def initialize_LpM2_phase(log_op, vessels, equipments, om):

    # save outputs required inside short named variables


    # initialize logistic phase
    phase = LogPhase(920, "Underwater inspection or on-site maintenance <30m")

    ''' Underwater inspection or on-site maintenance strategy for water depths <30m '''

    # initialize strategy
    phase.op_ve[0] = DefPhase(0, 'Inspection / On-site maintenance')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['Multicat'])],
                                        'equipment': [(1, equipments['divers'], 0)]}

    phase.op_ve[0].ve_combination[1] = {'vessel': [(1, vessels['CTV'])],
                                        'equipment': [(1, equipments['divers'], 0)]}

    phase.op_ve[0].ve_combination[2] = {'vessel': [(1, vessels['CSV'])],
                                        'equipment': [(1, equipments['divers'], 0)]}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                  log_op["VessPrep"]]

    # define sea operations
    for index, row in om.iterrows():

        om_id = om['ID [-]'].ix[index]

        if om_id == 'Insp3' or om_id == 'MoS3':

            phase.op_ve[0].op_seq_sea[index] = [log_op["TranPortSite"],
                                                log_op["VesPos"],

                                                log_op["Access"],
                                                log_op["Maintenance"],

                                                log_op["TranSiteSite"],
                                                log_op["TranSitePort"]]

    # define final demobilization tasks
    phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    return phase
