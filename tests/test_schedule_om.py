# -*- coding: utf-8 -*-

#    Copyright (C) 2021 Mathew Topper
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

# pragma pylint: disable=no-name-in-module

from datetime import datetime

from dtocean_logistics.performance.schedule.schedule_om import (SchedOM,
                                                                get_start)


def test_SchedOM_init():
    result = SchedOM()
    assert isinstance(result, SchedOM)


def test_get_start_dt():
    
    now = datetime.now()
    om = {'t_start [-]': [now]}
    
    test = get_start(om)
    expected = now.replace(minute=0, second=0, microsecond=0)
    assert test == expected


def test_get_start_string():
    
    now = datetime.now()
    datestr = now.strftime("%d:%m:%Y %H:%M:%S")
    om = {'t_start [-]': [datestr]}
    
    test = get_start(om)
    expected = now.replace(minute=0, second=0, microsecond=0)
    assert test == expected
