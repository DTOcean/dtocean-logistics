from .devices import devices_feas
from .electrical import cp_feas, dynamic_feas, export_feas, array_feas, external_feas
from .MF import MF_feas
from .SS import SS_feas


def glob_feas(log_phase, log_phase_id,
              site, device, sub_device,
              layout,
              collection_point, dynamic_cable, static_cable,
              cable_route, connectors, external_protection,
              topology,
              line, foundation):
    """glob.py contains a function that calls the appropriate sub-functions to
    determine the logistic requirements associated with one logistic phase

    Parameters
    ----------
    log_phase : Class
     Class of the logistic phase under consideration for assessment
    log_phase_id : str
     string describing the ID of the logistic phase under consideration
    user_inputs : dict
     dictionnary containing all required inputs to WP5 coming from WP1/end-user
    wp2_outputs : dict
     dictionnary containing all required inputs to WP5 coming from WP2
    wp3_outputs : dict
     dictionnary containing all required inputs to WP5 coming from WP3
    wp4_outputs : DataFrame
     Panda table containing all required inputs to WP5 coming from WP4

    Returns
    -------
    feasibility : tuple
     tuple containing all logistic requirements associated with every vessel
     and equipment type of the logistic phase under consideration
    """
    if log_phase_id == 'E_export':
        feasibility = export_feas(log_phase, log_phase_id, site,
                                  static_cable, cable_route, connectors,
                                  collection_point)
        
    if log_phase_id == 'E_array':
        feasibility = array_feas(log_phase, log_phase_id, site,
                                 static_cable, cable_route, connectors,
                                 collection_point)

    if log_phase_id == 'E_dynamic':
        feasibility = dynamic_feas(log_phase, log_phase_id, site,
                                   dynamic_cable, connectors)

    if any(log_phase_id in s for s in ['E_cp_seabed', 'E_cp_surface']):
        feasibility = cp_feas(log_phase, log_phase_id, site,
                              collection_point)

    if log_phase_id == 'E_external':
        feasibility = external_feas(log_phase, log_phase_id, site,
                              external_protection)
        
    elif any(log_phase_id in s for s in ['Driven', 'Gravity', 'M_drag', 'M_direct', 'M_suction','M_pile']):
        feasibility = MF_feas(log_phase, log_phase_id, 
                              layout,
                              line, foundation)

    elif log_phase_id == 'S_structure':
        feasibility = SS_feas(log_phase, log_phase_id, sub_device, layout, site)
        
    elif log_phase_id == 'Devices':
        feasibility = devices_feas(log_phase, log_phase_id, site,
                                   device, sub_device,
                                   layout)

    # print 'log_phase_id: ' + str(log_phase_id) # DEBUGGIN!!!
    return feasibility