"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org; pedro.vicente@wavec.org

Example_OM.py is an example file of the OM Logistics module within the suite of design tools
developped under the EU FP7 DTOcean project. Example.py provides an estimation of
the predicted performance of feasible maritime infrastructure solutions
that can carry out marine operations pertaining to the installation of
wave and tidal energy arrays.

Example.py can be described in the following sub-modules:
0- Loading the example input data
1- Calling the OM Logistics module

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

O&M_outputs (dict):  dictionnary containing all required inputs to WP5 coming from WP6
     'LogPhase1' (DataFrame): All inputs required for LpM1 logistic phase as defined by WP6

See also: ...

                       DTOcean project
                    http://www.dtocean.eu

                   WavEC Offshore Renewables
                    http://www.wavec.org/en

"""

from os import path
import sys
sys.path.append('..')


from dtocean_logistics.load import load_phase_order_data, load_time_olc_data
from dtocean_logistics.load import load_eq_rates
from dtocean_logistics.load import load_sf
from dtocean_logistics.load import load_vessel_data, load_equipment_data
from dtocean_logistics.load import load_port_data
from dtocean_logistics.load.wp_bom import load_user_inputs, load_hydrodynamic_outputs
from dtocean_logistics.load.wp_bom import load_OM_outputs
from dtocean_logistics.load.wp_bom import load_electrical_outputs, load_MF_outputs

from LOGISTICS_main import om_logistics_main



# # Set directory paths for loading inputs (@Tecnalia)
mod_path = path.dirname(path.realpath(__file__))

def database_file(file):
    """
    shortcut function to load files from the database folder
    """
    fpath = path.join('databases', '{0}'.format(file))
    db_path = path.join(mod_path, fpath)
    return db_path




"""
Load required inputs and database into panda dataframes
"""
# INPUT options:
#default_values inputs
schedule_OLC = load_time_olc_data(database_file("operations_time_OLC.xlsx"))
penet_rates, laying_rates, other_rates = load_eq_rates(database_file("equipment_perf_rates.xlsx"))
port_sf, vessel_sf, eq_sf = load_sf(database_file("safety_factors.xlsx"))
#Internal logistic module databases
vessels = load_vessel_data(database_file("logisticsDB_vessel_python.xlsx"))
equipments = load_equipment_data(database_file("logisticsDB_equipment_python.xlsx"))
ports = load_port_data(database_file("logisticsDB_ports_python.xlsx"))
#upstream module inputs/outputs
site, metocean, device, sub_device, landfall, entry_point = load_user_inputs(database_file("inputs_user.xlsx")) # THIS LINE HAS CHANGED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
layout = load_hydrodynamic_outputs(database_file("ouputs_hydrodynamic.xlsx"))
collection_point, dynamic_cable, static_cable, cable_route, connectors, external_protection, topology = load_electrical_outputs(database_file("ouputs_electrical.xlsx"))
# OM input information
om = load_OM_outputs(database_file("otherTesting/outputs_OM (test LpM1.1)_IWES.xlsx"))

# OUTPUT options:
# *** Print outputs to terminal ***
PRINT_FLAG = True
# PRINT_FLAG = False

om_output = om_logistics_main( vessels, equipments, ports,
                                         schedule_OLC, other_rates, port_sf, vessel_sf, eq_sf,
                                         site, metocean, device, sub_device, entry_point,
                                         layout,
                                         collection_point, dynamic_cable, static_cable, connectors,
                                         om,
                                         PRINT_FLAG
                                         )

print '-THE END-'