# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 13:20:13 2017

@author: mtopper
"""

import numpy as np
import pandas as pd

from dtocean_logistics.feasibility.feasability_om import (
                                                get_wet_mate_demating_force)


def test_get_wet_mate_demating_force():

    dyn_in = {u'MBL [N]': {u'Dynamic cable001': np.nan},
              u'MBR [m]': {u'Dynamic cable001': 0.84999999999999998},
              u'buoyancy diameter [mm]': {u'Dynamic cable001': 3000},
              u'buoyancy length [m]': {u'Dynamic cable001': np.nan},
              u'buoyancy number [-]': {u'Dynamic cable001': np.nan},
              u'buoyancy weigth [kg]': {u'Dynamic cable001': np.nan},
              u'diameter [mm]': {u'Dynamic cable001': 100},
              u'downstream ei id [-]': {u'Dynamic cable001': 2},
              u'downstream ei type [-]': {u'Dynamic cable001': u'wet-mate'},
              u'downstream termination id [-]':
                  {u'Dynamic cable001': u'device002'},
              u'downstream termination type [-]':
                  {u'Dynamic cable001': u'device'},
              u'downstream termination x coord [m]':
                  {u'Dynamic cable001': 495100.53000000003},
              u'downstream termination y coord [m]': 
                 {u'Dynamic cable001': 5675775.0499999998 },
              u'downstream termination zone [-]':
                  {u'Dynamic cable001': u'31 U'},
              u'dry mass [kg/m]': {u'Dynamic cable001': 50},
              u'length [m]': {u'Dynamic cable001': 500},
              u'total dry mass [kg]': {u'Dynamic cable001': np.nan},
              u'upstream ei id [-]': {u'Dynamic cable001': 1},
              u'upstream ei type [-]': {u'Dynamic cable001': u'wet-mate'},
              u'upstream termination id [-]':
                  {u'Dynamic cable001': u'device001'},
              u'upstream termination type [-]':
                  {u'Dynamic cable001': u'device'},
              u'upstream termination x coord [m]':
                  {u'Dynamic cable001': 495100.53000000003},
              u'upstream termination y coord [m]':
                  {u'Dynamic cable001': 5675500.0499999998},
              u'upstream termination zone [-]': {u'Dynamic cable001': u'31 U'}}
        
    dyn_df = pd.DataFrame(dyn_in)
    
    connectors_in = {u'demating force [N]': {1: 5.0,
                                             2: 5.0},
                     u'dry mass [kg]': {1: 150,
                                        2: 150},
                     u'height [m]': {1: np.nan,
                                     2: np.nan},
                     u'lenght [m]': {1: np.nan,
                                     2: np.nan},
                     u'mating force [N]': {1: 5.0,
                                           2: 5.0},
                     u'type [-]': {1: u'wet-mate',
                                   2: u'wet-mate'},
                     u'width [m]': {1: np.nan,
                                    2: np.nan}}
                     
    connectors = pd.DataFrame(connectors_in)
    
    demate_force = get_wet_mate_demating_force(dyn_df,
                                               connectors)
    
    assert np.isclose(demate_force.sum(), 5)
