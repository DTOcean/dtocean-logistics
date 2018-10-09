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
        