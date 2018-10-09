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

from check_param import check_float_positive
from check_param import check_float_positive_null
from check_param import check_unicode


def check_found(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():
        input_param = 'x coord [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'y coord [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'zone [-]'
        ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'length [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'width [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'height [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'installation depth [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'dry mass [kg]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'grout volume [m3]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'type [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'pile foundation' or  PARAM == 'pile anchor' or  PARAM == 'gravity foundation' or  PARAM == 'gravity anchor' \
                        or  PARAM == 'shallow foundation' or  PARAM == 'shallow anchor' or  PARAM == 'direct-embedment anchor'\
                        or  PARAM == 'drag-embedment anchor' or PARAM == 'suction caisson anchor'):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "pile foundation", "pile anchor", "gravity foundation", "gravity anchor", "shallow foundation", "shallow anchor", "direct-embedment anchor", "drag-embedment anchor" or "suction caisson anchor" accepted.')
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list


def check_ln(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():
        input_param = 'length [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'dry mass [kg]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list


