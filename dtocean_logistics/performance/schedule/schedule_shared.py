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
.. moduleauthor:: Boris Teillant <boris.teillant@wavec.org>
.. moduleauthor:: Paulo Chainho <paulo@wavec.org>
.. moduleauthor:: Mathew Topper <mathew.topper@dataonlygreater.com>
"""

import math
import timeit
import logging
import datetime as dt
from operator import itemgetter
from itertools import groupby
from collections import OrderedDict

import numpy as np
import pandas as pd

from ...ancillaries import indices

# Start the logger
module_logger = logging.getLogger(__name__)


class WaitingTime(object):
    
    def __init__(self, metocean,
                       min_window_years=3,
                       match_tolerance=0.1,
                       max_start_delay=8760):
        
        self.metocean = self._init_years(metocean, min_window_years)
        self._match_tol = match_tolerance
        self._max_start_delay = max_start_delay
        self._optimise_delay = False
        self._olc_ww = []
        
        return
    
    @classmethod
    def _init_years(cls, metocean, min_window_years):
        
        """Retain complete years in metocean data by searching for first and
        last hour of each year. Ensure that min_window_years years of data
        is available by looping if necessary.
        """
        
        # Test for first and last hour of each year (assuming hour 0 and
        # the last hour for the median time step)
        median_step = metocean["hour [-]"].diff().median()
        year_groups = metocean.groupby('year [-]')
        
        valid_years = []

        for year, df in year_groups:
            
            if not ((df["month [-]"] == 1) &
                    (df["day [-]"] == 1) &
                    (df["hour [-]"] == 0)).any(): continue
                    
            if not ((df["month [-]"] == 12) &
                    (df["day [-]"] == 31) &
                    (df["hour [-]"] == (24 - median_step))).any(): continue
                    
            valid_years.append(year)
            
        if not valid_years:
            
            errStr = ("No complete years for weather window calculation were "
                      "found in metocean data")
            raise ValueError(errStr)
            
        missing_years = set(year_groups.groups.keys()) - set(valid_years)
        
        if missing_years:
            
            missing_year_strs = [str(year) for year in missing_years]
            years_str = ", ".join(missing_year_strs)
            
            msgStr = ("Year(s) '{}' were incomplete and removed from weather "
                      "window calculation").format(years_str)
            module_logger.info(msgStr)
        
        # Check that the years are monotonic
        valid_years_iter = iter(valid_years)
        first_year = next(valid_years_iter)
    
        if not all(a == b for a, b in enumerate(valid_years_iter,
                                                first_year + 1)):
            
            valid_year_strs = [str(year) for year in valid_years]
            valid_str = ", ".join(valid_year_strs)
            errStr = ("Valid years in metocean data are not monotonic. Found: "
                      "{}").format(valid_str)
            raise ValueError(errStr)
                        
        final_metocean = metocean[metocean["year [-]"].isin(valid_years)]
        final_metocean = final_metocean.reset_index()
        
        n_years = len(valid_years)
        
        if n_years >= min_window_years: return final_metocean
        
        msgStr = ("Valid metocean data contains {} years which is less than "
                  "the minimum {} required. Data will be manipulated to "
                  "extend the duration").format(n_years,
                                                min_window_years)
        module_logger.info(msgStr)
        
        # Get the divisor and remainder for looping the years
        n_repeats = min_window_years / n_years - 1
        n_extra = min_window_years % n_years
        initial_metocean = final_metocean.copy()
        
        # Add repeats
        if n_repeats > 0:
            msgStr = "Repeating valid metocean data {} time(s)".format(
                                                                    n_repeats)
            module_logger.info(msgStr)

        for i in xrange(n_repeats):
            
            add_years = n_years * (i + 1)
            new_metocean = initial_metocean.copy()
            new_metocean["year [-]"] = new_metocean["year [-]"].apply(
                                                    lambda x: x + add_years)
            
            final_metocean = pd.concat([final_metocean, new_metocean],
                                       ignore_index=True)
            
            
        if n_extra == 0:
            assert len(final_metocean["year [-]"].unique()) == \
                                                            min_window_years
            return final_metocean
            
        # Add extra years
        msgStr = "Copying {} year(s) from valid metocean data".format(n_extra)
        module_logger.info(msgStr)
        
        add_years = n_years * (n_repeats + 1)
        extra_years = valid_years[:n_extra]
        
        filter_years = metocean["year [-]"].isin(extra_years)
        new_metocean =  metocean[filter_years].apply(lambda x: x + add_years)
        
        final_metocean = pd.concat([final_metocean, new_metocean],
                                   ignore_index=True,
                                   sort=False)
        
        assert len(final_metocean["year [-]"].unique()) == min_window_years
        
        return final_metocean
    
    def set_optimise_delay(self, value):
        
        self._optimise_delay = value
        
        return
    
    def get_weather_windows(self, olc):
        
        """This functions returns the starting times and the durations of all
        weather windows found in the met-ocean data for the given operational
        limit conditions (olc)
        """
    
        # Initialisation
        ww = {}
    
        # Operational limit conditions (consdiered static over the entire
        # duration of the marine operation)
        median_step = self.metocean["hour [-]"].diff().median()
            
        windowStr = "No weather windows were found for operational condition: "
        durationStr = ("Short durations (<8 hours) detected for operational "
                       "condition: ")
        
        # Build the binary weather windows:
        #   1 = authorized access,
        #   0 = denied access
        if 'maxHs' in olc and olc['maxHs'] > 0:
            Hs_bin = map(float, self.metocean['Hs [m]'] < olc['maxHs'])
        else:
            Hs_bin = [1] * len(self.metocean['Hs [m]'])
            olc['maxHs'] = max(self.metocean['Hs [m]'])
            
        if 'maxTp' in olc and olc['maxTp'] > 0:
            Tp_bin = map(float, self.metocean['Tp [s]'] < olc['maxTp'])
        else:
            Tp_bin = [1] * len(self.metocean['Tp [s]'])
            olc['maxTp'] = max(self.metocean['Tp [s]'])
            
        if 'maxWs' in olc and olc['maxWs'] > 0:
            Ws_bin = map(float, self.metocean['Ws [m/s]'] < olc['maxWs'])
        else:
            Ws_bin = [1] * len(self.metocean['Ws [m/s]'])
            olc['maxWs'] = max(self.metocean['Ws [m/s]'])
            
        if 'maxCs' in olc and olc['maxCs'] > 0:
            Cs_bin = map(float, self.metocean['Cs [m/s]'] < olc['maxCs'])
        else:
            Cs_bin = [1] * len(self.metocean['Cs [m/s]'])
            olc['maxCs'] = max(self.metocean['Cs [m/s]'])

        # Convert to numpy arrays and test for no windows and exit
        Hs_bin = np.array(Hs_bin)
        oppStr = "maxHs < {}".format(olc['maxHs'])
        
        if not Hs_bin.any():
            module_logger.warning(windowStr + oppStr)
            
            return ww
        
        # Check for short durations
        windows = get_window_indexes(Hs_bin, median_step)
        max_duration = max(windows.values())
        
        if max_duration < 8:
            module_logger.warning(durationStr + oppStr)
            
        Tp_bin = np.array(Tp_bin)
        oppStr = "maxTp < {}".format(olc['maxTp'])
        
        if not Tp_bin.any():
            module_logger.warning(windowStr + oppStr)
            
            return ww
        
        # Check for short durations
        windows = get_window_indexes(Tp_bin, median_step)
        max_duration = max(windows.values())
        
        if max_duration < 8:
            module_logger.warning(durationStr + oppStr)
            
        Ws_bin = np.array(Ws_bin)
        oppStr = "maxWs < {}".format(olc['maxWs'])
        
        if not Ws_bin.any():
            module_logger.warning(windowStr + oppStr)
            
            return ww
        
        # Check for short durations
        windows = get_window_indexes(Ws_bin, median_step)
        max_duration = max(windows.values())
        
        if max_duration < 8:
            module_logger.warning(durationStr + oppStr)
        
        Cs_bin = np.array(Cs_bin)
        oppStr = "maxCs < {}".format(olc['maxCs'])
        
        if not Cs_bin.any():
            module_logger.warning(windowStr + oppStr)
            
            return ww
        
        # Check for short durations
        windows = get_window_indexes(Cs_bin, median_step)
        max_duration = max(windows.values())
        
        if max_duration < 8:
            module_logger.warning(durationStr + oppStr)
        
        # Combine the windows
        WW_bin = np.logical_and.reduce((Hs_bin, Tp_bin, Ws_bin, Cs_bin))

        # No combined weather windows exit the function
        if not WW_bin.any():
            
            logStr = ("No combined weather windows were found for operational "
                      "conditions: maxHs < {}; maxTp < {}; maxWs < {}; "
                      "maxCs < {}").format(olc['maxHs'],
                                           olc['maxTp'],
                                           olc['maxWs'],
                                           olc['maxCs'])
            module_logger.warning(logStr)
            
            return ww
    
        # Determine the starting index and the durations of the weather windows
        windows = get_window_indexes(WW_bin, median_step)
    
        st_y = []
        st_m = []
        st_d = []
        st_h = []
        st_dt = []
        et_dt = []
        durations = []

        for ind_dt, duration in windows.iteritems():
            
            year = self.metocean['year [-]'][ind_dt]
            month = self.metocean['month [-]'][ind_dt]
            day = self.metocean['day [-]'][ind_dt]
            hour = self.metocean['hour [-]'][ind_dt]
            
            start_datetime = dt.datetime(year, month, day, hour)
            end_datetime = start_datetime + dt.timedelta(hours=int(duration))
            
            st_y.append(year)
            st_m.append(month)
            st_d.append(day)
            st_h.append(hour)
            st_dt.append(start_datetime)
            et_dt.append(end_datetime)
            durations.append(duration)

        ww['start'] = {'year': st_y,
                       'month': st_m,
                       'day': st_d,
                       'hour': st_h}
        ww['start_dt'] = st_dt
        ww['end_dt'] = et_dt
        ww['duration'] = durations
        
        return ww
    
    @classmethod
    def _get_whole_windows(cls, weather_windows, start_date_met, sea_time):
        
        ind_ww_sd = indices(weather_windows['start_dt'],
                                lambda x: x >= start_date_met)
        ind_ww_dur = indices(weather_windows['duration'],
                             lambda y: y >= sea_time)
        ind_ww_all = set(ind_ww_sd).intersection(ind_ww_dur)
        
        return list(ind_ww_all)
    
    @classmethod
    def _get_start_delay(cls, weather_windows, start_date_met, window_idx):
        
        delta_wt = weather_windows['start_dt'][window_idx] - start_date_met
        start_delay = int(delta_wt.total_seconds()) / 3600
        
        if start_delay < 0:
            errStr = "Start of window is before requested start date"
            raise RuntimeError(errStr)
            
        return start_delay
    
    @classmethod
    def _get_window_info(cls, weather_windows, start_date_met, idx_ww_sd):
        
        window_delays = []
        window_durations = []
        window_gaps = []
        last_end = None

        for idx in idx_ww_sd:
            
            delta_st = weather_windows['start_dt'][idx] - start_date_met
            delay = int(delta_st.total_seconds()) / 3600
            
            duration = weather_windows['duration'][idx]
                        
            window_delays.append(delay)
            window_durations.append(duration)

            delta_et = weather_windows['end_dt'][idx] - start_date_met
            end = int(delta_et.total_seconds()) / 3600
            
            if last_end is None:
                last_end = end
                continue
                
            gap = end - last_end
            last_end = end

            window_gaps.append(gap)
            
        return window_delays, window_durations, window_gaps
    
    @classmethod
    def _get_combined_windows(cls, window_delays,
                                   window_durations,
                                   window_gaps,
                                   sea_time,
                                   idx_ww_sd):
        
        delays = []
        wait_times = []
        
        for idx in xrange(len(idx_ww_sd)):
                        
            delay = window_delays[idx]
            check_durations = window_durations[idx:]
            check_gaps = window_gaps[idx:]
            
            cum_durations = np.cumsum(check_durations)
            cum_gaps = np.cumsum(check_gaps)
            
            # Leave the loop if the sea time cant be completed
            if not (cum_durations >= sea_time).any(): break
        
            last_idx = np.argmax(cum_durations >= sea_time)
            
            if cum_gaps.size > 0 and last_idx > 0:
                wait_time = cum_gaps[last_idx - 1]
            else:
                wait_time = 0.
            
            delays.append(delay)
            wait_times.append(wait_time)
            
        return delays, wait_times
    
    def _whole_window_strategy(self, weather_windows,
                                     start_date,
                                     sea_time):
        
        mean_delay = None
        waiting_time = None
        
        # Get the years of metocean data excluding the last
        years = self.metocean['year [-]'].unique()[:-1]

        start_delays = []
        
        # Attempt to find whole weather windows, starting in each year of the
        # metocean data and then calculate the mean start delay
        for i, year in enumerate(years):
            
            # Set the year to match metocean data and avoid reaching the 29th
            # of February in a 366 days year
            if (not is_leap_year(year) and
                start_date.month == 2 and
                start_date.day > 28):
                
                start_date_met = dt.datetime(year,
                                             3,
                                             1,
                                             start_date.hour)
                
            else:
                
                start_date_met = dt.datetime(year,
                                             start_date.month,
                                             start_date.day,
                                             start_date.hour)

            # Trim the windows to the operation start
            trimmed_windows = trim_weather_windows(weather_windows,
                                                   start_date_met)
                
            # Look for indexes of weather windows starting after the given
            # start date                        
            ind_ww_all = self._get_whole_windows(trimmed_windows,
                                                 start_date_met,
                                                 sea_time)
                    
            if not ind_ww_all:
                
                date_format = lambda x: "{:%d-%b %H:%M}".format(x)
                
                logStr = ("No combined start dates and durations found "
                          "for operation with start date '{}' and "
                          "duration {} hours in year {}").format(
                                                  date_format(start_date),
                                                  sea_time,
                                                  i)
                
                module_logger.warning(logStr)
                
                return mean_delay, waiting_time
                                
            # Find the index of the first suitable weather window
            ind_ww_first = min(ind_ww_all)
            
            # Get the start delay
            start_delay = self._get_start_delay(trimmed_windows,
                                                start_date_met,
                                                ind_ww_first)
                            
            # If the start delay exceeds the maximum then abort the strategy
            if (self._max_start_delay is not None and
                start_delay > self._max_start_delay):
                
                date_format = lambda x: "{:%d-%b %H:%M}".format(x)
                
                logStr = ("No continuous weather windows found "
                          "for operation with start date '{}' and "
                          "duration {} hours in year {}, below the maximum "
                          "start delay of {} hours.").format(
                                                      date_format(start_date),
                                                      sea_time,
                                                      year,
                                                      self._max_start_delay)
                
                module_logger.warning(logStr)
                
                return mean_delay, waiting_time
            
            start_delays.append(start_delay)
                                
        if start_delays:
            mean_delay = np.array(start_delays).mean()
            
        return mean_delay, waiting_time
    
    def _combined_window_strategy(self, weather_windows,
                                        start_date,
                                        sea_time):
        
        start_delays = []
        waiting_times = []
        
        # Get the years of metocean data excluding the last
        years = self.metocean['year [-]'].unique()[:-1]
        
        # Attempt to groups of weather windows covering the operation
        # duration, starting in each year of the metocean data and then
        # calculate the mean start delay and waiting time
        for i, year in enumerate(years):
        
            # Set the year to match metocean data and avoid reaching the 29th
            # of February in a 366 days year
            if (not is_leap_year(year) and
                start_date.month == 2 and
                start_date.day > 28):
                
                start_date_met = dt.datetime(year,
                                             3,
                                             1,
                                             start_date.hour)
                
            else:
                
                start_date_met = dt.datetime(year,
                                             start_date.month,
                                             start_date.day,
                                             start_date.hour)
                
            # Trim the windows to the operation start
            trimmed_windows = trim_weather_windows(weather_windows,
                                                   start_date_met)
                
            # Look for indexes of weather windows starting after the given
            # start date
            idx_ww_sd = indices(trimmed_windows['start_dt'],
                                lambda x: x >= start_date_met)
            
            # Collect delay, duration and gaps between windows
            (window_delays,
             window_durations,
             window_gaps) = self._get_window_info(trimmed_windows,
                                                  start_date_met,
                                                  idx_ww_sd)
                
            # Run through the windows, searching for the combination with least
            # waiting time
            delays, wait_times = self._get_combined_windows(window_delays,
                                                            window_durations,
                                                            window_gaps,
                                                            sea_time,
                                                            idx_ww_sd)
            
            if self._max_start_delay is not None:

                # Get group of windows with waiting time below the maximum
                year_wait_times = np.ma.masked_where(
                                    np.array(delays) > self._max_start_delay,
                                    wait_times)
                
            else:
                
                year_wait_times = np.ma.array(wait_times)
            
            # If no cumulative windows were found (possibly within the
            # maximum waiting time) then abort the strategy            
            if np.ma.is_masked(year_wait_times):
                check_mask = year_wait_times.mask.all()
            else:
                check_mask = False
            
            if not delays or check_mask:
                
                date_format = lambda x: "{:%d-%b %H:%M}".format(x)
                
                logStr = ("No cumulative windows found for operation with "
                          "start date '{}' in year {}").format(
                                                      date_format(start_date),
                                                      i)
                
                if self._max_start_delay is not None:
                    
                    extraStr = (" and maximum start delay of {} "
                                "hours").format(self._max_start_delay)
                    logStr += extraStr
                
                module_logger.warning(logStr)            
                
                return None, None
    
            if self._optimise_delay:
                
                # Get group of windows with minimum delay
                min_wait_idx = 0
                
            else:
                
                # Get the group of windows with minimum waiting time
                min_wait_idx = np.ma.argmin(year_wait_times)
                    
            start_delay = delays[min_wait_idx]
            waiting_time = wait_times[min_wait_idx]
                    
            start_delays.append(start_delay)
            waiting_times.append(waiting_time)
            
        mean_start_delay = sum(start_delays) / float(len(start_delays))
        mean_waiting_time = sum(waiting_times) / float(len(waiting_times))
        
        return mean_start_delay, mean_waiting_time
                
    def __call__(self, log_phase, sched_sol, start_date):
        
        """
        Waiting time calculation based on requested time and weather window
        """
        
        olc_names = ['maxHs',
                     'maxTp',
                     'maxWs',
                     'maxCs']
        
        start_delays = []
        wait_times = []
                
        # loop over the number of vessel journeys
        for journey in sched_sol['journey'].itervalues():
            
            # nansum will ignore NaN values (created by bugs...)
            sea_time = np.nansum(journey['sea_dur'])
            
            # initialisation of the parameters for the weather window
            # calculation
            olc = {'maxHs': [],
                   'maxTp': [],
                   'maxWs': [],
                   'maxCs': []}
                        
            for op_name, op_sea in zip(journey['sea_id'], journey['sea_olc']):
                
                olcMsgs = ["{}: {}".format(cond, op_sea_olc)
                            for cond, op_sea_olc in zip(olc_names, op_sea)]
                olcMsg = ", ".join(olcMsgs)
                logMsg = ("Checking limit conditions for phase '{}': "
                          "{}").format(op_name, olcMsg)
                module_logger.info(logMsg)
                                
                for i, name in enumerate(olc_names):
                    
                    op_sea_olc = op_sea[i]
                    
                    # replace 'nan' and negative OLC values by zero
                    if op_sea_olc <= 0 or math.isnan(op_sea_olc):
                        op_sea_olc = 0
                    
                    # Append OLC values
                    olc[name].append(op_sea_olc)
                        
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
    
            # Return phase OLC
            msg = []
    
            if olc['maxHs'] > 0:
                msg.append("Significant wave height: {}m".format(olc['maxHs']))
    
            if olc['maxTp'] > 0:
                msg.append("Peak period: {}s".format(olc['maxTp']))
    
            if olc['maxWs'] > 0:
                msg.append("Maximum wind speed: {}s".format(olc['maxWs']))
    
            if olc['maxCs'] > 0:
                msg.append("Maximum current speed: {}s".format(olc['maxCs']))
    
            msg_str = ', '.join(msg)
            module_logger.info("Combined operational limit for phase {}: "
                               "{}".format(log_phase.description, msg_str))
    
            # start_time = timeit.default_timer()      ## TIME ASSESSMENT
            
            # See if the same weather windows have been calculated and stored
            # before
            weather_wind = None
    
            for ww_dict in self._olc_ww:
                
                ww_olc = ww_dict['olc']
                delta = [abs(v - ww_olc[k]) for k, v in olc.items()]
                
                if all([x <= self._match_tol for x in delta]):
                    weather_wind = ww_dict['ww']
                    break
            
            # Calculate new weather windows
            if weather_wind is None:
                
                weather_wind = self.get_weather_windows(olc)
                self._olc_ww.append({'olc': olc,
                                     'ww': weather_wind})
            
            # OLC conditions allow no weather windows
            if not weather_wind: return [], 'NoWWindows'
                    
            # stop_time = timeit.default_timer()  # TIME ASSESSMENT
    
            # Start looking for whole weather windows in the metocean data
            # unless self._optimise_delay is True
            msgStr = ("Creating logistics plan for operation length {} hours "
                      "for phase {} on date {}").format(sea_time,
                                                        log_phase.description,
                                                        start_date)
            module_logger.info(msgStr)
            
            start_delay = None
            
            if not self._optimise_delay:
            
                (start_delay,
                 wait_time) = self._whole_window_strategy(weather_wind,
                                                          start_date,
                                                          sea_time)
            
            # If self._optimise_delay is True or if a whole window can not be
            # found look for cumulative windows
            if start_delay is None:
                
                (start_delay,
                 wait_time) = self._combined_window_strategy(
                                                         weather_wind,
                                                         start_date,
                                                         sea_time)
                
            if start_delay is not None:
                
                start_delays.append(start_delay)
                
                if start_delay > 720:
                    module_logger.warning("Long start delay found in phase "
                                          "{}: {} hours".format(
                                                      log_phase.description,
                                                      start_delay))
                
            else:
    
                return [], 'NoWWindows'
            
            if wait_time is not None:
                
                wait_times.append(wait_time)
                
                if wait_time > 720:
                    module_logger.warning("Long waiting time found in phase "
                                          "{}: {} hours".format(
                                                      log_phase.description,
                                                      wait_time))
    
        journey['start_delay'] = start_delays
        journey['wait_dur'] = wait_times
        
        return journey, 'WeatherWindowsFound'


def get_window_indexes(WW_bin, time_step):
    
    """Return starting index and duration of window as keys and values of
    an ordered dictionary"""
        
    WW_authorized = indices(WW_bin, lambda x: x == 1)
    window_groups = get_groups(WW_authorized)

    windows = OrderedDict()
    
    for group in window_groups:
        
        duration = len(group) - 1
        
        # Don't allow 0 length windows
        if duration == 0: continue
    
        start_index = group[0]
        duration = duration * time_step
        
        windows[start_index] = duration
    
    return windows


def get_groups(data):
    
    groups = []
    
    for k, g in groupby(enumerate(data), lambda (i, x): i - x):
        groups.append(map(itemgetter(1), g))
        
    return groups


def is_leap_year(year):
    
    if (((year % 4 == 0) and (year % 100 != 0)) or 
        (year % 400 == 0)):
        result = True
    else:
        result = False
    
    return result

def trim_weather_windows(weather_windows, op_start):
    
    """Remove any weather windows prior to the op_start and reduce the length
    of a window which contains the op_start, so that the window starts on the
    same date"""
    
    # Edge case with no weather windows earlier than the op_start
    if weather_windows['start_dt'][0] >= op_start: return weather_windows
        
    i = 0
    st_y = []
    st_m = []
    st_d = []
    st_h = []
    st_dt = []
    et_dt = []
    durations = []
    
    while i < len(weather_windows['end_dt']):
        
        end_dt = weather_windows['end_dt'][i]
        
        if end_dt < op_start:
            
            i += 1
            continue
        
        if end_dt == op_start: break
    
        start_diff = end_dt - op_start 
        duration = start_diff.total_seconds() / 3600.            
        
        st_y.append(op_start.year)
        st_m.append(op_start.month)
        st_d.append(op_start.day)
        st_h.append(op_start.hour)
        st_dt.append(op_start)
        et_dt.append(end_dt)
        durations.append(duration)
        
        break
                        
    st_y += weather_windows['start']['year'][i + 1:]
    st_m += weather_windows['start']['month'][i + 1:]
    st_d += weather_windows['start']['day'][i + 1:]
    st_h += weather_windows['start']['hour'][i + 1:]
    st_dt += weather_windows['start_dt'][i + 1:]
    et_dt += weather_windows['end_dt'][i + 1:]
    durations += weather_windows['duration'][i + 1:]
    
    new_ww = {}
        
    new_ww['start'] = {'year': st_y,
                       'month': st_m,
                       'day': st_d,
                       'hour': st_h}
    new_ww['start_dt'] = st_dt
    new_ww['end_dt'] = et_dt
    new_ww['duration'] = durations
    
    return new_ww
    
    
    
