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

from dtocean_logistics.ancillaries import differences


@pytest.mark.parametrize("test_input, expected", [
    ([], []),
    ([1], []),
    ([1,2], [1]),
    ([1,2,4], [1,2]),
    ([-1,1], [2]),
    ([1,-1], [-2]),
])
def test_differences(test_input, expected):
    
    result = differences(test_input)
    
    assert result == expected
