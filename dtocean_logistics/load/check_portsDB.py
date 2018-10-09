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

import pandas as pd

from check_param import check_float_positive
from check_param import check_float_positive_null
from check_param import check_unicode


def check_ports(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'UTM x [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'UTM y [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'UTM zone [-]'
        ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Type of terminal [Quay/Dry-dock]'
        ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Entrance width [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Terminal length [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Terminal load bearing [t/m^2]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Terminal draught [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Terminal area [m^2]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Max gantry crane lift capacity [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Max tower crane lift capacity [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Jacking capability [yes/no]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'Yes' or PARAM == 'No' or pd.isnull(PARAM)):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong!'
                                 + 'Only "Yes" or "No" accepted.')
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list