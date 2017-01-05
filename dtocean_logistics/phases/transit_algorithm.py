# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 10:04:16 2015

@author: pcvicente adapted from acollin

The transit algorithm calculates the distance and route between two sea points, considering the European coastline.
It is used to calculate the ship routing for the vessels performing installation or operation&maintenance activities.
It receives the coordinates in utm of the two points and returns the distance (together with the graphical representation
of the route).

"""

import csv
import matplotlib.pyplot as plt
import networkx as nx
import pickle
import utm
import timeit

from os import path
import os
import sys

import logging
module_logger = logging.getLogger(__name__)


def transit_algorithm(point_INI, point_FIN, point_path, graph_path):

    ini_x_utm = point_INI[0]
    ini_y_utm = point_INI[1]
    ini_zone_utm = point_INI[2]

    fin_x_utm = point_FIN[0]
    fin_y_utm = point_FIN[1]
    fin_zone_utm = point_FIN[2]
    
    # [LAT_INI, LONG_INI] = utm.to_latlon(ini_x_utm, ini_y_utm, int(ini_zone_utm[0:2]), str(ini_zone_utm[3]))
    # [LAT_FIN, LONG_FIN] = utm.to_latlon(fin_x_utm, fin_y_utm, int(fin_zone_utm[0:2]), str(fin_zone_utm[3]))

    ### Loading the water points off the European Coast:
    num_points = 1
    lat_i = []
    long_i = []
    with open(point_path, 'rb') as csvfile:
        datareader = csv.reader(csvfile, delimiter='\t')
        for row in datareader:
            # print num_points
            # print ', '.join(row)

            if num_points<=1000:
                lat_i.append(float(row[2])/1e15)
                long_i.append(float(row[3])/1e15)

            elif num_points==1001:
                lat_i.append(float(row[3])/1e15)
                long_i.append(float(row[4])/1e15)

            elif num_points>=1001:
                if num_points%1000==0 or (num_points-1)%1000==0:
                    lat_i.append(float(row[3])/1e15)
                    long_i.append(float(row[4])/1e15)
                else:
                    lat_i.append(float(row[4])/1e15)
                    long_i.append(float(row[5])/1e15)

            if (long_i[num_points-1]<1 and long_i[num_points-1]>0) or (long_i[num_points-1]>-1 and long_i[num_points-1]<0):
                long_i[num_points-1] = long_i[num_points-1]*1e15

            num_points = num_points+1

    # delt_lat = abs(lat_i[1168] - lat_i[0])
    delt_long = abs(long_i[1] - long_i[0])

    ### Loading of the graph
    start_time = timeit.default_timer()
    
    with open(graph_path, "rb" ) as graph_file:
        graph = pickle.load(graph_file)

    print '» graph loaded'
    stop_time = timeit.default_timer()
    print 'duration [s]:' + str(stop_time - start_time)

    ### Coordinates of the locations to graph points:
    ERROR_POINTS = delt_long/0.125

    [LAT_INI, LONG_INI] = utm.to_latlon(ini_x_utm, ini_y_utm, int(ini_zone_utm[0:2]), str(ini_zone_utm[3]))
    found_point_INI=0
    for point_vec in range(len(lat_i)):

        LAT_ini = lat_i[point_vec]
        LONG_ini = long_i[point_vec]
        # print [LAT, LONG]

        # dist_vec.append( distance(site_coords, port_coords) )

        if LAT_ini>LAT_INI-ERROR_POINTS and LAT_ini<LAT_INI+ERROR_POINTS:
            if LONG_ini>LONG_INI-ERROR_POINTS and LONG_ini<LONG_INI+ERROR_POINTS:
                if graph.has_node(point_vec):
                    point_INI = point_vec
                    found_point_INI=1
                    # print point_INI
                    break

    if found_point_INI==0:
        
        msg = ("Error in port selection: initial coordinates not accurate.")
        module_logger.warning(msg)

    [LAT_FIN, LONG_FIN] = utm.to_latlon(fin_x_utm, fin_y_utm, int(fin_zone_utm[0:2]), str(fin_zone_utm[3]))
    found_point_FIN=0
    for point_vec in range(len(lat_i)):

        LAT_fin = lat_i[point_vec]
        LONG_fin = long_i[point_vec]
        # print [LAT, LONG]

        if LAT_fin>LAT_FIN-ERROR_POINTS and LAT_fin<LAT_FIN+ERROR_POINTS:
            if LONG_fin>LONG_FIN-ERROR_POINTS and LONG_fin<LONG_FIN+ERROR_POINTS:
                if graph.has_node(point_vec):
                    point_FIN = point_vec
                    found_point_FIN=1
                    # print point_FIN
                    break

    if found_point_FIN==0:
        msg = ("Error in port selection: final coordinates not accurate.")
        module_logger.warning(msg)

    ### define start and end point:
    start = point_INI # port
    end = point_FIN # array location

    ### Calculate route:
    print '» routing!'
    start_time = timeit.default_timer()
    # print start_time

    # if path exists, run this
    if nx.has_path(graph,start,end):
        route = nx.dijkstra_path(graph,start,end)
        route_length = nx.dijkstra_path_length(graph,start,end)

    stop_time = timeit.default_timer()
    # print stop_time
    print 'duration [s]:' + str(stop_time - start_time)
    #print '* route:'
    #print route
    print '* distance [km]:' + str(route_length)

    ### Plot route on map:
    LONG_ROUTE = []
    LAT_ROUTE = []
    for ind_rout in range(len(route)):
        LONG_ROUTE.append(long_i[route[ind_rout]])
        LAT_ROUTE.append(lat_i[route[ind_rout]])
        
    plt.figure()

    # european sea points:
    plt.plot(long_i,lat_i, 'ro')

    # origin and destination points:
    plt.plot(LONG_ini,LAT_ini, 'yo')
    plt.plot(LONG_fin,LAT_fin, 'yo')

    # route:
    plt.plot(LONG_ROUTE,LAT_ROUTE,'y-')

    plt.show()

    return route_length