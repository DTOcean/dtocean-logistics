# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is responsible for the selection of ports for both the installation
and O&M logistic activities. 

BETA VERSION NOTES: This current version is limited to the feasibility functions 
of two logistic phases (one for the installation module and one for the O&M), 
this will be upgraded for the beta version due to october.
"""
import math
import utm
from geopy.distance import great_circle

import os

from .transit_algorithm import transit_algorithm
# from ..configure import get_install_paths

import logging
module_logger = logging.getLogger(__name__)


def distance(UTM_ini, UTM_fin):
    """
    distance returns the calculated distance (in kms) between two points
    defined in the UTM coordinate system
    
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



def install_port(device, sub_device,
                 site, entry_point,
                 ports,
                 line, foundation,
                 collection_point,
                 instal_order,
                 point_path=None,
                 graph_path=None):
    """install_port function selects the home port used by all logistic phases
    during installation. This selection is based on a 2 step process: 
        1 - the port feasibility functions from all logistic phases are taken
        into account, and the unfeasible ports are erased from the panda dataframes.  
        2 - the closest port to the project site is choosen from the feasbile
        list of ports.

    Parameters
    ----------
    user_inputs : dict
     dictionnary containing all required inputs to WP5 coming from WP1/end-user
    electrical_outputs : dict
     dictionnary containing all required inputs to WP5 coming from WP3
    MF_outputs : DataFrame
     panda table containing all required inputs to WP5 coming from WP4
    port_data : DataFrame
     panda table containing the ports database
    point_path and graph_path are inputs required for the transport_algorithm

    Returns
    -------
    port : dict
     dictionnary containing the results port_listof the port selection
    """
    # initialisation
    port_data = ports
    port = {'Terminal load bearing [t/m^2]': 0,
            'Terminal area [m^2]': 0,
            'Port list satisfying the minimum requirements': 0,
            'Distance port-site [km]': 0,
            'Selected base port for installation': 0}

    max_total_load = 0
    max_total_area = 0
    
    # path_dict = get_install_paths()
    # include_dir = path_dict["logistics_include"]
    # if point_path is None:
    #     point_path = os.path.join(include_dir, "Point_DTOcean_0.csv")
    # if graph_path is None:
    #     graph_path = os.path.join(include_dir, "graph_sea_european_sea.p")

    # TO BE CHANGED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if point_path is None:
        point_path = 'Point_DTOcean_0.csv'
    if graph_path is None:
        graph_path = 'graph_sea_european_sea.p'


    for ind_order in instal_order:

        if len(instal_order[ind_order])>0:
            instl_ord = instal_order[ind_order][0]
        else:
            continue

        if instl_ord == 'E_cp_seabed':

            # save outputs required inside short named variables
            cp_db = collection_point
            cp_db = cp_db[cp_db['type [-]'] != 'surface piercing']
            cp_db = cp_db[cp_db['downstream ei type [-]'] != 'hard-wired cable']        
            
            load_u = cp_db['dry mass [kg]'] / (cp_db['length [m]'] * cp_db['width [m]'])
            area_u = cp_db['length [m]'] * cp_db['width [m]']

            max_total_load = max(load_u)
            max_total_area = max(area_u)


        if instl_ord == 'Gravity' or instl_ord == 'M_drag' or instl_ord == 'M_direct' or \
           instl_ord == 'M_suction' or instl_ord == 'M_pile' or instl_ord == 'Driven' or instl_ord == 'S_structure':
            # calculate loading and projected area of foundations/anchors
            max_moo_loading = 0
            max_moo_area = 0
            for ind_found in range(len(foundation)):
                load_u = foundation['dry mass [kg]'][ind_found] / (foundation['length [m]'][ind_found] * foundation['width [m]'][ind_found])
                area_u = foundation['length [m]'][ind_found] * foundation['width [m]'][ind_found]

                max_moo_loading = max(max_moo_loading,load_u)
                max_moo_area = max(max_moo_area,area_u)

            max_total_load = max(max_total_load,max_moo_loading)
            max_total_area = max(max_total_area,max_moo_area)


        if instl_ord == 'Devices':
            # calculate loading and projected area of device or sub-device
            max_dev_loading = 0
            max_dev_area = 0
            for ind_subdev in range(len(sub_device)):

                # print 'indice:'
                # print ind_subdev

                area_u = float(sub_device['length [m]'][ind_subdev]*sub_device['width [m]'][ind_subdev] )
                if area_u !=0:
                    load_u = float(sub_device['dry mass [kg]'][ind_subdev] / area_u )
                else:
                    load_u = 0

                max_dev_loading = max(max_dev_loading,load_u)
                max_dev_area = max(max_dev_area,area_u)

            max_total_load = max(max_total_load,max_dev_loading)
            max_total_area = max(max_total_area,max_dev_area)

            # print 'maxmass:'
            # print max_total_load


            # check load out strategy
            loadout_methd = device['load out [-]'].ix[0]
            if loadout_methd == 'float away':
                port_data_all = port_data
                port_data = port_data_all[ port_data_all['Type of terminal [Quay/Dry-dock]'] == 'Dry-dock']
                port_data = port_data.append( port_data_all[ port_data_all['Type of terminal [Quay/Dry-dock]'] == 'Quay, dry-dock'] )
                port_data = port_data.append( port_data_all[ port_data_all['Type of terminal [Quay/Dry-dock]'] == 'Yard, dry-dock'] )
                port_data = port_data.append( port_data_all[ port_data_all['Type of terminal [Quay/Dry-dock]'].isnull()] )

            max_dev_area = 0
            for ind_subdev in range(len(sub_device)):
                load_u = sub_device['dry mass [kg]'][ind_subdev] / (sub_device['length [m]'][ind_subdev] * sub_device['width [m]'][ind_subdev])
                area_u = sub_device['length [m]'][ind_subdev] * sub_device['width [m]'][ind_subdev]

                max_dev_loading = max(max_dev_loading,load_u)
                max_dev_area = max(max_dev_area,area_u)

            max_total_load = max(max_total_load,max_dev_loading)
            max_total_area = max(max_total_area,max_dev_area)

            # check load out strategy
            loadout_methd = device['load out [-]'].ix[0]
            if loadout_methd == 'float away':
                port_data_all = port_data
                port_data = port_data_all[ port_data_all['Type of terminal [Quay/Dry-dock]'] == 'Dry-dock']
                port_data = port_data.append( port_data_all[ port_data_all['Type of terminal [Quay/Dry-dock]'] == 'Quay, dry-dock'] )
                port_data = port_data.append( port_data_all[ port_data_all['Type of terminal [Quay/Dry-dock]'] == 'Yard, dry-dock'] )
                port_data = port_data.append( port_data_all[ port_data_all['Type of terminal [Quay/Dry-dock]'].isnull()] )


    # terminal load bearing minimum requirement
    port['Terminal load bearing [t/m^2]'] = float(max_total_load)/1000.0  # t/m^2
    port_pd_nan = port_data
    port_data = port_data[ port_data['Terminal load bearing [t/m^2]'] >= port['Terminal load bearing [t/m^2]'] ]
    port_data = port_data.append(port_pd_nan[port_pd_nan['Terminal load bearing [t/m^2]'].isnull()])

    port['Terminal area [m^2]'] = float(max_total_area)
    port_pd_nan = port_data
    port_data = port_data[ port_data['Terminal area [m^2]'] >= port['Terminal area [m^2]'] ]
    port_data = port_data.append(port_pd_nan[port_pd_nan['Terminal area [m^2]'].isnull()])

    port['Port list satisfying the minimum requirements'] = port_data

    if len(port_data)==0:
        
        msg = ("There is no port that satisfies the project requirements. "
               "The closest port will be used. Requirements are: "
               "Terminal load bearing {} [t/m^2], "
               "Terminal area {} [m^2]".format(
                   port['Terminal load bearing [t/m^2]'],
                   port['Terminal area [m^2]']))
        module_logger.info(msg)                   

        port_data = ports

    # Distance ports-site calculation to be implemented once the transit distance algorithm is available
    # by making use of the grid coordinate position of the site and the ports

    # USING ENTRY POINT!!!
    site_coords_x = entry_point['x coord [m]'].ix[0]
    site_coords_y = entry_point['y coord [m]'].ix[0]
    site_coords_zone = entry_point['zone [-]'].ix[0]

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
        if closest_ports_all[ind_clst+1][2] == closest_ports_all[ind_clst][2]:   # if same name
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

        # dist_to_port_i = transit_algorithm(site_coords, port_coords, point_path, graph_path)
        dist_to_port_i = distance(site_coords, port_coords)  # simplification just for testing

        dist_to_clost_port_vec.append(dist_to_port_i)
        min_dist_to_clst_port = min(dist_to_clost_port_vec)
        if min_dist_to_clst_port == dist_to_port_i:
            port_choice_index = ind_port

    # Nearest port selection to be modified by making use of port['Distance port-site'] will be implemented
    port['Selected base port for installation'] = port_data.ix[port_choice_index]
    port['Distance port-site [km]'] = min_dist_to_clst_port
    # print 'Port Selected!'

    return port




