# -*- coding: utf-8 -*-

#    Copyright (C) 2016 Boris Teillant, Paulo Chainho, Pedro Vicente
#    Copyright (C) 2017-2018 Mathew Topper
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

import pandas as pd

from check_param import check_float_positive
from check_param import check_float_positive_null
from check_param import check_integer_long


def check_rov(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'ROV class [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'Inspection class' or PARAM == 'Workclass'):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "Inspection class" or "Workclass" accepted.')
            ERROR_IN_MODULE = True

        input_param = 'Depth rating [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Length [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Width [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Height [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Weight [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Payload [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'AE footprint [m^2]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'AE weight [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'AE supervisor [-]'
        ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'AE technician [-]'
        ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'ROV day rate [EURO/day]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Supervisor rate [EURO/12h]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Technician rate [EURO/12h]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list


def check_divers(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'Max operating depth [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Deployment eq. footprint [m^2]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Deployment eq. weight [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'Nr supervisors [-]'
#        ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Nr divers [-]'
#        ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Nr tenders [-]'
#        ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Nr technicians [-]'
#        ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Nr support technicians [-]'
#        ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Deployment eq. day rate [EURO/day]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Supervisor day rate [EURO/day]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Divers day rate [EURO/day]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Tenders day rate [EURO/day]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Technicians day rate [EURO/day]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Life support day rate [EURO/day]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'Total day rate [EURO/day]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list


def check_cable_burial(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

#        input_param = 'Burial tool type [-]'
#        PARAM = Input_DB[input_param][ind_elem]
#        if not (PARAM == 'Plough' or PARAM == 'ROV' or PARAM == 'Tracked' or pd.isnull(PARAM)):
#            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
#                                 + 'Only "Plough" or "ROV" or "Tracked" accepted.')
#            ERROR_IN_MODULE = True

        input_param = 'Max operating depth [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Tow force required [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Length [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Width [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Height [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Weight [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Jetting capability [yes/no]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'yes' or PARAM == 'no' or pd.isnull(PARAM)):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong!'
                                 + 'Only "yes" or "no" accepted.')
            ERROR_IN_MODULE = True

        input_param = 'Ploughing capability [yes/no]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'yes' or PARAM == 'no' or pd.isnull(PARAM)):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong!'
                                 + 'Only "yes" or "no" accepted.')
            ERROR_IN_MODULE = True

        input_param = 'Cutting capability [yes/no]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'yes' or PARAM == 'no' or pd.isnull(PARAM)):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong!'
                                 + 'Only "yes" or "no" accepted.')
            ERROR_IN_MODULE = True

        input_param = 'Jetting trench depth [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Ploughing trench depth [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Cutting trench depth [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Max cable diameter [mm]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Min cable bending radius [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'AE footprint [m^2]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'AE weight [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Burial tool day rate [EURO/day]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Personnel day rate [EURO/12h]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list


def check_excavating(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'Depth rating [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Width [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Height [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Weight [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'Lenght or diameter [m]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'Excavator day rate [EURO/day]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Personnel day rate [EURO/12h]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list


def check_mattress(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

#        input_param = 'Concrete resistance [N/mm^2]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Concrete density [kg/m^3]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'Unit lenght [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Unit width [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Unit thickness [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Unit weight air [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'Unit weight water [t]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Nr looped ropes [-]'
#        ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Ropes diameter [mm]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'Cost per unit [EURO]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list


def check_rockfilterbags(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'Weight [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        # input_param = 'Particle diameter [mm]'
        # ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        # if ERROR_IN_PARAM:
        #     ERROR_IN_MODULE = True

#        input_param = 'Mesh size [mm]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'Diameter [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Height [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'Volume [m^ 3]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Velocity unit [m/s]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Velocity grouped [m/s]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'Cost per unit [EURO]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list


def check_splitpipes(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

#        input_param = 'Material [-]'
#        ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Unit weight air [kg]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Unit weight water [kg]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'Unit length [mm]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'Unit wall thichness [mm]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Unit inner diameter [mm]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Unit outer diameter [mm]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Max cable size [mm]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Min bending radius [m]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'Cost per unit [EURO]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True



    return ERROR_IN_MODULE, warning_list


def check_hammer(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'Depth rating [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Length [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Weight in air [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Min pile diameter [mm]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Max pile diameter [mm]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'AE footprint [m^2]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'AE weight [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Hammer day rate [EURO/day]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Personnel day rate [EURO/12h]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list


def check_drillingrigs(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'Diameter [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Length [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Weight [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Drilling diameter range [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Max drilling depth [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Max water depth [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'Torque [kNm]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Pull back [t]'
#        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'AE footprint [m^2]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'AE weight [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Drill rig day rate [EURO/day]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Personnel day rate [EURO/day]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True



    return ERROR_IN_MODULE, warning_list


def check_vibrodriver(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'Width [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Length [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Height [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Vibro driver weight [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Clamp weight [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Min pile diameter [mm]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Max pile diameter [mm]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Max pile weight [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'AE footprint [m^2]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'AE weight [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Vibro diver day rate [EURO/day]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Personnel day rate [EURO/day]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True



    return ERROR_IN_MODULE, warning_list
