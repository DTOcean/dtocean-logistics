# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is the second and last part of the selection step in the WP5 methodology.
It contains functions to make the compatibility check between the characteristics
of port/vessel, port/equipment and vessel/equipment, returning only the feasible
and compatible solutions of vessels and equipments to perform the operations
sequence of the logistic phase.

BETA VERSION DETAILS: up to date, the functionalities explained previously have
not been implemented, this module should suffer major changes for the beta version
"""
import itertools
import numpy
import sys
import math

import logging
module_logger = logging.getLogger(__name__)

def compatibility_ve(install, log_phase, port_chosen_data):
    """This function is currently limited to the selection of the first two
    feasible solutions for the installation logistic phase in analysis.

    Parameters
    ----------
    install : dict
     not used
    log_phase : class
     class of the logistic phase under consideration for assessment, contains
     data refered to the feasible vessel and equipment combinations specific of
     each operation sequence of the logistic phase

    Returns
    -------
    sol : dict
     A dict of panda dataframes with unique feasible solutions
    log_phase : class
     An updated version of the log_phase argument containing only the feasible
     equipments within each vessel and equipment combinations dataframes
    """

    # deck requirements for structure (device. mooring or electrical) being installed
    deck_req = install['requirement'][5]
    deck_area_req = deck_req['deck area']
    deck_cargo_req = deck_req['deck cargo']
    deck_loading_req = deck_req['deck loading']

    sols_ve_indxs_combs_inseq = []
    len_sols_ve_indxs_comb_acum = 0
    # Go through different sequence options
    for seq in log_phase.op_ve:
        
        sols_ve_indxs_combs_incomb = []
        # Go through different possible combination
        for combi in range(len(log_phase.op_ve[seq].ve_combination)):
            # initialise solution variables
            ves_sol = {}
            ves_indexs = {}
            eq_sol = {}
            eq_indexs = {}
            #  Go through vessels
            nr_diff_ves = len(log_phase.op_ve[seq].ve_combination[combi]['vessel']) # nr_diff_ves in combination
            for ves_type in range(nr_diff_ves):
                ves = {}
                ves_index_vec = {}

                ves_quant = log_phase.op_ve[seq].ve_combination[combi]['vessel'][ves_type][0]  # Quantity of vessels in the solution
                ves_class = log_phase.op_ve[seq].ve_combination[combi]['vessel'][ves_type][1]  # Vessel class
                type_of_ves = log_phase.op_ve[seq].ve_combination[combi]['vessel'][ves_type][1].id 
             
                if type_of_ves == 'Tugboat': # Reduce the number of combinations
                    ves_index_vec = ((ves_class.panda['Op min Day Rate [EURO/day]']+ves_class.panda['Op max Day Rate [EURO/day]'])/2).idxmin() # Get only the first index that correspond to vessel class 
                    ves_index_vec = [ves_index_vec]
                    nr_feas_vess_i = 1  # Number of feasible vessels within vessel type 
                elif type_of_ves == 'Multicat' and ves_type != 0: # Reduce the number of combinations (Multicat should not be an installation vessel)
                    ves_index_vec = ((ves_class.panda['Op min Day Rate [EURO/day]']+ves_class.panda['Op max Day Rate [EURO/day]'])/2).idxmin() # Get only the first index that correspond to vessel class 
                    ves_index_vec = [ves_index_vec]
                    nr_feas_vess_i = 1  # Number of feasible vessels within vessel type                                     
                else:
                    ves_index_vec = ves_class.panda.index  # Get indexs that correspond to vessel class                     
                    nr_feas_vess_i = len(ves_index_vec)  # Number of feasible vessels within vessel type

                for indx_vec in range(nr_feas_vess_i):
                  # ves[indx_vec] = ves_class.panda.ix[indx_vec]  # Get info of the feasible vessels
                  ves[indx_vec] = ves_class.panda.ix[ves_index_vec[indx_vec]]

                ves_sol[ves_type] = {'type': type_of_ves, 'quantity': ves_quant,
                                     'Series': ves, 'indexs': ves_index_vec}  # Store info of the vessels
                ves_indexs[ves_type] = list(ves_index_vec)  # Vector of indexs of feasible vessels per type

            #  Go through equips
            nr_diff_equi = len(log_phase.op_ve[seq].ve_combination[combi]['equipment'])
            for eq_type in range(nr_diff_equi):
                eq = {}
                eq_index_vec = {}

                eq_quant = log_phase.op_ve[seq].ve_combination[combi]['equipment'][eq_type][0]  # Quantity of vessels in the solution
                eq_class = log_phase.op_ve[seq].ve_combination[combi]['equipment'][eq_type][1]  # Equipment class
                type_of_eq = log_phase.op_ve[seq].ve_combination[combi]['equipment'][eq_type][1].id
                eq_reltd_ves = log_phase.op_ve[seq].ve_combination[combi]['equipment'][eq_type][2]

                if type_of_eq == 'rov':  # Reduce the number of combinations
                    eq_index_vec = eq_class.panda['ROV day rate [EURO/day]'].idxmin()  # Get only the first index that correspond to vessel class 
                    eq_index_vec = [eq_index_vec]
                    nr_feas_eq_i = 1  # Number of feasible vessels within vessel type                    
                elif type_of_eq == 'split pipe': # Reduce the number of combinations
                    eq_index_vec = eq_class.panda['Cost per unit [EURO]'].idxmin()  # Get only the first index that correspond to vessel class 
                    eq_index_vec = [eq_index_vec]
                    nr_feas_eq_i = 1  # Number of feasible vessels within vessel type                      
                else:
                    eq_index_vec = eq_class.panda.index  # Get indexs that correspond to vessel class                     
                    nr_feas_eq_i = len(eq_index_vec)  # Number of feasible vessels within vessel type
                    
                for indx_vec in range(nr_feas_eq_i):
#                    eq[indx_vec] = eq_class.panda.ix[indx_vec]  # Get info of the feasible equipments
                    eq[indx_vec] = eq_class.panda.ix[eq_index_vec[indx_vec]]
                # eq_sol[eq_type] = {'type': type_of_eq, 'quantity': eq_quant,
                #                  'Series': eq, 'indexs': eq_index_vec, 'req_vessel': ves_sol[eq_reltd_ves]['type']}  # Store info of the equipments

                eq_sol[eq_type] = {'type': type_of_eq, 'quantity': eq_quant,
                                 'Series': eq, 'indexs': eq_index_vec, 'req_vessel': eq_reltd_ves}  # Store info of the equipments
                eq_indexs[eq_type] = list(eq_index_vec)  # Vector of indexs of feasible equipments per type

            # Build solutions
            sols_ves = []
            for ves_type in range(nr_diff_ves):  # Agregatte vessel type solutions
                VES = []
                for ves_intype in range(len(ves_sol[ves_type]['Series'])):
                    ves_type_name = ves_sol[ves_type]['type']
                    ves_type_quant = ves_sol[ves_type]['quantity']
                    ves_type_panda = ves_sol[ves_type]['Series'][ves_intype]
                    VES.append( [ves_type_name, ves_type_quant, ves_type_panda] )

                sols_ves.append(VES)

            sols_eq = []
            for eq_type in range(nr_diff_equi):  # Agregatte equipment type solutions
                EQS = []
                for eqs_intype in range(len(eq_sol[eq_type]['Series'])):
                    eq_type_name = eq_sol[eq_type]['type']
                    eq_type_quant = eq_sol[eq_type]['quantity']
                    eq_type_panda = eq_sol[eq_type]['Series'][eqs_intype]
                    eq_type_relation = eq_sol[eq_type]['req_vessel']
                    EQS.append( [eq_type_name, eq_type_quant, eq_type_panda, eq_type_relation] )

                sols_eq.append(EQS)
                
            sols_v_indxs_combs = list(itertools.product(*sols_ves))  # Combine vessel solutions
            sols_e_indxs_combs = list(itertools.product(*sols_eq))  # Combine equipment solutions
            sols_ve_indxs_sprt = (sols_v_indxs_combs, sols_e_indxs_combs)  # Agregatte vessel and equipment solutions
            sols_ve_indxs_comb = list(itertools.product(*sols_ve_indxs_sprt))  # Combine solutions
            sols_ve_indxs_combs_incomb.append(sols_ve_indxs_comb)  # Store solution per combination
            len_sols_ve_indxs_comb_acum += len(sols_ve_indxs_comb)

        sols_ve_indxs_combs_inseq.append(sols_ve_indxs_combs_incomb)  # Store solution per sequence

    # print 'output from itertools:' # FOR DEBUGGING!!!
    nr_sol_feas = len_sols_ve_indxs_comb_acum

    # Apply MATCHING

    # *** Vessel/Equipment ***
    req_m_ev = install['requirement'][4]
    sols_ve_indxs_combs_inseq = compatibility_vessels(
                                                    req_m_ev,
                                                    log_phase,
                                                    sols_ve_indxs_combs_inseq,
                                                    deck_area_req,
                                                    deck_cargo_req,
                                                    deck_loading_req)

    # *** Port/Vessel ***
    port_pd = port_chosen_data
    req_m_pv = install['requirement'][2]
    sols_ve_indxs_combs_inseq = compatibility_ports(req_m_pv,
                                                    log_phase,
                                                    sols_ve_indxs_combs_inseq,
                                                    port_pd)

    # # *** Port/Equipment ***
    # req_m_pe = install['requirement'][3]
    # match_rq_pe = dict.fromkeys(req_m_pe.keys())
    # Vessel/Equipment
    # print 'Vessel/Equipment:'


    # Shape solution for performance:
    final_sol = []
    Num_sols = 0
    for seq in range(len(sols_ve_indxs_combs_inseq)):
        sol = {}
        sols_iter = 0
        for combi in range(len(sols_ve_indxs_combs_inseq[seq])):
            for sols in range(len(sols_ve_indxs_combs_inseq[seq][combi])):
                sol_i = sols_ve_indxs_combs_inseq[seq][combi][sols]
                vels = sol_i[0]
                equips = sol_i[1]

                # sol[sols_iter] = { 'port': port_chosen_data, str(sols): [list(vels), list(equips)] }
                # OR
                ve_sols=[]
                for ind_ves_sol in range(len(vels)):
                    sol[sols_iter] = {'port': port_chosen_data}
                    ve_sol = list(vels[ind_ves_sol])
                    for ind_eq_sol in range(len(equips)):
                        ves_dpend = equips[ind_eq_sol][3]
                        if ves_dpend==ind_ves_sol:
                            ve_sol.append( list(equips[ind_eq_sol]) )
                    ve_sols.append(ve_sol)
                sol[sols_iter].update ( {'VEs': ve_sols} )

                sols_iter = sols_iter + 1

                # continue

        log_phase.op_ve[seq].sol = sol
        final_sol.append(log_phase.op_ve[seq].sol)
        Num_sols = Num_sols + len(log_phase.op_ve[seq].sol)


    # print 'Number of solutions found: ' + str(Num_sols)
    nr_sol_match = Num_sols

    if Num_sols==0:

        EXIT_FLAG = 'NoSolutions'
        
        logMsg = ("No vessel and equipment combinations found for "
                  "log phase: {}").format(log_phase.description)
        module_logger.critical(logMsg)

    else:

        EXIT_FLAG = 'SolutionsFound'

    log_phase.nr_sol_feas = nr_sol_feas
    log_phase.nr_sol_match = nr_sol_match

    return final_sol, log_phase, EXIT_FLAG


def compatibility_vessels(req_m_ev,
                          log_phase,
                          sols_ve_indxs_combs_inseq,
                          deck_area_req,
                          deck_cargo_req,
                          deck_loading_req):
    
    # *** Vessel/Equipment ***
    new_combs_inseq = []

    for combin in sols_ve_indxs_combs_inseq:
        
        new_ve_combinations = []
        
        for ve_combinations in combin:
            
            valid_combs = []

            for ve_comb in ve_combinations:

                ve_comb_ves = ve_comb[0]
                ve_comb_eqs = ve_comb[1]
                all_combos = True
                
                for eq_in_combi in ve_comb_eqs:

                    m_e_key_type = eq_in_combi[0]
                    eq_pd = eq_in_combi[2] # panda series data
                    req_ves = eq_in_combi[3]  # vessel (index) required to use equipment

                    ves_pd = ve_comb_ves[req_ves][2] # panda series data
                    
                    if m_e_key_type in req_m_ev:
                        
                        check_combo = check_vessels(ve_comb_eqs,
                                                    m_e_key_type,
                                                    req_m_ev,
                                                    eq_pd,
                                                    ves_pd,
                                                    deck_area_req,
                                                    deck_cargo_req,
                                                    deck_loading_req)
                        
                        all_combos = all_combos and check_combo
                            
                if all_combos: valid_combs.append(ve_comb)
                
            new_ve_combinations.append(valid_combs)
            
        new_combs_inseq.append(new_ve_combinations)
        
    return new_combs_inseq


def check_vessels(ve_comb_eqs,
                  m_ev_key_req,
                  req_m_ev,
                  eq_pd,
                  ves_pd,
                  deck_area_req,
                  deck_cargo_req,
                  deck_loading_req):

    for m_ev_read in req_m_ev[m_ev_key_req]:
        
        if m_ev_read[0] == 'PI': # specific to rock filter bags
            aux_op = math.pi
        elif m_ev_read[0] == '4': # specific to rock filter bags
            aux_op = 4.0
        else:
            aux_op = eq_pd[m_ev_read[0]]

        for ind_rd in range(1, len(m_ev_read) - 1, 2):
            
            next_ind = ind_rd + 1
           
            if m_ev_read[ind_rd] == 'plus':
               
                aux_op = aux_op + eq_pd[m_ev_read[ind_rd + 1]]
               
            elif m_ev_read[ind_rd] == 'mul':
               
                aux_op = aux_op * eq_pd[m_ev_read[ind_rd + 1]]
               
            elif m_ev_read[ind_rd] == 'div':
               
                aux_op = aux_op / eq_pd[m_ev_read[ind_rd + 1]]
               
            elif m_ev_read[ind_rd] == 'sup':
               
                if (deck_area_req == 'matching' or
                    deck_cargo_req == 'matching' or
                    deck_loading_req == 'matching'): # specific to external protection
                   
                    area_req = [0]
                    cargo_req = [0]
                    load_req = [0]
                   
                    for test in ve_comb_eqs:
                       
                        dims = test[2]
                       
                        if test[0] == 'mattress':
                           
                            area = dims['Unit lenght [m]'] * \
                                                   dims['Unit width [m]']
                            cargo = dims['Unit weight air [t]']
                            load = cargo / area
                           
                            area_req.append(area)
                            cargo_req.append(cargo)
                            load_req.append(load)
                            
                        elif test[0] == 'rock filter bags ':
                            
                            area = (math.pi / 4.) * dims['Diameter [m]'] ** 2
                            cargo = dims['Unit weight air [t]']
                            load = cargo / area

                            area_req.append(area)
                            cargo_req.append(cargo)
                            load_req.append(load)
                            
                    deck_area_req = sum(area_req)
                    deck_cargo_req = sum(cargo_req)
                    deck_loading_req = max(load_req)
                   
                if m_ev_read[next_ind] == 'Deck space [m^2]':
                    req_check = aux_op + deck_area_req
                elif m_ev_read[next_ind] == 'Max cargo [t]':
                    req_check = aux_op + deck_cargo_req
                elif m_ev_read[next_ind] == 'Deck loading [t/m^2]':
                    req_check = aux_op + deck_loading_req
                else:
                    req_check = aux_op
                    
                val_check = ves_pd[m_ev_read[next_ind]]

                if not numpy.isnan(val_check) and val_check < req_check:
                    
                    log_match_vessel(ves_pd,
                                     m_ev_read[ind_rd],
                                     m_ev_read[next_ind],
                                     req_check)
                    
                    return False

            elif m_ev_read[ind_rd] == 'equal':
               
                if m_ev_read[next_ind] == 'Deck space [m^2]':
                    req_check = aux_op + deck_area_req
                elif m_ev_read[next_ind] == 'Max cargo [t]':
                    req_check = aux_op + deck_cargo_req
                elif m_ev_read[next_ind] == 'Deck loading [t/m^2]':
                    req_check = aux_op + deck_loading_req
                else:
                    req_check = aux_op
                    
                val_check = ves_pd[m_ev_read[next_ind]]

                if not numpy.isnan(val_check) and val_check != req_check:
                    
                    log_match_vessel(ves_pd,
                                     m_ev_read[ind_rd],
                                     m_ev_read[next_ind],
                                     req_check)
                    
                    return False
                
    return True


def compatibility_ports(req_m_pv,
                        log_phase,
                        sols_ve_indxs_combs_inseq,
                        port_pd):
    
    # *** Port/Vessel ***
    new_combs_inseq = []

    for combin in sols_ve_indxs_combs_inseq:
        
        new_ve_combinations = []
        
        for ve_combinations in combin:
            
            valid_combs = []

            for ve_comb in ve_combinations:

                ve_comb_ves = ve_comb[0]
                ve_comb_eqs = ve_comb[1]
                all_combos = True
                
                for eq_in_combi in ve_comb_eqs:

                    m_pv_key_req = eq_in_combi[0]
                    req_ves = eq_in_combi[3]  # vessel (index) required to use equipment

                    ves_pd = ve_comb_ves[req_ves][2] # panda series data
                    
                    if m_pv_key_req in req_m_pv:
                                                
                        check_combo = check_ports(ve_comb_eqs,
                                                  m_pv_key_req,
                                                  req_m_pv,
                                                  port_pd,
                                                  ves_pd)
                        
                        all_combos = all_combos and check_combo
                            
                if all_combos: valid_combs.append(ve_comb)
                
            new_ve_combinations.append(valid_combs)
            
        new_combs_inseq.append(new_ve_combinations)
        
    return new_combs_inseq


def check_ports(ve_comb_eqs,
                m_pv_key_req,
                req_m_pv,
                port_pd,
                ves_pd):
    
    for m_pv_read in req_m_pv[m_pv_key_req]:

        if not m_pv_read[0] == 'Jacking capability [yes/no]':
            aux_op = ves_pd[m_pv_read[0]]

        for ind_rd in range(1, len(m_pv_read) - 1, 2):
           
            next_ind = ind_rd + 1
           
            if m_pv_read[ind_rd] == 'plus':
               
                aux_op = aux_op + ves_pd[m_pv_read[next_ind]]
               
            elif m_pv_read[ind_rd] == 'mul':
               
                aux_op = aux_op * ves_pd[m_pv_read[next_ind]]
               
            elif m_pv_read[ind_rd] == 'div':
               
                aux_op = aux_op / ves_pd[m_pv_read[next_ind]]
               
            elif m_pv_read[ind_rd] == 'sup':
               
                req_check = aux_op
                val_check = port_pd[m_pv_read[next_ind]]
                    
                if not numpy.isnan(val_check) and val_check < req_check:
                    
                    log_match_port(port_pd,
                                   m_pv_read[ind_rd],
                                   m_pv_read[next_ind],
                                   req_check)
                    
                    return False

            elif m_pv_read[ind_rd] == 'equal':
                
                if m_pv_read[ind_rd - 1] == 'Jacking capability [yes/no]':
                   
                    # Jack-up vessel is incompatible with port
                    if port_pd['Jacking capability [yes/no]'] == 'no':
                        
                        log_match_port(port_pd,
                                       m_pv_read[ind_rd],
                                       m_pv_read[next_ind],
                                       req_check)
                        
                        return False
                    
                else:
                    
                    req_check = aux_op
                    val_check = port_pd[m_pv_read[next_ind]]
                    
                    if not numpy.isnan(val_check) and val_check != req_check:
                    
                        log_match_port(port_pd,
                                       m_pv_read[ind_rd],
                                       m_pv_read[next_ind],
                                       req_check)
                        
                        return False


def log_match_vessel(ves_pd, meth, para, val):
    
    logStr = ("Vessel(s) '{}' from class '{}' did not meet "
              "requirement (including any safety factors): ").format(
                                                  ves_pd["Name"],
                                                  ves_pd["Vessel type [-]"])
    log_match(logStr, meth, para, val)
    
    return


def log_match_port(port_pd, meth, para, val):
    
    logStr = ("Port '{}' did not meet requirement (including any safety "
              "factors): ").format(port_pd["Name"])
    log_match(logStr, meth, para, val)
    
    return


def log_match(logStr, meth, para, val):
    
    if meth == "sup":
        requirement_str = "{} => {}"
    elif meth == "equal":
        requirement_str = "{} == {}"
        
    requirement_str = requirement_str.format(para, val)
        
    logStr = logStr + "{}".format(requirement_str)
    
    module_logger.info(logStr)
    
    return
                   