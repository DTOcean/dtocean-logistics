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
