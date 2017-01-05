# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module imports the WP5 databases required to run WP5 package.  All data
imported is translated to panda dataframes.

BETA VERSION NOTES: the module also aims to provide a buffer between the database
source and WP5 package, so it becomes simple to shift from the temporary .xlsx
and .csv files to the final SQL solution.
"""

import pandas as pd

from ..phases import VesselType
from ..phases import EquipmentType


def load_time_olc_data(file_path):
    """Imports olc database into a panda table

    Parameters
    ----------
    file_path : string
     the folder path of the time and olc data set

    Returns
    -------
    time_olc : dict
     dictionnary containing a panda dataframe with time duration and olc
    """
    # Transform time and olc database .xls into panda type
    excel = pd.ExcelFile(file_path)
    # Collect data from a particular tab
    time_olc = excel.parse('operations', header=0, index_col=0)

    return time_olc


def load_phase_order_data(file_path):
    """Imports phase order database into a panda table

    Parameters
    ----------
    file_path : string
     the folder path of the phase order table

    Returns
    -------
    phase_order : dict
     dictionnary containing a panda dataframe with the phase order
    """
    # Transform phase table .xls into panda type
    excel = pd.ExcelFile(file_path)
    # Collect data from a particular tab
    phase_order = excel.parse('InstallationOrder', header=0, index_col=0)

    return phase_order


def load_eq_rates(file_path):
    """Imports pile driving penetration rates and cable laying/trenching/burial
    rates into two panda tables

    Parameters
    ----------
    file_path : string
     the folder path of the phase order table

    Returns
    -------
    penet_rates : panda dataFrame table
     panda table containing the pile driving vertical penetration rates and the
     cable laying/trenching/burial horizontal progress rates
    """
    # Transform equipment performance rates table .xls into panda type
    excel = pd.ExcelFile(file_path)
    # Collect data from a particular tab
    penet_rates = excel.parse('penet', header=0, index_col=0)
    laying_rates = excel.parse('laying', header=0, index_col=0)
    other_rates = excel.parse('other', header=0, index_col=0)
    
    return penet_rates, laying_rates, other_rates


def load_sf(file_path):
    """Imports safety factors into a panda table

    Parameters
    ----------
    file_path : string
     the folder path of the phase order table

    Returns
    -------
    safety_factors : panda dataFrame table
     panda table containing the safety factors to apply on the feasiblity
     functions
    """
    # Transform equipment performance rates table .xls into panda type
    excel = pd.ExcelFile(file_path)
    # Collect data from a particular tab
    port_sf = excel.parse('port_sf', header=0, index_col=0)
    vessel_sf = excel.parse('vessel_sf', header=0, index_col=0)
    eq_sf = excel.parse('eq_sf', header=0, index_col=0)

    return port_sf, vessel_sf, eq_sf


def load_vessel_data(file_path):
    """Imports vessel database into panda dataframe and creates a class for each
    vessel type

    Parameters
    ----------
    file_path : string
     the folder path of the vessel database

    Returns
    -------
    vessels : dict
     dictionnary containing all classes defining the different vessel types
    """
    # Transform vessel database .xls into panda type
    excel = pd.ExcelFile(file_path)
    # Collect data from a particular tab
    pd_vessel = excel.parse('Python_Format', header=0, index_col=0)

    vessels_all = pd_vessel
    # Splits the pd_vessel object with the full dataset, into smaller panda objects with specific vessel types now done in the safe_factors function!!

    return vessels_all


def load_equipment_data(file_path):
    """Imports equipment database into panda dataframe and creates a class for
    each equipment type

    Parameters
    ----------
    file_path : string
     the folder path of the equipment database

    Returns
    -------
    vessels : dict
     dictionnary containing all classes defining the different equipment types
    """

    # Transform Equipment database .xls into panda type
    excel = pd.ExcelFile(file_path)

    # Collect data from a particular tab
    rov = excel.parse('rov', header=0, index_col=0)
    divers = excel.parse('divers', header=0, index_col=0)
    cable_burial = excel.parse('cable_burial', header=0, index_col=0)
    excavating = excel.parse('excavating', header=0, index_col=0)
    mattress = excel.parse('mattress', header=0, index_col=0)
    rock_filter_bags = excel.parse('rock_filter_bags', header=0, index_col=0)
    split_pipe = excel.parse('split_pipe', header=0, index_col=0)
    hammer = excel.parse('hammer', header=0, index_col=0)
    drilling_rigs = excel.parse('drilling_rigs', header=0, index_col=0)
    vibro_driver = excel.parse('vibro_driver', header=0, index_col=0)

    # Divide cable burial equipments per trenching capabilities
    jetting_trenchers = cable_burial[cable_burial['Jetting capability [yes/no]'] == 'yes']
    plough_trenchers = cable_burial[cable_burial['Ploughing capability [yes/no]'] == 'yes'] 
    cutting_trenchers = cable_burial[cable_burial['Cutting capability [yes/no]'] == 'yes'] 
    
    # Define equipment types by invoking EquipmentType class
    equipments = {'rov': EquipmentType("rov", rov),
                  'divers': EquipmentType("divers", divers),
                  'jetter': EquipmentType("jetter", jetting_trenchers),
                  'plough': EquipmentType("plough", plough_trenchers),
                  'cutter': EquipmentType("cutter", cutting_trenchers),
                  'cable burial': EquipmentType("cable burial", cable_burial),
                  'excavating': EquipmentType("excavating", excavating),
                  'mattress': EquipmentType("mattress", mattress),
                  'rock filter bags': EquipmentType("rock_filter_bags", rock_filter_bags),
                  'split pipe': EquipmentType("split pipe", split_pipe),
                  'hammer': EquipmentType("hammer", hammer),
                  'drilling rigs': EquipmentType("drilling rigs", drilling_rigs),
                  'vibro driver': EquipmentType("vibro driver", vibro_driver)
                  }

    return equipments


def load_port_data(file_path):
    """Imports port database into a panda table

    Parameters
    ----------
    file_path : string
     the folder path of the port database

    Returns
    -------
    vessels : dict
     dictionnary containing a panda dataframe with all ports
    """
    # Transform vessel database .xls into panda type
    excel = pd.ExcelFile(file_path)
    # Collect data from a particular tab
    ports = excel.parse('python', header=0, index_col=0)

    return ports
