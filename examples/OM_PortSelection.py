"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org, pedro.vicente@wavec.org

main_OM_PortSelection.py is the file of the WP5 module for the selection of the port dedicated to the
Operation and Maintenance within the suite of design tools developped under the EU FP7 DTOcean project.
main_OM_PortSelection.py provides an estimation of the distance to port and port chosen for the OM operation.
The OM_port function selects the port used by OM logistic phases
    required by the O&M module, depending if is inspection or actual maintenance.
    For the case of inspection the closest port is chosen and the ID in the input: "outputs_OM.xlsx" should be INS_PORT.
    For the case of the other logistic phases, the ID in the input: "outputs_OM.xlsx" should be OM_PORT, and in this case the selection is based on a 2 step process:
        1 - the port feasibility functions from all logistic phases are taken
        into account, and the unfeasible ports are erased from the panda dataframes.
        2 - the closest port to the project site is choosen from the feasbile
        list of ports.
    In both cases, the dimensions of the spare parts should correspond to the biggest weight and dimensions possibly expected.
    This should be called the before the actual logistic module is called.

See also: ...

                       DTOcean project
                    http://www.dtocean.eu

                   WavEC Offshore Renewables
                    http://www.wavec.org/en

"""

from os import path
import os
import sys
sys.path.append('..')


from dtocean_logistics.load import load_port_data
from dtocean_logistics.load import load_sf
from dtocean_logistics.load.wp_bom import load_hydrodynamic_outputs
from dtocean_logistics.load.wp_bom import load_OM_outputs
from dtocean_logistics.phases import select_port_OM


# # Set directory paths for loading inputs
mod_path = path.dirname(path.realpath(__file__))

def database_file(file):
    """shortcut function to load files from the database folder
    """
    fpath = path.join('databases', '{0}'.format(file))
    db_path = path.join(mod_path, fpath)
    return db_path


"""
Load required inputs and database into panda dataframes
"""

#default_values inputs
port_sf, vessel_sf, eq_sf = load_sf(database_file("safety_factors.xlsx"))

#Internal logistic module databases
ports = load_port_data(database_file("logisticsDB_ports_python.xlsx"))

#upstream module inputs/outputs
#hydrodynamic_outputs = load_hydrodynamic_outputs(database_file("ouputs_hydrodynamic.xlsx"))


OM_outputs_PORT = load_OM_outputs(database_file("outputs_OM_Port.xlsx"))
OM_outputs_INS_PORT = load_OM_outputs(database_file("outputs_OM_INS_PORT.xlsx")) # JUST FOR TESTING!!!
OM_outputs_OM_PORT = load_OM_outputs(database_file("outputs_OM_PORT.xlsx")) # JUST FOR TESTING!!!

# OM_port_choice_input = OM_outputs_PORT
OM_port_choice_input = OM_outputs_INS_PORT # JUST FOR TESTING!!!
# OM_port_choice_input = OM_outputs_OM_PORT # JUST FOR TESTING!!!



"""
Port Selection based on input
"""
om_port = select_port_OM.OM_port(OM_port_choice_input, ports)



print 'Distance port-site [km]: ' + str(om_port['Distance port-site [km]'])
print 'Port Name: ' + om_port['Selected base port for installation']['Name [-]']
print 'Port DB index: ' + str(om_port['Port database index [-]'])
