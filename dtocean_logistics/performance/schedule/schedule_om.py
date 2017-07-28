# -*- coding: utf-8 -*-
'unknown return to port status'# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 11:53:24 2015

@author: BTeillant
"""

# Set up logging
import logging
module_logger = logging.getLogger(__name__)

import math
import datetime as dt
from datetime import timedelta
import numpy as np
import timeit


from ...performance.schedule.om.schedule_site import sched_site
from ...performance.schedule.om.schedule_retrieve import sched_retrieve
from ...performance.schedule.om.schedule_replace import sched_replace

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
        
        msg = ("No weather window found for the given metocean data and "
               "selected installation vessel.")
        module_logger.warning(msg)

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


def waitingTime(log_phase, log_phase_id, metocean, om, sched_sol):
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
    # requested time to start the logistic phase
    rt = om['t_start [-]'][0] 
    requested_time = {'year': int(rt[6:10]),
                      'month': int(rt[3:5]),
                      'day': int(rt[0:2]),
                      'hour': int(rt[11:13]),
                      'min': int(rt[14:16])}
    nb_years = max(metocean['year [-]']) - min(metocean['year [-]']) + 1
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
#        print olc
        start_time = timeit.default_timer()      ## TIME ASSESSMENT

        if any(value['olc'] == olc for key, value in OLC_WW.iteritems()):
            for key, value in OLC_WW.iteritems():
                if value['olc'] == olc:
                    weather_wind = OLC_WW[key]['ww']
        else:
            weather_wind = weatherWindow(metocean, olc)
            OLC_WW.update( {OLC_WW_counter:{'olc':olc, 'ww': weather_wind}} )
            OLC_WW_counter += 1

        # weather_wind = weatherWindow(metocean, olc)

        stop_time = timeit.default_timer()      ## TIME ASSESSMENT

        #  add preparation time to starting time TO-DO...
#            if sched_sol['preparation'] > 0: # there is preparation time to account for
#                if sched_sol['preparation'] > 
        st_exp = requested_time
        wait_time = []
#                wait_time1 = []
        st_exp_dt = dt.datetime(st_exp['year'],
                                st_exp['month'],
                                st_exp['day'],
                                st_exp['hour'])
        # add onshore preparation time to expected starting date
        if log_phase_id == 'LpM6' or log_phase_id == 'LpM7':
            if sched_sol['RtP'] == 'retrieve':
                st_exp_dt = st_exp_dt + dt.timedelta(hours = float(sched_sol['prep time_retrieve']))
                et_exp_dt = st_exp_dt + dt.timedelta(hours = float(sched_sol['sea time_retrieve']))
            elif sched_sol['RtP'] == 'replace':
                st_exp_dt = sched_sol['st_rts_dt'] + dt.timedelta(hours = float(sched_sol['prep time_replace']))
                et_exp_dt = sched_sol['st_rts_dt'] + dt.timedelta(hours = float(sched_sol['sea time_replace']))
            else:
                msg = ("Unknown return to port status {}. Allowed: 'retieve' "
                       "or 'replace'".format(sched_sol['RtP']))
                module_logger.warning(msg)

        else:
            st_exp_dt = st_exp_dt + dt.timedelta(hours = float(sched_sol['prep time']))
            et_exp_dt = st_exp_dt + dt.timedelta(hours = float(sched_sol['sea time']))
        # initilise the year to start looking for weather window in the metocean data
        year = min(metocean['year [-]'])

        for y in range(nb_years):  # loop over the nb of years of metocean data
            # starting time in this year of the metocean data
#            if year % 4 == 0 and st_exp_dt.month == 2 and st_exp_dt.month > 28:
            if not (year % 4 == 0 and year & 100 !=0) and st_exp_dt.month == 2 and st_exp_dt.day > 28:
                st_exp_dt = st_exp_dt.replace(month = 3)
                st_exp_dt = st_exp_dt.replace(day = 1)
                st_exp_met_dt = dt.datetime(year,
                                            st_exp_dt.month,
                                            st_exp_dt.day,
                                            st_exp_dt.hour)
            else:
                st_exp_met_dt = dt.datetime(year,
                                            st_exp_dt.month,
                                            st_exp_dt.day,
                                            st_exp_dt.hour)
            # ending time in this year of the metocean data
#            print year
#            print et_exp_dt.month
#            print et_exp_dt.day
            if not (year % 4 == 0 and year & 100 !=0) and et_exp_dt.month == 2 and et_exp_dt.day > 28:
                et_exp_dt = et_exp_dt.replace(month = 3)
                et_exp_dt = et_exp_dt.replace(day = 1)
                et_exp_met_dt = dt.datetime(year,
                                            et_exp_dt.month,
                                            et_exp_dt.day,
                                            et_exp_dt.hour)
            else:
                et_exp_met_dt = dt.datetime(year,
                                            et_exp_dt.month,
                                            et_exp_dt.day,
                                            et_exp_dt.hour)
            # look for indexes of weather windows finishing before the expected ending time in this year
            ind_ww_ed = indices(weather_wind['end_dt'],
                                lambda x: x >= et_exp_met_dt)

            if log_phase_id == 'LpM6' or log_phase_id == 'LpM7':
                if sched_sol['RtP'] == 'retrieve':
                    ind_ww_dur = indices( weather_wind['duration'], lambda y: y >= sched_sol['sea time_retrieve'] )
                elif sched_sol['RtP'] == 'replace':
                    ind_ww_dur = indices( weather_wind['duration'], lambda y: y >= sched_sol['sea time_replace'] )
            else:
                ind_ww_dur = indices( weather_wind['duration'], lambda y: y >= sched_sol['sea time'] )
            ind_ww_all = set(ind_ww_ed).intersection(ind_ww_dur)

            if not ind_ww_all:
                logStr = ("Could not find weather window before {} in year "
                          "{}").format(et_exp_met_dt, year)
                module_logger.debug(logStr)
            elif ind_ww_all:
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
            all_wait_time.append(sum(wait_time)/float(len(wait_time)))
        else:
            # all_wait_time.append(14*24)
            msg = ("Suitable weather window not found.")
            module_logger.warning(msg)
            
            EXIT_FLAG = 'NoWWindows'
            return [], [], EXIT_FLAG

    journey['wait_dur'] = all_wait_time
    EXIT_FLAG = 'WeatherWindowsFound'
    return journey, st_exp_dt, EXIT_FLAG


def sched_om(log_phase, log_phase_id, site, device, sub_device, entry_point, metocean,
             layout, om):

    # initialisation
    global OLC_WW
    global OLC_WW_counter

    OLC_WW = {0:{'olc':{},'ww':{}}}
    OLC_WW_counter = 0

    sol = {}
    for seq in range(len(log_phase.op_ve)):  # loop over the number of
        # operation
        # sequencing options
        sol[seq] = []
        for ind_sol in range(len(log_phase.op_ve[seq].sol)):  # loop over the
            # number of solutions, i.e feasible combinations of
            # port/vessel(s)/equipment(s)

            # print 'ind_sol: ' + str(ind_sol)

            sol[seq].append([])
#            sol[seq][ind_sol] = []
            sched_sol = {'olc': [],
                         'total time': [],
                         'prep time': [],
                         'sea time': [],
                         'weather windows': [],
                         'weather windows start_dt': [],
                         'weather windows depart_dt': [],
                         'weather windows end_dt': [],
                         'waiting time': [],
                         'all': {},
                         'journey': {},
                         'transit time': []
                         }

            # check the nature of the logistic phase
            if log_phase_id == 'LpM1' or log_phase_id == 'LpM2' or log_phase_id == 'LpM3' or log_phase_id == 'LpM4' or log_phase_id == 'LpM5' or log_phase_id == 'LpM8':
                sched_sol = sched_site(log_phase_id, seq, ind_sol,
                                       log_phase, site, layout, entry_point,
                                       om, sched_sol)
                journey, st_exp_dt, WWINDOW_FLAG = waitingTime(log_phase,
                                                               log_phase_id,
                                                               metocean, om,
                                                               sched_sol)
                if WWINDOW_FLAG == 'NoWWindows':
                    return [], [], WWINDOW_FLAG

                if not sched_sol['waiting time']:
                    sched_sol['waiting time'] = journey['wait_dur']
                else:
                    sched_sol['waiting time'].append(journey['wait_dur'])

                # sched_sol['transit time'] = sched_sol['total time'] - sched_sol['waiting time'] - sched_sol['prep time']

                # pass outputs to log_phase
                log_phase.op_ve[seq].sol[ind_sol]['schedule'] = sched_sol
                log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows start_dt'] = st_exp_dt
                log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows depart_dt'] = st_exp_dt + timedelta(hours = sum(sched_sol['waiting time']))
                log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows end_dt'] = st_exp_dt + timedelta(hours = sum(sched_sol['waiting time'])) +  timedelta(hours=sched_sol['sea time'])

                sol[seq][ind_sol] = sched_sol

            elif log_phase_id == 'LpM6' or log_phase_id == 'LpM7':

                sched_sol = sched_retrieve(log_phase_id, seq, ind_sol,
                                           log_phase, site, device, sub_device, entry_point,
                                           layout, om, sched_sol)
#                print 'RETRIEVE'
                
                journey, st_exp_dt, WWINDOW_FLAG = waitingTime(log_phase,
                                                               log_phase_id,
                                                               metocean, om,
                                                               sched_sol)
                if WWINDOW_FLAG == 'NoWWindows':
                    return [], [], WWINDOW_FLAG

                if not sched_sol['waiting time']:
                    sched_sol['waiting time_retrieve'] = journey['wait_dur']
                else:
                    sched_sol['waiting time_retrieve'].append(journey['wait_dur'])
#                print {'wait_dur': journey['wait_dur']}
                # pass outputs to log_phase
                log_phase.op_ve[seq].sol[ind_sol]['schedule'] = sched_sol

                log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows start_dt'] = {}
                log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows depart_dt'] = {}
                log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows end_dt'] = {}

#                print 'retrieve'
#                print log_phase.op_ve[seq].sol[ind_sol]['schedule']['global']['nb of journeys_retrieve']
                log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows start_dt']['weather windows start_dt_retrieve'] = st_exp_dt
                log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows depart_dt']['weather windows depart_dt_retrieve'] = st_exp_dt  +  timedelta(hours = sum(sched_sol['waiting time_retrieve']))
                log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows end_dt']['weather windows end_dt_retrieve'] = st_exp_dt +  timedelta(hours = sum(sched_sol['waiting time_retrieve'])) +  timedelta(hours=sched_sol['sea time_retrieve'])
                sched_sol['st_rts_dt'] = log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows end_dt']['weather windows end_dt_retrieve']
                sched_sol['st_rts_dt'] =  sched_sol['st_rts_dt'] + dt.timedelta(hours = float(om['d_om [hour]'].ix[0]))
#                print {'start_dt': str(log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows start_dt_retrieve']),'depart_dt': str(log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows depart_dt_retrieve']), 'end_dt': str(log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows end_dt_retrieve'])}
                sol[seq][ind_sol] = sched_sol
#                print 'replace'
                sched_sol = sched_replace(log_phase_id, seq, ind_sol,
                                          log_phase, site, device, sub_device, entry_point,
                                          layout, om, sched_sol)
#                print 'REPLACE'
                journey, st_exp_dt, WWINDOW_FLAG = waitingTime(log_phase,
                                                               log_phase_id,
                                                               metocean, om,
                                                               sched_sol)
                if WWINDOW_FLAG == 'NoWWindows':
                    return [], [], WWINDOW_FLAG

#                print {'wait_dur': journey['wait_dur']}
                if not sched_sol['waiting time']:
                    sched_sol['waiting time_replace'] = journey['wait_dur']
                else:
                    sched_sol['waiting time_replace'].append(journey['wait_dur'])
                
                sched_sol['waiting time'] = sum(sched_sol['waiting time_retrieve']) + sum(sched_sol['waiting time_replace'])

                sched_sol['total time'] = sched_sol['total time'] + sched_sol['waiting time']
                # sched_sol['transit time'] = sched_sol['total time'] - sched_sol['waiting time'] - sched_sol['prep time']

                # pass outputs to log_phase
                log_phase.op_ve[seq].sol[ind_sol]['schedule'] = sched_sol

#                print log_phase.op_ve[seq].sol[ind_sol]['schedule']['global']['nb of journeys_replace']
                log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows start_dt']['weather windows start_dt_replace'] = st_exp_dt
                log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows depart_dt']['weather windows depart_dt_replace'] = st_exp_dt  +  timedelta(hours = sum(sched_sol['waiting time_replace']))
                log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows end_dt']['weather windows end_dt_replace'] = st_exp_dt +  timedelta(hours = sum(sched_sol['waiting time_replace'])) +  timedelta(hours=sched_sol['sea time_replace'])

                log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows start_dt'] = log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows start_dt']['weather windows start_dt_retrieve']
                log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows end_dt'] = log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows end_dt']['weather windows end_dt_replace']

                sol[seq][ind_sol] = sched_sol
#                print {'start_dt': str(log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows start_dt_replace']),'depart_dt': str(log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows depart_dt_replace']), 'end_dt': str(log_phase.op_ve[seq].sol[ind_sol]['schedule']['weather windows end_dt_replace'])}
            else:
                
                allowed_phases = ['LpM1', 'LpM2', 'LpM3', 'LpM4', 'LpM5',
                                  'LpM6', 'LpM7', 'LpM8']
                allowed_phases_str = ", ".join(allowed_phases)
            
                msg = ("Unknown logistic phase ID {}. Allowed IDs: {}.".format(
                    sched_sol['RtP'], allowed_phases_str))
                module_logger.warning(msg)

    EXIT_FLAG = 'ScheduleFound'
    return sol, log_phase, EXIT_FLAG
