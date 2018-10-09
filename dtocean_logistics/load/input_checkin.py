# -*- coding: utf-8 -*-

#    Copyright (C) 2016 Boris Teillant, Paulo Chainho, Pedro Vicente
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
.. moduleauthor:: Boris Teillant <boris.teillant@wavec.org>
.. moduleauthor:: Paulo Chainho <paulo@wavec.org>
.. moduleauthor:: Pedro Vicente <pedro.vicente@wavec.org>
"""

from check_vessels import check_vess
from check_equipments import check_rov, check_divers, check_cable_burial, check_excavating, check_mattress, \
    check_rockfilterbags, check_splitpipes, check_hammer, check_drillingrigs, check_vibrodriver
from check_portsDB import check_ports

from check_user_inputs import check_site, check_metocean, check_device, check_subdevice, check_landfall, check_entry_point
from check_hydrodynamics import check_hydro
from check_MF import check_found, check_ln
from check_electrical import check_collect, check_dynamic_cable, check_static_cable, check_cable_route, check_connectors, check_external_protection, check_layout




def input_check(vessels, equipments, ports,
                site, metocean, device, sub_device, landfall, entry_point,
                layout,
                collection_point, dynamic_cable, static_cable, cable_route,
                connectors, external_protection, topology,
                line, foundation,
                PRINT_FLAG, PLOT_FLAG, PLOT_GANTT, PRINT_CSV, cvs_filename
                ):

    # default value
    ERROR_IN_INPUT = False

    # collect all warning messages rather than print
    warning_list = []

#    # Vessels databases:
#    Input_module = 'Vessels'
#    Input_DB = vessels
#    ERROR_IN_MODULE, warning_list =  check_vess(Input_DB, Input_module, warning_list)
#    if ERROR_IN_MODULE:
#        ERROR_IN_INPUT = True

    # Equipments databases:
    Input_module = 'Equipments/rov'
    Input_DB = equipments['rov'].panda
    ERROR_IN_MODULE, warning_list =  check_rov(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'Equipments/divers'
    Input_DB = equipments['divers'].panda
    ERROR_IN_MODULE, warning_list =  check_divers(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'Equipments/cable_burial'
    Input_DB = equipments['cable burial'].panda
    ERROR_IN_MODULE, warning_list =  check_cable_burial(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'Equipments/excavating'
    Input_DB = equipments['excavating'].panda
    ERROR_IN_MODULE, warning_list =  check_excavating(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'Equipments/mattress'
    Input_DB = equipments['mattress'].panda
    ERROR_IN_MODULE, warning_list =  check_mattress(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'Equipments/rockfilterbags'
    Input_DB = equipments['rock filter bags'].panda
    ERROR_IN_MODULE, warning_list =  check_rockfilterbags(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'Equipments/splitpipes'
    Input_DB = equipments['split pipe'].panda
    ERROR_IN_MODULE, warning_list =  check_splitpipes(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'Equipments/hammer'
    Input_DB = equipments['hammer'].panda
    ERROR_IN_MODULE, warning_list =  check_hammer(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'Equipments/drillingrigs'
    Input_DB = equipments['drilling rigs'].panda
    ERROR_IN_MODULE, warning_list =  check_drillingrigs(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'Equipments/vibrodriver'
    Input_DB = equipments['vibro driver'].panda
    ERROR_IN_MODULE, warning_list =  check_vibrodriver(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True


    # Ports databases:
    Input_module = 'Ports'
    Input_DB = ports
    ERROR_IN_MODULE, warning_list =  check_ports(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True

    # User inputs:
    Input_module = 'User Inputs/site'
    Input_DB = site
    ERROR_IN_MODULE, warning_list =  check_site(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'User Inputs/metocean'
    Input_DB = metocean
    ERROR_IN_MODULE, warning_list =  check_metocean(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'User Inputs/device'
    Input_DB = device
    ERROR_IN_MODULE, warning_list =  check_device(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'User Inputs/sub_device'
    Input_DB = sub_device
    ERROR_IN_MODULE, warning_list =  check_subdevice(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'User Inputs/landfall'
    Input_DB = landfall
    ERROR_IN_MODULE, warning_list =  check_landfall(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'User Inputs/entry_point'
    Input_DB = entry_point
    ERROR_IN_MODULE, warning_list =  check_entry_point(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True


    # Hydrodynamics inputs:
    Input_module = 'Hydrodynamics'
    Input_DB = layout
    ERROR_IN_MODULE, warning_list =  check_hydro(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True

    # Electrical inputs:
    Input_module = 'Electrical/collection_point'
    Input_DB = collection_point
    ERROR_IN_MODULE, warning_list =  check_collect(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'Electrical/dynamic_cable'
    Input_DB = dynamic_cable
    ERROR_IN_MODULE, warning_list =  check_dynamic_cable(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'Electrical/static_cable'
    Input_DB = static_cable
    ERROR_IN_MODULE, warning_list =  check_static_cable(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    # Input_module = 'Electrical/cable_route'
    # Input_DB = cable_route
    # ERROR_IN_MODULE, warning_list =  check_cable_route(Input_DB, Input_module, warning_list)
    # if ERROR_IN_MODULE:
    #     ERROR_IN_INPUT = True
    Input_module = 'Electrical/connectors'
    Input_DB = connectors
    ERROR_IN_MODULE, warning_list =  check_connectors(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'Electrical/external_protection'
    Input_DB = external_protection
    ERROR_IN_MODULE, warning_list =  check_external_protection(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
#    Input_module = 'Electrical/topology'
#    Input_DB = topology
#    ERROR_IN_MODULE, warning_list =  check_layout(Input_DB, Input_module, warning_list)
#    if ERROR_IN_MODULE:
#        ERROR_IN_INPUT = True

    # Moorings and Foundations inputs:
    Input_module = 'MF/line'
    Input_DB = line
    ERROR_IN_MODULE, warning_list =  check_ln(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True
    Input_module = 'MF/foundation'
    Input_DB = foundation
    ERROR_IN_MODULE, warning_list =  check_found(Input_DB, Input_module, warning_list)
    if ERROR_IN_MODULE:
        ERROR_IN_INPUT = True


    return ERROR_IN_INPUT, warning_list