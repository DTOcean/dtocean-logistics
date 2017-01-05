# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org, pedro.vicente@wavec.org

This...
"""

import numpy as np
import pandas as pd
from .....phases.select_port import distance
from .....ancillaries.find import indices
from .....ancillaries.nanTOzero import nan2zero
import math

from dtocean_logistics.load.snap_2_grid import snap_to_grid

import logging
module_logger = logging.getLogger(__name__)


def sched_m_suction(seq, ind_sol, install, log_phase, site, entry_point, device, layout, foundation, penet_rates,
                  sched_sol):
    """sched_dev_deck determines the duration of each individual logistic operations
    for the installtion of ocean energy devices following a common methodology:
        - the time value duration can be extracted from a direct average
        default value
        - the time value duration can result from a specialized function
        - the time value duration can be derived from other sources, mostly by
        making use of values available in the database or provided from the
        end-user
    Parameters
    ----------
    seq: integer
     index of the operation sequencing strategy under consideration
    ind_sol: integer
     index representing the feasible logistic solution under consideration
    log_phase: class
     class containing all data relevant to the characterization of the feasible
     logistic solutions
     dictionnary containing all required inputs to WP5 coming from WP1/end-user.
    ...

    Returns
    -------
    sched_sol : dict
     ...
    """

    """
    Initialise variables
    """
    # initialise list containing the time value durations and OLC
    op_id_prep = []
    op_dur_prep = []
    op_id_sea = []
    op_dur_sea = []
    op_dur_transit = []     
    op_olc_sea = []
    op_id_demob = []
    op_dur_demob = []
    op_id_prep_jour = {0:[]}
    op_dur_prep_jour = {0:[]}
    op_id_sea_jour = {0:[]}
    op_dur_sea_jour = {0:[]}
    op_id_demob_jour = {0:[]}
    op_dur_demob_jour = {0:[]}
    op_olc_jour = {0:[]}

    # number of gravity anchors to install
    found_db = foundation
    suction_db = found_db[found_db['type [-]'] == 'suction caisson anchor']
    nb_anch = len(suction_db)

    # number of vessel type in this feasible solution
    nb_ves_type = range(len(log_phase.op_ve[seq].sol[ind_sol]['VEs']))
    # list of the vessel(s) and equipment combination used for this feasible solution
    ve_combi = log_phase.op_ve[seq].sol[ind_sol]['VEs']
    # use the proper names of the pandas as sent to WP1
    # initialise the area and dry mass list
    elem_area = suction_db['dry mass [kg]'].fillna(0)/1000.0 # [ton]
    elem_mass = suction_db['length [m]'].fillna(0) * suction_db['width [m]'].fillna(0)
    # assumption: the first vessel is always the main installation vessel
    sol_pd_series = log_phase.op_ve[seq].sol[ind_sol]['VEs'][0][2]
    # number of equipment in the main vessel
    nb_eq = len(log_phase.op_ve[seq].sol[ind_sol]['VEs'][0])-3
    # extract the deck area and cargo
    deck_area = sol_pd_series.ix['Deck space [m^2]']
    deck_cargo = sol_pd_series.ix['Max. cargo [t]']
    # calculate the footprint and the weight due to the equipment
    eq_area = []
    eq_cargo = []
    if nb_anch>0:
        for ind_eq in range(nb_eq):
            sol_pd_eq_series = log_phase.op_ve[seq].sol[ind_sol]['VEs'][0][ind_eq+3][2]
            sol_type_eq = log_phase.op_ve[seq].sol[ind_sol]['VEs'][0][ind_eq+3][0]
            if sol_type_eq == 'rov':
                eq_area.append( sol_pd_eq_series.ix['Length [m]']*sol_pd_eq_series.ix['Width [m]'] + sol_pd_eq_series.ix['AE footprint [m^2]'] )
                eq_cargo.append( sol_pd_eq_series.ix['Weight [t]'] + sol_pd_eq_series.ix['AE weight [t]'] )
            elif sol_type_eq == 'divers':
                eq_area.append( sol_pd_eq_series.ix['Deployment eq. footprint [m^2]'] )
                eq_cargo.append( sol_pd_eq_series.ix['Deployment eq. weight [t]'] )
    # update available deck cargo and deck area due to equipment
    deck_area = deck_area - min(eq_area)
    deck_cargo = deck_cargo - min(eq_cargo)
    # initialize variables
    nb_elem_port = nb_anch # initialise the number of elements to be transported that are initially at port
    nb_journey = 0 # initialise the number of vessel journeys
    nb_el_journey = [] # initialise the list of number of elements per journey
    id_el_journey = []

    nb_elem_port = nb_anch # initialise the number of elements to be transported that are initially at port
    nb_journey = 0 # initialise the number of vessel journeys
    nb_el_journey = [] # initialise the list of number of elements per journey
    id_el_journey = []
    ################################################
    # calculation of the number of vessel journeys #
    ################################################ 
    while nb_elem_port > 0:
        # determine the cumulative vector of element dry masses and area
        elem_area_accum = elem_area.cumsum()
        elem_mass_accum = elem_mass.cumsum()
        # determine the maximum number of elements that can fit on-deck due to max deck area or max deck cargo limitations
        nb_elem_area = indices(list(elem_area_accum.values), lambda x: x>deck_area)
        if not nb_elem_area:  # if the list is empty, all elements can be carried
            nb_elem_area = len(elem_area_accum)
            id_elem_area = list(elem_area_accum.index[:])
        else:
            nb_elem_area = min(nb_elem_area)
            id_elem_area = list(elem_area_accum.index[0:nb_elem_area])
        
        nb_elem_mass = indices(list(elem_mass_accum.values), lambda x: x>deck_cargo)
        if not nb_elem_mass: # if the list is empty, all elements can be carried
            nb_elem_mass = len(elem_mass_accum)
            id_elem_mass = list(elem_mass_accum.index[:])
        else:
            nb_elem_mass = min(nb_elem_mass)
            id_elem_mass = list(elem_mass_accum.index[0:nb_elem_mass])

        nb_el_journey.append(min(nb_elem_area,nb_elem_mass))
        id_el_journey.append(min(id_elem_area,id_elem_mass))
        # update the number of elements remaining at port and their areas/masses lists
        if nb_el_journey[nb_journey] == nb_elem_port:
            nb_elem_port = 0
        elif nb_el_journey[nb_journey] == 0:
            # error that means not a single element can fit!
            msg = ("No single element can fit on deck.")
            module_logger.warning(msg)
        else:
            nb_elem_port = nb_elem_port - nb_el_journey[nb_journey]
            elem_mass = elem_mass.iloc[nb_el_journey[-1]:]
            elem_area = elem_area.iloc[nb_el_journey[-1]:]
        # update the number of vessel journeys
        nb_journey = nb_journey + 1
    ################################################################
    # calculation of the prep, sea and demob time for all journeys #
    ################################################################          
    ind_el = 0
    for jour in range(nb_journey):
        journey = sched_sol['journey']
        journey[jour] = {'prep_id': [],
                         'prep_dur': [],
                         'sea_id': [],
                         'sea_dur': [],
                         'sea_olc': [],
                         'site_site_transit_dur': [],
                         'port_site_transit_dur': [],
                         'installation_dur': [],
                         'wait_dur': []}
        if jour>0:
            op_id_prep_jour[jour] = []
            op_dur_prep_jour[jour] = []
            op_id_sea_jour[jour] = []
            op_dur_sea_jour[jour] = []
            op_olc_jour[jour] = []
            op_id_demob_jour[jour] = []
            op_dur_demob_jour[jour] = []

        # number of operation sequence in the preparation phase
        nb_op_prep = len(log_phase.op_ve[seq].op_seq_prep)
        # determine the duration of the logistic phase preparation before departure of the vessel(s)
        for op_prep in range(nb_op_prep): # loop over the nb of onshore logistic operations
            log_op_prep = log_phase.op_ve[seq].op_seq_prep[op_prep]
            # create a panda series suitable for the discrimination
            # between type of methods for time assessment
            time_method = pd.Series([log_op_prep.time_value,
                                     log_op_prep.time_function,
                                     log_op_prep.time_other])

            # discriminate between the time assessment methods
            if not pd.isnull(time_method[0]): # direct value
                op_dur_prep.append(nb_el_journey[jour]*log_op_prep.time_value)
                op_id_prep.append(log_op_prep.description)

                op_id_prep_jour[jour].append(log_op_prep.description)
                op_dur_prep_jour[jour].append(nb_el_journey[jour]*log_op_prep.time_value)

                journey[jour]['prep_id'].append(log_op_prep.description)
                journey[jour]['prep_dur'].append(nb_el_journey[jour]*log_op_prep.time_value)

            elif not pd.isnull(time_method[1]): # function
                msg = ("No functions are currently available for onshore "
                       "operations.")
                module_logger.warning(msg)

            elif not pd.isnull(time_method[2]):
                if log_op_prep.time_other == "vesselsDB['Mob time [h]']" and jour == 0:
                    ves_mob_time = []
                    for vt in nb_ves_type:
                        ves_mob_time.append(ve_combi[vt][2].ix['Mob time [h]'])
                    ves_mob_time_long = max(ves_mob_time)
                    op_dur_prep.append(ves_mob_time_long)
                    op_id_prep.append(log_op_prep.description)
                    op_id_prep_jour[jour].append(log_op_prep.description)
                    op_dur_prep_jour[jour].append(ves_mob_time_long)
                    journey[jour]['prep_id'].append(log_op_prep.description)
                    journey[jour]['prep_dur'].append(ves_mob_time_long)
                elif log_op_prep.time_other == "vesselsDB['Mob time [h]']" and jour > 0:
                    continue
                else:
                    msg = ("Unknown 'other' method for time assessment of "
                           "this operation.")
                    module_logger.warning(msg)
#                only required if there are different element type which is not possible for devices
#                for dev_id, row in layout.iterrows(): # loop over the number of element type
#                    # number of operation sequence in the sea-work phase
#                    nb_op_sea = len(log_phase.op_ve[seq].op_seq_sea[dev_id])
        #########################################################################
        # include transportation from port to first element before each journey #
        #########################################################################  
        # obtain distance from port to site
        port_2_site_dist = install['port']['Distance port-site [km]']
        UTM_site = [entry_point['x coord [m]'].ix[0],
                    entry_point['y coord [m]'].ix[0],
                    entry_point['zone [-]'].ix[0]]
        # compute distance from site to first element
        id_first_elem = id_el_journey[jour][0]
        UTM_elem = [suction_db['x coord [m]'].ix[id_first_elem],
                    suction_db['y coord [m]'].ix[id_first_elem],
                    suction_db['zone [-]'].ix[id_first_elem]]
        site_2_elem_dist = distance(UTM_site,UTM_elem) # distance function returns [km]
        # loop over the nb of vessel types  
        ves_speed = []  
        olc = []                      
        for vt in nb_ves_type:
            ves_speed.append(log_phase.op_ve[seq].sol[ind_sol]['VEs'][vt][2].ix['Transit speed [m/s]'])
            ves_type = ve_combi[vt][2].ix['Vessel type [-]']
            olc_Hs = ve_combi[0][2].ix['OLC: Transit maxHs [m]']
            olc_Tp = ve_combi[0][2].ix['OLC: Transit maxTp [s]']
            olc_Ws = ve_combi[0][2].ix['OLC: Transit maxWs [m/s]']
            olc_Cs = ve_combi[0][2].ix['OLC: Transit maxCs [m/s]']
            olc_trans = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
            olc_trans = nan2zero(olc_trans)
            olc.append(olc_trans)
        # print olc
        olc = np.min(olc,0).tolist()
        ves_slow = 3.6*min(ves_speed) # [km/h]
        port_2_site_time = (port_2_site_dist + site_2_elem_dist)/ves_slow
        # append transit time from port to site
        op_id_sea.append('Transportation from port to element')
        op_dur_sea.append(port_2_site_time)
        op_dur_transit.append(port_2_site_time)
        op_olc_sea.append(olc)
        
        op_id_sea_jour[jour].append('Transportation from port to element')
        op_dur_sea_jour[jour].append(port_2_site_time)
        op_olc_jour[jour].append(olc)

        journey[jour]['sea_id'].append('Transportation from port to element')
        journey[jour]['sea_dur'].append(port_2_site_time)
        journey[jour]['port_site_transit_dur'].append(port_2_site_time)           
        journey[jour]['sea_olc'].append(olc)    

        #######################################################################
        # Loop over the different elements being installed during this 'jour' #
        #######################################################################              
        for elem_id in id_el_journey[jour]:
            # determine the duration of the logistic phase sea-work
            ################################################################### 
            # Loop over the different offshore logistic operations of elem_id #
            ################################################################### 
            for log_op_sea in log_phase.op_ve[seq].op_seq_sea[elem_id]:  # loop over the nb of offshore logistic operations
                # create a panda series suitable for the discrimination
                # between type of methods for time assessment
                time_method = pd.Series([log_op_sea.time_value,
                                         log_op_sea.time_function,
                                         log_op_sea.time_other])
                olc_method = log_op_sea.olc
 
                # discriminate between the time assessment methods
                if not pd.isnull(time_method[0]): # default value
                    # type of logistic operation
                    if log_op_sea.description == "Seafloor & equipment preparation":

                        olc_Hs = ve_combi[0][2].ix['OLC: Transit maxHs [m]']
                        olc_Tp = olc_method[1]
                        olc_Ws = olc_method[2]
                        olc_Cs = olc_method[3]
                        olc_trans = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                        olc_trans = nan2zero(olc_trans)
    
                        op_olc_sea.append(olc_trans)
                        op_id_sea.append(log_op_sea.description)
                        op_dur_sea.append(log_op_sea.time_value)
    
                        op_id_sea_jour[jour].append(log_op_sea.description)
                        op_dur_sea_jour[jour].append(log_op_sea.time_value)
                        op_olc_jour[jour].append(olc_trans)
    
                        journey[jour]['sea_id'].append(log_op_sea.description)
                        journey[jour]['sea_dur'].append(log_op_sea.time_value)
                        journey[jour]['sea_olc'].append(olc_trans)
                        
                    elif log_op_sea.description == "Pre-lay moorings or buoy off":
                        
                        olc_Hs = ve_combi[0][2].ix['OLC: Transit maxHs [m]']
                        olc_Tp = ve_combi[0][2].ix['OLC: Transit maxTp [s]']
                        olc_Ws = ve_combi[0][2].ix['OLC: Transit maxWs [m/s]']
                        olc_Cs = ve_combi[0][2].ix['OLC: Transit maxCs [m/s]']
                        olc_trans = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                        olc_trans = nan2zero(olc_trans)
    
                        op_olc_sea.append(olc_trans)
                        op_id_sea.append(log_op_sea.description)
                        op_dur_sea.append(log_op_sea.time_value)
    
                        op_id_sea_jour[jour].append(log_op_sea.description)
                        op_dur_sea_jour[jour].append(log_op_sea.time_value)
                        op_olc_jour[jour].append(olc_trans)
    
                        journey[jour]['sea_id'].append(log_op_sea.description)
                        journey[jour]['sea_dur'].append(log_op_sea.time_value)
                        journey[jour]['sea_olc'].append(olc_trans)
                    else:
                        msg = ("Unknown installation operation {}.".format(
                            log_op_sea.description))
                        module_logger.warning(msg)

                #################################### 
                # Time assessment: function        # 
                ####################################
                elif not pd.isnull(time_method[1]): 
                    # type of function
                    if log_op_sea.time_function == "distance":
                        ves_speed = []
                        olc = []                            
                        # extract information from the current and last element being installed in this journey                          
                        elem_ix = id_el_journey[jour].index(elem_id)
                        last_elem_ix = len(id_el_journey[jour])-1                   
                        # extract the coordinates of the lease area entry point
                        UTM_site = [entry_point['x coord [m]'].ix[0],
                                    entry_point['y coord [m]'].ix[0],
                                    entry_point['zone [-]'].ix[0]]
                        # extract the coordinates of the current element being installed                                  
                        UTM_elem = [suction_db['x coord [m]'].ix[elem_id],
                                    suction_db['y coord [m]'].ix[elem_id],
                                    suction_db['zone [-]'].ix[elem_id]]  
                        # check if it's the last element in the journey
                        if  elem_ix == last_elem_ix:
                            # compute distance from last element to the lease area entry point
                            dist = distance(UTM_elem, UTM_site)
                        else:
                            # extract the id of the next element being installed in this journey
                            next_elem_id = id_el_journey[jour][elem_ix+1]      
                            # extract the coordinates of the next element being installed  
                            UTM_next_elem = [suction_db['x coord [m]'].ix[next_elem_id],
                                             suction_db['y coord [m]'].ix[next_elem_id],
                                             suction_db['zone [-]'].ix[next_elem_id] ]                              
                            # compute distance from last element to the lease area entry point
                            dist = distance(UTM_elem, UTM_next_elem)                               
                        # loop over the nb of vessel types in the combination
                        ves_speed = []      
                        olc = []     
                        for vt in nb_ves_type:
                            ves_type = ve_combi[vt][2].ix['Vessel type [-]']
                            ves_speed.append(ve_combi[vt][2].ix['Transit speed [m/s]'])
                            olc_Hs = ve_combi[0][2].ix['OLC: Transit maxHs [m]']
                            olc_Tp = ve_combi[0][2].ix['OLC: Transit maxTp [s]']
                            olc_Ws = ve_combi[0][2].ix['OLC: Transit maxWs [m/s]']
                            olc_Cs = ve_combi[0][2].ix['OLC: Transit maxCs [m/s]']
                            olc_trans = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                            olc_trans = nan2zero(olc_trans)
                            olc.append(olc_trans)
                        # print olc
                        olc = np.min(olc,0).tolist()
                        ves_slow = 3.6*min(ves_speed) # [km/h]
                        dist_time = dist/ves_slow
                        # append transit time from element to site
                        op_id_sea.append(log_op_sea.description)                                
                        op_dur_sea.append(dist_time)
                        op_dur_transit.append(dist_time)
                        op_olc_sea.append(olc)
                        
                        op_id_sea_jour[jour].append(log_op_sea.description)
                        op_dur_sea_jour[jour].append(dist_time)
                        op_olc_jour[jour].append(olc) 
                        
                        journey[jour]['sea_id'].append(log_op_sea.description)
                        journey[jour]['sea_dur'].append(dist_time)
                        journey[jour]['site_site_transit_dur'].append(dist_time)                                  
                        journey[jour]['sea_olc'].append(olc)                                                         

                    elif log_op_sea.description == "Lowering anchors with mooring lines + Suction caisson anchor seafloor penetration + Tensioning":
                        if ve_combi[0][2].ix['Vessel type [-]'] == "JUP Barge" or ve_combi[0][2].ix['Vessel type [-]'] == "JUP Vessel":
                            olc_Hs = 0
                        else:
                            olc_Hs = ve_combi[0][2].ix['OLC: Transit maxHs [m]']
                        olc_Tp = olc_method[1]
                        olc_Ws = olc_method[2]
                        olc_Cs = olc_method[3]
                        olc = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                        olc = nan2zero(olc)
                        op_olc_sea.append(olc)
                        op_time = []


                        UTM_elem_x = suction_db['x coord [m]'].ix[elem_id]
                        UTM_elem_y = suction_db['y coord [m]'].ix[elem_id]
                        UTM_zone = suction_db['zone [-]'].ix[elem_id]
                        # check the closest point in the site data
                        closest_point = snap_to_grid(site, (UTM_elem_x,UTM_elem_y))
                        # obtain site data for the coordinates
                        site_coord = site[ (site['x coord [m]'] == float( closest_point[0] )) & \
                                           (site['y coord [m]'] == float( closest_point[1] )) & \
                                           (site['zone [-]'] == UTM_zone) ]
                        soil_type = site_coord['soil type [-]'].iloc[0]
                        ins_depth = site_coord['bathymetry [m]'].iloc[0]
                        depth_of_ins = suction_db['installation depth [m]'].ix[elem_id]


                        if log_op_sea.description == "Lowering anchors with mooring lines + Suction caisson anchor seafloor penetration + Tensioning":
                            penetration_rate = penet_rates.ix['ROV with suction pump [m/h]'][soil_type]
                        else:
                            msg = ("Unknown installation method penetration "
                                   "rate for phase {}.".format(
                                   log_op_sea.description))
                            module_logger.warning(msg)
                            penetration_rate = 0

                        if penetration_rate==0:
                            
                            msg = ("Soil penetration technique inappropriate "
                                   "for the soil type at location.")
                            module_logger.warning(msg)
                            
                        else:
                            op_time.append( depth_of_ins/penetration_rate )
                            
                        op_time_total = sum(op_time)
                        op_dur_sea.append(op_time_total)
                        op_id_sea.append(log_op_sea.description)
    
                        op_id_sea_jour[jour].append(log_op_sea.description)
                        op_dur_sea_jour[jour].append(op_time_total)
    
                        journey[jour]['sea_id'].append(log_op_sea.description)
                        journey[jour]['sea_dur'].append(op_time_total)
                        journey[jour]['sea_olc'].append(olc)
                    else:

                        msg = ("Unknown installation operation {}.".format(
                            log_op_sea.description))
                        module_logger.warning(msg)

                ########################## 
                # Time assessment: other #
                ##########################     
                elif not pd.isnull(time_method[2]):
                    pass
                
        ind_el = ind_el + nb_el_journey[jour]
        #######################################################################
        # include transportation from last element to port after each journey #
        #######################################################################  
        # extract site coordinates and last element of the journey coordinates          
        UTM_site = [entry_point['x coord [m]'].ix[0],
                    entry_point['y coord [m]'].ix[0],
                    entry_point['zone [-]'].ix[0]]
        # obtain distance from site to port            
        site_2_port_dist = install['port']['Distance port-site [km]']
        # loop over the nb of vessel types  
        ves_speed = []
        olc = []                                
        for vt in nb_ves_type:
            ves_speed.append(log_phase.op_ve[seq].sol[ind_sol]['VEs'][vt][2].ix['Transit speed [m/s]'])
            ves_type = ve_combi[vt][2].ix['Vessel type [-]']
            olc_Hs = ve_combi[0][2].ix['OLC: Transit maxHs [m]']
            olc_Tp = ve_combi[0][2].ix['OLC: Transit maxTp [s]']
            olc_Ws = ve_combi[0][2].ix['OLC: Transit maxWs [m/s]']
            olc_Cs = ve_combi[0][2].ix['OLC: Transit maxCs [m/s]']
            olc_trans = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
            olc_trans = nan2zero(olc_trans)
            olc.append(olc_trans)
        # print olc
        olc = np.min(olc,0).tolist()
        ves_slow = 3.6*min(ves_speed) # [km/h]
        site_2_port_time = (site_2_port_dist)/ves_slow
        # append transit time from port to site
        op_id_sea.append('Transportation from site to port')
        op_dur_sea.append(site_2_port_time)
        op_dur_transit.append(site_2_port_time)
        op_olc_sea.append(olc)
        
        op_id_sea_jour[jour].append('Transportation from site to port')
        op_dur_sea_jour[jour].append(site_2_port_time)
        op_olc_jour[jour].append(olc)
        
        journey[jour]['sea_id'].append('Transportation from site to port')
        journey[jour]['sea_dur'].append(site_2_port_time)
        journey[jour]['port_site_transit_dur'].append(site_2_port_time)          
        journey[jour]['sea_olc'].append(olc)            
        # increment journey
        ind_el = ind_el + nb_el_journey[jour]

    # add demobilisation time to finalise the logistic phase 
    log_op_demob = log_phase.op_ve[seq].op_seq_demob[0]
    # create a panda series suitable for the discrimination
    # between type of methods for time assessment
    time_method = pd.Series([log_op_demob.time_value,
                             log_op_demob.time_function,
                             log_op_demob.time_other])  
    if not pd.isnull(time_method[2]):
        ves_demob_time = []
        for vt in nb_ves_type:
            ves_demob_time.append(ve_combi[vt][2].ix['Mob time [h]'])
        ves_demob_time_long = max(ves_demob_time)
        if math.isnan(ves_demob_time_long):
            ves_demob_time_long = 0
        op_dur_demob.append(ves_demob_time_long) 
        op_id_demob.append(log_op_demob.description)
        op_id_sea_jour[nb_journey-1].append(log_op_demob.description)
        op_dur_sea_jour[nb_journey-1].append(ves_demob_time_long)
    else:
        msg = ("Only demob is allowed at the end of a logistic phase.")
        module_logger.warning(msg)
            
    """""""""""""""
    Format outputs
    """""""""""""""
    # Prepare the dataframe of the mobilization operations
    columns = ['Logitic operation [-]', 'Time value [h]']
    index = np.arange(len(op_id_prep))
    op_prep = pd.DataFrame(columns=columns, index = index)
    op_prep['Logitic operation [-]'] = op_id_prep
    op_prep['Time value [h]'] = op_dur_prep
    
    # Prepare the dataframe of the sea operations
    columns = ['Logitic operation [-]', 'Time value [h]', 'OLC: Hs [m], Tp [s], Ws [m/s], Cs [m/s]']
    index = np.arange(len(op_id_sea))
    op_sea = pd.DataFrame(columns=columns, index = index)
    op_sea['Logitic operation [-]'] = op_id_sea
    op_sea['Time value [h]'] = op_dur_sea
    op_sea['OLC: Hs [m], Tp [s], Ws [m/s], Cs [m/s]'] = op_olc_sea

    # Prepare the dataframe of the demob operations
    columns = ['Logitic operation [-]', 'Time value [h]']
    index = np.arange(len(op_id_demob))
    op_demob = pd.DataFrame(columns=columns, index = index)
    op_demob['Logitic operation [-]'] = op_id_demob
    op_demob['Time value [h]'] = op_dur_demob
    
    sched_sol['global'] = {'nb of journeys': nb_journey,
                           'nb of elements per journey': nb_el_journey,
                           'prep': op_prep,
                           'sea': op_sea,
                           'demob': op_demob}
    # Replace 'NaN' with zeros in outputs
    # pass outputs to sched_sol
    sched_sol['details per journey'] = {'nb of journeys': nb_journey,
                                        'nb of elements per journey': nb_el_journey,
                                        'prep': [op_id_prep_jour, op_dur_prep_jour],
                                        'sea': [op_id_sea_jour, op_dur_sea_jour, op_olc_jour],
                                        'demob': [op_id_demob_jour, op_dur_demob_jour]}

    # replace 'NaN' from the time duration values retrieved with '0'
    op_dur_prep_clean = op_dur_prep
    for ind_prep in range(len(op_dur_prep)):
        if math.isnan(op_dur_prep[ind_prep]):
            op_dur_prep_clean[ind_prep] = 0
    op_dur_sea_clean = op_dur_sea
    for ind_sea in range(len(op_dur_sea)):
        if math.isnan(op_dur_sea[ind_sea]):
            op_dur_sea_clean[ind_sea] = 0
    op_dur_demob_clean = op_dur_demob
    for ind_demob in range(len(op_dur_demob)):
        if math.isnan(op_dur_demob[ind_demob]):
            op_dur_demob_clean[ind_demob] = 0
    # Calculate cumulated times
    sched_sol['prep time'] = sum(op_dur_prep)
    sched_sol['sea time'] = sum(op_dur_sea)
    sched_sol['transit time'] = sum(op_dur_transit)
    sched_sol['total time'] = sched_sol['prep time'] + sched_sol['sea time'] #+ op_dur_demob_clean
    return sched_sol
            
            