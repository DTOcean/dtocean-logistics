from .classes import DefPhase, LogPhase


def initialize_LpM5_phase(log_op, vessels, equipments, om):

    # save outputs required inside short named variables
    # initialize logistic phase
    phase = LogPhase(920, "On-site maintenance on power cables")
    ''' On-site maintenance on power cables strategy '''

    # initialize strategy
    phase.op_ve[0] = DefPhase(0, 'On-site maintenance on power cables')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['CLV'])],
                                        'equipment': [ (1, equipments['rov'], 0)]}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                  log_op["VessPrep"]]
    # define sea operations
    for index, row in om.iterrows():
        om_id = om['ID [-]'].ix[index]
        if om_id == 'MoS7' or om_id == 'MoS8':
            phase.op_ve[0].op_seq_sea[index] = [log_op["TranPortSite"],
                                                log_op["VesPos"],

                                                log_op["Access"],
                                                log_op["Maintenance"],

                                                log_op["TranSiteSite"],
                                                log_op["TranSitePort"]]

    # define final demobilization tasks
    phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    return phase
