# -*- coding: utf-8 -*-

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
