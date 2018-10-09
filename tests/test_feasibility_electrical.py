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

from dtocean_logistics.feasibility.electrical import dynamic_feas

this_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(this_dir, "..", "test_data")


@pytest.fixture(scope="module")
def dynamic_cable():
    
    path = os.path.join(data_dir, "dynamic_cable.xlsx")
    df = pd.read_excel(path, index_col=0)
    
    return df


@pytest.fixture(scope="module")
def connectors():
    
    path = os.path.join(data_dir, "connectors.xlsx")
    df = pd.read_excel(path, index_col=0)
    
    return df


def test_dynamic_feas(site, dynamic_cable, connectors):

    (feas_e,
     feas_v,
     feas_m_pv,
     feas_m_pe,
     feas_m_ve,
     deck_req) = dynamic_feas(None, None, site, dynamic_cable, connectors)
    
    assert "rov" in feas_e
    assert set(feas_v.keys()) == set(['CLB', 'CLV'])
    assert set(feas_m_pv.keys()) == set(['CLB', 'CLV'])
    assert not feas_m_pe
    assert "rov" in feas_m_ve
    assert all([v >= 0 for k, v in deck_req.items()])
