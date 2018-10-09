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

def cost_p_year(Installation):

    # determine start and end date of whole installation
    start_date_list = []
    end_date_list = []
    for operation in Installation['OPERATION']:

        start_date_list.append( Installation['OPERATION'][operation]['DATE']['Start Date'] )
        end_date_list.append( Installation['OPERATION'][operation]['DATE']['End Date'] )


    Installation['DATE']['Start Date'] = min(start_date_list)
    Installation['DATE']['End Date'] = max(end_date_list)

    # initialise cost per year list
    installation_start_date_year = Installation['DATE']['Start Date'].year
    installation_end_date_year = Installation['DATE']['End Date'].year

    cost_year = {}
    for year_i in range( installation_start_date_year, installation_end_date_year+1, 1 ):
        cost_year[year_i] = 0





    # asses cost per year in each operation and sum per year
    for operation in Installation['OPERATION']:

        solution_cost = Installation['OPERATION'][operation]['COST']['Total Cost [EUR]']
        solution_end_year = Installation['OPERATION'][operation]['DATE']['End Date'].year

        cost_year[solution_end_year] = cost_year[solution_end_year] + solution_cost

    return cost_year