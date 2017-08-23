# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables, Mathew Topper
email: boris.teillant@wavec.org; paulo@wavec.org, dataonlygreater@gmail.com
"""

import timeit
import logging
import datetime as dt
from copy import deepcopy
from datetime import timedelta

from .schedule_shared import WaitingTime
from ...performance.schedule.install import (sched_dev,
                                             sched_e_export,
                                             sched_e_array,
                                             sched_e_dynamic,
                                             sched_e_cp_seabed,
                                             sched_e_cp_surface,
                                             sched_e_external,
                                             sched_driven,
                                             sched_gravity,
                                             sched_m_drag,
                                             sched_m_direct,
                                             sched_m_suction,
                                             sched_m_pile,
                                             sched_s_struct)

# Start the logger
module_logger = logging.getLogger(__name__)


def sched(x,
          y,
          install,
          log_phase,
          log_phase_id,
          site,
          metocean,
          device,
          sub_device,
          entry_point,
          layout,
          collection_point,
          dynamic_cable,
          static_cable,
          cable_route,
          connectors,
          external_protection,
          topology,
          line,
          foundation,
          penet_rates,
          laying_rates,
          other_rates):

    # initialisation
    waiting_time = WaitingTime(metocean)

    # end_dt_last = [] # to make only devices work?!?!?!!!
        
    # loop over the number of operations
    for seq, operation in log_phase.op_ve.iteritems():  

        new_sol = {}

        # loop over the number of solutions, i.e feasible combinations of
        # port/vessel(s)/equipment(s)
        for ind_sol in range(len(operation.sol)):
            
            # start_time = timeit.default_timer()  # TIME ASSESSMENT
            # print 'seq: ' + str(seq) + ', sol: ' + str(ind_sol)
            
            ve_groups = []
            ve_names = []
            
            for ve_comb in log_phase.op_ve[seq].sol[ind_sol]['VEs']:
                ve_groups.append(ve_comb[0])
                ve_names.append(ve_comb[2]["Name"])
            
            comb_strs = []
            
            for group, name in zip(ve_groups, ve_names):
                comb_strs.append("{}: {}".format(group, name))
                
            comb_str = ", ".join(comb_strs)
            msgStr = "Vessel & equipment combinations: {}".format(comb_str)
            module_logger.info(msgStr)
            
            sched_sol = get_sched_sol(log_phase_id,
                                      seq,
                                      ind_sol,
                                      install,
                                      log_phase,
                                      site,
                                      entry_point,
                                      device,
                                      sub_device,
                                      layout,
                                      static_cable,
                                      dynamic_cable,
                                      collection_point,
                                      external_protection,
                                      cable_route,
                                      foundation,
                                      laying_rates,
                                      penet_rates,
                                      other_rates)
            
            rt_dt, end_dt_last = get_start_end(x,
                                               install,
                                               device)
            
            # Add onshore preparation time to expected starting date
            st_exp_dt = rt_dt + dt.timedelta(
                                        hours=float(sched_sol['prep time']))

            journey, WWINDOW_FLAG = waiting_time(log_phase,
                                                 sched_sol,
                                                 st_exp_dt,
                                                 sched_sol['sea time'])

            # stop_time1 = timeit.default_timer()  # TIME ASSESSMENT   

            # Loop if no weather window
            if WWINDOW_FLAG == 'NoWWindows': continue

            if not sched_sol['waiting time']:
                sched_sol['waiting time'] = journey['wait_dur']
            else:
                sched_sol['waiting time'] += journey['wait_dur']
            
            # Update total time
            sched_sol['total time'] += journey['start_delay'] + \
                                                    sched_sol['waiting time']
            
            departure_dt = st_exp_dt + \
                                timedelta(hours=sum(journey['start_delay']))
            end_dt = departure_dt + \
                            timedelta(hours=sched_sol['sea time']) + \
                                timedelta(hours=sum(sched_sol['waiting time']))

            sched_sol['weather windows start_dt'] = st_exp_dt
            sched_sol['weather windows depart_dt'] = departure_dt
            sched_sol['weather windows end_dt'] = end_dt
            
            old_sol_item = deepcopy(log_phase.op_ve[seq].sol[ind_sol])
            old_sol_item['schedule'] = sched_sol

            new_sol_idx = len(new_sol)
            new_sol[new_sol_idx] = old_sol_item

            # TIME ASSESSMENT
            # stop_time = timeit.default_timer()
            # print 'Solution Duration [s]: ' + str(stop_time - start_time)  
        
        # Exit if no solutions were found
        if len(new_sol) == 0: return [], log_phase, 'NoWWindows'
        
        # Replace the log phase solutions
        log_phase.op_ve[seq].sol = new_sol

    EXIT_FLAG = 'ScheduleFound'

    return end_dt_last, log_phase, EXIT_FLAG


def get_sched_sol(log_phase_id,
                  seq,
                  ind_sol,
                  install,
                  log_phase,
                  site,
                  entry_point,
                  device,
                  sub_device,
                  layout,
                  static_cable,
                  dynamic_cable,
                  collection_point,
                  external_protection,
                  cable_route,
                  foundation,
                  laying_rates,
                  penet_rates,
                  other_rates):
    
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
        
        sched_sol = sched_dev(seq,
                              ind_sol,
                              install,
                              log_phase,
                              site,
                              entry_point,
                              device,
                              sub_device,
                              layout,
                              sched_sol)
        
    elif log_phase_id == 'E_export':
        
        sched_sol = sched_e_export(seq,
                                   ind_sol,
                                   install,
                                   log_phase,
                                   site,
                                   entry_point,
                                   static_cable,
                                   cable_route,
                                   laying_rates,
                                   other_rates,
                                   sched_sol)
        
    elif log_phase_id == 'E_array':
        
        sched_sol = sched_e_array(seq,
                                  ind_sol,
                                  install,
                                  log_phase,
                                  site,
                                  entry_point,
                                  static_cable,
                                  cable_route,
                                  laying_rates,
                                  other_rates,
                                  sched_sol)
        
    elif log_phase_id == 'E_dynamic':
        
        sched_sol = sched_e_dynamic(seq,
                                    ind_sol,
                                    install,
                                    log_phase,
                                    site,
                                    entry_point,
                                    dynamic_cable,
                                    other_rates,
                                    sched_sol)
        
    elif log_phase_id == 'E_cp_seabed':
        
        sched_sol = sched_e_cp_seabed(seq,
                                      ind_sol,
                                      install,
                                      log_phase,
                                      site,
                                      entry_point,
                                      collection_point,
                                      sched_sol)
        
    elif log_phase_id == 'E_cp_surface':
        
        sched_sol = sched_e_cp_surface(seq,
                                       ind_sol,
                                       install,
                                       log_phase,
                                       site,
                                       entry_point,
                                       collection_point,
                                       sched_sol)
        
    elif log_phase_id == 'E_external':
        
        sched_sol = sched_e_external(seq,
                                     ind_sol,
                                     install,
                                     log_phase,
                                     site,
                                     entry_point,
                                     external_protection,
                                     sched_sol)
        
    elif log_phase_id == 'Driven':
        
        sched_sol = sched_driven(seq,
                                 ind_sol,
                                 install,
                                 log_phase,
                                 site,
                                 entry_point,
                                 device,
                                 foundation,
                                 penet_rates,
                                 other_rates,
                                 sched_sol)
        
    elif log_phase_id == 'Gravity':
        
        sched_sol = sched_gravity(seq,
                                  ind_sol,
                                  install,
                                  log_phase,
                                  site,
                                  entry_point,
                                  device,
                                  layout,
                                  foundation,
                                  sched_sol)
        
    elif log_phase_id == 'M_direct':
        
        sched_sol = sched_m_direct(seq,
                                   ind_sol,
                                   install,
                                   log_phase,
                                   site,
                                   entry_point,
                                   device,
                                   layout,
                                   foundation,
                                   penet_rates,
                                   sched_sol)
        
    elif log_phase_id == 'M_suction':
        
        sched_sol = sched_m_suction(seq,
                                    ind_sol,
                                    install,
                                    log_phase,
                                    site,
                                    entry_point,
                                    device,
                                    layout,
                                    foundation,
                                    penet_rates,
                                    sched_sol)
        
    elif log_phase_id == 'M_drag':
        
        sched_sol = sched_m_drag(seq,
                                 ind_sol,
                                 install,
                                 log_phase,
                                 site,
                                 entry_point,
                                 device,
                                 layout,
                                 foundation,
                                 sched_sol)
        
    elif log_phase_id == 'M_pile':
        
        sched_sol = sched_m_pile(seq,
                                 ind_sol,
                                 install,
                                 log_phase,
                                 site,
                                 entry_point,
                                 device,
                                 layout,
                                 foundation,
                                 sched_sol)
        
    elif log_phase_id == 'S_structure':
        
        sched_sol = sched_s_struct(seq,
                                   ind_sol,
                                   install,
                                   log_phase,
                                   site,
                                   entry_point,
                                   device,
                                   sub_device,
                                   layout,
                                   sched_sol)
        
    else:
        
        msg = ("Unknown logistic phase ID: {}".format(log_phase_id))
        module_logger.warning(msg)

    return sched_sol


def get_start_end(x,
                  install,
                  device):
    
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
                
    return rt_dt, end_dt_last

