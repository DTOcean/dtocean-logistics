# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This...
"""

import math
import datetime as dt
from datetime import timedelta
import numpy as np
import timeit

import logging
module_logger = logging.getLogger(__name__)

from ...performance.schedule.install.install_dev.schedule_dev import sched_dev
from ...performance.schedule.install.install_elec.schedule_e_export import sched_e_export
from ...performance.schedule.install.install_elec.schedule_e_array import sched_e_array
from ...performance.schedule.install.install_elec.schedule_e_dynamic import sched_e_dynamic
from ...performance.schedule.install.install_elec.schedule_e_cp_seabed import sched_e_cp_seabed
from ...performance.schedule.install.install_elec.schedule_e_cp_surface import sched_e_cp_surface
from ...performance.schedule.install.install_elec.schedule_e_external import sched_e_external
from ...performance.schedule.install.install_mf.schedule_driven import sched_driven
from ...performance.schedule.install.install_mf.schedule_gravity import sched_gravity
from ...performance.schedule.install.install_mf.schedule_m_drag import sched_m_drag
from ...performance.schedule.install.install_mf.schedule_m_direct import sched_m_direct
from ...performance.schedule.install.install_mf.schedule_m_suction import sched_m_suction
from ...performance.schedule.install.install_mf.schedule_m_pile import sched_m_pile
from ...performance.schedule.install.install_mf.schedule_s_struct import sched_s_struct


from ...ancillaries.find import indices
from ...ancillaries.diff import differences

import logging
module_logger = logging.getLogger(__name__)


def weatherWindow(metocean, olc):
    """
    this functions returns the starting times and the durations of all weather
    windows found in the met-ocean data for the given operational limit
    conditions (olc)
    """

    # Initialisation
    ww = {'start': 0,
          'duration': 0,
          'start_dt': 0,
          'end_dt': 0}

    # Operational limit conditions (consdiered static over the entire duration
    # of the marine operation fro the moment)
    time_step = metocean['hour [-]'].ix[2] - metocean['hour [-]'].ix[1]
    # resourceDataPointNb = len(met_ocean.waveHs)
    # Build the binary weather windows: 1=authorized access, 0=denied access
    if olc['maxHs']:
        if olc['maxHs'] > 0:
            Hs_bin = map(float, metocean['Hs [m]'] < olc['maxHs'])
    else:
        Hs_bin = [1]*len(metocean['Hs [m]'])
    if olc['maxTp']:
        if olc['maxTp'] > 0:
            Tp_bin = map(float, metocean['Tp [s]'] < olc['maxTp'])
    else:
        Tp_bin = [1]*len(metocean['Tp [s]'])
    if olc['maxWs']:
        if olc['maxWs'] > 0:
            Ws_bin = map(float, metocean['Ws [m/s]'] < olc['maxWs'])
    else:
        Ws_bin = [1]*len(metocean['Ws [m/s]'])
    if olc['maxCs']:
        if olc['maxCs'] > 0:
            Cs_bin = map(float, metocean['Cs [m/s]'] < olc['maxCs'])
    else:
        Cs_bin = [1]*len(metocean['Cs [m/s]'])

    WW_bin = Hs_bin or Tp_bin or Ws_bin or Cs_bin

    # Determine the durations and the starting times of the weather windows
    # Look for all indexes permitting access
    WW_authorized = indices(WW_bin, lambda x: x == 1)

    if not WW_authorized:

        pass # no message needed here as repetition with main.py

    else:
        # Return the number of consecutive time steps where marine operations
        # are not permitted ("Gap") or 0 otherwise
        WW_authorized = np.array(WW_authorized)
        index = np.array(range(len(WW_authorized)))
        WW_authorized_0 = WW_authorized - index
        WW_Gap1 = differences(WW_authorized_0)
        # Find position of consecutive permitting weather window among Gap
        WW_posConsecutiveGap1 = indices([1] + WW_Gap1, lambda x: x > 0)
        # Give the number of consecutive permitting weather conditions without
        # interuption, i.e the durations of all weather windows
        # except the last one!
        WW_findConsecutive1 = differences(WW_posConsecutiveGap1)
        st_y = []
        st_m = []
        st_d = []
        st_h = []
        st_dt = []
        et_dt = []
        ind_ww = 0
        duration = np.array(WW_findConsecutive1)*time_step
        duration = list(duration)
        WW_bin0 = [0] + WW_bin
        for ind_dt in range(len(WW_bin)):
            if WW_bin0[ind_dt] == 0 and WW_bin0[ind_dt+1] == 1:
                st_y.append(metocean['year [-]'][ind_dt+1])
                st_m.append(metocean['month [-]'][ind_dt+1])
                st_d.append(metocean['day [-]'][ind_dt+1])
                st_h.append(metocean['hour [-]'][ind_dt+1])
                st_dt.append(dt.datetime(metocean['year [-]'][ind_dt+1],
                                         metocean['month [-]'][ind_dt+1],
                                         metocean['day [-]'][ind_dt+1],
                                         metocean['hour [-]'][ind_dt+1]))
                if ind_ww < len(duration):
                    et_dt.append(st_dt[ind_ww] +
                                 dt.timedelta(hours=float(duration[ind_ww])))
                else:
                    if WW_bin0[-1] == 1:
                        last_met_dt = dt.datetime(metocean['year [-]'].tail(1),
                                                  metocean['month [-]'].tail(1),
                                                  metocean['day [-]'].tail(1),
                                                  metocean['hour [-]'].tail(1))
                        delta_dt = last_met_dt - st_dt[-1]
                        delta_h = int(delta_dt.total_seconds()//(60*60))
                        duration.append(delta_h)
                        et_dt.append(st_dt[ind_ww] +
                                     dt.timedelta(hours=duration[ind_ww]))
                    else:
                        last_ww_ind = WW_authorized[-1]
                        last_ww_dt = dt.datetime(metocean['year [-]'][last_ww_ind],
                                                 metocean['month [-]'][last_ww_ind],
                                                 metocean['day [-]'][last_ww_ind],
                                                 metocean['hour [-]'][last_ww_ind])
                        delta_dt = last_ww_dt - st_dt[-1]
                        delta_h = int(delta_dt.total_seconds()//(60*60))
                        duration.append(delta_h)
                        et_dt.append(st_dt[ind_ww] +
                                     dt.timedelta(hours=duration[ind_ww]))
                ind_ww = ind_ww + 1

        ww['start'] = {'year': st_y,
                       'month': st_m,
                       'day': st_d,
                       'hour': st_h}
        ww['start_dt'] = st_dt
        ww['end_dt'] = et_dt
        ww['duration'] = duration
    return ww


def waitingTime(log_phase, log_phase_id, metocean, rt_dt, sched_sol):
    """
    waiting time calculation based on requested time and weather window
    """
    global OLC_WW
    global OLC_WW_counter
    # initialisation
    olc = {'maxHs': [],
           'maxTp': [],
           'maxWs': [],
           'maxCs': []}
    nb_years = max(metocean['year [-]']) - min(metocean['year [-]'])
    all_wait_time = []
    for jour in range(len(sched_sol['journey'])):  # loop over the number of vessel journeys
        # isolate information from the vessel journey of interest
        journey = sched_sol['journey'][jour]
        # initialisation of the parameters for the weather window calculation
        olc = {'maxHs': [],
               'maxTp': [],
               'maxWs': [],
               'maxCs': []}
        for op_sea in range(len(journey['sea_dur'])):
            # Append OLC values previously extracted
            olc['maxHs'].append(journey['sea_olc'][op_sea][0])
            olc['maxTp'].append(journey['sea_olc'][op_sea][1])
            olc['maxWs'].append(journey['sea_olc'][op_sea][2])
            olc['maxCs'].append(journey['sea_olc'][op_sea][3])
            # replace 'nan' and negative OLC values by zero
            if olc['maxHs'][op_sea] <= 0 or math.isnan(olc['maxHs'][op_sea]):
                olc['maxHs'][op_sea] = 0
            if olc['maxTp'][op_sea] <= 0 or math.isnan(olc['maxTp'][op_sea]):
                olc['maxTp'][op_sea] = 0
            if olc['maxWs'][op_sea] <= 0 or math.isnan(olc['maxWs'][op_sea]):
                olc['maxWs'][op_sea] = 0
            if olc['maxCs'][op_sea] <= 0 or math.isnan(olc['maxCs'][op_sea]):
                olc['maxCs'][op_sea] = 0
#                print olc

        # Extract the most restrictive OLC of the sea operation 
        if any(olc_hs > 0 for olc_hs in olc['maxHs']):
            olc['maxHs'] = min(i for i in olc['maxHs'] if i > 0)
        else:
            olc['maxHs'] = 0
        if any(olc_tp > 0 for olc_tp in olc['maxTp']):
            olc['maxTp'] = min(i for i in olc['maxTp'] if i > 0)
        else:
            olc['maxTp'] = 0
        if any(olc_ws > 0 for olc_ws in olc['maxWs']):
            olc['maxWs'] = min(i for i in olc['maxWs'] if i > 0)
        else:
            olc['maxWs'] = 0
        if any(olc_cs > 0 for olc_cs in olc['maxCs']):
            olc['maxCs'] = min(i for i in olc['maxCs'] if i > 0)
        else:
            olc['maxCs'] = 0

        # Warning messages in case of very restrictive OLC
        warn_OLC = False
        msg = []

        Hs_sensible_limit = 0.5 # moved here to allow for easy update in future
        Tp_sensible_limit = 8.
        Ws_sensible_limit = 5.
        Cs_sensible_limit = 0.2

        if olc['maxHs'] > 0 and olc['maxHs'] < Hs_sensible_limit:
            
            msg.append("Significant wave height < {} m".format(
                        Hs_sensible_limit))
            warn_OLC = True

        if olc['maxTp'] > 0 and olc['maxTp'] < Tp_sensible_limit:
              
            msg.append("Peak period < {} s".format(Tp_sensible_limit))
            warn_OLC = True

        if olc['maxWs'] > 0 and olc['maxWs'] < Ws_sensible_limit:
            
            msg.append("Maximum wind speed < {} s".format(Ws_sensible_limit))
            warn_OLC = True

        if olc['maxCs'] > 0 and olc['maxCs'] < Cs_sensible_limit:
             
            msg.append("Maximum current speed < {} s".format(
                        Cs_sensible_limit))
            warn_OLC = True

        if warn_OLC: 

            msg_str = ', '.join(msg)
            module_logger.warning("Restrictive operational limit found in "
                                  "phase {}: {}".format(log_phase_id,
                                                        msg_str))

        # start_time = timeit.default_timer()      ## TIME ASSESSMENT        

        if any(value['olc'] == olc for key, value in OLC_WW.iteritems()):
            for key, value in OLC_WW.iteritems():
                if value['olc'] == olc:
                    weather_wind = OLC_WW[key]['ww']
        else:
            weather_wind = weatherWindow(metocean, olc)
            OLC_WW.update({OLC_WW_counter: {'olc': olc, 'ww': weather_wind}})
            OLC_WW_counter += 1

        # stop_time = timeit.default_timer()  # TIME ASSESSMENT

#        st_exp = rt
        wait_time = []
##                wait_time1 = []
#        st_exp_dt = dt.datetime(st_exp['year'],
#                                st_exp['month'],
#                                st_exp['day'],
#                                st_exp['hour'])
        # add onshore preparation time to expected starting date
#        st_exp_dt = rt_dt + dt.timedelta(hours = float(sched_sol['prep time']) + sum(journey['sea_dur'][0:op_sea]))
        st_exp_dt = rt_dt + dt.timedelta(hours = float(sched_sol['prep time']))
        et_exp_dt = st_exp_dt + dt.timedelta(hours = float(sched_sol['sea time']))

        # initilise the year to start looking for weather window in the metocean data
        year = min(metocean['year [-]'])

        for y in range(nb_years):  # loop over the nb of years of metocean data
            # starting time in this year of the metocean data
            # Avoiding reaching the 29th of February in a 365 days year
            if not (year % 4 == 0 and year & 100 !=0) and st_exp_dt.month == 2 and st_exp_dt.day > 28:
                st_exp_dt = st_exp_dt.replace(month=3)
                st_exp_dt = st_exp_dt.replace(day=1)
                st_exp_met_dt = dt.datetime(year,
                                            st_exp_dt.month,
                                            st_exp_dt.day,
                                            st_exp_dt.hour)
            else:
                st_exp_met_dt = dt.datetime(year,
                                            st_exp_dt.month,
                                            st_exp_dt.day,
                                            st_exp_dt.hour)
            if not (year % 4 == 0 and year & 100 !=0) and et_exp_dt.month == 2 and et_exp_dt.day > 28:
                et_exp_dt = et_exp_dt.replace(month=3)
                et_exp_dt = et_exp_dt.replace(day=1)
                et_exp_met_dt = dt.datetime(year,
                                            et_exp_dt.month,
                                            et_exp_dt.day,
                                            et_exp_dt.hour)
            else:
                et_exp_met_dt = dt.datetime(year,
                                            et_exp_dt.month,
                                            et_exp_dt.day,
                                            et_exp_dt.hour)
            # look for indexes of weather windows finishing before the expected
            # ending time
            ind_ww_ed = indices(weather_wind['end_dt'],
                                lambda x: x >= et_exp_met_dt)
            ind_ww_dur = indices(weather_wind['duration'],
                                 lambda y: y >= sched_sol['sea time'])
            ind_ww_all = set(ind_ww_ed).intersection(ind_ww_dur)

            # if not ind_ww_all:  # not a single weather window found despite the
            #     # EXIT FLAG!
            #     # print y
            #     # print et_exp_met_dt
            # # el
            if ind_ww_all:
                # find the index of the first suitable weather window
                ind_ww_first = min(ind_ww_all)
                # calculate the waiting time
                delta_wt = weather_wind['start_dt'][ind_ww_first] - st_exp_met_dt
                wt = int(delta_wt.total_seconds()//(60*60))
                if wt < 0:
                    wt = 0
                wait_time.append(wt)
                
            year = year + 1

        if wait_time:
            
            # calculate average waiting time
            mean_wait_time = sum(wait_time) / float(len(wait_time))
            all_wait_time.append(mean_wait_time)
            
            if mean_wait_time > 500:
                module_logger.warning("Long waiting time found in "
                                      "phase {}: {}".format(log_phase_id,
                                                            mean_wait_time))
            
        else:

            EXIT_FLAG = 'NoWWindows'
            return [], [], EXIT_FLAG

    journey['wait_dur'] = all_wait_time
    EXIT_FLAG = 'WeatherWindowsFound'
    return journey, st_exp_dt, EXIT_FLAG


def sched(x, y, install, log_phase, log_phase_id, site, metocean, device,
          sub_device, entry_point, layout, collection_point, dynamic_cable, static_cable,
          cable_route, connectors, external_protection, topology, line,
          foundation, penet_rates, laying_rates, other_rates):

    # initialisation
    global OLC_WW
    global OLC_WW_counter

    OLC_WW = {0: {'olc': {}, 'ww': {}}}
    OLC_WW_counter = 0

    sol = {}
    # end_dt_last = [] # to make only devices work?!?!?!!!
    for seq in range(len(log_phase.op_ve)):  # loop over the number of
        # operation
        # Initialisation
        sol[seq] = []

        # loop over the number of solutions, i.e feasible combinations of
        # port/vessel(s)/equipment(s)
        for ind_sol in range(len(log_phase.op_ve[seq].sol)):
            
            # start_time = timeit.default_timer()  # TIME ASSESSMENT

            # print 'seq: ' + str(seq) + ', sol: ' + str(ind_sol)

            sol[seq].append([])
            sched_sol = {'total time': [],
                         'prep time': [],
                         'sea time': [],
                         'weather windows': [],
                         'waiting time': [],
                         'global': {},
                         'journey': {},
                         'details per journey': {},
                         'transit time': []
                         }

            # check the nature of the logistic phase
            if log_phase_id == 'Devices':
                sched_sol = sched_dev(seq, ind_sol, install, log_phase, site, entry_point,
                                      device, sub_device, layout, sched_sol)
            elif log_phase_id == 'E_export':
                sched_sol = sched_e_export(seq, ind_sol, install, log_phase,
                                           site, entry_point,
                                           static_cable, cable_route,
                                           laying_rates, other_rates,
                                           sched_sol)
            elif log_phase_id == 'E_array':
                sched_sol = sched_e_array(seq, ind_sol, install, log_phase,
                                          site, entry_point,
                                          static_cable, cable_route,
                                          laying_rates, other_rates,
                                          sched_sol)
            elif log_phase_id == 'E_dynamic':
                sched_sol = sched_e_dynamic(seq, ind_sol, install, log_phase,
                                            site, entry_point,
                                            dynamic_cable, other_rates,
                                            sched_sol)
            elif log_phase_id == 'E_cp_seabed':
                sched_sol = sched_e_cp_seabed(seq, ind_sol, install, log_phase,
                                              site, entry_point,
                                              collection_point, sched_sol)
            elif log_phase_id == 'E_cp_surface':
                sched_sol = sched_e_cp_surface(seq, ind_sol, install,
                                               log_phase, site, entry_point,
                                               collection_point, sched_sol)
            elif log_phase_id == 'E_external':
                sched_sol = sched_e_external(seq, ind_sol, install,
                                               log_phase, site, entry_point,
                                               external_protection, sched_sol)
            elif log_phase_id == 'Driven':
                sched_sol = sched_driven(seq, ind_sol, install, log_phase,
                                         site, entry_point, device, foundation,
                                         penet_rates, other_rates, sched_sol)
            elif log_phase_id == 'Gravity':
                sched_sol = sched_gravity(seq, ind_sol, install, log_phase,
                                          site, entry_point, device, layout, foundation,
                                          sched_sol)
            elif log_phase_id == 'M_direct':
                sched_sol = sched_m_direct(seq, ind_sol, install, log_phase,
                                           site, entry_point, device, layout, foundation,
                                           penet_rates, sched_sol)
            elif log_phase_id == 'M_suction':
                sched_sol = sched_m_suction(seq, ind_sol, install, log_phase,
                                            site, entry_point, device, layout, foundation,
                                            penet_rates, sched_sol)
            elif log_phase_id == 'M_drag':
                sched_sol = sched_m_drag(seq, ind_sol, install, log_phase,
                                         site, entry_point, device, layout, foundation,
                                         sched_sol)
            elif log_phase_id == 'M_pile':
                sched_sol = sched_m_pile(seq, ind_sol, install, log_phase,
                                         site, entry_point, device, layout, foundation,
                                         sched_sol)
            elif log_phase_id == 'S_structure':
                sched_sol = sched_s_struct(seq, ind_sol, install, log_phase,
                                           site, entry_point, device, sub_device, layout,
                                           sched_sol)
            else:
                
                msg = ("Unknown logistic phase ID: {}".format(log_phase_id))
                module_logger.warning(msg)

            # requested time to start the logistic phase 
            if x == min(install['plan']):  # find 1st layer of installation plan

                start_proj = device['Project start date [-]'].ix[0]        

                if isinstance(start_proj, dt.datetime):

                    rt_dt = start_proj

                else:

                    rt = {'year': int(start_proj[6:10]),
                          'month': int(start_proj[3:5]),
                          'day': int(start_proj[0:2]),
                          'hour': int(start_proj[11:13]),
                          'min': int(start_proj[14:16])}

                    rt_dt = dt.datetime(rt['year'],
                                        rt['month'],
                                        rt['day'],
                                        rt['hour'])

                end_dt_last = install['end_dt']

            elif x > min(install['plan']):  # assess extra layers of installation plan

                end_dt_last = install['end_dt']

                if x - 1 in install['plan']:

                    for y in range(len(install['plan'][x - 1])):

                        last_log_id_outcome = install['plan'][x - 1][y]

                        if type(last_log_id_outcome) is dict:

                            end_dt_last.append(
                                last_log_id_outcome['DATE']['End Date'])

                if not end_dt_last:

                    start_proj = device['Project start date [-]'].ix[0]             
                    
                    if isinstance(start_proj, dt.datetime):

                        rt_dt = start_proj

                    else:
 
                        rt = {'year': int(start_proj[6:10]),
                              'month': int(start_proj[3:5]),
                              'day': int(start_proj[0:2]),
                              'hour': int(start_proj[11:13]),
                              'min': int(start_proj[14:16])}
 
                        rt_dt = dt.datetime(rt['year'],
                                            rt['month'],
                                            rt['day'],
                                            rt['hour'])

                    end_dt_last = [rt_dt]

                else:

                    if type(end_dt_last) is list:

                        last_end_time = max(end_dt_last)
                        rt_dt = last_end_time

                    else:

                        rt_dt = end_dt_last

            journey, st_exp_dt, WWINDOW_FLAG = waitingTime(log_phase,
                                                           log_phase_id,
                                                           metocean, rt_dt,
                                                           sched_sol)

            # stop_time1 = timeit.default_timer()  # TIME ASSESSMENT   

            if WWINDOW_FLAG == 'NoWWindows':

                return [], [], [], WWINDOW_FLAG

            if not sched_sol['waiting time']:

                sched_sol['waiting time'] = journey['wait_dur']

            else:

                sched_sol['waiting time'] = \
                    sched_sol['waiting time'] + journey['wait_dur']
#            sched_sol['weather windows'] = weather_wind

            sched_sol['total time'] = sched_sol['total time'] + sched_sol['waiting time']
            # sched_sol['transit time'] = sched_sol['total time'] - sched_sol['waiting time'] - sched_sol['prep time']

            log_phase.op_ve[seq].sol[ind_sol]['schedule'] = sched_sol
            log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows start_dt'] = st_exp_dt
            log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows depart_dt'] = st_exp_dt + timedelta(hours = sum(sched_sol['waiting time']))
            log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows end_dt'] = st_exp_dt  + timedelta(hours = sum(sched_sol['waiting time'])) +  timedelta(hours = sched_sol['sea time'])

            sol[seq][ind_sol] = sched_sol

            # stop_time = timeit.default_timer()  # TIME ASSESSMENT
            # print 'Solution Duration [s]: ' + str(stop_time - start_time)  # TIME ASSESSMENT

    EXIT_FLAG = 'ScheduleFound'

    return sol, end_dt_last, log_phase, EXIT_FLAG
