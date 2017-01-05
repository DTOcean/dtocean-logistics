# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org, pedro.vicente@wavec.org

The function out_process processes the results to be outputed


"""

import numpy as np

def out_process(log_phase, module):


    # INITIAL:
    nr_ves_p_type=[]
    nr_ves_p_type_quant=[]
    nr_eq_p_type=[]
    nr_eq_p_type_quant=[]
    seq_descrip=[]
    op_in_seq_total={}
    nr_sols = 1
    for ind_seq in range(len(log_phase.op_ve_init)):

        seq_descrip.append( log_phase.op_ve_init[ind_seq].description )

        op_in_seq = []
        for ind_prep_op in range(len(log_phase.op_ve_init[ind_seq].op_seq_prep)):
            op_in_seq.append( log_phase.op_ve_init[ind_seq].op_seq_prep[ind_prep_op].description )
        for ind_sea_op in log_phase.op_ve_init[ind_seq].op_seq_sea.keys():
            for ind_smt in range(len(log_phase.op_ve_init[ind_seq].op_seq_sea[ind_sea_op])):
                op_in_seq.append( log_phase.op_ve_init[ind_seq].op_seq_sea[ind_sea_op][ind_smt].description )
        for ind_demob_op in range(len(log_phase.op_ve_init[ind_seq].op_seq_demob)):
            op_in_seq.append( log_phase.op_ve_init[ind_seq].op_seq_demob[ind_demob_op].description )
        op_in_seq_total.update( {log_phase.op_ve_init[ind_seq].description: op_in_seq} )


        for ind_combi in range(len(log_phase.op_ve_init[ind_seq].ve_combination)):

            for ind_ves_type in range(len(log_phase.op_ve_init[ind_seq].ve_combination[ind_combi]['vessel'])):
                new_vess = log_phase.op_ve_init[ind_seq].ve_combination[ind_combi]['vessel'][ind_ves_type][1].id
                new_vess_len = len(log_phase.op_ve_init[ind_seq].ve_combination[ind_combi]['vessel'][ind_ves_type][1].panda)
                vess_repeat=0
                for ind_vess in range(len(nr_ves_p_type)):
                    if new_vess == nr_ves_p_type[ind_vess]:
                        vess_repeat=1
                        break
                if vess_repeat==0:
                    nr_ves_p_type.append( new_vess )
                    nr_ves_p_type_quant.append( [new_vess, new_vess_len])
                    nr_sols *= new_vess_len

            for ind_eq_type in range(len(log_phase.op_ve_init[ind_seq].ve_combination[ind_combi]['equipment'])):
                new_eq = log_phase.op_ve_init[ind_seq].ve_combination[ind_combi]['equipment'][ind_eq_type][1].id
                new_eq_len = len(log_phase.op_ve_init[ind_seq].ve_combination[ind_combi]['equipment'][ind_eq_type][1].panda)
                eqs_repeat=0
                for ind_eq in range(len(nr_eq_p_type)):
                    if new_eq == nr_eq_p_type[ind_eq]:
                        eqs_repeat=1
                        break
                if eqs_repeat==0:
                    nr_eq_p_type.append( new_eq )
                    nr_eq_p_type_quant.append( [new_eq, new_eq_len] )
                    nr_sols *= new_eq_len


    nv_ve_combi_init = nr_sols



    # FEASABILITY:
    ves_types_feas=[]
    ves_types_feas_quant=[]
    eqs_types_feas=[]
    eqs_types_feas_quant=[]
    sols_feasability_p_seq = []
    for ind_seq in range(len(log_phase.op_ve)):

       sols_feasability_p_seq.append(len(log_phase.op_ve[ind_seq].ve_combination))

       for ind_combi in range(len(log_phase.op_ve[ind_seq].ve_combination)):

           for ind_ves_type in range(len(log_phase.op_ve[ind_seq].ve_combination[ind_combi]['vessel'])):
               new_vess = log_phase.op_ve[ind_seq].ve_combination[ind_combi]['vessel'][ind_ves_type][1].id
               new_vess_len = len(log_phase.op_ve[ind_seq].ve_combination[ind_combi]['vessel'][ind_ves_type][1].panda)
               vess_repeat=0
               for ind_vess in range(len(ves_types_feas)):
                    if new_vess == ves_types_feas[ind_vess]:
                        vess_repeat=1
                        break
               if vess_repeat==0:
                   ves_types_feas.append( new_vess )
                   ves_types_feas_quant.append( [new_vess, new_vess_len])


           for ind_eq_type in range(len(log_phase.op_ve[ind_seq].ve_combination[ind_combi]['equipment'])):
               new_eq = log_phase.op_ve[ind_seq].ve_combination[ind_combi]['equipment'][ind_eq_type][1].id
               new_eq_len = len(log_phase.op_ve[ind_seq].ve_combination[ind_combi]['equipment'][ind_eq_type][1].panda)
               eqs_repeat=0
               for ind_eq in range(len(eqs_types_feas)):
                    if new_eq == eqs_types_feas[ind_eq]:
                        eqs_repeat=1
                        break
               if eqs_repeat==0:
                   eqs_types_feas.append( new_eq )
                   eqs_types_feas_quant.append( [new_eq, new_eq_len] )



    # MATCHING:
    ves_types=[]
    eqs_types=[]
    vess_all=[]
    eqs_all=[]
    sols_matching_p_seq = []
    for ind_seq in range(len(log_phase.op_ve)):
        if len(module['combi_select'][ind_seq]) == 0: # a strategy with no solutions!
            continue

        sols_matching_p_seq.append(len(module['combi_select'][ind_seq]))

        for ind_sol in range(len(module['combi_select'][ind_seq])):
           for ind_vess_type_sol in range(len(module['combi_select'][ind_seq][ind_sol]['VEs'])):
               # vessel:
               new_vess = module['combi_select'][ind_seq][ind_sol]['VEs'][ind_vess_type_sol][0]
               # check if repeted vessel
               vess_repeat=0
               for ind_vess in range(len(ves_types)):
                   if new_vess == ves_types[ind_vess]:
                       vess_repeat=1
                       vess_all.append( [new_vess,
                                         module['combi_select'][ind_seq][ind_sol]['VEs'][ind_vess_type_sol][2].name] )
                       break
               if vess_repeat==0:
                   ves_types.append( new_vess )
                   vess_all.append( [new_vess,
                                         module['combi_select'][ind_seq][ind_sol]['VEs'][ind_vess_type_sol][2].name] )

               # equipment:
               if len(module['combi_select'][ind_seq][ind_sol]['VEs'][ind_vess_type_sol])>3:
                   nr_equip = len(module['combi_select'][ind_seq][ind_sol]['VEs'][ind_vess_type_sol]) - 3
                   for ind_eqs_in_vess in range(nr_equip):
                       new_equip = module['combi_select'][ind_seq][ind_sol]['VEs'][ind_vess_type_sol][3+ind_eqs_in_vess][0]
                       # check if repeted vessel
                       eqs_repeat=0
                       for ind_eqs in range(len(eqs_types)):
                           if new_equip == eqs_types[ind_eqs]:
                               eqs_repeat=1
                               eqs_all.append( [new_equip,
                                               module['combi_select'][ind_seq][ind_sol]['VEs'][ind_vess_type_sol][3+ind_eqs_in_vess][2].name] )
                               break
                       if eqs_repeat==0:
                           eqs_types.append( new_equip )
                           eqs_all.append( [new_equip,
                               module['combi_select'][ind_seq][ind_sol]['VEs'][ind_vess_type_sol][3+ind_eqs_in_vess][2].name] )
    sols_matching = sum(sols_matching_p_seq)

    # SOLUTIONS:
    sol_in_seq=[]
    sols_all=[]
    for ind_seq in range(len(log_phase.op_ve)):
        sol_in_seq.append( len(log_phase.op_ve[ind_seq].sol) )
        sols_all.append( log_phase.op_ve[ind_seq].sol )

    # VESSELS!!
    # inicializar dicionario com vessel type usados
    ves_types_match = {}
    for ind_ves_type in range(len(ves_types)):
        ves_types_match[ves_types[ind_ves_type]] = {}

    # contabilizar por index...........
    for ind_vess_all in range(len(vess_all)):
       ves_type_i = vess_all[ind_vess_all][0]
       ves_index_i = vess_all[ind_vess_all][1]
       if ves_index_i in ves_types_match[ves_type_i]:
           ves_types_match[ves_type_i][ves_index_i] += 1
       else:
           ves_types_match[ves_type_i].update( { ves_index_i: 1} )

    ves_types_match_quant= []
    for ind_vess_match in range(len(ves_types)):
       ves_types_match_quant.append( [ ves_types[ind_vess_match], len(ves_types_match[ves_types[ind_vess_match]]) ] )


    # EQUIPMENTS!!
    # inicializar dicionario com vessel type usados
    eqs_types_match = {}
    for ind_eqs_type in range(len(eqs_types)):
        eqs_types_match[eqs_types[ind_eqs_type]] = {}

    # contabilizar por index...........
    for ind_eqs_all in range(len(eqs_all)):
       eqs_type_i = eqs_all[ind_eqs_all][0]
       eqs_index_i = eqs_all[ind_eqs_all][1]
       if eqs_index_i in eqs_types_match[eqs_type_i]:
           eqs_types_match[eqs_type_i][eqs_index_i] += 1
       else:
           eqs_types_match[eqs_type_i].update( { eqs_index_i: 1} )

    eqs_types_match_quant= []
    for ind_eqs_match in range(len(eqs_types)):
       eqs_types_match_quant.append( [ eqs_types[ind_eqs_match], len(eqs_types_match[eqs_types[ind_eqs_match]]) ] )


    # SOLUTION:
    VE_sol = module['optimal']['vessel_equipment']
    # Vessels:
    Vess_in_sol=[]
    Vess_sol_output = []
    Vess_length = []
    Vess_quantity = []
    # Equipments:
    Eqs_in_sol=[]
    Eqs_sol_output = []
    for ind_vess_sol in range(len(VE_sol)):
       Vess_in_sol.append( VE_sol[ind_vess_sol][0] )
       Vess_type =  VE_sol[ind_vess_sol][0]
       Vess_quant = VE_sol[ind_vess_sol][1]
       Vess_id = VE_sol[ind_vess_sol][2].name
       Vess_sol_output.append( [Vess_quant, Vess_type, Vess_id] )
       Vess_length.append ( VE_sol[ind_vess_sol][2]['Length [m]'] )
       Vess_quantity.append( Vess_quant )
       if len(VE_sol[ind_vess_sol])>3:
           nr_equip = len(VE_sol[ind_vess_sol]) - 3
           for ind_eqs_in_vess in range(nr_equip):
                Eqs_in_sol.append( VE_sol[ind_vess_sol][3+ind_eqs_in_vess][0] )
                Eqs_type = VE_sol[ind_vess_sol][3+ind_eqs_in_vess][0]
                Eqs_quant = VE_sol[ind_vess_sol][3+ind_eqs_in_vess][1]
                Eqs_id = VE_sol[ind_vess_sol][3+ind_eqs_in_vess][2].name
                Eqs_sol_output.append( [Eqs_quant, Eqs_type, Eqs_id] )




    OUTPUT_dict =  {
                    'SELECTION': {
                        'Number Initial Solutions': nv_ve_combi_init,
                        'Solutions after Feasibility & Requirements': {
                            'Number Solutions': log_phase.nr_sol_feas,
                            # 'Vesssel Requirements': module['requirement'][1], # remove?
                            'Vesssel Requirements': module['requirement'][5]},
                            # 'Equipments Requirements': module['requirement'][0]} , # remove?
                        'Solutions after Matching':
                            # 'Number Solutions':
                            log_phase.nr_sol_match
                            # 'Vesssel-Equipment Requirements': module['requirement'][4], # remove?
                            #  'Vessel-Port Requirements': module['requirement'][2]} , # remove?
                    },

                    'VESSELS & EQUIPMENTS': {
                            'Vessels quantity/type/databaseID [-]': Vess_sol_output,
                            'Equipments quantity/type/databaseID [-]': Eqs_sol_output
                    },

                    'LOGISTICS': {
                        # 'Operation Name': log_phase.description, # incluir??!?!?
                        'Sea operations': module['optimal']['logistic operations']['sea'],
                        'Strategy Name': module['optimal']['strategy'],
                        'Number of Journeys': module['optimal']['numb of journeys'],
                        'Elements per Journey': module['optimal']['elems per journey'],
                                },

                    'DATE': {'Start Date': module['optimal']['start_dt'],
                            'Depart Date': module['optimal']['depart_dt'],
                            'End Date': module['optimal']['end_dt']},

                    'TIME': {'Preparation Time [h]': module['optimal']['schedule prep time'],
                             'Waiting Time [h]': module['optimal']['schedule waiting time'],
                             'Sea Transit Time [h]': module['optimal']['schedule sea transit time'],
                             'Sea Operation Time [h]': module['optimal']['schedule sea operation time'],
                             # 'Sea Time [h]': module['optimal']['schedule sea time'],
                             'Total Time [h]': module['optimal']['schedule total time']
                             },

                    'COST': {'Vessel Cost [EUR]': module['optimal']['vessel cost'],
                            'Equipment Cost [EUR]': module['optimal']['equipment cost'],
                            'Port Cost [EUR]': module['optimal']['port cost'],
                            'Fuel Cost [EUR]': module['optimal']['fuel cost'],
                            'Total Cost [EUR]': module['optimal']['total cost']}


                    ,'WARNING': {}
    }


    OUTPUT_extra = {
                    'logistic_phase_description': log_phase.description,

                    'initial': {
                                    'ves_types_init': nr_ves_p_type_quant,
                                    'eq_types_init': nr_eq_p_type_quant

                    },

                    'feasibility':{
                                    'ves_req': {'deck area': module['requirement'][5]['deck area'],
                                                'deck cargo': module['requirement'][5]['deck cargo'],
                                                'deck loading': module['requirement'][5]['deck loading'],
                                                'crane capacity': module['requirement'][5]['deck cargo']
                                                },

                                    'ves_req_feas': module['requirement'][1],
                                    'eq_req_feas': module['requirement'][0],

                                    'ves_types_feas': ves_types_feas_quant,
                                    'eq_types_feas': eqs_types_feas_quant
                    },

                    'matching': { 'port_ves_req': module['requirement'][2],
                                  'ves_eq_req': module['requirement'][4],

                                  'ves_types_match': ves_types_match_quant,
                                  'eq_types_match': eqs_types_match_quant
                    },

                    'sol': sols_all,
                    'nb_strat': seq_descrip,
                    'nb_task': op_in_seq_total,

                    'all_sol': {'sched_all': module['schedule'],
                             'cost_all': module['cost'],

                             'risk_all': module['risk'],
                             'env_all': module['envir']},

                    'PORT': module['port'],
                    'MEAN_VESSEL_LENGTH': np.mean(Vess_length),
                    'NUMBR_VESSEL': np.sum(Vess_quantity)
    }

    return OUTPUT_dict, OUTPUT_extra