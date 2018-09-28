# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 13:20:13 2017

@author: mtopper
"""

from dtocean_logistics.feasibility.SS import SS_feas


def test_dynamic_feas(site, sub_device, layout):

    (feas_e,
     feas_v,
     feas_m_pv,
     feas_m_pe,
     feas_m_ve,
     deck_req) = SS_feas(None, None, sub_device, layout, site)
    
    assert "rov" in feas_e
    assert set(feas_v.keys()) == set(['JUP Barge',
                                      'Crane Barge',
                                      'JUP Vessel',
                                      'CSV',
                                      'Crane Vessel'])
    assert set(feas_m_pv.keys()) == set(['Crane Vessel',
                                         'Tugboat',
                                         'JUP Barge',
                                         'Crane Barge',
                                         'Multicat',
                                         'CSV',
                                         'JUP Vessel'])
    assert not feas_m_pe
    assert "rov" in feas_m_ve
    assert all([v >= 0 for k, v in deck_req.items()])
