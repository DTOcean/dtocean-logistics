

from dtocean_logistics.outputs.plotting_batch import plot_batch

output = {}
output['COST'] = {}

input = [0.1, 0.2, 0.3, 0.4]
output['COST']['Total Installation Cost [EUR]'] = [2, 20, 200, 2000]
variable_CHG = 'cena'
PARAM_SET = 'COISA'


plot_batch(PARAM_SET, output, input, variable_CHG)


