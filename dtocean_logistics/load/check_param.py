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

import numbers
import pandas as pd


def check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list):

    ERROR_IN_PARAM = False # default value:
    PARAM = Input_DB[input_param][ind_elem]

    if not (( isinstance(PARAM, float) or isinstance(PARAM, numbers.Integral) ) and PARAM > 0):
        if isinstance(PARAM, unicode):
            warning_list.append('Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! Value must be a positive float.')
            ERROR_IN_PARAM = True
        elif not pd.isnull(PARAM):
            warning_list.append('Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! Value must be a positive float.')
            ERROR_IN_PARAM = True

    return ERROR_IN_PARAM, warning_list



def check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list):

    ERROR_IN_PARAM = False # default value:
    PARAM = Input_DB[input_param][ind_elem]

    if not (( isinstance(PARAM, float) or isinstance(PARAM, numbers.Integral) ) and PARAM >= 0):
        if isinstance(PARAM, unicode):
            warning_list.append('Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! Value must be a float >= 0.')
            ERROR_IN_PARAM = True
        elif not pd.isnull(PARAM):
            warning_list.append('Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! Value must be a float >= 0.')
            ERROR_IN_PARAM = True

    return ERROR_IN_PARAM, warning_list



def check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list):

    ERROR_IN_PARAM = False # default value:
    PARAM = Input_DB[input_param][ind_elem]

    if not isinstance(PARAM, unicode):
        if not pd.isnull(PARAM):
            warning_list.append('Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! A string is expected.')
            ERROR_IN_PARAM = True

    return ERROR_IN_PARAM, warning_list



def check_integer(Input_DB, ind_elem, input_param, Input_module, warning_list):

    ERROR_IN_PARAM = False # default value:
    PARAM = Input_DB[input_param][ind_elem]

    if not (PARAM).is_integer():
        if isinstance(PARAM, unicode):
            warning_list.append('Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! Value must be integer.')
            ERROR_IN_PARAM = True
        elif not pd.isnull(PARAM):
            warning_list.append('Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! Value must be integer.')
            ERROR_IN_PARAM = True

    return ERROR_IN_PARAM, warning_list



def check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list):

    ERROR_IN_PARAM = False # default value:
    PARAM = Input_DB[input_param][ind_elem]

    if not isinstance(PARAM, numbers.Integral):
        if isinstance(PARAM, unicode):
            warning_list.append('Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! Value must be integer.')
            ERROR_IN_PARAM = True
        elif not pd.isnull(PARAM):
            warning_list.append('Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! Value must be integer.')
            ERROR_IN_PARAM = True

    return ERROR_IN_PARAM, warning_list



def check_float_integer(Input_DB, ind_elem, input_param, Input_module, warning_list):

    ERROR_IN_PARAM = False # default value:
    PARAM = Input_DB[input_param][ind_elem]

    if not ( isinstance(PARAM, float) or isinstance(PARAM, numbers.Integral) ):
        if isinstance(PARAM, unicode):
            warning_list.append('Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! Value must be a float or an integer.')
            ERROR_IN_PARAM = True
        elif not pd.isnull(PARAM):
            warning_list.append('Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! Value must be a float or an integer.')
            ERROR_IN_PARAM = True

    return ERROR_IN_PARAM, warning_list