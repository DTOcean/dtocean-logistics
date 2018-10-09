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

from check_param import check_float_positive_null
from check_param import check_unicode
from check_param import check_integer_long


def check_site(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'x coord [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'y coord [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'zone [-]'
        ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'bathymetry [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'soil type [-]'
        ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list



def check_metocean(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'year [-]'
        ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'month [-]'
        ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'day [-]'
        ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'hour [-]'
        ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Hs [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Tp [s]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Ws [m/s]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Cs [m/s]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list



def check_device(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'type [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'fixed TEC' or PARAM == 'float TEC' or PARAM == 'float WEC' or PARAM == 'fixed WEC'):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "fixed TEC" or "float TEC" or "float WEC" or "fixed WEC" accepted.')
            ERROR_IN_MODULE = True

        input_param = 'length [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'width [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'height [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'dry mass [kg]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'sub system list [-]'
        ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'assembly strategy [-]'
#        PARAM = Input_DB[input_param][ind_elem]
#        # ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if not (PARAM == '([A,B,C],D)' or PARAM == '([A,B,C,D])'):
#            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
#                                 + 'Only "([A,B,C],D)" or "([A,B,C,D])" accepted.')
#            ERROR_IN_MODULE = True

        input_param = 'assembly duration [h]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'load out [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'skidded' or PARAM == 'trailer' or PARAM == 'float away' or PARAM == 'lift away'):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "skidded" or "trailer" or "float away" or "lift away" accepted.')
            ERROR_IN_MODULE = True

        input_param = 'transportation method [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'deck' or PARAM == 'tow'):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "deck" or "tow" accepted.')
            ERROR_IN_MODULE = True

        input_param = 'bollard pull [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'connect duration [h]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'disconnect duration [h]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'max Hs [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'max Tp [s]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'max wind speed [m/s]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'max current speed [m/s]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Project start date [-]'
        ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list




def check_subdevice(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'length [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'width [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'height [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'dry mass [kg]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'assembly strategy [-]' # 'assembly location [-]' !..
#        PARAM = Input_DB[input_param][ind_elem]
#        if not (PARAM == 'port' or PARAM == 'site'):
#            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
#                                 + 'Only "port" or "site" accepted.')
#            ERROR_IN_MODULE = True

        input_param = 'assembly duration [h]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list


def check_landfall(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'method [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'OCT' or PARAM == 'HDD'):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "OCT" or "HDD" accepted.')
            ERROR_IN_MODULE = True

#        input_param = 'ground-out [yes/no]'
#        PARAM = Input_DB[input_param][ind_elem]
#        if not (PARAM == 'yes' or PARAM == 'no'):
#            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
#                                 + 'Only "yes" or "no" accepted.')
#            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list



def check_entry_point(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'x coord [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'y coord [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'zone [-]'
        ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'bathymetry [m]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'soil type [-]'
#        ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list