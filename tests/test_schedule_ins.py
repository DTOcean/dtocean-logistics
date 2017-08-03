
import os
import datetime as dt

import pytest
import numpy as np
import pandas as pd

from dtocean_logistics.ancillaries.find import indices
from dtocean_logistics.performance.schedule.schedule_ins import (
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
    assert np.isclose(start_delay, 156)
    

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
    
    assert start_delay == 27507
    assert waiting_time == 393
    
    
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
