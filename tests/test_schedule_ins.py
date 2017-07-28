
import os

import pytest
import pandas as pd

from dtocean_logistics.performance.schedule.schedule_ins import (get_groups,
                                                                 WaitingTime)

this_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(this_dir, "..", "test_data")


@pytest.fixture(scope="module")
def metocean():
    
    metocean_path = os.path.join(data_dir, "metocean.xlsx")
    df = pd.read_excel(metocean_path)
    
    return df


@pytest.mark.parametrize("test_input, expected", [
    ([1,2,3,4,1], [[1, 2, 3, 4], [1]]),
    ([1], [[1]]),
    ([], [])
])
def test_get_groups(test_input, expected):
    
    result = get_groups(test_input)
    
    assert result == expected
    

def test_WaitingTime_init(metocean):
    
    result = WaitingTime(metocean)
    
    assert isinstance(result, WaitingTime)
    

def test_WaitingTime_get_weather_window(metocean):
    
    test = WaitingTime(metocean)
    
    olc = {'maxHs': 4,
           'maxTp': 15,
           'maxWs': 15}
    
    result = test.get_weather_window(olc)
    
    assert len(result['duration']) > 0
    assert (len(result['duration']) == 
            len(result['start_dt']) ==
            len(result['end_dt']))
        