# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 13:20:13 2017

@author: mtopper
"""

import os

import pytest
import pandas as pd

this_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(this_dir, "..", "test_data")


@pytest.fixture(scope="session")
def site():
    
    path = os.path.join(data_dir, "site.xlsx")
    df = pd.read_excel(path, index_col=0)
    
    return df

@pytest.fixture(scope="session")
def device():
    
    path = os.path.join(data_dir, "device.xlsx")
    df = pd.read_excel(path, index_col=0)
    
    return df


@pytest.fixture(scope="session")
def sub_device():
    
    path = os.path.join(data_dir, "sub_device.xlsx")
    df = pd.read_excel(path, index_col=0)
    
    return df


@pytest.fixture(scope="session")
def layout():
    
    layout_dict = {"device [-]": ["device001",
                                  "device002",
                                  "device003",
                                  "device004"],
                   "x coord [m]": [367391, 367246, 367226, 367046],
                   "y coord [m]": [6125723, 6125433, 6125233, 6125033],
                   "zone [-]": ["30 U"] * 4}
    
    layout = pd.DataFrame(layout_dict)
    
    return layout
