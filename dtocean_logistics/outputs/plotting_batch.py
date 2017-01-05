# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org, pedro.vicente@wavec.org

The function out_plotting plots the results outputed


"""

import matplotlib.pyplot as plt
import numpy as np


# import plotly.tools as tls
# tls.set_credentials_file(username='dtocean_py', api_key='0y4l4o1wbe')
# from plotly.tools import FigureFactory as FF
# import plotly.plotly as py
# py.sign_in("dtocean_py", "dtocean_py")

color_VEC = ["lightskyblue", "yellowgreen", "mediumpurple", "red", "blue"] # CONTINUE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def plot_bar(PARAM_SET, INPUTS, VARIABLE, OUTPUTS, PARAM):

    mpl_fig = plt.figure()

    ax = mpl_fig.add_subplot(111)

    N = len(OUTPUTS)-1
    ind = INPUTS #??????????????????????????????????
    # ind = np.arange(N)    # the x locations for the groups


    width = 1/0.5

    for indx_pt in range(len(OUTPUTS)):

        ind_i = INPUTS[indx_pt]

        pi = []
        color_i = 0
        bottom_i = 0
        for output_type in OUTPUTS[indx_pt]:
            if not (output_type == 'Total Installation Cost [EUR]' or
                            output_type == 'Total Estimated Cost [EUR]' or
                            output_type == 'Yearly Cost [yy, EUR]') :
                pi.append( ax.bar(ind_i, OUTPUTS[indx_pt][output_type], width, color = color_VEC[color_i], bottom=bottom_i) )
                bottom_i += OUTPUTS[indx_pt][output_type]
                color_i += 1

    ax.set_ylabel(' ')
    # ax.set_ylabel('Time [h]')
    ax.set_xlabel(VARIABLE)
    ax.set_title(PARAM)

    # ax.set_xticks(INPUTS + width/2.)
    ax.set_xticklabels(INPUTS)

    # plt.legend((pi[0], p2[0], p3[0]),
    #            (x[0], x[1], x[2]))


    plt.savefig( 'Outputs/' + PARAM_SET + '/Fig_Plot_' + VARIABLE + '.png' )

    # plt.show()




def plot_batch(PARAM_SET, output, input, variable_CHG):

    # PARAM = 'Total Installation Cost [EUR]'
    # output_VEC =[]
    # for ind_x in range(len(output)):
    #     output_VEC.append( output[ind_x]['COST'][PARAM] )
    # plot_bar(PARAM_SET, input, variable_CHG, output_VEC, PARAM )

    PARAM = 'COST'
    output_VEC =[]
    for ind_x in range(len(output)):
        output_VEC.append( output[ind_x][PARAM])
    plot_bar(PARAM_SET, input, variable_CHG, output_VEC/1000.0, PARAM + ' [kEUR]' )

    return