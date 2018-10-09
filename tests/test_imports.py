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

def test_installation_imports():
    
    from dtocean_logistics.phases.operations import logOp_init
    from dtocean_logistics.phases.install import logPhase_install_init
    from dtocean_logistics.phases.install import planning
    from dtocean_logistics.phases import select_port
    from dtocean_logistics.feasibility.glob import glob_feas
    from dtocean_logistics.selection.select_ve import select_e, select_v
    from dtocean_logistics.selection.match import compatibility_ve
    from dtocean_logistics.performance.schedule.schedule_ins import sched
    from dtocean_logistics.performance.economic.eco import cost
    from dtocean_logistics.performance.optim_sol import opt_sol
    from dtocean_logistics.outputs.output_processing import out_process
    from dtocean_logistics.outputs.output_plotting2 import out_ploting
    from dtocean_logistics.load.safe_factors import safety_factors
    from dtocean_logistics.performance.economic.cost_year import cost_p_year

    assert True
