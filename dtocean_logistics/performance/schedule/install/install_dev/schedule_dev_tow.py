# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This...
"""

import numpy as np
import pandas as pd
import math

from .....phases.select_port import distance
from .....ancillaries.nanTOzero import nan2zero

import logging
module_logger = logging.getLogger(__name__)

def sched_dev_tow(seq, ind_sol, install, log_phase, site, entry_point, device, sub_device,
                  layout, sched_sol):
    """
    sched_dev_deck determines the duration of each individual logistic operations
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
    user_inputs : dict
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
    # number of devices to install    
    nb_dev = len(layout)
    # number of vessel type in this feasible solution
    nb_ves_type = range(len(log_phase.op_ve[seq].sol[ind_sol]['VEs']))
    # list of the vessel(s) and equipment combination used for this feasible solution
    ve_combi = log_phase.op_ve[seq].sol[ind_sol]['VEs']

    """
    Time assessment for the logistic phase
    """
    # determination of the number of vessel journeys
    # for towing transportation it is always assumed the vessel installs one
    # device at a time
    nb_journey = nb_dev
    nb_el_journey = [1]*nb_journey
    ind_el = 0
    ################################################################           
    # calculation of the prep, sea and demob time for all journeys #        
    ################################################################ 
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
        if jour > 0:
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
                if log_op_prep.description == "Load-out:Lifted away":
                    op_dur_prep.append(nb_el_journey[jour]*log_op_prep.time_value)
                    op_id_prep.append(log_op_prep.description)
                    op_id_prep_jour[jour].append(log_op_prep.description)
                    op_dur_prep_jour[jour].append(nb_el_journey[jour]*log_op_prep.time_value)
                    journey[jour]['prep_id'].append(log_op_prep.description)
                    journey[jour]['prep_dur'].append(nb_el_journey[jour]*log_op_prep.time_value)
                elif log_op_prep.description == "Load-out:Skidded/Trailler":
                    op_dur_prep.append(nb_el_journey[jour]*log_op_prep.time_value)
                    op_id_prep.append(log_op_prep.description)
                    op_id_prep_jour[jour].append(log_op_prep.description)
                    op_dur_prep_jour[jour].append(nb_el_journey[jour]*log_op_prep.time_value)
                    journey[jour]['prep_id'].append(log_op_prep.description)
                    journey[jour]['prep_dur'].append(nb_el_journey[jour]*log_op_prep.time_value)
                elif log_op_prep.description == "Load-out:Floated away":
                    op_dur_prep.append(nb_el_journey[jour]*log_op_prep.time_value)
                    op_id_prep.append(log_op_prep.description)
                    op_id_prep_jour[jour].append(log_op_prep.description)
                    op_dur_prep_jour[jour].append(nb_el_journey[jour]*log_op_prep.time_value)
                    journey[jour]['prep_id'].append(log_op_prep.description)
                    journey[jour]['prep_dur'].append(nb_el_journey[jour]*log_op_prep.time_value)
                else:
                    
                    msg = ("Unknown default value time value duration for "
                           "this logistic operation associated with the "
                           "installation of devices.")
                    module_logger.warning(msg)

            elif not pd.isnull(time_method[1]): # function
                # type of function
                msg = ("No functions are currently available for onshore "
                       "operations.")
                module_logger.warning(msg)
                 
            elif not pd.isnull(time_method[2]):
                if log_op_prep.time_other == "vesselsDB['Mob time [h]']" and jour == 0:
                    ves_mob_time = []
                    for vt in nb_ves_type:
                        ves_mob_time.append(ve_combi[vt][2].ix['Mob time [h]'])
                    ves_mob_time_long = float(max(ves_mob_time))
                    op_dur_prep.append(ves_mob_time_long)
                    op_id_prep.append(log_op_prep.description)
                    op_id_prep_jour[jour].append(log_op_prep.description)
                    op_dur_prep_jour[jour].append(ves_mob_time_long)
                    journey[jour]['prep_id'].append(log_op_prep.description)
                    journey[jour]['prep_dur'].append(ves_mob_time_long)
                elif log_op_prep.time_other == "vesselsDB['Mob time [h]']" and jour > 0:
                    continue
                elif log_op_prep.time_other == "device['assembly duration [h]']":
                    assemb_time = float(device['assembly duration [h]'].ix[0])
                    op_dur_prep.append(nb_el_journey[jour]*assemb_time)
                    op_id_prep.append(log_op_prep.description)
                    op_id_prep_jour[jour].append(log_op_prep.description)
                    op_dur_prep_jour[jour].append(nb_el_journey[jour]*assemb_time)
                    journey[jour]['prep_id'].append(log_op_prep.description)
                    journey[jour]['prep_dur'].append(nb_el_journey[jour]*assemb_time)
                else:
                    
                    msg = ("Unknown 'other' method for time value duration "
                           "assessment of this onshore operation.")
                    module_logger.warning(msg)

                    # only required if there are different element type which is not possible for devices
        #########################################################################
        # include transportation from port to first element before each journey #
        #########################################################################  
        # obtain distance from port to site
        port_2_site_dist = install['port']['Distance port-site [km]']
        UTM_site = [entry_point['x coord [m]'].ix[0],
                    entry_point['y coord [m]'].ix[0],
                    entry_point['zone [-]'].ix[0]]
        # compute distance from site to element being installed each 'jour'
        id_first_elem = layout.iloc[jour].name
        UTM_elem = [layout['x coord [m]'].ix[id_first_elem],
                    layout['y coord [m]'].ix[id_first_elem],
                    layout['zone [-]'].ix[id_first_elem]]
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
        
        ###################################################
        # obtain the element id being towed each journey  #
        ###################################################           
        elem_id = layout.iloc[jour].name   
        # determine the duration of the logistic phase sea-work
        ################################################################### 
        # Loop over the different offshore logistic operations of elem_id #
        ###################################################################          
        for log_op_sea in log_phase.op_ve[seq].op_seq_sea[elem_id]: 
            # create a panda series suitable for the discrimination
            # between type of methods for time assessment
            time_method = pd.Series([log_op_sea.time_value,
                                     log_op_sea.time_function,
                                     log_op_sea.time_other])
            olc_method = log_op_sea.olc
            # discriminate between the time assessment methods
            #################################### 
            # Time assessment: default value   #
            #################################### 
            if not pd.isnull(time_method[0]): 
                # type of logistic operation
                if log_op_sea.description == "Vessel Positioning": # vessel positioning
                    if any(olc_method[op] == "vessel" for op in range(len(olc_method))):
                        if ves_type == "JUP Barge" or ves_type == "JUP Vessel":
                            # OLC:
                            olc_Hs = ve_combi[0][2].ix['OLC: Jacking maxHs [m]']
                            olc_Tp = ve_combi[0][2].ix['OLC: Jacking maxTp [s]']
                            olc_Ws = ve_combi[0][2].ix['OLC: Jacking maxWs [m/s]']
                            olc_Cs = ve_combi[0][2].ix['OLC: Jacking maxCs [m/s]']
                            olc_trans = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                            olc_trans = nan2zero(olc_trans)
                            # SPEED:
                            UTM_elem = [ layout['x coord [m]'].ix[elem_id],
                                         layout['y coord [m]'].ix[elem_id],
                                         layout['zone [-]'].ix[elem_id] ]
                            # obtain site depth for the coordinates
                            site_depth = site[ (site['x coord [m]'] == UTM_elem[0]) & \
                                               (site['y coord [m]'] == UTM_elem[1]) & \
                                               (site['zone [-]'] == UTM_elem[2]) ]
                            location_depth = site_depth['bathymetry [m]'].iloc[0]
                            jackup_speed = ve_combi[0][2].ix['JackUp speed down [m/min]']
                            time_value_ves_pos_min = location_depth / jackup_speed
                            time_value_ves_pos = time_value_ves_pos_min/60.0 # in hour
                        else:
                            olc_Hs = ve_combi[0][2].ix['OLC: Transit maxHs [m]']
                            olc_Tp = ve_combi[0][2].ix['OLC: Transit maxTp [s]']
                            olc_Ws = ve_combi[0][2].ix['OLC: Transit maxWs [m/s]']
                            olc_Cs = ve_combi[0][2].ix['OLC: Transit maxCs [m/s]']
                            olc_trans = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                            olc_trans = nan2zero(olc_trans)
                            time_value_ves_pos = log_op_sea.time_value
                    else:
                        time_value_ves_pos = log_op_sea.time_value
                    # append information
                    op_id_sea.append(log_op_sea.description)
                    op_dur_sea.append(time_value_ves_pos)
                    op_olc_sea.append(olc_trans)
                    
                    op_id_sea_jour[jour].append(log_op_sea.description)                            
                    op_dur_sea_jour[jour].append(time_value_ves_pos)
                    op_olc_jour[jour].append(olc_trans)

                    journey[jour]['sea_id'].append(log_op_sea.description)
                    journey[jour]['sea_dur'].append(time_value_ves_pos)
                    journey[jour]['sea_olc'].append(olc_trans)
                else:
                    if any(olc_method[op] == "vessel" for op in range(len(olc_method))):
                        olc_Hs = ve_combi[0][2].ix['OLC: Transit maxHs [m]']
                        olc_Tp = ve_combi[0][2].ix['OLC: Transit maxTp [s]']
                        olc_Ws = ve_combi[0][2].ix['OLC: Transit maxWs [m/s]']
                        olc_Cs = ve_combi[0][2].ix['OLC: Transit maxCs [m/s]']
                    else: 
                        olc_Hs = olc_method[0]
                        olc_Tp = olc_method[1]
                        olc_Ws = olc_method[2]
                        olc_Cs = olc_method[3]
                    olc_trans = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                    olc_trans = nan2zero(olc_trans)
                    # append information
                    op_id_sea.append(log_op_sea.description)
                    op_dur_sea.append(log_op_sea.time_value)
                    op_olc_sea.append(olc_trans)
                    
                    op_id_sea_jour[jour].append(log_op_sea.description)
                    op_dur_sea_jour[jour].append(log_op_sea.time_value)
                    op_olc_jour[jour].append(olc_trans)
                    
                    journey[jour]['sea_id'].append(log_op_sea.description)
                    journey[jour]['sea_dur'].append(log_op_sea.time_value)
                    journey[jour]['sea_olc'].append(olc_trans)

            #################################### 
            # Time assessment: function        #
            ####################################
            elif not pd.isnull(time_method[1]): 
                # type of function
                if log_op_sea.time_function == "distance":
                    ves_speed = []
                    olc = []                            
                    # extract the coordinates of the lease area entry point
                    UTM_site = [entry_point['x coord [m]'].ix[0],
                                entry_point['y coord [m]'].ix[0],
                                entry_point['zone [-]'].ix[0]]
                    # extract the coordinates of the current element being installed                                  
                    UTM_elem = [layout['x coord [m]'].ix[elem_id],
                                layout['y coord [m]'].ix[elem_id],
                                layout['zone [-]'].ix[elem_id]]
                    # compute distance from last element to the lease area entry point
                    elem_2_site_dist = distance(UTM_elem, UTM_site)                                
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
                    elem_2_site_time = elem_2_site_dist/ves_slow
                    # append transit time from element to site
                    op_id_sea.append(log_op_sea.description)                                
                    op_dur_sea.append(elem_2_site_time)
                    op_dur_transit.append(elem_2_site_time)
                    op_olc_sea.append(olc)
                    
                    op_id_sea_jour[jour].append(log_op_sea.description)
                    op_dur_sea_jour[jour].append(elem_2_site_time)
                    op_olc_jour[jour].append(olc) 
                    
                    journey[jour]['sea_id'].append(log_op_sea.description)
                    journey[jour]['sea_dur'].append(elem_2_site_time)
                    journey[jour]['site_site_transit_dur'].append(elem_2_site_time)                                  
                    journey[jour]['sea_olc'].append(olc)                                                         
                        
                else:

                    msg = ("Unknown sea operation {} using a function for the "
                           "time assessment. Only 'distance' accepted.".format(
                           log_op_sea.time_function))
                    module_logger.warning(msg)

            ########################## 
            # Time assessment: other #
            ########################## 
            elif not pd.isnull(time_method[2]):  
                if log_op_sea.time_other == "device['connect duration [h]']":
                    dev_connect_time = device['connect duration [h]'].ix[0]
                    olc_Hs = device['max Hs [m]'].ix[0]
                    olc_Tp = device['max Tp [s]'].ix[0]
                    olc_Ws = device['max wind speed [m/s]'].ix[0]
                    olc_Cs = device['max current speed [m/s]'].ix[0]
                    olc_dev_connect = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                    olc_dev_connect = nan2zero(olc_dev_connect)

                    op_id_sea.append(log_op_sea.description)
                    op_dur_sea.append(dev_connect_time)                     
                    op_olc_sea.append(olc_dev_connect)
                    
                    op_id_sea_jour[jour].append(log_op_sea.description)
                    op_dur_sea_jour[jour].append(dev_connect_time)
                    op_olc_jour[jour].append(olc_dev_connect)
                    
                    journey[jour]['sea_id'].append(log_op_sea.description)
                    journey[jour]['sea_dur'].append(dev_connect_time)
                    journey[jour]['sea_olc'].append(olc_dev_connect)
                                   
                elif log_op_sea.time_other == "device['disconnect duration [h]']":
                    dev_disconnect_time = device['connect duration [h]'].ix[0]
                    olc_Hs = device['max Hs [m]'].ix[0]
                    olc_Tp = device['max Tp [s]'].ix[0]
                    olc_Ws = device['max wind speed [m/s]'].ix[0]
                    olc_Cs = device['max current speed [m/s]'].ix[0]
                    olc_dev_disconnect = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                    olc_dev_disconnect = nan2zero(olc_dev_disconnect)
                    
                    op_id_sea.append(log_op_sea.description)
                    op_dur_sea.append(dev_disconnect_time)                    
                    op_olc_sea.append(olc_dev_disconnect)
                    
                    op_id_sea_jour[jour].append(log_op_sea.description)
                    op_dur_sea_jour[jour].append(dev_disconnect_time)
                    op_olc_jour[jour].append(olc_dev_disconnect)
                    
                    journey[jour]['sea_id'].append(log_op_sea.description)
                    journey[jour]['sea_dur'].append(dev_disconnect_time)
                    journey[jour]['sea_olc'].append(olc_dev_disconnect)
                else:
                    
                    msg = ("Unknown 'other' method for time assessment of "
                           "this operation.")
                    module_logger.warning(msg)

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