import logging
module_logger = logging.getLogger(__name__)

def logPhase_select(OM_outputs):

    # obtain first maintenance id of the OM_outputs dataframe
    df_index = OM_outputs.index.values
    om_id = OM_outputs['ID [-]'].ix[df_index[0]]

    # check if only one id type is being called
    if all(OM_outputs['ID [-]'] == om_id):
        pass
    else:
        
        msg = ("OM maintenance id - more than one id type supplied.")
        module_logger.warning(msg)

    # Associate maintenance id with logphase id
    for index, row in OM_outputs.iterrows():

        om_id = OM_outputs['ID [-]'].ix[index]

        if om_id == 'Insp1' or om_id == 'MoS1' or om_id == 'Insp2' or om_id == 'MoS2':
            log_phase_id = 'LpM1'

        elif om_id == 'Insp3' or om_id == 'MoS3':
              log_phase_id = 'LpM2'

        elif om_id == 'Insp4' or om_id == 'Insp5' or om_id == 'MoS4':
              log_phase_id = 'LpM3'

        elif om_id == 'MoS5' or om_id == 'MoS6':
              log_phase_id = 'LpM4'

        elif om_id == 'MoS7' or om_id == 'MoS8':
              log_phase_id = 'LpM5'

        elif om_id == 'RtP1' or om_id == 'RtP2':
              log_phase_id = 'LpM6'

        elif om_id == 'RtP3' or om_id == 'RtP4':
              log_phase_id = 'LpM7'

        elif om_id == 'RtP5' or om_id == 'RtP6':
              log_phase_id = 'LpM8'

        else:
            
            allowed_phases = ['Insp1','Insp2','Insp3','Insp4',
                              'MoS1', 'MoS2', 'MoS3', 'MoS4', 'MoS5', 'MoS6',
                              'MoS7', 'MoS8',
                              'RtP1', 'RtP2', 'RtP3', 'RtP4', 'RtP5', 'RtP6']
            allowed_phases_str = ", ".join(allowed_phases)
            msg = ("OM maintenance id {} not supported. Allowed ids are: "
                   "{}.".format(om_id, allowed_phases_str))
            module_logger.warning(msg)

    return log_phase_id


