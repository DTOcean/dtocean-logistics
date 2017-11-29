# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is part of the characterization step in the WP5 methodology. It 
contains feasibility functions to compute the minimum logistic requirements to 
carry out the different logistic phases. This particular modules includes the
function related to the installation of electrical infrastructure.

BETA VERSION NOTES: This module is still to be done.
"""
from math import pi
import pandas as pd
import numpy as np
from dtocean_logistics.load.snap_2_grid import SnapToGrid

import logging
module_logger = logging.getLogger(__name__)

def export_feas(log_phase, log_phase_id, site, static_cable, cable_route,
                connectors, collection_point):
    """cp_feas is a function which determines the logistic requirement associated 
    with one logistic phase dealing with the installation of the electrical infrastructure
    """
    """array_feas is a function which determines the logistic requirement associated 
    with the one logistic phase dealing with the installation of export static cables
    """
    # Input collection --------------------------------------------------------
    static_db = static_cable
    route_db = cable_route
    connect_db = connectors
    cp_db = collection_point
    site = site
    site_up = pd.DataFrame()
    site_down = pd.DataFrame()
    site_hardwired = site
    
    # Select only export cables database and route
    export_db = static_db[static_db['type [-]'] == 'export']
    export_index = static_db.index.values
    export_route = route_db[route_db['static cable id [-]'].isin(export_index)]
    
    depth = export_route['bathymetry [m]']

    # Obtain cable characteristics
    export_mass = export_db['dry mass [kg/m]'].fillna(0)/1000.0
    export_total_mass = export_db['total dry mass [kg]'].fillna(0)
    export_lenght = export_db['length [m]'].fillna(0)
    export_diam = export_db['diameter [mm]'].fillna(0)
    export_MBR = export_db['MBR [m]'].fillna(0)
    
    export_up_type = export_db['upstream termination type [-]']
    export_down_type = export_db['downstream termination type [-]']
    
    export_up_ei = export_db['upstream ei type [-]']
    export_up_ei_id = export_db['upstream ei id [-]']
    export_down_ei = export_db['downstream ei type [-]']
    export_down_ei_id = export_db['downstream ei id [-]']
    
    # Obtain connectors characteristics
    export_wet = export_db[export_db['upstream ei type [-]'] == 'wet-mate']
    export_wet.append(export_db[export_db['downstream ei type [-]'] == 'wet-mate'])
    export_connect_id = export_db['upstream ei id [-]']
    export_connect_id.append(export_db['downstream ei id [-]'])
    export_wet_connect = connect_db.ix[export_connect_id]
    
    # Obtain cable route characteristics
    burial_depth = export_route['burial depth [m]']
    
    # Obtain hard-wired collection point characteristics
    if (export_up_ei == 'hard-wired').any():
        export_hardwired_db = export_db[export_db['upstream ei type [-]'] == 'hard-wired']
        export_hardwired_id = list(export_hardwired_db.index.values)   
        export_hardwired_route = pd.DataFrame()
        
        for a in range(len(export_hardwired_id)):
            cable_id = export_hardwired_id[a]   
            export_hardwired_route = export_hardwired_route.append( static_route[(static_route['static cable id [-]'] == cable_id)] )
            
        depth_hardwired = max( export_hardwired_route['bathymetry [m]'] )
        
        export_hardwired_mass = export_hardwired_db['dry mass [kg/m]'].fillna(0)/1000.0
        export_hardwired_lenght = export_hardwired_db['length [m]'].fillna(0)
        export_hardwired_cp = export_hardwired_db['upstream ei id [-]']

        cp_hardwired_db = cp_db.index[export_hardwired_cp]
        
        cp_weight = cp_hardwired_db['dry mass [kg]'].fillna(0)/1000.0
        cp_lenght = cp_hardwired_db['length [m]'].fillna(0)
        cp_width = cp_hardwired_db['width [m]'].fillna(0)
        cp_pigtails_nr = cp_db['nr pigtails [-]'].fillna(0)
        cp_pigtails_lenght = cp_db['pigtails length [m]'].fillna(0)
        cp_pigtails_diam = cp_db['pigtails diameter [mm]'].fillna(0)/1000.0
        cp_pigtails_mass = cp_db['pigtails cable dry mass [kg/m]'].fillna(0)/1000.0

        area = cp_lenght*cp_width + cp_pigtails_nr*cp_pigtails_lenght*cp_pigtails_diam
        lifting = 3*depth_hardwired*export_hardwired_mass + cp_weight + \
                  cp_pigtails_nr*cp_pigtails_mass*cp_pigtails_lenght
        
    # Feasibility functions ---------------------------------------------------

    # Vessels       
    turntable_load = max( max(export_total_mass), max(export_lenght*export_mass) )
    turntable_radius = max(export_MBR)*2
    bathymetry = max(depth)
    DP = 1
    if (export_up_ei == 'hard-wired').any():
        deck_area = max(area)
        deck_cargo =  max( max(export_total_mass), max(export_lenght*export_mass) )
        deck_loading = 0
        lifting_cap = max(lifting)
    else: 
        deck_area = 0
        deck_cargo =  max( max(export_total_mass), max(export_lenght*export_mass) )
        deck_loading = 0
        lifting_cap = max(3*bathymetry*export_mass)
        
    # ROV    
    if (export_up_ei == 'wet-mate').any() or (export_down_ei == 'wet-mate').any():
        rov_class = 'Workclass'
        mate_force = max(export_wet_connect['mating force [N]'])
    else:
        rov_class = 'Inspection class'
        mate_force = 0

    # Cable Burial Tool
    trench_depth = max(burial_depth)
    trench_diam = max(export_diam)
    MBR = max(export_MBR)

    feas_e = {'rov': [ ['Depth rating [m]', 'sup', bathymetry],
                       ['ROV class [-]', 'equal', rov_class],
                       ['Manipulator grip force [N]', 'sup', mate_force], ], 

              'plough': [ ['Max operating depth [m]', 'sup', bathymetry],
                          ['Max cable diameter [mm]', 'sup', trench_diam],
                          ['Min cable bending radius [m]', 'sup', MBR],
                          ['Ploughing trench depth [m]', 'sup', trench_depth]  ],

              'jetter': [ ['Max operating depth [m]', 'sup', bathymetry],
                          ['Max cable diameter [mm]', 'sup', trench_diam],
                          ['Min cable bending radius [m]', 'sup', MBR],
                          ['Jetting trench depth [m]', 'sup', trench_depth]  ],

              'cutter': [ ['Max operating depth [m]', 'sup', bathymetry],
                          ['Max cable diameter [mm]', 'sup', trench_diam],
                          ['Min cable bending radius [m]', 'sup', MBR],
                          ['Cutting trench depth [m]', 'sup', trench_depth]  ] }

 
    feas_v = {'CLV': [ ['Deck space [m^2]', 'sup', deck_area],
                       ['Turntable loading [t]', 'sup', turntable_load],
                       ['Turntable inner diameter [m]', 'sup', turntable_radius],
                       ['DP [-]', 'sup', DP],
                       ['Crane capacity [t]', 'sup', lifting_cap] ],

              'CLB': [ ['Deck space [m^2]', 'sup', deck_area],
                       ['Turntable loading [t]', 'sup', turntable_load],
                       ['Turntable inner diameter [m]', 'sup', turntable_radius],
                       ['DP [-]', 'sup', DP],
                       ['Crane capacity [t]', 'sup', lifting_cap] ] }
 
    # Matching ----------------------------------------------------------------
    feas_m_pv = {'CLV': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                 'CLB':  [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                           ['Length [m]', 'sup', 'Terminal length [m]'],
                           ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ] }
    feas_m_pe = {}

    feas_m_ve = {'rov': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                          ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                          ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'] ],

                 'plough': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                             ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                             ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'],
                             ['Tow force required [t]', 'sup', 'Bollard pull [t]'] ],

                 'jetter': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                             ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                             ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'] ],

                 'cutter': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                             ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                             ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'] ] }


    deck_req = {'deck area': deck_area, 'deck cargo': deck_cargo, 'deck loading': deck_loading}
    
    return feas_e, feas_v, feas_m_pv, feas_m_pe, feas_m_ve, deck_req


def array_feas(log_phase, log_phase_id, site, static_cable, cable_route,
               connectors, collection_point):
    """array_feas is a function which determines the logistic requirement associated 
    with the one logistic phase dealing with the installation of array static cables
    """
    # Input collection --------------------------------------------------------
    static_db = static_cable
    route_db = cable_route
    connect_db = connectors
    cp_db = collection_point
    site = site
    site_up = pd.DataFrame()
    site_down = pd.DataFrame()
    site_hardwired = site
    
    # Select only array cables database and route
    array_db = static_db[static_db['type [-]'] == 'array']
    array_index = list(array_db.index.values)    
    array_route = route_db[route_db['static cable id [-]'].isin(array_index)]                             
    
    depth = array_route['bathymetry [m]']

    # Obtain cable characteristics
    array_mass = array_db['dry mass [kg/m]'].fillna(0)/1000.0
    array_total_mass = array_db['total dry mass [kg]'].fillna(0)
    array_lenght = array_db['length [m]'].fillna(0)
    array_diam = array_db['diameter [mm]'].fillna(0)
    array_MBR = array_db['MBR [m]'].fillna(0)
    
    array_up_type = array_db['upstream termination type [-]']
    array_down_type = array_db['downstream termination type [-]']
    
    array_up_ei = array_db['upstream ei type [-]']
    array_up_ei_id = array_db['upstream ei id [-]']
    array_down_ei = array_db['downstream ei type [-]']
    array_down_ei_id = array_db['downstream ei id [-]']
    
    # Obtain connectors characteristics
    array_wet = array_db[array_db['upstream ei type [-]'] == 'wet-mate']
    array_wet.append(array_db[array_db['downstream ei type [-]'] == 'wet-mate'])
    array_connect_id = array_db['upstream ei id [-]']
    array_connect_id.append(array_db['downstream ei id [-]'])
    array_wet_connect = connect_db.ix[array_connect_id]
    
    # Obtain cable route characteristics
    burial_depth = array_route['burial depth [m]']
   
    # Obtain hard-wired collection point characteristics
    if (array_up_ei == 'hard-wired').any():
        array_hardwired_db = array_db[array_db['upstream ei type [-]'] == 'hard-wired']
        array_hardwired_id = list(array_hardwired_db.index.values)   
        array_hardwired_route = pd.DataFrame()
        
        for a in range(len(array_hardwired_id)):
            cable_id = array_hardwired_id[a]   
            array_hardwired_route = array_hardwired_route.append( static_route[(static_route['static cable id [-]'] == cable_id)] )
            
        depth_hardwired = max( array_hardwired_route['bathymetry [m]'] )
        
        array_hardwired_mass = array_hardwired_db['dry mass [kg/m]'].fillna(0)/1000.0
        array_hardwired_lenght = array_hardwired_db['length [m]'].fillna(0)
        array_hardwired_cp = array_hardwired_db['upstream ei id [-]']

        cp_hardwired_db = cp_db.index[array_hardwired_cp]
        
        cp_weight = cp_hardwired_db['dry mass [kg]'].fillna(0)/1000.0
        cp_lenght = cp_hardwired_db['length [m]'].fillna(0)
        cp_width = cp_hardwired_db['width [m]'].fillna(0)
        cp_pigtails_nr = cp_db['nr pigtails [-]'].fillna(0)
        cp_pigtails_lenght = cp_db['pigtails length [m]'].fillna(0)
        cp_pigtails_diam = cp_db['pigtails diameter [mm]'].fillna(0)/1000.0
        cp_pigtails_mass = cp_db['pigtails cable dry mass [kg/m]'].fillna(0)/1000.0

        area = cp_lenght*cp_width + cp_pigtails_nr*cp_pigtails_lenght*cp_pigtails_diam
        lifting = 3*depth_hardwired*array_hardwired_mass + cp_weight + \
                  cp_pigtails_nr*cp_pigtails_mass*cp_pigtails_lenght
        
    # Feasibility functions ---------------------------------------------------

    # Vessels       
    turntable_load = max( max(array_total_mass), max(array_lenght*array_mass) )
    turntable_radius = max(array_MBR)*2
    bathymetry = max(depth)
    DP = 1
    if (array_up_ei == 'hard-wired').any():
        deck_area = max(area)
        deck_cargo =  max( max(array_total_mass), max(array_lenght*array_mass) )
        deck_loading = 0
        lifting_cap = max(lifting)
    else: 
        deck_area = 0
        deck_cargo =  max( max(array_total_mass), max(array_lenght*array_mass) )
        deck_loading = 0
        lifting_cap = max(3*bathymetry*array_mass)
        
    # ROV    
    if (array_up_ei == 'wet-mate').any() or (array_down_ei == 'wet-mate').any():
        rov_class = 'Workclass'
        mate_force = max(array_wet_connect['mating force [N]'])
    else:
        rov_class = 'Inspection class'
        mate_force = 0

    # Cable Burial Tool
    trench_depth = max(burial_depth)
    trench_diam = max(array_diam)
    MBR = max(array_MBR)

    feas_e = {'rov': [ ['Depth rating [m]', 'sup', bathymetry],
                       ['ROV class [-]', 'equal', rov_class],
                       ['Manipulator grip force [N]', 'sup', mate_force], ], 

              'plough': [ ['Max operating depth [m]', 'sup', bathymetry],
                          ['Max cable diameter [mm]', 'sup', trench_diam],
                          ['Min cable bending radius [m]', 'sup', MBR],
                          ['Ploughing trench depth [m]', 'sup', trench_depth]  ],

              'jetter': [ ['Max operating depth [m]', 'sup', bathymetry],
                          ['Max cable diameter [mm]', 'sup', trench_diam],
                          ['Min cable bending radius [m]', 'sup', MBR],
                          ['Jetting trench depth [m]', 'sup', trench_depth]  ],

              'cutter': [ ['Max operating depth [m]', 'sup', bathymetry],
                          ['Max cable diameter [mm]', 'sup', trench_diam],
                          ['Min cable bending radius [m]', 'sup', MBR],
                          ['Cutting trench depth [m]', 'sup', trench_depth]  ] }

 
    feas_v = {'CLV': [ ['Deck space [m^2]', 'sup', deck_area],
                       ['Turntable loading [t]', 'sup', turntable_load],
                       ['Turntable inner diameter [m]', 'sup', turntable_radius],
                       ['DP [-]', 'sup', DP],
                       ['Crane capacity [t]', 'sup', lifting_cap] ],

              'CLB': [ ['Deck space [m^2]', 'sup', deck_area],
                       ['Turntable loading [t]', 'sup', turntable_load],
                       ['Turntable inner diameter [m]', 'sup', turntable_radius],
                       ['DP [-]', 'sup', DP],
                       ['Crane capacity [t]', 'sup', lifting_cap] ] }
 
    # Matching ----------------------------------------------------------------
    feas_m_pv = {'CLV': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                 'CLB':  [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                           ['Length [m]', 'sup', 'Terminal length [m]'],
                           ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ] }
    feas_m_pe = {}

    feas_m_ve = {'rov': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                          ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                          ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'] ],

                 'plough': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                             ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                             ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'],
                             ['Tow force required [t]', 'sup', 'Bollard pull [t]'] ],

                 'jetter': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                             ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                             ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'] ],

                 'cutter': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                             ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                             ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'] ] }

    deck_req = {'deck area': deck_area, 'deck cargo': deck_cargo, 'deck loading': deck_loading}
    
    return feas_e, feas_v, feas_m_pv, feas_m_pe, feas_m_ve, deck_req


def dynamic_feas(log_phase, log_phase_id, site, 
                 dynamic_cable, connectors):
    """dynamic_feas is a function which determines the logistic requirement associated 
    with the one logistic phase dealing with the installation of dynamic cables
    """
    # Input collection --------------------------------------------------------
    dyn_db = dynamic_cable
    site = site
    site_up = pd.DataFrame()
    site_down = pd.DataFrame()
    connect_db = connectors
    
    snap_to_grid = SnapToGrid(site)
        
    dyn_mass = dyn_db['dry mass [kg/m]'].fillna(0)/1000.0
    dyn_total_mass = dyn_db['total dry mass [kg]'].fillna(0)
    dyn_lenght = dyn_db['length [m]'].fillna(0)
    dyn_diam = dyn_db['diameter [mm]'].fillna(0)/1000.0
    dyn_MBR = dyn_db['MBR [m]'].fillna(0)
    
    dyn_up_type = dyn_db['upstream termination type [-]']
    dyn_down_type = dyn_db['downstream termination type [-]']
    
    dyn_up_ei = dyn_db['upstream ei type [-]']
    dyn_up_ei_id = dyn_db['upstream ei id [-]']
    dyn_down_ei = dyn_db['downstream ei type [-]']
    dyn_down_ei_id = dyn_db['downstream ei id [-]']

    dyn_wet = dyn_db[dyn_db['upstream ei type [-]'] == 'wet-mate']
    dyn_wet.append(dyn_db[dyn_db['downstream ei type [-]'] == 'wet-mate'])
    wet_connect_id = dyn_wet['upstream ei id [-]']
    wet_connect_id.append(dyn_wet['downstream ei id [-]'])
    dyn_wet_connect = connect_db.ix[wet_connect_id]

    bouyancy_nr = dyn_db['buoyancy number [-]'].fillna(0)/1000.0
    bouyancy_diam = dyn_db['buoyancy diameter [mm]'].fillna(0)/1000.0
    
    # Obtain bathymetry for all sites
    coord_x_up = list(dyn_db['upstream termination x coord [m]'])
    coord_y_up = list(dyn_db['upstream termination y coord [m]'])
    coord_zone_up = list(dyn_db['upstream termination zone [-]'])

    for a in range(len(coord_x_up)):
        UTM_elem_x = coord_x_up[a]
        UTM_elem_y = coord_y_up[a]
        UTM_zone = coord_zone_up[a]

        # check the closest point in the site data
        closest_point = snap_to_grid((UTM_elem_x,UTM_elem_y))
        # obtain site data for the coordinates
        site_up = site_up.append( site[ (site['x coord [m]'] == float( closest_point[0] )) & \
                           (site['y coord [m]'] == float( closest_point[1] )) & \
                           (site['zone [-]'] == UTM_zone) ])
                                       
    depth_up = site_up['bathymetry [m]'].fillna(0)
    depth_up = depth_up.tolist()    
    
    coord_x_down = list(dyn_db['downstream termination x coord [m]'])
    coord_y_down = list(dyn_db['downstream termination y coord [m]'])
    coord_zone_down = list(dyn_db['downstream termination zone [-]'])
    
    for a in range(len(coord_x_down)):
        UTM_elem_x = coord_x_down[a]
        UTM_elem_y = coord_y_down[a]
        UTM_zone = coord_zone_down[a]

        # check the closest point in the site data
        closest_point = snap_to_grid((UTM_elem_x,UTM_elem_y))
        # obtain site data for the coordinates
        site_down = site_down.append( site[ (site['x coord [m]'] == float( closest_point[0] )) & \
                           (site['y coord [m]'] == float( closest_point[1] )) & \
                           (site['zone [-]'] == UTM_zone) ])
    
    depth_down = site_down['bathymetry [m]'].fillna(0)
    depth_down = depth_down.tolist()
    
    # Feasibility functions ---------------------------------------------------
    
    # Vessel
    deck_area = max( bouyancy_nr*(pi*(bouyancy_diam/2)**2) )
    deck_cargo =  max( max(dyn_total_mass), max(dyn_lenght*dyn_mass) )
    deck_loading = 0
    turntable_load = max( max(dyn_total_mass), max(dyn_lenght*dyn_mass) )
    turntable_radius = max(dyn_MBR)*2
    bathymetry = max( max(depth_up), max(depth_down)  )
    lifting_cap = 3*max( max(depth_up*dyn_mass), max(depth_down*dyn_mass) )
    
    # ROV
    if (dyn_up_ei == 'wet-mate').any() or (dyn_down_ei == 'wet-mate').any():
        rov_class = 'Workclass'
        mate_force = max(dyn_wet_connect['mating force [N]'])
    else:
        rov_class = 'Inspection class'
        mate_force = 0

    feas_e = {'rov': [ ['Depth rating [m]', 'sup', bathymetry],
                       ['ROV class [-]', 'equal', rov_class],
                       ['Manipulator grip force [N]', 'sup', mate_force] ] }

    feas_v = {'CLV': [ ['Deck space [m^2]', 'sup', deck_area],
                       ['Turntable loading [t]', 'sup', turntable_load],
                       ['Turntable inner diameter [m]', 'sup', turntable_radius],
                       ['Crane capacity [t]', 'sup', lifting_cap] ],

              'CLB': [ ['Deck space [m^2]', 'sup', deck_area],
                       ['Turntable loading [t]', 'sup', turntable_load],
                       ['Turntable inner diameter [m]', 'sup', turntable_radius],
                       ['Crane capacity [t]', 'sup', lifting_cap] ] }
 
    # Matching ----------------------------------------------------------------
    feas_m_pv = {'CLV': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                 'CLB':  [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                           ['Length [m]', 'sup', 'Terminal length [m]'],
                           ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ] }
    feas_m_pe = {}

    feas_m_ve = {'rov': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                          ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                          ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'] ] }

    deck_req = {'deck area': deck_area, 'deck cargo': deck_cargo, 'deck loading': deck_loading}
    

    return feas_e, feas_v, feas_m_pv, feas_m_pe, feas_m_ve, deck_req

    
def cp_feas(log_phase, log_phase_id, site, collection_point):
    """cp_feas is a function which determines the logistic requirement associated 
    with the two logistic phases dealing with the installation of collection points
    """
    # Input collection --------------------------------------------------------
    cp_db = collection_point

    if log_phase_id == 'E_cp_seabed':
        cp_db = cp_db[ (cp_db['type [-]'] == 'seabed') | (cp_db['type [-]'] == 'seabed with pigtails') ]
    elif log_phase_id == 'E_cp_surface':
        cp_db = cp_db[ cp_db['type [-]'] == 'surface piercing' ]
    else:
        msg = ("CP feasibility - wrong log_phase_id supplied {}.".format(
            log_phase_id))
        module_logger.warning(msg)

    site = site
    site_cp = pd.DataFrame()
    
    snap_to_grid = SnapToGrid(site)
    
    cp_weight = cp_db['dry mass [kg]'].fillna(0)/1000.0
    cp_lenght = cp_db['length [m]'].fillna(0)
    cp_width = cp_db['width [m]'].fillna(0)
    cp_pigtails_nr = cp_db['nr pigtails [-]'].fillna(0)
    cp_pigtails_lenght = cp_db['pigtails length [m]'].fillna(0)
    cp_pigtails_diam = cp_db['pigtails diameter [mm]'].fillna(0)/1000.0
    cp_pigtails_mass = cp_db['pigtails total dry mass [kg]'].fillna(0)/1000.0
    
    cp_coord_x = list(cp_db['x coord [m]'])
    cp_coord_y = list(cp_db['y coord [m]'])
    cp_coord_zone = list(cp_db['zone [-]'])
    
    for a in range(len(cp_coord_x)):
        UTM_elem_x = cp_coord_x[a]
        UTM_elem_y = cp_coord_y[a]
        UTM_zone = cp_coord_zone[a]
        # check the closest point in the site data
        closest_point = snap_to_grid((UTM_elem_x,UTM_elem_y))
        # obtain site data for the coordinates
        site_cp = site_cp.append( site[ (site['x coord [m]'] == float( closest_point[0] )) & \
                           (site['y coord [m]'] == float( closest_point[1] )) & \
                           (site['zone [-]'] == UTM_zone) ])
    
    depth = site_cp['bathymetry [m]'].fillna(0)
    depth = depth.tolist()
    
    # Feasibility functions ---------------------------------------------------
    deck_area = max( cp_lenght*cp_width + cp_pigtails_nr*cp_pigtails_lenght*cp_pigtails_diam )
    deck_cargo = max(cp_weight + cp_pigtails_nr*cp_pigtails_mass)
    deck_loading = max( cp_weight/(cp_lenght*cp_width) )
    lifting_cap = max(cp_weight + cp_pigtails_nr*cp_pigtails_mass)
    bathymetry = max(depth)
    DP = 1
    rov_class = 'Inspection class'

    feas_e = {'rov': [ ['Depth rating [m]', 'sup', bathymetry],
                       ['ROV class [-]', 'equal', rov_class] ] }

    feas_v = {'Crane Vessel': [ ['Deck space [m^2]', 'sup', deck_area],
                                ['Max. cargo [t]', 'sup', deck_cargo],
                                ['Deck loading [t/m^2]', 'sup', deck_loading],
                                ['Crane capacity [t]', 'sup', lifting_cap],
                                ['DP [-]', 'sup', DP] ],

              'Crane Barge':  [ ['Deck space [m^2]', 'sup', deck_area],
                                ['Max. cargo [t]', 'sup', deck_cargo],
                                ['Deck loading [t/m^2]', 'sup', deck_loading],
                                ['Crane capacity [t]', 'sup', lifting_cap],
                                ['DP [-]', 'sup', DP] ],

              'JUP Vessel':   [ ['Deck space [m^2]', 'sup', deck_area],
                                ['Max. cargo [t]', 'sup', deck_cargo],
                                ['Deck loading [t/m^2]', 'sup', deck_loading],
                                ['Crane capacity [t]', 'sup', lifting_cap],
                                ['DP [-]', 'sup', DP],
                                ['JackUp max payload [t]', 'sup', deck_cargo],
                                ['JackUp max water depth [m]', 'sup', bathymetry] ],

              'JUP Barge':    [ ['Deck space [m^2]', 'sup', deck_area],
                                ['Max. cargo [t]', 'sup', deck_cargo],
                                ['Deck loading [t/m^2]', 'sup', deck_loading],
                                ['Crane capacity [t]', 'sup', deck_cargo],
                                ['DP [-]', 'sup', DP],
                                ['JackUp max payload [t]', 'sup', deck_cargo],
                                ['JackUp max water depth [m]', 'sup', bathymetry] ],

              'CSV':          [ ['Deck space [m^2]', 'sup', deck_area],
                                ['Max. cargo [t]', 'sup', deck_cargo],
                                ['Deck loading [t/m^2]', 'sup', deck_loading],
                                ['Crane capacity [t]', 'sup', deck_cargo],
                                ['DP [-]', 'sup', DP] ] }
 
    # Matching ----------------------------------------------------------------
    feas_m_pv = {'Crane Vessel': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                 'Crane Barge':  [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                 'JUP Vessel':   [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                                   
                 'JUP Barge':    [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                 'CSV':          [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ] }
    feas_m_pe = {}

    feas_m_ve = {'rov': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                          ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                          ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'] ] }

    deck_req = {'deck area': deck_area, 'deck cargo': deck_cargo, 'deck loading': deck_loading}
    
    return feas_e, feas_v, feas_m_pv, feas_m_pe, feas_m_ve, deck_req
 

def external_feas(log_phase, log_phase_id, site, external_protection):
    """external_feas is a function which determines the logistic requirement associated 
    with the logistic phase dealing with the installation of external protection
    """
    # Input collection --------------------------------------------------------
    external_db = external_protection
    mattress_db = external_db[external_db['protection type [-]'] == 'concrete matress']
    rockbag_db = external_db[external_db['protection type [-]'] == 'rock filter bag']

    nr_mattress = mattress_db['protection type [-]'].count()
    nr_rockbag = rockbag_db['protection type [-]'].count()
   
    site = site
    site_external = pd.DataFrame()
    
    snap_to_grid = SnapToGrid(site)
    
    external_coord_x = list(external_db['x coord [m]'])
    external_coord_y = list(external_db['y coord [m]'])
    external_coord_zone = list(external_db['zone [-]'])
    
    for a in range(len(external_coord_x)):
        UTM_elem_x = external_coord_x[a]
        UTM_elem_y = external_coord_y[a]
        UTM_zone = external_coord_zone[a]

        # check the closest point in the site data
        closest_point = snap_to_grid((UTM_elem_x,UTM_elem_y))
        # obtain site data for the coordinates
        site_external = site_external.append( site[ (site['x coord [m]'] == float( closest_point[0] )) & \
                           (site['y coord [m]'] == float( closest_point[1] )) & \
                           (site['zone [-]'] == UTM_zone) ])
    
    depth = site_external['bathymetry [m]'].fillna(0)
    depth = depth.tolist()
    
    # Feasibility functions ---------------------------------------------------
    deck_area = 'matching'
    deck_cargo = 'matching'
    deck_loading = 'matching'
    lifting_cap = 'matching'
    bathymetry = max(depth)
    mattress_tickness = 0.3
    DP = 1
    rov_class = 'Inspection class'

    feas_e = {'rov': [ ['Depth rating [m]', 'sup', bathymetry],
                       ['ROV class [-]', 'equal', rov_class] ],
                       
              'mattress': [ ['Unit thickness [m]', 'sup', mattress_tickness] ] }

    feas_v = {'Crane Vessel': [ ['DP [-]', 'sup', DP] ],

              'Crane Barge':  [ ['DP [-]', 'sup', DP] ],

              'CSV':          [ ['DP [-]', 'sup', DP] ] }
 
    # Matching ----------------------------------------------------------------
    feas_m_pv = {'Crane Vessel': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                 'Crane Barge':  [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                 'CSV':          [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ] }
    feas_m_pe = {}

    feas_m_ve = {'rov': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                          ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                          ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'] ],
                 
                 'mattress': [ ['Unit weight air [t]', 'sup', 'Crane capacity [t]'],
                               ['Unit lenght [m]', 'mul', 'Unit width [m]', 'sup', 'Deck space [m^2]']  ],

                 'rock filter bags': [ ['PI', 'mul', 'Diameter [m]', 'mul', 'Diameter [m]', 'div', '4', 'sup', 'Deck space [m^2]'],
                                       ['Weight [t]', 'sup', 'Crane capacity [t]']] }


    deck_req = {'deck area': deck_area, 'deck cargo': deck_cargo, 'deck loading': deck_loading}


    return feas_e, feas_v, feas_m_pv, feas_m_pe, feas_m_ve, deck_req