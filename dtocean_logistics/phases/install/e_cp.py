"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org, pedro.vicente@wavec.org

e_cp.py contains the functions to initiallize the logistic phase: "collection point 
installation". This consists of:
    (1) Defining Vessels and Equipment combinations capable to carry out the logistic activities
    (2) Defining the list of operations required to conduct out the logistic activities

Parameters
----------
vessels (DataFrame): Panda table containing the vessel database

equipments (DataFrame): Panda table containing the equipment database

collection_point (DataFrame): Panda table containing the collection points database


Returns
-------

phase (class): contains the initialized characteristics of the logistic phase

See also: ...

                       DTOcean project
                    http://www.dtocean.eu

                   WavEC Offshore Renewables
                    http://www.wavec.org/en

"""

from .classes import DefPhase, LogPhase

def init_e_cp_seabed_phase(log_op, vessels, equipments, collection_point):

    phase ={}
    if len(collection_point)>0:
        # save outputs required inside short named variables
        cp_db = collection_point
        cp_db = cp_db[cp_db['type [-]'] != 'surface piercing']
        cp_db = cp_db[cp_db['downstream ei type [-]'] != 'hard-wired cable']

        # initialize logistic phase
        phase = LogPhase(102, "Installation of collection point (seabed)")

        # initialize strategy (all strategies will be individually assessed by the
        # performance functions, with the lowest costs on being choosen)
        phase.op_ve[0] = DefPhase(1, 'Installation of seabed collection points')

        # define vessel and equipment combinations suited for this strategy
        phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['Crane Vessel']), (1, vessels['Multicat'])],
                                            'equipment': [(1, equipments['rov'], 0)]}

        phase.op_ve[0].ve_combination[1] = {'vessel': [(1, vessels['Crane Barge']), (1, vessels['Tugboat']), (1, vessels['Multicat'])],
                                            'equipment': [(1, equipments['rov'], 0)]}

        phase.op_ve[0].ve_combination[2] = {'vessel': [(1, vessels['JUP Vessel']), (1, vessels['Multicat'])],
                                            'equipment': [(1, equipments['rov'], 0)]}

        phase.op_ve[0].ve_combination[3] = {'vessel': [(1, vessels['JUP Barge']), (1, vessels['Tugboat']), (1, vessels['Multicat'])],
                                            'equipment': [(1, equipments['rov'], 0)]}

        phase.op_ve[0].ve_combination[4] = {'vessel': [(1, vessels['CSV']), (1, vessels['Multicat'])],
                                            'equipment': [(1, equipments['rov'], 0)]}

        # define initial mobilization and onshore preparation tasks
        phase.op_ve[0].op_seq_prep = [ log_op["Mob"],
                                       log_op["AssPort"],
                                       log_op["VessPrep"] ]

        # loop over the 'index' elements to install
        for index, row in cp_db.iterrows():

            # define sea operations
            phase.op_ve[0].op_seq_sea[index] = [ log_op["VesPos"] ]

            # check the collection point type
            if cp_db['type [-]'].ix[index] == 'seabed':

                # checks for the need to lift laid cables
                if any(x in 'dry-mate' for x in cp_db['upstream ei type [-]'].ix[index]):
                    for x in range(cp_db['upstream ei type [-]'].ix[index].count('dry-mate')): #counts how may 'dry-mate' types exist and loops over the number
                        phase.op_ve[0].op_seq_sea[index].extend([ log_op["Lift_Cable_Seabed"] ])

                if any(x in 'dry-mate' for x in cp_db['downstream ei type [-]'].ix[index]):
                    for x in range(cp_db['downstream ei type [-]'].ix[index].count('dry-mate')): #counts how may 'dry-mate' types exist and loops over the number
                        phase.op_ve[0].op_seq_sea[index].extend([ log_op["Lift_Cable_Seabed"] ])

                # checks for the need to perform onboard dry-mate connections
                if any(x in 'dry-mate' for x in cp_db['upstream ei type [-]'].ix[index]) or \
                   any(x in 'dry-mate' for x in cp_db['downstream ei type [-]'].ix[index]):
                    phase.op_ve[0].op_seq_sea[index].extend([ log_op["Dry_Connect"],
                                                              log_op["Lower_CP_Seabed"] ])

                # if all electrical interfaces are wet-mate just lower the cp
                elif all(x in 'wet-mate' for x in cp_db['upstream ei type [-]'].ix[index]) and \
                     all(x in 'wet-mate' for x in cp_db['downstream ei type [-]'].ix[index]):
                     phase.op_ve[0].op_seq_sea[index].extend([ log_op["Lower_CP_Seabed"] ])

                phase.op_ve[0].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])

            if cp_db['type [-]'].ix[index] == 'seabed with pigtails':

                # checks for the need to lift laid cables
                if any(x in 'dry-mate' for x in cp_db['downstream ei type [-]'].ix[index]):
                    for x in range(cp_db['downstream ei type [-]'].ix[index].count('dry-mate')): #counts how may 'dry-mate' types exist and loops over the number
                        phase.op_ve[0].op_seq_sea[index].extend([ log_op["Lift_Cable_Seabed"] ])

                    phase.op_ve[0].op_seq_sea[index].extend([ log_op["Dry_Connect"],
                                                              log_op["Lower_CP_Seabed"] ])

                # if all electrical interfaces are wet-mate just lower the cp
                elif all(x in 'wet-mate' for x in cp_db['downstream ei type [-]'].ix[index]):
                      phase.op_ve[0].op_seq_sea[index].extend([ log_op["Lower_CP_Seabed"]] )

                phase.op_ve[0].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])

        # define final demobilization tasks
        phase.op_ve[0].op_seq_demob = [ log_op["Demob"] ]

    return phase


def init_e_cp_surface_phase(log_op, vessels, equipments, collection_point):
    
    phase ={}
    if len(collection_point)>0:
        # save outputs required inside short named variables
        cp_db = collection_point
        cp_db = cp_db[cp_db['type [-]'] == 'surface piercing']

        # initialize logistic phase
        phase = LogPhase(103, "Installation of collection point (surface piercing)")

        # initialize strategy (all strategies will be individually assessed by the
        # performance functions, with the lowest costs on being choosen)
        phase.op_ve[0] = DefPhase(1, 'Installation of surface piercing collection points')

        # define vessel and equipment combinations suited for this strategy
        phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['Crane Vessel']), (1, vessels['Multicat'])],
                                            'equipment': [(1, equipments['rov'], 0)]}

        phase.op_ve[0].ve_combination[1] = {'vessel': [(1, vessels['Crane Barge']), (1, vessels['Tugboat']), (1, vessels['Multicat'])],
                                            'equipment': [(1, equipments['rov'], 0)]}

        phase.op_ve[0].ve_combination[2] = {'vessel': [(1, vessels['JUP Vessel']), (1, vessels['Multicat'])],
                                            'equipment': [(1, equipments['rov'], 0)]}

        phase.op_ve[0].ve_combination[3] = {'vessel': [(1, vessels['JUP Barge']), (1, vessels['Tugboat']), (1, vessels['Multicat'])],
                                            'equipment': [(1, equipments['rov'], 0)]}

        phase.op_ve[0].ve_combination[4] = {'vessel': [(1, vessels['CSV']), (1, vessels['Multicat'])],
                                            'equipment': [(1, equipments['rov'], 0)]}

        # define initial mobilization and onshore preparation tasks
        phase.op_ve[0].op_seq_prep = [ log_op["Mob"],
                                       log_op["AssPort"],
                                       log_op["VessPrep_SurfaceCP"] ]

        # iterate over the list of elements to be installed.
        # each element is associated with a customized operation sequence depending on it's characteristics.
        for index, row in cp_db.iterrows():

            # define sea operations
            phase.op_ve[0].op_seq_sea[index] = [ log_op["VesPos"],

                                                 log_op["Lift_Topside"],
                                                 log_op["Connect_Topside"],

                                                 log_op["TranSiteSite"] ]

        # define final demobilization tasks
        phase.op_ve[0].op_seq_demob = [ log_op["Demob"] ]
    
    return phase