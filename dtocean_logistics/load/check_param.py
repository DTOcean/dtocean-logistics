import numbers
import numpy as np
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