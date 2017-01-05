from check_param import check_float_positive
from check_param import check_float_positive_null
from check_param import check_unicode
from check_param import check_integer
from check_param import check_float_integer
from check_param import check_integer_long

def check_hydro(Input_DB, Input_module, warning_list):

    ERROR_IN_MODULE = False # default value:

    for ind_elem, row in Input_DB.iterrows():
        input_param = 'x coord [m]'
        ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'y coord [m]'
        ERROR_IN_PARAM, warning_list = check_integer_long(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True

        input_param = 'zone [-]'
        ERROR_IN_PARAM, warning_list = check_unicode(Input_DB, ind_elem, input_param, Input_module, warning_list)
        if ERROR_IN_PARAM:
            ERROR_IN_MODULE = True



    return ERROR_IN_MODULE, warning_list