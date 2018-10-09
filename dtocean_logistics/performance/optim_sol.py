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
The function opt_sol indicates based on the cost calculation for each solution,
the minimal cost and respective solution

.. moduleauthor:: Boris Teillant <boris.teillant@wavec.org>
.. moduleauthor:: Paulo Chainho <paulo@wavec.org>
.. moduleauthor:: Pedro Vicente <pedro.vicente@wavec.org>
.. moduleauthor:: Mathew Topper <mathew.topper@dataonlygreater.com>
"""


def opt_sol(log_phase, log_phase_id):

    # loop over the number of operation sequencing options
    sol_index_inseq_vec = []
    for seq in range(len(log_phase.op_ve)):
        # loop over the number of solutions, i.e feasible combinations of port/vessel(s)/equipment(s)
        total_cost_vec = []
        if not len(log_phase.op_ve[seq].sol) == 0: # a strategy with no solutions!
            for ind_sol in range(len(log_phase.op_ve[seq].sol)):
                vessel_cost = log_phase.op_ve[seq].sol_cost[ind_sol]['vessel cost']
                equip_cost = log_phase.op_ve[seq].sol_cost[ind_sol]['equipment cost']
                port_cost = log_phase.op_ve[seq].sol_cost[ind_sol]['port cost']
                fuel_cost = log_phase.op_ve[seq].sol_cost[ind_sol]['fuel cost']
                total_cost = log_phase.op_ve[seq].sol_cost[ind_sol]['total cost']
                strategy = log_phase.op_ve[seq].description
                total_cost_vec.append([total_cost, vessel_cost, equip_cost, port_cost, fuel_cost, ind_sol, seq, strategy])
                # total_cost_vec.append(total_cost)
                # min_total_cost = min(total_cost_vec)
                # if min_total_cost == total_cost:
                #     sol_index_inseq = [total_cost, vessel_cost, equip_cost, port_cost, ind_sol, seq]

            min_total_cost = min(total_cost_vec)
            sol_index_inseq_vec.append(min_total_cost)

    min_sol_cost_sorted = sorted(sol_index_inseq_vec)
    # min_sol_cost_sorted = sol_index_inseq_vec
    # min_sol_cost_sorted.sort()
    min_total_cost_final_sol = min_sol_cost_sorted[0][0]
    min_vessel_cost_final_sol = min_sol_cost_sorted[0][1]
    min_equip_cost_final_sol = min_sol_cost_sorted[0][2]
    min_port_cost_final_sol = min_sol_cost_sorted[0][3]
    min_fuel_cost_final_sol = min_sol_cost_sorted[0][4]
    sol_nr_final_sol = min_sol_cost_sorted[0][5]
    seq_final_sol = min_sol_cost_sorted[0][6]
    strategy_sol = min_sol_cost_sorted[0][7]

    sol = log_phase.op_ve[seq_final_sol].sol[sol_nr_final_sol]
    if log_phase_id == 'LpM6' or log_phase_id == 'LpM7':
        sol_sched_seaoptime = sol['schedule']['sea time_retrieve'] + \
                            sol['schedule']['sea time_replace'] - sol['schedule']['transit time']
        sol_sched_seatransittime = sol['schedule']['transit time']
        sol_sched_seatime = sol['schedule']['sea time_retrieve'] + \
                            sol['schedule']['sea time_replace']
        sol_sched_waitingtime = sum(sol['schedule']['waiting time_retrieve'] \
                                    + sol['schedule']['waiting time_replace'])
        sol_sched_preptime = sol['schedule']['prep time_retrieve'] + \
                             sol['schedule']['prep time_replace']
        sol_sched_totaltime = sol['schedule']['total time_retrieve'] + \
                              sol['schedule']['total time_replace']
        sol_sched_nb_journeys = sol['schedule']['global']['nb of journeys_retrieve'] + \
                                sol['schedule']['global']['nb of journeys_replace']
        sol_sched_elems_p_journeys = sol['schedule']['global']['nb of elements per journey']
    else:
        sol_sched_seaoptime = sol['schedule']['sea time'] - sol['schedule']['transit time']
        sol_sched_seatransittime = sol['schedule']['transit time']
        sol_sched_seatime = sol['schedule']['sea time']
        sol_sched_waitingtime = sum(sol['schedule']['waiting time'])
        sol_sched_preptime = sol['schedule']['prep time']
        sol_sched_totaltime = sol['schedule']['prep time'] + sum(sol['schedule']['waiting time']) + sol['schedule']['sea time']
        sol_sched_nb_journeys = sol['schedule']['global']['nb of journeys']
        sol_sched_elems_p_journeys = sol['schedule']['global']['nb of elements per journey']

    start_dt = sol['schedule']['weather windows start_dt']
    depart_dt = sol['schedule']['weather windows depart_dt']
    end_dt = sol['schedule']['weather windows end_dt']

    sol = {'total cost': min_total_cost_final_sol,
           'vessel cost': min_vessel_cost_final_sol,
           'equipment cost': min_equip_cost_final_sol,
           'port cost': min_port_cost_final_sol,
           'fuel cost': min_fuel_cost_final_sol,
           'schedule sea operation time': sol_sched_seaoptime,
           'schedule sea transit time': sol_sched_seatransittime,
           'schedule sea time': sol_sched_seatime,
           'schedule waiting time': sol_sched_waitingtime,
           'schedule prep time': sol_sched_preptime,
           'schedule total time': sol_sched_totaltime,

           'start_dt': start_dt, 'depart_dt': depart_dt, 'end_dt': end_dt,

           'numb of journeys': sol_sched_nb_journeys,
           'elems per journey': sol_sched_elems_p_journeys,
           'logistic operations': sol['schedule']['global'],
           'strategy': strategy_sol,
           'vessel_equipment': sol['VEs']}

    return sol
