# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is responsible for the interphase relation between the different
logistic phases during installation. The inputs from the user and other DTOcean
packages build up unique projects which require specific installation sequences.
The functions in this module return the installation sequence required based on
some pre-defined cases (type of foundations, type of moorings, type of device,
type of electrical infranstrucutres).

BETA VERSION NOTES: the methodology was defined and implemented, should not
suffer major changes on the next version of the code. However the content (the
installation sequences) will be updated.
"""

import numpy as np
import pandas as pd
from ....phases.select_port import distance
from ....ancillaries.find import indices
from ....ancillaries.nanTOzero import nan2zero
import math

import logging
module_logger = logging.getLogger(__name__)


def sched_site(log_phase_id, seq, ind_sol, log_phase, site, layout, entry_point,
               om, sched_sol):
    """sched_dev determines the duration of each individual logistic operations
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
    user_inputs: dict
     dictionary contaning four panda DataFrames collecting information on the
     site, on the device (and sub_device) and on the metocean 
    om : panda DataFrame
     DataFrame containing all required inputs to WP5 coming from WP6
    ...

    Returns
    -------
    sched_sol : dict
     dictionary containing the results from the time values assessment of the 
     durations of all onshore operations and offshore operations for each
     feasible logistic solutions
    """
    
    """
    Initialise variables
    """
    # initialise list containing the time value durations and OLC
    op_id_prep = []
    op_dur_prep = []
    op_id_sea = []
    op_dur_sea = []
    op_olc_sea = []
    op_id_demob = []
    op_dur_demob = []
    op_id_prep_jour = {0: []}
    op_dur_prep_jour = {0: []}
    op_id_sea_jour = {0: []}
    op_dur_sea_jour = {0: []}
    op_id_demob_jour = {0: []}
    op_dur_demob_jour = {0: []}
    op_olc_jour = {0: []}
    # use the proper names of the pandas as sent to WP1
    om = om
    # obtain first maintenance id from om
    df_index = om.index.values
    om_id = om['ID [-]'].ix[df_index[0]]
    # number of elements to transport to site    
    nb_elem = len(om)
    # number of vessel type in this feasible solution
    nb_ves_type = range(len(log_phase.op_ve[seq].sol[ind_sol]['VEs']))
    # list of the vessel(s) and equipment combination used for this feasible solution
    ve_combi = log_phase.op_ve[seq].sol[ind_sol]['VEs']
    
#    device = user_inputs['device']
    """
    Time assessment for the logistic phase
    """
    # initialise the area and dry mass list
    elem_area = [0]*nb_elem
    elem_mass = [0]*nb_elem
    cable_mass = [0]*nb_elem
    for el in range(nb_elem):  # loop over the number of elements
        if log_phase_id == 'LpM5':
            cable_mass[el] = float(om['sp_dry_mass [kg]'].ix[el])/1000  # [ton]    
        elif log_phase_id == 'LpM8':
            if om_id == 'RtP5':  # mooring replacement
                # initialise the mooring lenght
                moor_length = [0]*nb_elem
                for el in range(nb_elem):  # loop over the number of elements
                    # add
                    moor_length[el] = float(om['sp_length [m]'].ix[el])

            if om_id == 'RtP6':  # umbilical replacement
                # initialise the area and dry mass list
                cable_mass = [0]*nb_elem
                for el in range(nb_elem):  # loop over the number of elements
                    # calculate the area and dry mass of all elements
                    cable_mass[el] = float(om['sp_dry_mass [kg]'].ix[el])/1000  # [ton]
        else:
            # calculate the area and dry mass of all elements
            elem_area[el] = float(om['sp_length [m]'].ix[el])*float(om['sp_width [m]'].ix[el])  # [m^2]
            elem_mass[el] = float(om['sp_dry_mass [kg]'].ix[el])/1000  # [ton]

    nb_elem_port = nb_elem  # initialise the number of elements to be transported that are initially at port
    nb_journey = 0  # initialise the number of vessel journeys
    nb_el_journey = []  # initialise the list of number of elements per journey
    while nb_elem_port > 0:
        # extract the panda series of the transporting vessel
        # assumption: the first vessel is always the transporting vessel
        sol_pd_series = log_phase.op_ve[seq].sol[ind_sol]['VEs'][0][2]
        if log_phase_id == 'LpM5':
            # extract the deck area and cargo
            turntable_total_loading = sol_pd_series.ix['Turntable number [-]'] * sol_pd_series.ix['Turntable loading [t]']

            # determine the cumulative list of element areas and dry masses (equipment included???!)
            eq_loading = [0]  # only cable considered
            cable_mass_accum = np.add(np.cumsum(cable_mass), eq_loading).tolist()

            nb_el_turntable = indices(cable_mass_accum, lambda x: x>turntable_total_loading)
            if not nb_el_turntable:
                nb_el_turntable = len(cable_mass_accum)
            else:
                nb_el_turntable = min(nb_el_turntable)

            nb_el_journey.append(nb_el_turntable)

            # update the number of elements remaining at port and their areas/masses lists
            if nb_el_journey[nb_journey] == nb_elem_port:
                nb_elem_port = 0
            elif nb_el_journey[nb_journey] == 0:
                # error that means not a single element can fit!
                msg = ("No single element can fit on the deck.")
                module_logger.warning(msg)
            else:
                nb_elem_port = nb_elem_port - nb_el_journey[nb_journey]
                cable_mass = cable_mass[nb_el_journey[-1]:]
            # update the number of vessel journeys
            nb_journey = nb_journey + 1
        elif log_phase_id == 'LpM8':
            # number of equipment in the main vessel
            nb_eq = len(log_phase.op_ve[seq].sol[ind_sol]['VEs'][0])-3
            # extract the deck area and cargo
            deck_area = sol_pd_series.ix['Deck space [m^2]']
            deck_cargo = sol_pd_series.ix['Max. cargo [t]']
            drum_cap = sol_pd_series.ix['AH drum capacity [m]']
            # calculate the footprint and the weight due to the equipment
            eq_area = [0]
            eq_cargo = [0]

            if nb_eq>0:
                for ind_eq in range(nb_eq):
                    sol_pd_eq_series = log_phase.op_ve[seq].sol[ind_sol]['VEs'][0][ind_eq+3][2]
                    sol_type_eq = log_phase.op_ve[seq].sol[ind_sol]['VEs'][0][ind_eq+3][0]
                    if sol_type_eq == 'rov':
                        eq_area.append( sol_pd_eq_series.ix['Length [m]']*sol_pd_eq_series.ix['Width [m]'] + sol_pd_eq_series.ix['AE footprint [m^2]'] )
                        eq_cargo.append( sol_pd_eq_series.ix['Weight [t]'] + sol_pd_eq_series.ix['AE weight [t]'] )
            eq_area_max = sum(eq_area)
            eq_cargo_max = sum(eq_cargo)
    
            # determine the cumulative list of element areas and dry masses (equipment included???!)
    
            if om_id == 'RtP5':  # mooring line replacement
                elem_lenght_accum = list(np.cumsum(moor_length))
                # determine the maximum number of elements that can fit on-deck due to max deck area or max deck cargo or winch drum limitations
                nb_el_lenght = indices(elem_lenght_accum,
                                       lambda x: x > drum_cap)
                if not nb_el_lenght:
                    nb_el_lenght = len(elem_lenght_accum)
                else:
                    nb_el_lenght = min(nb_el_lenght)
                nb_el_journey.append(nb_el_lenght)
                
            if om_id == 'RtP6':  # umbilical replacement
                elem_mass_accum = list(np.add(np.cumsum(cable_mass), eq_cargo_max))
                # determine the maximum number of elements that can fit on-deck due to max deck area or max deck cargo or winch drum limitations
                nb_el_mass = indices(elem_mass_accum,
                                     lambda x: x > deck_cargo)
                if not nb_el_mass:
                    nb_el_mass = len(elem_mass_accum)
                else:
                    nb_el_mass = min(nb_el_mass)
                nb_el_journey.append(nb_el_mass)

            # update the number of elements remaining at port and their areas/masses lists
            if nb_el_journey[nb_journey] == nb_elem_port:
                nb_elem_port = 0
            elif nb_el_journey[nb_journey] == 0:
                # error that means not a single element can fit!
                msg = ("No single element can fit on the deck.")
                module_logger.warning(msg)
            else:
                nb_elem_port = nb_elem_port - nb_el_journey[nb_journey]
                if om_id == 'RtP5':  # umbilical replacement
                    moor_length = moor_length[nb_el_journey[-1]:]
                if om_id == 'RtP6':  # umbilical replacement
                    cable_mass = cable_mass[nb_el_journey[-1]:]
            # update the number of vessel journeys
            nb_journey = nb_journey + 1

        else:
            # number of equipment in the main vessel   
            nb_eq = len(log_phase.op_ve[seq].sol[ind_sol]['VEs'][0])-3
            # extract the deck area and cargo
            deck_area = sol_pd_series.ix['Deck space [m^2]']
            deck_cargo = sol_pd_series.ix['Max. cargo [t]']
            # calculate the footprint and the weight due to the equipment
            eq_area = [0]
            eq_cargo = [0]
            if nb_eq>0:
                for ind_eq in range(nb_eq):
                    sol_pd_eq_series = log_phase.op_ve[seq].sol[ind_sol]['VEs'][0][ind_eq+3][2]
                    sol_type_eq = log_phase.op_ve[seq].sol[ind_sol]['VEs'][0][ind_eq+3][0]
                    if sol_type_eq == 'rov':
                        eq_area.append( sol_pd_eq_series.ix['Length [m]']*sol_pd_eq_series.ix['Width [m]'] + sol_pd_eq_series.ix['AE footprint [m^2]'] )
                        eq_cargo.append( sol_pd_eq_series.ix['Weight [t]'] + sol_pd_eq_series.ix['AE weight [t]'] )
                    elif sol_type_eq == 'divers':
                        eq_area.append( sol_pd_eq_series.ix['Deployment eq. footprint [m^2]'] )
                        eq_cargo.append( sol_pd_eq_series.ix['Deployment eq. weight [t]'] )
            eq_area_max = sum(eq_area)
            eq_cargo_max = sum(eq_cargo)
            # determine the cumulative list of element areas and dry masses (equipment included???!)
            elem_area_accum = list(np.add(np.cumsum(elem_area), eq_area_max))
            elem_mass_accum = list(np.add(np.cumsum(elem_mass), eq_cargo_max))
            # determine the maximum number of elements that can fit on-deck due to max deck area or max deck cargo limitations
            nb_el_area = indices(elem_area_accum, lambda x: x>deck_area)
            if not nb_el_area:
                nb_el_area = len(elem_area_accum)
            else:
                nb_el_area = min(nb_el_area)
            nb_el_mass = indices(elem_mass_accum, lambda x: x>deck_cargo)
            if not nb_el_mass:
                nb_el_mass = len(elem_mass_accum)
            else:
                nb_el_mass = min(nb_el_mass)
            nb_el_journey.append(min([nb_el_area,nb_el_mass]))
            # update the number of elements remaining at port and their areas/masses lists
            if nb_el_journey[nb_journey] == nb_elem_port:
                nb_elem_port = 0
            elif nb_el_journey[nb_journey] == 0:
                # error that means not a single element can fit!
                msg = ("No single element can fit on the deck.")
                module_logger.warning(msg)
            else:
                nb_elem_port = nb_elem_port - nb_el_journey[nb_journey]
                elem_area = elem_area[nb_el_journey[-1]:]
                elem_mass = elem_mass[nb_el_journey[-1]:]
            # update the number of vessel journeys
            nb_journey = nb_journey + 1
        
        ind_el = 0
    for jour in range(nb_journey):
        journey=sched_sol['journey']
        journey[jour] = {'prep_id': [],
                         'prep_dur': [],
                         'sea_id': [],
                         'sea_dur': [],
                         'sea_olc': [],
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
                if log_op_prep.description == "Vessel preparation & loading": # CHANGED TO WP6 INPUT!!
                    log_op_prep.time_value = om['Prep_time [h]'][0]
                    op_dur_prep.append(log_op_prep.time_value)
                    op_id_prep.append(log_op_prep.description)
                    op_id_prep_jour[jour].append(log_op_prep.description)
                    op_dur_prep_jour[jour].append(log_op_prep.time_value)
                    journey[jour]['prep_id'].append(log_op_prep.description)
                    journey[jour]['prep_dur'].append(log_op_prep.time_value)
                else:
                    msg = ("Unknown default value time value duration for "
                           "this logistic operation associated with the "
                           "logistic phase for maintenance.")
                    module_logger.warning(msg)
            elif not pd.isnull(time_method[1]): # function
                # type of function
                msg = ("No functions are currently available for onshore "
                       "operations.")
                module_logger.warning(msg)
                    
            elif not pd.isnull(time_method[2]):
                if jour==0:
                    if log_op_prep.time_other == "vesselsDB['Mob time [h]']":
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
                    else:
                        msg = ("Unknown 'other' method for time value "
                               "duration assessment of this operation.")
                        module_logger.warning(msg)
    #                only required if there are different element type which is not possible for devices

        for el_id, row in om.iterrows(): # loop over the number of element type
            # number of operation sequence in the sea-work phase
            nb_op_sea = len(log_phase.op_ve[seq].op_seq_sea[el_id])
#                nb_op_sea = len(log_phase.op_ve[seq].op_seq_sea[0])
        # determine the duration of the logistic phase sea-work
#        for el in nb_el_journey[jour]: # loop over the nb of elements per journey
        for op_sea in range(nb_op_sea): # loop over the nb of offshore logistic operations
            log_op_sea = log_phase.op_ve[seq].op_seq_sea[el_id][op_sea]
            # create a panda series suitable for the discrimination
            # between type of methods for time assessment
            time_method = pd.Series([log_op_sea.time_value,
                                     log_op_sea.time_function,
                                     log_op_sea.time_other])  
            # discriminate between the time assessment methods
            if not pd.isnull(time_method[0]): # default value
                # type of logistic operation
                if log_op_sea.description == "Vessel Positioning": # vessel positioning
                    # vessel type
                    if ve_combi[0][2].ix['Vessel type [-]'] == "JUP Barge" or ve_combi[0][2].ix['Vessel type [-]'] == "JUP Vessel":
#                                    for dev in nb_el_journey[jour]:# water depth at each device location...
#                                        water_depth
#                                    UTM_dev_z = layout['zone [-]'].ix[0] 
                        water_depth_dev = om['Bathymetry [m]'].ix[0]
                        jacking_time = water_depth_dev/ve_combi[0][2].ix['JackUp speed down [m/min]']*60.0 # [8hour]
                        op_dur_sea.append(nb_el_journey[jour]*jacking_time)
                        olc_Hs = ve_combi[0][2].ix['OLC: Jacking maxHs [m]']
                        olc_Tp = ve_combi[0][2].ix['OLC: Jacking maxTp [s]']
                        olc_Ws = ve_combi[0][2].ix['OLC: Jacking maxWs [m/s]']
                        olc_Cs = ve_combi[0][2].ix['OLC: Jacking maxCs [m/s]']#*0.514444
                        olc_jack = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                        op_olc_sea.append(olc_jack)
                        op_id_sea.append(log_op_sea.description)
                        op_id_sea_jour[jour].append(log_op_sea.description)
                        op_dur_sea_jour[jour].append(nb_el_journey[jour]*jacking_time)
                        op_olc_jour[jour].append(olc_jack)
                        journey[jour]['sea_id'].append(log_op_sea.description)
                        journey[jour]['sea_dur'].append(nb_el_journey[jour]*jacking_time)
                        journey[jour]['sea_olc'].append(olc_jack)
                    else: 
                        op_dur_sea.append(nb_el_journey[jour]*log_op_sea.time_value)
                        olc_Hs = ve_combi[0][2].ix['OLC: Transit maxHs [m]']
                        olc_Tp = ve_combi[0][2].ix['OLC: Transit maxTp [s]']
                        olc_Ws = ve_combi[0][2].ix['OLC: Transit maxWs [m/s]']
                        olc_Cs = ve_combi[0][2].ix['OLC: Transit maxCs [m/s]']#*0.514444
                        olc_trans = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                        olc_trans = nan2zero(olc_trans)
                        op_olc_sea.append(olc_trans)
                        op_id_sea.append(log_op_sea.description)
                        op_id_sea_jour[jour].append(log_op_sea.description)
                        op_dur_sea_jour[jour].append(nb_el_journey[jour]*log_op_sea.time_value)
                        op_olc_jour[jour].append(olc_trans)
                        journey[jour]['sea_id'].append(log_op_sea.description)
                        journey[jour]['sea_dur'].append(nb_el_journey[jour]*log_op_sea.time_value)
                        journey[jour]['sea_olc'].append(olc_trans)
            elif not pd.isnull(time_method[1]): # function
                # type of function
                if log_op_sea.time_function == "transit_algorithm":
#                            port_pd = log_phase.op_ve[seq].sol[ind_sol]['port']
#                            UTM_port = [port_pd.ix['UTM x [m]'],
#                                        port_pd.ix['UTM y [m]'],
#                                        port_pd.ix['UTM zone [-]']]
#                            site = user_inputs['site']
#                            UTM_site = [site['x coord [m]'].ix[0],
#                                        site['y coord [m]'].ix[0],
#                                        site['zone [-]'].ix[0]]
#                            port_2_site_dist = transit_algorithm(UTM_port, UTM_site)
                    port_2_site_dist = om['Dist_port [km]'].ix[0]
                    UTM_site = [entry_point['x coord [m]'].ix[0],
                                entry_point['y coord [m]'].ix[0],
                                entry_point['zone [-]'].ix[0]]
                    UTM_el_0 = [om['x coord [m]'].ix[ind_el],
                                om['y coord [m]'].ix[ind_el],
                                om['zone [-]'].ix[ind_el]]
                    site_2_el_dist = distance(UTM_site,UTM_el_0)
                    # loop over the nb of vessel types  
                    ves_speed = [] 
                    olc = []                                       
                    for vt in nb_ves_type:
                        ves_speed.append(ve_combi[vt][2].ix['Transit speed [m/s]'])
                        ves_type = ve_combi[vt][2].ix['Vessel type [-]']
                        olc_method = log_op_sea.olc
                        if any(olc_method[op] == "vessel" for op in range(len(olc_method))):
                            if ves_type == "JUP Barge" or ves_type == "JUP Vessel":
                                olc_Hs = ve_combi[0][2].ix['OLC: Jacking maxHs [m]']
                                olc_Tp = ve_combi[0][2].ix['OLC: Jacking maxTp [s]']
                                olc_Ws = ve_combi[0][2].ix['OLC: Jacking maxWs [m/s]']
                                olc_Cs = ve_combi[0][2].ix['OLC: Jacking maxCs [m/s]']
                                olc_jack = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                                olc_jack = nan2zero(olc_jack)
                                olc.append(olc_jack)
                                
#                                op_olc_sea.append(olc_jack)
#                                op_olc_jour[jour].append(olc_jack)
#                                
#                                journey[jour]['sea_olc'].append(olc_jack)
                            else:
                                olc_Hs = ve_combi[0][2].ix['OLC: Transit maxHs [m]']
                                olc_Tp = ve_combi[0][2].ix['OLC: Transit maxTp [s]']
                                olc_Ws = ve_combi[0][2].ix['OLC: Transit maxWs [m/s]']
                                olc_Cs = ve_combi[0][2].ix['OLC: Transit maxCs [m/s]']
                                olc_trans = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                                olc_trans = nan2zero(olc_trans)
                                olc.append(olc_trans)
                                
#                                op_olc_sea.append(olc_trans)
#                                op_olc_jour[jour].append(olc_trans)
#                                
#                                journey[jour]['sea_olc'].append(olc_trans)
                    olc = np.min(olc,0).tolist()
                    op_olc_sea.append(olc)
                    op_olc_jour[jour].append(olc)
                    ves_slow = 3.6*min(ves_speed) # [km/h]
                    port_2_site_time = (port_2_site_dist + site_2_el_dist)/ves_slow
                    # append transit time from port to site
                    op_dur_sea.append(port_2_site_time)
                    op_id_sea.append(log_op_sea.description)
                    op_id_sea_jour[jour].append(log_op_sea.description)
                    op_dur_sea_jour[jour].append(port_2_site_time)
                    journey[jour]['sea_id'].append(log_op_sea.description)
                    journey[jour]['sea_dur'].append(port_2_site_time)
                    journey[jour]['sea_olc'].append(olc)
                    
                elif log_op_sea.time_function == "distance":
                    dist_tot = 0
                    dist_el = []
                    if nb_elem > 1:    
                        for el in range(nb_el_journey[jour]-1):
                            UTM_el_i = [om['x coord [m]'].ix[ind_el+el],
                                        om['y coord [m]'].ix[ind_el+el],
                                        om['zone [-]'].ix[ ind_el+el]]
                            UTM_el_f = [om['x coord [m]'].ix[ind_el+el+1],
                                        om['y coord [m]'].ix[ind_el+el+1],
                                        om['zone [-]'].ix[ind_el+el+1]]
                            dist_el.append(distance(UTM_el_i,UTM_el_f))
                            dist_tot = dist_tot + dist_el[el]
                    ves_speed = []
                    olc = []
                    for vt in nb_ves_type:
                        ves_type = ve_combi[vt][2].ix['Vessel type [-]']
                        ves_speed.append(ve_combi[vt][2].ix['Transit speed [m/s]'])
                        olc_method = log_op_sea.olc
                        if any(olc_method[op] == "vessel" for op in range(len(olc_method))):
                            if ves_type == "JUP Barge" or ves_type == "JUP Vessel":
                                olc_Hs = ve_combi[0][2].ix['OLC: Jacking maxHs [m]']
                                olc_Tp = ve_combi[0][2].ix['OLC: Jacking maxTp [s]']
                                olc_Ws = ve_combi[0][2].ix['OLC: Jacking maxWs [m/s]']
                                olc_Cs = ve_combi[0][2].ix['OLC: Jacking maxCs [m/s]']#*0.514444
                                olc_jack = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                                olc_jack = nan2zero(olc_jack)
                                olc.append(olc_jack)
                            else:
                                olc_Hs = ve_combi[0][2].ix['OLC: Transit maxHs [m]']
                                olc_Tp = ve_combi[0][2].ix['OLC: Transit maxTp [s]']
                                olc_Ws = ve_combi[0][2].ix['OLC: Transit maxWs [m/s]']
                                olc_Cs = ve_combi[0][2].ix['OLC: Transit maxCs [m/s]']#*0.514444
                                olc_trans = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                                olc_trans = nan2zero(olc_trans)
                                olc.append(olc_trans)
                    olc = np.min(olc,0).tolist()
                    op_olc_sea.append(olc)
                    op_olc_jour[jour].append(olc)
                    ves_slow = 3.6*min(ves_speed) # [km/h]
                    site_2_site_time = dist_tot/ves_slow
                    # append transit time from site to site
                    op_dur_sea.append(site_2_site_time)
                    op_id_sea.append(log_op_sea.description)
                    op_id_sea_jour[jour].append(log_op_sea.description)
                    op_dur_sea_jour[jour].append(site_2_site_time)
                    journey[jour]['sea_id'].append(log_op_sea.description)
                    journey[jour]['sea_dur'].append(site_2_site_time)
                    journey[jour]['sea_olc'].append(olc)

            elif not pd.isnull(time_method[2]):
                if log_op_sea.time_other == "om['d_acc [hour]']":
                    el_acc_time = om['d_acc [hour]'].ix[ind_el]
                    op_id_sea.append(log_op_sea.description)
                    op_dur_sea.append(el_acc_time) 
                    olc_Hs = om['Hs_acc [m]'].ix[ind_el]
                    olc_Tp = om['Tp_acc [s]'].ix[ind_el]
                    olc_Ws = om['Ws_acc [m/s]'].ix[ind_el]
                    olc_Cs = om['Cs_acc [m/s]'].ix[ind_el]
                    olc_el_acc = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                    olc_el_acc = nan2zero(olc_el_acc)
                    op_olc_sea.append(olc_el_acc)
                    op_id_sea_jour[jour].append(log_op_sea.description)
                    op_dur_sea_jour[jour].append(el_acc_time)
                    op_olc_jour[jour].append(olc_el_acc)
                    journey[jour]['sea_id'].append(log_op_sea.description)
                    journey[jour]['sea_dur'].append(el_acc_time)
                    journey[jour]['sea_olc'].append(olc_el_acc)
                elif log_op_sea.time_other == "om['d_om [hour]']":
                    el_om_time = om['d_om [hour]'].ix[ind_el]
                    op_id_sea.append(log_op_sea.description)
                    op_dur_sea.append(el_om_time)
                    olc_Hs = om['Hs_om [m]'].ix[ind_el]
                    olc_Tp = om['Tp_om [s]'].ix[ind_el]
                    olc_Ws = om['Ws_om [m/s]'].ix[ind_el]
                    olc_Cs = om['Cs_om [m/s]'].ix[ind_el]
                    olc_el_om = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                    olc_el_om = nan2zero(olc_el_om)
                    op_olc_sea.append(olc_el_om)
                    op_id_sea_jour[jour].append(log_op_sea.description)
                    op_dur_sea_jour[jour].append(el_om_time)
                    op_olc_jour[jour].append(olc_el_om)
                    journey[jour]['sea_id'].append(log_op_sea.description)
                    journey[jour]['sea_dur'].append(el_om_time)
                    journey[jour]['sea_olc'].append(olc_el_om)
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
        op_id_demob_jour[nb_journey-1].append(log_op_demob.description)
        op_dur_demob_jour[nb_journey-1].append(ves_demob_time_long)
    else:
        msg = ("Only demob is allowed at the end of a logistic phase.")
        module_logger.warning(msg)

    """
    Format outputs
    """
    sched_sol['global'] = {'nb of journeys': nb_journey,
                           'nb of elements per journey': nb_el_journey,
                           'prep': [op_id_prep, op_dur_prep],
                           'sea': [op_id_sea, op_dur_sea, op_olc_sea],
                           'demob': [op_id_demob, op_dur_demob]}
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
    sched_sol['total time'] = sched_sol['prep time'] + sched_sol['sea time'] + op_dur_demob_clean
    return sched_sol
            

# see = selectSeq(end_user_inputs, WP3_outputs, WP4_outputs)

