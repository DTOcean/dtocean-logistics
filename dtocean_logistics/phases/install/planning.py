# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is responsible for the chronological ordering of the different
logistic phases during installation. The selection from the user and inputs
from upstream DTOcean modules build up specific installation sequences.
This module returns the installation sequence based on either the phase order
specified by the user or default ordering relying on: type of foundations,
type of moorings, type of electrical infranstrucutre and the type of devices.

"""

from ...ancillaries.find import indices
from ...ancillaries.compare import comp


def install_plan(phase_order, device, layout, collection_point, dynamic_cable,
                 static_cable, external_protection, line, foundation):
    """
    install_plan :


    Parameters
    ----------
    layout : panda DataFrame
     

    Returns
    -------
    install_plan : list
     list containing the id of the logistic phases required to conduct
     the installation of the project plus information about the interphase
     relation and sequence.
    """

    # Initialisation
    install_plan = {}

    # Extract the list of logistic phase ids from the default order defined by
    # the user
    po_type_list = list(phase_order.index.values)
    # Recognize logistic phases to be considered for the assessment

    # 1- Moorings and foundations installed first by default
    # Extract list of foundation type
    f_type_list = foundation['type [-]'].tolist()
    # Check if there are any foundations to be installed
    if len(foundation) > 0:
        # initialisation 
        install_plan[0] = []
        # default order for foundations and anchors is assumed to be ´0´,
        # i.e installed before any other array elements
        order_f_d = 0
        order_m_d = 0
        order_f_g = 0
        order_m_drag = 0
        order_m_direct = 0
        order_m_suct = 0
        # Check if there are any pile foundation/anchor to be installed
        if any(typ == 'pile foundation' for typ in f_type_list) or any(typ == 'pile anchor' for typ in f_type_list):
            # Check if it is a floating or a bottom fixed system
            if len(line) > 0:
                # Consider the order defined by the user if any
                if any(typ == 'Driven' for typ in po_type_list):
                    order_f_d = phase_order['Default Order'].ix['Driven']
                    if order_f_d in install_plan:
                        install_plan[order_f_d].append('Driven')
                    else:
                        install_plan[order_f_d] = ['Driven']
                    # Mooring line always installed after pile anchor
                    order_m_d = order_f_d + 1
                    if order_m_d in install_plan:
                        install_plan[order_m_d].append('M_pile')
                    else:
                        install_plan[order_m_d] = ['M_pile']
                else:  # Default order is 0 for the pile anchor and 1 for the
                    # line installation
                    order_f_d = 0
                    order_m_d = order_f_d + 1
                    install_plan[order_f_d].append('Driven')
                    install_plan[order_m_d] = ['M_pile']
            # Bottom-fixed system, hence no mooring line installation
            # Consider the order defined by the user if any
            elif any(typ == 'Driven' for typ in po_type_list):
                order_f_d = phase_order['Default Order'].ix['Driven']
                if order_f_d in install_plan:
                    install_plan[order_f_d].append('Driven')
                else:
                    install_plan[order_f_d] = ['Driven']
            else:  # Default order is 0 for the pile foundation
                order_f_d = 0
                install_plan[order_f_d].append('Driven')
        if any(typ == 'gravity anchor' for typ in f_type_list) or any(typ == 'gravity foundation' for typ in f_type_list):
            # Consider the order defined by the user if any
            if any(typ == 'Gravity' for typ in po_type_list):
                order_f_g = phase_order['Default Order'].ix['Gravity']
                if order_f_g in install_plan:
                    install_plan[order_f_g].append('Gravity')
                else:
                    install_plan[order_f_g] = ['Gravity']
            else:  # Default order is 0 for the gravity based stucture
                order_f_g = 0
                install_plan[order_f_g].append('Gravity')
        if any(typ == 'drag' for typ in f_type_list) or any(typ == 'drag-embedment anchor' for typ in f_type_list):
            # Consider the order defined by the user if any
            if any(typ == 'M_drag' for typ in po_type_list):
                order_m_drag = phase_order['Default Order'].ix['M_drag']
                if order_m_drag in install_plan:
                    install_plan[order_m_drag].append('M_drag')
                else:
                    install_plan[order_m_drag] = ['M_drag']
            else:  # Default order is 0 for the drag-embedment anchor
                order_m_drag = 0
                install_plan[order_m_drag].append('M_drag')
        if any(typ == 'direct' for typ in f_type_list) or any(typ == 'direct-embedment anchor' for typ in f_type_list):
            # Consider the order defined by the user if any
            if any(typ == 'M_direct' for typ in po_type_list):
                order_m_direct = phase_order['Default Order'].ix['M_direct']
                if order_m_direct in install_plan:
                    install_plan[order_m_direct].append('M_direct')
                else:
                    install_plan[order_m_direct] = ['M_direct']
            else:  # Default order is 0 for the direct-embedment anchor
                order_m_direct = 0
                install_plan[order_m_direct].append('M_direct')
        if any(typ == 'suction caisson' for typ in f_type_list) or any(typ == 'suction caisson anchor' for typ in f_type_list):
            # Consider the order defined by the user if any
            if any(typ == 'M_suction' for typ in po_type_list):
                order_m_suct = phase_order['Default Order'].ix['M_suction']
                if order_m_suct in install_plan:
                    install_plan[order_m_suct].append('M_suction')
                else:
                    install_plan[order_m_suct] = ['M_suction']
            else:  # Default order is 0 for the suction anchor
                order_m_suct = 0
                install_plan[order_m_suct].append('M_suction')
        order_mf = max(order_f_d, order_m_d, order_f_g, order_m_drag,
                       order_m_direct, order_m_suct)
    else:  # No foundations/moorings installation considered
        install_plan[0] = []
        order_mf = 0

    # 2- Electrical infrastructure and devices installtion order follows some
    # default rules unless the order was specified by the user in phase_order
    # Static cables installation
    # Extract relevant list from panda dataframes
    sc_type_list = static_cable['type [-]'].tolist()  # static cable type
    cp_type_list = collection_point['type [-]'].tolist()  # collection point type
    cp_uei_list = collection_point['upstream ei type [-]'].tolist()  # upstream ei type of cp
    # Indexes of collection point of seabed type
    cp_seabed_id = indices(cp_type_list, lambda x: x == 'seabed')
    # Extract and desaggregate upstream connector type of corresponding to a seabed collection point
    cp_uei_seabed_list = [cp_uei_list[cp_id] for cp_id in cp_seabed_id]
    # Export static cable and surface piercing collection point installation
#    if len(static_cable) > 0:
    if not (1 in install_plan):
        install_plan[1] = []
    # Collection point installation
    # installation of surface piecing collection point
    if len(collection_point) > 0 and any(typ == 'surface piercing' for typ in cp_type_list):
        # Consider the order defined by the user if any
        if any(typ == 'E_cp_surface' for typ in po_type_list):
            order_cp_su = phase_order['Default Order'].ix['E_cp_surface']
            if order_cp_su in install_plan:
                install_plan[order_cp_su].append('E_cp_surface')
            else:
                install_plan[order_cp_su] = ['E_cp_surface']
        else:  # cp surface piercing always installed before cables
            order_cp_su = order_mf
            install_plan[order_cp_su].append('E_cp_surface')
        if len(static_cable) > 0 and (any(typ == 'export' for typ in sc_type_list) or any(typ == 'array' for typ in sc_type_list)):
            # Extract list of upstream termination type and ei type
            sc_ut_list = static_cable['upstream termination type [-]'].tolist()
            sc_utei_list = static_cable['upstream ei type [-]'].tolist()
            # Indexes of static cable with colletion point as upstream termination type
            sc_ut_id = indices(sc_ut_list, lambda x: x == 'collection point')
            # Consider the order defined by the user if any
            if any(typ == 'E_export' for typ in po_type_list):
                order_e_exp = phase_order['Default Order'].ix['E_export']
                if order_e_exp in install_plan:
                    install_plan[order_e_exp].append('E_export')
                else:
                    install_plan[order_e_exp] = ['E_export']
            # Consider the order defined by the user if any
            if any(typ == 'E_array' for typ in po_type_list):
                order_e_ar = phase_order['Default Order'].ix['E_array']
                if order_e_ar in install_plan:
                    install_plan[order_e_ar].append('E_array')
                else:
                    install_plan[order_e_ar] = ['E_array']
            # Check if there is device as upstream termination and if
            # there are devices to be considered for installation
            if 'device' in sc_ut_list:
                # Get the indices of the device and j-tube from static_cable
                dev_ut_id = indices(sc_ut_list, lambda x: x == 'device')
                jtub_ut_id = indices(sc_utei_list, lambda x: x == 'j-tube')
                if len(layout) > 0:
                    # Consider the order defined by the user if any
                    if any(typ == 'Devices' for typ in po_type_list):
                        order_dev = phase_order['Default Order'].ix['Devices']
                        if order_dev in install_plan:
                            install_plan[order_dev].append('Devices')
                        else:
                            install_plan[order_dev] = ['Devices']
                        if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                            order_e_exp = max(order_cp_su, order_dev) + 1 
                            install_plan[order_e_exp].append('E_export')
                        if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                            order_e_ar = max(order_cp_su, order_dev) + 1 
                            install_plan[order_e_ar].append('E_array')
                    # Check if there is any j-tube termination type
                    # and check if there are j-tube linked to a device
                    elif len(jtub_ut_id) > 0 and comp(dev_ut_id, jtub_ut_id):
                            # Device must be installed before static cables
                            order_dev = 1
                            install_plan[order_dev].append('Devices')
                            if not (order_dev + 1 in install_plan):
                                install_plan[order_dev + 1] = []
                            if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                order_e_exp = max(order_cp_su, order_dev) + 1 
                                install_plan[order_e_exp].append('E_export')
                            if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                order_e_ar = max(order_cp_su, order_dev) + 1 
                                install_plan[order_e_ar].append('E_array')
                    else:
                        order_dev = order_cp_su + 2
                        if not (order_dev - 1 in install_plan):
                            install_plan[order_dev - 1] = []
                        if not (order_dev in install_plan):
                            install_plan[order_dev] = []
                        install_plan[order_dev].append('Devices')
                        if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                            order_e_exp = order_dev - 1
                            install_plan[order_e_exp].append('E_export')
                        if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                            order_e_ar = order_dev - 1
                            install_plan[order_e_ar].append('E_array')
                else:
                    if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                        order_e_exp = order_cp_su + 1
                        if not (order_e_exp in install_plan):
                            install_plan[order_e_exp] = ['E_export']
                        else:
                            install_plan[order_e_exp].append('E_export')
                    if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                        order_e_ar = order_cp_su + 1
                        if not (order_e_ar in install_plan):
                            install_plan[order_e_ar] = ['E_array']
                        else:
                            install_plan[order_e_exp].append('E_array')     
            # Check if there is dynamic cable as upstream termination and if
            # there are dynamic cables to be considered for installation
            elif 'dynamic cable' in sc_ut_list: 
                # Get the indices of the dynamic cable and j-tube from static_cable
                dc_ut_id = indices(sc_ut_list, lambda x: x == 'dynamic cable')
                jtub_ut_id = indices(sc_utei_list, lambda x: x == 'j-tube')
                if len(dynamic_cable) > 0:
                    # Consider the order defined by the user if any
                    if any(typ == 'E_dynamic' for typ in po_type_list):
                        order_dc = phase_order['Default Order'].ix['E_dynamic']
                        if order_dc in install_plan:
                            install_plan[order_dc].append('E_dynamic')
                        else:
                            install_plan[order_dc] = ['E_dynamic']
                        if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                            order_e_exp = order_dc - 1
                            install_plan[order_e_exp].append('E_export')
                        if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                            order_e_ar = order_dc - 1
                            install_plan[order_e_ar].append('E_array')
                    # Check if there is any j-tube termination type
                    # and check if there are j-tube linked to a dynamic cable
                    elif len(jtub_ut_id) > 0 and comp(dc_ut_id, jtub_ut_id):
                        # Dynamic cable must be installed before static cables
                        order_dc = 1
                        if not (order_dc in install_plan):
                            install_plan[order_dc] = ['E_dynamic']
                        else:
                            install_plan[order_dc].append('E_dynamic')
                        if not (order_dc + 1 in install_plan):
                            install_plan[order_dc + 1] = []
                        if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                            order_e_exp = max(order_cp_su, order_dc) + 1 
                            install_plan[order_e_exp].append('E_export')
                        if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                            order_e_ar = max(order_cp_su, order_dc) + 1 
                            install_plan[order_e_ar].append('E_array')
                    else:
                        order_dc = order_cp_su + 2
                        if not (order_dc - 1 in install_plan):
                            install_plan[order_dc - 1] = []
                        if not (order_dc in install_plan):
                            install_plan[order_dc] = []
                        install_plan[order_dc].append('E_dynamic')
                        if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                            order_e_exp = order_dc - 1
                            install_plan[order_e_exp].append('E_export')
                        if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                            order_e_ar = order_dc - 1
                            install_plan[order_e_ar].append('E_array')
                else:
                    if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                        order_e_exp = order_cp_su + 1
                        if not (order_e_exp in install_plan):
                            install_plan[order_e_exp] = ['E_export']
                        else:
                            install_plan[order_e_exp].append('E_export')
                    if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                        order_e_ar = order_cp_su + 1
                        if not (order_e_ar in install_plan):
                            install_plan[order_e_ar] = ['E_array']
                        else:
                            install_plan[order_e_exp].append('E_array')
            if all(sc_ut_list[scut_id] == 'collection point' for scut_id in range(len(sc_ut_list))):
                if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                    order_e_exp = order_cp_su + 1
                    if not (order_e_exp in install_plan):
                        install_plan[order_e_exp] = ['E_export']
                    else:
                        install_plan[order_e_exp].append('E_export')
                if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                    order_e_ar = order_cp_su + 1
                    if not (order_e_ar in install_plan):
                        install_plan[order_e_ar] = ['E_array']
                    else:
                        install_plan[order_e_exp].append('E_array')       
    # installation of seabed mounted collection point
    elif len(collection_point) > 0 and any(typ == 'seabed' for typ in cp_type_list):
        # Consider the order defined by the user if any
        if any(typ == 'E_cp_seabed' for typ in po_type_list):
            order_cp_sb = phase_order['Default Order'].ix['E_cp_surface']
            if order_cp_sb in install_plan:
                install_plan[order_cp_sb].append('E_cp_surface')
            else:
                install_plan[order_cp_sb] = ['E_cp_surface']
            if len(static_cable) > 0 and (any(typ == 'export' for typ in sc_type_list) or any(typ == 'array' for typ in sc_type_list)):
                # Extract list of upstream termination type and ei type
                sc_ut_list = static_cable['upstream termination type [-]'].tolist()
                sc_utei_list = static_cable['upstream ei type [-]'].tolist()
                # Indexes of static cable with colletion point as upstream termination type
                sc_ut_id = indices(sc_ut_list, lambda x: x == 'collection point')
                # Consider the order defined by the user if any
                if any(typ == 'E_export' for typ in po_type_list) and not ('order_e_exp' in locals()):
                    order_e_exp = phase_order['Default Order'].ix['E_export']
                    if order_e_exp in install_plan:
                        install_plan[order_e_exp].append('E_export')
                    else:
                        install_plan[order_e_exp] = ['E_export']
                # Consider the order defined by the user if any
                if any(typ == 'E_array' for typ in po_type_list) and not ('order_e_ar' in locals()):
                    order_e_ar = phase_order['Default Order'].ix['E_array']
                    if order_e_ar in install_plan:
                        install_plan[order_e_ar].append('E_array')
                    else:
                        install_plan[order_e_ar] = ['E_array']
                # Check if there is device as upstream termination and if
                # there are devices to be considered for installation
                if 'device' in sc_ut_list:
                    # Get the indices of the device and j-tube from static_cable
                    dev_ut_id = indices(sc_ut_list, lambda x: x == 'Devices')
                    jtub_ut_id = indices(sc_utei_list, lambda x: x == 'j-tube')
                    if len(layout) > 0:
                        # Consider the order defined by the user if any
                        if any(typ == 'Devices' for typ in po_type_list) and not ('order_dev' in locals()):
                            order_dev = phase_order['Default Order'].ix['Devices']
                            if order_dev in install_plan:
                                install_plan[order_dev].append('Devices')
                            else:
                                install_plan[order_dev] = ['Devices']
                            if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                order_e_exp = max(order_cp_sb, order_dev) + 1 
                                install_plan[order_e_exp].append('E_export')
                            if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                order_e_ar = max(order_cp_sb, order_dev) + 1 
                                install_plan[order_e_ar].append('E_array')
                        # Check if there is any j-tube termination type
                        # and check if there are j-tube linked to a device
                        elif len(jtub_ut_id) > 0 and comp(dev_ut_id, jtub_ut_id):
                                # Device must be installed before static cables
                                order_dev = 1
                                install_plan[order_dev].append('Devices')
                                if not (order_dev + 1 in install_plan):
                                    install_plan[order_dev + 1] = []
                                if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                    order_e_exp = max(order_cp_sb, order_dev) + 1 
                                    install_plan[order_e_exp].append('E_export')
                                if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                    order_e_ar = max(order_cp_sb, order_dev) + 1 
                                    install_plan[order_e_ar].append('E_array')
                        else:
                            order_dev = order_cp_sb + 2
                            if not (order_dev - 1 in install_plan):
                                install_plan[order_dev - 1] = []
                            if not (order_dev in install_plan):
                                install_plan[order_dev] = []
                            install_plan[order_dev].append('Devices')
                            if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                order_e_exp = order_dev - 1
                                install_plan[order_e_exp].append('E_export')
                            if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                order_e_ar = order_dev - 1
                                install_plan[order_e_ar].append('E_array')
                    else:
                        if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                            order_e_exp = order_cp_sb + 1
                            if not (order_e_exp in install_plan):
                                install_plan[order_e_exp] = ['E_export']
                            else:
                                install_plan[order_e_exp].append('E_export')
                        if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                            order_e_ar = order_cp_sb + 1
                            if not (order_e_ar in install_plan):
                                install_plan[order_e_ar] = ['E_array']
                            else:
                                install_plan[order_e_exp].append('E_array') 
                # Check if there is dynamic cable as upstream termination and if
                # there are dynamic cables to be considered for installation
                elif 'dynamic cable' in sc_ut_list: 
                    # Get the indices of the dynamic cable and j-tube from static_cable
                    dc_ut_id = indices(sc_ut_list, lambda x: x == 'dynamic cable')
                    jtub_ut_id = indices(sc_utei_list, lambda x: x == 'j-tube')
                    if len(dynamic_cable) > 0:
                        # Consider the order defined by the user if any
                        if any(typ == 'E_dynamic' for typ in po_type_list):
                            order_dc = phase_order['Default Order'].ix['E_dynamic']
                            if order_dc in install_plan:
                                install_plan[order_dc].append('E_dynamic')
                            else:
                                install_plan[order_dc] = ['E_dynamic']
                            if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                order_e_exp = order_dc - 1
                                install_plan[order_e_exp].append('E_export')
                            if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                order_e_ar = order_dc - 1
                                install_plan[order_e_ar].append('E_array')
                        # Check if there is any j-tube termination type
                        # and check if there are j-tube linked to a dynamic cable
                        elif len(jtub_ut_id) > 0 and comp(dc_ut_id, jtub_ut_id):
                            # Dynamic cable must be installed before static cables
                            order_dc = 1
                            if order_dc in install_plan:
                                install_plan[order_dc].append('E_dynamic')
                            else:
                                install_plan[order_dc] = ['E_dynamic']
                            if not (order_dc + 1 in install_plan):
                                install_plan[order_dc + 1] = []
                            if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                order_e_exp = max(order_cp_sb, order_dc) + 1 
                                install_plan[order_e_exp].append('E_export')
                            if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                order_e_ar = max(order_cp_sb, order_dc) + 1 
                                install_plan[order_e_ar].append('E_array')
                        else:
                            order_dc = order_cp_sb + 2
                            if not (order_dc - 1 in install_plan):
                                install_plan[order_dc - 1] = []
                            if not (order_dc in install_plan):
                                install_plan[order_dc] = []
                            install_plan[order_dc].append('E_dynamic')
                            if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                order_e_exp = order_dc - 1
                                install_plan[order_e_exp].append('E_export')
                            if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                order_e_ar = order_dc - 1
                                install_plan[order_e_ar].append('E_array')
                    else:
                        if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                            order_e_exp = order_cp_sb + 1
                            if not (order_e_exp in install_plan):
                                install_plan[order_e_exp] = ['E_export']
                            else:
                                install_plan[order_e_exp].append('E_export')
                        if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                            order_e_ar = order_cp_sb + 1
                            if not (order_e_ar in install_plan):
                                install_plan[order_e_ar] = ['E_array']
                            else:
                                install_plan[order_e_exp].append('E_array')
                if all(sc_ut_list[scut_id] == 'collection point' for scut_id in range(len(sc_ut_list))):
                    if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                        order_e_exp = order_cp_sb + 1
                        if not (order_e_exp in install_plan):
                            install_plan[order_e_exp] = ['E_export']
                        else:
                            install_plan[order_e_exp].append('E_export')
                    if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                        order_e_ar = order_cp_sb + 1
                        if not (order_e_ar in install_plan):
                            install_plan[order_e_ar] = ['E_array']
                        else:
                            install_plan[order_e_exp].append('E_array')
        # cp seabed always installed before cables if all wet-mate connections
        #elif all(cp_uei_list[cpsb_id] == 'wet-mate' or cp_uei_list[cpsb_id] == ['wet-mate','wet-mate'] for cpsb_id in cp_seabed_id):   
        elif not(any(cp_uei_list[cpsb_id].find('j-tube') > 0 for cpsb_id in cp_seabed_id) or any(cp_uei_list[cpsb_id].find('dry-mate') > 0 for cpsb_id in cp_seabed_id)):
            order_cp_sb = order_mf
            install_plan[order_cp_sb].append('E_cp_seabed')
            if len(static_cable) > 0 and (any(typ == 'export' for typ in sc_type_list) or any(typ == 'array' for typ in sc_type_list)):
                # Extract list of upstream termination type and ei type
                sc_ut_list = static_cable['upstream termination type [-]'].tolist()
                sc_utei_list = static_cable['upstream ei type [-]'].tolist()
                # Indexes of static cable with colletion point as upstream termination type
                sc_ut_id = indices(sc_ut_list, lambda x: x == 'collection point')
                # Consider the order defined by the user if any
                if any(typ == 'E_export' for typ in po_type_list) and not ('order_e_exp' in locals()):
                    order_e_exp = phase_order['Default Order'].ix['E_export']
                    if order_e_exp in install_plan:
                        install_plan[order_e_exp].append('E_export')
                    else:
                        install_plan[order_e_exp] = ['E_export']
                # Consider the order defined by the user if any
                if any(typ == 'E_array' for typ in po_type_list) and not ('order_e_ar' in locals()):
                    order_e_ar = phase_order['Default Order'].ix['E_array']
                    if order_e_ar in install_plan:
                        install_plan[order_e_ar].append('E_array')
                    else:
                        install_plan[order_e_ar] = ['E_array']
                # Check if there is device as upstream termination and if
                # there are devices to be considered for installation
                if 'device' in sc_ut_list:
                    # Get the indices of the device and j-tube from static_cable
                    dev_ut_id = indices(sc_ut_list, lambda x: x == 'device')
                    jtub_ut_id = indices(sc_utei_list, lambda x: x == 'j-tube')
                    if len(layout) > 0:
                        # Consider the order defined by the user if any
                        if any(typ == 'Devices' for typ in po_type_list) and not ('order_dev' in locals()):
                            order_dev = phase_order['Default Order'].ix['Devices']
                            if order_dev in install_plan:
                                install_plan[order_dev].append('Devices')
                            else:
                                install_plan[order_dev] = ['Devices']
                            if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                order_e_exp = max(order_cp_sb, order_dev) + 1 
                                install_plan[order_e_exp].append('E_export')
                            if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                order_e_ar = max(order_cp_sb, order_dev) + 1 
                                install_plan[order_e_ar].append('E_array')
                        # Check if there is any j-tube termination type
                        # and check if there are j-tube linked to a device
                        elif len(jtub_ut_id) > 0 and comp(dev_ut_id, jtub_ut_id):
                                # Device must be installed before static cables
                                order_dev = 1
                                install_plan[order_dev].append('Devices')
                                if not (order_dev + 1 in install_plan):
                                    install_plan[order_dev + 1] = []
                                if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                    order_e_exp = max(order_cp_sb, order_dev) + 1 
                                    install_plan[order_e_exp].append('E_export')
                                if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                    order_e_ar = max(order_cp_sb, order_dev) + 1 
                                    install_plan[order_e_ar].append('E_array')
                        else:
                            order_dev = order_cp_sb + 2
                            if not (order_dev - 1 in install_plan):
                                install_plan[order_dev - 1] = []
                            if not (order_dev in install_plan):
                                install_plan[order_dev] = []
                            install_plan[order_dev].append('Devices')
                            if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                order_e_exp = order_dev - 1
                                install_plan[order_e_exp].append('E_export')
                            if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                order_e_ar = order_dev - 1
                                install_plan[order_e_ar].append('E_array')
                    else:
                        if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                            order_e_exp = order_cp_sb + 1
                            if not (order_e_exp in install_plan):
                                install_plan[order_e_exp] = ['E_export']
                            else:
                                install_plan[order_e_exp].append('E_export')
                        if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                            order_e_ar = order_cp_sb + 1
                            if not (order_e_ar in install_plan):
                                install_plan[order_e_ar] = ['E_array']
                            else:
                                install_plan[order_e_exp].append('E_array') 
                # Check if there is dynamic cable as upstream termination and if
                # there are dynamic cables to be considered for installation
                elif 'dynamic cable' in sc_ut_list:  
                    # Get the indices of the dynamic cable and j-tube from static_cable
                    dc_ut_id = indices(sc_ut_list, lambda x: x == 'dynamic cable')
                    jtub_ut_id = indices(sc_utei_list, lambda x: x == 'j-tube')
                    if len(dynamic_cable) > 0:
                        # Consider the order defined by the user if any
                        if any(typ == 'E_dynamic' for typ in po_type_list):
                            order_dc = phase_order['Default Order'].ix['E_dynamic']
                            if not (order_dc - 1 in install_plan):
                                install_plan[order_dc - 1] = []
                            if order_dc in install_plan:
                                install_plan[order_dc].append('E_dynamic')
                            else:
                                install_plan[order_dc] = ['E_dynamic']
                            if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                order_e_exp = order_dc - 1
                                install_plan[order_e_exp].append('E_export')
                            if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                order_e_ar = order_dc - 1
                                install_plan[order_e_ar].append('E_array')
                        # Check if there is any j-tube termination type
                        # and check if there are j-tube linked to a dynamic cable
                        elif len(jtub_ut_id) > 0 and comp(dc_ut_id, jtub_ut_id):
                            # Dynamic cable must be installed before static cables
                            order_dc = 1
                            if order_dc in install_plan:
                                install_plan[order_dc].append('E_dynamic')
                            else:
                                install_plan[order_dc] = ['E_dynamic']
                            if not (order_dc + 1 in install_plan):
                                install_plan[order_dc + 1] = []
                            if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                order_e_exp = max(order_cp_sb, order_dc) + 1
                                if not (order_e_exp in install_plan):
                                    install_plan[order_e_exp] = ['E_export']
                                else:
                                    install_plan[order_e_exp].append('E_export')
                            if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                order_e_ar = max(order_cp_sb, order_dc) + 1 
                                if not (order_e_ar in install_plan):
                                    install_plan[order_e_ar] = ['E_array']
                                else:
                                    install_plan[order_e_exp].append('E_array')
                        else:
                            order_dc = order_cp_sb + 2
                            if not (order_dc - 1 in install_plan):
                                install_plan[order_dc - 1] = []
                            if not (order_dc in install_plan):
                                install_plan[order_dc] = []
                            install_plan[order_dc].append('E_dynamic')
                            if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                order_e_exp = order_dc - 1
                                install_plan[order_e_exp].append('E_export')
                            if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                order_e_ar = order_dc - 1
                                install_plan[order_e_ar].append('E_array')
                    else:
                        if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                            order_e_exp = order_cp_sb + 1
                            if not (order_e_exp in install_plan):
                                install_plan[order_e_exp] = ['E_export']
                            else:
                                install_plan[order_e_exp].append('E_export')
                        if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                            order_e_ar = order_cp_sb + 1
                            if not (order_e_ar in install_plan):
                                install_plan[order_e_ar] = ['E_array']
                            else:
                                install_plan[order_e_exp].append('E_array')
                if all(sc_ut_list[scut_id] == 'collection point' for scut_id in range(len(sc_ut_list))):
                    if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                        order_e_exp = order_cp_sb + 1
                        if not (order_e_exp in install_plan):
                            install_plan[order_e_exp] = ['E_export']
                        else:
                            install_plan[order_e_exp].append('E_export')
                    if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                        order_e_ar = order_cp_sb + 1
                        if not (order_e_ar in install_plan):
                            install_plan[order_e_ar] = ['E_array']
                        else:
                            install_plan[order_e_exp].append('E_array')
        # if not all wet-mate connectors collection point to be installed 
        # after cables
        else:  
            if len(static_cable) > 0 and (any(typ == 'export' for typ in sc_type_list) or any(typ == 'array' for typ in sc_type_list)):
                # Extract list of upstream termination type and ei type
                sc_ut_list = static_cable['upstream termination type [-]'].tolist()
                sc_utei_list = static_cable['upstream ei type [-]'].tolist()
                # Indexes of static cable with colletion point as upstream termination type
                sc_ut_id = indices(sc_ut_list, lambda x: x == 'collection point')
                # Consider the order defined by the user if any
                if any(typ == 'E_export' for typ in po_type_list) and not ('order_e_exp' in locals()):
                    order_e_exp = phase_order['Default Order'].ix['E_export']
                    if order_e_exp in install_plan:
                        install_plan[order_e_exp].append('E_export')
                    else:
                        install_plan[order_e_exp] = ['E_export']
                # Consider the order defined by the user if any
                if any(typ == 'E_array' for typ in po_type_list) and not ('order_e_ar' in locals()):
                    order_e_ar = phase_order['Default Order'].ix['E_array']
                    if order_e_ar in install_plan:
                        install_plan[order_e_ar].append('E_array')
                    else:
                        install_plan[order_e_ar] = ['E_array']
                # Check if there is device as upstream termination and if
                # there are devices to be considered for installation
                if 'device' in sc_ut_list:
                    # Get the indices of the device and j-tube from static_cable
                    dev_ut_id = indices(sc_ut_list, lambda x: x == 'device')
                    jtub_ut_id = indices(sc_utei_list, lambda x: x == 'j-tube')
                    if len(layout) > 0: # there are devices to install
                        # Consider the order defined by the user if any
                        if any(typ == 'Devices' for typ in po_type_list) and not ('order_dev' in locals()):
                            order_dev = phase_order['Default Order'].ix['Devices']
                            if order_dev in install_plan:
                                install_plan[order_dev].append('Devices')
                            else:
                                install_plan[order_dev] = ['Devices']
                            if not (order_dev + 1 in install_plan):
                                    install_plan[order_dev + 1] = []
                            if not (order_dev + 2 in install_plan):
                                order_cp_sb = order_dev + 2
                                install_plan[order_cp_sb] = ['E_cp_seabed']
                            else:
                                order_cp_sb = order_dev + 2
                                install_plan[order_cp_sb].append(['E_cp_seabed'])
                            if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                order_e_exp = order_dev + 1
                                install_plan[order_e_exp].append('E_export')
                            if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                order_e_ar = order_dev + 1
                                install_plan[order_e_ar].append('E_array')
                        # Check if there is any j-tube termination type
                        elif len(jtub_ut_id) > 0:
                            # Check if there are j-tube linked to a device
                            if comp(dev_ut_id, jtub_ut_id):
                                # Device must be installed before static cables
                                if not ('order_dev' in locals()):
                                    order_dev = 1
                                    install_plan[order_dev].append('Devices')
                                if not (order_dev + 1 in install_plan):
                                    install_plan[order_dev + 1] = []
                                if not (order_dev + 2 in install_plan):
                                    order_cp_sb = order_dev + 2
                                    install_plan[order_cp_sb] = ['E_cp_seabed']
                                else:
                                    order_cp_sb = order_dev + 2
                                    install_plan[order_cp_sb].append(['E_cp_seabed'])
                                if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                    order_e_exp = order_dev + 1
                                    install_plan[order_e_exp].append('E_export')
                                if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                    order_e_ar = order_dev + 1
                                    install_plan[order_e_ar].append('E_array')
                            else:
                                if not ('order_dev' in locals()):
                                    if not ('order_e_exp' in locals()):
                                        order_e_exp = 0
                                    if not ('order_e_ar' in locals()):
                                        order_e_ar = 0
                                    order_cp_sb = max(order_e_exp, order_e_ar,1) + 1
                                    order_dev = order_cp_sb + 2
                                    if not (order_dev in install_plan):
                                        install_plan[order_dev] = ['Devices']
                                    else:
                                        install_plan[order_dev].append('Devices')
                                if not (order_dev - 1 in install_plan):
                                    install_plan[order_dev - 1] = []
                                if not (order_dev in install_plan):
                                    install_plan[order_dev] = []
                                if not (order_cp_sb in install_plan):
                                    install_plan[order_cp_sb] = ['E_cp_seabed']
                                else:
                                    install_plan[order_cp_sb].append(['E_cp_seabed'])
                                if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                    order_e_exp = order_dev - 1
                                    install_plan[order_e_exp].append('E_export')
                                if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                    order_e_ar = order_dev - 1
                                    install_plan[order_e_ar].append('E_array')
                        else:  # device installation after cables if no j-tube
                            if not ('order_dev' in locals()):
                                order_dev = 2
                                if not (order_dev in install_plan):
                                    install_plan[order_dev] = ['Devices']
                                else:
                                    install_plan[order_dev].append('Devices')
                            if not (order_dev - 1 in install_plan):
                                install_plan[order_dev - 1] = []
                            if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                order_e_exp = order_dev - 1
                                install_plan[order_e_exp].append('E_export')
                            if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                order_e_ar = order_dev - 1
                                install_plan[order_e_ar].append('E_array') 
                        if not ('order_e_cp_sb' in locals()):
                            if not ('order_e_exp' in locals()):
                                order_e_exp = 0
                            if not ('order_e_ar' in locals()):
                                order_e_ar = 0
                            if not ('order_e_exp' in locals()):
                                order_e_exp = 0
                            if not ('order_dev' in locals()):
                                order_dev = 0
                            order_cp_sb = max(order_e_exp, order_e_ar,order_dev - 1, 1) + 1
                            if not (order_cp_sb in install_plan):
                                install_plan[order_cp_sb] = ['E_cp_seabed']
                            else:
                                install_plan[order_cp_sb].append('E_cp_seabed')
                    else: # no devices but may be other electrical component
                        order_cp_sb = order_mf
                        if not (order_cp_sb in install_plan):
                            install_plan[order_cp_sb] = ['E_cp_seabed']
                        else:
                            install_plan[order_cp_sb].append('E_cp_seabed')
                        if not (order_mf + 1 in install_plan):
                            install_plan[order_mf + 1] = []
                        if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                            order_e_exp = order_mf + 1
                            install_plan[order_e_exp].append('E_export')
                        if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                            order_e_ar = order_mf + 1
                            install_plan[order_e_ar].append('E_array')
                # Check if there is dynamic cable as upstream termination and if
                # there are dynamic cables to be considered for installation
                if 'dynamic cable' in sc_ut_list:
                    # Get the indices of the dynamic cable and j-tube from static_cable
                    dc_ut_id = indices(sc_ut_list, lambda x: x == 'dynamic cabe')
                    jtub_ut_id = indices(sc_utei_list, lambda x: x == 'j-tube')
                    if len(dynamic_cable) > 0:
                        # Consider the order defined by the user if any
                        if any(typ == 'E_dynamic' for typ in po_type_list) and not ('order_dc' in locals()):
                            order_dc = phase_order['Default Order'].ix['E_dynamic']
                            if order_dc in install_plan:
                                install_plan[order_dc].append('E_dynamic')
                            else:
                                install_plan[order_dc] = ['E_dynamic']
                            if not (order_dc - 1 in install_plan):
                                    install_plan[order_dc - 1] = []
                            if not (order_dc - 2 in install_plan):
                                order_cp_sb = order_dc - 2
                                install_plan[order_cp_sb] = ['E_cp_seabed']
                            else:
                                order_cp_sb = order_dc - 2
                                install_plan[order_cp_sb].append(['E_cp_seabed'])
                            if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                order_e_exp = order_dc - 1
                                install_plan[order_e_exp].append('E_export')
                            if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                order_e_ar = order_dc - 1
                                install_plan[order_e_ar].append('E_array')
                        # Check if there is any j-tube termination type
                        elif len(jtub_ut_id) > 0:
                            # Check if there are j-tube linked to a dynamic cable
                            if comp(dc_ut_id, jtub_ut_id):
                                # Dynamic cable must be installed before static cables
                                if not ('order_dc' in locals()):
                                    order_dc = 1
                                    if order_dc in install_plan:
                                        install_plan[order_dc].append('E_dynamic')
                                    else:
                                        install_plan[order_dc] = ['E_dynamic']
                                if not (order_dev + 1 in install_plan):
                                    install_plan[order_dc + 1] = []
                                if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                    order_e_exp = order_dc + 1
                                    install_plan[order_e_exp].append('E_export')
                                if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                    order_e_ar = order_dc + 1
                                    install_plan[order_e_ar].append('E_array')
                            else:
                                if not ('order_dc' in locals()):
                                    if not ('order_e_exp' in locals()):
                                        order_e_exp = 0
                                    if not ('order_e_ar' in locals()):
                                        order_e_ar = 0
                                    order_cp_sb = max(order_e_exp, order_e_ar,1) + 1
                                    order_dc = order_cp_sb + 2
                                    if order_dc in install_plan:
                                        install_plan[order_dc].append('E_dynamic')
                                    else:
                                        install_plan[order_dc] = ['E_dynamic']
                                if not (order_dc - 1 in install_plan):
                                    install_plan[order_dc - 1] = []
                                if not (order_dc in install_plan):
                                    install_plan[order_dc] = []
                                if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                    order_e_exp = order_dc - 1
                                    install_plan[order_e_exp].append('E_export')
                                if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                    order_e_ar = order_dc - 1
                                    install_plan[order_e_ar].append('E_array')
                        else:  # dynamic cable installation after cables if no j-tube
                            if not ('order_dc' in locals()):
                                order_dc = 2
                                if order_dc in install_plan:
                                    install_plan[order_dc].append('E_dynamic')
                                else:
                                    install_plan[order_dc] = ['E_dynamic']
                            if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                                order_e_exp = order_dc - 1
                                install_plan[order_e_exp].append('E_export')
                            if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                                order_e_ar = order_dc - 1
                                install_plan[order_e_ar].append('E_array') 
                        if not ('order_e_cp_sb' in locals()):
                            if not ('order_e_exp' in locals()):
                                order_e_exp = 0
                            if not ('order_e_ar' in locals()):
                                order_e_ar = 0
                            if not ('order_e_exp' in locals()):
                                order_e_exp = 0
                            if not ('order_dev' in locals()):
                                order_dc = 0
                            order_cp_sb = max(order_e_exp, order_e_ar,order_dc - 1, 1) + 1
                            if not (order_cp_sb in install_plan):
                                install_plan[order_cp_sb] = ['E_cp_seabed']
                            else:
                                install_plan[order_cp_sb].append('E_cp_seabed')
                    else:
                        if not ('order_cp_sb' in locals()):
                            order_cp_sb = order_mf
                            if not (order_cp_sb in install_plan):
                                install_plan[order_cp_sb] = ['E_cp_seabed']
                            else:
                                install_plan[order_cp_sb].append('E_cp_seabed')
                        if not (order_mf + 1 in install_plan):
                            install_plan[order_mf + 1] = []
                        if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                            order_e_exp = order_mf + 1
                            install_plan[order_e_exp].append('E_export')
                        if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                            order_e_ar = order_mf + 1
                            install_plan[order_e_ar].append('E_array')
                if all(sc_ut_list[scut_id] == 'collection point' for scut_id in range(len(sc_ut_list))):
                    if not ('order_cp_sb' in locals()):
                        order_cp_sb = order_mf
                        if not (order_cp_sb in install_plan):
                            install_plan[order_cp_sb] = ['E_cp_seabed']
                        else:
                            install_plan[order_cp_sb].append('E_cp_seabed')
                    if not (order_mf + 1 in install_plan):
                        install_plan[order_mf + 1] = []
                    if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                        order_e_exp = order_mf + 1
                        install_plan[order_e_exp].append('E_export')
                    if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                        order_e_ar = order_mf + 1
                        install_plan[order_e_ar].append('E_array')
#            order_cp_sp = 0
#            order_cp_sb = 0
#    elif len(collection_point > 0):
#        print 'unknown collection point type. Only "seabed" and "surface piercing" are recognized'
    # no collection point to be installed but may be other electrical sub-systems
    else:
        if len(static_cable) > 0 and (any(typ == 'export' for typ in sc_type_list) or any(typ == 'array' for typ in sc_type_list)):
            # Extract list of upstream termination type and ei type
            sc_ut_list = static_cable['upstream termination type [-]'].tolist()
            sc_utei_list = static_cable['upstream ei type [-]'].tolist()
            # Indexes of static cable with colletion point as upstream termination type
            sc_ut_id = indices(sc_ut_list, lambda x: x == 'collection point')
            # Consider the order defined by the user if any
            if any(typ == 'E_export' for typ in po_type_list) and not ('order_e_exp' in locals()):
                order_e_exp = phase_order['Default Order'].ix['E_export']
                if order_e_exp in install_plan:
                    install_plan[order_e_exp].append('E_export')
                else:
                    install_plan[order_e_exp] = ['E_export']
            # Consider the order defined by the user if any
            if any(typ == 'E_array' for typ in po_type_list) and not ('order_e_ar' in locals()):
                order_e_ar = phase_order['Default Order'].ix['E_array']
                if order_e_ar in install_plan:
                    install_plan[order_e_ar].append('E_array')
                else:
                    install_plan[order_e_ar] = ['E_array']
            # Check if there is device as upstream termination and if
            # there are devices to be considered for installation
            if 'device' in sc_ut_list and len(layout) > 0:
                # Get the indices of the device and j-tube from static_cable
                dev_ut_id = indices(sc_ut_list, lambda x: x == 'device')
                jtub_ut_id = indices(sc_utei_list, lambda x: x == 'j-tube')
                # Consider the order defined by the user if any
                if any(typ == 'Devices' for typ in po_type_list) and not ('order_dev' in locals()):
                    order_dev = phase_order['Default Order'].ix['Devices']
                    if order_dev in install_plan:
                        install_plan[order_dev].append('Devices')
                    else:
                        install_plan[order_dev] = ['Devices']
                # Check if there is any j-tube termination type
                elif len(jtub_ut_id) > 0:
                    # Check if there are j-tube linked to a device
                    if comp(dev_ut_id, jtub_ut_id):
                        # Device must be installed before static cables
                        if not ('order_dev' in locals()):
                            order_dev = 1
                            if order_dev in install_plan:
                                install_plan[order_dev].append('Devices')
                            else:
                                install_plan[order_dev] = ['Devices']
                        if not (order_dev + 1 in install_plan):
                            install_plan[order_dev + 1] = []
                        if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                            order_e_exp = order_dev + 1
                            install_plan[order_e_exp].append('E_export')
                        if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                            order_e_ar = order_dev + 1
                            install_plan[order_e_ar].append('E_array')
                    else:
                        if not ('order_dev' in locals()):
                            if not ('order_e_exp' in locals()):
                                order_e_exp = 0
                            if not ('order_e_ar' in locals()):
                                order_e_ar = 0
                            order_cp_sb = max(order_e_exp, order_e_ar,1) + 1
                            order_dev = order_cp_sb + 2
                            if order_dev in install_plan:
                                install_plan[order_dev].append('Devices')
                            else:
                                install_plan[order_dev] = ['Devices']
                        if not (order_dev - 1 in install_plan):
                            install_plan[order_dev - 1] = []
                        if not (order_dev in install_plan):
                            install_plan[order_dev] = []
                        if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                            order_e_exp = order_dev - 1
                            install_plan[order_e_exp].append('E_export')
                        if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                            order_e_ar = order_dev - 1
                            install_plan[order_e_ar].append('E_array')
                else:  # device installation after cables if no j-tube
                    if not ('order_dev' in locals()):
                        order_dev = 2
                        if order_dev in install_plan:
                            install_plan[order_dev].append('Devices')
                        else:
                            install_plan[order_dev] = ['Devices']
                    if not (order_dev - 1 in install_plan):
                        install_plan[order_dev - 1] = []
                    if any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
                        order_e_exp = order_dev - 1
                        install_plan[order_e_exp].append('E_export')
                    if any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
                        order_e_ar = order_dev - 1
                        install_plan[order_e_ar].append('E_array') 
                if not ('order_e_cp_sb' in locals()):
                    if not ('order_e_exp' in locals()):
                        order_e_exp = 0
                    if not ('order_e_ar' in locals()):
                        order_e_ar = 0
                    if not ('order_e_exp' in locals()):
                        order_e_exp = 0
                    if not ('order_dev' in locals()):
                        order_dev = 0
                    order_cp_sb = max(order_e_exp, order_e_ar,order_dev - 1, 1) + 1
                    if not (order_cp_sb in install_plan):
                        install_plan[order_cp_sb] = ['E_cp_seabed']
                    else:
                        install_plan[order_cp_sb].append('E_cp_seabed')
        order_cp_sp = 0
        order_cp_sb = 0   
    # Static cable installation
    if len(static_cable) > 0 and any(typ == 'export' for typ in sc_type_list) and not ('order_e_exp' in locals()):
        if any(typ == 'E_export' for typ in po_type_list):
            order_e_exp = phase_order['Default Order'].ix['E_export']
            if not (order_e_exp in install_plan):
                install_plan[order_e_exp] = ['E_export']
            else:
                install_plan[order_e_exp].append('E_export')
        else:
            if not ('order_dev' in locals()):  # static cables installed right
            # after moorings & foundations
                order_e_exp = order_mf + 1
            else:  # static cables installed right before devices
                order_e_exp = order_dev - 1
            if order_e_exp in install_plan:
                install_plan[order_e_exp].append('E_export')
            else:
                install_plan[order_e_exp] = ['E_export']
    if len(static_cable) > 0 and any(typ == 'array' for typ in sc_type_list) and not ('order_e_ar' in locals()):
        if any(typ == 'E_array' for typ in po_type_list):
            order_e_ar = phase_order['Default Order'].ix['E_array']
            if not (order_e_exp in install_plan):
                install_plan[order_e_ar] = ['E_array']
            else:
                install_plan[order_e_ar].append('E_array')
        else:
            if not ('order_dev' in locals()):  # static cables installed right
            # after moorings & foundations
                order_e_ar = order_mf + 1
            else:  # static cables installed right before devices
                order_e_ar = order_dev - 1
            if order_e_ar in install_plan:
                install_plan[order_e_ar].append('E_array')
            else:
                install_plan[order_e_ar] = ['E_array']
    # Dynamic cable installation
    if len(dynamic_cable) > 0 and not ('order_dc' in locals()):
        if any(typ == 'E_dynamic' for typ in po_type_list):
            order_dc = phase_order['Default Order'].ix['E_dynamic']
            if not (order_dc in install_plan):
                install_plan[order_dc] = ['E_dynamic']
            else:
                install_plan[order_dc].append('E_dynamic')
        else:
            if not ('order_dev' in locals()):  # dyn cables installed right
            # after moorings & foundations
                order_dc = order_mf + 1
            else:  # dynamic cables installed right before devices
                order_dc = order_dev - 1
            if order_dc in install_plan:
                install_plan[order_dc].append('E_dynamic')
            else:
                install_plan[order_dc] = ['E_dynamic']

    # Static cable extrernal protection installation
    if len(external_protection) > 0:
        if any(typ == 'E_external' for typ in po_type_list):
            order_e_ep = phase_order['Default Order'].ix['E_external']
            if not (order_e_ep in install_plan):
                install_plan[order_e_ep] = ['E_external']
            else:
                install_plan[order_e_ep].append('E_external')
        else:
            if not ('order_e_ep' in locals()):
                if not ('order_e_exp' in locals()):
                    order_e_exp = 0
                if not ('order_e_ar' in locals()):
                    order_e_ar = 0
                if not ('order_e_exp' in locals()):
                    order_e_exp = 0
                if not ('order_dev' in locals()):
                    order_dev = 0
                order_e_ep = max(order_e_exp, order_e_ar, order_dev - 1, 1) + 1
                if not (order_e_ep in install_plan):
                    install_plan[order_e_ep] = ['E_external']
                else:
                    install_plan[order_e_ep].append('E_external')
    
    if len(layout) > 0 and not ('order_dev' in locals()):
        plan_k = install_plan.keys()
        order_dev = max(plan_k) + 1
        install_plan[order_dev] = ['Devices']

    # Support structure installtion
    if len(layout) > 0 and device['assembly strategy [-]'].iloc[0] == '([A,B,C],D)':
        if any(typ == 'S_structure' for typ in po_type_list):
            order_ss = phase_order['Default Order'].ix['S_structure']
            if order_ss in install_plan:
                install_plan[order_ss].append('S_structure')
            else:
                install_plan[order_ss] = ['S_structure']
        else:
            order_ss = order_dev - 1
            if order_ss in install_plan:
                install_plan[order_ss].append('S_structure')
            else:
                install_plan[order_ss] = ['S_structure']  
    # remove empty items from dictionnary 
    install_plan = dict((k, v) for k, v in install_plan.iteritems() if v)

    return install_plan

