"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org; pedro.vicente@wavec.org

Example.py is an example file of the Installation module within the suite of design tools
developped under the EU FP7 DTOcean project. Example.py provides an estimation of
the predicted performance of feasible maritime infrastructure solutions
that can carry out marine operations pertaining to the installation of
wave and tidal energy arrays.

Example.py can be described in the following sub-modules:
0- Loading the example input data
1- Calling the Installation module

Parameters
----------
vessels(DataFrame): Panda table containing the vessel database

equipments (DataFrame): Panda table containing the equipment database

ports (DataFrame): Panda table containing the ports database

user_inputs (dict): dictionnary containing all required inputs to the Installation module coming from WP1/end-user:
     'device' (Dataframe): inputs required from the device
     'metocean' (Dataframe): metocean data

hydrodynamic_outputs (dict): dictionnary containing all required inputs to the Installation module coming from WP2
     'units' (DataFrame): number of devices
     'position' (DataFrame): UTM position of the devices

electrical_outputs (dict): dictionnary containing all required inputs to the Installation module coming from WP3
     'layout' (DataFrame): to be specified

M&F_outputs (DataFrame): containing foundation data required for each device


Returns
-------

installation (dict): dictionnary compiling all key results obtained from the assessment of the logistic phases for installation:
'inst_log':	List of logistic phase during installation
'port_req':	Dictionary of the port requirements calculated
'port_feas':	Dictionary of ports satisfying the requirements
'port_sol':	Dictionary of the port selected and its distance to site
'planning':	Dictionary containing the layering rules for the planning of the logitic phases during installation
'inst_sol':	Dictionary containing the outcome of the optimal solutions for each logistic phase during installation
'dev_com':    Commissioning time per device
'warning':	Warning message

The 'inst_sol' dictionnary compiles all key results obtained from the assessment of each logistic phase in the installation:
    'plan' (dict): installation sequence of the required logistic phases
    'port' (DataFrame): port data related to the selected installation port
    'requirement' (tuple): minimum requirements returned from the feasibility functions
    'eq_select' (dict): list of equipments satisfying the minimum requirements
    've_select' (dict): list of vessels satisfying the minimum requirements
    'combi_select' (dict): list of solutions passing the compatibility check
    'schedule' (dict): list of parameters with data about time
    'cost'  (dict): vessel equiment and port cost
    'risk': to be defined
    'envir': to be defined
    'status': to be defined

See also: ...

                       DTOcean project
                    http://www.dtocean.eu

                   WavEC Offshore Renewables
                    http://www.wavec.org/en

"""

from os import path
import timeit

from dtocean_logistics.load import load_phase_order_data, load_time_olc_data
from dtocean_logistics.load import load_eq_rates
from dtocean_logistics.load import load_sf
from dtocean_logistics.load import load_vessel_data, load_equipment_data
from dtocean_logistics.load import load_port_data
from dtocean_logistics.load.wp_bom import load_user_inputs, load_hydrodynamic_outputs
from dtocean_logistics.load.wp_bom import load_electrical_outputs, load_MF_outputs

from installation_main import installation_main
from dtocean_logistics.load.input_checkin import input_check

# # Set directory paths for loading inputs (@Tecnalia)
mod_path = path.dirname(path.realpath(__file__))


def database_file(file):
    """
    shortcut function to load files from the database folder
    """
    fpath = path.join('databases', '{0}'.format(file))
    db_path = path.join(mod_path, fpath)
    return db_path

###
### Load required inputs and database into panda dataframes
###

# INPUT options:
#default_values inputs
phase_order = load_phase_order_data(database_file("installation_order_0.xlsx"))
schedule_OLC = load_time_olc_data(database_file("operations_time_OLC.xlsx"))
penet_rates, laying_rates, other_rates = load_eq_rates(database_file("equipment_perf_rates.xlsx"))
port_sf, vessel_sf, eq_sf = load_sf(database_file("safety_factors.xlsx"))
#Internal logistic module databases
vessels = load_vessel_data(database_file("logisticsDB_vessel_python.xlsx"))
equipments = load_equipment_data(database_file("logisticsDB_equipment_python.xlsx"))
ports = load_port_data(database_file("logisticsDB_ports_python.xlsx"))
ports.replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
#upstream module inputs/outputs
site, metocean, device, sub_device, landfall, entry_point = load_user_inputs(database_file("inputs_user.xlsx"))
layout = load_hydrodynamic_outputs(database_file("ouputs_hydrodynamic.xlsx"))
collection_point, dynamic_cable, static_cable, cable_route, connectors, external_protection, topology = load_electrical_outputs(database_file("ouputs_electrical.xlsx"))
line, foundation = load_MF_outputs(database_file("outputs_MF.xlsx"))

# OUTPUT options:
# *** Print outputs to terminal ***
PRINT_FLAG = True
# PRINT_FLAG = False
# *** Print plots ***
# PLOT_FLAG = True
PLOT_FLAG = False
# *** Produce csv ***
# PRINT_CSV = True
PRINT_CSV = False
cvs_filename = "Outputs/Installation_All.csv"
# *** Plot Gantt chart ***
PLOT_GANTT = True
# PLOT_GANTT = False
# *** Check Inputs ***
CHECK_INPUTS = True
# CHECK_INPUTS = False

start_time_ck = timeit.default_timer()
if CHECK_INPUTS:
    ERROR_IN_INPUT, input_warning_list = input_check(vessels, equipments, ports,
                                 site, metocean, device, sub_device, landfall, entry_point,
                                 layout,
                                 collection_point, dynamic_cable, static_cable,
                                 cable_route, connectors, external_protection,
                                 topology,
                                 line, foundation,
                                 PRINT_FLAG, PLOT_FLAG, PLOT_GANTT, PRINT_CSV,
                                 cvs_filename
                                 )
    for indx_error_warn in range(len(input_warning_list)):
        print input_warning_list[indx_error_warn]
else:
    ERROR_IN_INPUT = False


stop_time_ck = timeit.default_timer()
# print 'Input check simulation time [s]: ' + str(stop_time_ck - start_time_ck) # DEBUG!

if not ERROR_IN_INPUT:
    installation_output = installation_main(vessels, equipments, ports,
                                            phase_order, schedule_OLC,
                                            penet_rates, laying_rates,
                                            other_rates,
                                            port_sf, vessel_sf, eq_sf,
                                            site, metocean, device, sub_device,
                                            landfall, entry_point,
                                            layout,
                                            collection_point, dynamic_cable,
                                            static_cable, cable_route,
                                            connectors, external_protection,
                                            topology,
                                            line, foundation,
                                            PRINT_FLAG, PLOT_FLAG, PLOT_GANTT,
                                            PRINT_CSV, cvs_filename
                                            )
    print '-THE END-'
else:
    print 'Error in the Inputs!'