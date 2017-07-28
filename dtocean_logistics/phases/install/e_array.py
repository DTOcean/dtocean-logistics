"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org, pedro.vicente@wavec.org

e_array.py contains the functions to initiallize the logistic phase: "array cable 
installation". This consists of:
    (1) Compute the number of protection elements required (split pipes)
    (2) Defining Vessels and Equipment combinations capable to carry out the logistic activities
    (3) Defining the list of operations required to conduct out the logistic activities

Parameters
----------
vessels (DataFrame): Panda table containing the vessel database

equipments (DataFrame): Panda table containing the equipment database

ports (DataFrame): Panda table containing the ports database

static_cable (DataFrame): Panda table containing the static cables database

cable_route (DataFrame): Panda table containing the cable route database

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

import logging

from ...ancillaries.dist import distance
from .classes import DefPhase, LogPhase
from .shared import get_burial_equip

# Start logging
module_logger = logging.getLogger(__name__)


def init_e_array_phase(log_op, vessels, equipments, static_cable,
                       cable_route, collection_point):

    phase = {}
    if len(static_cable)>0:
        # save outputs required inside short named variables
        static_db = static_cable
        array_db = static_db[static_db['type [-]'] == 'array']
        array_index = array_db.index.values

        trench_type_all = array_db['trench type [-]']
        trench_type = array_db['trench type [-]'].iloc[0]
        
        route_db = cable_route
        array_route = route_db[route_db['static cable id [-]'].isin(array_index)]

        cp_db = collection_point
        pipe_db = equipments['split pipe'].panda

        # compute the number of split pipes required
        number_pipes = [0]

        for index, row in array_db.iterrows():
            index_route_db = array_route[array_route['static cable id [-]'] == index]

            for a in range(len(index_route_db.index)-1):
                if index_route_db['split pipe [-]'].iloc[a] == 'yes':

                    UTM_ini = [ index_route_db['x coord [m]'].iloc[a],
                                index_route_db['y coord [m]'].iloc[a],
                                index_route_db['zone [-]'].iloc[a] ]

                    UTM_fin = [ index_route_db['x coord [m]'].iloc[a+1],
                                index_route_db['y coord [m]'].iloc[a+1],
                                index_route_db['zone [-]'].iloc[a+1] ]

                    dist = distance(UTM_ini, UTM_fin)*1000.0 # obtain the distance in meters

                    pipe_length = max(pipe_db['Unit length [mm]'])/1000.0 # obtain the length of the pipes in meters

                    number_pipes.append( int(dist/pipe_length) )

        number_pipes = sum(number_pipes)

        # initialize logistic phase
        phase = LogPhase(102, "Installation of static array cables")

        ''' Static Array Cable Installation Strategy '''
#
#        if (trench_type_all == trench_type).all():
#            pass
#        else:
#            msg = ("Trenching types should be the same for all export cables.")
#            module_logger.warning(msg)

        # create as many strategys as possible trenching types
        for a in range(len(trench_type)):

            technique = trench_type[a]
            burial_equip = get_burial_equip(technique)

            # initialize strategy
            phase.op_ve[a] = DefPhase(1, 'Static Array Cable Installation Strategy: %s' % trench_type[a])

            # define vessel and equipment combinations suited for this strategy
            if technique == 'no burial'  or (array_route['burial depth [m]'] == 0).all() or array_route['burial depth [m]'].isnull().all():
                phase.op_ve[a].ve_combination[0] = {'vessel': [(1, vessels['CLV']),
                                                               (2, vessels['Multicat'])],

                                                    'equipment': [(number_pipes, equipments['split pipe'], 0),
                                                                  (1, equipments['rov'], 0)] }

                phase.op_ve[a].ve_combination[1] = {'vessel': [(1, vessels['CLB']),
                                                               (1, vessels['Tugboat']),
                                                               (2, vessels['Multicat'])],

                                                    'equipment': [(number_pipes, equipments['split pipe'], 0),
                                                                  (1, equipments['rov'], 0)] }

            else:
                phase.op_ve[a].ve_combination[0] = {'vessel': [(1, vessels['CLV']),
                                                               (2, vessels['Multicat'])],

                                                    'equipment': [(1, equipments[burial_equip], 0),
                                                                  (number_pipes, equipments['split pipe'], 0),
                                                                  (1, equipments['rov'], 0)] }

                phase.op_ve[a].ve_combination[1] = {'vessel': [(1, vessels['CLB']),
                                                               (1, vessels['Tugboat']),
                                                               (2, vessels['Multicat'])],

                                                    'equipment': [(1, equipments[burial_equip], 0),
                                                                  (number_pipes, equipments['split pipe'], 0),
                                                                  (1, equipments['rov'], 0)] }

            # define initial mobilization and onshore preparation tasks
            phase.op_ve[a].op_seq_prep = [ log_op["Mob"],
                                           log_op["AssPort"],
                                           log_op["LoadCableFactory"] ]

            # iterate over the list of elements to be installed.
            # each element is associated with a customized operation sequence depending on it's characteristics.
            for index, row in array_db.iterrows():

                # define sea operations
                phase.op_ve[a].op_seq_sea[index] = [ log_op["VesPosCables"] ]

                # condition check to obtain suitable operation sequence for the downstream termination
                if array_db['downstream termination type [-]'].ix[index] == 'device':

                  if array_db['downstream ei type [-]'].ix[index] == 'dry-mate' or \
                     array_db['downstream ei type [-]'].ix[index] == 'wet-mate':
                      phase.op_ve[a].op_seq_sea[index].extend([ log_op["Lower_Cable_Seabed"] ])

                  elif array_db['upstream ei type [-]'].ix[index] == 'j-tube':
                      phase.op_ve[a].op_seq_sea[index].extend([ log_op["Jtube_Connect"] ])

                  else:
                      msg = ("Error in array cable {}: "
                             "Downstream electrical interface type not "
                             "recognized or doesnt match with termination "
                             "type".format(index))

                      module_logger.warning(msg)

                elif array_db['downstream termination type [-]'].ix[index] == 'collection point':

                    cp_id = array_db['downstream termination id [-]'].ix[index]

                    if cp_db['type [-]'].ix[cp_id] == 'seabed' or \
                       cp_db['type [-]'].ix[cp_id] == 'seabed with pigtails':

                        if array_db['downstream ei type [-]'].ix[index] == 'dry-mate':
                            phase.op_ve[a].op_seq_sea[index].extend([ log_op["Lower_Cable_Seabed"] ])

                        elif array_db['downstream ei type [-]'].ix[index] == 'wet-mate':
                            phase.op_ve[a].op_seq_sea[index].extend([ log_op["Wet_Connect"] ])

                        else:
                            msg = ("Error in array cable: Collection point "
                                   "index {} upstream electrical interface "
                                   "type is not recognized or doesnt match "
                                   "with termination type".format(cp_id))
                            module_logger.warning(msg)

                    elif cp_db['type [-]'].ix[cp_id] == 'surface piercing':
                        phase.op_ve[a].op_seq_sea[index].extend([ log_op["Jtube_Connect"] ])

                    else:
                        msg = ("Error in array cable: Collection point {} type"
                               " is not recognized".format(cp_id))
                        module_logger.warning(msg)

                else:
                    msg = ("Error in array cable {}: Upstream termination "
                           "type is not valid".format(index))
                    module_logger.warning(msg)

                # include cable route laying operation between terminations
                index_route_db = array_route[array_route['static cable id [-]'] == index]

                trenching = 0 # variable stating trenching status, 0 == not trenching / 1 = trenching
                for index1, row in index_route_db.iterrows():

                    if index_route_db['burial depth [m]'].ix[index1] == 0 and \
                       index_route_db['split pipe [-]'].ix[index1] == 'no':

                       if trenching == 0:
                           phase.op_ve[a].op_seq_sea[index].extend([ log_op["CableLay_Route"] ])

                       elif trenching == 1:
                           phase.op_ve[a].op_seq_sea[index].extend([ log_op["BurialToolRecov"],
                                                                     log_op["CableLay_Route"] ])
                           trenching = 0

                    elif index_route_db['burial depth [m]'].ix[index1] == 0 and \
                         index_route_db['split pipe [-]'].ix[index1] == 'yes':

                           if trenching == 0:
                               phase.op_ve[a].op_seq_sea[index].extend([ log_op["CableLay_SplitPipe"] ])

                           elif trenching == 1:
                               phase.op_ve[a].op_seq_sea[index].extend([ log_op["BurialToolRecov"],
                                                                         log_op["CableLay_SplitPipe"] ])
                               trenching = 0

                    elif index_route_db['burial depth [m]'].ix[index1] != 0:

                         if trenching == 0:
                             phase.op_ve[a].op_seq_sea[index].extend([ log_op["BurialToolDeploy"],
                                                                       log_op["CableLay_Burial"] ])
                             trenching = 1

                         elif trenching == 1:
                             phase.op_ve[a].op_seq_sea[index].extend([ log_op["CableLay_Burial"] ])

                # condition check to obtain suitable operation sequence for the upstream termination
                if array_db['upstream termination type [-]'].ix[index] == 'device':

                  if array_db['upstream ei type [-]'].ix[index] == 'dry-mate' or \
                     array_db['upstream ei type [-]'].ix[index] == 'wet-mate':
                      phase.op_ve[a].op_seq_sea[index].extend([ log_op["Lower_Cable_Seabed"] ])

                  elif array_db['upstream ei type [-]'].ix[index] == 'j-tube':
                      phase.op_ve[a].op_seq_sea[index].extend([ log_op["Jtube_Connect"] ])

                  else:
                      msg = ("Error in array cable {}: "
                             "Downstream electrical interface type not "
                             "recognized or doesnt match with termination "
                             "type".format(index))

                      module_logger.warning(msg)

                elif array_db['upstream termination type [-]'].ix[index] == 'collection point':

                    cp_id = array_db['upstream termination id [-]'].ix[index]

                    if array_db['upstream ei type [-]'].ix[index] == 'hard-wired':
                        phase.op_ve[a].op_seq_sea[index].extend([ log_op["Lower_CP_Seabed"] ])

                    elif array_db['upstream ei type [-]'].ix[index] == 'dry-mate' or \
                         array_db['upstream ei type [-]'].ix[index] == 'wet-mate' or \
                         array_db['upstream ei type [-]'].ix[index] == 'j-tube':

                        if cp_db['type [-]'].ix[cp_id] == 'seabed' or \
                           cp_db['type [-]'].ix[cp_id] == 'seabed with pigtails':

                            if array_db['upstream ei type [-]'].ix[index] == 'dry-mate':
                                phase.op_ve[a].op_seq_sea[index].extend([ log_op["Lower_Cable_Seabed"] ])

                            elif array_db['upstream ei type [-]'].ix[index] == 'wet-mate':
                                phase.op_ve[a].op_seq_sea[index].extend([ log_op["Wet_Connect"] ])

                        elif cp_db['type [-]'].ix[cp_id] == 'surface piercing':
                            phase.op_ve[a].op_seq_sea[index].extend([ log_op["Jtube_Connect"] ])

                        else:
                            msg = ("Error in array cable: Collection point "
                                   "index {} downstream electrical interface "
                                   "type is not recognized.".format(cp_id))
                            module_logger.warning(msg)

                    else:
                        msg = ("Error in array cable {}: "
                               "Upstream electrical interface type not "
                               "recognized.".format(index))

                        module_logger.warning(msg)

                phase.op_ve[a].op_seq_sea[index].extend([ log_op["TranSiteSite"] ])
            # define final demobilization tasks
            phase.op_ve[a].op_seq_demob = [log_op["Demob"]]

    return phase

