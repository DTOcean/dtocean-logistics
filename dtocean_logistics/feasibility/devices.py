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
This module is part of the characterization step in the WP5 methodology. It
contains feasibility functions to compute the minimum logistic requirements to
carry out the different logistic phases. This particular modules includes the
function related to the installation of devices.

.. moduleauthor:: Boris Teillant <boris.teillant@wavec.org>
.. moduleauthor:: Paulo Chainho <paulo@wavec.org>
.. moduleauthor:: Mathew Topper <mathew.topper@dataonlygreater.com>
"""

from dtocean_logistics.load.snap_2_grid import SnapToGrid


def devices_feas(log_phase, log_phase_id, site, device, sub_device, layout):
    """wp1_feas is a function which determines the logistic requirement
    associated with one logistic phase dealing with the installation of devices

    Parameters
    ----------
    log_phase : Class
     Class of the logistic phase under consideration for assessment
    log_phase_id : str
     string describing the ID of the logistic phase under consideration
    user_inputs : dict
     dictionnary containing all required inputs to WP5 coming from WP1/end-user

    Returns
    -------
    feas_e : dict
     dictionnary containing all logistic requirements associated with every
     equipment type of the logistic phase under consideration
    feas_v : dict
     dictionnary containing all logistic requirements associated with every
     vessel type of the logistic phase under consideration
    """
    # Input collection --------------------------------------------------------
    device_length = device['length [m]'].iloc[0]
    device_width = device['width [m]'].iloc[0]
    device_mass = device['dry mass [kg]'].iloc[0]/1000.0

    sub_device_length = sub_device['length [m]']
    sub_device_width = sub_device['width [m]']
    sub_device_mass = sub_device['dry mass [kg]']/1000.0
    
    tow_force = device['bollard pull [t]'].iloc[0]
    assembly_method = device['assembly strategy [-]'].iloc[0]
    trans_methd = device['transportation method [-]'].iloc[0]
    loadout_methd = device['load out [-]']
    
    snap_to_grid = SnapToGrid(site)

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
    max_bathymetry = max(device_depth)

    # Obtain deck requirements
    if assembly_method == '([A,B,C,D])': # all devices assumed the same
        deck_area = device_length * device_width
        deck_cargo = device_mass
        deck_loading = device_mass / (device_length * device_width)

    elif assembly_method == '([A,B,C],D)':
        deck_area = max(sub_device_length['A':'C'] * sub_device_width['A':'C'])
        deck_cargo = sub_device_mass['A':'C'].sum()
        deck_loading = max(sub_device_mass['A':'C']['A':'C'] /
                               (sub_device_length['A':'C'] *
                                                sub_device_width['A':'C']))
    
    # Obtain tow requirements
    if trans_methd == 'deck': # all devices assumed the same
        bollard_pull = 0.0
        
    elif trans_methd == 'tow': # all devices assumed the same
        bollard_pull = tow_force

    # Equipment and vessel feasiblity ---------------------------------------
    # these should be dictionaries, with the keys being the name of the vessels
    # and the requirements always a list of lists e.g.:
    #     'vessel': [['parameter', 'evaluation', value]]

    feas_e = {'rov': [['Depth rating [m]', 'sup', max_bathymetry],
                      ['ROV class [-]', 'equal', 'Inspection class']]}

    feas_v = {'JUP Vessel': [['Deck loading [t/m^2]', 'sup', deck_loading],
                             ['Max. cargo [t]', 'sup', deck_cargo],
                             ['Deck space [m^2]', 'sup', deck_area],
                             ['Crane capacity [t]', 'sup', deck_cargo],
                             ['DP [-]', 'sup', 1],
                             ['JackUp max payload [t]', 'sup', deck_cargo],
                             ['JackUp max water depth [m]',
                              'sup',
                              max_bathymetry]],

              'JUP Barge': [['Deck loading [t/m^2]', 'sup', deck_loading],
                            ['Max. cargo [t]', 'sup', deck_cargo],
                            ['Deck space [m^2]', 'sup', deck_area],
                            ['Crane capacity [t]', 'sup', deck_cargo],
                            ['DP [-]', 'sup', 1],
                            ['JackUp max payload [t]', 'sup', deck_cargo],
                            ['JackUp max water depth [m]',
                             'sup',
                             max_bathymetry]], 

              'CSV':       [['Deck loading [t/m^2]', 'sup', deck_loading],
                            ['Max. cargo [t]', 'sup', deck_cargo],
                            ['Deck space [m^2]', 'sup', deck_area],
                            ['Crane capacity [t]', 'sup', deck_cargo],
                            ['DP [-]', 'sup', 1]],

              'Crane Barge': [['Deck loading [t/m^2]', 'sup', deck_loading],
                              ['Max. cargo [t]', 'sup', deck_cargo],
                              ['Deck space [m^2]', 'sup', deck_area],
                              ['Crane capacity [t]', 'sup', deck_cargo],
                              ['DP [-]', 'sup', 1]],

              'Crane Vessel': [['Deck loading [t/m^2]', 'sup', deck_loading],
                               ['Max. cargo [t]', 'sup', deck_cargo],
                               ['Deck space [m^2]', 'sup', deck_area],
                               ['Crane capacity [t]', 'sup', deck_cargo],
                               ['DP [-]', 'sup', 1]],

              'AHTS': [['Bollard pull [t]', 'sup', bollard_pull]]}

    # Matching

    feas_m_pv = {'JUP Vessel': [['Beam [m]', 'sup', 'Entrance width [m]'],
                                ['Length [m]', 'sup', 'Terminal length [m]'],
                                ['Max. draft [m]',
                                 'sup',
                                 'Terminal draught [m]']
                              # ['Jacking capability [yes/no]','equal','yes']
                                ],
                 'CSV':       [['Beam [m]', 'sup', 'Entrance width [m]'],
                               ['Length [m]', 'sup', 'Terminal length [m]'],
                               ['Max. draft [m]',
                                'sup',
                                'Terminal draught [m]']],

                 'JUP Barge': [['Beam [m]', 'sup', 'Entrance width [m]'],
                               ['Length [m]', 'sup', 'Terminal length [m]'],
                               ['Max. draft [m]',
                                'sup',
                                'Terminal draught [m]']
                              # ['Jacking capability [yes/no]','equal','yes']
                               ],
                 'Tugboat': [['Beam [m]', 'sup', 'Entrance width [m]'],
                             ['Length [m]', 'sup', 'Terminal length [m]'],
                             ['Max. draft [m]',
                              'sup',
                              'Terminal draught [m]']]}

    feas_m_pe = {'rov': [['length [m]',
                          'mul',
                          'width [m]',
                          'plus',
                          'AE footprint [m^2]',
                          'sup',
                          'Terminal area [m^2]'],
                         ['AE weight [t]',
                          'div',
                          'AE footprint [m^2]',
                          'sup',
                          'Deck loading [t/m^2]']]}

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
                         ['AE weight [t]',
                          'div',
                          'AE footprint [m^2]',
                          'sup',
                          'Deck loading [t/m^2]'],
                         ['Weight [t]', 'sup', 'AH winch rated pull [t]']]}


    deck_req = {'deck area': deck_area,
                'deck cargo': deck_cargo,
                'deck loading': deck_loading}
    
    return feas_e, feas_v, feas_m_pv, feas_m_pe, feas_m_ve, deck_req
