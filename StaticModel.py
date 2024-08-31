import sched
import shutil
import sys
import datetime,os
import time

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, \
    QGridLayout, QLineEdit, QLabel, QFrame, QMessageBox, QButtonGroup, QTextEdit, QComboBox, QCheckBox, QRadioButton, \
    QMenuBar, QFormLayout, QScrollArea, QMainWindow, QDialog, QAction
from PyQt5.QtCore import Qt, QMimeData, QLine, QPoint, QTimer, QEventLoop
from PyQt5.QtGui import QDrag, QIcon, QPixmap, QDoubleValidator, QStandardItem, QStandardItemModel, QPainter, QPen, \
    QColor
from functools import partial
import pandas as pd
import random,math
import numpy as np

import DynamicModel
import EnvironmentModel


class Button(QPushButton):
    def __init__(self, button_text, parent):
        super().__init__(button_text, parent)
        self.setStyleSheet('width: 40px; height: 20px; font-size: 15px')

class DeviceFrameWork(QListWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        #TODO: Remove list later in end
        global FrameWorkValues
        FrameWorkValues = []
        global FrameWorkValue
        FrameWorkValue = {}
        l1  = QListWidgetItem("")
        FrameWorkValue["Object_id"] = l1
        FrameWorkValue["Device_id"]=l1
        FrameWorkValue["Device"]=l1
        FrameWorkValue["Connectivity"]=l1
        FrameWorkValue["Device Distribution"]=l1
        FrameWorkValue["Owner_id"]=l1
        FrameWorkValue["Owner_name"]=l1
        FrameWorkValue["Manufacturing_id"]=l1
        FrameWorkValue["Service_id"]=l1
        FrameWorkValue["Application_id"]=l1
        FrameWorkValue["Connectivity"]=l1

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        print("Entered :"+e.mimeData().text())
        self.setText(e.mimeData().text())

class Button_Device(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setStyleSheet("border-image:url(test.jpg);")
        # self.setStyleSheet("border-image:url(test.jpg);padding: 10px;width: 20px; height: 20px;color: blue; font-size: 20px;padding: 5 5 5 5;")


    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):

        super().mousePressEvent(e)

        if e.button() == Qt.RightButton:
            print('press')

class AddButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setParent(simLayout)
        self.setFixedSize(30,40)
        self.device_id =FrameWorkValue["Device_id"]
        self.device_connectivity =FrameWorkValue["Connectivity"]
        self.device_mobility = FrameWorkValue["Device_mobility"]
        hoverlist = ["Device_id","Device","Device Distribution","Connectivity"]
        hovertext = ""
        for i in FrameWorkValue:
            if(i in hoverlist):
                hovertext = hovertext+FrameWorkValue[i].text()
                hovertext = hovertext+"\n"
        hovertext = hovertext[:-1]
        self.setToolTip(hovertext)

class DesignArea(QFrame):

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFixedSize(700,650)
        self.setStyleSheet("background-color:white;")
        self.lines = []
        self.relation_line = [[],[],[],[],[],[],[],[],[],[],[]]
        self.realtion_lines = []
        self.circle_wifi = []
        self.circle_zigbee = []
        self.circle_gsm = []
        self.circle_bluetooth = []
        self.objectsPresent = []
        self.circle_activation = True

    def paintEvent(self,event):
        QFrame.paintEvent(self, event)

        #For relationship line
        if(len(self.relation_line[0])>0):
            painter11 = QPainter(self)
            pen11 = QPen(QColor("#d4d4d4"), 2)
            pen11.setStyle(Qt.SolidLine)
            painter11.setPen(pen11)
            for line in self.relation_line[0]:
                painter11.drawLine(line)
                first = line.p1()
                second = line.p2()
                painter11.drawText((first+second)/2,"STOR")
        if(len(self.relation_line[1])>0):
            painter12 = QPainter(self)
            pen12 = QPen(QColor("#9e4757"), 2)
            pen12.setStyle(Qt.SolidLine)
            painter12.setPen(pen12)
            for line in self.relation_line[1]:
                painter12.drawLine(line)
                first = line.p1()
                second = line.p2()
                painter12.drawText((first+second)/2,"SROR")
        if(len(self.relation_line[2])>0):
            painter13 = QPainter(self)
            pen13 = QPen(QColor("#c56c00"), 2)
            pen13.setStyle(Qt.SolidLine)
            painter13.setPen(pen13)
            for line in self.relation_line[2]:
                painter13.drawLine(line)
                first = line.p1()
                second = line.p2()
                painter13.drawText((first+second)/2,"GUOR")
        if(len(self.relation_line[3])>0):
            painter14 = QPainter(self)
            pen14 = QPen(QColor("#1ac500"), 2)
            pen14.setStyle(Qt.SolidLine)
            painter14.setPen(pen14)
            for line in self.relation_line[3]:
                painter14.drawLine(line)
                first = line.p1()
                second = line.p2()
                painter14.drawText((first+second)/2,"CWOR")
        if(len(self.relation_line[4])>0):
            painter15 = QPainter(self)
            pen15 = QPen(QColor("#5f3b00"), 2)
            pen15.setStyle(Qt.SolidLine)
            painter15.setPen(pen15)
            for line in self.relation_line[4]:
                painter15.drawLine(line)
                first = line.p1()
                second = line.p2()
                painter15.drawText((first+second)/2,"CLOR")
        if(len(self.relation_line[5])>0):
            painter16 = QPainter(self)
            pen16 = QPen(QColor("#785f36"), 2)
            pen16.setStyle(Qt.SolidLine)
            painter16.setPen(pen16)
            for line in self.relation_line[5]:
                painter16.drawLine(line)
                first = line.p1()
                second = line.p2()
                painter16.drawText((first+second)/2,"POR")
        if(len(self.relation_line[6])>0):
            painter17 = QPainter(self)
            pen17 = QPen(QColor("#4c4c4c"), 2)
            pen17.setStyle(Qt.SolidLine)
            painter17.setPen(pen17)
            for line in self.relation_line[6]:
                painter17.drawLine(line)
                first = line.p1()
                second = line.p2()
                painter17.drawText((first+second)/2,"GSTOR")
        if(len(self.relation_line[7])>0):
            painter18 = QPainter(self)
            pen18 = QPen(Qt.red, 2)
            pen18.setStyle(Qt.SolidLine)
            painter18.setPen(pen18)
            for line in self.relation_line[7]:
                painter18.drawLine(line)
                first = line.p1()
                second = line.p2()
                painter18.drawText((first+second)/2,"SIBOR")
        if(len(self.relation_line[8])>0):
            painter19 = QPainter(self)
            pen19 = QPen(QColor("#004fc5"), 2)
            pen19.setStyle(Qt.SolidLine)
            painter19.setPen(pen19)
            for line in self.relation_line[8]:
                painter19.drawLine(line)
                first = line.p1()
                second = line.p2()
                painter19.drawText((first+second)/2,"SOR")
        if(len(self.relation_line[9])>0):
            painter20 = QPainter(self)
            pen20 = QPen(QColor("#539e47"), 2)
            pen20.setStyle(Qt.SolidLine)
            painter20.setPen(pen20)
            for line in self.relation_line[9]:
                painter20.drawLine(line)
                first = line.p1()
                second = line.p2()
                painter20.drawText((first+second)/2,"OOR")

        #For link line
        if(len(self.lines)>0):
            painter = QPainter(self)
            pen = QPen(Qt.black, 2)
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            for line in self.lines:
                painter.drawLine(line)
        #For relationship line
        if(len(self.realtion_lines)>0):
            painter1 = QPainter(self)
            pen1 = QPen(Qt.red, 2)
            pen1.setStyle(Qt.SolidLine)
            painter1.setPen(pen1)
            for line in self.realtion_lines:
                painter1.drawLine(line)
        #For Circle
        if(len(self.circle_wifi)>0):
            painter2 = QPainter(self)
            pen2 = QPen(Qt.black, 2)
            pen2.setStyle(Qt.DashLine)
            painter2.setPen(pen2)
            for center in self.circle_wifi:
                painter2.drawEllipse(center,40,40)
        if(len(self.circle_bluetooth)>0):
            painter3 = QPainter(self)
            pen3 = QPen(Qt.blue, 2)
            pen3.setStyle(Qt.DashLine)
            painter3.setPen(pen3)
            for center in self.circle_bluetooth:
                painter3.drawEllipse(center,20,20)
        if(len(self.circle_gsm)>0):
            painter4 = QPainter(self)
            pen4 = QPen(Qt.green, 2)
            pen4.setStyle(Qt.DashLine)
            painter4.setPen(pen4)
            for center in self.circle_gsm:
                painter4.drawEllipse(center,30,30)
        if(len(self.circle_zigbee)>0):
            painter5 = QPainter(self)
            pen5 = QPen(Qt.yellow, 2)
            pen5.setStyle(Qt.DashLine)
            painter5.setPen(pen5)
            for center in self.circle_zigbee:
                painter5.drawEllipse(center,25,25)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):

        position = e.pos()
        l1  = QListWidgetItem(str(position.x())+","+str(position.y()))
        FrameWorkValue["GPS_Start"]=l1
        if(FrameWorkValue["Device"].text()!=""):
            #Reading the file
            added_dataframe = pd.read_csv(creating_filename)
            #To create device_id
            l1  = QListWidgetItem("D"+str(len(added_dataframe)+1))
            FrameWorkValue["Device_id"]=l1

            #Creating Button for Object on Design Area
            object_button = AddButton()
            self.objectsPresent.append(object_button)
            #Place image where the user has dropped the image.
            object_button.move(position)
            url = "object_images/"+(FrameWorkValue["Device"].text())+".jpg"
            object_button.setStyleSheet("border-image:url("+url+");width: 30px; height: 30px; font-size: 15px;color:black")
            object_button.show()

            #Circle Drawing
            centre = QPoint(position.x()+25,position.y()+25)
            # print(list(FrameWorkValue["Connectivity"].text().split(",")))
            if("Wifi" in list(FrameWorkValue["Connectivity"].text().split(",")) and centre not in simLayout.circle_wifi):
                simLayout.circle_wifi.append(centre)
                simLayout.update()
            if("Bluetooth" in list(FrameWorkValue["Connectivity"].text().split(",")) and centre not in simLayout.circle_bluetooth):
                simLayout.circle_bluetooth.append(centre)
                simLayout.update()
            if("GSM" in list(FrameWorkValue["Connectivity"].text().split(",")) and centre not in simLayout.circle_gsm):
                simLayout.circle_gsm.append(centre)
                simLayout.update()
            if("ZigBee" in list(FrameWorkValue["Connectivity"].text().split(",")) and centre not in simLayout.circle_zigbee):
                simLayout.circle_zigbee.append(centre)
                simLayout.update()

            #Convert data to text to save
            temp ={}
            for i in FrameWorkValue:
                temp[i]= FrameWorkValue[i].text()
            #To add to database
            added_dataframe = added_dataframe.append(temp,ignore_index=True)
            added_dataframe.to_csv(creating_filename,header=True,index=False)
            e.setDropAction(Qt.MoveAction)

            #To add Values to the Combo-box
            linkArea.device1.addItem(FrameWorkValue["Device_id"].text())
            linkArea.device2.addItem(FrameWorkValue["Device_id"].text())
            relationArea.device1.addItem(FrameWorkValue["Device_id"].text())
            relationArea.device2.addItem(FrameWorkValue["Device_id"].text())
            e.accept()

class ProtocolButton(QPushButton):
    def __init__(self,text):
        super().__init__(text)
        self.setStyleSheet('width: 50px; height: 20px; font-size: 15px')


    def mousePressEvent(self, e):
        super().mousePressEvent(e)

        if e.button() == Qt.LeftButton:
            # print('press')

            text_selected = self.text()

            # To Get Values from QList
            # items = []
            # for i in range(simLayout1.count()):
            #     items.append(simLayout1.item(i))

            for i in FrameWorkValues:
                if(i.text() in Protocol_list):
                    simLayout1.takeItem(simLayout1.row(i))
                    FrameWorkValues.remove(i)
                    l1  = QListWidgetItem(text_selected)
                    FrameWorkValues.append(l1)
                    simLayout1.addItem(l1)
                    return
            l1  = QListWidgetItem(text_selected)
            FrameWorkValues.append(l1)
            simLayout1.addItem(l1)

class ProtocolGroup(QFrame):
    def __init__(self):
        super().__init__()
        # global protocol_entered
        # protocol_entered = None
        self.setFrameStyle(2)
        vLayout = QVBoxLayout()
        global Protocol_list
        Protocol_list = ["ZiggBee","Wi-Fi","Bluetooth","GSM","Wi-Max"]
        vLayout.addWidget(QLabel("Protocol"))
        for i in Protocol_list:
            vLayout.addWidget(ProtocolButton(i))
        self.setLayout(vLayout)

class DeviceDistributionButton(QPushButton):
    def __init__(self,text):
        super().__init__(text)
        self.setStyleSheet('width: 40px; height: 20px; font-size: 15px')
        self.setFixedSize(175,35)


    def mousePressEvent(self, e):
        super().mousePressEvent(e)

        if e.button() == Qt.LeftButton:
            text_selected = self.text()
            for i in FrameWorkValue:
                j = FrameWorkValue[i]
                temp = j.text()
                if(temp in ["Static","Random"]):
                    simLayout1.takeItem(simLayout1.row(j))
                    l1  = QListWidgetItem(text_selected)
                    FrameWorkValue["Device Distribution"]=l1
                    simLayout1.addItem(l1)
                    return
            l1  = QListWidgetItem(text_selected)
            FrameWorkValue["Device Distribution"]=l1
            simLayout1.addItem(l1)

class DeviceDistribution(QFrame):
    def __init__(self):
        super().__init__()
        # global DeviceDistribution_list
        self.setFrameStyle(2)
        self.setFixedSize(350,100)
        vLayout = QVBoxLayout()
        hLayout = QHBoxLayout()
        DeviceDistribution_list = ["Static","Random"]
        vLayout.addWidget(QLabel("Device Distribution"),Qt.AlignCenter)
        for i in DeviceDistribution_list:
            hLayout.addWidget(DeviceDistributionButton(i))
        vLayout.addLayout(hLayout)
        self.setLayout(vLayout)

class Distribution(QFrame):
    def __init__(self):
        super().__init__()
        # global DeviceDistribution_list
        self.setFrameStyle(2)
        self.setFixedSize(350,100)
        vLayout = QVBoxLayout()
        hLayout = QHBoxLayout()
        DeviceDistribution_list = ["Random","Uniform"]
        vLayout.addWidget(QLabel("Distribution"))
        for i in DeviceDistribution_list:
            hLayout.addWidget(QPushButton(i))
        vLayout.addLayout(hLayout)
        self.setLayout(vLayout)

class LinkArea(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(2)
        self.setFixedSize(300,150)
        #To read Data From database
        self.added_dataframe = pd.read_csv(creating_filename)
        self.resize(400,200)
        self.lay = QVBoxLayout()
        head = QLabel("Choose Devices to establish link",self)
        self.device1 = QComboBox(self)
        self.device1.addItems(list(self.added_dataframe["Device_id"]))
        self.device1.setFixedWidth(100)
        self.device2 = QComboBox(self)
        self.device2.addItems(list(self.added_dataframe["Device_id"]))
        self.device2.setFixedWidth(100)
        but = QPushButton("Submit",self)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.device1)
        hLayout.addWidget(self.device2)

        but.clicked.connect(self.onClicking)

        self.lay.addWidget(head)
        self.lay.addLayout(hLayout)
        self.lay.addWidget(but)

        self.setLayout(self.lay)
        self.setWindowTitle("Link")


    #Function to check if value is nan
    def isNaN(self,string):
        return string != string

    def onClicking(self):
        entered_device1  = self.device1.currentText()
        entered_device2  = self.device2.currentText()
        if(entered_device1 == entered_device2):
            QMessageBox.critical(self,"ERROR","Same Device selected")
            return

        self.added_dataframe = pd.read_csv(creating_filename)
        device_id_list  = list(self.added_dataframe["Device_id"])
        # print(device_id_list)
        device1_index = device_id_list.index(entered_device1)
        device2_index = device_id_list.index(entered_device2)
        GPS_list  = list(self.added_dataframe["GPS_Start"])
        point1 = GPS_list[device1_index]
        point2 = GPS_list[device2_index]
        # print(int(point1.split(",")[0]),int(point1.split(",")[1]))
        #Drawing line
        line = QLine(int(point1.split(",")[0]),int(point1.split(",")[1]),int(point2.split(",")[0]),int(point2.split(",")[1]))
        if(line not in simLayout.lines):
            simLayout.lines.append(line)
            simLayout.update()
        #Enter Values to database
        #Enter Device1 link data
        if(self.isNaN(self.added_dataframe.loc[device1_index,"Link"])):
            self.added_dataframe.loc[device1_index,"Link"] = entered_device2
        #Checking if link already exists
        elif(entered_device2 in list((self.added_dataframe.loc[device1_index,"Link"]).split(","))):
            QMessageBox.critical(self,"ERROR","Link already exists")
            return
        else:
            self.added_dataframe.loc[device1_index,"Link"] = self.added_dataframe.loc[device1_index,"Link"]+","+entered_device2
        #Enter Device2 link data
        if(self.isNaN(self.added_dataframe.loc[device2_index,"Link"])):
            self.added_dataframe.loc[device2_index,"Link"] = entered_device1
        elif(entered_device1 in list((self.added_dataframe.loc[device2_index,"Link"]).split(","))):
            QMessageBox.critical(self,"ERROR","Link already exists")
            return
        else:
            self.added_dataframe.loc[device2_index,"Link"] = self.added_dataframe.loc[device2_index,"Link"]+","+entered_device1

        self.added_dataframe.to_csv(creating_filename,header=True,index=False)

        # self.hide()

class LinkButton(QPushButton):
    def __init__(self,title,parent):
        super().__init__(title,parent)
        self.setStyleSheet("border-image:url(image.png);padding: 5px;width: 20px; height: 20px;")
        # self.setStyleSheet('width: 40px; height: 20px; font-size: 15px')
        self.setFixedSize(175,35)

    def mousePressEvent(self, e):
        super().mouseMoveEvent(e)
        if e.button() == Qt.LeftButton:
            self.linkArea = LinkArea()
            # vLayoutofLinkArea.addWidget(self.linkArea)
            self.linkArea.show()

class RelationshipArea(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(2)
        self.setFixedSize(300,250)
        #To read Data From database
        self.added_dataframe = pd.read_csv(creating_filename)

        self.resize(400,200)
        self.lay = QVBoxLayout()
        head = QLabel("Choose Devices to establish Relationship",self)
        self.device1 = QComboBox(self)
        self.device1.addItems(list(self.added_dataframe["Device_id"]))
        self.device1.setFixedWidth(100)
        self.device2 = QComboBox(self)
        self.device2.addItems(list(self.added_dataframe["Device_id"]))
        self.device2.setFixedWidth(100)
        but = QPushButton("Submit",self)

        # self.device1.setPlaceholderText("Enter Device1 ID")
        # self.device2.setPlaceholderText("Enter Device2 ID")
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.device1)
        hLayout.addWidget(self.device2)

        #Relationship buttons
        gridLayoutOfRealtionship = QGridLayout()
        self.radio1 = QRadioButton("OOR")
        self.radio2 = QRadioButton("SOR")
        self.radio3 = QRadioButton("SIBOR")
        self.radio4 = QRadioButton("GSTOR")

        self.radio5 = QRadioButton("GUOR")
        self.radio6 = QRadioButton("STOR")
        self.radio7 = QRadioButton("SROR")
        self.radio8 = QRadioButton("POR")
        self.radio9 = QRadioButton("CLOR")
        self.radio10 = QRadioButton("CWOR")

        gridLayoutOfRealtionship.addWidget(self.radio1,1,1)
        gridLayoutOfRealtionship.addWidget(self.radio2,2,1)
        gridLayoutOfRealtionship.addWidget(self.radio3,3,1)
        gridLayoutOfRealtionship.addWidget(self.radio4,4,1)
        gridLayoutOfRealtionship.addWidget(self.radio5,1,2)
        gridLayoutOfRealtionship.addWidget(self.radio6,2,2)
        gridLayoutOfRealtionship.addWidget(self.radio7,3,2)
        gridLayoutOfRealtionship.addWidget(self.radio8,4,2)
        gridLayoutOfRealtionship.addWidget(self.radio9,5,2)
        gridLayoutOfRealtionship.addWidget(self.radio10,6,2)

        but.clicked.connect(self.onClicking)

        self.lay.addWidget(head,Qt.AlignCenter)
        self.lay.addLayout(hLayout)
        self.lay.addLayout(gridLayoutOfRealtionship)
        self.lay.addWidget(but)

        self.setLayout(self.lay)
        self.setWindowTitle("Relationship")

    #Function to check if value is nan
    def isNaN(self,string):
        return string != string

    def onClicking(self):
        entered_device1  = self.device1.currentText()
        entered_device2  = self.device2.currentText()
        realtionship_selected =""
        if(self.radio1.isChecked()):
            realtionship_selected=self.radio1.text()
        if(self.radio2.isChecked()):
            realtionship_selected =  self.radio2.text()
        if(self.radio3.isChecked()):
            realtionship_selected =  self.radio3.text()
        if(self.radio4.isChecked()):
            realtionship_selected =  self.radio4.text()
        if(self.radio5.isChecked()):
            realtionship_selected =  self.radio5.text()
        if(self.radio6.isChecked()):
            realtionship_selected =  self.radio6.text()
        if(self.radio7.isChecked()):
            realtionship_selected =  self.radio7.text()
        if(self.radio8.isChecked()):
            realtionship_selected =  self.radio8.text()
        if(self.radio9.isChecked()):
            realtionship_selected =  self.radio9.text()
        if(self.radio10.isChecked()):
            realtionship_selected =  self.radio10.text()

        if(entered_device1 == entered_device2):
            QMessageBox.critical(self,"ERROR","Same Device selected")
            return
        if(realtionship_selected == ""):
            QMessageBox.critical(self,"ERROR","Choose a realtionship")
            return

        self.added_dataframe = pd.read_csv(creating_filename)
        device_id_list  = list(self.added_dataframe["Device_id"])
        device1_index = device_id_list.index(entered_device1)
        device2_index = device_id_list.index(entered_device2)

        #If Already existing link selected to check in database
        linked_devices = self.added_dataframe.loc[device1_index,"Link"]
        if(self.isNaN(linked_devices)):
            QMessageBox.critical(self,"ERROR","No link Between Selected Devices")
            return
        linked_devices = list(linked_devices.split(","))
        if(entered_device2 not in linked_devices):
            QMessageBox.critical(self,"ERROR","No link Between Selected Devices")
            return

        GPS_list  = list(self.added_dataframe["GPS_Start"])
        point1 = GPS_list[device1_index]
        point2 = GPS_list[device2_index]
        relation_line = QLine(int(point1.split(",")[0])+10,int(point1.split(",")[1])+10,int(point2.split(",")[0])+10,int(point2.split(",")[1])+10)
        if(relation_line not in simLayout.realtion_lines):
            simLayout.realtion_lines.append(relation_line)
            simLayout.update()
        #Enter Values to database
        #Enter Device1 link data
        # print(entered_device2+":"+realtionship_selected)

        if(self.isNaN(self.added_dataframe.loc[device1_index,"Relationship"])):
            self.added_dataframe.loc[device1_index,"Relationship"] = entered_device2+":"+realtionship_selected
        # else:
        #     self.added_dataframe.loc[device1_index,"Relationship"] = self.added_dataframe.loc[device1_index,"Relationship"]+","+entered_device2+":"+realtionship_selected
        #Should add values or no or should update
        else:
            relations_present = list((self.added_dataframe.loc[device1_index,"Relationship"]).split(","))
            relation = [i.split(':', 1)[0] for i in relations_present]
            correspondning_relation = [i.split(':', 1)[1] for i in relations_present]
            #To Check if relationship already exists
            if(entered_device2 in relation):
                loc = relation.index(entered_device2)
                rel = ""
                for i in range(0,len(relation)):
                    if(i==loc):
                        rel = rel+relation[i]+":"+realtionship_selected+","
                    else:
                        rel = rel+relation[i]+":"+correspondning_relation[i]+","
                rel = rel[:-1]
                self.added_dataframe.loc[device1_index,"Relationship"] = rel
            else:
                self.added_dataframe.loc[device1_index,"Relationship"] = self.added_dataframe.loc[device1_index,"Relationship"]+","+entered_device2+":"+realtionship_selected

        #Enter Device2 link data
        if(self.isNaN(self.added_dataframe.loc[device2_index,"Relationship"])):
            self.added_dataframe.loc[device2_index,"Relationship"] = entered_device1+":"+realtionship_selected
        # else:
        #     self.added_dataframe.loc[device2_index,"Relationship"] = self.added_dataframe.loc[device2_index,"Relationship"]+","+entered_device1+":"+realtionship_selected
        else:
            relations_present = list((self.added_dataframe.loc[device2_index,"Relationship"]).split(","))
            relation = [i.split(':', 1)[0] for i in relations_present]
            correspondning_relation = [i.split(':', 1)[1] for i in relations_present]
            #To Check if relationship already exists
            if(entered_device1 in relation):
                loc = relation.index(entered_device1)
                rel = ""
                for i in range(0,len(relation)):
                    if(i==loc):
                        rel = rel+relation[i]+":"+realtionship_selected+","
                    else:
                        rel = rel+relation[i]+":"+correspondning_relation[i]+","
                rel = rel[:-1]
                self.added_dataframe.loc[device2_index,"Relationship"] = rel
            else:
                self.added_dataframe.loc[device2_index,"Relationship"] = self.added_dataframe.loc[device2_index,"Relationship"]+","+entered_device1+":"+realtionship_selected

        self.added_dataframe.to_csv(creating_filename,header=True,index=False)

        # self.hide()

class RelationshipButton(QPushButton):
    def __init__(self,title,parent):
        super().__init__(title,parent)
        self.setStyleSheet("border-image:url(image2.png);padding: 5px;width: 20px; height: 20px;")
        # self.setStyleSheet('width: 40px; height: 20px; font-size: 15px')
        self.setFixedSize(175,35)

    def mousePressEvent(self, e):
        super().mouseMoveEvent(e)
        if e.button() == Qt.LeftButton:
            self.relationshipArea = RelationshipArea()
            # vLayoutofrelationArea.addWidget(self.relationshipArea)
            self.relationshipArea.show()

#Consists of Link and Relationship buttons
class ConnectionType(QFrame):

    def __init__(self):
        super().__init__()
        # self.setFrameStyle(2)
        vLayout = QVBoxLayout()
        button1 = LinkButton("Link",self)
        button2 = RelationshipButton("Relationship",self)
        # vLayout.addWidget(QLabel("Connection Type"))
        vLayout.addWidget(button1)
        vLayout.addWidget(button2)
        self.setLayout(vLayout)

class InputArea(QFrame):
    def __init__(self):
        super().__init__()
        self.resize(350,200)
        #If button is clicked or no

        self.lay = QGridLayout()
        self.setFrameStyle(2)
        self.setFixedSize(720,350)
        self.checkBox1 = QCheckBox("Wifi")
        self.checkBox2 = QCheckBox("Bluetooth")
        self.checkBox3 = QCheckBox("GSM")
        self.checkBox4 = QCheckBox("ZigBee")

        # self.head = QLineEdit("INPUT DEVICE",self)
        # self.head.setReadOnly(True)

        self.input = QComboBox(self)
        self.input_list = ["Private","Public"]
        self.input.addItems(self.input_list)
        self.input.currentIndexChanged.connect(self.type_function)


        self.device = QComboBox(self)
        self.device_list = []

        self.type = QComboBox(self)
        self.type_list = ["Mobile","Static"]
        self.type.addItems(self.type_list)
        self.type.currentIndexChanged.connect(self.type_function)
        self.type_function(0)

        self.device.currentIndexChanged.connect(self.device_function)
        self.device_function(0)

        #Layout of CheckBoxes
        gridLayout = QVBoxLayout()
        heading_layout = QHBoxLayout()
        h1= QLabel("Protocol")
        h2= QLabel("Data Rate")
        h3= QLabel("Bandwidth")
        h4= QLabel("Battery")
        heading_layout.addWidget(h1)
        heading_layout.addWidget(h2)
        heading_layout.addWidget(h3)
        heading_layout.addWidget(h4)

        wifi_layout = QHBoxLayout()
        self.wifi_datarate = QLineEdit()
        self.wifi_datarate.setText("1000")
        self.wifi_datarate.setFixedSize(40,20)
        self.wifi_bandwidth = QLineEdit()
        self.wifi_bandwidth.setText("11000")
        self.wifi_bandwidth.setFixedSize(40,20)
        self.wifi_battery = QLineEdit()
        self.wifi_battery.setText("100")
        self.wifi_battery.setFixedSize(40,20)
        wifi_layout.addWidget(self.checkBox1)
        wifi_layout.addWidget(self.wifi_datarate)
        wifi_layout.addWidget(self.wifi_bandwidth)
        wifi_layout.addWidget(self.wifi_battery)

        bluetooth_layout = QHBoxLayout()
        self.bluetooth_datarate = QLineEdit()
        self.bluetooth_datarate.setText("250")
        self.bluetooth_datarate.setFixedSize(40,20)
        self.bluetooth_bandwidth = QLineEdit()
        self.bluetooth_bandwidth.setText("720")
        self.bluetooth_bandwidth.setFixedSize(40,20)
        self.bluetooth_battery = QLineEdit()
        self.bluetooth_battery.setText("100")
        self.bluetooth_battery.setFixedSize(40,20)
        bluetooth_layout.addWidget(self.checkBox2)
        bluetooth_layout.addWidget(self.bluetooth_datarate)
        bluetooth_layout.addWidget(self.bluetooth_bandwidth)
        bluetooth_layout.addWidget(self.bluetooth_battery)

        GSM_layout = QHBoxLayout()
        self.GSM_datarate = QLineEdit()
        self.GSM_datarate.setText("120")
        self.GSM_datarate.setFixedSize(40,20)
        self.GSM_bandwidth = QLineEdit()
        self.GSM_bandwidth.setText("900")
        self.GSM_bandwidth.setFixedSize(40,20)
        self.GSM_battery = QLineEdit()
        self.GSM_battery.setText("100")
        self.GSM_battery.setFixedSize(40,20)
        GSM_layout.addWidget(self.checkBox3)
        GSM_layout.addWidget(self.GSM_datarate)
        GSM_layout.addWidget(self.GSM_bandwidth)
        GSM_layout.addWidget(self.GSM_battery)

        zigbee_layout = QHBoxLayout()
        self.zigbee_datarate = QLineEdit()
        self.zigbee_datarate.setText("60")
        self.zigbee_datarate.setFixedSize(40,20)
        self.zigbee_bandwidth = QLineEdit()
        self.zigbee_bandwidth.setText("250")
        self.zigbee_bandwidth.setFixedSize(40,20)
        self.zigbee_battery = QLineEdit()
        self.zigbee_battery.setText("100")
        self.zigbee_battery.setFixedSize(40,20)
        zigbee_layout.addWidget(self.checkBox4)
        zigbee_layout.addWidget(self.zigbee_datarate)
        zigbee_layout.addWidget(self.zigbee_bandwidth)
        zigbee_layout.addWidget(self.zigbee_battery)

        gridLayout.addLayout(heading_layout)
        gridLayout.addLayout(wifi_layout)
        gridLayout.addLayout(bluetooth_layout)
        gridLayout.addLayout(GSM_layout)
        gridLayout.addLayout(zigbee_layout)

        self.but = QPushButton("Submit",self)
        self.but.setFixedSize(150,40)
        self.but.clicked.connect(self.onClicking)

        self.disablebut = QPushButton("Disable Range",self)
        self.disablebut.setFixedSize(150,40)
        self.disablebut.clicked.connect(self.onClicking_disable)

        self.enablebut = QPushButton("Enable Range",self)
        self.enablebut.setFixedSize(150,40)
        self.enablebut.clicked.connect(self.onClicking_enable)

        l1 =  QLabel("Private/Public")
        l2 = QLabel("Mobility")
        l3 = QLabel("Device Type")
        temp1 = QHBoxLayout()
        temp1.addWidget(l1)
        temp1.addWidget(self.input)
        temp2 =QHBoxLayout()
        temp2.addWidget(l2)
        temp2.addWidget(self.type)
        temp3 = QHBoxLayout()
        temp3.addWidget(l3)
        temp3.addWidget(self.device)

        vLayout1 = QVBoxLayout()
        vLayout1.addLayout(temp1)
        vLayout1.addLayout(temp2)
        vLayout1.addLayout(temp3)
        vLayout1.addLayout(gridLayout)

        #Profiling Part
        heading = QLabel("Object Profiling")
        heading.setAlignment(Qt.AlignCenter)
        l6= QLabel("Object Id")
        self.object_id = QLineEdit()
        self.object_id.setPlaceholderText("Enter Object Id")
        self.object_id.setFixedSize(150,30)
        l1= QLabel("Owner Id")
        self.owner_id = QLineEdit()
        self.owner_id.setPlaceholderText("Enter Owner Id")
        self.owner_id.setFixedSize(150,30)
        l2 = QLabel("Owner Name")
        self.owner_name = QLineEdit()
        self.owner_name.setPlaceholderText("Enter Owner Name")
        self.owner_name.setFixedSize(150,30)
        l3 = QLabel("Manufacturing Id")
        self.manufacturing_id = QLineEdit()
        self.manufacturing_id.setPlaceholderText("Enter Manufacturing ID")
        self.manufacturing_id.setFixedSize(150,30)
        l4 = QLabel("Service Id")
        self.service_id = QLineEdit()
        self.service_id.setPlaceholderText("Enter Service ID")
        self.service_id.setFixedSize(150,30)
        l5 = QLabel("Application Id")
        self.application_id = QLineEdit()
        self.application_id.setPlaceholderText("Enter Application ID")
        self.application_id.setFixedSize(150,30)

        #TODO: Enter Values to database
        vLayout2 = QFormLayout()
        vLayout2.addWidget(heading)
        vLayout2.addRow(l6,self.object_id)
        vLayout2.addRow(l1,self.owner_id)
        vLayout2.addRow(l2,self.owner_name)
        vLayout2.addRow(l3,self.manufacturing_id)
        vLayout2.addRow(l4,self.service_id)
        vLayout2.addRow(l5,self.application_id)

        vLayout3 = QVBoxLayout()
        vLayout3.addWidget(self.disablebut)
        vLayout3.addWidget(self.enablebut)
        self.lay.addLayout(vLayout1,0,0)
        self.lay.addLayout(vLayout2,0,2)
        self.lay.addLayout(vLayout3,1,1)
        self.lay.addWidget(self.but,1,2)

        self.setLayout(self.lay)
        self.setWindowTitle("INPUT DEVICE")

    def type_function(self,index):
        # print(index)
        self.device_dataframe = pd.read_csv("Input_sheet.csv")
        input_entered = self.input.currentText()
        type_entered = self.type.currentText()
        self.device.clear()
        # print(self.input_entered,self.type_entered)
        for i,row in self.device_dataframe.iterrows():
            if(row["Input"]==input_entered and row["Type"]==type_entered):
                self.device_list.append(row["Device"])
        self.device.addItems(self.device_list)
        del self.device_list[:]

    def device_function(self,index):
        # print(index)
        self.device_dataframe = pd.read_csv("Input_sheet.csv")
        input_entered = self.input.currentText()
        type_entered = self.type.currentText()
        device_entered = self.device.currentText()

        for i,row in self.device_dataframe.iterrows():
            if(row["Input"]==input_entered and row["Type"]==type_entered and row["Device"]==device_entered):
                con = list(row["Connectivity"].split(","))
                if(self.checkBox1.text() in con):
                    self.checkBox1.setChecked(True)
                else:
                    self.checkBox1.setChecked(False)
                if(self.checkBox2.text() in con):
                    self.checkBox2.setChecked(True)
                else:
                    self.checkBox2.setChecked(False)
                if(self.checkBox3.text() in con):
                    self.checkBox3.setChecked(True)
                else:
                    self.checkBox3.setChecked(False)
                if(self.checkBox4.text() in con):
                    self.checkBox4.setChecked(True)
                else:
                    self.checkBox4.setChecked(False)
                return

    def onClicking_disable(self):
        simLayout.circle_bluetooth= []
        simLayout.circle_wifi = []
        simLayout.circle_gsm = []
        simLayout.circle_zigbee = []
        simLayout.circle_activation = False
        simLayout.update()

    def onClicking_enable(self):
        simLayout.circle_activation = True
        objects = simLayout.objectsPresent
        for i in objects:
            centre = QPoint(i.x()+25,i.y()+25)
            if("Wifi" in list(i.device_connectivity.text().split(",")) and centre not in simLayout.circle_wifi):
                simLayout.circle_wifi.append(centre)
                simLayout.update()
            if("Bluetooth" in list(i.device_connectivity.text().split(",")) and centre not in simLayout.circle_bluetooth):
                simLayout.circle_bluetooth.append(centre)
                simLayout.update()
            if("GSM" in list(i.device_connectivity.text().split(",")) and centre not in simLayout.circle_gsm):
                simLayout.circle_gsm.append(centre)
                simLayout.update()
            if("ZigBee" in list(i.device_connectivity.text().split(",")) and centre not in simLayout.circle_zigbee):
                simLayout.circle_zigbee.append(centre)
                simLayout.update()

    def onClicking(self):

        #For Profiling
        # device_id_entered = self.device_id_entered.text()
        object_id_entered = self.object_id.text()
        owner_id_entered = self.owner_id.text()
        owner_name_entered = self.owner_name.text()
        manufacturing_id_entered = self.manufacturing_id.text()
        service_id_entered = self.service_id.text()
        application_id_entered = self.application_id.text()
        if(owner_id_entered=="" or owner_name_entered=="" or manufacturing_id_entered==""
                or service_id_entered=="" or application_id_entered==""):
            QMessageBox.critical(self,"ERROR","Profiling values not entered\n"
                                              "Like Owner ID,Owner Name,Manufacturing ID,Service ID, Apppllication ID")
            return

        if(FrameWorkValue["Object_id"].text()!=""):
            simLayout1.takeItem(simLayout1.row(FrameWorkValue["Object_id"]))
            l1  = QListWidgetItem(object_id_entered)
            FrameWorkValue["Object_id"]= l1
            simLayout1.addItem(l1)
        else:
            l1  = QListWidgetItem(object_id_entered)
            FrameWorkValue["Object_id"]= l1
            simLayout1.addItem(l1)
        if(FrameWorkValue["Owner_id"].text()!=""):
            simLayout1.takeItem(simLayout1.row(FrameWorkValue["Owner_id"]))
            l1  = QListWidgetItem(owner_id_entered)
            FrameWorkValue["Owner_id"]= l1
            simLayout1.addItem(l1)
        else:
            l1  = QListWidgetItem(owner_id_entered)
            FrameWorkValue["Owner_id"]= l1
            simLayout1.addItem(l1)
        if(FrameWorkValue["Owner_id"].text()!=""):
            simLayout1.takeItem(simLayout1.row(FrameWorkValue["Owner_id"]))
            l1  = QListWidgetItem(owner_id_entered)
            FrameWorkValue["Owner_id"]= l1
            simLayout1.addItem(l1)
        else:
            l1  = QListWidgetItem(owner_id_entered)
            FrameWorkValue["Owner_id"]= l1
            simLayout1.addItem(l1)

        if(FrameWorkValue["Owner_name"].text()!=""):
            simLayout1.takeItem(simLayout1.row(FrameWorkValue["Owner_name"]))
            l1  = QListWidgetItem(owner_name_entered)
            FrameWorkValue["Owner_name"]= l1
            simLayout1.addItem(l1)
        else:
            l1  = QListWidgetItem(owner_name_entered)
            FrameWorkValue["Owner_name"]= l1
            simLayout1.addItem(l1)
        if(FrameWorkValue["Manufacturing_id"].text()!=""):
            simLayout1.takeItem(simLayout1.row(FrameWorkValue["Manufacturing_id"]))
            l1  = QListWidgetItem(manufacturing_id_entered)
            FrameWorkValue["Manufacturing_id"]= l1
            simLayout1.addItem(l1)
        else:
            l1  = QListWidgetItem(manufacturing_id_entered)
            FrameWorkValue["Manufacturing_id"]= l1
            simLayout1.addItem(l1)
        if(FrameWorkValue["Service_id"].text()!=""):
            simLayout1.takeItem(simLayout1.row(FrameWorkValue["Service_id"]))
            l1  = QListWidgetItem(service_id_entered)
            FrameWorkValue["Service_id"]= l1
            simLayout1.addItem(l1)
        else:
            l1  = QListWidgetItem(service_id_entered)
            FrameWorkValue["Service_id"]= l1
            simLayout1.addItem(l1)
        if(FrameWorkValue["Application_id"].text()!=""):
            simLayout1.takeItem(simLayout1.row(FrameWorkValue["Application_id"]))
            l1  = QListWidgetItem(application_id_entered)
            FrameWorkValue["Application_id"]= l1
            simLayout1.addItem(l1)
        else:
            l1  = QListWidgetItem(application_id_entered)
            FrameWorkValue["Application_id"]= l1
            simLayout1.addItem(l1)

        # print(FrameWorkValue["Connectivity"].text())
        #For Connectivity
        text_selected =""
        if(self.checkBox1.isChecked()):
            text_selected = text_selected+self.checkBox1.text()+","
        if(self.checkBox2.isChecked()):
            text_selected = text_selected+self.checkBox2.text()+","
        if(self.checkBox3.isChecked()):
            text_selected = text_selected+self.checkBox3.text()+","
        if(self.checkBox4.isChecked()):
            text_selected = text_selected+self.checkBox4.text()+","
        #To remove extra ,
        text_selected = text_selected[:-1]
        connectivity_database = ["Wifi","Bluetooth","GSM","ZigBee"]
        previous_connectivity  = FrameWorkValue["Connectivity"]
        temp = False
        for i in previous_connectivity.text().split(","):
            if(i in connectivity_database):
                simLayout1.takeItem(simLayout1.row(previous_connectivity))
                l1  = QListWidgetItem(text_selected)
                FrameWorkValue["Connectivity"]=l1
                simLayout1.addItem(l1)
                temp =True
                break
        if(temp == False):
            l1  = QListWidgetItem(text_selected)
            FrameWorkValue["Connectivity"]=l1
            simLayout1.addItem(l1)

        #For device mobility
        device_mobility = self.type.currentText()
        l1  = QListWidgetItem(device_mobility)
        FrameWorkValue["Device_mobility"] = l1

        #For device Type
        device_type = self.input.currentText()
        l1  = QListWidgetItem(device_type)
        FrameWorkValue["Device_type"] = l1

        device_selected = self.device.currentText()
        if(FrameWorkValue["Device"].text()!=""):
            simLayout1.takeItem(simLayout1.row(FrameWorkValue["Device"]))
            l1  = QListWidgetItem(device_selected)
            FrameWorkValue["Device"]= l1
            simLayout1.addItem(l1)
        else:
            l1  = QListWidgetItem(device_selected)
            FrameWorkValue["Device"]= l1
            simLayout1.addItem(l1)

        #For Changing Object button image
        url = "object_images/"+device_selected
        adding_button.setStyleSheet("border-image:url("+url+");")

        # self.hide()

class DesignAreaButton(QPushButton):
     def __init__(self,title,parent):
        super().__init__(title,parent)
        self.setStyleSheet('width: 400px; height: 20px; font-size: 15px;color:black;')
        self.setEnabled(False)

class MoveButton(QPushButton):
    def __init__(self,title,parent):
        super().__init__(title,parent)
        self.setStyleSheet('width: 40px; height: 20px; font-size: 15px')
        self.setFixedSize(175,35)
        # self.counter = 0


# class RelationFinderButton(QPushButton):
#     def __init__(self,title,parent):
#         super().__init__(title,parent)
#         self.setStyleSheet('width: 40px; height: 20px; font-size: 15px')
#         self.setFixedSize(175,35)
#
#     def isNaN(self,string):
#         return string != string
#
#     def disCal(self,d1,d2):
#         a_x = int(d1.split(",")[0])
#         a_y = int(d1.split(",")[1])
#         b_x = int(d2.split(",")[0])
#         b_y = int(d2.split(",")[1])
#         dis = math.sqrt((a_x-b_x)**2+(a_y-b_y)**2)
#         return dis
#
#     def mousePressEvent(self,e):
#         super().mouseMoveEvent(e)
#         if e.button() == Qt.LeftButton:
#             #For Profiling deatils
#             added_dataframe = pd.read_csv(creating_filename)
#             #Finding relationships
#             # moved_file = creating_filename.split("added.csv")[0]+"movedObjects.csv"
#             read_data = pd.read_csv(moved_file)
#             # print(read_data)
#             dic={"Device_id":list(added_dataframe["Device_id"])}
#             relation_data = pd.DataFrame(dic)
#             #To initialize the vlaues with null in the matix of dataframe
#             for i in list(added_dataframe["Device_id"]):
#                 relation_data[i]=""
#
#             for i,row in read_data.iterrows():
#                 j = 2
#                 deviceInteractionDic = {}
#                 #To initialse all the intersections
#                 for z in list(added_dataframe["Device_id"]):
#                     if(z!=row.iloc[0]):
#                         deviceInteractionDic[z] =0
#                 #Loop for individual interaction coloumn
#                 while(j<len(read_data.columns)):
#                     # print(row.iloc[0],row.iloc[j])
#                     if(not self.isNaN(row.iloc[j])):
#                         temp = row.iloc[j].split(",")
#                         temp = [i.split(":")[0] for i in temp]
#                         #Removing mulitple interaction of Protocol for same device
#                         temp = np.unique(np.array(temp))
#                         for z in temp:
#                             if(z in deviceInteractionDic.keys()):
#                                 deviceInteractionDic[z] = deviceInteractionDic[z]+1
#                     j = j+2
#                 # print(row.iloc[0],deviceInteractionDic)
#                 for z in deviceInteractionDic.keys():
#                     #To get row of that particualr object we split the device_id  and go to that particualr index added_dataframe.iloc[int(z[1:])-1
#                     #To get particualr value with column name and row name we use this added_dataframe.iloc[i, added_dataframe.columns.get_loc("Device")]
#                     # print(z,added_dataframe.iloc[i, added_dataframe.columns.get_loc("Device")],added_dataframe.iloc[int(z[1:])-1, added_dataframe.columns.get_loc("Device")])
#                     #Here i has already index of each Object
#
#                     d1_type = added_dataframe.iloc[i, added_dataframe.columns.get_loc("Device")]
#                     #Here no index so we split and get interger and -1 to get index
#                     d2_type = added_dataframe.iloc[int(z[1:])-1, added_dataframe.columns.get_loc("Device")]
#
#                     d1_brand = added_dataframe.iloc[i, added_dataframe.columns.get_loc("Manufacturing_id")]
#                     d2_brand = added_dataframe.iloc[int(z[1:])-1, added_dataframe.columns.get_loc("Manufacturing_id")]
#
#                     tem = "Move"+str((len(read_data.columns)-1)//2)
#                     d1_gps = read_data.iloc[i, read_data.columns.get_loc(tem)]
#                     d2_gps = read_data.iloc[int(z[1:])-1, read_data.columns.get_loc(tem)]
#
#                     d1_ctg = added_dataframe.iloc[i, added_dataframe.columns.get_loc("Device_type")]
#                     d2_ctg = added_dataframe.iloc[int(z[1:])-1, added_dataframe.columns.get_loc("Device_type")]
#
#                     d1_pro = added_dataframe.iloc[i, added_dataframe.columns.get_loc("Connectivity")]
#                     d2_pro = added_dataframe.iloc[int(z[1:])-1, added_dataframe.columns.get_loc("Connectivity")]
#
#                     # print(row.iloc[0],z,self.disCal(d1_gps,d2_gps),d1_type !=d2_type,self.disCal(d1_gps,d2_gps)<=120,
#                     #         d1_ctg=="Public",d2_ctg=="Private","ZigBee" in list(d1_pro.split(",")) and
#                     #         "ZigBee" in list(d2_pro.split(",")),d1_brand!=d2_brand,deviceInteractionDic[z]==0)
#                     # print(i,relation_data.columns.get_loc(z))
#
#                     if(d1_type != d2_type and self.disCal(d1_gps,d2_gps)<=120 and
#                             d1_ctg=="Public" and d2_ctg=="Private" and "ZigBee" in list(d1_pro.split(",")) and
#                             "ZigBee" in list(d2_pro.split(",")) and d1_brand!=d2_brand  and deviceInteractionDic[z]==0):
#                         print("{} and {} are in STOR".format(row.iloc[0],z))
#                         relation_line = QLine(int(d1_gps.split(",")[0])+10,int(d1_gps.split(",")[1])+10,int(d2_gps.split(",")[0])+10,int(d2_gps.split(",")[1])+10)
#                         if(relation_line not in simLayout.realtion_lines):
#                             simLayout.realtion_lines.append(relation_line)
#                             simLayout.update()
#                         relation_data.iloc[i,relation_data.columns.get_loc(z)]="STOR"
#
#                     if(d1_type == d2_type and self.disCal(d1_gps,d2_gps)<=120 and
#                             d1_ctg=="Public" and d2_ctg=="Private" and "Wifi" in list(d1_pro.split(",")) and
#                             "Wifi" in list(d2_pro.split(",")) and d1_brand!=d2_brand  and deviceInteractionDic[z]>=0):
#                         print("{} and {} are in SROR".format(row.iloc[0],z))
#                         relation_line = QLine(int(d1_gps.split(",")[0])+10,int(d1_gps.split(",")[1])+10,int(d2_gps.split(",")[0])+10,int(d2_gps.split(",")[1])+10)
#                         if(relation_line not in simLayout.realtion_lines):
#                             simLayout.realtion_lines.append(relation_line)
#                             simLayout.update()
#                         relation_data.iloc[i,relation_data.columns.get_loc(z)]="SROR"
#
#                     if(d1_type != d2_type and 400<self.disCal(d1_gps,d2_gps)<800 and
#                             d1_ctg=="Private" and d2_ctg=="Private" and ("Wifi" in list(d1_pro.split(",")) or "Bluetooth" in list(d1_pro.split(",")))
#                             and ("Wifi" in list(d2_pro.split(",")) or "Bluetooth" in list(d2_pro.split(",")))and d1_brand!=d2_brand  and deviceInteractionDic[z]<6):
#                         print("{} and {} are in GUOR".format(row.iloc[0],z))
#                         relation_line = QLine(int(d1_gps.split(",")[0])+10,int(d1_gps.split(",")[1])+10,int(d2_gps.split(",")[0])+10,int(d2_gps.split(",")[1])+10)
#                         if(relation_line not in simLayout.realtion_lines):
#                             simLayout.realtion_lines.append(relation_line)
#                             simLayout.update()
#                         relation_data.iloc[i,relation_data.columns.get_loc(z)]="GUOR"
#
#                     if(d1_type != d2_type and self.disCal(d1_gps,d2_gps)<80 and
#                             d1_ctg=="Private" and d2_ctg=="Private" and ("Wifi" in list(d1_pro.split(",")) or "Bluetooth" in list(d1_pro.split(",")))
#                             and ("Wifi" in list(d2_pro.split(",")) or "Bluetooth" in list(d2_pro.split(",")))and d1_brand!=d2_brand  and deviceInteractionDic[z]>2):
#                         print("{} and {} are in CWOR".format(row.iloc[0],z))
#                         relation_line = QLine(int(d1_gps.split(",")[0])+10,int(d1_gps.split(",")[1])+10,int(d2_gps.split(",")[0])+10,int(d2_gps.split(",")[1])+10)
#                         if(relation_line not in simLayout.realtion_lines):
#                             simLayout.realtion_lines.append(relation_line)
#                             simLayout.update()
#                         relation_data.iloc[i,relation_data.columns.get_loc(z)]="CWOR"
#
#                     if(d1_type == d2_type and 80<self.disCal(d1_gps,d2_gps)<400 and
#                             d1_ctg=="Private" and d2_ctg=="Private" and ("Wifi" in list(d1_pro.split(",")) or "Bluetooth" in list(d1_pro.split(",")) or "ZigBee" in list(d1_pro.split(",")))
#                             and ("Wifi" in list(d2_pro.split(",")) or "Bluetooth" in list(d2_pro.split(",")) or "ZigBee" in list(d2_pro.split(",")))and d1_brand!=d2_brand  and deviceInteractionDic[z]>=2):
#                         print("{} and {} are in CLOR".format(row.iloc[0],z))
#                         relation_line = QLine(int(d1_gps.split(",")[0])+10,int(d1_gps.split(",")[1])+10,int(d2_gps.split(",")[0])+10,int(d2_gps.split(",")[1])+10)
#                         if(relation_line not in simLayout.realtion_lines):
#                             simLayout.realtion_lines.append(relation_line)
#                             simLayout.update()
#                         relation_data.iloc[i,relation_data.columns.get_loc(z)]="CLOR"
#
#                     if(d1_type == d2_type and self.disCal(d1_gps,d2_gps)<3200 and
#                             d1_ctg=="Private" and d2_ctg=="Private" and ("Wifi" in list(d1_pro.split(",")) or "Bluetooth" in list(d1_pro.split(",")) or "ZigBee" in list(d1_pro.split(",")))
#                             and ("Wifi" in list(d2_pro.split(",")) or "Bluetooth" in list(d2_pro.split(",")) or "ZigBee" in list(d2_pro.split(",")))and d1_brand==d2_brand  and deviceInteractionDic[z]>=6):
#                         print("{} and {} are in POR".format(row.iloc[0],z))
#                         relation_line = QLine(int(d1_gps.split(",")[0])+10,int(d1_gps.split(",")[1])+10,int(d2_gps.split(",")[0])+10,int(d2_gps.split(",")[1])+10)
#                         if(relation_line not in simLayout.realtion_lines):
#                             simLayout.realtion_lines.append(relation_line)
#                             simLayout.update()
#                         relation_data.iloc[i,relation_data.columns.get_loc(z)]="POR"
#
#                     if(d1_type == d2_type and self.disCal(d1_gps,d2_gps)<80 and
#                             d1_ctg=="Private" and d2_ctg=="Private" and ("Wifi" in list(d1_pro.split(",")) or "Bluetooth" in list(d1_pro.split(",")) or "ZigBee" in list(d1_pro.split(",")))
#                             and ("Wifi" in list(d2_pro.split(",")) or "Bluetooth" in list(d2_pro.split(",")) or "ZigBee" in list(d2_pro.split(",")))and d1_brand!=d2_brand  and deviceInteractionDic[z]==1):
#                         print("{} and {} are in GSTOR".format(row.iloc[0],z))
#                         relation_line = QLine(int(d1_gps.split(",")[0])+10,int(d1_gps.split(",")[1])+10,int(d2_gps.split(",")[0])+10,int(d2_gps.split(",")[1])+10)
#                         if(relation_line not in simLayout.realtion_lines):
#                             simLayout.realtion_lines.append(relation_line)
#                             simLayout.update()
#                         relation_data.iloc[i,relation_data.columns.get_loc(z)]="GSTOR"
#
#                     if(d1_type != d2_type and self.disCal(d1_gps,d2_gps)<400 and
#                             d1_ctg=="Private" and d2_ctg=="Private" and ("Wifi" in list(d1_pro.split(",")) or "Bluetooth" in list(d1_pro.split(",")) or "ZigBee" in list(d1_pro.split(",")))
#                             and ("Wifi" in list(d2_pro.split(",")) or "Bluetooth" in list(d2_pro.split(",")) or "ZigBee" in list(d2_pro.split(",")))and d1_brand!=d2_brand  and deviceInteractionDic[z]<=3):
#                         print("{} and {} are in SIBOR".format(row.iloc[0],z))
#                         relation_line = QLine(int(d1_gps.split(",")[0])+10,int(d1_gps.split(",")[1])+10,int(d2_gps.split(",")[0])+10,int(d2_gps.split(",")[1])+10)
#                         if(relation_line not in simLayout.realtion_lines):
#                             simLayout.realtion_lines.append(relation_line)
#                             simLayout.update()
#                         relation_data.iloc[i,relation_data.columns.get_loc(z)]="SIBOR"
#
#                     if(d1_type != d2_type and 160<self.disCal(d1_gps,d2_gps)<400 and
#                             d1_ctg=="Public" and d2_ctg=="Private" and ("Wifi" in list(d1_pro.split(",")) or "ZigBee" in list(d1_pro.split(",")))
#                             and ("Wifi" in list(d2_pro.split(",")) or "ZigBee" in list(d2_pro.split(",")))and d1_brand!=d2_brand  and deviceInteractionDic[z]==2):
#                         print("{} and {} are in SIBOR".format(row.iloc[0],z))
#                         relation_line = QLine(int(d1_gps.split(",")[0])+10,int(d1_gps.split(",")[1])+10,int(d2_gps.split(",")[0])+10,int(d2_gps.split(",")[1])+10)
#                         if(relation_line not in simLayout.realtion_lines):
#                             simLayout.realtion_lines.append(relation_line)
#                             simLayout.update()
#                         relation_data.iloc[i,relation_data.columns.get_loc(z)]="SIBOR"
#
#                     if(d1_type != d2_type and self.disCal(d1_gps,d2_gps)<160 and
#                             d1_ctg=="Public" and d2_ctg=="Private" and ("Wifi" in list(d1_pro.split(",")) or "Bluetooth" in list(d1_pro.split(",")) or "ZigBee" in list(d1_pro.split(",")))
#                             and ("Wifi" in list(d2_pro.split(",")) or "Bluetooth" in list(d1_pro.split(",")) or "ZigBee" in list(d2_pro.split(",")))and d1_brand==d2_brand  and deviceInteractionDic[z]>3):
#                         print("{} and {} are in OOR".format(row.iloc[0],z))
#                         relation_line = QLine(int(d1_gps.split(",")[0])+10,int(d1_gps.split(",")[1])+10,int(d2_gps.split(",")[0])+10,int(d2_gps.split(",")[1])+10)
#                         if(relation_line not in simLayout.realtion_lines):
#                             simLayout.realtion_lines.append(relation_line)
#                             simLayout.update()
#                         relation_data.iloc[i,relation_data.columns.get_loc(z)]="OOR"
#
#             #To create the saved relation file with appropritate relations
#             relation_data.to_csv(relation_file,header=True,index=False)


class RelationFinderButton(QPushButton):
    def __init__(self,title,parent):
        super().__init__(title,parent)
        self.setStyleSheet('width: 40px; height: 20px; font-size: 15px')
        self.setFixedSize(175,35)

    def isNaN(self,string):
        return string != string

    def disCal(self,d1,d2):
        a_x = int(d1.split(",")[0])
        a_y = int(d1.split(",")[1])
        b_x = int(d2.split(",")[0])
        b_y = int(d2.split(",")[1])
        dis = math.sqrt((a_x-b_x)**2+(a_y-b_y)**2)
        return dis

    def mousePressEvent(self,e):
        super().mouseMoveEvent(e)
        if e.button() == Qt.LeftButton:

            self.relation_line = [[],[],[],[],[],[],[],[],[],[],[]]
            #For Profiling deatils
            added_dataframe = pd.read_csv(creating_filename)
            #Finding relationships
            # moved_file = creating_filename.split("added.csv")[0]+"movedObjects.csv"
            read_data = pd.read_csv(moved_file)
            # print(read_data)
            dic={"Device_id":list(added_dataframe["Device_id"])}
            relation_data = pd.DataFrame(dic)
            #To initialize the vlaues with null in the matix of dataframe
            for i in list(added_dataframe["Device_id"]):
                relation_data[i]=""

            for i,row in read_data.iterrows():
                j = 2
                deviceInteractionDic = {}
                #To initialse all the intersections
                for z in list(added_dataframe["Device_id"]):
                    if(z!=row.iloc[0]):
                        deviceInteractionDic[z] =0
                #Loop for individual interaction coloumn
                while(j<len(read_data.columns)):
                    # print(row.iloc[0],row.iloc[j])
                    if(not self.isNaN(row.iloc[j])):
                        temp = row.iloc[j].split(",")
                        temp = [i.split(":")[0] for i in temp]
                        #Removing mulitple interaction of Protocol for same device
                        temp = np.unique(np.array(temp))
                        for z in temp:
                            if(z in deviceInteractionDic.keys()):
                                deviceInteractionDic[z] = deviceInteractionDic[z]+1
                    j = j+2
                # print(row.iloc[0],deviceInteractionDic)
                for z in deviceInteractionDic.keys():
                    #To get row of that particualr object we split the device_id  and go to that particualr index added_dataframe.iloc[int(z[1:])-1
                    #To get particualr value with column name and row name we use this added_dataframe.iloc[i, added_dataframe.columns.get_loc("Device")]
                    # print(z,added_dataframe.iloc[i, added_dataframe.columns.get_loc("Device")],added_dataframe.iloc[int(z[1:])-1, added_dataframe.columns.get_loc("Device")])
                    #Here i has already index of each Object

                    d1_type = added_dataframe.iloc[i, added_dataframe.columns.get_loc("Device")]
                    #Here no index so we split and get interger and -1 to get index
                    d2_type = added_dataframe.iloc[int(z[1:])-1, added_dataframe.columns.get_loc("Device")]

                    d1_brand = added_dataframe.iloc[i, added_dataframe.columns.get_loc("Manufacturing_id")]
                    d2_brand = added_dataframe.iloc[int(z[1:])-1, added_dataframe.columns.get_loc("Manufacturing_id")]

                    tem = "Move"+str((len(read_data.columns)-1)//2)
                    d1_gps = read_data.iloc[i, read_data.columns.get_loc(tem)]
                    d2_gps = read_data.iloc[int(z[1:])-1, read_data.columns.get_loc(tem)]

                    d1_ctg = added_dataframe.iloc[i, added_dataframe.columns.get_loc("Device_type")]
                    d2_ctg = added_dataframe.iloc[int(z[1:])-1, added_dataframe.columns.get_loc("Device_type")]

                    d1_pro = added_dataframe.iloc[i, added_dataframe.columns.get_loc("Connectivity")]
                    d1_pro = list(d1_pro.split(","))
                    d2_pro = added_dataframe.iloc[int(z[1:])-1, added_dataframe.columns.get_loc("Connectivity")]
                    d2_pro = list(d2_pro.split(","))

                    theoretical_relation = pd.read_csv("Relationship_criteria.csv")
                    toReplace_name = {"Same":"==","Different":"!="}
                    for i_condition,row_condition in theoretical_relation.iterrows():
                        condition_relation = row_condition.iloc[theoretical_relation.columns.get_loc("Relation")]
                        condition_type = row_condition.iloc[theoretical_relation.columns.get_loc("Type")]
                        condition_dis = row_condition.iloc[theoretical_relation.columns.get_loc("Distance")]
                        condtion_catg = row_condition.iloc[theoretical_relation.columns.get_loc("Category")]
                        condition_procol = row_condition.iloc[theoretical_relation.columns.get_loc("Protocol")]
                        condition_procol = list(condition_procol.split(","))
                        condition_manu = row_condition.iloc[theoretical_relation.columns.get_loc("Manufacturer")]
                        condition_inter = row_condition.iloc[theoretical_relation.columns.get_loc("Intersections")]

                        type = "\'"+d1_type+"\'"+toReplace_name[condition_type]+"\'"+d2_type+"\'"
                        dis = "0==0"
                        if(len(condition_dis.split(","))==2):
                            dis = condition_dis.split(",")[0]+str(self.disCal(d1_gps,d2_gps))+condition_dis.split(",")[1]
                        if(len(condition_dis.split(","))==1):
                            dis = str(self.disCal(d1_gps,d2_gps))+condition_dis
                        catg1 = (d1_ctg == condtion_catg.split("-")[0])
                        catg2 = (d2_ctg == condtion_catg.split("-")[1])
                        inter_d = set(d1_pro).intersection(set(d2_pro))
                        inter_d_p = set(inter_d).intersection(set(condition_procol))
                        manu = str(d1_brand)+toReplace_name[condition_manu]+str(d2_brand)
                        inter = str(deviceInteractionDic[z])+condition_inter

                        if(eval(type) and eval(dis) and catg1 and catg2 and len(inter_d_p)>0 and eval(manu) and eval(inter)):
                            print("{} and {} are in {}".format(row.iloc[0],z,condition_relation))
                            relation_line = QLine(int(d1_gps.split(",")[0])+10,int(d1_gps.split(",")[1])+10,int(d2_gps.split(",")[0])+10,int(d2_gps.split(",")[1])+10)
                            if(relation_line not in simLayout.relation_line[i_condition]):
                                simLayout.relation_line[i_condition].append(relation_line)
                                simLayout.update()

                            relation_data.iloc[i,relation_data.columns.get_loc(z)]=condition_relation



            #To create the saved relation file with appropritate relations
            relation_data.to_csv(relation_file,header=True,index=False)

class MovementRelationFinder(QFrame):

    def __init__(self):
        super().__init__()
        self.setFrameStyle(2)
        self.setFixedSize(300,130)
        l1= QLabel("Time (Sec)")
        self.timeEntered = QLineEdit()
        self.timeEntered.setPlaceholderText("Time in Sec")
        self.timeEntered.setFixedSize(100,30)
        formLayout = QFormLayout()
        formLayout.addRow(l1,self.timeEntered)
        moveButton = MoveButton("Start",self)
        moveButton.clicked.connect(self.onClickingMove)
        formLayout.addWidget(moveButton)
        relationFinder = RelationFinderButton("Find Relationship",self)
        formLayout.addWidget(relationFinder)
        self.setLayout(formLayout)

    def movementCode(self):
        # To time in For  code to be executed
        counter = int(self.timeEntered.text())
        if counter > 0:
            #updating Time with 1 sec less
            self.timeEntered.setText(str(counter-1))
            #To get all the objects presetn on the layout
            objects = simLayout.objectsPresent
            #To remove all drawing lines in Layout
            simLayout.relation_line = [[],[],[],[],[],[],[],[],[],[],[]]
            simLayout.circle_zigbee = []
            simLayout.circle_wifi = []
            simLayout.circle_gsm = []
            simLayout.circle_bluetooth = []
            simLayout.lines =[]
            simLayout.realtion_lines = []
            lis_gps =[]
            lis_device_id = []
            lis_intersection = []
            simLayout.update()
            #File where moves GPS are located
            # moved_file = creating_filename.split("added.csv")[0]+"movedObjects.csv"
            read_data = pd.read_csv(moved_file)

            for i in objects:
                #Only mobility objects should move
                if(i.device_mobility.text()=="Mobile"):
                    # New random coordinates with 100 range
                    new_x = i.x()+random.randrange(-100,100)
                    new_y = i.y()+random.randrange(-100,100)
                    #Coinditions for boundary of the layout as coordinates should not exced the boundary
                    while(new_x<0 or new_x>675):
                        new_x = i.x()+random.randrange(-100,100)
                    while(new_y<0 or new_y>625):
                        new_y = i.y()+random.randrange(-100,100)
                    #Moving of object
                    i.move(new_x,new_y)
                    new_gps = str(new_x)+","+str(new_y)
                    #Appending Device name and coordiantes of each movement to be stored in the CSV File Created as movedObjects.csv
                    lis_gps.append(new_gps)
                    lis_device_id.append(i.device_id.text())
                    #Drawing if required i.e if it is enabled
                    if(simLayout.circle_activation ==True):
                        centre = QPoint(new_x+25,new_y+25)
                        # print(list(FrameWorkValue["Connectivity"].text().split(",")))
                        if("Wifi" in list(i.device_connectivity.text().split(",")) and centre not in simLayout.circle_wifi):
                            simLayout.circle_wifi.append(centre)
                            simLayout.update()
                        if("Bluetooth" in list(i.device_connectivity.text().split(",")) and centre not in simLayout.circle_bluetooth):
                            simLayout.circle_bluetooth.append(centre)
                            simLayout.update()
                        if("GSM" in list(i.device_connectivity.text().split(",")) and centre not in simLayout.circle_gsm):
                            simLayout.circle_gsm.append(centre)
                            simLayout.update()
                        if("ZigBee" in list(i.device_connectivity.text().split(",")) and centre not in simLayout.circle_zigbee):
                            simLayout.circle_zigbee.append(centre)
                            simLayout.update()
                #Drawing circles if required
                else:
                    new_gps = str(i.x())+","+str(i.y())
                    lis_gps.append(new_gps)
                    lis_device_id.append(i.device_id.text())
                    if(simLayout.circle_activation == True):
                        centre = QPoint(i.x()+25,i.y()+25)
                        if("Wifi" in list(i.device_connectivity.text().split(",")) and centre not in simLayout.circle_wifi):
                            simLayout.circle_wifi.append(centre)
                            simLayout.update()
                        if("Bluetooth" in list(i.device_connectivity.text().split(",")) and centre not in simLayout.circle_bluetooth):
                            simLayout.circle_bluetooth.append(centre)
                            simLayout.update()
                        if("GSM" in list(i.device_connectivity.text().split(",")) and centre not in simLayout.circle_gsm):
                            simLayout.circle_gsm.append(centre)
                            simLayout.update()
                        if("ZigBee" in list(i.device_connectivity.text().split(",")) and centre not in simLayout.circle_zigbee):
                            simLayout.circle_zigbee.append(centre)
                            simLayout.update()
            #checking for intersection of objects in diff ranges
            #Only one object intersection is checked Like if D2 is intersecting with D3 it is stored only in D2 not in D3
            for i in range(0,len(objects)):
                intersection = ""
                for j in range(i+1,len(objects)):
                    a_x = objects[i].x()
                    a_y = objects[i].y()
                    b_x = objects[j].x()
                    b_y = objects[j].y()
                    dis = math.sqrt((a_x-b_x)**2+(a_y-b_y)**2)
                    if(dis < 80 and "Wifi" in objects[j].device_connectivity.text().split(",") and "Wifi" in objects[i].device_connectivity.text().split(",")):
                        intersection = intersection+objects[j].device_id.text()+":Wifi,"
                        # print("Intersecting {} and {} with WiFi".format(objects[i].device_id.text(),objects[j].device_id.text()))
                    if(dis < 40 and "Bluetooth" in objects[j].device_connectivity.text().split(",") and "Bluetooth" in objects[i].device_connectivity.text().split(",")):
                        intersection = intersection+objects[j].device_id.text()+":Bluetooth,"
                        # print("Intersecting {} and {} with Bluetooth".format(objects[i].device_id.text(),objects[j].device_id.text()))
                    if(dis < 60 and "GSM" in objects[j].device_connectivity.text().split(",") and "GSM" in objects[i].device_connectivity.text().split(",")):
                        intersection = intersection+objects[j].device_id.text()+":GSM,"
                        # print("Intersecting {} and {} with GSM".format(objects[i].device_id.text(),objects[j].device_id.text()))
                    if(dis < 50 and "Zigbee" in objects[j].device_connectivity.text().split(",") and "Zigbee" in objects[i].device_connectivity.text().split(",")):
                        intersection = intersection+objects[j].device_id.text()+":Zigbee,"
                        # print("Intersecting {} and {} with Zigbee".format(objects[i].device_id.text(),objects[j].device_id.text()))

                #To remove extra , in the end and append to the list of that particular object
                lis_intersection.append(intersection[:-1])

            #Storing all the data to the csv File with column names with the move numebr and intersection with the number
            colm_name = "Move"+str(len(read_data.columns)//2+1)
            colm_name1 = "Intersection"+str(len(read_data.columns)//2+1)
            read_data["Device_id"]=np.asarray(lis_device_id)
            read_data[colm_name]=np.asarray(lis_gps)
            read_data[colm_name1]=np.asarray(lis_intersection)
            read_data.to_csv(moved_file,header=True,index=False)
        else:
            self.timer.stop()

    def onClickingMove(self):

        #To create new file moved with time as the name and copyign all the device ID to that file
        added_dataframe = pd.read_csv(creating_filename)
        dic={"Device_id":list(added_dataframe["Device_id"])}
        filecreation_time = str(datetime.datetime.now().time())
        global moved_file
        moved_file = creating_filename.split("added.csv")[0]+"movedObjects"+"-"+self.timeEntered.text()+"-"+filecreation_time+".csv"
        global relation_file
        relation_file = creating_filename.split("added.csv")[0]+"relationObjects"+"-"+self.timeEntered.text()+"-"+filecreation_time+".csv"
        df = pd.DataFrame(dic)
        df.to_csv(moved_file,header=True,index=False)
        self.timer = QTimer(self)
        #Code to be executed in Loop with interval
        self.timer.timeout.connect(self.movementCode)
        self.counter = 0
        #Time of Delay in movement
        self.timer.start(1000)

class RelationChange(QDialog):
    def __init__(self):
        super().__init__()
        # self.setFrameStyle(2)
        self.setFixedSize(400,350)
        self.path = "Relationship_criteria.csv"
        self.relation_dataframe = pd.read_csv(self.path)

        layout = QGridLayout()
        formLayout = QFormLayout()
        heading = QLabel("Change Theoretical Relations")
        head1 = QLabel("Relation")
        head2 = QLabel("Device")
        head3 = QLabel("Distance")
        head4 = QLabel("Device Type")
        head5 = QLabel("Protocol")
        head6 = QLabel("Manufacturer")
        head7 = QLabel("Intersections")

        self.relation = QComboBox(self)
        self.relation.addItems(list(self.relation_dataframe["Relation"]))

        self.device = QComboBox(self)
        self.device.addItems(["Different","Same"])
        self.distance = QLineEdit("")
        self.category = QComboBox(self)
        self.category.addItems(["Public-Private","Private-Private","Public-Public","Private-Public"])
        self.intersections = QLineEdit("")
        self.checkBox2_1 = QCheckBox("Wifi")
        self.checkBox2_2 = QCheckBox("Bluetooth")
        self.checkBox2_3 = QCheckBox("GSM")
        self.checkBox2_4 = QCheckBox("ZigBee")
        self.manufacturer = QComboBox(self)
        self.manufacturer.addItems(["Different","Same"])
        protocol_grid = QGridLayout()
        protocol_grid.addWidget(self.checkBox2_1,0,0)
        protocol_grid.addWidget(self.checkBox2_2,0,1)
        protocol_grid.addWidget(self.checkBox2_3,0,2)
        protocol_grid.addWidget(self.checkBox2_4,0,3)

        self.submit_button = QPushButton("Update Conditions")
        self.submit_button.clicked.connect(self.onCLicking)

        formLayout.addWidget(heading)
        formLayout.addRow(head1,self.relation)
        formLayout.addRow(head2,self.device)
        formLayout.addRow(head3,self.distance)
        formLayout.addRow(head4,self.category)
        formLayout.addRow(head5,protocol_grid)
        formLayout.addRow(head6,self.manufacturer)
        formLayout.addRow(head7,self.intersections)
        formLayout.addWidget(self.submit_button)

        self.relation.currentIndexChanged.connect(self.relation_function)
        self.relation_function(0)

        layout.addLayout(formLayout,0,0)
        self.setLayout(layout)

    def onCLicking(self):
        message = QMessageBox.question(self,"Message","Are you sure u want to update",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if message != QMessageBox.Yes:
            return
        relation_entered = self.relation.currentText()
        type = self.device.currentText()
        distance = self.distance.text()
        category = self.category.currentText()
        manufacturer = self.manufacturer.currentText()
        intersections = self.intersections.text()
        protocol = ""
        if(self.checkBox2_1.isChecked()):
            protocol = protocol+"Wifi"+","
        if(self.checkBox2_2.isChecked()):
            protocol = protocol+"Bluetooth"+","
        if(self.checkBox2_3.isChecked()):
            protocol = protocol+"GSM"+","
        if(self.checkBox2_4.isChecked()):
            protocol = protocol+"ZigBee"+","
        protocol = protocol[:-1]
        self.relation_dataframe.loc[self.relation_dataframe["Relation"]==relation_entered,"Type"] = type
        self.relation_dataframe.loc[self.relation_dataframe["Relation"]==relation_entered,"Distance"] = distance
        self.relation_dataframe.loc[self.relation_dataframe["Relation"]==relation_entered,"Category"] = category
        self.relation_dataframe.loc[self.relation_dataframe["Relation"]==relation_entered,"Protocol"] = protocol
        self.relation_dataframe.loc[self.relation_dataframe["Relation"]==relation_entered,"Manufacturer"] = manufacturer
        self.relation_dataframe.loc[self.relation_dataframe["Relation"]==relation_entered,"Intersections"] = intersections
        self.relation_dataframe.to_csv(self.path,header=True,index=False)

    def relation_function(self,index):
        relation_entered = self.relation.currentText()

        self.device.setCurrentText(self.relation_dataframe.loc[self.relation_dataframe["Relation"]==relation_entered,"Type"].values[0])
        self.distance.setText(self.relation_dataframe.loc[self.relation_dataframe["Relation"]==relation_entered,"Distance"].values[0])
        self.category.setCurrentText(self.relation_dataframe.loc[self.relation_dataframe["Relation"]==relation_entered,"Category"].values[0])
        self.manufacturer.setCurrentText(self.relation_dataframe.loc[self.relation_dataframe["Relation"]==relation_entered,"Manufacturer"].values[0])
        self.intersections.setText(self.relation_dataframe.loc[self.relation_dataframe["Relation"]==relation_entered,"Intersections"].values[0])
        protocol  = self.relation_dataframe.loc[self.relation_dataframe["Relation"]==relation_entered,"Protocol"].values[0]
        protocol = protocol.split(",")
        self.checkBox2_1.setChecked(False)
        self.checkBox2_2.setChecked(False)
        self.checkBox2_3.setChecked(False)
        self.checkBox2_4.setChecked(False)
        for i in protocol:
            if(i=="Wifi"):
                self.checkBox2_1.setChecked(True)
            if(i=="Bluetooth"):
                self.checkBox2_2.setChecked(True)
            if(i=="GSM"):
                self.checkBox2_3.setChecked(True)
            if(i=="ZigBee"):
                self.checkBox2_4.setChecked(True)



class Canvas(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):
        self.fig = Figure(figsize=(width, height), dpi=dpi,)
        self.ax = self.fig.add_subplot(111)
        # self.ax.margins(x=100.0,y=100.0)
        # self.ax.set_size_inches(100,100)
        # self.ax.xticks([1, 2, 3, 4, 5])
        self.ax.axis([0,10,-9,9])
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 800)
        global date
        date = datetime.datetime.now()
        cwd = os.getcwd()
        print(cwd)
        os.mkdir(cwd+"/simulation_data/ExistingModel/"+str(date))
        global creating_filename
        creating_filename = cwd+"/simulation_data/ExistingModel/"+str(date)+"/added.csv"
        shutil.copyfile(cwd+"/added.csv",creating_filename)
        print(date)
        #Main Grid layout
        mainLayout = QGridLayout(self)

        #List of Framework
        global simLayout1
        simLayout1  = DeviceFrameWork()
        simLayout1.setFixedSize(280,100)
        #Object Button
        global adding_button
        adding_button = Button_Device("",self)
        adding_button.setFixedSize(100,75)

        #movement and relation finder Layout
        movementRelationfinder = MovementRelationFinder()

        hLayoutofFrameWork = QHBoxLayout()
        hLayoutofFrameWork.addWidget(simLayout1)
        hLayoutofFrameWork.addWidget(adding_button)
        hLayoutofFrameWork.addWidget(movementRelationfinder)

         # Simulator Area
        Label = DesignAreaButton("Simulation Area",self)
        global  simLayout
        simLayout = DesignArea()

        vLayoutofFrameWork = QVBoxLayout()
        vLayoutofFrameWork.addWidget(Label)
        vLayoutofFrameWork.addWidget(simLayout)

        vLayoutofFirstColoumn = QVBoxLayout()
        vLayoutofFirstColoumn.addLayout(hLayoutofFrameWork)
        vLayoutofFirstColoumn.addLayout(vLayoutofFrameWork)

        #Last Coloumn
        vLayoutofLastColoumn = QVBoxLayout()
        inputArea = InputArea()
        vLayoutofLastColoumn.addWidget(inputArea)

        # hLayoutofDistribution = QHBoxLayout()
        # deviceDistribution = DeviceDistribution()
        # distribution = Distribution()
        # hLayoutofDistribution.addWidget(deviceDistribution)
        # hLayoutofDistribution.addWidget(distribution)

        global linkArea
        global relationArea

        linkArea = LinkArea()
        relationArea = RelationshipArea()

        vLayoutofLinkAreaRelationArea = QVBoxLayout()
        vLayoutofLinkAreaRelationArea.addWidget(linkArea)
        vLayoutofLinkAreaRelationArea.addWidget(relationArea)

        self.canvas = Canvas(self, width=10, height=13)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.graph_button = QPushButton("Plot Differences")
        self.graph_button.clicked.connect(self.button_graph)
        vlayoutGraph = QVBoxLayout()
        vlayoutGraph.addWidget(self.graph_button)
        vlayoutGraph.addWidget(self.toolbar)
        vlayoutGraph.addWidget(self.canvas)

        hLayoutLinkRelationGraph = QHBoxLayout()
        hLayoutLinkRelationGraph.addLayout(vLayoutofLinkAreaRelationArea)
        hLayoutLinkRelationGraph.addLayout(vlayoutGraph)

        vLayoutofLastColoumn.addLayout(hLayoutLinkRelationGraph)


        mainLayout.addLayout(vLayoutofFirstColoumn,0,0)
        mainLayout.addLayout(vLayoutofLastColoumn,0,1)

        #Menu Layout
        file_menu = self.menuBar().addMenu("&Navigate")
        open_static_action = QAction("Dynamic Model", self)
        open_static_action.setStatusTip("Dynamic Model")
        open_static_action.triggered.connect(self.dynamic_button)
        file_menu.addAction(open_static_action)

        open_envi_action = QAction("Environment Model", self)
        open_envi_action.setStatusTip("Environment Model")
        open_envi_action.triggered.connect(self.envi_button)
        file_menu.addAction(open_envi_action)

        # creating a edit menu bar
        edit_menu = self.menuBar().addMenu("&Edit")
        #relationship
        self.rel_action = QAction("Change relationship parameters")
        # adding status tip
        self.rel_action.setStatusTip("Change relationship parameters")
        # when triggered undo the editor
        self.rel_action.triggered.connect(self.rel_open)
        edit_menu.addAction(self.rel_action)

        # creating a help menu bar
        help_menu = self.menuBar().addMenu("&Help")
        open_help_action = QAction("Help", self)
        open_help_action.triggered.connect(self.help_open)
        help_menu.addAction(open_help_action)

        self.setWindowTitle('Existing Model')

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
        self.response = False

    def isNaN(self,string):
        return string != string

    def button_graph(self):
        added_dataframe = pd.read_csv(creating_filename)
        relation_dataframe = pd.read_csv(relation_file)
        y_test = []
        y_pred = []
        values = ['0', 'STOR', 'CLOR', 'SIBOR', 'GUOR', 'CWOR', 'GSTOR', 'SOR',
                  'OOR', 'POR','SROR']
        for i,row in added_dataframe.iterrows():
            deviceDic = {}
            #To initialse all the intersections
            for z in list(added_dataframe["Device_id"]):
                if(z!=row.iloc[0]):
                    deviceDic[z] =0
            try:
                relation = list(row.iloc[14].split(","))
                for j in relation:
                    deviceDic[j.split(":")[0]] = j.split(":")[1]
            except:
                pass
            for j in deviceDic.keys():
                y_test.append(values.index(str(deviceDic[j])))
                relation = relation_dataframe.loc[relation_dataframe["Device_id"]==row.iloc[0],j].values[0]
                if(not self.isNaN(relation)):
                    y_pred.append(values.index(relation))
                else:
                    y_pred.append(0)
        pred_y = []
        for i in range(0,len(y_pred)):
            pred_y.append(-1*y_pred[i])
        x_devices = np.arange(len(y_test))
        label  = [ 'STOR', 'CLOR', 'SIBOR', 'GUOR', 'CWOR', 'GSTOR', 'SOR',
                   'OOR', 'POR','SROR']
        label = label[::-1]
        label = label+['No-Relation', 'STOR', 'CLOR', 'SIBOR', 'GUOR', 'CWOR', 'GSTOR', 'SOR',
                       'OOR', 'POR','SROR']

        self.canvas.ax.bar(x_devices,y_test,label="Before Simulation")
        self.canvas.ax.bar(x_devices,pred_y,label="After Simulation")
        self.canvas.ax.legend()
        self.canvas.ax.set_xlabel("Device Numbers")
        self.canvas.ax.axis([-1,len(y_test),-10,10])
        self.canvas.ax.set_yticklabels(label)
        self.canvas.ax.set_title("Comparision b/w Before and After Simulation")
        self.canvas.ax.set_yticks(np.arange(-10,11))
        self.canvas.draw()

    def help_open(self):
        QMessageBox.information(self,"HELP","1.  Choose objects and define characteristics to them such as objectprofiling and communication protocols.\n"
                                            "2.  Drag and Drop objects into the simulation area.\n"
                                            "3.  Define links between any two objects.\n"
                                            "4.  Define relationship between only those objects that are linked.\n"
                                            "5.  Specify  time  and  objects  that  are  mobile  will  move  around  thesimulator.\n"
                                            "6.  The user then clicks on the ’Find Relationship’ button to obtainsimulated relationships.\n"
                                            "7.  A graph is plotted when the user clicks on ’Plot differences’ stat-ing the differences between the User established relationships andSimulation obtained relationships.")

    def rel_open(self):
        relLayout = RelationChange()
        # if executed
        if relLayout.exec_():
            pass

    def dynamic_button(self):
        main_page.close()
        if(self.response):
            DynamicModel.start()

    def envi_button(self):
        main_page.close()
        if(self.response):
            EnvironmentModel.start()

    #To exit notification
    def closeEvent(self,event):
        message = QMessageBox.question(self,"Message","This will Quit Existing Page ?",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)

        if message == QMessageBox.Yes:
            self.response = True
            event.accept()
        else:
            self.response = False
            event.ignore()

def start():
    global main_page
    main_page = AppDemo()
    main_page.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())

