# -*- coding: utf-8 -*-

#    Copyright (C) 2016 Boris Teillant, Paulo Chainho
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
function related to the installation of moorings and foundations.

BETA VERSION NOTES: The current version is limited to an installation strategy
consisting of installation of 1 set of foundations at the time. This will be 
futher developed in the beta version due to October.

.. moduleauthor:: Boris Teillant <boris.teillant@wavec.org>
.. moduleauthor:: Paulo Chainho <paulo@wavec.org>
"""

def MF_feas(log_phase, log_phase_id, layout, line, foundation):
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

    if log_phase_id == 'Driven':
        foundation_db = foundation
        found_db = foundation_db[foundation_db['type [-]'] == 'pile foundation']
        found_db = found_db.append(foundation_db[foundation_db['type [-]'] == 'pile anchor'])
    elif log_phase_id == 'Gravity':
        foundation_db = foundation
        found_db = foundation_db[foundation_db['type [-]'] == 'gravity foundation']
        found_db = found_db.append(foundation_db[foundation_db['type [-]'] == 'gravity anchor'])
        found_db = found_db.append(foundation_db[foundation_db['type [-]'] == 'shallow foundation'])
        found_db = found_db.append(foundation_db[foundation_db['type [-]'] == 'shallow anchor'])
    elif log_phase_id == 'M_direct':
        foundation_db = foundation
        found_db = foundation_db[foundation_db['type [-]'] == 'direct-embedment anchor']
    elif log_phase_id == 'M_drag':
        foundation_db = foundation
        found_db = foundation_db[foundation_db['type [-]'] == 'drag-embedment anchor']
    elif log_phase_id == 'M_pile':
        foundation_db = foundation
        found_db = foundation_db[foundation_db['type [-]'] == 'pile anchor']
    elif log_phase_id == 'M_suction':
        foundation_db = foundation
        found_db = foundation_db[foundation_db['type [-]'] == 'suction caisson anchor']

    line_db = line

    num_found = len(found_db)
    num_line = len(line_db)

    diam_u_f = []  # list of diameter of each foundation per unit
    load_u_f = []  # list of loading due to each foundation per unit
    cargo_u_f = []  # list of loading due to each foundation per unit
    area_u_f = []  # list of area occupied by each foundation per unit
    depth_u_f = []  # list of area occupied by each foundation per unit
    moo_line_len_u_f = []  # list of area occupied by each foundation per unit
    moo_mass_u_f = []  # list of area occupied by each foundation per unit

    for ind_found, row in found_db.iterrows():
        load_u_f.append( found_db['dry mass [kg]'].ix[ind_found] / (found_db['length [m]'].ix[ind_found] * found_db['width [m]'].ix[ind_found]) )
        cargo_u_f.append( found_db['dry mass [kg]'].ix[ind_found] )
        area_u_f.append( found_db['length [m]'].ix[ind_found] * found_db['width [m]'].ix[ind_found] )
        diam_u_f.append( found_db['length [m]'].ix[ind_found] )
        depth_u_f.append( found_db['installation depth [m]'].ix[ind_found] )

    for ind_line, row in line_db.iterrows():
        moo_line_len_u_f.append( line_db['length [m]'].ix[ind_line] )
        moo_mass_u_f.append( line_db['dry mass [kg]'].ix[ind_line] + line_db['dry mass [kg]'].ix[ind_line] )

    if num_found>0:
        deck_loading = max(load_u_f)/1000.0  # t/m^2!
        deck_cargo = max(cargo_u_f)/1000.0  # t!
        deck_area = max(area_u_f)  # m^2
        sleeve_diam = max(diam_u_f)  # m
        max_depth = max(depth_u_f)  # m
    else:
        deck_loading = 0
        deck_cargo = 0
        deck_area = 0
        sleeve_diam = 0
        max_depth = 0

    if num_line>0:
        max_linelength = max(moo_line_len_u_f)  # m
        max_moomass = max(moo_mass_u_f)/1000.0  # t!
    else:
        max_linelength = 0
        max_moomass = 0


    # ***********************************************************************************************************************
    if log_phase_id == 'M_drag' or log_phase_id == 'M_direct' or log_phase_id == 'M_suction' or log_phase_id == 'M_pile': # ??!?!?!?!?!??!?!?!?!?!?!?!?!?!?!?

        # Equipment and vessel feasiblity

        feas_e = {'rov': [['Depth rating [m]', 'sup', max_depth]]}

        feas_v = {'Multicat': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['AH winch rated pull [t]', 'sup', max_moomass],
                           ['AH drum capacity [m]', 'sup', max_linelength],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['AH drum capacity [m]', 'sup', max_depth],
                           ['Deck space [m^2]', 'sup', deck_area],
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes']
                               ],
                  'AHTS': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['AH winch rated pull [t]', 'sup', max_moomass],
                           ['AH drum capacity [m]', 'sup', max_linelength],
                           ['Deck space [m^2]', 'sup', deck_area],
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes']
                           ]}

        # Matching

        feas_m_pv = {'Multicat': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                     'AHTS': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']]}

        # feas_m_pe = {'rov': [['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Terminal area [m^2]'],
        #           ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max gantry crane lift capacity [t]'],
        #           ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max tower crane lift capacity [t]'],
        #           ['AE weight [t]', 'div', 'AE footprint [m^2]', 'sup', 'Deck loading [t/m^2]']]}
        feas_m_pe = {}

        feas_m_ve = {'rov': [['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                  ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                  ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'],
                      ['Weight [t]', 'sup', 'AH winch rated pull [t]']]}



    # ***********************************************************************************************************************
    elif log_phase_id == 'Gravity':

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
                  'Barge': [['Deck loading [t/m^2]', 'sup', deck_loading],
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
                     'Barge': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                     'JUP Barge': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]'],
                          ['Jacking capability [yes/no]','equal','Yes']],
                     'Tugboat': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                     'Multicat': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']]}

        # feas_m_pe = {'rov': [['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Terminal area [m^2]'],
        #           ['AE weight [t]', 'div', 'AE footprint [m^2]', 'sup', 'Deck loading [t/m^2]']]}
        feas_m_pe = {}

        feas_m_ve = {'rov': [['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                  ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                  ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'],
                      ['Weight [t]', 'sup', 'AH winch rated pull [t]']]}




    # ***********************************************************************************************************************
    elif log_phase_id == 'Driven':

        # Equipment and vessel feasiblity

        feas_e = {'hammer': [['Depth rating [m]', 'sup', max_depth],
                             ['Min pile diameter [mm]', 'inf', sleeve_diam*1000.0],
                             ['Max pile diameter [mm]', 'sup', sleeve_diam*1000.0]],
                  'drilling rigs': [['Max water depth [m]', 'sup', max_depth],
                                    ['Drilling diameter range [m]', 'sup', sleeve_diam],
                                    ['Max drilling depth [m]', 'sup', max_depth]],
                  'vibro driver': [['Max pile weight [t]', 'sup', max_moomass],
                                   ['Min pile diameter [mm]', 'inf', sleeve_diam*1000.0],
                                   ['Max pile diameter [mm]', 'sup', sleeve_diam*1000.0]],
                  'rov': [['Depth rating [m]', 'sup', max_depth]]}

        feas_v = {'JUP Vessel': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['Deck space [m^2]', 'sup', deck_area],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['DP [-]', 'sup', 1],
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes'],
                           ['JackUp max payload [t]', 'sup', deck_cargo],
                           ['JackUp max water depth [m]', 'sup', max_depth]],
                  'CSV': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['Deck space [m^2]', 'sup', deck_area],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['DP [-]', 'sup', 1],
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes']
                          ],
                  'JUP Barge': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['Deck space [m^2]', 'sup', deck_area],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['DP [-]', 'sup', 1],
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes'],
                           ['JackUp max payload [t]', 'sup', deck_cargo],
                           ['JackUp max water depth [m]', 'sup', max_depth]]}

        # Matching

        feas_m_pv = {'JUP Vessel': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]'],
                          ['Jacking capability [yes/no]','equal','Yes']],
                     'CSV': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                     'JUP Barge': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]'],
                          ['Jacking capability [yes/no]','equal','Yes']],
                     'Tugboat': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']]}

        # feas_m_pe = {'rov': [['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Terminal area [m^2]'],
        #           ['AE weight [t]', 'div', 'AE footprint [m^2]', 'sup', 'Deck loading [t/m^2]']]}
        feas_m_pe = {}

        feas_m_ve = {'rov': [['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                             ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                             ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'],
                             ['Weight [t]', 'sup', 'AH winch rated pull [t]']],

                     'hammer': [['AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                                ['Weight in air [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                                ['Weight in air [t]', 'sup', 'Crane capacity [t]']],

                     'drilling rigs': [['Diameter [m]', 'mul', 'Length [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                                       ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                                       ['Weight [t]', 'sup', 'Crane capacity [t]']],

                     'vibro driver': [['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                                      ['Vibro driver weight [m]', 'plus', 'Clamp weight [m]','plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                                      ['Vibro driver weight [m]', 'plus', 'Clamp weight [m]', 'sup', 'Crane capacity [t]']]}




    deck_req = {'deck area': deck_area, 'deck cargo': deck_cargo, 'deck loading': deck_loading}
    return feas_e, feas_v, feas_m_pv, feas_m_pe, feas_m_ve, deck_req