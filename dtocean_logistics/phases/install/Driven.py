"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org, pedro.vicente@wavec.org

Driven.py contains the functions to initiallize the logistic phase: "driven pile 
installation". This consists of:
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

def init_drive_phase(log_op, vessels, equipments, foundation, penet_rates, site):

    snap_to_grid = SnapToGrid(site)
    
    phase = {}
    if len(foundation) > 0:
        # save outputs required inside short named variables
        found_db = foundation
        driven_db = found_db[found_db['type [-]'] == 'pile foundation']
        driven_db = driven_db.append(found_db[found_db['type [-]'] == 'pile anchor'])

        penet_rates_VEC = []
        for indx_moo, row in driven_db.iterrows():
            UTM_elem_x = driven_db['x coord [m]'].ix[indx_moo]
            UTM_elem_y = driven_db['y coord [m]'].ix[indx_moo]
            UTM_zone = driven_db['zone [-]'].ix[indx_moo]
            # check the closest point in the site data
            closest_point = snap_to_grid((UTM_elem_x,UTM_elem_y))
            # obtain site data for the coordinates
            site_coord = site[ (site['x coord [m]'] == float( closest_point[0] )) & \
                               (site['y coord [m]'] == float( closest_point[1] )) & \
                               (site['zone [-]'] == UTM_zone) ]
            soil_type = site_coord['soil type [-]'].iloc[0]
            penet_rates_VEC.append( penet_rates[soil_type] )

    
        # initialize logistic phase
        phase = LogPhase(110, "Installation of driven piles anchors/foundations")
        indx_strategy = 0
    
        ''' Drilling Installation Strategy (Pre-Piling) '''
    
        Drilling_Tech = 'OK'
        for indx_pen in range(len(penet_rates_VEC)):
            if penet_rates_VEC[indx_pen]['Drilling rig [m/h]']==0:
                
                msg = ("Drilling technique inadequate for site soil types.")
                module_logger.warning(msg)

                Drilling_Tech = 'NOK'
                break
    
        if Drilling_Tech == 'OK':
            # initialize strategy
            phase.op_ve[indx_strategy] = DefPhase(indx_strategy, 'Drilling (Pre-Piling)')
    
            # define vessel and equipment combinations suited for this strategy
            phase.op_ve[indx_strategy].ve_combination[0] = {'vessel': [(1, vessels['CSV'])],
                                               'equipment': [(1, equipments['drilling rigs'], 0), (1, equipments['rov'], 0)]}
    
            phase.op_ve[indx_strategy].ve_combination[1] = {'vessel': [(1, vessels['JUP Barge']), (1, vessels['Tugboat'])],
                                               'equipment': [(1, equipments['drilling rigs'], 0), (1, equipments['rov'], 0)]}
    
            phase.op_ve[indx_strategy].ve_combination[2] = {'vessel': [(1, vessels['JUP Vessel'])],
                                               'equipment': [(1, equipments['drilling rigs'], 0), (1, equipments['rov'], 0)]}
    
            # define initial mobilization and onshore preparation tasks
            phase.op_ve[indx_strategy].op_seq_prep = [log_op["Mob"],
                                          log_op["AssPort"],
                                          log_op["VessPrep_driven"]]
    
            # iterate over the list of elements to be installed.
            # each element is associated with a customized operation sequence depending on it's characteristics
            for index, row in driven_db.iterrows():
    
                # initialize an empty operation sequence list for the 'index' element
                phase.op_ve[indx_strategy].op_seq_sea[index] = []
    
                phase.op_ve[indx_strategy].op_seq_sea[index].extend([ log_op["VesPos"],
                                                                      log_op["PileDrill"],
                                                                      log_op["Grout"],
                                                                      log_op["GroutRemov"]])

                # transportation operations
                phase.op_ve[indx_strategy].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])

            # define final demobilization tasks
            phase.op_ve[indx_strategy].op_seq_demob = [log_op["Demob"]]
            indx_strategy += 1
    
    
        ''' Hammering Installation Strategy (Pre-Piling) '''
    
        Hammering_Tech = 'OK'
        for indx_pen in range(len(penet_rates_VEC)):
            if penet_rates_VEC[indx_pen]['Hammer [m/h]']==0:
                
                msg = ("Hammering technique inadequate for site soil types.")
                module_logger.warning(msg)

                Hammering_Tech = 'NOK'
                break
    
        if Hammering_Tech == 'OK':
            # initialize strategy
            phase.op_ve[indx_strategy] = DefPhase(indx_strategy, 'Hammering (Pre-Piling)')
    
            # define vessel and equipment combinations suited for this strategy
            phase.op_ve[indx_strategy].ve_combination[0] = {'vessel': [(1, vessels['CSV'])],
                                               'equipment': [(1, equipments['hammer'], 0), (1, equipments['rov'], 0)]}
    
            phase.op_ve[indx_strategy].ve_combination[1] = {'vessel': [(1, vessels['JUP Barge']), (1, vessels['Tugboat'])],
                                               'equipment': [(1, equipments['hammer'], 0), (1, equipments['rov'], 0)]}
    
            phase.op_ve[indx_strategy].ve_combination[2] = {'vessel': [(1, vessels['JUP Vessel'])],
                                               'equipment': [(1, equipments['hammer'], 0), (1, equipments['rov'], 0)]}
    
            # define initial mobilization and onshore preparation tasks
            phase.op_ve[indx_strategy].op_seq_prep = [log_op["Mob"],
                                          log_op["AssPort"],
                                          log_op["VessPrep_driven"]]
    
            # iterate over the list of elements to be installed.
            # each element is associated with a customized operation sequence depending on it's characteristics
            for index, row in driven_db.iterrows():
    
                # initialize an empty operation sequence list for the 'index' element
                phase.op_ve[indx_strategy].op_seq_sea[index] = []
    
                phase.op_ve[indx_strategy].op_seq_sea[index].extend([ log_op["VesPos"],
                                                                      log_op["PileHamm"],
                                                                      log_op["Grout"],
                                                                      log_op["GroutRemov"]])

                # transportation operations
                phase.op_ve[indx_strategy].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])

            # define final demobilization tasks
            phase.op_ve[indx_strategy].op_seq_demob = [log_op["Demob"]]
            indx_strategy += 1
    
    
        ''' Vibro-Piling Installation Strategy (Pre-Piling) '''
    
        Vibro_Tech = 'OK'
        for indx_pen in range(len(penet_rates_VEC)):
            if penet_rates_VEC[indx_pen]['Vibro driver [m/h]']==0:
                
                msg = ("Vibro-Piling technique inadequate for site soil types"
                       ".")
                module_logger.warning(msg)

                Vibro_Tech = 'NOK'
                break
    
        if Vibro_Tech == 'OK':
            # initialize strategy
            phase.op_ve[indx_strategy] = DefPhase(indx_strategy, 'Vibro-Piling (Pre-Piling)')
    
            # define vessel and equipment combinations suited for this strategy
            phase.op_ve[indx_strategy].ve_combination[0] = {'vessel': [(1, vessels['CSV'])],
                                               'equipment': [(1, equipments['vibro driver'], 0), (1, equipments['rov'], 0)]}
    
            phase.op_ve[indx_strategy].ve_combination[1] = {'vessel': [(1, vessels['JUP Barge']), (1, vessels['Tugboat'])],
                                               'equipment': [(1, equipments['vibro driver'], 0), (1, equipments['rov'], 0)]}
    
            phase.op_ve[indx_strategy].ve_combination[2] = {'vessel': [(1, vessels['JUP Vessel'])],
                                               'equipment': [(1, equipments['vibro driver'], 0), (1, equipments['rov'], 0)]}
    
            # define initial mobilization and onshore preparation tasks
            phase.op_ve[indx_strategy].op_seq_prep = [log_op["Mob"],
                                                      log_op["AssPort"],
                                                      log_op["VessPrep_driven"]]
    
            # iterate over the list of elements to be installed.
            # each element is associated with a customized operation sequence depending on it's characteristics
            for index, row in driven_db.iterrows():
    
                # initialize an empty operation sequence list for the 'index' element
                phase.op_ve[indx_strategy].op_seq_sea[index] = []
    
                phase.op_ve[indx_strategy].op_seq_sea[index].extend([ log_op["VesPos"],
                                                                      log_op["PileVibro"],
                                                                      log_op["Grout"],
                                                                      log_op["GroutRemov"] ])

                # transportation operations
                phase.op_ve[indx_strategy].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])

            # define final demobilization tasks
            phase.op_ve[indx_strategy].op_seq_demob = [ log_op["Demob"] ]
            indx_strategy += 1
    
    
        if indx_strategy==0:
            
            msg = ("There is no single strategy that can install the Driven "
                   "Piles in the different site soil types.")
            module_logger.warning(msg)

    return phase
