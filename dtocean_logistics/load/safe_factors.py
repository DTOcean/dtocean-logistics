import timeit
from ..phases import VesselType

def safety_factors(ports, vessels_0, equipments, port_sf, vessel_sf, eq_sf):


    # PORT:
    start_time_sf = timeit.default_timer()
    for indx_param, row_param in port_sf.iterrows():
        # print 'indx_param: ' + str(indx_param) # DEBUGGING

        param2change = port_sf['Port parameter and unit [-]'][indx_param]
        ports.loc[:,param2change] /= ( 1 + port_sf['Safety factor (in %) [-]'][indx_param] )
    stop_time_sf = timeit.default_timer()
    # print 'PORTS Safety factors simulation time [s]: ' + str(stop_time_sf - start_time_sf) # DEBUG!

    # VESSEL:
    start_time_sf = timeit.default_timer()
    for indx_param, row_param in vessel_sf.iterrows():
        # print 'indx_param: ' + str(indx_param) # DEBUGGING

        param2change = vessel_sf['Vessel parameter and unit [-]'][indx_param]
        vessels_0.loc[:,param2change] /= ( 1 + vessel_sf['Safety factor (in %) [-]'][indx_param] )

    # Splits the pd_vessel object with the full dataset, into smaller panda
    # objects with specific vessel types. Each vessel object is initiated with
    # the vessel class: VesselType
    pd_vessel = vessels_0
    vessels = {'Barge': VesselType("Barge", pd_vessel[pd_vessel['Vessel type [-]'] == 'Barge']),
               'Tugboat': VesselType("Tugboat", pd_vessel[pd_vessel['Vessel type [-]'] == 'Tugboat']),
               'Crane Barge': VesselType("Crane Barge", pd_vessel[pd_vessel['Vessel type [-]'] == 'Crane Barge']),
               'Crane Vessel': VesselType("Crane Vessel", pd_vessel[pd_vessel['Vessel type [-]'] == 'Crane Vessel']),
               'JUP Barge': VesselType("JUP Barge", pd_vessel[pd_vessel['Vessel type [-]'] == 'JUP Barge']),
               'JUP Vessel': VesselType("JUP Vessel", pd_vessel[pd_vessel['Vessel type [-]'] == 'JUP Vessel']),
               'AHTS': VesselType("AHTS", pd_vessel[pd_vessel['Vessel type [-]'] == 'AHTS']),
               'Multicat': VesselType("Multicat", pd_vessel[pd_vessel['Vessel type [-]'] == 'Multicat']),
               'CLV': VesselType("CLV", pd_vessel[pd_vessel['Vessel type [-]'] == 'CLV']),
               'CLB': VesselType("CLB", pd_vessel[pd_vessel['Vessel type [-]'] == 'CLB']),
               'CTV': VesselType("CTV", pd_vessel[pd_vessel['Vessel type [-]'] == 'CTV']),
               'CSV': VesselType("CSV", pd_vessel[pd_vessel['Vessel type [-]'] == 'CSV']),
               'Fit for Purpose': VesselType("Fit for Purpose", pd_vessel[pd_vessel['Vessel type [-]'] == 'Fit for Purpose']),
               'PSV': VesselType("Platform Supply Vessel", pd_vessel[pd_vessel['Vessel type [-]'] == 'Platform Support Vessel']),
               'Helicopter': VesselType("Helicopter", pd_vessel[pd_vessel['Vessel type [-]'] == 'Helicopter'])
               }
    stop_time_sf = timeit.default_timer()
    # print 'VESSELS Safety factors simulation time [s]: ' + str(stop_time_sf - start_time_sf) # DEBUG!


    # EQUIPMENT:
    start_time_sf = timeit.default_timer()
    for indx_param, row_param in eq_sf.iterrows():
        # print 'indx_param: ' + str(indx_param) # DEBUGGING

        for indx_eqs_type in equipments.keys():
            # print 'indx_eqs_type: ' + str(indx_eqs_type) # DEBUGGING

            if indx_eqs_type == eq_sf['Equipment type id [-]'][indx_param]:

                param2change = eq_sf['Equipment parameter and unit [-]'][indx_param]
                # equipments[indx_eqs_type].panda[ param2change ][indx_eqs] /= ( 1 + eq_sf['Safety factor (in %) [-]'][indx_param] )
                equipments[indx_eqs_type].panda.loc[:,param2change ] /= ( 1 + eq_sf['Safety factor (in %) [-]'][indx_param] )

    stop_time_sf = timeit.default_timer()
    # print 'EQUIPS Safety factors simulation time [s]: ' + str(stop_time_sf - start_time_sf) # DEBUG!



    return ports, vessels, equipments