# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is part of the characterization step in the WP5 methodology. It
contains feasibility functions to compute the minimum logistic requirements to
carry out the different logistic phases. This particular modules includes the
function related to the installation of devices.

BETA VERSION NOTES: This function is not being used in the current version.
"""

def user_inputs_feas(log_phase, log_phase_id, user_inputs):
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

    # dev_type = user_inputs['device']['type [-]']
    assembly_method = user_inputs['device']['assembly strategy [-]'].ix[0]
    # trans_methd = user_inputs['device']['transportation method [-]']
    # loadout_methd = user_inputs['device']['load out [-]']
    max_bathymetry = max(user_inputs['site']['bathymetry [m]']) #TO BE DEVELOPED - ASSOCIATION WITH SITE DB IS NEEDED

    if assembly_method == '([A,B,C,D])': # all devices assumed the same
        deck_area = user_inputs['device']['length [m]'].ix[0] * user_inputs['device']['width [m]'].ix[0]
        deck_cargo = user_inputs['device']['dry mass [kg]'].ix[0]/1000
        deck_loading = user_inputs['device']['dry mass [kg]'].ix[0] / (user_inputs['device']['length [m]'].ix[0] * user_inputs['device']['width [m]'].ix[0])

    elif assembly_method == '([A,B,C],D)':
        deck_area = max(user_inputs['sub_device']['length [m]']['A':'C'] * user_inputs['sub_device']['width [m]']['A':'C'])
        deck_cargo = user_inputs['sub_device']['dry mass [kg]']['A':'C'].sum()/1000
        deck_loading = max(user_inputs['sub_device']['dry mass [kg]']['A':'C'] / (1000 * user_inputs['sub_device']['length [m]']['A':'C'] * user_inputs['sub_device']['width [m]']['A':'C']))

    # Equipment and vessel feasiblity ---------------------------------------
    # these should be dictionaries, with the keys being the name of the vessels
    # and the requirements always a list of lists e.g. 'vessel': [ ['parameter', 'evaluation', value] ]

    feas_e = {'rov': [ ['Depth rating [m]', 'sup', max_bathymetry],
                       ['ROV class [-]', 'equal', 'Inspection class']
                       ]}

    feas_v = {'JUP Vessel': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['Deck space [m^2]', 'sup', deck_area],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['DP [-]', 'sup', 1],
                           ['JackUp max payload [t]', 'sup', deck_cargo],
                           ['JackUp max water depth [m]', 'sup', max_bathymetry]],

                  'JUP Barge': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['Deck space [m^2]', 'sup', deck_area],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['DP [-]', 'sup', 1],
                           ['JackUp max payload [t]', 'sup', deck_cargo],
                           ['JackUp max water depth [m]', 'sup', max_bathymetry]],

                  'CSV': [['Deck loading [t/m^2]', 'sup', deck_loading],
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

                  'AHTS': [['Bollard pull [t]', 'sup', deck_cargo]]}

    # Matching

    feas_m_pv = {'JUP Vessel': [['Beam [m]', 'sup', 'Entrance width [m]'],
                      ['Length [m]', 'sup', 'Terminal length [m]'],
                      ['Max. draft [m]', 'sup', 'Terminal draught [m]'],
                      ['Jacking capability [yes/no]','equal','yes']],
                 'CSV': [['Beam [m]', 'sup', 'Entrance width [m]'],
                      ['Length [m]', 'sup', 'Terminal length [m]'],
                      ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                 'JUP Barge': [['Beam [m]', 'sup', 'Entrance width [m]'],
                      ['Length [m]', 'sup', 'Terminal length [m]'],
                      ['Max. draft [m]', 'sup', 'Terminal draught [m]'],
                      ['Jacking capability [yes/no]','equal','yes']],
                 'Tugboat': [['Beam [m]', 'sup', 'Entrance width [m]'],
                      ['Length [m]', 'sup', 'Terminal length [m]'],
                      ['Max. draft [m]', 'sup', 'Terminal draught [m]']]}

#    feas_m_pe = {'rov': [['length [m]', 'mul', 'width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Terminal area [m^2]'],
#              ['Weight [t]', 'plus', 'AE weight [t]', 'div', 'Length [m]', 'mul', 'Width [m]', 'sup', 'Terminal load bearing [t/m^2]']]}

    feas_m_ve = {'rov': [['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
              ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
              ['Weight [t]', 'plus', 'AE weight [t]', 'div', 'Length [m]', 'mul', 'Width [m]', 'sup', 'Deck loading [t/m^2]'],
                  ['Weight [t]', 'sup', 'AH winch rated pull [t]']]}


    return feas_e, feas_v, feas_m_pv, feas_m_ve
