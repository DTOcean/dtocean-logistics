from .classes import DefPhase, LogPhase


def initialize_LpM7_phase(log_op, vessels, equipments, om):

    # obtain first maintenance id from om
    df_index = om.index.values
    om_id = om['ID [-]'].ix[df_index[0]]

    # initialize logistic phase
    phase = LogPhase(920, "Onshore maintenance of devices or array sub-component - tow transport")

    if om_id == 'RtP3':
        ''' Retrieval from surface including lifting - maintenance strategy '''

        # initialize strategy
        phase.op_ve[0] = DefPhase(0, 'Retrieval from surface including lifting')

        # define vessel and equipment combinations suited for this strategy
        phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['Multicat'])],
                                            'equipment': []}

        phase.op_ve[0].ve_combination[1] = {'vessel': [(1, vessels['AHTS'])],
                                            'equipment': []}

        # define initial mobilization and onshore preparation tasks
        phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                      log_op["VessPrep"]]

        # define sea operations
        for index, row in om.iterrows():
            phase.op_ve[0].op_seq_sea[index] = [log_op["TranPortSite"],
                                                log_op["VesPos"],

                                                log_op["Access"],
                                                log_op["TranSitePort"],

                                                log_op["Maintenance"],

                                                log_op["TranPortSite"],
                                                log_op["VesPos"],

                                                log_op["Access"],
                                                log_op["TranSitePort"]]
       
        # define final demobilization tasks
        phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    if om_id == 'RtP4':
        ''' Retrieval from bottom including lifting and subsea operations - maintenance strategy '''

        # initialize strategy
        phase.op_ve[0] = DefPhase(0, 'Retrieval from bottom including lifting and subsea operations')
    
        # define vessel and equipment combinations suited for this strategy
        phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['Multicat'])],
                                            'equipment': [(1, equipments['rov'], 0)]}

        phase.op_ve[0].ve_combination[1] = {'vessel': [(1, vessels['AHTS'])],
                                            'equipment': [(1, equipments['rov'], 0)]}

        # define initial mobilization and onshore preparation tasks
        phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                      log_op["VessPrep"]]
    
        # define sea operations
        for index, row in om.iterrows():
            phase.op_ve[0].op_seq_sea[index] = [log_op["TranPortSite"],
                                                log_op["VesPos"],

                                                log_op["Access"],
                                                log_op["TranSitePort"],

                                                log_op["Maintenance"],

                                                log_op["TranPortSite"],
                                                log_op["VesPos"],

                                                log_op["Access"],
                                                log_op["TranSitePort"]]

        # define final demobilization tasks
        phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    return phase
