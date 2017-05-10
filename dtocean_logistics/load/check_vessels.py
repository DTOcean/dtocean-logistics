from check_param import check_float_positive
from check_param import check_float_positive_null
from check_param import check_unicode
from check_param import check_integer
import numpy as np
import pandas as pd

def check_vess(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():
        input_param = 'Gross tonnage [ton]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Length [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True          

        input_param = 'Beam [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True          

        input_param = 'Consumption [l/h]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Consumption [l/h]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Deck space [m^2]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Deck loading [t/m^2]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Max. cargo [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Bollard pull [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Transit speed [m/s]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'Max. Speed [m/s]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Crew size [-]'
#        ERROR_IN_PARAM, warning_list = check_integer(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'External  personnel [-]'
        ERROR_IN_PARAM, warning_list = check_integer(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'OLC: Transit maxHs [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'OLC: Transit maxTp [s]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'OLC: Transit maxCs [m/s]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'OLC: Transit maxWs [m/s]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'OLC: Towing maxHs [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'OLC: Towing maxTp [s]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'OLC: Towing maxCs [knots]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'OLC: Towing maxWs [m/s]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'OLC: Jacking maxHs [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'OLC: Jacking maxTp [s]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'OLC: Jacking maxCs [m/s]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'OLC: Jacking maxWs [m/s]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Crane capacity [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'Crane radius [m]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'Turntable number [-]'
        ERROR_IN_PARAM, warning_list = check_integer(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Turntable loading [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'Turntable outer diameter [m]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'Turntable inner diameter [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'Turntable height [m]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'Cable splice [yes/no]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'yes' or PARAM == 'no' or pd.isnull(PARAM)):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong!'
                                 + 'Only "yes" or "no" accepted.')
            ERROR_IN_MODULE = True

#        input_param = 'Ground out capabilities [yes/no]'
#        PARAM = Input_DB[input_param][ind_elem]
#        if not (PARAM == 'yes' or PARAM == 'no' or pd.isnull(PARAM)):
#            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong!'
#                                 + 'Only "yes" or "no" accepted.')
#            ERROR_IN_MODULE = True

        input_param = 'DP [-]'
        ERROR_IN_PARAM, warning_list = check_integer(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'Rock storage capacity [t]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Max dumping depth [m]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Max dumping capacity [t/h]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Fall pipe diameter [mm]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Diving moonpool [yes/no]'
#        PARAM = Input_DB[input_param][ind_elem]
#        if not (PARAM == 'yes' or PARAM == 'no' or pd.isnull(PARAM)):
#            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong!'
#                                 + 'Only "yes" or "no" accepted.')
#            ERROR_IN_MODULE = True

#        input_param = 'Diving depth [m]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Diving capacity [-]'
#        ERROR_IN_PARAM, warning_list = check_integer(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'ROV inspection [yes/no]'
#        PARAM = Input_DB[input_param][ind_elem]
#        if not (PARAM == 'yes' or PARAM == 'no' or pd.isnull(PARAM)):
#            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong!'
#                                 + 'Only "yes" or "no" accepted.')
#            ERROR_IN_MODULE = True

#        input_param = 'ROV inspection max depth [m]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'ROV workclass [yes/no]'
#        PARAM = Input_DB[input_param][ind_elem]
#        if not (PARAM == 'yes' or PARAM == 'no' or pd.isnull(PARAM)):
#            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong!'
#                                 + 'Only "yes" or "no" accepted.')
#            ERROR_IN_MODULE = True

#        input_param = 'ROV workclass max depth [m]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'JackUp leg lenght [m]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'JackUp leg diameter [m]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'JackUp max water depth [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'JackUp speed Up [m/min]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'JackUp speed down [m/min]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'JackUp max payload [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'Mooring number  winches [-]'
#        ERROR_IN_PARAM, warning_list = check_integer(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Mooring line pull [t]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Mooring wire lenght [m]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Mooring number anchors [-]'
#        ERROR_IN_PARAM, warning_list = check_integer(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Mooring anchor weight [t]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'AH drum capacity [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'AH wire size [mm]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'AH winch rated pull [t]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

#        input_param = 'AH winch break load [t]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Dredge depth [m]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

#        input_param = 'Dredge type [-]'
#        ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

        input_param = 'Mob time [h]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Mob percentage [%]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Op min Day Rate [EURO/day]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'Op max Day Rate [EURO/day]'
        ERROR_IN_PARAM, warning_list = check_float_positive(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list