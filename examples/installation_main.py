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


import copy
import logging
from datetime import timedelta

import numpy as np

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
from dtocean_logistics.load.safe_factors import safety_factors
from dtocean_logistics.performance.economic.cost_year import cost_p_year

from dtocean_logistics.load.input_checkin import input_check

# Set up logging
module_logger = logging.getLogger(__name__)


def installation_main(vessels, equipments, ports, phase_order, schedule_OLC,
                      penet_rates, laying_rates, other_rates, port_sf,
                      vessel_sf, eq_sf, site, metocean, device, sub_device,
                      landfall, entry_point, layout, collection_point,
                      dynamic_cable, static_cable, cable_route, connectors,
                      external_protection, topology, line, foundation,
                      PRINT_FLAG = False, PLOT_FLAG = False,
                      PLOT_GANTT = False, PRINT_CSV = False,
                      csv_filename = None,
                      plan_only=False,
                      skip_phase=False,
                      check_inputs=False):
                          
    '''The main file of the installation module, providing an estimation of the
    predicted performance of feasible maritime infrastructure solutions that
    can carry out marine installation operations. Five processes are performed:

        1- Initialising the logistic classes
        2- Defining the installation plan
        3- Selecting the installation port
        4- Performing the assessment of all logistic phases sequencially,
           following six steps:
               (i) characterizartion of logistic requirements
               (ii) selection of the maritime infrastructure
               (iii) schedule assessment of the logistic phase
               (iv) cost assessment of the logistic phase
               (v) risk assessment of the logistic phase
               (vi) environmental impact assessment of the logistic phase

    Args:
        vessels(DataFrame) [-]: Panda table containing the vessel database.
        equipments (DataFrame) [-]: Panda table containing the equipment
            database.
        ports (DataFrame) [-]: Panda table containing the ports database.
        phase_order (Dataframe) [-]: dataframe containing a panda dataframe
            with the logistic operation phase order.
        schedule_OLC (Dataframe) [-]: dataframe containing a panda dataframe
         with time duration and operational limit conditions.
         penet_rates (Dataframe) [-]: dataframe containing the penetration
             rates according to soil type.
        laying_rates (Dataframe) [-]: dataframe containing the laying rates
            according to soil type.
        other_rates (Dataframe) [-]: dataframe containing other rates.
        port_sf (Dataframe) [-]: dataframe containing the safety factors
            applied to ports.
        vessel_sf (Dataframe) [-]: dataframe containing the safety factors
            applied to vessels.
        eq_sf (Dataframe) [-]: dataframe containing the safety factors applied
            to equipments.
        site (Dataframe) [-]: inputs required from the site leasa area
            coordinates.
        metocean (Dataframe) [-]: metocean data.
        device (Dataframe) [-]: inputs required from the device.
        sub_device (Dataframe) [-]: inputs required from the sub-device.
        landfall (Dataframe) [-]: inputs required from the landfall point.
        layout (DataFrame) [-]: UTM position of the devices.
        collection_point (Dataframe) [-]: collection point data.
        dynamic_cable (Dataframe) [-]: dynamic cable data.
        static_cable (Dataframe) [-]: static cable data.
        cable_route (Dataframe) [-]: cable route data.
        connectors (Dataframe) [-]: cabe connectors data.
        external_protection' (Dataframe): coordinates and type of the external
         protection elements data.
        topology (Dataframe) [-]: electrical layout type.
        line (Dataframe) [-]: mooring lines data.
        foundation (Dataframe) [-]: foundations data.
        PRINT_FLAG (boolean)[-]: flag to indicate if output prints should be
            sent to the terminal.
        PLOT_FLAG (boolean) [-]: flag to indicate if output plots should be
            presented and saved.
        PLOT_GANTT (boolean) [-]: flag to indicate if the installation gantt
            chart should be presented and saved.
        PRINT_CSV (boolean) [-]: flag to indicate if the output .csv file with
        results per logistic phase should be produced.
        csv_filename (string) [-]: name to give to the csv output file (if
            requested as an output)

    Returns:

        installation (dict): dictionary compiling all key results obtained from
            the ssessment of the logistic phases for installation. Keys are:

            'inst_log': List of logistic phase during installation.
            'port_req': Dictionary of the port requirements calculated.
            'port_feas': Dictionary of ports satisfying the requirements.
            'port_sol': Dictionary of the port selected and its distance to
                site.
            'planning': Dictionary containing the layering rules for the
                planning of the logistic phases during installation.
            'inst_sol': Dictionary containing the outcome of the optimal
                solutions for each logistic phase during installation, with
                keys:
                    plan (dict): installation sequence of the required logistic
                        phases.
                    port (DataFrame): port data related to the selected
                        installation port.
                    requirement (tuple): minimum requirements returned from the
                        feasibility functions.
                    eq_select (dict): list of equipments satisfying the minimum
                        requirements.
                    ve_select (dict): list of vessels satisfying the minimum
                        requirements.
                    combi_select (dict): list of solutions passing the
                        compatibility check.
                    schedule (dict): list of parameters with data about time.
                    cost (dict): vessel equiment and port cost.
                    risk (dict)': currently empty.
                    envir (dict)': currently empty.
                    status: string indicating if the computation was successful
                        and a solution was found.
            'dev_com': Commissioning time per device.
            'warning': Warning message.

    Note:
        location of the outside file for the port selection process:
            'point_path' (path): location of the european coastline grid data
            'graph_path' (path): location of the graph structure for the port
                                 selection algorithm

        Additional output plots can be produced if the user indicates.
            Plot bar: indicating the cost, schedule and simulation time values
            Plot pie: indicating the cost, schedule and simulation time
                      percentual distribution
            Plot table: indicating the number and type of vessel equipment
                        available through selection process and the selection
                        requirements per logistic phase, with the name of the
                        file accordingly.

    '''

    # check inputs
    if check_inputs:
        
        msg = ("Error checking inputs...")
        module_logger.info(msg)
        
        input_error, input_warning_list = input_check(vessels,
                                                         equipments,
                                                         ports,
                                                         site,
                                                         metocean,
                                                         device,
                                                         sub_device,
                                                         landfall,
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
                                                         PRINT_FLAG,
                                                         PLOT_FLAG,
                                                         PLOT_GANTT,
                                                         PRINT_CSV,
                                                         csv_filename)
    
        if input_error:

            all_errors = ". ".join(input_warning_list)
            errStr = 'Some errors in input data: {}'.format(all_errors)
            raise ValueError(errStr)
            
        else:
            
            msg = ("Error checking inputs passed...")
            module_logger.info(msg)

    # apply safety factors in vessels parameters
    ports, vessels, equipments = safety_factors(ports, vessels, equipments,
                                                port_sf, vessel_sf, eq_sf)


    vessels_ini = copy.deepcopy(vessels)
    equipments_ini = copy.deepcopy(equipments)

    logOp = logOp_init(schedule_OLC)

    ### Check the presence of the lease area entry point
    if len(entry_point)==0:

        entry_point['x coord [m]'] = site['x coord [m]'].iloc[0]
        entry_point['y coord [m]'] = site['y coord [m]'].iloc[0]
        entry_point['zone [-]'] = site['zone [-]'].iloc[0]
        entry_point['bathymetry [m]'] = site['bathymetry [m]'].iloc[0]
        entry_point['soil type [-]'] = site['soil type [-]'].iloc[0]

    ### Determine the adequate installation logistic phase plan
    install_plan = planning.install_plan(phase_order, device, layout,
                                         collection_point, dynamic_cable,
                                         static_cable, external_protection,
                                         line, foundation)

    ### Select the most appropriate base installation port
    install_port = select_port.install_port(device, sub_device, site,
                                            entry_point, ports, line, 
                                            foundation, collection_point,
                                            install_plan)

    port_name = install_port['Selected base port for installation']['Name [-]']
    logMsg = "'{}' selected as installation port".format(port_name)
    module_logger.info(logMsg)

    # Incremental assessment of all logistic phase of the installation process
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
               }

    Installation = {'PORT': {},
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
    Installation_total_prep_time = 0
    Installation_total_time = 0
    Installation_total_sea_op_time = 0
    Installation_total_sea_trans_time = 0

    if plan_only: return

    #  loop over the phases of the installation plan
    install['findSolution'] = 'SolutionFound'
    
    logPhase_install = logPhase_install_init(logOp,
                                             vessels,
                                             equipments,
                                             device,
                                             sub_device,
                                             landfall,
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
                                             site)
    
    skipped = []
    something_installed = False

    for x in install['plan']:
        
        for y in range(len(install['plan'][x])):

            # extract LogPhase ID to be evaluated from the installation plan
            log_phase_id = install['plan'][x][y]

            log_phase = logPhase_install[log_phase_id]
            log_phase.op_ve_init = log_phase.op_ve
                        
            msg = ("Checking installation requirements for phase: {}.").format(
                   log_phase.description)

            module_logger.info(msg)

            # characterize the logistic requirements
            install['requirement'] = glob_feas(log_phase,
                                               log_phase_id,
                                               site,
                                               device,
                                               sub_device,
                                               layout,
                                               collection_point,
                                               dynamic_cable,
                                               static_cable,
                                               cable_route,
                                               connectors,
                                               external_protection,
                                               topology,
                                               line,
                                               foundation)
            
            # Selection of the feasible equipment
            install['eq_select'], log_phase = select_e(install, log_phase)
                        
            # Selection of the feasible vessels
            install['ve_select'], log_phase = select_v(install, log_phase)
                        
            # matching requirements for combinations of port/vessel/equipment
            install['combi_select'], log_phase, MATCH_FLAG = compatibility_ve(
                install, log_phase,
                install_port['Selected base port for installation'])

            #TODO: Tidy this summation - check the data structure
            Num_sols = 0

            for strg in install['combi_select']:
                Num_sols += len(strg)

            msg = ("{} possible solutions found.").format(Num_sols)
            module_logger.info(msg)

            if MATCH_FLAG == 'NoSolutions':

                msg = ("Cannot complete installation phase: {}. See logs for "
                       "further details").format(log_phase.description)

                if not skip_phase: raise RuntimeError(msg)
                    
                module_logger.warning(msg)

                install['findSolution'] = (
                    'NoSolutionsFound' + ' in ' + log_phase.description)
                    
                skipped.append(log_phase.description)
                
                continue

            # schedule assessment of the different operation sequence
            (install['end_dt'],
             log_phase, 
             SCHEDULE_FLAG) = sched(x,
                                    y,
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

            if SCHEDULE_FLAG == 'NoWWindows':
                
                msg = ("Cannot complete installation phase {}. No suitable"
                       " weather window found.").format(
                       log_phase.description)
                
                if not skip_phase: raise RuntimeError(msg)

                module_logger.warning(msg)

                install['findSolution'] = 'NoWeatherWindowFound'

                skipped.append(log_phase.description)
                
                continue
                
            something_installed = True

            # cost assessment of the different operation sequence
            install['COST'], log_phase = \
                cost(install, log_phase, log_phase_id, other_rates)

            # assessment of the solution with minimum cost
            install['optimal'] = opt_sol(log_phase, log_phase_id)
            install['findSolution'] = 'SolutionFound'
            
            # check for vessel fuel
            if install['optimal']['fuel cost'] == 0:

                module_logger.warning("Lack of information on vessel "
                                      "fuel consumption. Fuel cost "
                                      "not considered for this "
                                      "installation phase.")

            # check for equipment cost
            if install['optimal']['equipment cost'] == 0:
                
                module_logger.warning("Lack of information on "
                                      "equipment cost. Equipment cost "
                                      "not considered for this "
                                      "installation phase.")

            msg = ("Final solution found.") # how much detail here?
            module_logger.info(msg)

            if PRINT_FLAG:

                print 'Final Solution Found!'
                print '- VESSEL SPREAD: '
                print ('Number of Journeys (port-site-port): ' +
                        str(install['optimal']['numb of journeys']))

                for vessel in install['optimal']['vessel_equipment']:

                    msg = ("Vessel Type: {} | Quantity: {} | "
                           "Database index: {}".format(
                           vessel[0], vessel[1], vessel[2].name ))
                    print msg 

                    for equipment in vessel[3:]:

                        msg = ("\t -> Equipment Type: {} | Quantity: "
                               "{} | Database index: {}".format(
                               equipment[0], equipment[1],
                               equipment[2].name))
                        print msg

                print '- DATES: '
                print ('Start date: ' +
                    str(install['optimal']['start_dt']))
                print ('Depart date: ' +
                    str(install['optimal']['depart_dt']))
                print ('End date: ' +
                    str(install['optimal']['end_dt']))

                print '- COST: '
                print ('Solution Vessel Cost [EURO]: ' +
                    str(round(install['optimal']['vessel cost'], 2)))
                print ('Solution Equipment Cost [EURO]: ' +
                    str(round(install['optimal']['equipment cost'],2)))
                print ('Solution Port Cost [EURO]: ' +
                    str(round(install['optimal']['port cost'], 2)))
                print ('Solution Total Cost [EURO]: ' +
                    str(round(install['optimal']['total cost'], 2)))

                print '- TIME: '
                print ('Solution Schedule preparation time [h]: ' +
                    str(round(install['optimal']\
                        ['schedule prep time'], 2)))
                print ('Solution Schedule waiting time [h]: ' +
                    str(round(install['optimal']\
                        ['schedule waiting time'], 2)))
                print ('Solution Schedule Sea Operation time [h]: ' +
                    str(round(install['optimal']\
                        ['schedule sea operation time'], 2)))
                print ('Solution Schedule Sea Transit time [h]: ' +
                        str(round(install['optimal']\
                        ['schedule sea transit time'], 2)))
                print ('Solution Schedule TOTAL time [h]: ' +
                    str(round(
                            install['optimal']['schedule prep time'] +
                            install['optimal']\
                                ['schedule waiting time'] +
                            install['optimal']\
                                ['schedule sea operation time'] +
                            install['optimal']\
                                ['schedule sea transit time'], 2)))

                print '- LOGISTICS: '
                print ('Number of Journeys: ' +
                        str(install['optimal']['numb of journeys']))

            simul_time = {} # leave empty to pass into out_ploting

            # formatted output dictionary containing all key results
            # for the logistic phase that was assessed
            logistic, OUTPUT_extra = out_process(log_phase, install)
            out_ploting(install,
                        logistic,
                        simul_time,
                        PLOT_FLAG,
                        log_phase.description)

            # Installation[ log_phase.description
            Installation['OPERATION'][log_phase.description] = \
                logistic  # trocar ?!?!
            # Installation['OPERATION'][log_phase_id] = logistic
            Installation['PLANNING']['List of Operations [-]'].append(
                log_phase.description)
            install['plan'][x][y] = logistic

            logistic_phase_description.append(log_phase.description)
            mean_vess_length_ope.append(
                OUTPUT_extra['MEAN_VESSEL_LENGTH'])
            numbr_vess_ope.append(OUTPUT_extra['NUMBR_VESSEL'])

            # COST:
            Installation_total_port_cost += \
                logistic['COST']['Port Cost [EUR]']
            Installation_total_vessel_cost += \
                logistic['COST']['Vessel Cost [EUR]']
            Installation_total_equip_cost += \
                logistic['COST']['Equipment Cost [EUR]']
            Installation_total_cost += \
                logistic['COST']['Total Cost [EUR]']

            # TIME:
            Installation_total_prep_time += \
                logistic['TIME']['Preparation Time [h]']
            Installation_total_wait_time += \
                logistic['TIME']['Waiting Time [h]']
            Installation_total_sea_trans_time += \
                logistic['TIME']['Sea Transit Time [h]']
            Installation_total_sea_op_time += \
                logistic['TIME']['Sea Operation Time [h]']
            Installation_total_time += \
                logistic['TIME']['Total Time [h]']

    if something_installed:

        # Cost
        Installation['COST']['Total Port Cost [EUR]'] = \
            Installation_total_port_cost
        Installation['COST']['Total Vessel Cost [EUR]'] = \
            Installation_total_vessel_cost
        Installation['COST']['Total Equipment Cost [EUR]'] = \
            Installation_total_equip_cost
        Installation['COST']['Total Installation Cost [EUR]'] = \
            Installation_total_cost
        Installation['COST']['Total Contingency Costs [EUR]'] = \
            Installation_total_cost * \
                other_rates['Default values']['Cost Contingency [%]'] / 100.0
        Installation['COST']['Yearly Cost [yy, EUR]'] = \
            cost_p_year(Installation)

        # Time
        Installation['TIME']['Total Preparation Time [h]'] = \
            Installation_total_prep_time
        Installation['TIME']['Total Waiting Time [h]'] = \
            Installation_total_wait_time
        Installation['TIME']['Total Sea Transit Time [h]'] = \
            Installation_total_sea_trans_time
        Installation['TIME']['Total Sea Operation Time [h]'] = \
            Installation_total_sea_op_time
        Installation['TIME']['Total Installation Time [h]'] = \
            Installation_total_time

        # Environmental
        Installation['ENVIRONMENTAL']['Number Vessels Installation [-]'] = \
            np.sum( numbr_vess_ope )
        Installation['ENVIRONMENTAL']['Vessel Mean Length [m]'] = \
            np.mean(mean_vess_length_ope)
    
        Installation['PORT'] = {
            'Port Name & ID [-]':
                    [install_port['Selected base port for installation']\
                        ['Name [-]'],
                     install_port['Selected base port for installation'].name],
            'Distance Port-Site [km]': install_port['Distance port-site [km]'],
            'Terminal Load Bearing Requirement [t/m^2]':
                install_port['Terminal load bearing [t/m^2]'],
            'Terminal Load Area Requirement [m^2]':
                install_port['Terminal area [m^2]']}
            
        if len(layout)>0:
            
            Installation['DATE']['Comissioning Date'] = \
                (Installation['DATE']['End Date'] + \
                    timedelta(weeks = other_rates['Default values']\
                                                ['Comissioning time [weeks]']))

        else:

            Installation['DATE']['Comissioning Date'] = []

        if PRINT_FLAG:

            print '\n'
            print 'OPERATION SCHEDULING:'

            ope = -1

            for x in range(len(install['plan'])):

                for y in range(len(install['plan'][x])):

                    log_id_outcome = install['plan'][x][y]
                    ope += 1

                    if type(log_id_outcome) is dict:

                        print ('logistic phase description: ' +
                                logistic_phase_description[ope])
                        print ('ending time: ' + 
                                str(log_id_outcome['DATE']['End Date']))

                    else:
                        
                        print '\n'
                        msg = ("logistic phase id: {} . "
                               "No solution found".format(log_id_outcome))
                        print msg
                        print '\n'
    
            print '\n'

            print 'TOTAL INSTALLATION COST: '

            print ('Installation Port Cost [EURO]: ' +
                str(round(Installation['COST']['Total Port Cost [EUR]'], 2)))

            print ('Installation Vessel Cost [EURO]: ' +
                str(round(Installation['COST']['Total Vessel Cost [EUR]'], 2)))

            print ('Installation Equipment Cost [EURO]: ' +
                str(round(Installation['COST']\
                    ['Total Equipment Cost [EUR]'], 2)))

            print ('Installation Total Cost [EURO]: ' +
                str(round(Installation['COST']\
                    ['Total Installation Cost [EUR]'], 2)))

            print 'TOTAL INSTALLATION TIME: '

            print ('Installation Schedule preparation time [h]:  ' +
                str(round(Installation['TIME']\
                    ['Total Preparation Time [h]'], 2)))
                    
            print ('Installation Schedule waiting time [h]: ' +
                str(round(Installation['TIME']['Total Waiting Time [h]'], 2)))
                
            print ('Installation Schedule Sea Transit time [h]: ' +
                str(round(Installation['TIME']\
                    ['Total Sea Transit Time [h]'], 2)))

            print ('Installation Schedule Sea Operation time [h]: ' +
                str(round(Installation['TIME']\
                    ['Total Sea Operation Time [h]'], 2)))

            total_sea_time = str(round(
                Installation['TIME']['Total Sea Transit Time [h]'] + 
                Installation['TIME']['Total Sea Operation Time [h]'], 2))

            print ('Installation Schedule Sea Total time [h]: ' +
                total_sea_time)

            print ('Installation Schedule Total Installation time [h]: ' +
                str(round(Installation['TIME']\
                    ['Total Installation Time [h]'], 2)))
    
            print '\n'
    
            print 'install[''findSolution'']: ' + install['findSolution']
            print '\n'
            print 'FINISH!'
            
    else:
        
        errStr = "No installation solution found."
        raise RuntimeError(errStr)

    if skipped:

        skipped_str = ', '.join(skipped)

        msg = "The following phases could not be installed: {}".format(
            skipped_str)

        module_logger.info(msg)

    module_logger.info("Planning of project installation complete...")

    return Installation
 