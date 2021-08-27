# -*- coding: utf-8 -*-

#    Copyright (C) 2017-2021 Mathew Topper
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

import os
import datetime as dt
from collections import deque
from itertools import product

import pytest
import numpy as np
import pandas as pd

from dtocean_logistics.ancillaries import indices
from dtocean_logistics.performance.schedule.schedule_shared import (
                                                        WaitingTime,
                                                        get_window_indexes,
                                                        get_groups,
                                                        trim_weather_windows)


this_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(this_dir, "..", "test_data")


@pytest.fixture(scope="module")
def metocean():
    
    metocean_path = os.path.join(data_dir, "metocean.xlsx")
    df = pd.read_excel(metocean_path)
    
    return df


@pytest.fixture(scope="module")
def metocean_synth():
    
    # Create a 12 hour window of overlapping zeros in one day (at 2-hour
    # intervals)
    twelve_hour_window = deque([0] * 9 + [1] * 3)
    window_cols = ["Hs [m]", "Tp [s]", "Ws [m/s]", "Cs [m/s]"]
    df_window_input = {}
    
    for col in window_cols:
        df_window_input[col] = list(twelve_hour_window)
        twelve_hour_window.rotate()
    
    df_twelve_hour = pd.DataFrame(df_window_input, columns=window_cols)
    
    # Create a 24 hour window of overlapping zeros in one day (at 2-hour
    # intervals)
    twentyfour_hour_window = deque([0] * 15 + [1] * 3)
    df_window_input = {}
    
    for col in window_cols:
        df_window_input[col] = list(twentyfour_hour_window)
        twentyfour_hour_window.rotate()
    
    df_twentyfour_hour = pd.DataFrame(df_window_input, columns=window_cols)
    
    # Create base time series of zeros for 3 years at 2-hour intervals
    base_time = pd.date_range("2000-01-01",
                              "2004-01-01",
                              freq="2H",
                              closed="left")
    
    df_base_input = {"time": base_time,
                     "Hs [m]": 1,
                     "Tp [s]": 1,
                     "Ws [m/s]": 1,
                     "Cs [m/s]": 1}
    base_cols = ["time"] + window_cols
    df_base = pd.DataFrame(df_base_input, columns=base_cols)
    df_base = df_base.set_index("time", drop=True)
    
    # Add 12 hour window to first day of odd months and 24 hour window to
    # even months
    df_build = df_base.copy()
    years = base_time.year.unique().values
    months = range(1, 13)
    
    for y, m in product(years, months):
    
        start_day = "{}-{:0>2}-01".format(y, m)
        
        if m % 2:
            end_day = "{}-{:0>2}-02".format(y, m)
        else:
            end_day = "{}-{:0>2}-02 12:00:00".format(y, m)
        
        month_time = pd.date_range(start_day,
                                   end_day,
                                   freq="2H",
                                   closed="left")
        
        if m % 2:
            month_window = df_twelve_hour.copy()
        else:
            month_window = df_twentyfour_hour.copy()
        
        month_window["time"] = month_time
        month_window = month_window.set_index("time", drop=True)
        
        df_build.update(month_window)
    
    df_build["year [-]"] = df_build.index.year
    df_build["month [-]"] = df_build.index.month
    df_build["day [-]"] = df_build.index.day
    df_build["hour [-]"] = df_build.index.hour
    
    final_cols = ["year [-]", "month [-]", "day [-]", "hour [-]"] + window_cols
    
    return df_build[final_cols].reset_index(drop=True)


@pytest.fixture(scope="module")
def metocean_synth_long():
    
    # Create a 12 hour window of overlapping zeros in one day (at 2-hour
    # intervals)
    twelve_hour_window = deque([0] * 9 + [1] * 3)
    window_cols = ["Hs [m]", "Tp [s]", "Ws [m/s]", "Cs [m/s]"]
    df_window_input = {}
    
    for col in window_cols:
        df_window_input[col] = list(twelve_hour_window)
        twelve_hour_window.rotate()
    
    df_twelve_hour = pd.DataFrame(df_window_input, columns=window_cols)
    
    # Create a 24 hour window of overlapping zeros in one day (at 2-hour
    # intervals)
    twentyfour_hour_window = deque([0] * 15 + [1] * 3)
    df_window_input = {}
    
    for col in window_cols:
        df_window_input[col] = list(twentyfour_hour_window)
        twentyfour_hour_window.rotate()
    
    df_twentyfour_hour = pd.DataFrame(df_window_input, columns=window_cols)
    
    # Create base time series of zeros for 3 years at 2-hour intervals
    base_time = pd.date_range("2000-01-01",
                              "2004-01-01",
                              freq="2H",
                              closed="left")
    
    df_base_input = {"time": base_time,
                     "Hs [m]": 1,
                     "Tp [s]": 1,
                     "Ws [m/s]": 1,
                     "Cs [m/s]": 1}
    base_cols = ["time"] + window_cols
    df_base = pd.DataFrame(df_base_input, columns=base_cols)
    df_base = df_base.set_index("time", drop=True)
    
    # Add 12 hour window to first day of odd months and 24 hour window to
    # even months
    df_build = df_base.copy()
    years = base_time.year.unique().values[-1:]
    months = range(1, 13)
    
    for y, m in product(years, months):
    
        start_day = "{}-{:0>2}-01".format(y, m)
        
        if m % 2:
            end_day = "{}-{:0>2}-02".format(y, m)
        else:
            end_day = "{}-{:0>2}-02 12:00:00".format(y, m)
        
        month_time = pd.date_range(start_day,
                                   end_day,
                                   freq="2H",
                                   closed="left")
        
        if m % 2:
            month_window = df_twelve_hour.copy()
        else:
            month_window = df_twentyfour_hour.copy()
        
        month_window["time"] = month_time
        month_window = month_window.set_index("time", drop=True)
        
        df_build.update(month_window)
    
    df_build["year [-]"] = df_build.index.year
    df_build["month [-]"] = df_build.index.month
    df_build["day [-]"] = df_build.index.day
    df_build["hour [-]"] = df_build.index.hour
    
    final_cols = ["year [-]", "month [-]", "day [-]", "hour [-]"] + window_cols
    
    return df_build[final_cols].reset_index(drop=True)


def test_WaitingTime_init(metocean):
    result = WaitingTime(metocean)
    assert isinstance(result, WaitingTime)


def test_WaitingTime_time_step_hours(metocean):
    result = WaitingTime(metocean)
    assert np.isclose(result._time_step_hours, 3)


def test_WaitingTime_init_years_trim(metocean):
    
    init_years = len(metocean["year [-]"].unique())
    test = WaitingTime(metocean)
    
    years = iter(test.metocean["year [-]"].unique())
    first = next(years)
    
    assert all(a == b for a, b in enumerate(years, first + 1))
    assert len(test.metocean["year [-]"].unique()) == init_years - 1


def test_WaitingTime_init_years_repeat(metocean):
    
    metocean_copy = metocean.copy()
    metocean_copy = metocean_copy[metocean_copy["year [-]"] == 1995]
    
    test = WaitingTime(metocean_copy)
    
    years = iter(test.metocean["year [-]"].unique())
    first = next(years)
    
    assert all(a == b for a, b in enumerate(years, first + 1))
    assert len(test.metocean["year [-]"].unique()) == 3
    

def test_WaitingTime_init_years_extra(metocean):
    
    metocean_copy = metocean.copy()
    metocean_copy = metocean_copy[metocean_copy["year [-]"].isin([1995,
                                                                  1996])]
    
    test = WaitingTime(metocean_copy)
    
    years = iter(test.metocean["year [-]"].unique())
    first = next(years)
    
    assert all(a == b for a, b in enumerate(years, first + 1))
    assert len(test.metocean["year [-]"].unique()) == 3


def test_WaitingTime_init_years_fail_missing(metocean):
    
    metocean_copy = metocean.copy()
    metocean_copy = metocean_copy[metocean_copy["year [-]"] == 1992]
    
    with pytest.raises(ValueError) as excinfo:
        WaitingTime(metocean_copy)
    
    assert "No complete years" in str(excinfo.value)


def test_WaitingTime_init_years_fail_monotonic(metocean):
    
    metocean_copy = metocean.copy()
    metocean_copy = metocean_copy[metocean_copy["year [-]"].isin([1993,
                                                                  1995])]
    
    with pytest.raises(ValueError) as excinfo:
        WaitingTime(metocean_copy)
    
    assert "not monotonic" in str(excinfo.value)


def test_WaitingTime_set_optimise_delay(metocean):
    
    test = WaitingTime(metocean)
    test.set_optimise_delay(True)
    
    assert test._optimise_delay


def test_WaitingTime_get_weather_windows_basic(metocean_synth):
    
    test = WaitingTime(metocean_synth)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    result = test.get_weather_windows(olc)
    
    assert len(result['duration']) > 0
    assert (len(result['duration']) == 
            len(result['start_dt']) ==
            len(result['end_dt']))

def test_WaitingTime_get_weather_windows_end_dt(metocean_synth):
    
    test = WaitingTime(metocean_synth)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    result = test.get_weather_windows(olc)
    
    assert result['end_dt'][0] == dt.datetime(2000, 1, 1, 18, 0)


def test_WaitingTime_get_weather_windows_cum_gap(metocean_synth):
    
    test = WaitingTime(metocean_synth)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    result = test.get_weather_windows(olc)
    cum_gap = result['cum_gap']
    
    assert cum_gap[0] == 0      # No gap to first window
    assert cum_gap[1] == 732    # 30 days and 12 hours till next


def test_WaitingTime_get_weather_windows_no_olc(metocean_synth):
    
    test = WaitingTime(metocean_synth)
    
    olc = {}
    
    result = test.get_weather_windows(olc)
    
    assert len(result['duration']) == 1
    assert np.isclose(result['duration'][0], 35064)


def test_WaitingTime_get_whole_windows(metocean_synth):
    
    test = WaitingTime(metocean_synth)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    windows = test.get_weather_windows(olc)
    start_date_met = dt.datetime(2000, 1, 1)

    ind_ww_all = test._get_whole_windows(windows, start_date_met, 20)
    
    assert ind_ww_all[0] == 1


@pytest.mark.parametrize("test_input, expected", [
    (0, 6),
    (1, 750) # 31 days and 6 hours
])
def test_WaitingTime_get_start_delay(metocean_synth, test_input, expected):
    
    test = WaitingTime(metocean_synth)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    windows = test.get_weather_windows(olc)
    start_date_met = dt.datetime(2000, 1, 1)

    start_delay = test._get_start_delay(windows, start_date_met, test_input)

    assert start_delay == expected


def test_WaitingTime_get_start_delay_negative(metocean_synth):
    
    test = WaitingTime(metocean_synth)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    windows = test.get_weather_windows(olc)
    start_date_met = dt.datetime(2000, 1, 3)
    
    with pytest.raises(RuntimeError):
        test._get_start_delay(windows, start_date_met, 0)


def test_WaitingTime_get_combined_windows(metocean_synth):
    
    test = WaitingTime(metocean_synth)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    windows = test.get_weather_windows(olc)
    start_date_met = dt.datetime(2000, 1, 1)
    
    trimmed_windows = trim_weather_windows(windows, start_date_met)
    
    all_cum_durations = np.array(trimmed_windows['cum_duration'])
    all_cum_gaps = np.array(trimmed_windows['cum_gap'])
    
    delays, wait_times = test._get_combined_windows(all_cum_durations,
                                                    all_cum_gaps,
                                                    36)
    
    assert all(x < y for x, y in zip(delays, delays[1:]))
    assert all(x >= 0 for x in wait_times)
    
    assert delays[0] == 0
    assert delays[1] == 744


def test_WaitingTime_whole_window_strategy(metocean_synth):
    
    test = WaitingTime(metocean_synth)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    windows = test.get_weather_windows(olc)
    start_date = dt.datetime(2000, 1, 1)

    start_delay, waiting_time = test._whole_window_strategy(windows,
                                                            start_date,
                                                            20)
    assert waiting_time is None
    assert np.isclose(start_delay, 750)     # 31 * 24 + 6
    

def test_WaitingTime_whole_window_strategy_long(metocean):
    
    test = WaitingTime(metocean)
    
    olc = {'maxHs': 4,
           'maxTp': 15,
           'maxWs': 15}
    
    windows = test.get_weather_windows(olc)
    start_date = dt.datetime(2000, 1, 1)

    start_delay, waiting_time = test._whole_window_strategy(windows,
                                                            start_date,
                                                            5000)
    assert waiting_time is None
    assert start_delay is None


def test_WaitingTime_whole_window_strategy_max_start_delay(metocean_synth):
    
    test = WaitingTime(metocean_synth,
                       max_start_delay=4)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    windows = test.get_weather_windows(olc)
    start_date = dt.datetime(2000, 1, 1)

    start_delay, waiting_time = test._whole_window_strategy(windows,
                                                            start_date,
                                                            10)
    
    assert start_delay is None
    assert waiting_time is None


def test_WaitingTime_combined_window_strategy_max_start_delay(metocean_synth):
    
    test = WaitingTime(metocean_synth,
                       max_start_delay=4)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    windows = test.get_weather_windows(olc)
    start_date = dt.datetime(2000, 1, 1)
    start_delay, waiting_time = test._combined_window_strategy(windows,
                                                               start_date,
                                                               24)
    
    assert start_delay is None
    assert waiting_time is None


def test_WaitingTime_combined_window_strategy_single(metocean_synth):
    
    test = WaitingTime(metocean_synth)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    windows = test.get_weather_windows(olc)
    start_date = dt.datetime(2000, 1, 1)
    start_delay, waiting_time = test._combined_window_strategy(windows,
                                                               start_date,
                                                               24)
    
    assert np.isclose(start_delay, 750.)
    assert np.isclose(waiting_time, 0)


def test_WaitingTime_combined_window_strategy_multi(metocean_synth):
    
    test = WaitingTime(metocean_synth)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    windows = test.get_weather_windows(olc)
    start_date = dt.datetime(2000, 1, 1)
    start_delay, waiting_time = test._combined_window_strategy(windows,
                                                               start_date,
                                                               36)
    
    assert np.isclose(start_delay, 750.) # Less waiting with 24 hour window
    assert np.isclose(waiting_time, 656.0) # (27 + 27 + 28) * 24 / 3


def test_WaitingTime_combined_window_strategy_max_start_none(
                                                    metocean_synth_long):
    
    test = WaitingTime(metocean_synth_long,
                       max_start_delay=None)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    windows = test.get_weather_windows(olc)
    start_date = dt.datetime(2000, 1, 1)

    start_delay, waiting_time = test._combined_window_strategy(windows,
                                                               start_date,
                                                               12)
    
    assert np.isclose(start_delay, 17534)
    assert waiting_time == 0.
    
    
def test_WaitingTime_combined_window_strategy_short(metocean_synth):
    
    test = WaitingTime(metocean_synth)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    windows = test.get_weather_windows(olc)
    start_date = dt.datetime(2000, 1, 1)

    start_delay, waiting_time = test._combined_window_strategy(windows,
                                                               start_date,
                                                               24)
    
    assert waiting_time == 0


def test_WaitingTime_combined_window_strategy_optimise(metocean_synth):
    
    test = WaitingTime(metocean_synth)
    test.set_optimise_delay(True)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    windows = test.get_weather_windows(olc)
    start_date = dt.datetime(2000, 1, 1)

    start_delay, waiting_time = test._combined_window_strategy(windows,
                                                               start_date,
                                                               24)
    
    assert np.isclose(start_delay, 6.)
    assert np.isclose(waiting_time, 732.0) # 30 days, 12 hours


def test_WaitingTime_combined_window_strategy_leap(metocean_synth):
    
    test = WaitingTime(metocean_synth)
    
    olc = {'maxHs': 0.5,
           'maxTp': 0.5,
           'maxWs': 0.5,
           'maxCs': 0.5}
    
    windows = test.get_weather_windows(olc)
    start_date = dt.datetime(2000, 2, 29)

    start_delay, waiting_time = test._combined_window_strategy(windows,
                                                               start_date,
                                                               12)
    
    assert np.isclose(start_delay, 14.0) # (30 + 6 + 6) / 3
    assert waiting_time == 0


def test_WaitingTime_call(mocker, metocean):
    
    test = WaitingTime(metocean)
    
    log_phase = mocker.Mock()
    log_phase.description = "Mocked phase"
    
    journey = {'prep_dur': [48, 48],
               'prep_id': [u'Mobilisation', u'Vessel preparation & loading'],
               'sea_dur': [35.52257567817756,
                           6.0,
                           2,
                           4,
                           0.0,
                           35.52257567817756],
               'sea_id': [u'Transportation from port to site',
                          u'Vessel Positioning',
                          u'Access to the element',
                          u'Inspection or Maintenance Operations',
                          u'Transportation from site to site',
                          u'Transportation from site to port'],
               'sea_olc': [[2.5, 0.0, 0.0, 0.0],
                           [2.5, 0, 0, 0],
                           [4, 6, 15, 2],
                           [4, 6, 15, 2],
                           [2.5, 0.0, 0.0, 0.0],
                           [2.5, 0.0, 0.0, 0.0]],
               'wait_dur': []}
    
    sched_sol = {"journey": {0: journey}}
    start_date = dt.datetime(2000, 1, 1)
    
    journey, exit_flag = test(log_phase,
                              sched_sol,
                              start_date)
    
    assert exit_flag == "WeatherWindowsFound"
    assert 'start_delay' in journey
    
    
def test_WaitingTime_call_twice(mocker, metocean):
    
    test = WaitingTime(metocean)
    
    log_phase = mocker.Mock()
    log_phase.description = "Mocked phase"
    
    journey = {'prep_dur': [48, 48],
               'prep_id': [u'Mobilisation', u'Vessel preparation & loading'],
               'sea_dur': [35.52257567817756,
                           6.0,
                           2,
                           4,
                           0.0,
                           35.52257567817756],
               'sea_id': [u'Transportation from port to site',
                          u'Vessel Positioning',
                          u'Access to the element',
                          u'Inspection or Maintenance Operations',
                          u'Transportation from site to site',
                          u'Transportation from site to port'],
               'sea_olc': [[2.5, 0.0, 0.0, 0.0],
                           [2.5, 0, 0, 0],
                           [4, 6, 15, 2],
                           [4, 6, 15, 2],
                           [2.5, 0.0, 0.0, 0.0],
                           [2.5, 0.0, 0.0, 0.0]],
               'wait_dur': []}
    
    sched_sol = {"journey": {0: journey}}
    start_date = dt.datetime(2000, 1, 1)
    
    journey, exit_flag = test(log_phase,
                              sched_sol,
                              start_date)
    
    assert exit_flag == "WeatherWindowsFound"
    assert 'start_delay' in journey
    
    journey, exit_flag = test(log_phase,
                              sched_sol,
                              start_date)
    
    assert exit_flag == "WeatherWindowsFound"
    assert 'start_delay' in journey


def test_WaitingTime_call_no_strategy(mocker, metocean):
    
    test = WaitingTime(metocean)
    
    log_phase = mocker.Mock()
    log_phase.description = "Mocked phase"
    
    # Use conditions where no strategy can be found although there are
    # weather windows for the OLC conditions.
    journey = {'prep_dur': [48, 48],
               'prep_id': [u'Mobilisation', u'Vessel preparation & loading'],
               'sea_dur': [35.52257567817756,
                           6.0,
                           2,
                           4,
                           0.0,
                           35.52257567817756],
               'sea_id': [u'Transportation from port to site',
                          u'Vessel Positioning',
                          u'Access to the element',
                          u'Inspection or Maintenance Operations',
                          u'Transportation from site to site',
                          u'Transportation from site to port'],
               'sea_olc': [[0.1, 0.0, 0.0, 0.0],
                           [2.5, 0, 0, 0],
                           [4, 6, 15, 2],
                           [4, 6, 15, 2],
                           [2.5, 0.0, 0.0, 0.0],
                           [2.5, 0.0, 0.0, 0.0]],
               'wait_dur': []}
    
    sched_sol = {"journey": {0: journey}}
    start_date = dt.datetime(2000, 1, 1)
    
    journey, exit_flag = test(log_phase,
                              sched_sol,
                              start_date)
    
    assert exit_flag == 'NoWWindows'
    assert not journey


def test_WaitingTime_call_no_windows(mocker, metocean):
    
    test = WaitingTime(metocean)
    
    log_phase = mocker.Mock()
    log_phase.description = "Mocked phase"
    
    # Use very small OLC conditions for which no windows are in metocean
    journey = {'prep_dur': [48, 48],
               'prep_id': [u'Mobilisation', u'Vessel preparation & loading'],
               'sea_dur': [35.52257567817756,
                           6.0,
                           2,
                           4,
                           0.0,
                           35.52257567817756],
               'sea_id': [u'Transportation from port to site',
                          u'Vessel Positioning',
                          u'Access to the element',
                          u'Inspection or Maintenance Operations',
                          u'Transportation from site to site',
                          u'Transportation from site to port'],
               'sea_olc': [[0.01, 0.0, 0.0, 0.0],
                           [2.5, 0, 0, 0],
                           [4, 6, 15, 2],
                           [4, 6, 15, 2],
                           [2.5, 0.0, 0.0, 0.0],
                           [2.5, 0.0, 0.0, 0.0]],
               'wait_dur': []}
    
    sched_sol = {"journey": {0: journey}}
    start_date = dt.datetime(2000, 1, 1)
    
    journey, exit_flag = test(log_phase,
                              sched_sol,
                              start_date)
        
    assert exit_flag == 'NoWWindows'
    assert not journey


def test_get_window_indexes():
    
    wdx = np.array([1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                    0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                    1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                    0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.])
    
    result = get_window_indexes(wdx, 2)
    indexes = result.keys()
    durations = result.values()
    
    assert all(x < y for x, y in zip(indexes, indexes[1:]))
    assert all(x > 0 for x in durations)
    assert len(result) == 2
    assert indexes[1] == 24
    assert np.isclose(durations, 24).all()


@pytest.mark.parametrize("test_input, expected", [
    ([1,2,3,4,1], [[1, 2, 3, 4], [1]]),
    ([1], [[1]]),
    ([], [])
])
def test_get_groups(test_input, expected):
    
    result = get_groups(test_input)
    
    assert result == expected
