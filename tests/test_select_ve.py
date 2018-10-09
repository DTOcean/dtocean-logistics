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

from dtocean_logistics.selection.select_ve import log_match_e, log_match_v

this_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(this_dir, "..", "test_data")


@pytest.fixture(scope="module")
def rov():
    
    data_path = os.path.join(data_dir, "rov.xlsx")
    df = pd.read_excel(data_path)
    
    return df


@pytest.fixture(scope="module")
def jupbarge():
    
    data_path = os.path.join(data_dir, "jupbarge.xlsx")
    df = pd.read_excel(data_path)
    
    return df


def test_get_burial_equip(rov):
    
    e_type = "rov"
    e_meth = "sup"
    e_para = "Depth rating [m]"
    e_val = 19.0
    e_pd_nan = rov
    feas_e_pd = rov.copy()
    
    feas_e_pd = feas_e_pd.drop(feas_e_pd.index[[1, 3]])
    
    log_match_e(e_type, e_meth, e_para, e_val, e_pd_nan, feas_e_pd)
    
    assert True
    

def test_get_burial_equip_all(rov):
    
    e_type = "rov"
    e_meth = "sup"
    e_para = "Depth rating [m]"
    e_val = 19.0
    e_pd_nan = rov
    feas_e_pd = rov.copy()
    
    feas_e_pd = feas_e_pd.drop(feas_e_pd.index[[0, 1, 2, 3, 4]])
    
    log_match_e(e_type, e_meth, e_para, e_val, e_pd_nan, feas_e_pd)
    
    assert True


def test_log_match_v(jupbarge):

    v_meth = "sup"
    v_para = "Deck loading [t/m^2]"
    v_val = 9.7362075759
    v_pd_nan = jupbarge
    feas_v_pd = jupbarge.copy()
    
    feas_v_pd = feas_v_pd.drop(feas_v_pd.index[[1, 3]])
    
    log_match_v(v_meth, v_para, v_val, v_pd_nan, feas_v_pd)
    
    assert True
