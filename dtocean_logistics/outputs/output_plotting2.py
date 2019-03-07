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


def simul_plot_bar(outputs, simul_time, log_phase_description):

    mpl_fig = plt.figure()


    ax = mpl_fig.add_subplot(121)

    y = [outputs['TIME']['Preparation Time [h]'],
         outputs['TIME']['Waiting Time [h]'],
         outputs['TIME']['Sea Transit Time [h]'] + outputs['TIME']['Sea Operation Time [h]']]
    N = 1
    ind = np.arange(N)    # the x locations for the groups

    x = ['prep time', 'wait time', 'sea time']
    width = 1/0.5

    p1 = ax.bar(ind, y[0], width, color="lightskyblue")
    p2 = ax.bar(ind, y[1], width, color="yellowgreen", bottom=y[0])
    p3 = ax.bar(ind, y[2], width, color="mediumpurple", bottom=y[0]+y[1])

    ax.set_ylabel(' ')
    # ax.set_ylabel('Time [h]')
    ax.set_xlabel('')
    ax.set_title('Schedule Time [h]')
    ax.set_xticks(ind + width/2.)
    ax.set_xticklabels(' ')

    plt.legend((p1[0], p2[0], p3[0]), (x[0], x[1], x[2]))



    ax = mpl_fig.add_subplot(122)

    y = [outputs['COST']['Port Cost [EUR]'],
         outputs['COST']['Vessel Cost [EUR]'],
         outputs['COST']['Equipment Cost [EUR]']]
    N = 1
    ind = np.arange(N)    # the x locations for the groups

    x = ['port cost', 'vessel cost', 'equip. cost']
    width = 1/0.5

    p1 = ax.bar(ind, y[0], width, color="mediumpurple")
    p2 = ax.bar(ind, y[1], width, color="yellowgreen", bottom=y[0])
    p3 = ax.bar(ind, y[2], width, color="lightskyblue", bottom=y[0]+y[1])

    ax.set_ylabel(' ')
    # ax.set_ylabel('Cost [EUR]')
    ax.set_xlabel('')
    ax.set_title('Installation Cost [EUR]')
    ax.set_xticks(ind + width/2.)
    ax.set_xticklabels(' ')

    plt.legend((p1[0], p2[0], p3[0]), (x[0], x[1], x[2]))




    # ax = mpl_fig.add_subplot(133)
    #
    # y = [simul_time['port_CPU_time'],
    #      simul_time['feas_CPU_time'],
    #      simul_time['match_CPU_time'],
    #      simul_time['sched_CPU_time'],
    #      simul_time['cost_CPU_time']]
    # N = 1
    # ind = np.arange(N)    # the x locations for the groups
    #
    # x = ['Port Select.', 'Feasability', 'Matching ', 'Schedule', 'Cost']
    # width = 1/0.5
    #
    # p1 = ax.bar(ind, y[0], width, color="green")
    # p2 = ax.bar(ind, y[1], width, color="yellowgreen", bottom=y[0])
    # p3 = ax.bar(ind, y[2], width, color="red", bottom=y[0]+y[1])
    # p4 = ax.bar(ind, y[3], width, color="lightskyblue", bottom=y[0]+y[1]+y[2])
    # p5 = ax.bar(ind, y[4], width, color="mediumpurple", bottom=y[0]+y[1]+y[2]+y[3])
    #
    # ax.set_ylabel(' ')
    # # ax.set_ylabel('CPU time [s]')
    # ax.set_xlabel('')
    # ax.set_title('CPU time [s]')
    # ax.set_xticks(ind + width/2.)
    # ax.set_xticklabels(' ')
    #
    # plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0]), (x[0], x[1], x[2], x[3], x[4]))

    log_phase_descript = log_phase_description
    log_phase_descript = log_phase_descript.replace("mooring systems with","")
    log_phase_descript = log_phase_descript.replace(" ","_")
    log_phase_descript = log_phase_descript.replace("/","_")
    plt.show()

    # print 'PLOTBAR FINNISHED!'



def simul_plot_pie(outputs, simul_time, log_phase_description):

    mpl_fig = plt.figure()

    ax = mpl_fig.add_subplot(121)
    labels = 'prep time', 'wait time', 'sea time'
    values = [ 100.0*outputs['TIME']['Preparation Time [h]']/outputs['TIME']['Total Time [h]'],
         100.0*outputs['TIME']['Waiting Time [h]']/outputs['TIME']['Total Time [h]'],
         100.0*(outputs['TIME']['Sea Transit Time [h]']+outputs['TIME']['Sea Operation Time [h]'])/outputs['TIME']['Total Time [h]'] ]

    colors = ['yellowgreen', 'mediumpurple', 'lightskyblue']
    explode = (0.075, 0.025, 0.025)    # proportion with which to offset each wedge
    patches1, texts1, autotexts1 = plt.pie(values,              # data
            explode=explode,    # offset parameters
            labels=labels,      # slice labels
            colors=colors,      # array of colours
            autopct='%1.1f%%',  # print the values inside the wedges
            shadow=True        # enable shadow
            ,startangle=0       # starting angle
            , labeldistance=1.1
            )
    for pie_wedge in patches1:
        pie_wedge.set_edgecolor('white')
    texts1[0].set_fontsize(10)
    autotexts1[0].set_fontsize(10)
    plt.axis('equal')
    ax.set_title('Schedule:')


    ax = mpl_fig.add_subplot(122)
    labels = 'port cost', 'vessel cost', 'equip. cost'
    values = [100.0*outputs['COST']['Port Cost [EUR]']/outputs['COST']['Total Cost [EUR]'],
         100.0*outputs['COST']['Vessel Cost [EUR]']/outputs['COST']['Total Cost [EUR]'],
         100.0*outputs['COST']['Equipment Cost [EUR]']/outputs['COST']['Total Cost [EUR]'] ]#,
         # 100.0*outputs['solution']['total_fuel_cost [EUR]']/outputs['solution']['total_cost [EUR]'] ]
    colors = ['yellowgreen', 'mediumpurple', 'lightskyblue']
    explode = (0.075, 0.025, 0.025)    # proportion with which to offset each wedge
    patches2, texts2, autotexts2 = plt.pie(values,              # data
            explode=explode,    # offset parameters
            labels=labels,      # slice labels
            colors=colors,      # array of colours
            autopct='%1.1f%%',  # print the values inside the wedges
            shadow=True        # enable shadow
            ,startangle=0       # starting angle
            , labeldistance=1.1
            )
    for pie_wedge in patches2:
        pie_wedge.set_edgecolor('white')
    texts2[0].set_fontsize(10)
    autotexts2[0].set_fontsize(10)
    plt.axis('equal')
    ax.set_title('Cost:')


    # ax = mpl_fig.add_subplot(133)
    # labels = 'Port Select.', 'Feasability', 'Matching ', 'Schedule'\
    #     # , 'Cost'
    # # print simul_time
    # values=[]
    # values = [100.0*simul_time['port_CPU_time']/simul_time['total_CPU_time'],
    #      100.0*simul_time['feas_CPU_time']/simul_time['total_CPU_time'],
    #      100.0*simul_time['match_CPU_time']/simul_time['total_CPU_time'],
    #      100.0*simul_time['sched_CPU_time']/simul_time['total_CPU_time'] ]
    #     # , simul_time['cost_CPU_time']]
    #
    #
    # # # SORTING!!
    # # data = []
    # # for index in range(len(values)):
    # #     data.append( [values[index], labels[index]] )
    # # sorted_data = sorted(data)
    # # values = []
    # # labels = []
    # # for index in range(len(sorted_data)):
    # #     values.append( sorted_data[index][0] )
    # #     labels.append( sorted_data[index][1] )
    # # values = tuple(values)
    # # labels = tuple(labels)
    #
    # colors = ['yellowgreen', 'mediumpurple', 'lightskyblue', 'red']
    # explode = (0.025, 0.075, 0.025, 0.075)    # proportion with which to offset each wedge
    # patches3, texts3, autotexts3 = plt.pie(values,              # data
    #         explode=explode,    # offset parameters
    #         labels=labels,      # slice labels
    #         colors=colors,      # array of colours
    #         autopct='%1.1f%%',  # print the values inside the wedges
    #         shadow=True        # enable shadow
    #         ,startangle=0       # starting angle
    #         , labeldistance=1.2
    #         )
    # for pie_wedge in patches3:
    #     pie_wedge.set_edgecolor('white')
    # texts3[0].set_fontsize(10)
    # texts3[2].set_fontsize(10)
    # autotexts3[0].set_fontsize(10)
    # autotexts3[2].set_fontsize(10)
    # plt.axis('equal')
    # ax.set_title('CPU time:')


    # print 'PIEBAR FINNISHED!'

    log_phase_descript = log_phase_description
    log_phase_descript = log_phase_descript.replace("mooring systems with","")
    log_phase_descript = log_phase_descript.replace(" ","_")
    log_phase_descript = log_phase_descript.replace("/","_")
    plt.show()

    return




def simul_plot_tables(module, outputs, simul_time):

    # SOLUTION:
    VE_sol = module['VESSELS & EQUIPMENTS']
    Vess_in_sol=[]
    Eqs_in_sol=[]
    for ind_vess_sol in range(len(VE_sol)):
       Vess_in_sol.append( VE_sol[ind_vess_sol][0] )
       if len(VE_sol[ind_vess_sol])>3:
           nr_equip = len(VE_sol[ind_vess_sol]) - 3
           for ind_eqs_in_vess in range(nr_equip):
                Eqs_in_sol.append( VE_sol[ind_vess_sol][3+ind_eqs_in_vess][0] )


    fig, axs =plt.subplots(2,1)
    log_phase_descript = outputs['logistic_phase_description']
    log_phase_descript = log_phase_descript.replace("mooring systems with","")
    log_phase_descript = log_phase_descript.replace(" ","_")
    log_phase_descript = log_phase_descript.replace("/","_")
    data_matrix = [ [log_phase_descript, 'Initial', outputs['ves_types_init'], outputs['eq_types_init']],
                   [log_phase_descript, 'After Feasability', outputs['ves_types_feas'], outputs['eq_types_feas']],
                   [log_phase_descript, 'After Matching', outputs['ves_types_match'], outputs['eq_types_match']],
                   [log_phase_descript, 'Solution', Vess_in_sol, Eqs_in_sol]
                    ]
    collabel=('LOGISTIC PHASE', 'STAGE:', 'VESSELS:', 'EQUIPMENTS:')
    axs[0].axis('tight')
    axs[0].axis('off')
    the_table = axs[0].table(cellText=data_matrix, colLabels=collabel, loc='center', cellLoc='center', fontsize=15, colWidths=[0.45, 0.20, 0.25, 0.25])
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(8)
    # the_table.set_title('title')
    # table.scale(1.25, 1.25)


    data_matrix = [ ['Deck Area [m^2]', "%.2f" % module['requirement'][5]['deck area']],
                   ['Deck Cargo [t]', "%.2f" % module['requirement'][5]['deck cargo']],
                   ['Deck Loading [t/m^2]', "%.2f" % module['requirement'][5]['deck loading']],
                   ['Crane Capacity [t]', "%.2f" % module['requirement'][5]['deck cargo']]
                    ]
    collabel=('PARAMETER:','PORT REQUIREMENTS:')
    axs[1].axis('tight')
    axs[1].axis('off')
    the_table = axs[1].table(cellText=data_matrix, colLabels=collabel, loc='center', cellLoc='center', fontsize=15, colWidths=[0.5, 0.3])
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(8)
    # table.scale(1.25, 1.25)

    # # iterate through cells of a table
    # table_props = the_table.properties()
    # table_cells = table_props['child_artists']
    # for cell in table_cells:
    #     cell._text.set_fontsize(10)
    #     cell._text.set_color('blue')
    #     break

    log_phase_descript = outputs['logistic_phase_description']
    log_phase_descript = log_phase_descript.replace("mooring systems with","")
    log_phase_descript = log_phase_descript.replace(" ","_")
    log_phase_descript = log_phase_descript.replace("/","_")
    plt.savefig( 'Outputs' + '/Fig_Table_' + log_phase_descript + '.png' )
    plt.show()


    # print 'TABLEPLOT FINNISHED!'


    return



def out_ploting(module, outputs, simul_time, PLOT_FLAG, log_phase_description):

    if PLOT_FLAG:
        simul_plot_bar(outputs, simul_time, log_phase_description)
        simul_plot_pie(outputs, simul_time, log_phase_description)
        # simul_plot_tables(module, outputs, simul_time) # NEEDS TO BE UPDATED!!!!!!!!


    # print 'PLOTTING FINNISHED!'

    return



import datetime as dt
from datetime import timedelta
import matplotlib.font_manager as font_manager
import matplotlib.dates
from matplotlib.dates import MONTHLY, DateFormatter, rrulewrapper, RRuleLocator
import matplotlib.gridspec as gridspec

from pylab import *

def create_date(year, month, day, hour, minute, second):
    """Creates the date"""

    date = dt.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    mdate = matplotlib.dates.date2num(date)

    return mdate


def out_ploting_installation(Installation, logistic_phase_description):

    # Data
    num_phases = len(Installation['OPERATION'])
    pos = arange(0.5,(num_phases)/2 + 1.0,0.5)

    ylabels = []
    customDates = []
    # for operation in Installation['OPERATION']:
    for operation in logistic_phase_description:
        l_phase = operation
        log_phase_descript = l_phase
        # log_phase_descript = log_phase_descript.replace("mooring systems with","")
        # log_phase_descript = log_phase_descript.replace(" ","_")
        # log_phase_descript = log_phase_descript.replace("/","_")
        ylabels.append(log_phase_descript)
        start_dt = Installation['OPERATION'][l_phase]['DATE']['Start Date'] - timedelta(hours = sum(Installation['OPERATION'][l_phase]['TIME']['Preparation Time [h]']))
        prep_dt = Installation['OPERATION'][l_phase]['DATE']['Start Date'] 
        depart_dt = Installation['OPERATION'][l_phase]['DATE']['Depart Date']
        end_dt = Installation['OPERATION'][l_phase]['DATE']['End Date']
        # print 'log_phase_descript: ' + l_phase # DEBUGGING
        # print 'start_dt: ' + str(start_dt) # DEBUGGING
        # print 'prep_dt: ' + str(prep_dt) # DEBUGGING
        # print 'depart_dt: ' + str(depart_dt) # DEBUGGING
        # print 'end_dt: ' + str(end_dt) # DEBUGGING
        customDates.append([create_date(start_dt.year, start_dt.month, start_dt.day, start_dt.hour, start_dt.minute ,start_dt.second),
                            create_date(prep_dt.year, prep_dt.month, prep_dt.day, prep_dt.hour, prep_dt.minute, prep_dt.second),
                            create_date(depart_dt.year, depart_dt.month, depart_dt.day, depart_dt.hour, depart_dt.minute, depart_dt.second),
                            create_date(end_dt.year, end_dt.month, end_dt.day, end_dt.hour, end_dt.minute, end_dt.second)])


    task_dates = {}
    for i,task in enumerate(ylabels):
        task_dates[task] = customDates[i]

    # Initialise plot

    fig = plt.figure()

    # ax = subplot2grid((1,3), (0,1), colspan=2)
    ax = subplot2grid((1,2), (0,1), colspan=1)

    # Plot the data:
    start_date, end_prep_begin_waiting_date, end_waiting_begin_sea_date, end_date = task_dates[ylabels[0]]
    ax.barh(0.5, end_date - start_date, left=start_date, height=0.4, align='center', color='blue', alpha = 0.75)
    ax.barh(0.4, (end_prep_begin_waiting_date - start_date), left=start_date, height=0.1, align='center', color='red', alpha = 0.75, label = "Prep Time")
    ax.barh(0.5, (end_waiting_begin_sea_date - end_prep_begin_waiting_date), left=end_prep_begin_waiting_date, height=0.1, align='center', color='yellow', alpha = 0.75, label = "Waiting Time")
    ax.barh(0.6, (end_date - end_waiting_begin_sea_date), left=end_waiting_begin_sea_date, height=0.1, align='center', color='green', alpha = 0.75, label = "Sea Time")

    for i in range(0,len(ylabels)-1):
        start_date, end_prep_begin_waiting_date, end_waiting_begin_sea_date, end_date = task_dates[ylabels[i+1]]
        ax.barh((i*0.5)+1.0, end_date - start_date, left=start_date, height=0.4, align='center', color='blue', alpha = 0.75)
        ax.barh((i*0.5)+1.0-0.1, (end_prep_begin_waiting_date - start_date), left=start_date, height=0.1, align='center', color='red', alpha = 0.75)
        ax.barh((i*0.5)+1.0, (end_waiting_begin_sea_date - end_prep_begin_waiting_date), left=end_prep_begin_waiting_date, height=0.1, align='center', color='yellow', alpha = 0.75)
        ax.barh((i*0.5)+1.0+0.1, (end_date - end_waiting_begin_sea_date), left=end_waiting_begin_sea_date, height=0.1, align='center', color='green', alpha = 0.75)

    # Format the y-axis

    locsy, labelsy = yticks(pos,ylabels)
    plt.setp(labelsy, fontsize = 12)

    # Format the x-axis

    ax.axis('tight')
    ax.set_ylim(ymin = -0.1, ymax = (num_phases)/2 + 1.0)
    ax.grid(color = 'g', linestyle = ':')

    ax.xaxis_date() #Tell matplotlib that these are dates...

    rule = rrulewrapper(MONTHLY, interval=1)
    loc = RRuleLocator(rule)
    formatter = DateFormatter("%b '%y")

    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(formatter)
    labelsx = ax.get_xticklabels()
    plt.setp(labelsx, rotation=30, fontsize=11)

    # Format the legend

    font = font_manager.FontProperties(size='small')
    ax.legend(loc=1,prop=font)

    # Finish up
    ax.invert_yaxis()
    fig.autofmt_xdate()

    #plt.savefig('gantt.svg')


    plt.savefig( 'Outputs' + '/Fig_Gantt_Installation' + '.png' )
    # plt.savefig( 'Fig_Gantt_Installation' + '.svg' )
    # plt.savefig( 'Fig_Gantt_Installation' + '.eps' )

    plt.show()


    return
