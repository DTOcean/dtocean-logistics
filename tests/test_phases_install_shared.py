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

import pytest

from dtocean_logistics.phases.install.shared import get_burial_equip


@pytest.mark.parametrize("test_input, expected", [
    ('ploughing', 'plough'),
    ('jetting', 'jetter'),
    ('cutting', 'cutter'),
    ('dredging', 'dredge'),
    ('no burial', None),
    ('no data', 'plough'),
    (None, 'plough')
])
def test_get_burial_equip(test_input, expected):
    
    result = get_burial_equip(test_input)
    
    assert result == expected
