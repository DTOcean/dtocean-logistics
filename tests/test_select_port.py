
import os

import pytest
import pandas as pd

from dtocean_logistics.phases.select_port import get_max_load_area_foundations

this_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(this_dir, "..", "test_data")


@pytest.fixture(scope="module")
def foundations():
    
    path = os.path.join(data_dir, "foundations.xlsx")
    df = pd.read_excel(path)
    
    return df
    

def test_get_max_load_area_foundations(foundations):
    
    load, area = get_max_load_area_foundations(foundations)
    
    assert load > 0.
    assert area > 0.
        