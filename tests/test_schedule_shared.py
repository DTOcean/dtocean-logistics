
import os
import datetime as dt

import pytest
import numpy as np
import pandas as pd

from dtocean_logistics.ancillaries.find import indices
from dtocean_logistics.performance.schedule.schedule_shared import (
                                                        WaitingTime,
                                                        get_window_indexes,
                                                        get_groups)


this_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(this_dir, "..", "test_data")


@pytest.fixture(scope="module")
def metocean():
    
    metocean_path = os.path.join(data_dir, "metocean.xlsx")
    df = pd.read_excel(metocean_path)
    
    return df
    

def test_WaitingTime_init(metocean):
    
    result = WaitingTime(metocean)
    
    assert isinstance(result, WaitingTime)


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
    
    with pytest.raises(ValueError):
        WaitingTime(metocean_copy)


def test_WaitingTime_init_years_fail_monotonic(metocean):
    
    metocean_copy = metocean.copy()
    metocean_copy = metocean_copy[metocean_copy["year [-]"].isin([1993,
                                                                  1995])]
    
    with pytest.raises(ValueError):
        WaitingTime(metocean_copy)
        
        
def test_WaitingTime_set_optimise_delay(metocean):
    
    test = WaitingTime(metocean)
    test.set_optimise_delay(True)
    
    assert test._optimise_delay


def test_WaitingTime_get_weather_windows(metocean):
    
    test = WaitingTime(metocean)
    
    olc = {'maxHs': 4,
           'maxTp': 15,
           'maxWs': 15}
    
    result = test.get_weather_windows(olc)
    
    assert len(result['duration']) > 0
    assert (len(result['duration']) == 
            len(result['start_dt']) ==
            len(result['end_dt']))
    
    
def test_WaitingTime_get_weather_windows_no_olc(metocean):
    
    test = WaitingTime(metocean)
    
    olc = {}
    
    result = test.get_weather_windows(olc)
    
    assert len(result['duration']) == 1
    assert np.isclose(result['duration'][0], 61341.0)
    
    
def test_WaitingTime_get_weather_windows_small_olc(metocean):
    
    test = WaitingTime(metocean)
    
    olc = {'maxHs': 0.01,
           'maxTp': 0.01,
           'maxWs': 0.01,
           'maxCs': 0.01}
    
    result = test.get_weather_windows(olc)
        
    assert not result
    

def test_WaitingTime_get_whole_windows(metocean):
    
    test = WaitingTime(metocean)
    
    olc = {'maxHs': 4,
           'maxTp': 15,
           'maxWs': 15}
    
    windows = test.get_weather_windows(olc)
    start_date_met = dt.datetime(1993, 1, 1)

    ind_ww_all = test._get_whole_windows(windows, start_date_met, 100)
    
    assert ind_ww_all[0] == 0


@pytest.mark.parametrize("test_input, expected", [
    (0, 0),
    (1, 111)
])
def test_WaitingTime_get_start_delay(metocean, test_input, expected):
    
    test = WaitingTime(metocean)
    
    olc = {'maxHs': 4,
           'maxTp': 15,
           'maxWs': 15}
    
    windows = test.get_weather_windows(olc)
    start_date_met = dt.datetime(1993, 1, 1)

    start_delay = test._get_start_delay(windows, start_date_met, test_input)

    assert start_delay == expected
    
    
def test_WaitingTime_get_start_delay_negative(metocean):
    
    test = WaitingTime(metocean)
    
    olc = {'maxHs': 4,
           'maxTp': 15,
           'maxWs': 15}
    
    windows = test.get_weather_windows(olc)
    start_date_met = dt.datetime(1993, 1, 2)

    with pytest.raises(RuntimeError):
        test._get_start_delay(windows, start_date_met, 0)
        
  
def test_WaitingTime_get_window_info(metocean):
    
    test = WaitingTime(metocean)
    
    olc = {'maxHs': 4,
           'maxTp': 15,
           'maxWs': 15}
    
    windows = test.get_weather_windows(olc)
    start_date_met = dt.datetime(1993, 1, 2)
    
    idx_ww_sd = indices(windows['start_dt'],
                        lambda x: x >= start_date_met)

    (window_delays,
     window_durations,
     window_gaps) = test._get_window_info(windows,
                                          start_date_met,
                                          idx_ww_sd)
    
    assert all(x < y for x, y in zip(window_delays, window_delays[1:]))    
    assert all(x > 0 for x in window_durations)
    assert all(x > 0 for x in window_gaps)
    
    
def test_WaitingTime_get_combined_windows(metocean):
    
    test = WaitingTime(metocean)
    
    olc = {'maxHs': 4,
           'maxTp': 15,
           'maxWs': 15}
    
    windows = test.get_weather_windows(olc)
    start_date_met = dt.datetime(1993, 1, 2)
    
    idx_ww_sd = indices(windows['start_dt'],
                        lambda x: x >= start_date_met)

    (window_delays,
     window_durations,
     window_gaps) = test._get_window_info(windows,
                                          start_date_met,
                                          idx_ww_sd)
    
    delays, wait_times = test._get_combined_windows(window_delays,
                                                    window_durations,
                                                    window_gaps,
                                                    5000,
                                                    idx_ww_sd)

    assert all(x < y for x, y in zip(delays, delays[1:]))    
    assert all(x > 0 for x in wait_times)
    assert delays[-1] < 87600


def test_WaitingTime_whole_window_strategy(metocean):
    
    test = WaitingTime(metocean)
    
    olc = {'maxHs': 4,
           'maxTp': 15,
           'maxWs': 15}
    
    windows = test.get_weather_windows(olc)
    start_date = dt.datetime(2000, 12, 25)

    start_delay, waiting_time = test._whole_window_strategy(windows,
                                                            start_date,
                                                            100)
    assert waiting_time is None
    assert np.isclose(start_delay, 50.5)
    

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
    

def test_WaitingTime_combined_window_strategy(metocean):
    
    test = WaitingTime(metocean)
    
    olc = {'maxHs': 4,
           'maxTp': 15,
           'maxWs': 15}
    
    windows = test.get_weather_windows(olc)
    start_date = dt.datetime(2000, 1, 1)

    start_delay, waiting_time = test._combined_window_strategy(windows,
                                                               start_date,
                                                               5000)
    
    assert np.isclose(start_delay, 2179.5)
    assert np.isclose(waiting_time, 2098.5)
    
    
def test_WaitingTime_combined_window_strategy_short(metocean):
    
    test = WaitingTime(metocean)
    
    olc = {'maxHs': 4,
           'maxTp': 15,
           'maxWs': 15}
    
    windows = test.get_weather_windows(olc)
    start_date = dt.datetime(2000, 1, 1)

    start_delay, waiting_time = test._combined_window_strategy(windows,
                                                               start_date,
                                                               100)
    
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
                    1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                    1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                    1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                    1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                    1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                    1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                    0.,  0.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                    1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  0.,
                    0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                    0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                    0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
                    1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                    1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                    1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                    1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                    1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                    1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,
                    1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.])
    
    result = get_window_indexes(wdx, 2)
    indexes = result.keys()
    durations = result.values()
    
    assert all(x < y for x, y in zip(indexes, indexes[1:]))    
    assert all(x > 0 for x in durations)
    assert len(result) == 3
    assert indexes[1] == 86
    assert durations[0] == 148


@pytest.mark.parametrize("test_input, expected", [
    ([1,2,3,4,1], [[1, 2, 3, 4], [1]]),
    ([1], [[1]]),
    ([], [])
])
def test_get_groups(test_input, expected):
    
    result = get_groups(test_input)
    
    assert result == expected
