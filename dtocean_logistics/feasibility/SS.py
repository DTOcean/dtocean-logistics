# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is part of the characterization step in the WP5 methodology. It 
contains feasibility functions to compute the minimum logistic requirements to 
carry out the different logistic phases. This particular modules includes the
function related to the installation of moorings and foundations.

BETA VERSION NOTES: The current version is limited to an installation strategy
consisting of installation of 1 set of foundations at the time. This will be 
futher developed in the beta version due to October.
"""

from dtocean_logistics.load.snap_2_grid import SnapToGrid


def SS_feas(log_phase, log_phase_id, sub_device, layout, site):
    """ wp4_feas is a function which determines the logistic requirement 
    associated with one logistic phase dealing with the installation of 
    moorings and foundation systems
    
    Parameters
    ----------
    log_phase : Class
     Class of the logistic phase under consideration for assessment
    log_phase_id : str
     string describing the ID of the logistic phase under consideration
    layout : dict
     dictionnary containing all required inputs to WP5 coming from WP2
    MF_outputs : DataFrame
     Panda table containing all required inputs to WP5 coming from WP4
    
    Returns
    -------
    feas_e : dict
     dictionnary containing all logistic requirements associated with every
     equipment type of the logistic phase under consideration
    feas_v : dict
     dictionnary containing all logistic requirements associated with every
     vessel type of the logistic phase under consideration
    """

    snap_to_grid = SnapToGrid(site)

    support = sub_device.ix['D'] # corresponds to 'D'

    length_ss = support['length [m]']
    width_ss = support['width [m]']
    drymass_ss = support['dry mass [kg]']/1000.0

    device_depth = []
    for indx_dev, row in layout.iterrows():
        UTM_elem_x = layout['x coord [m]'].ix[indx_dev]
        UTM_elem_y = layout['y coord [m]'].ix[indx_dev]
        UTM_zone = layout['zone [-]'].ix[indx_dev]
        # check the closest point in the site data
        closest_point = snap_to_grid((UTM_elem_x,UTM_elem_y))
        # obtain site data for the coordinates
        site_coord = site[ (site['x coord [m]'] == closest_point[0]) & \
                           (site['y coord [m]'] == closest_point[1]) & \
                           (site['zone [-]'] == UTM_zone) ]
        device_depth.append( site_coord['bathymetry [m]'].iloc[0] )


    area_s = length_ss*width_ss
    load_s = drymass_ss/area_s
    cargo_s = drymass_ss

    deck_loading = load_s  # t/m^2!
    deck_cargo = cargo_s  # t!
    deck_area = area_s  # m^2

    max_depth = max(device_depth)

    # Equipment and vessel feasiblity:
    feas_e = {'rov': [['Depth rating [m]', 'sup', max_depth]]}

    feas_v = {'Crane Barge': [['Deck loading [t/m^2]', 'sup', deck_loading],
                       ['Max. cargo [t]', 'sup', deck_cargo],
                       ['Deck space [m^2]', 'sup', deck_area],
                       ['Crane capacity [t]', 'sup', deck_cargo],
                       ['DP [-]', 'sup', 1]
                       # ['ROV inspection [yes/no]', 'equal', 'yes'],
                       # ['ROV workclass [yes/no]', 'equal', 'yes']
                              ],
              'Crane Vessel': [['Deck loading [t/m^2]', 'sup', deck_loading],
                       ['Max. cargo [t]', 'sup', deck_cargo],
                       ['Deck space [m^2]', 'sup', deck_area],
                       ['Crane capacity [t]', 'sup', deck_cargo],
                       ['DP [-]', 'sup', 1]
                       # ['ROV inspection [yes/no]', 'equal', 'yes'],
                       # ['ROV workclass [yes/no]', 'equal', 'yes']
                               ],
              'CSV': [['Deck loading [t/m^2]', 'sup', deck_loading],
                       ['Max. cargo [t]', 'sup', deck_cargo],
                       ['Deck space [m^2]', 'sup', deck_area],
                       ['Crane capacity [t]', 'sup', deck_cargo],
                       ['DP [-]', 'sup', 1]
                       # ['ROV inspection [yes/no]', 'equal', 'yes'],
                       # ['ROV workclass [yes/no]', 'equal', 'yes']
                      ],
              'JUP Vessel': [['Deck loading [t/m^2]', 'sup', deck_loading],
                       ['Max. cargo [t]', 'sup', deck_cargo],
                       ['Deck space [m^2]', 'sup', deck_area],
                       ['Crane capacity [t]', 'sup', deck_cargo],
                       ['DP [-]', 'sup', 1]],
              'JUP Barge': [['Deck loading [t/m^2]', 'sup', deck_loading],
                       ['Max. cargo [t]', 'sup', deck_cargo],
                       ['Deck space [m^2]', 'sup', deck_area],
                       ['Crane capacity [t]', 'sup', deck_cargo],
                       ['DP [-]', 'sup', 1],
                       # ['ROV inspection [yes/no]', 'equal', 'yes'],
                       # ['ROV workclass [yes/no]', 'equal', 'yes'],
                       ['JackUp max payload [t]', 'sup', deck_cargo],
                       ['JackUp max water depth [m]', 'sup', max_depth]]}

    # Matching:
    feas_m_pv = {'Crane Barge': [['Beam [m]', 'sup', 'Entrance width [m]'],
                      ['Length [m]', 'sup', 'Terminal length [m]'],
                      ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                 'Crane Vessel': [['Beam [m]', 'sup', 'Entrance width [m]'],
                      ['Length [m]', 'sup', 'Terminal length [m]'],
                      ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                 'CSV': [['Beam [m]', 'sup', 'Entrance width [m]'],
                      ['Length [m]', 'sup', 'Terminal length [m]'],
                      ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                 'JUP Vessel': [['Beam [m]', 'sup', 'Entrance width [m]'],
                      ['Length [m]', 'sup', 'Terminal length [m]'],
                      ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                 'JUP Barge': [['Beam [m]', 'sup', 'Entrance width [m]'],
                      ['Length [m]', 'sup', 'Terminal length [m]'],
                      ['Max. draft [m]', 'sup', 'Terminal draught [m]'],
                      ['Jacking capability [yes/no]','equal','yes']],
                 'Tugboat': [['Beam [m]', 'sup', 'Entrance width [m]'],
                      ['Length [m]', 'sup', 'Terminal length [m]'],
                      ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                 'Multicat': [['Beam [m]', 'sup', 'Entrance width [m]'],
                      ['Length [m]', 'sup', 'Terminal length [m]'],
                      ['Max. draft [m]', 'sup', 'Terminal draught [m]']]}

    feas_m_pe = {}

    feas_m_ve = {'rov': [['Length [m]',
                          'mul',
                          'Width [m]',
                          'plus',
                          'AE footprint [m^2]',
                          'sup',
                          'Deck space [m^2]'],
                         ['Weight [t]',
                          'plus',
                          'AE weight [t]',
                          'sup',
                          'Max. cargo [t]'],
                         ['Weight [t]',
                          'div',
                          'Width [m]',
                          'div',
                          'Length [m]',
                          'sup',
                          'Deck loading [t/m^2]'],
                         ['Weight [t]',
                          'sup',
                          'AH winch rated pull [t]']]}


    deck_req = {'deck area': deck_area,
                'deck cargo': deck_cargo,
                'deck loading': deck_loading}
        
    return feas_e, feas_v, feas_m_pv, feas_m_pe, feas_m_ve, deck_req