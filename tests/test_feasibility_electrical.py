# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 13:20:13 2017

@author: mtopper
"""

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
