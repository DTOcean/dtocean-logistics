"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org, pedro.vicente@wavec.org

installation_main.py is the main file of the WP5 module within the suite of design tools
developped under the EU FP7 DTOcean project. installation_main.py provides an estimation of
the predicted performance of feasible maritime infrastructure solutions
that can carry out marine operations pertaining to the installation of
wave and tidal energy arrays.

installation_main.py can be described in five core sub-modules:
1- Initialising the logistic classes
2- Defining the installation plan
3- Selecting the installation port
4- Performing the assessment of all logistic phases sequencially, following
   six steps:
    (i) characterizartion of logistic requirements
    (ii) selection of the maritime infrastructure
    (iii) schedule assessment of the logistic phase
    (iv) cost assessment of the logistic phase
    (v) risk assessment of the logistic phase
    (vi) environmental impact assessment of the logistic phase

Parameters
----------
vessels(DataFrame): Panda table containing the vessel database

equipments (DataFrame): Panda table containing the equipment database

ports (DataFrame): Panda table containing the ports database

user_inputs (dict): dictionnary containing all required inputs to WP5 coming from WP1/end-user:
     'device' (Dataframe): inputs required from the device
     'metocean' (Dataframe): metocean data

hydrodynamic_outputs (dict): dictionnary containing all required inputs to WP5 coming from WP2
     'units' (DataFrame): number of devices
     'position' (DataFrame): UTM position of the devices

electrical_outputs (dict): dictionnary containing all required inputs to WP5 coming from WP3
     'layout' (DataFrame): to be specified

M&F_outputs (DataFrame): containing foundation data required for each device


Returns
-------

install (dict): dictionnary compiling all key results obtained from the assessment of the logistic phases for installation
    'plan' (dict): installation sequence of the required logistic phases
    'port' (DataFrame): port data related to the selected installation port
    'requirement' (tuple): minimum requirements returned from the feasibility functions
    'eq_select' (dict): list of equipments satisfying the minimum requirements
    've_select' (dict): list of vessels satisfying the minimum requirements
    'combi_select' (dict): list of solutions passing the compatibility check
    'schedule' (dict): list of parameters with data about time
    'cost'  (dict): vessel equiment and port cost
    'risk': to be defined
    'envir': to be defined
    'status': to be defined


Examples
--------
# >>> LOGISTICS()


See also: ...

                       DTOcean project
                    http://www.dtocean.eu

                   WavEC Offshore Renewables
                    http://www.wavec.org/en

"""


from os import path
import sys
sys.path.append('..')
import timeit
from datetime import timedelta
import warnings as wn
import numpy as np
import copy

from dtocean_logistics.load import load_phase_order_data, load_time_olc_data
from dtocean_logistics.load import load_eq_rates
from dtocean_logistics.load import load_sf

from dtocean_logistics.phases.operations import logOp_init
from dtocean_logistics.phases.install import logPhase_install_init
from dtocean_logistics.phases.install import planning
from dtocean_logistics.phases import select_port
from dtocean_logistics.feasibility.glob import glob_feas
from dtocean_logistics.selection.select_ve import select_e, select_v
from dtocean_logistics.selection.match import compatibility_ve
from dtocean_logistics.performance.schedule.schedule_ins import sched
from dtocean_logistics.performance.economic.eco import cost
from dtocean_logistics.performance.optim_sol import opt_sol
from dtocean_logistics.outputs.output_processing import out_process
from dtocean_logistics.outputs.output_plotting2 import out_ploting
from dtocean_logistics.outputs.output_plotting2 import out_ploting_installation
from dtocean_logistics.load.safe_factors import safety_factors
from dtocean_logistics.performance.economic.cost_year import cost_p_year


def installation_main( vessels_0, equipments_0, ports_0,
                     phase_order, schedule_OLC, penet_rates, laying_rates, other_rates, port_sf, vessel_sf, eq_sf,
                     site, metocean, device, sub_device,landfall, entry_point,
                     layout,
                     collection_point, dynamic_cable, static_cable, cable_route, connectors, external_protection, topology,
                     line, foundation,
                     PRINT_FLAG, PLOT_FLAG, PLOT_GANTT, PRINT_CSV, cvs_filename
                     ):


    # # Set directory paths for loading inputs (@Tecnalia)
    mod_path = path.dirname(path.realpath(__file__))

    def database_file(file):
        """
        shortcut function to load files from the database folder
        """
        fpath = path.join('databases', '{0}'.format(file))
        db_path = path.join(mod_path, fpath)
        return db_path


    if PRINT_CSV:

        import csv

        outputing = csv.writer(open(cvs_filename, "wb"), delimiter='\t')
        # outputing_txt = open("Outputs/Installation.txt", "w")

        OUTPUT_MTRX =  ['OPERATION',
            'Terminal area [m^2]', 'Terminal load bearing [t/m^2]',
            '# Port satisfying reqs',
            'Port countries',
            '# Countries',
            'Port for installation',
            'Distance port-site [km]',

            'Deck area req', 'deck cargo req', 'deck loading req','crane capacity req.',

            'Initial #ves avail.',
            'Initial #eqs avail.',

            '# of vessels Feasability',
            'Vessels type quant. Feasability',
            '# of equips Feasability',
            'Equips type quant. Feasability',

            '# of solutions Matching',
            '# of vessels Matching',
            'Vessels type quant. Matching',
            '# of equips Matching',
            'Equips type. Matching',

            '# Sols',
            '# of vessels Sol.',
            'Vessels Sol.',
            '# of equips Sol.',
            'Equips Sol.',

            'schedule waiting time [h]', 'schedule sea time [h]',
            'schedule prep time [h]', 'schedule total time [h]',

            'port cost [EURO]', 'vessel cost [EURO]',
            'equipment cost [EURO]', 'total cost [EURO]',

        ]

        outputing.writerow(OUTPUT_MTRX)
        # # Print also .txt:
        # for ind_txt in range(len(OUTPUT_MTRX)):
        #     outputing_txt.write("%s \t" % OUTPUT_MTRX[ind_txt])
        # outputing_txt.write("\n")

    # apply dafety factors in vessels parameters
    start_time_sf = timeit.default_timer()
    ports, vessels, equipments = safety_factors(ports_0, vessels_0, equipments_0, port_sf, vessel_sf, eq_sf)
    stop_time_sf = timeit.default_timer()
    # print 'Safety factors simulation time [s]: ' + str(stop_time_sf - start_time_sf) # DEBUG!


    vessels_ini = copy.deepcopy(vessels)
    equipments_ini = copy.deepcopy(equipments)


    """
     Initialise logistic operations and logistic phases
    """

    # logOp = logOp_init()
    start_time = timeit.default_timer()

    if PRINT_FLAG:
        print 'START!'
        print '\n'

    logOp = logOp_init(schedule_OLC)



    """
    Check the presence of the lease area entry point
    """
    if len(entry_point)==0: # if this data does not exit use first position of the site data
        entry_point['x coord [m]'] = site['x coord [m]'].iloc[0]
        entry_point['y coord [m]'] = site['y coord [m]'].iloc[0]
        entry_point['zone [-]'] = site['zone [-]'].iloc[0]
        entry_point['bathymetry [m]'] = site['bathymetry [m]'].iloc[0]
        entry_point['soil type [-]'] = site['soil type [-]'].iloc[0]


    """
    Determine the adequate installation logistic phase plan
    """
    install_plan = planning.install_plan(phase_order, device, layout,
                                         collection_point, dynamic_cable,
                                         static_cable, external_protection,
                                         line, foundation)


    """
    Select the most appropriate base installation port
    """
    start_time_port = timeit.default_timer()
    install_port = select_port.install_port(device, sub_device, site, entry_point, ports,
                                            line, foundation, collection_point,
                                            install_plan)
    stop_time_port = timeit.default_timer()
    if PRINT_FLAG:
        print 'PORT: '
        print 'Port Selected: ' + install_port['Selected base port for installation']['Name [-]']
        print 'Distance Port-Site [km]: ' + str(install_port['Distance port-site [km]'])


    # Incremental assessment of all logistic phase forming the the installation process
    install = {'plan': install_plan,
               'port': install_port,
               'requirement': {},
               'eq_select': {},
               've_select': {},
               'combi_select': {},
               'schedule': {},
               'cost': {},
               'risk': {},
               'envir': {},
               'end_dt': []
               # ,'sol': {}
               }

    Installation = {
                'PORT': {},
                'PLANNING': {},
                'COST': {},
                'DATE': {},
                'TIME': {},
                'ENVIRONMENTAL': {},
                'WARNING': {},
                'OPERATION': {}
                    }
    Installation['PLANNING'] = { 'List of Operations [-]':  []}
    logistic_phase_description = []

    mean_vess_length_ope = []
    numbr_vess_ope = []

    Installation_total_port_cost = 0
    Installation_total_vessel_cost = 0
    Installation_total_equip_cost = 0
    Installation_total_cost = 0
    Installation_total_wait_time = 0
    # Installation_total_sea_time = 0
    Installation_total_prep_time = 0
    Installation_total_time = 0
    Installation_total_sea_op_time = 0
    Installation_total_sea_trans_time = 0
    #  loop over the number of layers of the installation plan
    #if install['status'] == "pending":
    install['findSolution'] = 'SolutionFound'
    for x in install['plan']:
        for y in range(len(install['plan'][x])):

            if install['findSolution'] != 'SolutionFound':
                continue

            # Reload of databases
            del vessels, equipments
            vessels = copy.deepcopy(vessels_ini)
            equipments = copy.deepcopy(equipments_ini)

            logPhase_install = logPhase_install_init(logOp, vessels, equipments,
                                                     device, sub_device, landfall,
                                                     layout,
                                                     collection_point, dynamic_cable,
                                                     static_cable, cable_route, connectors,
                                                     external_protection, topology,
                                                     line, foundation, penet_rates, site
                                                     )

            start_time_total = timeit.default_timer()

            # extract the LogPhase ID to be evaluated from the installation plan
            log_phase_id = install['plan'][x][y]

            log_phase = logPhase_install[log_phase_id]
            log_phase.op_ve_init = log_phase.op_ve

            if PRINT_FLAG:
                print '\n'
                print '---- ' + log_phase.description + ' ----'

                #  DBs INTEGRITY CHECK:
                numbr_vess = 0
                for vess_type in vessels:
                    numbr_vess += len(vessels[vess_type].panda)
                # print 'nbr vessels available: ' + str(numbr_vess)
                numbr_eqs = 0
                for eqs_type in equipments:
                    numbr_eqs += len(equipments[eqs_type].panda)
                # print 'nbr eqs available: ' + str(numbr_eqs)

            # characterize the logistic requirements
            install['requirement'] = glob_feas(log_phase, log_phase_id,
                                              site, device, sub_device,
                                              layout,
                                              collection_point, dynamic_cable, static_cable,
                                              cable_route, connectors, external_protection,
                                              topology,
                                              line, foundation)

            # selection of the maritime infrastructure
            start_time_feas = timeit.default_timer()
            install['eq_select'], log_phase = select_e(install, log_phase)
            install['ve_select'], log_phase = select_v(install, log_phase)
            stop_time_feas = timeit.default_timer()

            # matching requirements for combinations of port/vessel(s)/equipment
            start_time_match = timeit.default_timer()
            install['combi_select'], log_phase, MATCH_FLAG = compatibility_ve(install,
                                                                              log_phase,
                                                                              install_port['Selected base port for installation'])
            stop_time_match = timeit.default_timer()
            if PRINT_FLAG:
                Num_sols=0
                for ind_strg in range(len(install['combi_select'])):
                    Num_sols = Num_sols + len(install['combi_select'][ind_strg])
                print 'Number of solutions found: ' + str(Num_sols)

            if MATCH_FLAG == 'NoSolutions':
                ves_req = {'deck area [m^2]': round( install['requirement'][5]['deck area'],2),
                           'deck cargo [t]': round( install['requirement'][5]['deck cargo'],2),
                           'deck loading [t/m^2]': round( install['requirement'][5]['deck loading'],2)}
                # wn.warn('There are no solutions! vessel requirements: ' + str(ves_req) )
                print 'There are no solutions in ' + log_phase.description + ', --> vessel requirements: ' + str(ves_req)
                install['findSolution'] = 'NoSolutionsFound' + ' in ' + log_phase.description
            else:
                # schedule assessment of the different operation sequence
                start_time_sched = timeit.default_timer()
                install['schedule'], install['end_dt'], log_phase, SCHEDULE_FLAG = sched(x, y,
                                                                                         install,
                                                                                         log_phase,
                                                                                         log_phase_id,
                                                                                         site,
                                                                                         metocean,
                                                                                         device,
                                                                                         sub_device,
                                                                                         entry_point,
                                                                                         layout,
                                                                                         collection_point,
                                                                                         dynamic_cable,
                                                                                         static_cable,
                                                                                         cable_route,
                                                                                         connectors,
                                                                                         external_protection,
                                                                                         topology,
                                                                                         line,
                                                                                         foundation,
                                                                                         penet_rates,
                                                                                         laying_rates,
                                                                                         other_rates)
                stop_time_sched = timeit.default_timer()

                if SCHEDULE_FLAG == 'NoWWindows':
                     wn.warn('No weather window found!')
                     install['findSolution'] = 'NoWeatherWindowFound'
                else:
                    # cost assessment of the different operation sequence
                    start_time_cost = timeit.default_timer()
                    install['COST'], log_phase = cost(install, log_phase, log_phase_id, other_rates)
                    stop_time_cost = timeit.default_timer()

                    # assessment of the solution with minimum cost
                    install['optimal'] = opt_sol(log_phase, log_phase_id)
                    install['findSolution'] = 'SolutionFound'

                    stop_time_total = timeit.default_timer()

                    if PRINT_FLAG:
                        print 'Final Solution Found!'

                        print '- VESSEL SPREAD: '
                        print 'Number of Journeys (port-site-port): ' + str(install['optimal']['numb of journeys'])
                        for vessel in install['optimal']['vessel_equipment']:
                            print 'Vessel Type: ' + str(vessel[0]) + ' | Quantity: ' + str(vessel[1]) + ' | Database index: ' + str(vessel[2].name)
                            for equipment in vessel[3:]:
                                print '\t \'-> Equipment Type: ' + str(equipment[0]) + ' | Quantity: ' + str(equipment[1]) + ' | Database index: ' + str(equipment[2].name)
                        print '- COST: '
                        print 'Start date: ' + str( install['optimal']['start_dt'] )
                        print 'Depart date: ' + str( install['optimal']['depart_dt'] )
                        print 'End date: ' + str( install['optimal']['end_dt'] )
                        print '- COST: '
                        print 'Solution Vessel Cost [kEURO]: ' + str(round(install['optimal']['vessel cost']/1000.0, 2))
                        print 'Solution Equipment Cost [kEURO]: ' + str(round(install['optimal']['equipment cost']/1000.0, 2))
                        print 'Solution Port Cost [kEURO]: ' + str(round(install['optimal']['port cost']/1000.0, 2))
                        print 'Solution Total Cost [kEURO]: ' + str(round(install['optimal']['total cost']/1000.0, 2))
                        print '- TIME: '
                        print 'Solution Schedule preparation time [h]: ' + str(round(install['optimal']['schedule prep time'], 2))
                        print 'Solution Schedule waiting time [h]: ' + str(round(sum(install['optimal']['schedule waiting time']), 2))
                        print 'Solution Schedule Sea Operation time [h]: ' + str(round(install['optimal']['schedule sea operation time'], 2))
                        print 'Solution Schedule Sea Transit time [h]: ' + str(round(install['optimal']['schedule sea transit time'], 2))
                        print 'Solution Schedule TOTAL time [h]: ' + str( round( install['optimal']['schedule prep time'] +
                                                                                 sum(install['optimal']['schedule waiting time']) +
                                                                                 install['optimal']['schedule sea operation time'] +
                                                                                 install['optimal']['schedule sea transit time'], 2))
                        print '- LOGISTICS: '
                        print 'Number of Journeys: ' + str(install['optimal']['numb of journeys'])

                    simul_time = {}
                    simul_time['port_CPU_time'] = stop_time_port - start_time_port
                    simul_time['feas_CPU_time'] = stop_time_feas - start_time_feas
                    simul_time['match_CPU_time'] = stop_time_match - start_time_match
                    simul_time['sched_CPU_time'] = stop_time_sched - start_time_sched
                    simul_time['cost_CPU_time'] = stop_time_cost - start_time_cost
                    simul_time['total_CPU_time'] = stop_time_total - start_time_total

                    # # DEBUG:
                    # print 'simul_time: '
                    # print simul_time

                    # formatted output dictionary containing all key results
                    # for the logistic phase that was assessed
                    logistic, OUTPUT_extra = out_process(log_phase, install)
                    out_ploting(install, logistic, simul_time, PLOT_FLAG, log_phase.description)


                    # Installation[ log_phase.description
                    Installation['OPERATION'][log_phase.description] = logistic # trocar ?!?!
                    # Installation['OPERATION'][log_phase_id] = logistic
                    Installation['PLANNING']['List of Operations [-]'].append( log_phase.description )
                    install['plan'][x][y] = logistic

                    logistic_phase_description.append (log_phase.description)
                    mean_vess_length_ope.append( OUTPUT_extra['MEAN_VESSEL_LENGTH'] )
                    numbr_vess_ope.append( OUTPUT_extra['NUMBR_VESSEL'] )
                    # numbr_vess_ope_phase[x][y].append( OUTPUT_extra['NUMBR_VESSEL'] ) # ?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!

                    # VEs
                    # number_vessels_op.append( logistic['VESSELS & EQUIPMENTS']['numb_vess'] )
                    # vess_length_op =
                    # COST:
                    Installation_total_port_cost += logistic['COST']['Port Cost [EUR]']
                    Installation_total_vessel_cost += logistic['COST']['Vessel Cost [EUR]']
                    Installation_total_equip_cost += logistic['COST']['Equipment Cost [EUR]']
                    Installation_total_cost += logistic['COST']['Total Cost [EUR]']
                    # TIME:
                    Installation_total_prep_time += logistic['TIME']['Preparation Time [h]']
                    Installation_total_wait_time += sum(logistic['TIME']['Waiting Time [h]'])
                    Installation_total_sea_trans_time += logistic['TIME']['Sea Transit Time [h]']
                    Installation_total_sea_op_time += logistic['TIME']['Sea Operation Time [h]']
                    # Installation_total_sea_time += logistic['TIME']['Sea Time [h]']
                    Installation_total_time += logistic['TIME']['Total Time [h]']

                    if PRINT_CSV:

                        # PORTS:
                        port_countries_list = list(install_port['Port list satisfying the minimum requirements']['Country [-]'])
                        # check if repeted country
                        LEN_country_list = len(port_countries_list)-1
                        ind_country=0
                        while ind_country < LEN_country_list:
                           if port_countries_list[ind_country+1] == port_countries_list[ind_country]:   # if same name
                               del port_countries_list[ind_country+1]
                               LEN_country_list = LEN_country_list-1
                           else:
                               ind_country = ind_country+1

                        # SOLUTION:
                        VE_sol = install['optimal']['vessel_equipment']
                        Vess_in_sol=[]
                        Eqs_in_sol=[]
                        for ind_vess_sol in range(len(VE_sol)):
                           Vess_in_sol.append( VE_sol[ind_vess_sol][0] )
                           if len(VE_sol[ind_vess_sol])>3:
                               nr_equip = len(VE_sol[ind_vess_sol]) - 3
                               for ind_eqs_in_vess in range(nr_equip):
                                    Eqs_in_sol.append( VE_sol[ind_vess_sol][3+ind_eqs_in_vess][0] )


                        OUTPUT_MTRX =  [log_phase.description,
                                           install_port['Terminal area [m^2]'],
                                           install_port['Terminal load bearing [t/m^2]'],
                                           len(install_port['Port list satisfying the minimum requirements']),
                                           str(port_countries_list),
                                           len(port_countries_list),
                                           install_port['Selected base port for installation']['Name [-]'],
                                           install_port['Distance port-site [km]'],
    
                                           install['requirement'][5]['deck area'], install['requirement'][5]['deck cargo'],
                                           install['requirement'][5]['deck loading'], install['requirement'][5]['deck cargo'],
    
                                           OUTPUT_extra['initial']['ves_types_init'],
                                           OUTPUT_extra['initial']['eq_types_init'],
    
                                           len(OUTPUT_extra['feasibility']['ves_types_feas']),
                                           OUTPUT_extra['feasibility']['ves_types_feas'],
                                           len(OUTPUT_extra['feasibility']['eq_types_feas']),
                                           OUTPUT_extra['feasibility']['eq_types_feas'],
    
#                                           len(install['matching']['combi_select']),
                                           len(OUTPUT_extra['matching']['ves_types_match']),
                                           OUTPUT_extra['matching']['ves_types_match'],
                                           len(OUTPUT_extra['matching']['eq_types_match']),
                                           OUTPUT_extra['matching']['eq_types_match'],
    
                                           logistic['SELECTION']['Number Initial Solutions'],
                                           len(Vess_in_sol),
                                           Vess_in_sol,
                                           len(Eqs_in_sol),
                                           Eqs_in_sol,
    
                                           logistic['TIME']['Waiting Time [h]'],
                                           logistic['TIME']['Sea Transit Time [h]'],
                                           logistic['TIME']['Preparation Time [h]'],
                                           logistic['TIME']['Total Time [h]'],
    
                                           logistic['COST']['Port Cost [EUR]'],
                                           logistic['COST']['Vessel Cost [EUR]'],
                                           logistic['COST']['Equipment Cost [EUR]'],
                                           logistic['COST']['Total Cost [EUR]'],

                                       ]

                        outputing.writerow(OUTPUT_MTRX)
                        # # Print also .txt:
                        # for ind_txt in range(len(OUTPUT_MTRX)):
                        #     outputing_txt.write("%s \t" % OUTPUT_MTRX[ind_txt])
                        # outputing_txt.write("\n")

    # if PRINT_CSV == 'True':
    #     outputing_txt.close()


    if install['findSolution'] == 'SolutionFound':

        # COST:
        Installation['COST']['Total Port Cost [EUR]'] = Installation_total_port_cost
        Installation['COST']['Total Vessel Cost [EUR]'] = Installation_total_vessel_cost
        Installation['COST']['Total Equipment Cost [EUR]'] = Installation_total_equip_cost
        Installation['COST']['Total Installation Cost [EUR]'] = Installation_total_cost
        Installation['COST']['Total Cost with Contingency [EUR]'] = Installation_total_cost * ( 1 + other_rates['Default values']['Cost Contingency [%]']/100.0)
        Installation['COST']['Yearly Cost [yy, EUR]'] = cost_p_year(Installation)
        # TIME:
        Installation['TIME']['Total Preparation Time [h]'] = Installation_total_prep_time
        Installation['TIME']['Total Waiting Time [h]'] = Installation_total_wait_time
        Installation['TIME']['Total Sea Transit Time [h]'] = Installation_total_sea_trans_time
        Installation['TIME']['Total Sea Operation Time [h]'] = Installation_total_sea_op_time
        # Installation['TIME']['Total Sea Time [h]'] = Installation_total_sea_time
        Installation['TIME']['Total Installation Time [h]'] = Installation_total_time
        # ENV.:
        Installation['ENVIRONMENTAL']['Number Vessels Installation [-]'] = np.sum( numbr_vess_ope )
        Installation['ENVIRONMENTAL']['Vessel Mean Length [m]'] = np.mean( mean_vess_length_ope )


        Installation['PORT'] = {
                                'Port Name & ID [-]': [install_port['Selected base port for installation']['Name [-]'], install_port['Selected base port for installation'].name],
                                'Distance Port-Site [km]': install_port['Distance port-site [km]'],                                'Terminal Load Bearing Requirement [t/m^2]': install_port['Terminal load bearing [t/m^2]'],
                                'Terminal Load Area Requirement [m^2]': install_port['Terminal area [m^2]']
                                # 'Port Data': install_port['Selected base port for installation']
                                }
        if len(layout)>0:
            Installation['DATE']['Comissioning Date'] = Installation['DATE']['End Date'] + timedelta( weeks = other_rates['Default values']['Comissioning time [weeks]'] )
        else:
            Installation['DATE']['Comissioning Date'] = []

        # Installation['warning'] = warning_log ?!?!?


        if PRINT_CSV:
            OUTPUT_MTRX =  ['TOTAL',
                             '','','','','','','','','','','','','','','','','','','','','','','','','','','',
                                Installation['TIME']['Total Waiting Time [h]'],
                                '',
                                # Installation['TIME']['Total Sea Time [h]'],
                                Installation['TIME']['Total Preparation Time [h]'],
                                Installation['TIME']['Total Installation Time [h]'],
                                Installation['COST']['Total Port Cost [EUR]'],
                                Installation['COST']['Total Vessel Cost [EUR]'],
                                Installation['COST']['Total Equipment Cost [EUR]'],
                                Installation['COST']['Total Installation Cost [EUR]'],

                           ]
            outputing.writerow(OUTPUT_MTRX)

        # plot gantt chart of the installation logistic phases:
        if PLOT_GANTT:
            out_ploting_installation(Installation, logistic_phase_description)


        stop_time = timeit.default_timer()
        if PRINT_FLAG:
            # print '\n'
            print '\n'
            print 'OPERATION SCHEDULING:'
            ope = -1

            for x in install['plan']:

                for y in range(len(install['plan'][x])):

                    log_id_outcome = install['plan'][x][y]
                    ope += 1
                    if type(log_id_outcome) is dict:
                        print 'logistic phase description: ' + logistic_phase_description[ope]
                        print 'ending time: ' + str(log_id_outcome['DATE']['End Date'])
                    else:
                        print '\n'
                        print 'logistic phase id: ' + log_id_outcome + ' No solution found'
                        print '\n'

            print '\n'
            print 'TOTAL INSTALLATION COST: '
            print 'Installation Port Cost [kEURO]: ' + str(round(Installation['COST']['Total Port Cost [EUR]']/1000.0, 2))
            print 'Installation Vessel Cost [kEURO]: ' + str(round(Installation['COST']['Total Vessel Cost [EUR]']/1000.0, 2))
            print 'Installation Equipment Cost [kEURO]: ' + str(round(Installation['COST']['Total Equipment Cost [EUR]']/1000.0, 2))
            print 'Installation Total Cost [kEURO]: ' + str(round(Installation['COST']['Total Installation Cost [EUR]']/1000.0, 2))
            print 'TOTAL INSTALLATION TIME: '
            print 'Installation Schedule preparation time [h]:  ' + str(round(Installation['TIME']['Total Preparation Time [h]'], 2))
            print 'Installation Schedule waiting time [h]: ' + str(round(Installation['TIME']['Total Waiting Time [h]'], 2))
            print 'Installation Schedule Sea Transit time [h]: ' + str(round(Installation['TIME']['Total Sea Transit Time [h]'], 2))
            print 'Installation Schedule Sea Operation time [h]: ' + str(round(Installation['TIME']['Total Sea Operation Time [h]'], 2))
            print 'Installation Schedule Sea Total time [h]: ' + str(round(Installation['TIME']['Total Sea Transit Time [h]'] + Installation['TIME']['Total Sea Operation Time [h]'], 2))
            print 'Installation Schedule Total Installation time [h]: ' + str(round(Installation['TIME']['Total Installation Time [h]'], 2))

            print '\n'
            print 'Simulation Duration [s]: ' + str(stop_time - start_time)

            print 'install[''findSolution'']: ' + install['findSolution']
            print '\n'
            print 'FINISH!'



    return Installation