import sys
import os
import matplotlib as mpl
import joblib as joblib
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QGridLayout, QComboBox, \
    QPushButton, QCheckBox, QFrame, QMessageBox, QScrollArea, QMainWindow, QAction
from PyQt5.uic.properties import QtWidgets
from matplotlib.backends import qt_compat

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.transforms import Bbox

import math
import numpy as np
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.pyplot import axhspan
from scipy import spatial
from sklearn.metrics import classification_report,confusion_matrix
from sko.ACA import ACA_TSP

import DynamicModel
import EnvironmentModel
import StaticModel
import TrainingCode


def isNaN(string):
    return string != string

def disCal(d1,d2):
    a_x = int(d1.split(",")[0])
    a_y = int(d1.split(",")[1])
    b_x = int(d2.split(",")[0])
    b_y = int(d2.split(",")[1])
    dis = math.sqrt((a_x-b_x)**2+(a_y-b_y)**2)
    return round(dis,2)

# moved_dataframe = pd.read_csv("2021-05-09 18:01:06.975995/movedObjects4018:04:18.294713.csv")
# added_dataframe = pd.read_csv("2021-05-09 18:01:06.975995/added.csv")
# relation_dataframe = pd.read_csv("2021-05-09 18:01:06.975995/relationObjects4018:04:18.294713.csv")

def rel_dis():
    for i,row in moved_dataframe.iterrows():
        j = 2
        deviceInteractionDic = {}
        #To initialse all the intersections
        for z in list(moved_dataframe["Device_id"]):
            if(z!=row.iloc[0]):
                deviceInteractionDic[z] =0
        #Loop for individual interaction coloumn
        while(j<len(moved_dataframe.columns)):
            # print(row.iloc[0],row.iloc[j])
            if(not isNaN(row.iloc[j])):
                temp = row.iloc[j].split(",")
                temp = [i.split(":")[0] for i in temp]
                #Removing mulitple interaction of Protocol for same device
                temp = np.unique(np.array(temp))
                for z in temp:
                    if(z in deviceInteractionDic.keys()):
                        deviceInteractionDic[z] = deviceInteractionDic[z]+1
            j = j+2
        out_text = ""
        for i in deviceInteractionDic.keys():
            out_text = out_text+str(i)+":"+str(deviceInteractionDic[i])+","
        out_text = out_text[:-1]

        #For distance
        tem = "Move"+str((len(moved_dataframe.columns)-1)//2)
        d1_gps = row.iloc[moved_dataframe.columns.get_loc(tem)]
        out_text_dis= ""
        for z in list(moved_dataframe["Device_id"]):
            if(z!=row.iloc[0]):
                d2_gps = moved_dataframe.loc[moved_dataframe["Device_id"]== z,tem]
                d2_gps = str(d2_gps).split("\n")[0].split("    ")[1]
                out_text_dis = out_text_dis+str(z)+":"+str(disCal(d1_gps,d2_gps))+","
        out_text_dis = out_text_dis[:-1]
        # print(out_text_dis)

        added_dataframe.loc[added_dataframe["Device_id"] == row.iloc[0],"Intersection"] = out_text
        added_dataframe.loc[added_dataframe["Device_id"] == row.iloc[0],"Distance"] = out_text_dis
    return added_dataframe



def preProcessing():
    data_frame = rel_dis()
    #Dropping unwanted features
    data_frame.drop(['Device Distribution','Link','Relationship'],axis=1,inplace=True)
    data_frame.drop(["Owner_name","Service_id","GPS_Start"],axis=1,inplace=True)

    #Discretization of Data
    data = data_frame.Device.unique()
    data_new = np.arange(len(data_frame.Device.unique()))
    data_frame.Device.replace(data, data_new, inplace=True)
    data_frame.Device_type.replace(["Public","Private"], [0,1], inplace=True)
    data_frame.Device_mobility.replace(["Static","Mobile"],[0,1],inplace=True)
    data = ['ZigBee', 'Wifi','Bluetooth,ZigBee','Wifi,Bluetooth,GSM']
    data_new = np.arange(len(data))
    data_frame.Connectivity.replace(data, data_new, inplace=True)

    data_new =[]
    for i,row in data_frame.iterrows():
        if(isNaN(row.iloc[10])):
            continue
        inter = row.iloc[10].split(",")
        dis = row.iloc[11].split(",")
        tem = "Move"+str((len(moved_dataframe.columns)-1)//2)
        d_gps = moved_dataframe.loc[moved_dataframe["Device_id"]==row.iloc[0] ,tem]
        d_gps = str(d_gps).split("\n")[0].split("    ")[1]
        for i in range(0,len(inter)):
            relation = relation_dataframe.loc[relation_dataframe["Device_id"]==row.iloc[0],inter[i].split(":")[0]]
            # print(relation.values[0])
            if(isNaN(relation.values[0])):
                rel = "-1"
            else:
                rel = relation.values[0]
            manu  = data_frame.loc[data_frame["Device_id"]==inter[i].split(":")[0],"Manufacturing_id"]
            manu = manu.values[0]
            if(row.iloc[6]==int(manu)):
                #Same Manufacturing ID for two devices 1 else 0
                manu = 1
            else:
                manu = 0
            own  = data_frame.loc[data_frame["Device_id"]==inter[i].split(":")[0],"Owner_id"]
            own = own.values[0]
            if(row.iloc[6]==int(own)):
                #Same Owner ID for two devices 1 else 0
                own = 1
            else:
                own = 0
            #Same Conectivity for two devices 1 else 0
            con_data  = data_frame.loc[data_frame["Device_id"]==inter[i].split(":")[0],"Connectivity"]
            con_data = int(con_data.values[0])
            if(row.iloc[8]==2):
                if(con_data==0 or con_data==2):
                    con = 1
                else:
                    con = 0
            elif(row.iloc[8]== 3):
                if(con_data==1 or con_data==2 or con_data==3):
                    con = 1
                else:
                    con = 0
            elif(row.iloc[8]==con_data):
                con = 1
            else:
                con = 0
            if(isinstance(row.iloc[7], str)):
                temp = row.iloc[7].split(",")
                for j in temp:
                    data_new.append({
                        "Device_id" : row.iloc[0],
                        "Device_id_to" : inter[i].split(":")[0],
                        "Device" : row.iloc[1],
                        "Device_type" : row.iloc[2],
                        "Device_mobility" : row.iloc[3],
                        "Owner_id" : own,
                        "Manufacturing_id" : manu,
                        "Application_id" : int(j),
                        "Connectivity" : con,
                        "X_GPS" : int(d_gps.split(",")[0]),
                        "Y_GPS" : int(d_gps.split(",")[1]),
                        "Intersection" : int(inter[i].split(":")[1]),
                        "Distance" : float(dis[i].split(":")[1]),
                        "Relation" : rel,
                    })
            else:
                data_new.append({
                    "Device_id" : row.iloc[0],
                    "Device_id_to" : inter[i].split(":")[0],
                    "Device" : row.iloc[1],
                    "Device_type" : row.iloc[2],
                    "Device_mobility" : row.iloc[3],
                    "Owner_id" : own,
                    "Manufacturing_id" : manu,
                    "Application_id" : row.iloc[7],
                    "Connectivity" : con,
                    "X_GPS" : int(d_gps.split(",")[0]),
                    "Y_GPS" : int(d_gps.split(",")[1]),
                    "Intersection" : int(inter[i].split(":")[1]),
                    "Distance" : float(dis[i].split(":")[1]),
                    "Relation" : rel,
                })
    dataframe_new = pd.DataFrame(data_new)

    #Replacing Labels with corresponding index
    values = ['-1', 'STOR', 'CLOR', 'SIBOR', 'GUOR', 'CWOR', 'GSTOR', 'SOR',
              'OOR', 'POR','SROR']
    data_new = np.arange(len(values))
    dataframe_new.Relation.replace(values, data_new, inplace=True)

    return dataframe_new

class Canvas(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.subplots_adjust(hspace=0.50)
        self.fig.subplots_adjust(left=0.1,right=0.8)
        self.ax = self.fig.add_subplot(111)
        self.ax1 = ""
        self.ax2 = ""
        self.ax3 = ""
        # self.ax.margins(x=100.0,y=100.0)
        # self.ax.set_size_inches(100,100)
        # self.ax.xticks([1, 2, 3, 4, 5])
        self.ax.axis([0,700,0,700])
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

    # def plot(self):
        # x = np.array([50, 30,40])
        # y = np.array([20, 40,60])
        # ax = self.figure.add_subplot(111)
        # ax.scatter(x,y)

class Canvas_Classification(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax1 = self.fig.add_subplot(222)
        self.ax2 = self.fig.add_subplot(212)
        self.ax3 = self.fig.add_subplot(221)

        # self.ax.axis([0,650,0,700])

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

class GraphAll:

    def __init__(self, vertices):
        # No. of vertices
        self.V = vertices

        # default dictionary to store graph
        self.graph = defaultdict(list)

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    '''A recursive function to print all paths from 'u' to 'd'.
    visited[] keeps track of vertices in current path.
    path[] stores actual vertices and path_index is current
    index in path[]'''

    def printAllPathsUtil(self, u, d, visited, path):
        # Mark the current node as visited and store in path
        visited[u]= True
        path.append(u)
        # If current vertex is same as destination, then print
        if u == d:
            print (path)
            pa_x = []
            pa_y = []
            for i in path:
                pa_x.append(int(dataframe_new.loc[dataframe_new["Device_id"]=="D"+str(i) ,"X_GPS"].values[0]))
                pa_y.append(int(dataframe_new.loc[dataframe_new["Device_id"]=="D"+str(i) ,"Y_GPS"].values[0]))
            all_line_x.append(pa_x)
            all_line_y.append(pa_y)
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in self.graph[u]:
                if visited[i]== False:
                    self.printAllPathsUtil(i, d, visited, path)
        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u]= False


    # Prints all paths from 's' to 'd'
    def printAllPaths(self, s, d):

        # Mark all the vertices as not visited
        visited =[False]*(self.V)

        # Create an array to store paths
        path = []

        # Call the recursive helper function to print all paths
        self.printAllPathsUtil(s, d, visited, path)

class Graph:
    def __init__(self):
        # dictionary containing keys that map to the corresponding vertex object
        self.vertices = {}

    def add_vertex(self, key):
        """Add a vertex with the given key to the graph."""
        vertex = Vertex(key)
        self.vertices[key] = vertex

    def get_vertex(self, key):
        """Return vertex object with the corresponding key."""
        return self.vertices[key]

    def __contains__(self, key):
        return key in self.vertices

    def add_edge(self, src_key, dest_key, weight=1):
        """Add edge from src_key to dest_key with given weight."""
        self.vertices[src_key].add_neighbour(self.vertices[dest_key], weight)

    def does_edge_exist(self, src_key, dest_key):
        """Return True if there is an edge from src_key to dest_key."""
        return self.vertices[src_key].does_it_point_to(self.vertices[dest_key])

    def __len__(self):
        return len(self.vertices)

    def __iter__(self):
        return iter(self.vertices.values())

class Vertex:
    def __init__(self, key):
        self.key = key
        self.points_to = {}

    def get_key(self):
        """Return key corresponding to this vertex object."""
        return self.key

    def add_neighbour(self, dest, weight):
        """Make this vertex point to dest with given edge weight."""
        self.points_to[dest] = weight

    def get_neighbours(self):
        """Return all vertices pointed to by this vertex."""
        return self.points_to.keys()

    def get_weight(self, dest):
        """Get weight of edge from this vertex to dest."""
        return self.points_to[dest]

    def does_it_point_to(self, dest):
        """Return True if this vertex points to dest."""
        return dest in self.points_to

def floyd_warshall(g):
    """Return dictionaries distance and next_v.

    distance[u][v] is the shortest distance from vertex u to v.
    next_v[u][v] is the next vertex after vertex v in the shortest path from u
    to v. It is None if there is no path between them. next_v[u][u] should be
    None for all u.

    g is a Graph object which can have negative edge weights.
    """
    distance = {v:dict.fromkeys(g, float('inf')) for v in g}
    next_v = {v:dict.fromkeys(g, None) for v in g}

    for v in g:
        for n in v.get_neighbours():
            distance[v][n] = v.get_weight(n)
            next_v[v][n] = n

    for v in g:
        distance[v][v] = 0
        next_v[v][v] = None

    for p in g:
        for v in g:
            for w in g:
                if distance[v][w] > distance[v][p] + distance[p][w]:
                    distance[v][w] = distance[v][p] + distance[p][w]
                    next_v[v][w] = next_v[v][p]

    return distance, next_v

def print_path(next_v, u, v):
    shortest_line_x = []
    shortest_line_y = []
    devices_in_path = []
    p = u
    while (next_v[p][v]):
        print('{} -> '.format(p.get_key()), end='')
        devices_in_path.append(p.get_key())
        shortest_line_x.append(int(dataframe_new.loc[dataframe_new["Device_id"]==p.get_key() ,"X_GPS"].values[0]))
        shortest_line_y.append(int(dataframe_new.loc[dataframe_new["Device_id"]==p.get_key() ,"Y_GPS"].values[0]))
        p = next_v[p][v]
    print('{} '.format(v.get_key()), end='')
    devices_in_path.append(v.get_key())
    shortest_line_x.append(int(dataframe_new.loc[dataframe_new["Device_id"]==p.get_key() ,"X_GPS"].values[0]))
    shortest_line_y.append(int(dataframe_new.loc[dataframe_new["Device_id"]==p.get_key() ,"Y_GPS"].values[0]))
    return shortest_line_x,shortest_line_y,devices_in_path

def cal_total_distance(routine):
    num_points, = routine.shape
    return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])

def antocolony():
    grouped  = dataframe_new.groupby("Device_id")
    coordinates = []
    labels = []
    for name,group in grouped:
        labels.append(name)
        coordinates.append([group["X_GPS"].values[0],group["Y_GPS"].values[0]])

    num_points = len(coordinates)
    global distance_matrix
    distance_matrix = spatial.distance.cdist(coordinates, coordinates, metric='euclidean')
    aca = ACA_TSP(func=cal_total_distance, n_dim=num_points,
                  size_pop=50, max_iter=200,
                  distance_matrix=distance_matrix)
    total_shortest_path, total_distance = aca.run()
    return total_shortest_path, total_distance


def weights(relation_enabled,protocol_enabled,service_enabled,source_device="D1",destination_device="D1",protocol_selected=[]):
    g = Graph()
    device_id = set(dataframe_new["Device_id"])
    added_dataframe = pd.read_csv(session_path+"/added.csv")

    for i in device_id:
        g.add_vertex(i)
    for i,row in dataframe_new.iterrows():
        if(protocol_enabled==True and relation_enabled==True and service_enabled==True):
            d1_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Service_id"].values[0].split(","))
            d2_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Service_id"].values[0].split(","))
            inter = set(d1_service).intersection(set(d2_service))
            d1_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Connectivity"].values[0].split(","))
            d2_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Connectivity"].values[0].split(","))
            inter_protocol = set(d1_protocol).intersection(set(d2_protocol))
            inter_value_protocol = inter_protocol.intersection(protocol_selected)
            if(int(row.iloc[8])!=0 and int(row.iloc[14])!=0 and len(inter)!=0 and len(inter_value_protocol)!=0 and
                    len(inter_value_protocol)>=len(protocol_selected)):
                #If condition are satisfied then there is a link between the devices i.e edge
                g.add_edge(row.iloc[0], row.iloc[1], row.iloc[12])

        elif protocol_enabled==True and relation_enabled==True:
            d1_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Connectivity"].values[0].split(","))
            d2_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Connectivity"].values[0].split(","))
            inter_protocol = set(d1_protocol).intersection(set(d2_protocol))
            inter_protocol = set(d1_protocol).intersection(set(d2_protocol))
            inter_value_protocol = inter_protocol.intersection(protocol_selected)
            if(int(row.iloc[8])!=0 and int(row.iloc[14])!=0 and len(inter_value_protocol)!=0 and len(inter_value_protocol)>=len(protocol_selected)):
                g.add_edge(row.iloc[0], row.iloc[1], row.iloc[12])
            # print("Protocol and Relation")
        elif(protocol_enabled==True and service_enabled==True):
            d1_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Service_id"].values[0].split(","))
            d2_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Service_id"].values[0].split(","))
            inter = set(d1_service).intersection(set(d2_service))
            d1_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Connectivity"].values[0].split(","))
            d2_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Connectivity"].values[0].split(","))
            inter_protocol = set(d1_protocol).intersection(set(d2_protocol))
            inter_protocol = set(d1_protocol).intersection(set(d2_protocol))
            inter_value_protocol = inter_protocol.intersection(protocol_selected)
            if(len(inter)!=0 and int(row.iloc[8])!=0 and len(inter_value_protocol)!=0 and len(inter_value_protocol)>=len(protocol_selected)):
                g.add_edge(row.iloc[0], row.iloc[1], row.iloc[12])
            # print("Protocol  and Service")
        elif(relation_enabled==True and service_enabled==True):
            d1_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Service_id"].values[0].split(","))
            d2_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Service_id"].values[0].split(","))
            inter = set(d1_service).intersection(set(d2_service))
            if(len(inter)!=0 and int(row.iloc[14])!=0):
                g.add_edge(row.iloc[0], row.iloc[1], row.iloc[12])
            # print("Relation and Service")
        elif(relation_enabled==True):
            if(int(row.iloc[14])!=0):
                g.add_edge(row.iloc[0], row.iloc[1], row.iloc[12])
            # print("Relation")
        elif(protocol_enabled==True):
            d1_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Connectivity"].values[0].split(","))
            d2_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Connectivity"].values[0].split(","))
            inter_protocol = set(d1_protocol).intersection(set(d2_protocol))
            inter_protocol = set(d1_protocol).intersection(set(d2_protocol))
            inter_value_protocol = inter_protocol.intersection(protocol_selected)
            if(int(row.iloc[8])!=0 and len(inter_value_protocol)!=0 and len(inter_value_protocol)>=len(protocol_selected)):
                g.add_edge(row.iloc[0], row.iloc[1], row.iloc[12])
            # print("Protocol")
        elif(service_enabled==True):
            # print(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Service_id"].values[0])
            d1_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Service_id"].values[0].split(","))
            d2_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Service_id"].values[0].split(","))
            inter = set(d1_service).intersection(set(d2_service))
            if(len(inter)!=0):
                g.add_edge(row.iloc[0], row.iloc[1], row.iloc[12])
            # print("Service")


    distance, next_v = floyd_warshall(g)
    shortest_line_x = []
    shortest_line_y = []
    devices_in_path = []
    for start in g:
        for end in g:
            #TODO: Get device id from dropdown
            if(start.get_key()==source_device and end.get_key()==destination_device):
                if next_v[start][end]:

                    print('From {} to {}: '.format(start.get_key(),
                                                   end.get_key()),
                          end = '')
                    shortest_line_x,shortest_line_y,devices_in_path = print_path(next_v, start, end)
                    # print('(distance {})'.format(distance[start][end]))
    return shortest_line_x,shortest_line_y,devices_in_path

def allPath(relation_enabled,protocol_enabled,service_enabled,source_device="D1",destination_device="D1",protocol_selected=[]):
    device_id = set(dataframe_new["Device_id"])
    g = GraphAll(len(device_id)+1)
    added_dataframe = pd.read_csv(session_path+"/added.csv")

    for i,row in dataframe_new.iterrows():
        if(protocol_enabled==True and relation_enabled==True and service_enabled==True):
            d1_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Service_id"].values[0].split(","))
            d2_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Service_id"].values[0].split(","))
            inter = set(d1_service).intersection(set(d2_service))
            d1_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Connectivity"].values[0].split(","))
            d2_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Connectivity"].values[0].split(","))
            inter_protocol = set(d1_protocol).intersection(set(d2_protocol))
            inter_value_protocol = inter_protocol.intersection(protocol_selected)
            if(int(row.iloc[8])!=0 and int(row.iloc[14])!=0 and len(inter)!=0 and len(inter_value_protocol)!=0 and len(inter_value_protocol)>=len(protocol_selected)):
                g.addEdge(int(row.iloc[0].split("D")[1]), int(row.iloc[1].split("D")[1]))
            # print("Protocol and Relation and Service")
        elif(protocol_enabled==True and relation_enabled==True):
            d1_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Connectivity"].values[0].split(","))
            d2_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Connectivity"].values[0].split(","))
            inter_protocol = set(d1_protocol).intersection(set(d2_protocol))
            inter_value_protocol = inter_protocol.intersection(protocol_selected)
            if(int(row.iloc[8])!=0 and int(row.iloc[14])!=0 and len(inter_value_protocol)!=0 and len(inter_value_protocol)>=len(protocol_selected)):
                g.addEdge(int(row.iloc[0].split("D")[1]), int(row.iloc[1].split("D")[1]))
            # print("Protocol and Relation")
        elif(protocol_enabled==True and service_enabled==True):
            d1_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Service_id"].values[0].split(","))
            d2_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Service_id"].values[0].split(","))
            inter = set(d1_service).intersection(set(d2_service))
            d1_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Connectivity"].values[0].split(","))
            d2_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Connectivity"].values[0].split(","))
            inter_protocol = set(d1_protocol).intersection(set(d2_protocol))
            inter_value_protocol = inter_protocol.intersection(protocol_selected)
            if(len(inter)!=0 and int(row.iloc[8])!=0 and len(inter_value_protocol)!=0 and len(inter_value_protocol)>=len(protocol_selected)):
                g.addEdge(int(row.iloc[0].split("D")[1]), int(row.iloc[1].split("D")[1]))
            # print("Protocol  and Service")
        elif(relation_enabled==True and service_enabled==True):
            d1_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Service_id"].values[0].split(","))
            d2_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Service_id"].values[0].split(","))
            inter = set(d1_service).intersection(set(d2_service))
            if(len(inter)!=0 and int(row.iloc[14])!=0):
                g.addEdge(int(row.iloc[0].split("D")[1]), int(row.iloc[1].split("D")[1]))
            # print("Relation and Service")
        elif(relation_enabled==True):
            if(int(row.iloc[14])!=0):
                g.addEdge(int(row.iloc[0].split("D")[1]), int(row.iloc[1].split("D")[1]))
            # print("Relation")
        elif(protocol_enabled==True):
            d1_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Connectivity"].values[0].split(","))
            d2_protocol = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Connectivity"].values[0].split(","))
            inter_protocol = set(d1_protocol).intersection(set(d2_protocol))
            inter_value_protocol = inter_protocol.intersection(protocol_selected)
            if(int(row.iloc[8])!=0 and len(inter_value_protocol)!=0 and len(inter_value_protocol)>=len(protocol_selected)):
                g.addEdge(int(row.iloc[0].split("D")[1]), int(row.iloc[1].split("D")[1]))
            # print("Protocol")
        elif(service_enabled==True):
            # print(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Service_id"].values[0])
            d1_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[0],"Service_id"].values[0].split(","))
            d2_service = list(added_dataframe.loc[added_dataframe["Device_id"]==row.iloc[1],"Service_id"].values[0].split(","))
            inter = set(d1_service).intersection(set(d2_service))
            if(len(inter)!=0):
                g.addEdge(int(row.iloc[0].split("D")[1]), int(row.iloc[1].split("D")[1]))
            # print("Service")

    s = int(source_device.split("D")[1]) ; d = int(destination_device.split("D")[1])
    print ("Following are all different paths from % d to % d :" %(s, d))
    global all_line_x,all_line_y
    all_line_x = []
    all_line_y = []
    g.printAllPaths(s, d)
    # print(all_line_x,all_line_y)

class NavigationLayout(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(2)
        # self.setFixedSize(400,350)

        heading = QLabel("Navigation Configuration Panel")
        heading.setFont(QFont("Arial", 15))
        heading.setAlignment(Qt.AlignCenter)

        #CheckBox for choosing conditions for routing
        head2 = QLabel("Select Metrics",self)
        self.checkBox1 = QCheckBox("Relation")
        self.checkBox1.setChecked(True)
        self.combox1 = QComboBox()


        self.checkBox2 = QCheckBox("Protocol")
        self.checkBox2.setChecked(True)
        self.checkBox2_1 = QCheckBox("Wifi")
        self.checkBox2_1.setChecked(True)
        self.checkBox2_2 = QCheckBox("Bluetooth")
        self.checkBox2_3 = QCheckBox("GSM")
        self.checkBox2_4 = QCheckBox("ZigBee")
        protocol_grid = QGridLayout()
        protocol_grid.addWidget(self.checkBox2_1,0,0)
        protocol_grid.addWidget(self.checkBox2_2,0,1)
        protocol_grid.addWidget(self.checkBox2_3,0,2)
        protocol_grid.addWidget(self.checkBox2_4,0,3)

        vLayout_protocol = QVBoxLayout()
        vLayout_protocol.addWidget(self.checkBox2)
        vLayout_protocol.addLayout(protocol_grid)

        self.checkBox3 = QCheckBox("Same Services")

        vLayout1 = QVBoxLayout()
        vLayout1.addWidget(head2)
        vLayout1.addWidget(self.checkBox1)
        vLayout1.addLayout(vLayout_protocol)
        vLayout1.addWidget(self.checkBox3)
        vLayout1.setAlignment(Qt.AlignCenter)

        # Dropdown for Sevice b/w two device
        head3 = QLabel("Choose Source",self)
        head4 = QLabel("Choose Destination",self)
        self.source = QComboBox(self)
        self.source.addItems(list(added_dataframe['Device_id']))
        self.destination = QComboBox(self)
        self.destination.addItems(list(added_dataframe['Device_id']))
        vLayout = QVBoxLayout()
        vLayout.addWidget(head3)
        vLayout.addWidget(self.source)
        vLayout.addWidget(head4)
        vLayout.addWidget(self.destination)
        # hLayout2 = QHBoxLayout()
        # hLayout2.addWidget(head3)
        # hLayout2.addLayout(hLayout)

        head5 = QLabel("Choose Service",self)
        self.choose_service = QComboBox(self)
        sensor_data = session_path+"/sensor.csv"
        try :
            sensor_data = pd.read_csv(sensor_data)
            sensor_name = list(set(list(sensor_data['Sensor_name'])))
        except:
            sensor_name = ["Dynamic Model"]
        self.choose_service.addItems(sensor_name)
        vLayout4 = QVBoxLayout()
        vLayout4.addWidget(head5)
        vLayout4.addWidget(self.choose_service)
        vLayout4.setAlignment(Qt.AlignCenter | Qt.AlignRight)

        head4 = QLabel("Choose Theoritical/AI Method",self)
        self.algo_class = QComboBox(self)
        path = "models/Classification"
        class_models = [i.split("_")[0] for i in os.listdir(path)]
        class_models.insert(0,"Theoritical Method")
        self.algo_class.addItems(class_models)
        hLayout3 = QHBoxLayout()
        hLayout3.addWidget(head4)
        hLayout3.addWidget(self.algo_class)

        hLayout_source_service = QHBoxLayout()
        hLayout_source_service.addLayout(vLayout)
        hLayout_source_service.addLayout(vLayout4)

        vLayout_source_service_ai = QVBoxLayout()
        vLayout_source_service_ai.addLayout(hLayout_source_service)
        vLayout_source_service_ai.addLayout(hLayout3)

        source_service_ai  = QFrame()
        source_service_ai.setLayout(vLayout_source_service_ai)
        source_service_ai.setFrameStyle(2)

        hLayout_end = QHBoxLayout()
        # vLayout_end.addLayout(vLayout)
        hLayout_end.addLayout(vLayout1)
        hLayout_end.addWidget(source_service_ai)

        vLayout_end = QVBoxLayout()
        vLayout_end.addWidget(heading)
        vLayout_end.addLayout(hLayout_end)

        self.setLayout(vLayout_end)

class ClassificationLayout(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(2)

        heading = QLabel("Classification Configuration Panel")
        heading.setFont(QFont("Arial", 15))
        heading.setAlignment(Qt.AlignCenter)

        head = QLabel("Choose Classsification Algorithm",self)
        self.options = QComboBox(self)
        # class_models = ["ANN","KNN","Naive Bayes","Decision Tree"]
        path = "models/Classification"
        class_models = [i.split("_")[0] for i in os.listdir(path)]
        self.options.addItems(class_models)


        vLayout = QVBoxLayout()
        vLayout.addWidget(heading)
        vLayout.addWidget(head)
        vLayout.addWidget(self.options)

        self.setLayout(vLayout)


class ClusteringLayout(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(2)

        heading = QLabel("Clustering Configuration Panel")
        heading.setFont(QFont("Arial", 15))
        heading.setAlignment(Qt.AlignCenter)

        head = QLabel("Choose Clustering Algorithm",self)
        self.options = QComboBox(self)
        # class_models = ["K-Means","Gaussian Mixture"]
        path = "models/Clustering"
        cluss_models = [i.split("_")[0] for i in os.listdir(path)]
        self.options.addItems(cluss_models)
        vLayout = QVBoxLayout()
        vLayout.addWidget(heading)
        vLayout.addWidget(head)
        vLayout.addWidget(self.options)

        self.setLayout(vLayout)

class AppDemo(QMainWindow):
    def __init__(self,path):
        super().__init__()
        self.resize(1000, 800)
        mainLayout = QGridLayout()
        global session_path
        session_path = str(path)

        self.layout_name = True

        self.canvas = Canvas(self, width=16, height=5.8)
        self.canvas.draw()
        self.widget = QWidget()
        self.scroll = QScrollArea(self.widget)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.horizontalScrollBar().setEnabled(False)
        self.scroll.setWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.canvas.mpl_connect("scroll_event", self.scrolling)

        heading = QLabel("Algorithm")
        heading.setAlignment(Qt.AlignCenter)
        heading.setFont(QFont("Arial", 15))


        self.button_classification = QPushButton("Classification")
        self.button_clustering = QPushButton("Clustering")
        self.button_navigation = QPushButton("Navigation")
        self.button_classification.clicked.connect(self.classification_button)
        self.button_clustering.clicked.connect(self.clustering_button)
        self.button_navigation.clicked.connect(self.navigation_button)

        hLayout_menu1 = QHBoxLayout()
        hLayout_menu1.addWidget(self.button_classification)
        hLayout_menu1.addWidget(self.button_clustering)

        # Dropdown for choosing file
        no_need =["added.csv","sensor.csv"]
        files_set = set()
        for i in os.listdir(str(session_path)):
            if(i not in no_need):
                files_set.add(i.split("-",1)[1].split(".csv")[0])
        head1 = QLabel("Select Simulated Data",self)
        self.file = QComboBox(self)
        self.file.addItems(list(files_set))
        self.file.currentIndexChanged.connect(self.file_function)
        self.file_function(0)

        self.back_button = QPushButton("Back")
        self.back_button.setFixedSize(70,30)
        self.back_button.clicked.connect(self.button_back)
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.back_button)
        hLayout.addWidget(heading)

        vLayout = QVBoxLayout()
        vLayout.addLayout(hLayout)
        self.training_button = QPushButton("Code Editor")
        self.training_button.clicked.connect(self.button_training)

        vLayout_main = QVBoxLayout()
        vLayout_main.addLayout(hLayout_menu1)
        vLayout_main.addWidget(self.training_button)
        frame_main = QFrame()
        frame_main.setFrameStyle(2)
        frame_main.setLayout(vLayout_main)

        self.own_naviagtion_button = QPushButton("Code Editor")
        self.own_naviagtion_button.clicked.connect(self.button_own_naviagtion)

        vLayout_editor = QVBoxLayout()
        vLayout_editor.addWidget(self.button_navigation)
        vLayout_editor.addWidget(self.own_naviagtion_button)
        frame_editor = QFrame()
        frame_editor.setFrameStyle(2)
        frame_editor.setLayout(vLayout_editor)


        hLayout = QHBoxLayout()
        hLayout.addWidget(frame_main)
        hLayout.addWidget(frame_editor)
        vLayout.addLayout(hLayout)
        vLayout.addWidget(head1)
        vLayout.addWidget(self.file)

        # layout.addWidget(self.button)

        self.button1 = QPushButton('Show paths')
        self.button3 = QPushButton('Plot Devices')
        self.button4 = QPushButton('Plot based on Services')
        self.button5 = QPushButton('ACO')
        self.button1.clicked.connect(self.navigation_plot_button)
        self.button3.clicked.connect(self.navigation_plot_button_devices)
        self.button4.clicked.connect(self.navigation_plot_button_services)
        self.button5.clicked.connect(self.navigation_plot_button_ant)
        self.button1.setToolTip("1.Choose metrics\n2.Choose source & dest\n3.Choose method")
        self.button3.setToolTip("1.Choose metrics")
        self.button5.setToolTip("On Click gives Ant Colony Optimisation")
        self.button4.setToolTip("1.Choose metrics\n2.Choose source & dest\n3.Choose Service\n4.Choose method")
        self.button2 = QPushButton('Statistics Report')
        self.button6 = QPushButton('Statistics Details')
        self.comboBox = QComboBox()
        self.comboBox.addItems(["Classification Report","Confusion Matrix","Comparision"])
        self.but = QPushButton("Save Image")

        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.button3)
        self.hlayout.addWidget(self.button5)
        self.hlayout.addWidget(self.button1)
        self.hlayout.addWidget(self.button4)

        self.vLayout_end = QGridLayout()
        self.algoArea = NavigationLayout()
        self.vLayout_end.addWidget(self.algoArea,0,0)
        self.vLayout_end.addLayout(self.hlayout,1,0)

        # hLayout_menu.addLayout(vLayout_end)

        hlayout = QHBoxLayout()
        hlayout.addLayout(vLayout)
        hlayout.addLayout(self.vLayout_end)

        layout = QVBoxLayout()
        # layout.addLayout(hLayout_menu)
        layout.addLayout(hlayout)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.scroll)


        mainLayout.addLayout(layout,0,0)
        # mainLayout.addLayout(vLayout_end,0,1)

        #Menu Layout
        #Creating navigation menu
        file_menu = self.menuBar().addMenu("&Navigate")
        open_static_action = QAction("Static Model", self)
        open_static_action.setStatusTip("Static Model")
        open_static_action.triggered.connect(self.static_button)
        file_menu.addAction(open_static_action)

        open_dynamic_action = QAction("Dynamic Model", self)
        open_dynamic_action.setStatusTip("Dynamic Model")
        open_dynamic_action.triggered.connect(self.dynamic_button)
        file_menu.addAction(open_dynamic_action)

        open_envi_action = QAction("Environment Model", self)
        open_envi_action.setStatusTip("Environment Model")
        open_envi_action.triggered.connect(self.envi_button)
        file_menu.addAction(open_envi_action)

        # creating a help menu bar
        help_menu = self.menuBar().addMenu("&Help")
        open_help_action = QAction("Help", self)
        open_help_action.triggered.connect(self.help_open)
        help_menu.addAction(open_help_action)



        self.setWindowTitle('RESULTS & STATISTICS')

        scrollArea = QScrollArea()
        widget = QWidget()
        widget.setLayout(mainLayout)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(widget)
        # self.setLayout(mainLayout)
        self.setCentralWidget(scrollArea)

        self.showMaximized()

    def full_extent(self,ax_new, pad=0.0):
        ax_new.figure.canvas.draw()
        items = ax_new.get_xticklabels() + ax_new.get_yticklabels()
        #    items += [ax, ax.title, ax.xaxis.label, ax.yaxis.label]
        items += [ax_new, ax_new.title]
        bbox = Bbox.union([item.get_window_extent() for item in items])

        return bbox.expanded(1.0 + pad, 1.0 + pad)

    def save_figure_new(self):
        filetypes = self.canvas.get_supported_filetypes_grouped()
        sorted_filetypes = sorted(filetypes.items())
        default_filetype = self.canvas.get_default_filetype()

        startpath = os.path.expanduser(mpl.rcParams['savefig.directory'])
        start = os.path.join(startpath, self.canvas.get_default_filename())
        filters = []
        selectedFilter = None
        for name, exts in sorted_filetypes:
            exts_list = " ".join(['*.%s' % ext for ext in exts])
            filter = '%s (%s)' % (name, exts_list)
            if default_filetype in exts:
                selectedFilter = filter
            filters.append(filter)
        filters = ';;'.join(filters)

        fname, filter = qt_compat._getSaveFileName(
            self.canvas.parent(), "Choose a filename to save to", start,
            filters, selectedFilter)
        if fname:
            # Save dir for next time, unless empty str (i.e., use cwd).
            if startpath != "":
                mpl.rcParams['savefig.directory'] = os.path.dirname(fname)
            try:
                print(self.comboBox.currentIndex())
                if(self.comboBox.currentIndex()==0):
                    # extent = self.canvas.ax3.get_window_extent().transformed(self.canvas.fig.dpi_scale_trans.inverted())
                    extent = self.full_extent(self.canvas.ax3).transformed(self.canvas.fig.dpi_scale_trans.inverted())
                    self.canvas.fig.savefig(fname, bbox_inches=extent)
                if(self.comboBox.currentIndex()==1):
                    extent = self.full_extent(self.canvas.ax1).transformed(self.canvas.fig.dpi_scale_trans.inverted())
                    self.canvas.fig.savefig(fname, bbox_inches=extent)
                if(self.comboBox.currentIndex()==2):
                    extent = self.full_extent(self.canvas.ax2).transformed(self.canvas.fig.dpi_scale_trans.inverted())
                    self.canvas.fig.savefig(fname, bbox_inches=extent)
            except Exception as e:
                QMessageBox.critical(
                    self, "Error saving file", str(e),
                    QMessageBox.Ok,QMessageBox.NoButton)

    def scrolling(self, event):
        val = self.scroll.verticalScrollBar().value()
        if event.button =="down":
            self.scroll.verticalScrollBar().setValue(val+50)
        else:
            self.scroll.verticalScrollBar().setValue(val-50)

    def help_open(self):
        QMessageBox.information(self,"HELP","1.  The  user  can  choose  to  apply  Classification  or  Clustering  tech-niques  on  the  data  by  clicking  on  ’Statistics  details’  button  toobtain graphs and ’Statistics Report’ button to generate report.\n"
                                            "2.  When the user clicks on the ’Plot Devices’ button, devices satis-fying selected metric conditions are plotted.\n"
                                            "3.  When the user clicks on ’ACO’ button, ant colony optimisation isapplied to find shortest path for all previously added devices.\n"
                                            "4.  When the user clicks on ’Show paths’ button, all possible pathsand shortest path are plotted between source and destination.\n"
                                            "5.  When the user clicks on ’Plot based on Services’ button, shortestpath between source and destination is plotted based on the spe-cific service metric chosen from the drop down which works as afilter.\n"
                                            "6.  User  can  save  combined  plots  by  clicking  on  the  ’Save’  symbolin the toolbar or save individual graphs by selecting graph namefrom the drop drop available.")

    def static_button(self):
        StaticModel.start()
        main_page.close()
    def dynamic_button(self):
        DynamicModel.start()
        main_page.close()
    def envi_button(self):
        EnvironmentModel.start()
        main_page.close()

    def button_back(self):
        main_page.close()

    def button_own_naviagtion(self):
        TrainingCode.start_navigation(preprocessed,session_path)
        main_page.close()

    def button_training(self):
        TrainingCode.start(preprocessed,session_path)
        main_page.close()

    def classification_button(self):
        if(self.layout_name != False):
            self.canvas.ax.remove()
            self.canvas.ax1 = self.canvas.fig.add_subplot(222)
            self.canvas.ax2 = self.canvas.fig.add_subplot(212)
            self.canvas.ax3 = self.canvas.fig.add_subplot(221)
            self.canvas.ax1.clear()
            self.canvas.ax2.clear()
            self.canvas.ax3.clear()
            self.canvas.draw()
            self.layout_name =False

            self.algoArea.deleteLater()
            self.button1.deleteLater()
            self.button3.deleteLater()
            self.button4.deleteLater()
            self.button5.deleteLater()
            self.hlayout.deleteLater()
            self.algoArea = ClassificationLayout()
            self.button2 = QPushButton('Statistics Report')
            self.button6 = QPushButton('Statistics Details')

            self.button6.clicked.connect(self.classification_plot1_button)
            self.button2.clicked.connect(self.classification_plot_button)
            self.vLayout_end.addWidget(self.algoArea,0,0)

            self.comboBox = QComboBox()
            self.comboBox.addItems(["Classification Report","Confusion Matrix","Comparision"])
            self.but = QPushButton("Save Image")
            self.but.clicked.connect(self.save_figure_new)
            hLayout_save = QHBoxLayout()
            hLayout_save.addWidget(self.comboBox)
            hLayout_save.addWidget(self.but)

            buttonLayout = QHBoxLayout()
            buttonLayout.addWidget(self.button2)
            buttonLayout.addWidget(self.button6)
            vLayout = QVBoxLayout()
            vLayout.addLayout(buttonLayout)
            vLayout.addLayout(hLayout_save)
            self.vLayout_end.addLayout(vLayout,1,0)
        else:
            self.canvas.ax1.clear()
            self.canvas.ax2.clear()
            self.canvas.ax3.clear()
            #For CLasssification to clustering
            self.algoArea.deleteLater()
            self.button2.deleteLater()
            self.button6.deleteLater()
            self.but.deleteLater()
            self.comboBox.deleteLater()
            self.algoArea = ClassificationLayout()
            self.button2 = QPushButton('Statistics Report')
            self.button6 = QPushButton('Statistics Details')
            self.button6.clicked.connect(self.classification_plot1_button)
            self.button2.clicked.connect(self.classification_plot_button)
            self.vLayout_end.addWidget(self.algoArea,0,0)

            self.comboBox = QComboBox()
            self.comboBox.addItems(["Classification Report","Confusion Matrix","Comparision"])
            self.but = QPushButton("Save Image")
            self.but.clicked.connect(self.save_figure_new)
            hLayout_save = QHBoxLayout()
            hLayout_save.addWidget(self.comboBox)
            hLayout_save.addWidget(self.but)

            buttonLayout = QHBoxLayout()
            buttonLayout.addWidget(self.button2)
            buttonLayout.addWidget(self.button6)
            vLayout = QVBoxLayout()
            vLayout.addLayout(buttonLayout)
            vLayout.addLayout(hLayout_save)
            self.vLayout_end.addLayout(vLayout,1,0)

    def classification_plot1_button(self):
        self.canvas.ax1.clear()
        self.canvas.ax2.clear()
        self.canvas.ax3.clear()

        filename = "models/Classification/"
        filename = filename + self.algoArea.options.currentText()+"_model.sav"

        loaded_model = joblib.load(filename)
        x = dataframe_new.iloc[:,2:13]
        x.drop(["X_GPS","Y_GPS"],axis=1,inplace=True)
        y = dataframe_new.iloc[:,13:14]
        x_dataset = x.values
        y_dataset = y.values
        pred_y = loaded_model.predict(x_dataset)
        class_report = classification_report(y_dataset, pred_y)
        QMessageBox.information(self,"Classification Report",str(class_report))

    def classification_plot_button(self):
        self.canvas.ax1.clear()
        self.canvas.ax2.clear()
        self.canvas.ax3.clear()

        filename = "models/Classification/"
        filename = filename + self.algoArea.options.currentText()+"_model.sav"

        loaded_model = joblib.load(filename)
        x = dataframe_new.iloc[:,2:13]
        x.drop(["X_GPS","Y_GPS"],axis=1,inplace=True)
        y = dataframe_new.iloc[:,13:14]
        x_dataset = x.values
        y_dataset = y.values
        pred_y = loaded_model.predict(x_dataset)

        #To get Labels of predicted Classes
        data = set(dataframe_new.Relation.unique())
        data_pred = set(pred_y)
        inter = data_pred.union(data)
        values = ['No-Rel', 'STOR', 'CLOR', 'SIBOR', 'GUOR', 'CWOR', 'GSTOR', 'SOR',
                  'OOR', 'POR','SROR']
        label = []
        for i in inter:
            label.append(values[i])


        #Classification report and spliting values for graph into diff lists
        class_report = classification_report(y_dataset, pred_y)
        # print(class_report)
        # QMessageBox.critical()
        lines = class_report.split("\n")[2:2+len(label)]
        accuracy = float(class_report.split("\n")[3+len(label)].split("                          ")[1].split("    ")[0])
        clas_x =[]
        value1_y = []
        value2_y = []
        value3_y = []

        for i in lines:
            temp = i.split("       ")
            clas_x.append(int(temp[1].split("    ")[1]))
            value1_y.append(float(temp[2].split("      ")[0]))
            value2_y.append(float(temp[2].split("      ")[1]))
            value3_y.append(float(temp[2].split("      ")[2]))
        # print(clas_x,value1_y,value2_y,value3_y)
        cm = confusion_matrix(y_dataset, pred_y)

        #Predicted Values converted to negative for bar chart
        y_test = []
        y_pred = []
        for i in range(0,len(y_dataset)):
            y_test.append(y_dataset[i][0])
            y_pred.append(-1*pred_y[i])
        # print(y_test,y_pred)
        x_devices = np.arange(len(y_test))
        # self.canvas.ax2.axes.plot(x_devices,y_test,color='r',label="Expected")
        # self.canvas.ax2.axes.plot(x_devices,y_pred,label="Predicted")
        label_ytick  = [ 'STOR', 'CLOR', 'SIBOR', 'GUOR', 'CWOR', 'GSTOR', 'SOR',
                   'OOR', 'POR','SROR']
        label_ytick = label_ytick[::-1]
        label_ytick = label_ytick+['No-Rel', 'STOR', 'CLOR', 'SIBOR', 'GUOR', 'CWOR', 'GSTOR', 'SOR',
                       'OOR', 'POR','SROR']
        #Drawing Predicted vs Expected values bar chart
        self.canvas.ax2.bar(x_devices,y_test,label="Theoretical")
        self.canvas.ax2.bar(x_devices,y_pred,label="Predicted")
        self.canvas.ax2.legend()
        self.canvas.ax2.set_xlabel("Device Numbers")
        self.canvas.ax2.set_ylabel("Predicted Relations")
        self.canvas.ax2.axis([0,len(y_test),-10,10])
        self.canvas.ax2.set_title("Comparision b/w Theoretical and Predicted")
        # self.canvas.ax2.set_xticks(np.arange(len(x_devices)))
        self.canvas.ax2.set_yticks(np.arange(-10,11))
        self.canvas.ax2.set_yticklabels(label_ytick)

        #For heatmap of Confusion Matrix
        self.canvas.ax1.imshow(cm,aspect='auto')
        self.canvas.ax1.set_xticks(np.arange(len(label)))
        self.canvas.ax1.set_yticks(np.arange(len(label)))
        #To Lable axis
        self.canvas.ax1.set_xticklabels(label)
        self.canvas.ax1.set_yticklabels(label)
        self.canvas.ax1.set_xlabel("Predicted")
        self.canvas.ax1.set_ylabel("Actual")
        self.canvas.ax1.set_title("Heatmap of Confusion Matrix")
        # Loop over data dimensions and create text annotations.
        for i in range(len(label)):
            for j in range(len(label)):
                text = self.canvas.ax1.text(j, i, cm[i, j],
                               ha="center", va="center", color="w")

        #Drawing bar graph for precision,recal,f1-score
        clas_x = np.asarray(clas_x)
        self.canvas.ax3.bar(clas_x-0.20,value1_y,width=0.25,color='r',label="Precision")
        self.canvas.ax3.bar(clas_x+0.00,value2_y,width=0.25,color = 'b',label="recall")
        self.canvas.ax3.bar(clas_x+0.25,value3_y,width=0.25,color= 'g',label="f1-score")
        self.canvas.ax3.axes.plot([-1,10],[accuracy,accuracy],label="accuracy")
        self.canvas.ax3.legend()
        self.canvas.ax3.set_xticks(np.arange(len(values)))
        self.canvas.ax3.set_xticklabels(values)
        self.canvas.ax3.set_xlabel("Relation")
        self.canvas.ax3.set_ylabel("Value")
        self.canvas.ax3.axis([-1,10,0,1])
        self.canvas.ax3.set_title("Classification Report")

        self.canvas.draw()
        # QMessageBox.information()
        # print(confusion_matrix(y_dataset, pred_y))
        # print(pred_y)
        # print(y_dataset)

    def clustering_plot1_button(self):
        self.canvas.ax1.clear()
        self.canvas.ax2.clear()
        self.canvas.ax3.clear()

        filename = "models/Clustering/"
        filename = filename + self.algoArea.options.currentText()+"_model.sav"
        filename_pca = "models/pca_model.sav"
        loaded_model = joblib.load(filename)
        loaded_pca_model = joblib.load(filename_pca)
        x = dataframe_new.iloc[:,2:13]
        x.drop(["X_GPS","Y_GPS"],axis=1,inplace=True)
        y = dataframe_new.iloc[:,13:14]
        x_dataset = x.values
        pca_x_dataset = loaded_pca_model.transform(x_dataset)
        #To change class to No relation and Yes Relation
        y_dataset = y.values
        test_y_class = []
        for i in y_dataset:
            if(i == 0):
                test_y_class.append([0])
            else:
                test_y_class.append([1])
        pred_y = loaded_model.predict(pca_x_dataset)
        class_report = classification_report(test_y_class, pred_y)
        QMessageBox.information(self,"Classification Report",str(class_report))

    def clustering_plot_button(self):
        self.canvas.ax1.clear()
        self.canvas.ax2.clear()
        self.canvas.ax3.clear()

        filename = "models/Clustering/"
        filename = filename + self.algoArea.options.currentText()+"_model.sav"

        # filename = "models/kmeans_model.sav"
        # if(self.algoArea.options.currentText()=="KMeans"):
        #     filename = "models/kmeans_model.sav"
        # elif(self.algoArea.options.currentText()=="Gaussian-Mixture"):
        #     filename = "models/Gaussian-Mixture_model_pca.sav"
        filename_pca = "models/pca_model.sav"
        loaded_model = joblib.load(filename)
        loaded_pca_model = joblib.load(filename_pca)
        x = dataframe_new.iloc[:,2:13]
        x.drop(["X_GPS","Y_GPS"],axis=1,inplace=True)
        y = dataframe_new.iloc[:,13:14]
        x_dataset = x.values
        pca_x_dataset = loaded_pca_model.transform(x_dataset)
        # print(pca_x_dataset)
        #To change class to No relation and Yes Relation
        y_dataset = y.values
        # test_y_class = []
        # for i in y_dataset:
        #     if(i == 0):
        #         test_y_class.append([0])
        #     else:
        #         test_y_class.append([1])
        pred_y = loaded_model.predict(pca_x_dataset)

        #To get Labels of predicted Classes
        # label = ["No Relation","Relation"]
        label = ['No-Rel', 'STOR', 'CLOR', 'SIBOR', 'GUOR', 'CWOR', 'GSTOR', 'SOR',
         'OOR', 'POR','SROR']
        y_data = []
        for i in y_dataset:
            y_data.append(i[0])
        length = set(pred_y).union(set(y_data))
        #Classification report and spliting values for graph into diff lists
        class_report = classification_report(y_data, pred_y)
        print(class_report)
        lines = class_report.split("\n")[2:2+len(length)]
        accuracy = float(class_report.split("\n")[3+len(length)].split("                          ")[1].split("    ")[0])
        clas_x =[]
        value1_y = []
        value2_y = []
        value3_y = []
        new_label = []
        for i in lines:
            temp = i.split("       ")
            clas_x.append(int(temp[1].split("   ")[1]))
            new_label.append(label[int(temp[1].split("   ")[1])])
            value1_y.append(float(temp[2].split("      ")[0]))
            value2_y.append(float(temp[2].split("      ")[1]))
            value3_y.append(float(temp[2].split("      ")[2]))
        # print(clas_x,value1_y,value2_y,value3_y)

        cm = confusion_matrix(y_data, pred_y)

        #Predicted Values sorted to classes for plot
        # x_no = []
        # y_no = []
        # x_yes = []
        # y_yes = []
        # for i in range(0,len(pred_y)):
        #     if(pred_y[i] == [0]):
        #         x_no.append(pca_x_dataset[i,0])
        #         y_no.append(pca_x_dataset[i,1])
        #     else:
        #         x_yes.append(pca_x_dataset[i,0])
        #         y_yes.append(pca_x_dataset[i,1])
        x_plot = [[],[],[],[],[],[],[],[],[],[],[]]
        y_plot = [[],[],[],[],[],[],[],[],[],[],[]]
        x_max = -9999999999
        y_max = -9999999999
        x_min = 0
        y_min = 0

        for i in range(0,len(pred_y)):
            if(x_min>pca_x_dataset[i,0]):
                x_min = pca_x_dataset[i,0]
            if(y_min>pca_x_dataset[i,1]):
                y_min = pca_x_dataset[i,1]
            if(x_max<pca_x_dataset[i,0]):
                x_max = pca_x_dataset[i,0]
            if(y_max<pca_x_dataset[i,1]):
                y_max = pca_x_dataset[i,1]
            x_plot[pred_y[i]].append(pca_x_dataset[i,0])
            y_plot[pred_y[i]].append(pca_x_dataset[i,1])
        #Drawing Scatter plot of Devices
        for i in range(0,len(x_plot)):
            self.canvas.ax2.scatter(x_plot[i],y_plot[i],label=label[i])
        # self.canvas.ax2.scatter(x_no,y_no,label="No Relation")
        # self.canvas.ax2.scatter(x_yes,y_yes,label="Relation")
        self.canvas.ax2.axis([int(x_min)-10,int(x_max)+100,int(y_min)-10,int(y_max)+10])
        self.canvas.ax2.legend()
        self.canvas.ax2.set_xlabel("PCA Feature 1")
        self.canvas.ax2.set_ylabel("PCA Feature 2")
        self.canvas.ax2.set_title("Clustering")


        #For heatmap of Confusion Matrix
        self.canvas.ax1.imshow(cm,aspect='auto')
        self.canvas.ax1.set_xticks(np.arange(len(new_label)))
        self.canvas.ax1.set_yticks(np.arange(len(new_label)))
        #To Lable axis
        self.canvas.ax1.set_xticklabels(new_label)
        self.canvas.ax1.set_yticklabels(new_label)
        self.canvas.ax1.set_xlabel("Predicted")
        self.canvas.ax1.set_ylabel("Actual")
        self.canvas.ax1.set_title("Heatmap of Confusion Matrix")
        # Loop over data dimensions and create text annotations.
        for i in range(len(new_label)):
            for j in range(len(new_label)):
                text = self.canvas.ax1.text(j, i, cm[i, j],
                                            ha="center", va="center", color="w")

        #Drawing bar graph for precision,recal,f1-score
        clas_x = np.asarray(clas_x)
        self.canvas.ax3.bar(clas_x-0.20,value1_y,width=0.25,color='r',label="Precision")
        self.canvas.ax3.bar(clas_x+0.00,value2_y,width=0.25,color = 'b',label="recall")
        self.canvas.ax3.bar(clas_x+0.25,value3_y,width=0.25,color= 'g',label="f1-score")
        self.canvas.ax3.axes.plot([-1,len(new_label)],[accuracy,accuracy],label="accuracy")
        self.canvas.ax3.legend()
        self.canvas.ax3.set_xticks(np.arange(len(new_label)))
        self.canvas.ax3.set_xticklabels(new_label)
        self.canvas.ax3.set_xlabel("Relation")
        self.canvas.ax3.set_ylabel("Value")
        self.canvas.ax3.axis([-1,len(new_label),0,1])
        self.canvas.ax3.set_title("Clustering Report")

        self.canvas.draw()
        # print(confusion_matrix(y_dataset, pred_y))
        # print(pred_y)
        # print(y_dataset)

    def clustering_button(self):
        if(self.layout_name != False ):
            #For Navigation to clustering
            self.canvas.ax.remove()
            self.canvas.ax1 = self.canvas.fig.add_subplot(222)
            self.canvas.ax2 = self.canvas.fig.add_subplot(212)
            self.canvas.ax3 = self.canvas.fig.add_subplot(221)
            self.canvas.ax1.clear()
            self.canvas.ax2.clear()
            self.canvas.ax3.clear()
            self.canvas.draw()
            self.layout_name =False

            self.algoArea.deleteLater()
            self.button1.deleteLater()
            self.button3.deleteLater()
            self.button4.deleteLater()
            self.button5.deleteLater()
            self.hlayout.deleteLater()
            self.algoArea = ClusteringLayout()
            self.button2 = QPushButton('Statistics Report')
            self.button6 = QPushButton('Statistics Details')
            self.button6.clicked.connect(self.clustering_plot1_button)
            self.button2.clicked.connect(self.clustering_plot_button)
            self.vLayout_end.addWidget(self.algoArea,0,0)

            self.comboBox = QComboBox()
            self.comboBox.addItems(["Clustering Report","Confusion Matrix","Clusters"])
            self.but =QPushButton("Save Image")
            self.but.clicked.connect(self.save_figure_new)
            hLayout_save = QHBoxLayout()
            hLayout_save.addWidget(self.comboBox)
            hLayout_save.addWidget(self.but)

            buttonLayout = QHBoxLayout()
            buttonLayout.addWidget(self.button2)
            buttonLayout.addWidget(self.button6)
            vLayout = QVBoxLayout()
            vLayout.addLayout(buttonLayout)
            vLayout.addLayout(hLayout_save)
            self.vLayout_end.addLayout(vLayout,1,0)

        else:
            self.canvas.ax1.clear()
            self.canvas.ax2.clear()
            self.canvas.ax3.clear()
            #For CLasssification to clustering
            self.algoArea.deleteLater()
            self.button2.deleteLater()
            self.button6.deleteLater()
            self.but.deleteLater()
            self.comboBox.deleteLater()
            self.algoArea = ClusteringLayout()
            self.button2 = QPushButton('Statistics Report')
            self.button6 = QPushButton('Statistics Details')
            self.button6.clicked.connect(self.clustering_plot1_button)
            self.button2.clicked.connect(self.clustering_plot_button)
            self.vLayout_end.addWidget(self.algoArea,0,0)

            self.comboBox = QComboBox()
            self.comboBox.addItems(["Clustering Report","Confusion Matrix","Clusters"])
            self.but =QPushButton("Save Image")
            self.but.clicked.connect(self.save_figure_new)
            hLayout_save = QHBoxLayout()
            hLayout_save.addWidget(self.comboBox)
            hLayout_save.addWidget(self.but)

            buttonLayout = QHBoxLayout()
            buttonLayout.addWidget(self.button2)
            buttonLayout.addWidget(self.button6)
            vLayout = QVBoxLayout()
            vLayout.addLayout(buttonLayout)
            vLayout.addLayout(hLayout_save)
            self.vLayout_end.addLayout(vLayout,1,0)

    def navigation_button(self):
        if(self.layout_name == False ):
            self.canvas.ax1.remove()
            self.canvas.ax2.remove()
            self.canvas.ax3.remove()
            self.canvas.ax = self.canvas.fig.add_subplot(111)
            self.canvas.ax.axis([0,700,0,700])
            self.canvas.draw()
            self.layout_name = True

            self.algoArea.deleteLater()
            self.button2.deleteLater()
            self.button6.deleteLater()
            self.but.deleteLater()
            self.comboBox.deleteLater()
            self.algoArea = NavigationLayout()
            self.button1 = QPushButton('Show paths')
            self.button3 = QPushButton('Plot Devices')
            self.button4 = QPushButton('Plot based on Services')
            self.button5 = QPushButton('ACO')
            self.button1.clicked.connect(self.navigation_plot_button)
            self.button3.clicked.connect(self.navigation_plot_button_devices)
            self.button4.clicked.connect(self.navigation_plot_button_services)
            self.button5.clicked.connect(self.navigation_plot_button_ant)
            self.button1.setToolTip("1.Choose metrics\n2.Choose source & dest\n3.Choose method")
            self.button3.setToolTip("1.Choose metrics")
            self.button5.setToolTip("On Click gives Ant Colony Optimisation")
            self.button4.setToolTip("1.Choose metrics\n2.Choose source & dest\n3.Choose Service\n4.Choose method")
            self.hlayout = QHBoxLayout()
            self.hlayout.addWidget(self.button3)
            self.hlayout.addWidget(self.button5)
            self.hlayout.addWidget(self.button1)
            self.hlayout.addWidget(self.button4)

            self.vLayout_end.addWidget(self.algoArea,0,0)
            self.vLayout_end.addLayout(self.hlayout,1,0)

    def navigation_plot_button_ant(self):
        total_shortest_path, total_distance = antocolony()
        grouped  = dataframe_new.groupby("Device_id")
        x = []
        y = []
        labels = []
        for name,group in grouped:
            labels.append(name)
            x.append(group['X_GPS'].values[0])
            y.append(group['Y_GPS'].values[0])
        #TO PLot devices
        self.canvas.ax.clear()
        self.canvas.ax.scatter(x,y)
        for i in range(0,len(x)):
            #To name them
            self.canvas.ax.annotate(labels[i], (x[i], y[i]))
        shortest_line_x=[]
        shortest_line_y=[]
        for i in total_shortest_path:
            shortest_line_x.append(x[i])
            shortest_line_y.append(y[i])

        self.canvas.ax.axes.plot(shortest_line_x,shortest_line_y,'r',marker='*',label="Shortest Path")
        self.canvas.ax.annotate("Distance"+str(round(total_distance,2)), (5, 650))
        self.canvas.ax.legend()
        self.canvas.ax.axis([0,700,0,700])
        self.canvas.draw()

    def navigation_plot_button_services(self):

            source_device  = self.algoArea.source.currentText()
            destination_device  = self.algoArea.destination.currentText()
            filename = "models/Classification/"

            x = dataframe_new.iloc[:,2:13]
            x.drop(["X_GPS","Y_GPS"],axis=1,inplace=True)
            y = dataframe_new.iloc[:,13:14]
            x_dataset = x.values
            if(self.algoArea.algo_class.currentText() == "Theoritical Method"):
                pred_y = y
            else:
                filename = filename + self.algoArea.algo_class.currentText()+"_model.sav"
                loaded_model = joblib.load(filename)
                pred_y = loaded_model.predict(x_dataset)
            dataframe_new["Predicted_Relation"] = pred_y

            if(source_device == destination_device):
                QMessageBox.critical(self,"ERROR","Same Device selected")
                return
            relation_enabled = False
            protocol_enabled = False
            service_enabled = False
            if(self.algoArea.checkBox1.isChecked()):
                relation_enabled= True
            if(self.algoArea.checkBox2.isChecked()):
                protocol_enabled= True
            if(self.algoArea.checkBox3.isChecked()):
                service_enabled= True

            # For Protocol check box
            protocol_selected  = []
            if(self.algoArea.checkBox2_1.isChecked()):
                protocol_selected.append(self.algoArea.checkBox2_1.text())
            if(self.algoArea.checkBox2_2.isChecked()):
                protocol_selected.append(self.algoArea.checkBox2_2.text())
            if(self.algoArea.checkBox2_3.isChecked()):
                protocol_selected.append(self.algoArea.checkBox2_3.text())
            if(self.algoArea.checkBox2_4.isChecked()):
                protocol_selected.append(self.algoArea.checkBox2_4.text())


            grouped  = dataframe_new.groupby("Device_id")
            x = []
            y = []
            labels = []
            added_dataframe = pd.read_csv(session_path+"/added.csv")
            for name,group in grouped:
                con = added_dataframe.loc[added_dataframe["Device_id"]==name,"Connectivity"].values[0]
                inter = set(con.split(",")).intersection(set(protocol_selected))
                if(len(inter)>=len(protocol_selected)):
                    labels.append(name)
                    x.append(group['X_GPS'].values[0])
                    y.append(group['Y_GPS'].values[0])
            # x = dataframe_new.iloc[:,9]
            # y = dataframe_new.iloc[:,10]
            self.canvas.ax.clear()
            self.canvas.ax.scatter(x,y)
            for i in range(0,len(x)):
                self.canvas.ax.annotate(labels[i], (x[i], y[i]))

            #Function for Floyds
            shortest_line_x,shortest_line_y,devices_in_path = weights(relation_enabled=relation_enabled,protocol_enabled=protocol_enabled,
                                                                      service_enabled=service_enabled,source_device=source_device,
                                                                      destination_device=destination_device,protocol_selected=protocol_selected)
            # print(devices_in_path)

            #TO add services
            for i in devices_in_path:
                application_id  = added_dataframe.loc[added_dataframe["Device_id"]==i,"Application_id_sensor"].values[0]
                if(not isNaN(application_id)):
                    list_application_id = list(application_id.split(","))
                    text = ""
                    for j in list_application_id:
                        print(labels.index(i),x[labels.index(i)],y[labels.index(i)])
                        sensor_data = pd.read_csv(session_path+"/sensor.csv")
                        values_sensor = sensor_data.loc[sensor_data["Application_id"]==j,["Value","Sensor_name"]].values
                        for k in values_sensor:
                            if(self.algoArea.choose_service.currentText() == k[1]):
                                text = text + k[1]+":"+k[0]+"\n"
                    text = text[:-1]
                    self.canvas.ax.annotate(text, (x[labels.index(i)]+5, y[labels.index(i)]+15))

            #Function for all path
            # allPath(relation_enabled=relation_enabled,protocol_enabled=protocol_enabled,
            #         service_enabled=service_enabled,source_device=source_device,
            #         destination_device=destination_device,protocol_selected=protocol_selected)

            # i =0
            # for i in range(0,len(all_line_x)-1):
            #     self.canvas.ax.axes.plot(all_line_x[i],all_line_y[i],'b')
            # if(i!=0):
            #     self.canvas.ax.axes.plot(all_line_x[i+1],all_line_y[i+1],'b',label="All Paths")

            self.canvas.ax.axes.plot(shortest_line_x,shortest_line_y,'r',marker='*',label="Shortest Path")

            self.canvas.ax.legend()
            self.canvas.ax.axis([0,700,0,700])
            self.canvas.draw()

    def navigation_plot_button_devices(self):

        relation_enabled = False
        protocol_enabled = False
        service_enabled = False
        if(self.algoArea.checkBox1.isChecked()):
            relation_enabled= True
        if(self.algoArea.checkBox2.isChecked()):
            protocol_enabled= True
        if(self.algoArea.checkBox3.isChecked()):
            service_enabled= True

        # For Protocol check box
        protocol_selected  = []
        if(self.algoArea.checkBox2_1.isChecked()):
            protocol_selected.append(self.algoArea.checkBox2_1.text())
        if(self.algoArea.checkBox2_2.isChecked()):
            protocol_selected.append(self.algoArea.checkBox2_2.text())
        if(self.algoArea.checkBox2_3.isChecked()):
            protocol_selected.append(self.algoArea.checkBox2_3.text())
        if(self.algoArea.checkBox2_4.isChecked()):
            protocol_selected.append(self.algoArea.checkBox2_4.text())

        grouped  = dataframe_new.groupby("Device_id")
        x = []
        y = []
        labels = []
        added_dataframe = pd.read_csv(session_path+"/added.csv")
        for name,group in grouped:
            con = added_dataframe.loc[added_dataframe["Device_id"]==name,"Connectivity"].values[0]
            inter = set(con.split(",")).intersection(set(protocol_selected))
            if(len(inter)>=len(protocol_selected)):
                labels.append(name)
                x.append(group['X_GPS'].values[0])
                y.append(group['Y_GPS'].values[0])

        self.canvas.ax.clear()
        self.canvas.ax.scatter(x,y)
        for i in range(0,len(x)):
            self.canvas.ax.annotate(labels[i], (x[i], y[i]))
        self.canvas.ax.axis([0,700,0,700])
        self.canvas.draw()

    def navigation_plot_button(self):

        source_device  = self.algoArea.source.currentText()
        destination_device  = self.algoArea.destination.currentText()
        filename = "models/Classification/"
        # filename = filename + self.algoArea.algo_class.currentText()+"_model.sav"
        # if(self.algoArea.algo_class.currentText()=="ANN"):
        #     filename = "models/Ann_model.sav"
        # elif(self.algoArea.algo_class.currentText()=="KNN"):
        #     filename = "models/KNN_model.sav"
        # elif(self.algoArea.algo_class.currentText()=="NB"):
        #     filename = "models/NB_model.sav"
        # elif(self.algoArea.algo_class.currentText()=="Decision Tree"):
        #     filename = "models/DecisionTree_model.sav"
        x = dataframe_new.iloc[:,2:13]
        x.drop(["X_GPS","Y_GPS"],axis=1,inplace=True)
        y = dataframe_new.iloc[:,13:14]
        x_dataset = x.values
        if(self.algoArea.algo_class.currentText() == "Theoritical Method"):
            pred_y = y
        else:
            filename = filename + self.algoArea.algo_class.currentText()+"_model.sav"
            loaded_model = joblib.load(filename)
            pred_y = loaded_model.predict(x_dataset)
        dataframe_new["Predicted_Relation"] = pred_y

        if(source_device == destination_device):
            QMessageBox.critical(self,"ERROR","Same Device selected")
            return
        relation_enabled = False
        protocol_enabled = False
        service_enabled = False
        if(self.algoArea.checkBox1.isChecked()):
            relation_enabled= True
        if(self.algoArea.checkBox2.isChecked()):
            protocol_enabled= True
        if(self.algoArea.checkBox3.isChecked()):
            service_enabled= True

        # For Protocol check box
        protocol_selected  = []
        if(self.algoArea.checkBox2_1.isChecked()):
            protocol_selected.append(self.algoArea.checkBox2_1.text())
        if(self.algoArea.checkBox2_2.isChecked()):
            protocol_selected.append(self.algoArea.checkBox2_2.text())
        if(self.algoArea.checkBox2_3.isChecked()):
            protocol_selected.append(self.algoArea.checkBox2_3.text())
        if(self.algoArea.checkBox2_4.isChecked()):
            protocol_selected.append(self.algoArea.checkBox2_4.text())

        grouped  = dataframe_new.groupby("Device_id")
        x = []
        y = []
        labels = []
        added_dataframe = pd.read_csv(session_path+"/added.csv")
        for name,group in grouped:
            con = added_dataframe.loc[added_dataframe["Device_id"]==name,"Connectivity"].values[0]
            inter = set(con.split(",")).intersection(set(protocol_selected))
            if(len(inter)>=len(protocol_selected)):
                labels.append(name)
                x.append(group['X_GPS'].values[0])
                y.append(group['Y_GPS'].values[0])
        # x = dataframe_new.iloc[:,9]
        # y = dataframe_new.iloc[:,10]
        self.canvas.ax.clear()
        self.canvas.ax.scatter(x,y)
        for i in range(0,len(x)):
            self.canvas.ax.annotate(labels[i], (x[i], y[i]))

        #Function for Floyds
        shortest_line_x,shortest_line_y,devices_in_path = weights(relation_enabled=relation_enabled,protocol_enabled=protocol_enabled,
                                                  service_enabled=service_enabled,source_device=source_device,
                                                  destination_device=destination_device,protocol_selected=protocol_selected)

        #TO Add Services
        # for i in devices_in_path:
        #     application_id  = added_dataframe.loc[added_dataframe["Device_id"]==i,"Application_id_sensor"].values[0]
        #     if(not isNaN(application_id)):
        #         print(labels.index(i),x[labels.index(i)],y[labels.index(i)])
        #         sensor_data = pd.read_csv(session_path+"/sensor.csv")
        #         values_sensor = sensor_data.loc[sensor_data["Application_id"]==application_id,["Value","Sensor_name"]].values
        #         text = ""
        #         for j in values_sensor:
        #             text = text + j[1]+":"+j[0]+"\n"
        #         text = text[:-1]
        #         self.canvas.ax.annotate(text, (x[labels.index(i)]+5, y[labels.index(i)]+15))

        #Function for all path
        allPath(relation_enabled=relation_enabled,protocol_enabled=protocol_enabled,
                service_enabled=service_enabled,source_device=source_device,
                destination_device=destination_device,protocol_selected=protocol_selected)
        i =0
        for i in range(0,len(all_line_x)-1):
            self.canvas.ax.axes.plot(all_line_x[i],all_line_y[i],'b')
        if(i!=0):
            self.canvas.ax.axes.plot(all_line_x[i+1],all_line_y[i+1],'b',label="All Paths")
        self.canvas.ax.axes.plot(shortest_line_x,shortest_line_y,'r',marker='*',label="Shortest Path")
        # self.canvas.ax.xlabel("X_GPS")
        # self.canvas.ax.ylabel("Y_GPS")
        self.canvas.ax.legend()
        self.canvas.ax.axis([0,700,0,700])
        self.canvas.draw()

    def file_function(self,index):
        file_entered = self.file.currentText()
        global moved_dataframe,added_dataframe,relation_dataframe,preprocessed
        moved_dataframe = pd.read_csv(session_path+"/"+"movedObjects-"+file_entered+".csv")
        added_dataframe = pd.read_csv(session_path+"/added.csv")
        relation_dataframe = pd.read_csv(session_path+"/"+"relationObjects-"+file_entered+".csv")

        global dataframe_new
        dataframe_new = preProcessing()
        preprocessed = session_path+"/"+"PreProcessed-"+file_entered+".csv"
        dataframe_new.to_csv(preprocessed,header=True,index=False)
        # filename = "models/Ann_model.sav"
        # loaded_model = joblib.load(filename)
        # x = dataframe_new.iloc[:,2:13]
        # x.drop(["X_GPS","Y_GPS"],axis=1,inplace=True)
        # y = dataframe_new.iloc[:,13:14]
        # x_dataset = x.values
        # pred_y = loaded_model.predict(x_dataset)
        # dataframe_new["Predicted_Relation"] = pred_y
        dataframe_new.info()

        # dataframe_new = pd.read_csv("/Users/saicharan/PycharmProjects/FYP/AfterPreprocessing.csv")
        # dataframe_new.info()
        # weights()

def start(date):
    global main_page
    main_page = AppDemo(date)
    main_page.show()
    return main_page

if __name__ == '__main__':
    app = QApplication(sys.argv)
    global main_page
    # main_page = AppDemo("2021-05-13 18:45:10.881902")
    # main_page = AppDemo("2021-05-09 18:01:06.975995")
    # main_page = AppDemo("2021-05-16 17:48:34.480828")
    # main_page = AppDemo("2021-05-19 19:14:55.252118")

    #For Environment
    main_page = AppDemo("/Users/saicharan/PycharmProjects/FYP/simulation_data/DynamicModel/2021-06-03 18:33:00.192093")
    main_page.show()
    sys.exit(app.exec_())
