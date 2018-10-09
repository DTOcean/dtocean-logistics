# -*- coding: utf-8 -*-

#    Copyright (C) 2016 Boris Teillant, Paulo Chainho
#    Copyright (C) 2017-2018 Mathew Topper
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
This module governs the definition of all individual logistic operations
considered within the DTOcean tool, in terms of id, description, pre-defined
time for completition and operational limit conditions. These will be used to
further characterize the operation sequence of each logistic phase.

.. moduleauthor:: Boris Teillant <boris.teillant@wavec.org>
.. moduleauthor:: Paulo Chainho <paulo@wavec.org>
.. moduleauthor:: Mathew Topper <mathew.topper@dataonlygreater.com>
"""

class LogOp(object):

    def __init__(self, op_id,
                       description,
                       time_value,
                       time_function,
                       time_other,
                       olc):
        
        self.id = op_id
        self.description = description
        self.time_value = time_value
        self.time_function = time_function
        self.time_other = time_other
        self.olc = olc
        
        return


def logOp_init(op_db):
    
    """logOp_init function defines all individual logistic operations
    considered within the DTOcean tool. Each individual operation is defined by
    invoking the class LogOp. Explanation of the key ID numbering system
    implemented:
        
    1st digit:  1 = General individual operation shared with all/most logistic
                    phases;
                2 = Specialized individual operation for the installation of
                    electrical infrastructure;
                3 = Specialized individual operation for the installation of
                    foundations;
                4 = Specialized individual operation for the installation of
                    moorings;
                5 = Specialized individual operation for the installation of
                    tidal or wave energyd devices;
                6 = Specialized individual operation for inspection activities;
                7 = Specialized individual operation for on-site maintenance
                    interventions;
                8 = Specialized individual operation for port-based maintenance
                    interventions;
                    
    2nd/3rd digit: simple counter to discriminate between different individual
                   operations within the same category defined by the 1st digit

    Parameters
    ----------

    Returns
    -------
    logOp : dict
     dictionnary containing all classes defining the logistic operations
    """
    
    logOp = {}
        
    name_map = {'id [-]': "id",
                'Logitic operation [-]': "op",
                'Time: value [h]': "val",
                'Time: function [-]': "func",
                'Time: other [-]': "other",
                'OLC: Hs [m]': "hs",
                'OLC: Tp [s]': "tp",
                'OLC: Ws [m/s]': "ws",
                'OLC: Cs [m/s]': "cs"}
    
    new_op_db = op_db.rename(columns=name_map)

    # Create a dictionary containing all listed operations
    for row in new_op_db.itertuples():
        
        olcs = [row.hs, row.tp, row.ws, row.cs]

        logOp[row.Index] = LogOp(row.id,
                                 row.op,
                                 row.val,
                                 row.func,
                                 row.other,
                                 olcs)

    return logOp
