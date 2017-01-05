
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