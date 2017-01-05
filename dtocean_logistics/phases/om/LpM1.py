from .classes import DefPhase, LogPhase


def initialize_LpM1_phase(log_op, vessels, equipments, om):

    # save outputs required inside short named variables

    # initialize logistic phase
    phase = LogPhase(920, "Inspection or on-site maintenance of topside elements")

    ''' Inspection or On-site maintenance strategy'''

    # initialize strategy
    phase.op_ve[0] = DefPhase(0, 'Inspection / On-site maintenance')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['Multicat'])],
                                        'equipment': []}

    phase.op_ve[0].ve_combination[1] = {'vessel': [(1, vessels['CTV'])],
                                        'equipment': []}

    if 'yes' in om['helideck [-]'].values:  # include helicopter if helipad is available

        phase.op_ve[0].ve_combination[2] = {'vessel': [(1, vessels['Helicopter'])],
                                            'equipment': []}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                  log_op["VessPrep"]]

    # define sea operations
    for index, row in om.iterrows():

        om_id = om['ID [-]'].ix[index]

        if om_id == 'Insp1' or om_id == 'MoS1' or om_id == 'Insp2' or om_id == 'MoS2':

            phase.op_ve[0].op_seq_sea[index] = [log_op["TranPortSite"],
                                                log_op["VesPos"],

                                                log_op["Access"],
                                                log_op["Maintenance"],

                                                log_op["TranSiteSite"],
                                                log_op["TranSitePort"]]

    # define final demobilization tasks
    phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    return phase
