# -*- coding: utf-8 -*-

#    Copyright (C) 2016 Boris Teillant, Paulo Chainho
#    Copyright (C) 2017-2018 Mathew Topper
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

"""
This module is responsible for the selection of ports for the O&M logistic 
activities.

.. moduleauthor:: Boris Teillant <boris.teillant@wavec.org>
.. moduleauthor:: Paulo Chainho <paulo@wavec.org>
.. moduleauthor:: Mathew Topper <mathew.topper@dataonlygreater.com>
"""

import math
import logging

import utm
from geopy.distance import great_circle

# from .transit_algorithm import transit_algorithm
# from ..configure import get_install_paths

module_logger = logging.getLogger(__name__)


def distance(UTM_ini, UTM_fin):
    """
    distance returns the calculated distance (in kms) between two points
    defined in the UTM coordinate system using geographical distances
    
    Parameters
    ----------
    UTM_ini : list
    initial UTM coordinates in x,y, zone format
    UTM_fin : list
    final UTM coordinates in x,y, zone format

    Returns
    -------
    dist : float
    direct geographical distance in kms between two UTM coordinates
    """

    UTM_ini_x = UTM_ini[0]
    UTM_ini_y = UTM_ini[1]
    UTM_ini_zone = UTM_ini[2]

    UTM_fin_x = UTM_fin[0]
    UTM_fin_y = UTM_fin[1]
    UTM_fin_zone = UTM_fin[2]

    [LAT_INI, LONG_INI] = utm.to_latlon(UTM_ini_x, UTM_ini_y, int(UTM_ini_zone[0:2]), str(UTM_ini_zone[3]))  # to get dd.dd from utm
    [LAT_FIN, LONG_FIN] = utm.to_latlon(UTM_fin_x, UTM_fin_y, int(UTM_fin_zone[0:2]), str(UTM_fin_zone[3]))  # to get dd.dd from utm

    point_i = (LAT_INI, LONG_INI)
    point_f = (LAT_FIN, LONG_FIN)

    distance = great_circle(point_i, point_f).kilometers # gives you a distance (in kms) between two coordinate in dd.dd
    
    return distance

def OM_port(OM_outputs,
            port_data,
            point_path=None,
            graph_path=None):
    """main_OM_PortSelection.py is the file of the WP5 module for the selection of the port dedicated to the
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
=======
    Arguments
    ----------
    OM_outputs : dict
     dictionnary containing all required inputs to WP5 coming from WP6/end-user stating the biggest of all the sp dimensions and weight for either
     inspection or actual maintenance
    port_data : DataFrame
     panda table containing the ports database     
    point_path and graph_path are files required for transit algorithm.

    Returns
    -------
    port : dict
     dictionnary containing the results of the port selection
    """

#    path_dict = get_install_paths()
#    include_dir = path_dict["logistics_include"]
#    if point_path is None:
#        point_path = os.path.join(include_dir, "Point_DTOcean_0.csv")
#    if graph_path is None:
#        graph_path = os.path.join(include_dir, "graph_sea_european_sea.p")

    # # TO BE CHANGED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # if point_path is None:
    #     point_path = 'Point_DTOcean_0.csv'
    # if graph_path is None:
    #     graph_path = 'graph_sea_european_sea.p'



    # initialisation
    port = {'Terminal load bearing [t/m^2]': 0,
            'Terminal area [m^2]': 0,
            'Port list satisfying the minimum requirements': 0,
            'Distance port-site [km]': 0,
            'Selected base port for installation': 0,
            'Port database index' : 0}


    if OM_outputs['ID [-]'].ix[0] == 'INS_PORT':

        msg = ("Inspection only, will use the closest port")
        module_logger.warning(msg)

    elif OM_outputs['ID [-]'].ix[0] == 'OM_PORT':

        msg = ("Will use the closest feasible port")
        module_logger.info(msg)

        # Calculate loading and projeted area of Spare Parts:
        # Input collection
        lenght_SP = OM_outputs['sp_length [m]'].ix[0]
        width_SP = OM_outputs['sp_width [m]'].ix[0]
        height_SP = OM_outputs['sp_height [m]'].ix[0]
        total_mass_SP = OM_outputs['sp_dry_mass [kg]'].ix[0]

        # Feasibility functions
        SP_area = float(lenght_SP) * float(width_SP)
        SP_loading = float(total_mass_SP) / float(SP_area) / 1000

        # terminal load bearing minimum requirement
        port_pd_nan = port_data
        port_data = port_data[port_data['Terminal area [m^2]'] >= SP_area]
        port_data = port_data.append(port_pd_nan[port_pd_nan['Terminal area [m^2]'].isnull()])

        deselected = port_pd_nan[port_pd_nan['Terminal area [m^2]'] < SP_area]
    
        if not deselected.empty:
    
            port_names = deselected['Name [-]']
            ports_str = ", ".join(port_names)
            
            logMsg = (u"The following ports did not meet the 'Terminal area' "
                      "requirement of {} m^2: "
                      "{}").format(SP_area, ports_str).encode('utf-8')
            module_logger.info(logMsg)

        port_pd_nan = port_data
        port_data = port_data[port_data['Terminal load bearing [t/m^2]'] >= SP_loading] # t/m^2
        port_data = port_data.append(port_pd_nan[port_pd_nan['Terminal load bearing [t/m^2]'].isnull()])

        deselected = port_pd_nan[
                    port_pd_nan['Terminal load bearing [t/m^2]'] < SP_loading]
    
        if not deselected.empty:
            
            port_names = deselected['Name [-]']
            ports_str = ", ".join(port_names)
            
            logMsg = ("The following ports did not meet the 'Terminal load "
                      "bearing' requirement of {} t/m^2: {}").format(
                                                                  SP_loading,
                                                                  ports_str)
            module_logger.info(logMsg)

        port['Port list satisfying the minimum requirements'] = port_data

        if len(port_data)==0:
            msg = ("There is no port that satisfies the project requirements. "
                   "The closest port will be used. "
                   "Requirements are: "
                   "Terminal load bearing {} [t/m^2], "
                   "Terminal area {} [m^2]".format(
                       port['Terminal load bearing [t/m^2]'],
                       port['Terminal area [m^2]']))
            module_logger.info(msg)           
            port_data = port_data


    else:
        msg = ("ERROR: unknown ID {} for port calculation. Accepted: INS_PORT "
               " or OM_PORT.".format(OM_outputs['ID [-]'].ix[0]))
        module_logger.warning(msg)

    # using UTM coordinates in the input which should match the ones of the entry point to be considered
    site_coords_x = OM_outputs['x coord [m]'].ix[0]
    site_coords_y = OM_outputs['y coord [m]'].ix[0]
    site_coords_zone = OM_outputs['zone [-]'].ix[0]
    site_coords = [site_coords_x, site_coords_y, site_coords_zone]

    dist_to_port_vec = []
    for ind_port, row in port_data.iterrows():
        port_coords_x = port_data['UTM x [m]'][ind_port]
        port_coords_y = port_data['UTM y [m]'][ind_port]
        port_coords_zone = port_data['UTM zone [-]'][ind_port]
        port_coords = [port_coords_x, port_coords_y, port_coords_zone]

        if math.isnan(port_coords_x):
            continue
        dist_to_port_i = distance(site_coords, port_coords)   # closest ports by geo distance!
        dist_to_port_vec.append( [dist_to_port_i, ind_port, port_data['Name [-]'][ind_port]] )
    closest_ports_all=sorted(dist_to_port_vec)
    # furthest_ports_all = closest_ports_all.reverse()

    # check if repeted port (by terminal)
    LEN_clst = len(closest_ports_all)-1
    ind_clst=0
    while ind_clst < LEN_clst:
        if closest_ports_all[ind_clst+1][2] == closest_ports_all[ind_clst][2]:  # if same name
            del closest_ports_all[ind_clst+1]
            LEN_clst = LEN_clst-1
        else:
            ind_clst = ind_clst+1


    # Identify the n=num_ports_consider closest ports:
    # num_ports_consider = len(dist_to_port_vec)  # consider all
    num_ports_consider = 5
    closest_ports_n = closest_ports_all[:min(num_ports_consider,len(closest_ports_all))]


    # Find the closest port using the transit_algorithm:
    dist_to_clost_port_vec=[]
    for ind_closest_port in range(len(closest_ports_n)):
        ind_port= closest_ports_n[ind_closest_port][1]
        port_coords_x = port_data['UTM x [m]'][ind_port]
        port_coords_y = port_data['UTM y [m]'][ind_port]
        port_coords_zone = port_data['UTM zone [-]'][ind_port]
        port_coords = [port_coords_x, port_coords_y, port_coords_zone]

        if math.isnan(port_coords_x):
            continue

#        dist_to_port_i = transit_algorithm(site_coords, port_coords, point_path, graph_path)
        dist_to_port_i = distance(site_coords, port_coords)  # simplification just for TESTING!!!!!!!!!!!!!!!!!!!!!!!!!

        dist_to_clost_port_vec.append(dist_to_port_i)
        min_dist_to_clst_port = min(dist_to_clost_port_vec)
        if min_dist_to_clst_port == dist_to_port_i:
            port_choice_index = ind_port


    port['Selected base port for installation'] = port_data.ix[port_choice_index]
    port['Distance port-site [km]'] = min_dist_to_clst_port
    port['Port database index [-]'] = int(port_choice_index)


    return port