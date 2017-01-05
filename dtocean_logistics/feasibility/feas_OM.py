from .devices import devices_feas
# from .electrical import static_feas, cp_feas, external_feas
from .MF import MF_feas
from .om import om_feas

def feas_om(log_phase, log_phase_id, user_inputs, om, electrical_outputs, MF_outputs):
    """feas_OM.py contains a function that calls the appropriate sub-functions to
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

    feasibility = om_feas(log_phase, log_phase_id, om, user_inputs, electrical_outputs, MF_outputs)

    return feasibility
