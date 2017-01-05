import numpy as np
import pandas as pd

from check_param import check_float_positive_null
from check_param import check_float_positive_null
from check_param import check_unicode
from check_param import check_integer_long

def check_collect(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'type [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'surface piercing' or PARAM == 'seabed'):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "surface piercing" or "seabed" accepted.')
            ERROR_IN_MODULE = True

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

        # input_param = 'upstream ei type [-]'
        # ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
        # if ERROR_IN_PARAM:
        #     ERROR_IN_MODULE = True
        #
        # input_param = 'upstream ei id [-]'
        # ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
        # if ERROR_IN_PARAM:
        #     ERROR_IN_MODULE = True
        #
        # input_param = 'downstream ei type [-]'
        # ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
        # if ERROR_IN_PARAM:
        #     ERROR_IN_MODULE = True
        #
        # input_param = 'downstream ei id [-]'
        # ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
        # if ERROR_IN_PARAM:
        #     ERROR_IN_MODULE = True

        input_param = 'nr pigtails [-]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'pigtails length [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'pigtails diameter [mm]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'pigtails cable dry mass [kg/m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'pigtails total dry mass [kg]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list


def check_dynamic_cable(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'upstream termination type [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'device' or PARAM == 'collection point'):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "device" or "collection point" accepted.')
            ERROR_IN_MODULE = True

        input_param = 'upstream ei type [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'wet-mate' or PARAM == 'dry-mate' or PARAM == 'j-tube' or PARAM == 'hard-wired'):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "wet-mate" or "dry-mate" or "j-tube" or "hard-wired" accepted.')
            ERROR_IN_MODULE = True

        input_param = 'downstream termination type [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'device' or PARAM == 'static cable' or PARAM == 'collection point'):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "static cable" or "collection point" accepted.')
            ERROR_IN_MODULE = True

        input_param = 'downstream ei type [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'wet-mate' or PARAM == 'dry-mate' or PARAM == 'j-tube' or PARAM == 'splice'):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "wet-mate" or "dry-mate" or "j-tube" or "splice" accepted.')
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list



def check_static_cable(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'type [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'export' or PARAM == 'array'):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "export" or "array" accepted.')
            ERROR_IN_MODULE = True

        input_param = 'upstream termination type [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'device' or PARAM == 'collection point'):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "device" or "collection point" accepted.')
            ERROR_IN_MODULE = True

        input_param = 'upstream ei type [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'wet-mate' or PARAM == 'dry-mate' or PARAM == 'j-tube' or PARAM == 'hard-wired'):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "wet-mate" or "dry-mate" or "j-tube" or "hard-wired" accepted.')
            ERROR_IN_MODULE = True

        input_param = 'downstream termination type [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'device' or PARAM == 'static cable' or PARAM == 'collection point' or pd.isnull(PARAM)):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "device" or "static cable" or "collection point" accepted.')
            ERROR_IN_MODULE = True

        input_param = 'downstream ei type [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'wet-mate' or PARAM == 'dry-mate' or PARAM == 'j-tube' or PARAM == 'splice' or pd.isnull(PARAM)):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "wet-mate" or "dry-mate" or "j-tube" or "splice" accepted.')
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list



def check_cable_route(Input_DB, Input_module, warning_list):

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

        input_param = 'burial depth [m]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'split pipe [-]'
        ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

    return ERROR_IN_MODULE, warning_list




def check_connectors(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

#        input_param = 'type [-]'
#        PARAM = Input_DB[input_param][ind_elem]
#        if not (PARAM == 'wet-mate' or PARAM == 'dry-mate' or PARAM == 'splice'):
#            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
#                                 + 'Only "wet-mate" or "dry-mate" or "splice" accepted.')
#            ERROR_IN_MODULE = True

#        input_param = 'length [m]'
#        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
#        if ERROR_IN_PARAM:
#            ERROR_IN_MODULE = True

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

        input_param = 'mating force [N]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'demating force [N]'
        ERROR_IN_PARAM, warning_list = check_float_positive_null(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

    return ERROR_IN_MODULE, warning_list



def check_external_protection(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'protection type [-]'
        PARAM = Input_DB[input_param][ind_elem]
        if not (PARAM == 'concrete matress' or PARAM == 'rock filter bag'):
            warning_list.append( 'Input: ' + input_param + ' = ' + str(PARAM) + ' in ' + Input_module + '/index:' + str(ind_elem) + ' is Wrong! '
                                 + 'Only "concrete matress" or "rock filter bag" accepted.')
            ERROR_IN_MODULE = True

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


    return ERROR_IN_MODULE, warning_list



def check_layout(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():

        input_param = 'Electrical Layout [-]'
        ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True


    return ERROR_IN_MODULE, warning_list