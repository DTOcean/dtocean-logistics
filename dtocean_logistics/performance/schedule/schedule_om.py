# -*- coding: utf-8 -*-

#    Copyright (C) 2016 Boris Teillant, Paulo Chainho
#    Copyright (C) 2017-2018 Mathew Topper
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Created on Sun Aug 16 11:53:24 2015

.. moduleauthor:: Boris Teillant <boris.teillant@wavec.org>
.. moduleauthor:: Paulo Chainho <paulo@wavec.org>
.. moduleauthor:: Mathew Topper <mathew.topper@dataonlygreater.com>
"""

import timeit
import logging
import datetime as dt
from copy import deepcopy

from .schedule_shared import WaitingTime
from ...performance.schedule.om.schedule_site import sched_site
from ...performance.schedule.om.schedule_retrieve import sched_retrieve
from ...performance.schedule.om.schedule_replace import sched_replace

# Set up logging
module_logger = logging.getLogger(__name__)


def sched_om(log_phase,
             log_phase_id,
             site,
             device,
             sub_device,
             entry_point,
             metocean,
             layout,
             om,
             optimise_delay=False,
             custom_waiting=None):
        
    # Check the phase ID
    allowed_phases = ['LpM1',
                      'LpM2',
                      'LpM3',
                      'LpM4',
                      'LpM5',
                      'LpM6',
                      'LpM7',
                      'LpM8']
    
    if log_phase_id not in allowed_phases:
    
        allowed_phases_str = ", ".join(allowed_phases)
        errStr = ("Unknown logistic phase ID {}. Allowed IDs are: "
                  "{}").format(log_phase_id,
                               allowed_phases_str)
        
        raise ValueError(errStr)

    # initialisation
    if custom_waiting is None:
        waiting_time = WaitingTime(metocean)
    else:
        waiting_time = custom_waiting
        
    waiting_time.set_optimise_delay(optimise_delay)
        
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
            

            # Get requested start time
            rt_dt = get_start(om)
            
            # check the nature of the logistic phase
            if log_phase_id not in ['LpM6', 'LpM7']:
                
                sched_sol = sched_site(log_phase_id,
                                       seq,
                                       ind_sol,
                                       log_phase,
                                       site,
                                       layout,
                                       entry_point,
                                       om,
                                       sched_sol)
                
                
                st_exp_dt = rt_dt + dt.timedelta(
                                        hours=float(sched_sol['prep time']))
                                
                journey, WWINDOW_FLAG = waiting_time(log_phase,
                                                     sched_sol,
                                                     st_exp_dt)
                
                # Loop if no weather window
                if WWINDOW_FLAG == 'NoWWindows': continue
    
                if not sched_sol['waiting time']:
                    sched_sol['waiting time'] = journey['wait_dur']
                else:
                    sched_sol['waiting time'] += journey['wait_dur']
                
                start_delays = journey['start_delay']
                mean_delay = sum(start_delays) / float(len(start_delays))
                
                # Update total time
                sched_sol['total time'] += [mean_delay] + \
                                                    sched_sol['waiting time']
                
                departure_dt = st_exp_dt + dt.timedelta(hours=mean_delay)
                end_dt = departure_dt + \
                        dt.timedelta(hours=sched_sol['sea time']) + \
                            dt.timedelta(hours=sum(sched_sol['waiting time']))
    
                sched_sol['weather windows start_dt'] = st_exp_dt
                sched_sol['weather windows depart_dt'] = departure_dt
                sched_sol['weather windows end_dt'] = end_dt
                
            else:
                
                # Retrieve stage
                sched_sol = sched_retrieve(log_phase_id,
                                           seq,
                                           ind_sol,
                                           log_phase,
                                           site,
                                           device,
                                           sub_device,
                                           entry_point,
                                           layout,
                                           om,
                                           sched_sol)
                
                st_exp_dt_retrieve = rt_dt + dt.timedelta(
                                hours=float(sched_sol['prep time_retrieve']))
                sea_time = sched_sol['sea time_retrieve']
                
                journey_retrieve, WWINDOW_FLAG = waiting_time(
                                                        log_phase,
                                                        sched_sol,
                                                        st_exp_dt_retrieve)
                
                # Loop if no weather window
                if WWINDOW_FLAG == 'NoWWindows': continue
            
                if not sched_sol['waiting time']:
                    waiting_time_retrieve = journey_retrieve['wait_dur']
                else:
                    waiting_time_retrieve = sched_sol['waiting time'] + \
                                                journey_retrieve['wait_dur']
                                                
                start_delays = journey_retrieve['start_delay']
                mean_retrieve_delay = sum(start_delays) / \
                                                    float(len(start_delays))
                                                
                retrieve_time = [mean_retrieve_delay] + waiting_time_retrieve
                om_time = float(om['d_om [hour]'].ix[0])
                                                
                st_rts_dt = st_exp_dt_retrieve + \
                                    dt.timedelta(hours=sum(retrieve_time)) + \
                                    dt.timedelta(hours=om_time)

                # Replace stage
                sched_sol = sched_replace(log_phase_id,
                                          seq,
                                          ind_sol,
                                          log_phase,
                                          site,
                                          device,
                                          sub_device,
                                          entry_point,
                                          layout,
                                          om,
                                          sched_sol)

                st_exp_dt_replace = st_rts_dt + dt.timedelta(
                                hours=float(sched_sol['prep time_replace']))
                sea_time = sched_sol['sea time_replace']
                
                journey_replace, WWINDOW_FLAG = waiting_time(log_phase,
                                                             sched_sol,
                                                             st_exp_dt_replace)

                # Loop if no weather window
                if WWINDOW_FLAG == 'NoWWindows': continue

                if not sched_sol['waiting time']:
                    waiting_time_replace = journey_replace['wait_dur']
                else:
                    waiting_time_replace = sched_sol['waiting time'] + \
                                                journey_replace['wait_dur']
                                                
                start_delays = journey_replace['start_delay']
                mean_replace_delay = sum(start_delays) / \
                                                    float(len(start_delays))
                                                
                replace_time = [mean_replace_delay] + waiting_time_replace
                                                    
                # Record solution
                sched_sol['waiting time_retrieve'] = waiting_time_retrieve
                sched_sol['waiting time_replace'] = waiting_time_replace
                sched_sol['waiting time'] = waiting_time_retrieve + \
                                                        waiting_time_replace
                                                        
                sched_sol['total time'] = retrieve_time + replace_time
                                          
                sched_sol['weather windows start_dt'] = st_exp_dt_retrieve
                sched_sol['weather windows end_dt'] = \
                    st_exp_dt_replace + dt.timedelta(hours=sum(replace_time))

                depart_dt = {}

                depart_dt['weather windows depart_dt_retrieve'] = \
                    st_exp_dt_retrieve + \
                    dt.timedelta(hours=mean_retrieve_delay)
                depart_dt['weather windows depart_dt_replace'] = \
                    st_exp_dt_replace + \
                    dt.timedelta(hours=mean_replace_delay)

                sched_sol['weather windows depart_dt'] = depart_dt

            old_sol_item = deepcopy(log_phase.op_ve[seq].sol[ind_sol])
            old_sol_item['schedule'] = sched_sol

            new_sol_idx = len(new_sol)
            new_sol[new_sol_idx] = old_sol_item

            # TIME ASSESSMENT
            # stop_time = timeit.default_timer()
            # print 'Solution Duration [s]: ' + str(stop_time - start_time)  
        
        # Exit if no solutions were found
        if len(new_sol) == 0: return log_phase, 'NoWWindows'
        
        # Replace the log phase solutions
        log_phase.op_ve[seq].sol = new_sol

    EXIT_FLAG = 'ScheduleFound'

    return log_phase, EXIT_FLAG


def get_start(om):
    
    t_start = om['t_start [-]'][0]
    
    if isinstance(t_start, dt.datetime):

        rt_dt = t_start

    else:

        rt = {'year': int(t_start[6:10]),
              'month': int(t_start[3:5]),
              'day': int(t_start[0:2]),
              'hour': int(t_start[11:13]),
              'min': int(t_start[14:16])}
        
        rt_dt = dt.datetime(rt['year'],
                            rt['month'],
                            rt['day'],
                            rt['hour'])
    
    return rt_dt
