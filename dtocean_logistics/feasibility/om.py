# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is part of the characterization step in the WP5 methodology. It
contains feasibility functions to compute the minimum logistic requirements to
carry out the different logistic phases. This particular modules includes the
function related to the O&M repair actions.

BETA VERSION NOTES: The current version is limited to one logistic phase, the
repair action related to offshore inspection and maintenance activities.
"""

import numpy as np

import logging
module_logger = logging.getLogger(__name__)

def om_feas(log_phase, log_phase_id, OM_outputs, user_inputs, electrical_outputs, MF_outputs):
    """ om_feas is a function which determines the logistic requirement
    associated with the logistic phases related to the O&M

    Parameters
    ----------
    log_phase : Class
     Class of the logistic phase under consideration for assessment
    log_phase_id : str
     string describing the ID of the logistic phase under consideration
    wp6_outputs : dict
     dictionnary containing all required inputs to WP5 coming from WP6

    Returns
    -------
    feas_e : dict
     dictionnary containing all logistic requirements associated with every
     equipment type of the logistic phase under consideration
    feas_v : dict
     dictionnary containing all logistic requirements associated with every
     vessel type of the logistic phase under consideration
    """

    ''' LogPhase LpM1: Inspection or on-site maintenance of topside elements '''

    if log_phase_id == 'LpM1':

        # Input collection
        lenght_SP = OM_outputs['sp_length [m]'].fillna(0)
        width_SP = OM_outputs['sp_width [m]'].fillna(0)
        dry_mass_SP = OM_outputs['sp_dry_mass [kg]'].fillna(0)/1000.0
        nr_technician = OM_outputs['technician [-]'].fillna(0)

        # Feasibility functions
        deck_area = max(lenght_SP*width_SP)
        deck_cargo = max(dry_mass_SP)
        deck_loading = max(dry_mass_SP/(lenght_SP*width_SP))
        ext_personnel = max(nr_technician)

        feas_e = {}
        feas_v = {'CTV':        [['Deck loading [t/m^2]', 'sup', deck_loading],
                                 ['Deck space [m^2]', 'sup', deck_area],
                                 ['Max. cargo [t]', 'sup', deck_cargo],
                                 ['External  personnel [-]', 'sup', ext_personnel]],

                  'Multicat':   [['Deck loading [t/m^2]', 'sup', deck_loading],
                                 ['Deck space [m^2]', 'sup', deck_area],
                                 ['Max. cargo [t]', 'sup', deck_cargo],
                                 ['External  personnel [-]', 'sup', ext_personnel]],

                  'Helicopter': [['Deck loading [t/m^2]', 'sup', deck_loading],
                                 ['Deck space [m^2]', 'sup', deck_area],
                                 ['Max. cargo [t]', 'sup', deck_cargo],
                                 ['External  personnel [-]', 'sup', ext_personnel]]

                                 }

        # Matching
        feas_m_pv = {'CTV': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                              ['Length [m]', 'sup', 'Terminal length [m]'],
                              ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'Multicat': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ]
                        }

        feas_m_pe = {}

        feas_m_ve = {}


    ''' LogPhase LpM2: Inspection or on-site maintenance of elements at water depth<30m '''

    if log_phase_id == 'LpM2':

        # Input collection
        lenght_SP = OM_outputs['sp_length [m]'].fillna(0)
        width_SP = OM_outputs['sp_width [m]'].fillna(0)
        dry_mass_SP = OM_outputs['sp_dry_mass [kg]'].fillna(0)/1000.0
        nr_technician = OM_outputs['technician [-]'].fillna(0)
        depth = OM_outputs['depth [m]'].fillna(0)

        # Feasibility functions
        deck_area = max(lenght_SP*width_SP)
        deck_cargo = max(dry_mass_SP)
        deck_loading = max(dry_mass_SP/(lenght_SP*width_SP))
        ext_personnel = max(nr_technician)
        bathymetry = max(depth)

        feas_e = {'divers': [ ['Max operating depth [m]', 'sup', bathymetry] ]

                           }

        feas_v = {'CTV':        [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                  ['Deck space [m^2]', 'sup', deck_area],
                                  ['Max. cargo [t]', 'sup', deck_cargo],
                                  ['External  personnel [-]', 'sup', ext_personnel] ],

                  'Multicat':   [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                  ['Deck space [m^2]', 'sup', deck_area],
                                  ['Max. cargo [t]', 'sup', deck_cargo],
                                  ['External  personnel [-]', 'sup', ext_personnel] ],

                  'CSV':        [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                  ['Deck space [m^2]', 'sup', deck_area],
                                  ['Max. cargo [t]', 'sup', deck_cargo],
                                  ['External  personnel [-]', 'sup', ext_personnel] ]
                                 }


        # Matching
        feas_m_pv = {'CTV': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                              ['Length [m]', 'sup', 'Terminal length [m]'],
                              ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'Multicat': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'CSV':      [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ]
                        }

        feas_m_pe = {}

        feas_m_ve = {'divers': [ ['Deployment eq. footprint [m^2]', 'sup', 'Deck space [m^2]'],
                                 ['Deployment eq. weight [t]', 'sup', 'Max. cargo [t]'] ]
                                }

    ''' LogPhase LpM3: Inspection or on-site maintenance of elements at water depth>30m '''

    if log_phase_id == 'LpM3':

        # Input collection
        lenght_SP = OM_outputs['sp_length [m]'].fillna(0)
        width_SP = OM_outputs['sp_width [m]'].fillna(0)
        dry_mass_SP = OM_outputs['sp_dry_mass [kg]'].fillna(0)/1000.0
        nr_technician = OM_outputs['technician [-]'].fillna(0)
        depth = OM_outputs['depth [m]'].fillna(0)
        om_index = OM_outputs.index.values[0]        
        om_id = OM_outputs['ID [-]'].ix[om_index]

        # Feasibility functions
        deck_area = max(lenght_SP*width_SP)
        deck_cargo = max(dry_mass_SP)
        deck_loading = max(dry_mass_SP/(lenght_SP*width_SP))
        ext_personnel = max(nr_technician)
        bathymetry = max(depth)
        if om_id == 'Insp5':
            rov_class = 'Workclass'
        elif om_id == 'Insp4' or om_id == 'MoS4':
            rov_class = 'Inspection class'


        feas_e = {'rov': [ ['Depth rating [m]', 'sup', bathymetry],
                           ['ROV class [-]', 'equal', rov_class] ]
                         }

        feas_v = {'CTV':        [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                  ['Deck space [m^2]', 'sup', deck_area],
                                  ['Max. cargo [t]', 'sup', deck_cargo],
                                  ['External  personnel [-]', 'sup', ext_personnel] ],

                  'Multicat':   [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                  ['Deck space [m^2]', 'sup', deck_area],
                                  ['Max. cargo [t]', 'sup', deck_cargo],
                                  ['External  personnel [-]', 'sup', ext_personnel] ],

                  'CSV':        [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                  ['Deck space [m^2]', 'sup', deck_area],
                                  ['Max. cargo [t]', 'sup', deck_cargo],
                                  ['External  personnel [-]', 'sup', ext_personnel] ]
                                 }

        # Matching
        feas_m_pv = {'CTV':      [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'Multicat': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'CSV':      [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ]
                        }

        feas_m_pe = {}

        feas_m_ve = {'rov': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                              ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                              ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'] ]
                             }

    ''' LogPhase LpM4: Inspection or on-site maintenance on the mooring systems '''

    if log_phase_id == 'LpM4':

        # Input collection
        lenght_SP = OM_outputs['sp_length [m]'].fillna(0)
        width_SP = OM_outputs['sp_width [m]'].fillna(0)
        dry_mass_SP = OM_outputs['sp_dry_mass [kg]'].fillna(0)/1000.0
        nr_technician = OM_outputs['technician [-]'].fillna(0)
        depth = OM_outputs['depth [m]'].fillna(0)
        om_index = OM_outputs.index.values[0]        
        om_id = OM_outputs['ID [-]'].ix[om_index]

        # Feasibility functions 
        deck_area = max(lenght_SP*width_SP)
        deck_cargo = max(dry_mass_SP)
        deck_loading = max(dry_mass_SP/(lenght_SP*width_SP))
        ext_personnel = max(nr_technician)
        bathymetry = max(depth)
        rov_class = 'Workclass'

        feas_e = {'rov': [ ['Depth rating [m]', 'sup', bathymetry],
                           ['ROV class [-]', 'equal', rov_class] ]
                         }

        feas_v = {'AHTS':       [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                  ['Deck space [m^2]', 'sup', deck_area],
                                  ['Max. cargo [t]', 'sup', deck_cargo],
                                  ['External  personnel [-]', 'sup', ext_personnel] ],

                  'Multicat':   [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                  ['Deck space [m^2]', 'sup', deck_area],
                                  ['Max. cargo [t]', 'sup', deck_cargo],
                                  ['External  personnel [-]', 'sup', ext_personnel] ]
                    }

        # Matching
        feas_m_pv = {'AHTS': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                               ['Length [m]', 'sup', 'Terminal length [m]'],
                               ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'Multicat': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ]
                        }

        feas_m_pe = {}

        feas_m_ve = {'rov': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                              ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                              ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'] ]
                             }

    ''' LogPhase LpM5: Inspection or on-site maintenance on on static power cables '''

    if log_phase_id == 'LpM5':

        # Input collection
        lenght_SP = OM_outputs['sp_length [m]'].fillna(0)
        width_SP = OM_outputs['sp_width [m]'].fillna(0)
        dry_mass_SP = OM_outputs['sp_dry_mass [kg]'].fillna(0)/1000.0
        nr_technician = OM_outputs['technician [-]'].fillna(0)
        depth = OM_outputs['depth [m]'].fillna(0)

        # Feasibility functions
        deck_area = 0
        deck_cargo = max(dry_mass_SP)
        deck_loading = 0
        ext_personnel = max(nr_technician)
        bathymetry = max(depth)
        rov_class = 'Workclass'

        feas_e = {'rov': [ ['Depth rating [m]', 'sup', bathymetry],
                           ['ROV class [-]', 'equal', rov_class] ]
                         }

        feas_v = {'CLV': [ ['Turntable loading [t]', 'sup', deck_cargo],
                           ['Cable splice [yes/no]', 'equal', 'yes'] ]
                                }

        # Matching
        feas_m_pv = {'CLV': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                              ['Length [m]', 'sup', 'Terminal length [m]'],
                              ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ]
                        }

        feas_m_pe = {}

        feas_m_ve = {'rov': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                              ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                              ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'] ]
                             }

    ''' LogPhase LpM6: Onshore maintenance of devices or array sub-component - on deck transport '''

    if log_phase_id == 'LpM6':

        # Input collection
        lenght_SP = OM_outputs['sp_length [m]'].fillna(0)
        width_SP = OM_outputs['sp_width [m]'].fillna(0)
        dry_mass_SP = OM_outputs['sp_dry_mass [kg]'].fillna(0)/1000.0
        nr_technician = OM_outputs['technician [-]'].fillna(0)
        depth = OM_outputs['depth [m]'].fillna(0)
        
        element_type = OM_outputs['element_type [-]']
        element_subtype = OM_outputs['element_subtype [-]']
        element_id = OM_outputs['element_ID [-]']
       
        if (element_type == 'device').any():
            
            device_df = user_inputs['device']
            device_index = device_df.index.values[0]
            sub_device_df = user_inputs['sub_device']
       
            if device_df['assembly strategy [-]'][device_index] == '([A,B,C,D])':
       
                element_length = device_df['length [m]']
                element_width = device_df['width [m]']
                element_mass = device_df['dry mass [kg]']/1000.0
       
            elif device_df['assembly strategy [-]'][device_index] == '([A,B,C],D)':
       
                element_length = sub_device_df['length [m]']['A':'C']
                element_width = sub_device_df['width [m]']['A':'C']
                element_mass = sub_device_df['dry mass [kg]']['A':'C']/1000.0
       
            else:
                msg = ("Device assembly strategy {} not supported.Only "
                       "'([A,B,C,D])' or '([A,B,C],D)' accepted.".format(
                       device_df['assembly strategy [-]'][device_index]))
                module_logger.warning(msg)

        # Feasibility functions
        deck_area = max(lenght_SP*width_SP) + max(element_length*element_width) 
        deck_cargo = max(dry_mass_SP) + sum(element_mass) 
        deck_loading = max( max(dry_mass_SP/(lenght_SP*width_SP)), max(element_mass/(element_length*element_width)) ) 
        ext_personnel = max(nr_technician) 
        bathymetry = max(depth) 
        rov_class = 'Workclass'

        feas_e = {'rov': [ ['Depth rating [m]', 'sup', bathymetry],
                           ['ROV class [-]', 'equal', rov_class] ]
                         }

        feas_v = {'Crane Vessel': [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                    ['Deck space [m^2]', 'sup', deck_area],
                                    ['Max. cargo [t]', 'sup', deck_cargo],
                                    ['Crane capacity [t]', 'sup', deck_cargo],
                                    ['External  personnel [-]', 'sup', ext_personnel] ],

                  'JUP Vessel':   [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                    ['Deck space [m^2]', 'sup', deck_area],
                                    ['Max. cargo [t]', 'sup', deck_cargo],
                                    ['Crane capacity [t]', 'sup', deck_cargo],
                                    ['External  personnel [-]', 'sup', ext_personnel] ],

                 'CSV':           [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                    ['Deck space [m^2]', 'sup', deck_area],
                                    ['Max. cargo [t]', 'sup', deck_cargo],
                                    ['Crane capacity [t]', 'sup', deck_cargo],
                                    ['External  personnel [-]', 'sup', ext_personnel] ],

                 'Crane Barge':   [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                    ['Deck space [m^2]', 'sup', deck_area],
                                    ['Max. cargo [t]', 'sup', deck_cargo],
                                    ['Crane capacity [t]', 'sup', deck_cargo],
                                    ['External  personnel [-]', 'sup', ext_personnel] ],

                 'JUP Barge':     [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                    ['Deck space [m^2]', 'sup', deck_area],
                                    ['Max. cargo [t]', 'sup', deck_cargo],
                                    ['Crane capacity [t]', 'sup', deck_cargo],
                                    ['External  personnel [-]', 'sup', ext_personnel] ],

                 'Multicat':      [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                    ['Deck space [m^2]', 'sup', deck_area],
                                    ['Max. cargo [t]', 'sup', deck_cargo],
                                    ['Crane capacity [t]', 'sup', deck_cargo],
                                    ['External  personnel [-]', 'sup', ext_personnel] ]
                                }

        # Matching
        feas_m_pv = {'CTV':          [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                       ['Length [m]', 'sup', 'Terminal length [m]'],
                                       ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'Crane Vessel': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                       ['Length [m]', 'sup', 'Terminal length [m]'],
                                       ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'JUP Vessel':   [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                       ['Length [m]', 'sup', 'Terminal length [m]'],
                                       ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'CSV':          [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                       ['Length [m]', 'sup', 'Terminal length [m]'],
                                       ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'Crane Barge':  [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                       ['Length [m]', 'sup', 'Terminal length [m]'],
                                       ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'JUP Barge':    [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                       ['Length [m]', 'sup', 'Terminal length [m]'],
                                       ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'Multicat':     [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                       ['Length [m]', 'sup', 'Terminal length [m]'],
                                       ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ]
                                }
        feas_m_pe = {}

        feas_m_ve = {'rov': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                              ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                              ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'] ]
                             }


    ''' LogPhase LpM7: Onshore maintenance of devices or array sub-component - tow transport '''

    if log_phase_id == 'LpM7':
        
        # Input collection
        dry_mass_SP = OM_outputs['sp_dry_mass [kg]'].fillna(0)/1000.0
        nr_technician = OM_outputs['technician [-]'].fillna(0)
        depth = OM_outputs['depth [m]'].fillna(0)
        
        element_type = OM_outputs['element_type [-]']
        element_subtype = OM_outputs['element_subtype [-]']
        element_id = OM_outputs['element_ID [-]']
        element_mass = [0]
       
        if (element_type == 'device').any():
            device_df = user_inputs['device']
            device_index = device_df.index.values[0]
            sub_device_df = user_inputs['sub_device']
       
            if device_df['assembly strategy [-]'][device_index] == '([A,B,C,D])':
                element_mass = device_df['dry mass [kg]']/1000.0
       
            elif device_df['assembly strategy [-]'][device_index] == '([A,B,C],D)':
                element_mass = sub_device_df['dry mass [kg]']['A':'C']/1000.0
       
            else:
                msg = ("Device assembly strategy {} not supported.Only "
                       "'([A,B,C,D])' or '([A,B,C],D)' accepted.".format(
                       device_df['assembly strategy [-]'][device_index]))
                module_logger.warning(msg)
                
        # Feasibility functions
        deck_area = 0
        deck_cargo = 0
        deck_loading = 0
        BollardPull = sum(element_mass)
        ext_personnel = max(nr_technician)
        bathymetry = max(depth)
        rov_class = 'Workclass'

        feas_e = {'rov': [ ['Depth rating [m]', 'sup', bathymetry],
                           ['ROV class [-]', 'equal', rov_class] ]
                           }

        feas_v = {'Multicat': [ ['Bollard pull [t]', 'sup', BollardPull],
                                ['External  personnel [-]', 'sup', ext_personnel] ],

                  'AHTS':     [ ['Bollard pull [t]', 'sup', BollardPull],
                                ['External  personnel [-]', 'sup', ext_personnel] ]
                                }

        # Matching
        feas_m_pv = {'Multicat':     [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                       ['Length [m]', 'sup', 'Terminal length [m]'],
                                       ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'AHTS':         [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                       ['Length [m]', 'sup', 'Terminal length [m]'],
                                       ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ]
                                       }
                                       
        feas_m_pe = {}

        feas_m_ve = {'rov': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                              ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                              ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'] ]
                             }


    ''' LogPhase LpM8: Replacement of mooring line or umbilical cable '''

    if log_phase_id == 'LpM8':

        # Input collection
        moor_length = [0]
        cable_weight = [0]
        weight = [0]
        area = [0]
        loading = [0]
        demate_force = [0]

        lenght_SP = OM_outputs['sp_length [m]'].fillna(0)
        width_SP = OM_outputs['sp_width [m]'].fillna(0)
        dry_mass_SP = OM_outputs['sp_dry_mass [kg]'].fillna(0)/1000.0
        nr_technician = OM_outputs['technician [-]'].fillna(0)
        depth = OM_outputs['depth [m]'].fillna(0)
        element_type = OM_outputs['element_type [-]']
        element_id = OM_outputs['element_ID [-]']
        
        # inputs needed for maintenance action 'RtP5' - Replacement of mooring lines
        if (element_type == 'mooring line').all():        # elements should all be mooring lines
            moor_length = lenght_SP
            rov_type = 'Workclass'
 
        # inputs needed for maintenance action 'RtP6' - Replacement of dynamic cables       
        if (element_type == 'dynamic cable').all():      # elements should all be dynamic cables 
            dyn_df = electrical_outputs['dynamic cable'].ix[element_id] 
            
            # Check for wet-mate electrical interfaces  
            if (dyn_df['upstream ei type [-]'] == 'wet-mate').any() or (dyn_df['downstream ei type [-]'] == 'wet-mate').any():
                dyn_wet_df = dyn_df[dyn_df['upstream ei type [-]'] == 'wet-mate']
                dyn_wet_connector_id = dyn_wet_df['upstream ei id [-]']                
                dyn_wet_df = dyn_df[dyn_df['downstream ei type [-]'] == 'wet-mate'] 
                dyn_wet_connector_id.append(dyn_wet_df['downstream ei id [-]'])
                
                connector_df = electrical_outputs['connectors'].ix[dyn_wet_connector_id]

                rov_type = 'Workclass'                
                demate_force = connector_df['demating force [N]'].fillna(0)
               
            # Check for dry-mate/splice upstream electrical interfaces 
            if (dyn_df['upstream ei type [-]'] == 'dry-mate').any() or (dyn_df['upstream ei type [-]'] == 'splice').any():                
                dyn_dry_df = dyn_df[dyn_df['upstream ei type [-]'] == 'dry-mate']
                dyn_dry_df.append(dyn_df[dyn_df['upstream ei type [-]'] == 'splice'])
                rov_type = 'Inspection class'
                  
                # Check for collection point terminations
                if (dyn_dry_df['upstream termination type [-]'] == 'collection point').any():
                    dyn_dry_cp_df = dyn_dry_df[dyn_dry_df['upstream ei type [-]'] == 'collection point']
                    dyn_dry_cp_id = dyn_dry_cp_df['upstream termination id [-]']
                    
                    cp_df = electrical_outputs['collection point'].ix[dyn_dry_cp_id]

                    cp_length = cp_df['length [m]'].fillna(0)          
                    cp_width = cp_df['width [m]'].fillna(0)
                    cp_mass = cp_df['dry mass [kg]'].fillna(0)/1000.0
                    
                    weight.append( max(cp_mass) )
                    area.append( max(cp_length*cp_width) )
                    loading.append( max(cp_mass/(cp_length*cp_width)) )

                # Check for static cable terminations
                if (dyn_dry_df['upstream termination type [-]'] == 'static cable').any():
                    dyn_dry_static_df = dyn_dry_df[dyn_dry_df['upstream ei type [-]'] == 'static cable']
                    dyn_dry_static_id = dyn_dry_static_df['upstream termination id [-]']
                    dyn_dry_connector_id = dyn_dry_static_df['upstream ei id [-]']
                    
                    static_df = electrical_outputs['static cable'].ix[dyn_dry_static_id]
                    connector_df = electrical_outputs['connectors'].ix[dyn_dry_connector_id]

                    dyn_mass = dyn_dry_static_df['dry mass [kg/m]'].fillna(0)/1000.0
                    static_mass = static_df['dry mass [kg/m]'].fillna(0)/1000.0
                    connector_mass = connector_df['dry mass [kg]'].fillna(0)/1000.0
                  
                    weight.append( max(3*depth*static_mass + 3*depth*dyn_mass + connector_mass) )

                # Check for device terminations    
                if (dyn_df['upstream termination type [-]'] == 'device').any():
                    device_df = user_inputs['device']
                    sub_device_df = user_inputs['sub_device']
                    
                    # Check for fixed devices (floating do not have special requirements)
                    if device_df['type [-]'] == 'fixed WEC' or device_df['type [-]'] == 'fixed TEC':
                        if device_df['transportation method [-]'] == 'deck':  
                            
                            # Check assembly strategy (if support structure is required to be lifted)
                            if device_df['assembly strategy [-]'] == '([A,B,C,D])':
                                
                                device_length = device_df['length [m]'].fillna(0)
                                device_width = device_df['width [m]'].fillna(0)                             
                                device_mass = device_df['dry mass [kg]'].fillna(0)/1000.0
                                
                                weight.append( device_mass )
                                area.append( device_length*device_width )
                                loading.append( device_mass/(device_length*device_width) )                            

                            # Check assembly strategy (if support structure is not required to be lifted)
                            if device_df['assembly strategy [-]'] == '([A,B,C],D)':
                                
                                sub_device_length = sub_device_df['length [m]']['A':'C'].fillna(0)
                                sub_device_width = sub_device_df['width [m]']['A':'C'].fillna(0)                            
                                sub_device_mass = sub_device_df['dry mass [kg]']['A':'C'].fillna(0)/1000.0
                                
                                weight.append( max(sub_device_mass) )
                                area.append( max(sub_device_length*sub_device_width) )
                                loading.append( max(sub_device_mass/(sub_device_length*sub_device_width)) )  
            
            # Check downstream terminations 
            if (dyn_df['downstream ei type [-]']== 'dry-mate').any()  or (dyn_df['downstream ei type [-]'] == 'splice').any():                
                dyn_dry_df = dyn_df[dyn_df['downstream ei type [-]'] == 'dry-mate']
                dyn_dry_df.append(dyn_df[dyn_df['downstream ei type [-]'] == 'splice'])
                
                if (dyn_dry_df['downstream termination type [-]'] == 'collection point').any():
                    dyn_dry_cp_df = dyn_dry_df[dyn_dry_df['downstream ei type [-]'] == 'collection point']
                    dyn_dry_cp_id = dyn_dry_cp_df['downstream termination id [-]']
                    
                    cp_df = electrical_outputs['collection point'].ix[dyn_dry_cp_id]

                    cp_length = cp_df['length [m]'].fillna(0)          
                    cp_width = cp_df['width [m]'].fillna(0)
                    cp_mass = cp_df['dry mass [kg]'].fillna(0)/1000.0
                    
                    weight.append( max(cp_mass) )
                    area.append( max(cp_length*cp_width) )
                    loading.append( max(cp_mass/(cp_length*cp_width)) )

                if (dyn_dry_df['downstream termination type [-]'] == 'static cable').any():
                    dyn_dry_static_df = dyn_dry_df[dyn_dry_df['downstream ei type [-]'] == 'static cable']
                    dyn_dry_static_id = dyn_dry_static_df['downstream termination id [-]']
                    dyn_dry_connector_id = dyn_dry_static_df['downstream ei id [-]']
                    
                    static_df = electrical_outputs['static cable'].ix[dyn_dry_static_id]
                    connector_df = electrical_outputs['connectors'].ix[dyn_dry_connector_id]

                    dyn_mass = dyn_dry_static_df['dry mass [kg/m]'].fillna(0)/1000.0
                    static_mass = static_df['dry mass [kg/m]'].fillna(0)/1000.0
                    connector_mass = connector_df['dry mass [kg]'].fillna(0)/1000.0
                    
                    weight.append( max(3*depth*static_mass + 3*depth*dyn_mass + connector_mass) )
    
                if (dyn_df['downstream termination type [-]'] == 'device').any():
                    device_df = user_inputs['device']
                    sub_device_df = user_inputs['sub_device']
                    
                    if device_df['type [-]'] == 'fixed WEC' or device_df['type [-]'] == 'fixed TEC':
                        if device_df['transportation method [-]'] == 'deck':  
                            
                            if device_df['assembly strategy [-]'] == '([A,B,C,D])':
                                
                                device_length = device_df['length [m]'].fillna(0)
                                device_width = device_df['width [m]'].fillna(0)                             
                                device_mass = device_df['dry mass [kg]'].fillna(0)/1000.0
                                
                                weight.append( device_mass )
                                area.append( device_length*device_width )
                                loading.append( device_mass/(device_length*device_width) )                            

                            if device_df['assembly strategy [-]'] == '([A,B,C],D)':
                                
                                sub_device_length = sub_device_df['length [m]']['A':'C'].fillna(0)
                                sub_device_width = sub_device_df['width [m]']['A':'C'].fillna(0)                             
                                sub_device_mass = sub_device_df['dry mass [kg]']['A':'C'].fillna(0)/1000.0
                                
                                weight.append( max(sub_device_mass) )
                                area.append( max(sub_device_length*sub_device_width) )
                                loading.append( max(sub_device_mass/(sub_device_length*sub_device_width)) )  

        # Feasibility functions
        drum_cap = max(lenght_SP)
        deck_area = max(area)
        deck_cargo = max(weight) + max(dry_mass_SP)
        lifting_cap = max(weight)
        deck_loading = max(loading)
        ext_personnel = max(nr_technician)
        bathymetry = max(depth)
        demate_force = max(demate_force)
        rov_class = rov_type

        feas_e = {'rov': [ ['Depth rating [m]', 'sup', bathymetry],
                           ['ROV class [-]', 'equal', rov_class],
                           ['Manipulator grip force [N]', 'sup', demate_force] ]
                          }

        feas_v = {'Multicat': [ ['AH drum capacity [m]', 'sup', drum_cap],
                                ['External  personnel [-]', 'sup', ext_personnel] ] ,

                  'AHTS':     [ ['AH drum capacity [m]', 'sup', drum_cap],
                                ['External  personnel [-]', 'sup', ext_personnel] ],

                  'CLV':      [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                ['Deck space [m^2]', 'sup', deck_area],
                                ['Max. cargo [t]', 'sup', deck_cargo],
                                ['Crane capacity [t]', 'sup', lifting_cap],
                                ['External  personnel [-]', 'sup', ext_personnel] ],

                  'CSV':      [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                ['Deck space [m^2]', 'sup', deck_area],
                                ['Max. cargo [t]', 'sup', deck_cargo],
                                ['Crane capacity [t]', 'sup', lifting_cap],
                                ['External  personnel [-]', 'sup', ext_personnel] ]  
                            }
 
        # Matching
        feas_m_pv = {'Multicat':     [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                       ['Length [m]', 'sup', 'Terminal length [m]'],
                                       ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'AHTS':         [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                       ['Length [m]', 'sup', 'Terminal length [m]'],
                                       ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'CLV':          [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                       ['Length [m]', 'sup', 'Terminal length [m]'],
                                       ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                                       
                     'CSV':          [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                       ['Length [m]', 'sup', 'Terminal length [m]'],
                                       ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ]
                                }
        feas_m_pe = {}

        feas_m_ve = {'rov': [ ['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                              ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                              ['Weight [t]', 'div', 'Width [m]', 'div', 'Length [m]', 'sup', 'Deck loading [t/m^2]'] ]
                             }
                             
    deck_req = {'deck area': deck_area, 'deck cargo': deck_cargo, 'deck loading': deck_loading}
    
    return feas_e, feas_v, feas_m_pv, feas_m_pe, feas_m_ve, deck_req
