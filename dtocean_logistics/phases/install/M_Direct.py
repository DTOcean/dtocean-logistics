"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org, pedro.vicente@wavec.org

M_Direct.py contains the functions to initiallize the logistic phase: "direct 
embedment anchor installation". This consists of:
    (1) Defining Vessels and Equipment combinations capable to carry out the logistic activities
    (2) Defining the list of operations required to conduct out the logistic activities

Parameters
----------
vessels (DataFrame): Panda table containing the vessel database

equipments (DataFrame): Panda table containing the equipment database

foundation (DataFrame): Panda table containing the foundations database

penet_rates (DataFrame): Panda table containing the penetration rates

site (DataFrame): Panda table containing the site database


Returns
-------
phase (class): contains the initialized characteristics of the logistic phase

See also: ...

                       DTOcean project
                    http://www.dtocean.eu

                   WavEC Offshore Renewables
                    http://www.wavec.org/en

"""

from .classes import DefPhase, LogPhase
from dtocean_logistics.load.snap_2_grid import SnapToGrid

import logging
module_logger = logging.getLogger(__name__)

def init_m_direct_phase(log_op, vessels, equipments, foundation, penet_rates, site):

    snap_to_grid = SnapToGrid(site)
    
    phase = {}
    if len(foundation) > 0:
        # save outputs required inside short named variables
        found_db = foundation
        direct_db = found_db[found_db['type [-]'] == 'direct-embedment anchor']  # "direct-embedment anchor" OU "direct embedment" ?!?!?!?!?!?!?!?!?
    
        penet_rates_VEC = []
        for indx_moo, row in direct_db.iterrows():
            UTM_elem_x = direct_db['x coord [m]'].ix[indx_moo]
            UTM_elem_y = direct_db['y coord [m]'].ix[indx_moo]
            UTM_zone = direct_db['zone [-]'].ix[indx_moo]
            # check the closest point in the site data
            closest_point = snap_to_grid((UTM_elem_x,UTM_elem_y))
            # obtain site data for the coordinates
            site_coord = site[ (site['x coord [m]'] == float( closest_point[0] )) & \
                               (site['y coord [m]'] == float( closest_point[1] )) & \
                               (site['zone [-]'] == UTM_zone) ]
            soil_type = site_coord['soil type [-]'].iloc[0]
            penet_rates_VEC.append( penet_rates[soil_type])
    
        # initialize logistic phase
        phase = LogPhase(114, "Installation of mooring systems with direct-embedment anchors")
        indx_strategy = 0
    
    
        ''' Direct-embedment anchor penetration through suction-embedment installation strategy '''
    
        Suction_Tech = 'OK'
        for indx_pen in range(len(penet_rates_VEC)):
            if penet_rates_VEC[indx_pen]['ROV with suction pump [m/h]']==0:
                
                msg = ("Suction-embedment technique inadequate for all soil "
                       "types.")
                module_logger.warning(msg)

                Suction_Tech = 'NOK'
                break
    
        if Suction_Tech == 'OK':
            # initialize strategy
            phase.op_ve[indx_strategy] = DefPhase(indx_strategy, 'Deploy direct-embedment anchor by suction-embedment')
    
            # define vessel and equipment combinations suited for this strategy
            phase.op_ve[indx_strategy].ve_combination[0] = {'vessel': [(1, vessels['AHTS'])],
                                                'equipment': [(1, equipments['rov'], 0)]}
    
            phase.op_ve[indx_strategy].ve_combination[1] = {'vessel': [(1, vessels['Multicat'])],
                                                'equipment': [(1, equipments['rov'], 0)]}
    
            # define initial mobilization and onshore preparation tasks
            phase.op_ve[indx_strategy].op_seq_prep = [log_op["Mob"],
                                                      log_op["AssPort"],
                                                      log_op["VessPrep_direct"]]
    
            # iterate over the list of elements to be installed.
            # each element is associated with a customized operation sequence depending on it's characteristics
            for index, row in direct_db.iterrows():
    
                # initialize an empty operation sequence list for the 'index' element
                phase.op_ve[indx_strategy].op_seq_sea[index] = []
    
                phase.op_ve[indx_strategy].op_seq_sea[index].extend([ log_op["SeafloorEquipPrep"],
                                                                      log_op["DirecSuct"],
                                                                      log_op["PreLay"] ])

                # transportation operations
                phase.op_ve[indx_strategy].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])

            # define final demobilization tasks
            phase.op_ve[0].op_seq_demob = [log_op["Demob"]]
            indx_strategy += 1
    
    
    
        ''' Direct-embedment anchor penetration through hydro-jetting installation strategy '''
    
        Hydro_Tech = 'OK'
        for indx_pen in range(len(penet_rates_VEC)):
            if penet_rates_VEC[indx_pen]['ROV with jetting [m/h]']==0:
                
                msg = ("Hydro-jetting technique inadequate for all soil "
                       "types.")
                module_logger.warning(msg)

                Hydro_Tech = 'NOK'
                break
    
        if Hydro_Tech == 'OK':
            # initialize strategy
            phase.op_ve[indx_strategy] = DefPhase(indx_strategy, 'Deploy direct-embedment anchor by hydro-jetting')
    
            # define vessel and equipment combinations suited for this strategy
            phase.op_ve[indx_strategy].ve_combination[0] = {'vessel': [(1, vessels['AHTS'])],
                                                'equipment': [(1, equipments['rov'], 0)]}
    
            phase.op_ve[indx_strategy].ve_combination[1] = {'vessel': [(1, vessels['Multicat'])],
                                                'equipment': [(1, equipments['rov'], 0)]}
    
            # define initial mobilization and onshore preparation tasks
            phase.op_ve[indx_strategy].op_seq_prep = [log_op["Mob"],
                                                      log_op["AssPort"],
                                                      log_op["VessPrep_direct"]]
    
            # iterate over the list of elements to be installed.
            # each element is associated with a customized operation sequence depending on it's characteristics
            for index, row in direct_db.iterrows():
    
                # initialize an empty operation sequence list for the 'index' element
                phase.op_ve[indx_strategy].op_seq_sea[index] = []
    
                phase.op_ve[indx_strategy].op_seq_sea[index].extend([ log_op["SeafloorEquipPrep"],
                                                                      log_op["DirecJet"],
                                                                      log_op["PreLay"] ])

                # transportation operations
                phase.op_ve[indx_strategy].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])

            # define final demobilization tasks
            phase.op_ve[indx_strategy].op_seq_demob = [log_op["Demob"]]
            indx_strategy += 1
    
    
        ''' Direct-embedment anchor penetration through mechanical-embedment installation strategy '''
    
        Mechanical_Tech = 'OK'
        for indx_pen in range(len(penet_rates_VEC)):
            if penet_rates_VEC[indx_pen]['Hammer [m/h]']==0:
                
                msg = ("Mechanical-embedment technique inadequate for all "
                       "soil types.")
                module_logger.warning(msg)

                Mechanical_Tech = 'NOK'
                break
    
        if Mechanical_Tech == 'OK':
            # initialize strategy
            phase.op_ve[indx_strategy] = DefPhase(indx_strategy, 'Deploy direct-embedment anchor by mechanical-embedment')
    
            # define vessel and equipment combinations suited for this strategy
            phase.op_ve[indx_strategy].ve_combination[0] = {'vessel': [(1, vessels['AHTS'])],
                                                'equipment': [(1, equipments['hammer'], 0), (1, equipments['rov'], 0)]}
    
            phase.op_ve[indx_strategy].ve_combination[1] = {'vessel': [(1, vessels['Multicat'])],
                                                'equipment': [(1, equipments['hammer'], 0), (1, equipments['rov'], 0)]}
    
            # define initial mobilization and onshore preparation tasks
            phase.op_ve[indx_strategy].op_seq_prep = [log_op["Mob"],
                                                      log_op["AssPort"],
                                                      log_op["VessPrep_direct"]]
    
            # iterate over the list of elements to be installed.
            # each element is associated with a customized operation sequence depending on it's characteristics
            for index, row in direct_db.iterrows():
    
                # initialize an empty operation sequence list for the 'index' element
                phase.op_ve[indx_strategy].op_seq_sea[index] = []
    
                phase.op_ve[indx_strategy].op_seq_sea[index].extend([ log_op["SeafloorEquipPrep"],
                                                                      log_op["DirecMech"],
                                                                      log_op["PreLay"] ])

                # transportation operations
                phase.op_ve[indx_strategy].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])

            # define final demobilization tasks
            phase.op_ve[indx_strategy].op_seq_demob = [log_op["Demob"]]
            indx_strategy += 1
    
    
        if indx_strategy==0:
            
            msg = ("There is no single strategy that can install the Direct "
                   "Embedment anchors in the different soil types.")
            module_logger.warning(msg)

    return phase
