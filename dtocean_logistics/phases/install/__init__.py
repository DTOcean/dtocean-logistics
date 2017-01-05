# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module governs the definition of the logistic phases. The functions included
are responsible to initialize and characterize the logistic phases both of the
installation and O&M modules. The functions return a class of each logistic phase
characterized in terms of operations sequence and vessel & equipment combination.

BETA VERSION NOTES: In this version, only two logistic phases were characterized,
one related to Moorings and Foundation Installation: Driven Pile, and another
related to Operation and Maintenance: Offshore Inspection.
"""

from .classes import LogPhase, DefPhase

from .e_export import init_e_export_phase
from .e_array import init_e_array_phase
from .e_cp import init_e_cp_seabed_phase
from .e_cp import init_e_cp_surface_phase
from .e_dynamic import init_e_dynamic_phase
from .e_external import init_e_external

from .Driven import init_drive_phase
from .Gravity import init_gravity_phase

from .M_Drag import init_m_drag_phase
from .M_Direct import init_m_direct_phase
from .M_Suction import init_m_suction_phase
from .M_Pile import init_m_pile_phase

from .S_Structure import init_support_phase
from .devices import init_devices_phase


def logPhase_install_init(log_op, vessels, equipments,
                          device, sub_device, landfall,
                          layout,
                          collection_point, dynamic_cable, static_cable,
                          cable_route, connectors, external_protection,
                          topology,
                          line, foundation, penet_rates, site):

    """This function initializes and characterizes all logistic phases associated
    with the installation module. The first step uses LogPhase class to initialize
    each class with a key ID and description, the second step uses the DefPhase
    class to characterize each phase with a set of operation sequences and vessel
    and equipment combinations.
    Explanation of the key ID numbering system implemented:
     1st digit: 1 = Installation;
                9 = O&M
     2nd digit: 0 = Electrical infrastructure;
                1 = Moorings and foundations;
                2 = Wave and Tidal devices;
     3rd digit: component/sub-system type - differ depending on the logistic phase
     4th digit: method (level 1) - differ depending on the logistic phase
     5th digit: sub-method (level 2) - differ depending on the logistic phase

    Parameters
    ----------
    log_op : dict
     dictionnary containing all classes defining the individual logistic operations
    vessels : DataFrame
     Panda table containing the vessel database
    equipments : DataFrame
     Panda table containing the equipment database

    Returns
    -------
    logPhase_install : dict
     dictionnary containing all classes defining the logistic phases for installation
    """

    # 1st Level - Initialize the logistic phases through LogPhase classes

    # TO BE CHANGED IN ORDER TO ONLY INITIALISE THE PHASES THAT ARE REQUESTED ACCORDING TO THE INSTALLATION PLAN (AND/OR OPERATION SEQUENCE)
    logPhase_install = {'E_export': init_e_export_phase(log_op,
                                                        vessels,
                                                        equipments,
                                                        landfall,
                                                        static_cable,
                                                        cable_route,
                                                        collection_point),

                        'E_array': init_e_array_phase(log_op,
                                                      vessels,
                                                      equipments,
                                                      static_cable,
                                                      cable_route,
                                                      collection_point),

                        'E_dynamic': init_e_dynamic_phase(log_op,
                                                          vessels,
                                                          equipments,
                                                          dynamic_cable,
                                                          collection_point),

                        'E_external': init_e_external(log_op,
                                                      vessels,
                                                      equipments,
                                                      external_protection),

                        'E_cp_seabed': init_e_cp_seabed_phase(log_op,
                                                              vessels,
                                                              equipments,
                                                              collection_point),


                        'E_cp_surface': init_e_cp_surface_phase(log_op,
                                                                vessels,
                                                                equipments,
                                                                collection_point),

                        'Driven': init_drive_phase(log_op,
                                                   vessels, equipments,
                                                   foundation, penet_rates, site),

                        'Gravity': init_gravity_phase(log_op,
                                                      vessels,
                                                      equipments,
                                                      foundation),

                        'M_drag': init_m_drag_phase(log_op,
                                                    vessels, equipments,
                                                    foundation),

                        'M_direct': init_m_direct_phase(log_op,
                                                        vessels,
                                                        equipments,
                                                        foundation,
                                                        penet_rates, site),

                        'M_suction': init_m_suction_phase(log_op,
                                                          vessels,
                                                          equipments,
                                                          foundation),
                        'M_pile': init_m_pile_phase(log_op,
                                                    vessels,
                                                    equipments,
                                                    foundation),

                        'S_structure': init_support_phase(log_op,
                                                          vessels,
                                                          equipments,
                                                          device,
                                                          sub_device,
                                                          layout),

                        'Devices': init_devices_phase(log_op,
                                                      vessels,
                                                      equipments,
                                                      device,
                                                      layout)
                        }
    return logPhase_install
