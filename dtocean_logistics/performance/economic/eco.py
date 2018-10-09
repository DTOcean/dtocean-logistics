# -*- coding: utf-8 -*-

#    Copyright (C) 2016 Boris Teillant, Paulo Chainho, Pedro Vicente
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

"""
This module is responsible for the cost step in the Logistics methodology. It contains
functions to calculate the cost of each solution based on the schedule, day rates
of vessels and equipments and port economic assessment.

.. moduleauthor:: Boris Teillant <boris.teillant@wavec.org>
.. moduleauthor:: Paulo Chainho <paulo@wavec.org>
.. moduleauthor:: Pedro Vicente <pedro.vicente@wavec.org>
.. moduleauthor:: Mathew Topper <mathew.topper@dataonlygreater.com>
"""

import numpy as np

import logging
module_logger = logging.getLogger(__name__)

def cost(module, log_phase, log_phase_id, other_rates):
    sol = {}
    # loop over the number of operation sequencing options
    for seq in range(len(log_phase.op_ve)):
        # loop over the number of solutions, i.e feasible combinations of port/vessel(s)/equipment(s)
        for ind_sol in range(len(log_phase.op_ve[seq].sol)):
            sched = log_phase.op_ve[seq].sol[ind_sol]['schedule']
            if log_phase_id == 'LpM6' or log_phase_id == 'LpM7':
                dur_sea_wait = sched['sea time_retrieve'] + \
                               sched['sea time_replace'] + \
                               sum(sched['waiting time_retrieve']) + \
                               sum(sched['waiting time_replace'])
                dur_prep = sched['prep time']
                nb_ves_type = len(log_phase.op_ve[seq].sol[ind_sol]['VEs'])
            else:
                dur_sea_wait = sched['sea time'] + sum(sched['waiting time'])
                dur_prep = sched['prep time']
                nb_ves_type = len(log_phase.op_ve[seq].sol[ind_sol]['VEs'])

            # loop over the nb of vessel types
            vessel_cost = []
            equip_cost_ves = []
            ves_GT = []
            ves_fuel_consm = []
            for vt in range(nb_ves_type):
                qty_vt = log_phase.op_ve[seq].sol[ind_sol]['VEs'][vt][1]
                ves_data = log_phase.op_ve[seq].sol[ind_sol]['VEs'][vt][2]
                ves_GT.append(ves_data['Gross tonnage [ton]'])
                if log_phase.op_ve[seq].description=='Towing transportation' or log_phase.description=='Onshore maintenance of devices or array sub-component - tow transport':
                    ves_fuel_consm.append(ves_data['Consumption towing [l/h]'])
                else:
                    ves_fuel_consm.append(ves_data['Consumption [l/h]'])
                op_cost_max = ves_data['Op max Day Rate [EURO/day]']
                op_cost_min = ves_data['Op min Day Rate [EURO/day]']
                mob_perc = np.nan_to_num(float(ves_data['Mob percentage [%]']))/100

                vessel_cost_h = np.mean([op_cost_max, op_cost_min])/24.0  # [€/hour]
                vessel_cost.append( qty_vt * ( vessel_cost_h*dur_sea_wait + mob_perc*vessel_cost_h*dur_prep ) )
                # vessel_cost.append( qty_vt * ( vessel_cost_h*dur_sea_wait + mob_perc*vessel_cost_h*dur_prep  + mob_perc*vessel_cost_h*dur_demob ) )


                # check if vessel carries any equipment
                nr_equip = len(log_phase.op_ve[seq].sol[ind_sol]['VEs'][vt]) - 3  #  first 3 elements are type, quant and series
                equip_cost_eq_i = []
                eq_cost = 0
                for eqp in range(nr_equip):
                    eq_type = log_phase.op_ve[seq].sol[ind_sol]['VEs'][vt][3+eqp][0]
                    qty_eqp = log_phase.op_ve[seq].sol[ind_sol]['VEs'][vt][3+eqp][1]
                    eq_data = log_phase.op_ve[seq].sol[ind_sol]['VEs'][vt][3+eqp][2]

                    if eq_type == 'rov':
                        if not np.isnan(eq_data['ROV day rate [EURO/day]']):
                            eq_cost += eq_data['ROV day rate [EURO/day]']
                        if not np.isnan(eq_data['AE supervisor [-]']*eq_data['Supervisor rate [EURO/12h]']):
                            eq_cost += eq_data['AE supervisor [-]']*eq_data['Supervisor rate [EURO/12h]']*2.0
                        if not np.isnan(eq_data['AE technician [-]']*eq_data['Technician rate [EURO/12h]']):
                            eq_cost += eq_data['AE technician [-]']*eq_data['Technician rate [EURO/12h]']*2.0

                    elif eq_type == 'divers':
                        eq_cost = eq_data['Total day rate [EURO/day]'] # [€/day]

                    elif eq_type == 'plough' or eq_type == 'jetter' or eq_type == 'cutter':
                        if not np.isnan(eq_data['Burial tool day rate [EURO/day]']):
                            eq_cost += eq_data['Burial tool day rate [EURO/day]']
                        if not np.isnan(eq_data['Personnel day rate [EURO/12h]']):
                            eq_cost += eq_data['Personnel day rate [EURO/12h]']*2.0 # [€/day]

                    elif eq_type == 'excavating':
                        if not np.isnan(eq_data['Excavator day rate [EURO/day]']):
                            eq_cost += eq_data['Excavator day rate [EURO/day]']
                        if not np.isnan(eq_data['Personnel day rate [EURO/12h]']):
                            eq_cost += eq_data['Personnel day rate [EURO/12h]']*2.0 # [€/day]

                    elif eq_type == 'mattress':
                        eq_cost = eq_data['Cost per unit [EURO]']

                    elif eq_type == 'rock_filter_bags':
                        eq_cost = eq_data['Cost per unit [EURO]']

                    elif eq_type == 'split pipe':
                        eq_cost = eq_data['Cost per unit [EURO]']

                    elif eq_type == 'hammer':
                        if not np.isnan(eq_data['Hammer day rate [EURO/day]']):
                            eq_cost += eq_data['Hammer day rate [EURO/day]']
                        if not np.isnan(eq_data['Personnel day rate [EURO/12h]']):
                            eq_cost += eq_data['Personnel day rate [EURO/12h]']*2.0 # [€/day]

                    elif eq_type == 'drilling rigs':
                        if not np.isnan(eq_data['Drill rig day rate [EURO/day]']):
                            eq_cost += eq_data['Drill rig day rate [EURO/day]']
                        if not np.isnan(eq_data['Personnel day rate [EURO/day]']):
                            eq_cost += eq_data['Personnel day rate [EURO/day]'] # [€/day]

                    elif eq_type == 'vibro driver': # ?!?!
                        if not np.isnan(eq_data['Vibro diver day rate [EURO/day]']):
                            eq_cost += eq_data['Vibro diver day rate [EURO/day]']
                        if not np.isnan(eq_data['Personnel day rate [EURO/day]']):
                            eq_cost += eq_data['Personnel day rate [EURO/day]'] # [€/day]

                    else:
#                        msg = ("Cost for equipment {} not available. This is "
#                               "omitted from the total installation "
#                               "cost.".format(eq_type))

#                        module_logger.warning(msg)

                        eq_cost = 0

                    # check if the cost is unitary or time dependent                   
                    if eq_type == 'mattress' or eq_type == 'rock_filter_bags' or eq_type == 'split pipe':
                        eq_cost_h = 0
                        eq_cost_unit = eq_cost  # to be implemented?????

                    else:
                        eq_cost_h = eq_cost/24.0  # [€/day »» €/hour]
                        eq_cost_unit = 0
                        
                    equip_cost_eq_i.append(qty_eqp*(eq_cost_h*dur_sea_wait) + qty_eqp*eq_cost_unit)

                equip_cost_ves.append(sum(equip_cost_eq_i))

            equip_total_cost = float(sum(equip_cost_ves))
            vessel_total_cost = float(np.sum(vessel_cost))

            ves_GT_total = float(sum(ves_GT))
            if np.isnan(ves_fuel_consm).any():
                
#                module_logger.warning("Lack of information on vessel fuel "
#                                      "consumption, fuel cost not considered "
#                                      "for this installation phase.")

                ves_fuel_consm_total = 0
            else:
                ves_fuel_consm_total = float(sum(ves_fuel_consm))

            # FUEL COST: (plot separado para fuel cost???????????)
            cost_of_fuel = other_rates['Default values']['Fuel cost rate [EUR/l]']
            transit_time = sched['sea time']
            fuel_cost = cost_of_fuel * ves_fuel_consm_total * transit_time
            vessel_total_cost += fuel_cost

            # PORT COST:
            # port_cost_per_GT = module['port']['Selected base port for installation']['Tonnage charges [euro/GT]']
            # if np.isnan(port_cost_per_GT):
            #     pre_port_total_cost = float(0)
            # else:
            #     pre_port_total_cost = ves_GT_total * port_cost_per_GT

            # pre_total_cost = vessel_total_cost + equip_total_cost + pre_port_total_cost
            pre_total_cost = vessel_total_cost + equip_total_cost
            port_perc_cost = other_rates['Default values']['Port percentual cost [%]']/100.0
            port_total_cost = (port_perc_cost/(1-port_perc_cost)) * pre_total_cost # to change ?!?!?!?!?!?!??!?!?!?!?!?!??!?!?!?!?!?!??!?!?!?!?!?!??!?!?!?!?!?!??!?!?!?!?!?!??!?!?!?!?!?!??!?!?!?!?!?!?

            if np.isnan(vessel_total_cost):
                vessel_total_cost = 0
            if np.isnan(equip_total_cost):
                equip_total_cost = 0
            if np.isnan(port_total_cost):
                port_total_cost = 0

            log_phase.op_ve[seq].sol_cost[ind_sol] = {'vessel cost': vessel_total_cost, 'equipment cost': equip_total_cost, 'port cost': port_total_cost, 'fuel cost': fuel_cost,
                                                      'total cost': vessel_total_cost + equip_total_cost + port_total_cost}

        sol[seq] = log_phase.op_ve[seq].sol_cost

    return sol, log_phase
