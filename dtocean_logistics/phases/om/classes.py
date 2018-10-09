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

class LogPhase(object):

    def __init__(self, id, description):
        self.id = id
        self.description = description
        self.op_ve = {}
        self.strategy = {}

#        self.feasibility = feasiblity
#        self.matching = matching
#        self.v&e&p_selected = {}
#        self.schedule = {}
#        self.time = {}
#        self.cost = {}
#        self.environmental = environment
#        self.risk = risk


class DefPhase(object):

    def __init__(self, id, description):
        self.id = id
        self.description = description
        self.op_seq_prep = []  # includes all individual logistic operations
        self.op_seq_sea = {}
        self.op_seq_demob = []
        self.ve_combination = {}
        self.sol = {}
        self.sol_cost = {}


class VE_solutions(object):

    def __init__(self, id):
        self.id = id
        self.sol_combi = {}
        self.sol_ves = {}
        self.sol_eq = {}
        self.schedule = {}
        self.cost = {}
