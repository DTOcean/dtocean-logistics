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

from .schedule_shared import WaitingTime
from ...performance.schedule.om.schedule_site import sched_site
from ...performance.schedule.om.schedule_retrieve import sched_retrieve
from ...performance.schedule.om.schedule_replace import sched_replace

# Set up logging
module_logger = logging.getLogger(__name__)


class SchedOM(object):
    
    def __init__(self):
        
        self._pre_site = {}
        self._pre_replace = {}
        self._pre_retrieve = {}
        self._old_sched = None
        self._old_sched_log_phase_id = None
        self._old_sched_seq = None
        self._old_sched_ind_sol = None
        self._old_sched_element_IDs = None
        
        return
    
    def _get_sched_site(self, log_phase_id,
                              seq,
                              ind_sol,
                              log_phase,
                              site,
                              layout,
                              entry_point,
                              om,
                              sched_sol):
        
        element_IDs = om['element_ID [-]'].unique()
        x_coord = om['x coord [m]'].astype(float)
        y_coord = om['y coord [m]'].astype(float)
        
        if (log_phase_id in self._pre_site and
            seq in self._pre_site[log_phase_id] and
            ind_sol in self._pre_site[log_phase_id][seq]):
            
            saved_tuples = self._pre_site[log_phase_id][seq][ind_sol]
            
            for (test_elements,
                 test_x_coord,
                 test_y_coord,
                 saved_sched_sol) in saved_tuples:

                if (set(element_IDs) == set(test_elements) and
                    x_coord.equals(test_x_coord) and
                    y_coord.equals(test_y_coord)):
                    
#                    if (self._old_sched is not None and
#                        self._old_sched_log_phase_id == log_phase_id and
#                        self._old_sched_seq == seq and
#                        self._old_sched_ind_sol == ind_sol and
#                        self._old_sched_element_IDs == set(element_IDs)):
#                        
#                        compare_sched(saved_sched_sol,
#                                      self._old_sched)
#                        
#                        self._old_sched = None
                    
                    return copy_sched(saved_sched_sol)
        
        save_tuple = (element_IDs,
                      x_coord,
                      y_coord,
                      copy_sched(sched_sol))
        
        sched_sol = sched_site(log_phase_id,
                               seq,
                               ind_sol,
                               log_phase,
                               site,
                               layout,
                               entry_point,
                               om,
                               sched_sol)
        
        save_tuple = (element_IDs,
                      x_coord,
                      y_coord,
                      copy_sched(sched_sol))
        
        if log_phase_id in self._pre_site:
        
            if seq in self._pre_site[log_phase_id]:
                
                seq_dict = self._pre_site[log_phase_id][seq]
                
                if ind_sol in seq_dict:
                    seq_dict[ind_sol].append(save_tuple)
                else:
                    seq_dict[ind_sol] = [save_tuple]
            
            else:
                
                save_dict = {ind_sol: [save_tuple]}
                self._pre_site[log_phase_id][seq] = save_dict
        
        else:
            
            save_dict = {seq: {ind_sol: [save_tuple]}}
            self._pre_site[log_phase_id] = save_dict
#        
#        if self._old_sched is None:
#            
#            self._old_sched = deepcopy(sched_sol)
#            self._old_sched_log_phase_id = log_phase_id
#            self._old_sched_seq = seq
#            self._old_sched_ind_sol = ind_sol
#            self._old_sched_element_IDs = set(element_IDs)
        
        return sched_sol
    
    def _get_wws_site(self, rt_dt,
                            waiting_time,
                            log_phase_id,
                            seq,
                            ind_sol,
                            log_phase,
                            site,
                            layout,
                            entry_point,
                            om,
                            sched_sol):
        
        sched_sol = self._get_sched_site(log_phase_id,
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
        if WWINDOW_FLAG == 'NoWWindows':
            return False
        
        if not sched_sol['waiting time']:
            sched_sol['waiting time'] = journey['wait_dur']
        else:
            sched_sol['waiting time'] += journey['wait_dur']
        
        start_delays = journey['start_delay']
        mean_delay = sum(start_delays) / float(len(start_delays))
        
        # Update total time
        sched_sol['total time'] += [mean_delay] + sched_sol['waiting time']
        
        departure_dt = st_exp_dt + dt.timedelta(hours=mean_delay)
        end_dt = departure_dt + \
                    dt.timedelta(hours=sched_sol['sea time']) + \
                        dt.timedelta(hours=sum(sched_sol['waiting time']))
        
        sched_sol['weather windows start_dt'] = st_exp_dt
        sched_sol['weather windows depart_dt'] = departure_dt
        sched_sol['weather windows end_dt'] = end_dt
        
        return sched_sol
    
    def __call__(self,
                 log_phase,
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
                    
                    sched_sol = self._get_wws_site(rt_dt,
                                                   waiting_time,
                                                   log_phase_id,
                                                   seq,
                                                   ind_sol,
                                                   log_phase,
                                                   site,
                                                   layout,
                                                   entry_point,
                                                   om,
                                                   sched_sol)
                    
                    if not sched_sol: continue
                
                else:
                    
                    sched_sol = _get_wws_base(rt_dt,
                                              waiting_time,
                                              log_phase_id,
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
                    
                    if not sched_sol: continue
                
                old_sol_item = log_phase.op_ve[seq].sol[ind_sol]
                old_sol_item['schedule'] = sched_sol
                
                new_sol_idx = len(new_sol)
                new_sol[new_sol_idx] = old_sol_item
                
                # TIME ASSESSMENT
                # stop_time = timeit.default_timer()
                # print 'Solution Duration [s]: ' + str(stop_time - start_time
            
            # Exit if no solutions were found
            if len(new_sol) == 0: return log_phase, 'NoWWindows'
            
            # Replace the log phase solutions
            log_phase.op_ve[seq].sol = new_sol
        
        EXIT_FLAG = 'ScheduleFound'
        
        return log_phase, EXIT_FLAG


def _get_wws_base(rt_dt,
                  waiting_time,
                  log_phase_id,
                  seq,
                  ind_sol,
                  log_phase,
                  site,
                  device,
                  sub_device,
                  entry_point,
                  layout,
                  om,
                  sched_sol):
    
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
    journey_retrieve, WWINDOW_FLAG = waiting_time(log_phase,
                                                  sched_sol,
                                                  st_exp_dt_retrieve)
    
    # Loop if no weather window
    if WWINDOW_FLAG == 'NoWWindows': return False
    
    if not sched_sol['waiting time']:
        waiting_time_retrieve = journey_retrieve['wait_dur']
    else:
        waiting_time_retrieve = sched_sol['waiting time'] + \
                                            journey_retrieve['wait_dur']
                                    
    start_delays = journey_retrieve['start_delay']
    mean_retrieve_delay = sum(start_delays) / float(len(start_delays))
                                    
    retrieve_time = [mean_retrieve_delay] +  waiting_time_retrieve
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
    
    ## TODO: Why is the existing total time not taken into account in this 
    ## case?
    journey_replace, WWINDOW_FLAG = waiting_time(log_phase,
                                                 sched_sol,
                                                 st_exp_dt_replace)
    
    # Loop if no weather window
    if WWINDOW_FLAG == 'NoWWindows': return False
    
    if not sched_sol['waiting time']:
        waiting_time_replace = journey_replace['wait_dur']
    else:
        waiting_time_replace = sched_sol['waiting time'] + \
                                            journey_replace['wait_dur']
                                    
    start_delays = journey_replace['start_delay']
    mean_replace_delay = sum(start_delays) / float(len(start_delays))
    
    replace_time = [mean_replace_delay] + waiting_time_replace
    
    # Record solution
    sched_sol['waiting time_retrieve'] = waiting_time_retrieve
    sched_sol['waiting time_replace'] = waiting_time_replace
    sched_sol['waiting time'] = waiting_time_retrieve + \
                                                waiting_time_replace
                                            
    sched_sol['total time'] = retrieve_time + replace_time
                              
    sched_sol['weather windows start_dt'] = st_exp_dt_retrieve
    sched_sol['weather windows end_dt'] = st_exp_dt_replace + \
                                    dt.timedelta(hours=sum(replace_time))
    
    depart_dt = {}
    
    ww_ddt_retrieve = st_exp_dt_retrieve + \
                                dt.timedelta(hours=mean_retrieve_delay)
    ww_ddt_replace = st_exp_dt_replace + \
                                dt.timedelta(hours=mean_replace_delay)
    
    depart_dt['weather windows depart_dt_retrieve'] = ww_ddt_retrieve
    depart_dt['weather windows depart_dt_replace'] = ww_ddt_replace
    
    sched_sol['weather windows depart_dt'] = depart_dt
    
    return sched_sol


def get_start(om):
    
    t_start = om['t_start [-]'][0]
    
    if isinstance(t_start, dt.datetime):
        
        rt_dt = t_start.replace(minute=0, second=0, microsecond=0)
    
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


def copy_sched(old):
    
    new = {}
    
    for k, v in old.iteritems():
        
        if k in ['total time', 'waiting time']:
            new[k] = v[:]
        else:
            new[k] = v
    
    return new


def compare_sched(new, old):
    
    def check_recursive(new_obj, old_obj):
        
        if isinstance(new_obj, dict):
            
            assert isinstance(old_obj, dict)
            
            for k, v in new_obj.iteritems():
                assert k in old_obj
                check_recursive(v, old_obj[k])
        
        elif isinstance(new_obj, list):
            
            assert isinstance(old_obj, list)
            assert len(new_obj) == len(old_obj)
            
            for i, v in enumerate(new_obj):
                check_recursive(v, old_obj[i])
        
        else:
            
            assert new_obj == old_obj
    
    for k, v in new.iteritems():
        assert k in old
        old_v = old[k]
        check_recursive(v, old_v)


def print_sched(new, old):
    
    def print_recursive(new_obj, old_obj):
        
        result = [True]
        
        if isinstance(new_obj, dict):
            for k, v in new_obj.iteritems():
                print "key", k
                assert k in old_obj
                result.extend(print_recursive(v, old_obj[k]))
                    
        elif isinstance(new_obj, list):
            
            if not isinstance(old_obj, list):
                print "fail not list", old_obj
                return [False]
            elif len(new_obj) != len(old_obj):
                print "fail length", len(new_obj), len(old_obj)
                return [False]
            else:
                for i, v in enumerate(new_obj):
                    print "list index", i
                    result.extend(print_recursive(v, old_obj[i]))
                
        else:
            
            if not new_obj == old_obj:
                print "fail compare", new_obj, old_obj
                return [False]
            else:
                return [True]
            
        return result
    
    check = []
    
    for k, v in new.iteritems():
        print "key", k
        assert k in old
        old_v = old[k]
        check.extend(print_recursive(v, old_v))
    
    return all(check)
