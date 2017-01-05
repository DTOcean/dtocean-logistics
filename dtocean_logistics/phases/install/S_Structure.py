from .classes import DefPhase, LogPhase


def init_support_phase(log_op, vessels, equipments, device, sub_device,
                       layout):

    phase = {}
    if len(layout) > 0:
        # save outputs required inside short named variables
        support_db = layout

        # initialize logistic phase
        phase = LogPhase(112, "Installation of support structure")

            # initialize strategy (all strategies will be individually assessed by the
        # performance functions, with the lowest costs on being choosen)
        phase.op_ve[0] = DefPhase(0, 'Support Structure Installation')

        # define vessel and equipment combinations suited for this strategy
        phase.op_ve[0].ve_combination[0] = {'vessel': [ (1, vessels['Crane Vessel']), (1, vessels['Multicat']) ],
                                            'equipment': [ (1, equipments['rov'], 0) ]}
                                            
        phase.op_ve[0].ve_combination[1] = {'vessel': [ (1, vessels['Crane Barge']), (1, vessels['Tugboat']), (1, vessels['Multicat'])],
                                            'equipment': [ (1, equipments['rov'], 0) ]}

        phase.op_ve[0].ve_combination[2] = {'vessel': [ (1, vessels['JUP Vessel']), (1, vessels['Multicat']) ],
                                            'equipment': [ (1, equipments['rov'], 0) ]}
    
        phase.op_ve[0].ve_combination[3] = {'vessel': [ (1, vessels['JUP Barge']), (1, vessels['Tugboat']), (1, vessels['Multicat']) ],
                                            'equipment': [ (1, equipments['rov'], 0) ]}
                                            
        phase.op_ve[0].ve_combination[4] = {'vessel': [ (1, vessels['CSV']), (1, vessels['Multicat']) ],
                                            'equipment': [ (1, equipments['rov'], 0) ]}

        # define initial mobilization and onshore preparation tasks
        phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                      log_op["AssPort"],
                                      log_op["VessPrep_support"]]


        # iterate over the list of elements to be installed.
        # each element is associated with a customized operation sequence depending on it's characteristics,
        for index, row in support_db.iterrows():

            # initialize an empty operation sequence list for the 'index' element
            phase.op_ve[0].op_seq_sea[index] = []
            
            # initialize an empty operation sequence list for the 'index' element
            phase.op_ve[0].op_seq_sea[index].extend([ log_op["VesPos"],
                                                      log_op["SuppStrutPos"],
                                                      log_op["TranSiteSite"] ])
    
        # define final demobilization tasks
        phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    return phase
