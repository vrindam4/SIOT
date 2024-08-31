import sched
import shutil
import string
import sys
import datetime,os


from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, \
    QGridLayout, QLineEdit, QLabel, QFrame, QMessageBox, QComboBox, QRadioButton, QFormLayout, QMainWindow, QScrollArea, \
    QDialog, QAction
from PyQt5.QtCore import Qt, QMimeData, QLine, QPoint, QTimer
from PyQt5.QtGui import QDrag, QPainter, QPen,QBrush, QColor
import pandas as pd
import random,math
import numpy as np
import DynamicModel,StatsModel
import StaticModel


class Button(QPushButton):
    def __init__(self, button_text, parent):
        super().__init__(button_text, parent)
        self.setFixedSize(30,30)
        self.setStyleSheet('width: 40px; height: 20px; font-size: 15px')
    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.LeftButton:
            print('press')

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
        # FrameWorkValue["Object_id"] = l1
        # FrameWorkValue["Device_id"]=l1
        # FrameWorkValue["Device"]=l1
        # FrameWorkValue["Connectivity"]=l1
        # FrameWorkValue["Device Distribution"]=l1
        # FrameWorkValue["Owner_id"]=l1
        # FrameWorkValue["Owner_name"]=l1
        # FrameWorkValue["Manufacturing_id"]=l1
        # FrameWorkValue["Service_id"]=l1
        # FrameWorkValue["Application_id"]=l1
        # FrameWorkValue["Connectivity"]=l1
        FrameWorkValue["Service"] = l1
        FrameWorkValue["Application"] =l1

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
        self.device = ""
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

class Device_Buttons(QPushButton):

    def __init__(self, title, name,parent):
        super().__init__(title, parent)
        self.setStyleSheet("border-image:url(test.jpg);")
        self.setFixedSize(80,70)
        input_dataframe = pd.read_csv("Input_sheet.csv")
        row = input_dataframe.loc[input_dataframe['Device'] == name]
        self.device = row.iloc[0,input_dataframe.columns.get_loc("Device")]
        self.device_type = row.iloc[0,input_dataframe.columns.get_loc("Input")]
        self.device_mobility = row.iloc[0,input_dataframe.columns.get_loc("Type")]
        self.connectivity = row.iloc[0,input_dataframe.columns.get_loc("Connectivity")]

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
        # self.sensor_id = FrameWorkValue["Sensor_id"].text()
        # self.device_mobility = QListWidgetItem("")
        # self.device_id =FrameWorkValue["Device_id"]
        # self.device_connectivity =FrameWorkValue["Connectivity"]
        # self.device_mobility = FrameWorkValue["Device_mobility"]
        # self.setStyleSheet("background-image:url(test.jpg);width: 30px; height: 30px; font-size: 15px;color:black")
        hoverlist = ["Sensor_id","Sensor_name","Application_id","Application_name"]
        hovertext = ""
        for i in FrameWorkValue:
            if(i in hoverlist):
                hovertext = hovertext+FrameWorkValue[i].text()
                hovertext = hovertext+"\n"
        hovertext = hovertext[:-1]
        self.setToolTip(hovertext)

class AddButtonDevice(QPushButton):
    def __init__(self):
        super().__init__()
        self.setParent(simLayout)
        self.setFixedSize(30,40)
        self.device_id =FrameWorkValue["Device_id"]
        self.device_connectivity =FrameWorkValue["Connectivity"]
        self.device_mobility = FrameWorkValue["Device_mobility"]
        # self.sensor_id = ""
        # self.setStyleSheet("background-image:url(test.jpg);width: 30px; height: 30px; font-size: 15px;color:black")
        hoverlist = ["Device_id","Device","Device Distribution","Connectivity"]
        hovertext = ""
        for i in FrameWorkValue:
            if(i in hoverlist):
                hovertext = hovertext+FrameWorkValue[i].text()
                hovertext = hovertext+"\n"
        hovertext = hovertext[:-1]
        self.setToolTip(hovertext)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        #On Clicking the Object in the simulator
        if e.button() == Qt.LeftButton:
            device_id = self.device_id.text()
            added_dataframe = pd.read_csv(creating_filename)
            #Reading Profile Data of each object from database and adding it in the profiling section
            profilingArea.device_id.setText(device_id)
            profilingArea.device.setText(str(added_dataframe.loc[added_dataframe["Device_id"]==device_id,"Device"].values[0]))
            profilingArea.device_type.setText(str(added_dataframe.loc[added_dataframe["Device_id"]==device_id,"Device_type"].values[0]))
            profilingArea.device_mobility.setText(str(added_dataframe.loc[added_dataframe["Device_id"]==device_id,"Device_mobility"].values[0]))
            profilingArea.owner_id.setText(str(added_dataframe.loc[added_dataframe["Device_id"]==device_id,"Owner_id"].values[0]))
            profilingArea.manufacuting_id.setText(str(added_dataframe.loc[added_dataframe["Device_id"]==device_id,"Manufacturing_id"].values[0]))
            profilingArea.service_id.setText(str(added_dataframe.loc[added_dataframe["Device_id"]==device_id,"Service_id"].values[0]))
            profilingArea.application_id.setText(str(added_dataframe.loc[added_dataframe["Device_id"]==device_id,"Application_id"].values[0]))
            profilingArea.application_id_loaded.setText(str(added_dataframe.loc[added_dataframe["Device_id"]==device_id,"Application_id_sensor"].values[0]))
            profilingArea.connectivity.setText(str(added_dataframe.loc[added_dataframe["Device_id"]==device_id,"Connectivity"].values[0]))

class DesignArea(QFrame):

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFixedSize(700,650)
        self.setStyleSheet("background-color:white;")
        self.lines = []
        self.relation_line = [[],[],[],[],[],[],[],[],[],[],[]]
        self.relation_line1 = []
        self.relation_line2 = []
        self.relation_line3 = []
        self.relation_line4 = []
        self.relation_line5 = []
        self.relation_line6 = []
        self.relation_line7 = []
        self.relation_line8 = []
        self.relation_line9 = []
        self.relation_line10 = []

        self.circle_wifi = []
        self.circle_zigbee = []
        self.circle_gsm = []
        self.circle_bluetooth = []
        self.objectsPresent = []
        self.applicationArea = []
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

        #For Circle of Protocols
        if(len(self.circle_wifi)>0):
            painter2 = QPainter(self)
            pen2 = QPen(Qt.black, 2)
            pen2.setStyle(Qt.DashLine)
            painter2.setPen(pen2)
            for center in self.circle_wifi:
                painter2.drawEllipse(center,40,40)
                # painter2.drawText(center,"This is circel")
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
        #Application Boundary Circle
        if(len(self.applicationArea)>0):
            painter6 = QPainter(self)
            pen6 = QPen(Qt.black, 2)
            # pen6.setStyle(Qt.DashLine)
            painter6.setPen(pen6)
            painter6.setBrush(QBrush(Qt.lightGray, Qt.Dense4Pattern))
            for center in self.applicationArea:
                painter6.drawEllipse(center,150,150)

    def dragEnterEvent(self, e):
        e.accept()

    def isNaN(self,string):
        return string != string

    def disCal(self,a_x,a_y,b_x,b_y):
        dis = math.sqrt((a_x-b_x)**2+(a_y-b_y)**2)
        return dis

    def sensor_value(self,sensor_name):
        if(sensor_name=="System Time"):
            now = datetime.datetime.now()
            dt_string = now.strftime("%H:%M")
            l1  = QListWidgetItem(str(dt_string))
            return(l1)
        elif(sensor_name=="Electronic gadget"):
            status = ["Present","Not Present"]
            l1  = QListWidgetItem(str(status[random.randint(0,1)]))
            return(l1)
        elif(sensor_name=="CO2"):
            l1  = QListWidgetItem(str(random.randint(350,450))+"ppm")
            return(l1)
        elif(sensor_name=="Sound"):
            l1  = QListWidgetItem(str(random.randint(30,100))+"dB")
            return(l1)
        elif(sensor_name=="Temperature"):
            l1  = QListWidgetItem(str(random.randint(-10,50))+"ºC")
            return(l1)
        elif(sensor_name=="Wind"):
            l1  = QListWidgetItem(str(random.randint(30,100))+"Kmph")
            return(l1)
        elif(sensor_name=="Solar Radiation"):
            l1  = QListWidgetItem(str(random.randint(1000,1380))+"W/m2")
            return(l1)
        elif(sensor_name=="SDR"):
            l1  = QListWidgetItem(str(round(random.uniform(0.1,1.2),2))+"J")
            return(l1)
        elif(sensor_name=="Doppler sensors"):
            status = ["Red","Green"]
            l1  = QListWidgetItem(str(status[random.randint(0,1)]))
            return(l1)
        elif(sensor_name=="LDR"):
            status = ["On","Off"]
            l1  = QListWidgetItem(str(status[random.randint(0,1)]))
            return(l1)
        elif(sensor_name=="Accelerometer"):
            l1  = QListWidgetItem(str(random.randint(0,160))+"Kmph")
            return(l1)
        elif(sensor_name=="Gyroscope"):
            l1  = QListWidgetItem(str(random.randint(0,360))+","+str(random.randint(0,360))+","+str(random.randint(0,360)))
            return(l1)
        elif(sensor_name=="3D MLI"):
            l1  = QListWidgetItem(str(random.randint(0,500)))
            return(l1)
        elif(sensor_name=="Level Indicator"):
            status = ["Full ","Empty"]
            l1  = QListWidgetItem(str(status[random.randint(0,1)]))
            return(l1)
        elif(sensor_name=="PLS"):
            status = ["Full ","Empty"]
            l1  = QListWidgetItem(str(status[random.randint(0,1)]))
            return(l1)
        elif(sensor_name=="Thermal sensor"):
            l1  = QListWidgetItem(str(round(random.uniform(96,103),2))+"F")
            return(l1)
        elif(sensor_name=="Pressure sensor"):
            l1  = QListWidgetItem(str(round(random.uniform(19,31),2))+"Hg")
            return(l1)
        elif(sensor_name=="ECG"):
            l1  = QListWidgetItem(str(random.randint(60,100))+"bpm")
            return(l1)
        elif(sensor_name=="Presence"):
            l1  = QListWidgetItem(str(random.randint(0,50)))
            return(l1)
        elif(sensor_name=="Energy Consumption"):
            l1  = QListWidgetItem(str(random.randint(0.1,1.2))+"J")
            return(l1)

    def dropEvent(self, e):

        position = e.pos()
        if(FrameWorkValue["Service"].text()!=""):
            services_dataframe = pd.read_csv("services.csv")
            #Reading the file
            sensor_dataframe = pd.read_csv(creating_filename_sensor)
            row  = services_dataframe.loc[services_dataframe['Service_name'] == FrameWorkValue["Service"].text()]
            devices = list(row.iloc[0,2].split(","))
            application_ids = set(sensor_dataframe["Application_id"])
            application_id_created = ""
            application_center = ""
            #To Check if the droped service is in the range of any application that is already present in the simulator area
            for i in application_ids:
                if(not self.isNaN(i)):
                    i_center = list(set(sensor_dataframe.loc[sensor_dataframe["Application_id"]==i,"Application_Centre"]))
                    x_center = i_center[-1].split(",")[0]
                    y_center = i_center[-1].split(",")[1]
                    if(self.disCal(int(x_center),int(y_center),int(position.x()),int(position.y()))<150):
                        #If it is inside a Application then the Application ID is assigned to this service
                        application_id_created = i
                        application_center = str(x_center)+","+str(y_center)
            for i in range(0,len(devices)):
                #Adding Services in the Dropped location and moving each sensor by 40 distance
                x = position.x()
                x = x+i*40
                y = position.y()
                #To create Service details
                l1  = QListWidgetItem("S"+str(len(sensor_dataframe)+1))
                FrameWorkValue["Sensor_id"]=l1
                l1  = QListWidgetItem(devices[i])
                FrameWorkValue["Sensor_name"]=l1
                l1  = QListWidgetItem(application_id_created)
                FrameWorkValue["Application_id"]=l1
                if(application_id_created!=""):
                    app_name  = sensor_dataframe.loc[sensor_dataframe["Application_id"]==application_id_created,"Application_name"].values[0]
                else:
                    app_name =""
                l1  = QListWidgetItem(app_name)
                FrameWorkValue["Application_name"]=l1
                l1  = QListWidgetItem(str(x)+","+str(y))
                FrameWorkValue["GPS_Start"]=l1
                l1  = QListWidgetItem(application_center)
                FrameWorkValue["Application_Centre"]=l1
                #To add Values to sensors
                if(devices[i]=="GPS"):
                    l1  = QListWidgetItem(str(x)+","+str(y))
                    FrameWorkValue["Value"] = l1
                else:
                    FrameWorkValue["Value"] = self.sensor_value(devices[i])
                #Creation of Sensors
                object_button = AddButton()
                #Senosor are not moving so we dont need them to add to a list
                # self.objectsPresent.append(object_button)
                object_button.move(QPoint(x,y))
                url = "sensors_images/"+(devices[i])
                object_button.setStyleSheet("border-image:url("+url+");width: 30px; height: 30px; font-size: 15px;color:black")
                object_button.show()

                #List of Values to Senosr.csv
                adding_values = ["Sensor_id","Application_id","Sensor_name","Application_name","GPS_Start","Application_Centre","Value"]
                #Convert data to text to save
                temp ={}
                for i in FrameWorkValue:
                    if(i in adding_values):
                        temp[i]= FrameWorkValue[i].text()
                #To add to database
                sensor_dataframe = sensor_dataframe.append(temp,ignore_index=True)
                sensor_dataframe.to_csv(creating_filename_sensor,header=True,index=False)
                l1 = QListWidgetItem("")
                FrameWorkValue["Service"] =l1
                serviceDropDown.services.setCurrentIndex(0)

        elif(FrameWorkValue["Application"].text()!=""):
            #Reading the file
            sensor_dataframe = pd.read_csv(creating_filename_sensor)
            application_dataframe = pd.read_csv("applications.csv")
            services_dataframe = pd.read_csv("services.csv")
            #Creating application id
            application_id_created = "A"+str(len(sensor_dataframe["Application_id"])+1)

            #Reading Application details
            row  = application_dataframe.loc[application_dataframe['Applications'] == FrameWorkValue["Application"].text()]
            services = list(row.iloc[0,3].split(","))
            max_devices = -1
            for j in range(0,len(services)):
                # Reading service deatils from database
                row_service  = services_dataframe.loc[services_dataframe['Service_name'] == services[j]]
                devices = list(row_service.iloc[0,2].split(","))
                if(max_devices<len(devices)):
                    max_devices = len(devices)
                #Adding Sensors to simulator area
                for i in range(0,len(devices)):
                    #Adding Sensors by moving services sensors in a row and adding different services in column wise
                    x = position.x()
                    x = x+i*40
                    y = position.y()
                    y = y+j*40
                    #To create device_id
                    l1  = QListWidgetItem("S"+str(len(sensor_dataframe)+1))
                    FrameWorkValue["Sensor_id"]=l1
                    l1  = QListWidgetItem(devices[i])
                    FrameWorkValue["Sensor_name"]=l1
                    l1  = QListWidgetItem(application_id_created)
                    FrameWorkValue["Application_id"]=l1
                    l1  = QListWidgetItem(FrameWorkValue["Application"].text())
                    FrameWorkValue["Application_name"]=l1
                    l1  = QListWidgetItem(str(x)+","+str(y))
                    FrameWorkValue["GPS_Start"]=l1

                    #To add Values to sensors
                    if(devices[i]=="GPS"):
                        l1  = QListWidgetItem(str(x)+","+str(y))
                        FrameWorkValue["Value"] = l1
                    else:
                        FrameWorkValue["Value"] = self.sensor_value(devices[i])

                    #Creation of Sensors
                    object_button = AddButton()
                    #Senosor are not moving so we dont need them to add to a list
                    # self.objectsPresent.append(object_button)
                    object_button.move(QPoint(x,y))
                    url = "sensors_images/"+(devices[i])
                    object_button.setStyleSheet("border-image:url("+url+");width: 30px; height: 30px; font-size: 15px;color:black")
                    object_button.show()

                    #List of Values to Senosr.csv
                    adding_values = ["Sensor_id","Application_id","Sensor_name","Application_name","GPS_Start","Value"]
                    #Convert data to text to save
                    temp ={}
                    for i in FrameWorkValue:
                        if(i in adding_values):
                            temp[i]= FrameWorkValue[i].text()
                    #To add to database
                    sensor_dataframe = sensor_dataframe.append(temp,ignore_index=True)
                    sensor_dataframe.to_csv(creating_filename_sensor,header=True,index=False)

            #TODO: Drive monitoring should check formula of center
            centre_str = str(position.x()+(max_devices//2)*40)+","+str(position.y()+(len(services)//2)*40)
            centre = QPoint(position.x()+(max_devices//2)*40,position.y()+(len(services)//2)*40)
            simLayout.applicationArea.append(centre)
            simLayout.update()

            sensor_dataframe.loc[sensor_dataframe["Application_id"]==application_id_created,"Application_Centre"]=centre_str
            sensor_dataframe.to_csv(creating_filename_sensor,header=True,index=False)

            l1 = QListWidgetItem("")
            FrameWorkValue["Application"] =l1
            applicationDropDown.application.setCurrentIndex(0)
            linkArea.device2.addItem(FrameWorkValue["Application_id"].text())

        elif(e.source().device!=""):
            application_dataframe = pd.read_csv("applications.csv")
            for i in range(0,int(countOfObjects.text())):
                #Position of Object
                if(i==0):
                    x = position.x()
                    y = position.y()
                else:
                    x = random.randint(0,700)
                    y = random.randint(0,650)
                #Reading the file
                added_dataframe = pd.read_csv(creating_filename)
                FrameWorkValue["Device_id"] = QListWidgetItem("D"+str(len(added_dataframe)+1))
                FrameWorkValue["Device"] = QListWidgetItem(e.source().device)
                FrameWorkValue["Device_type"] = QListWidgetItem(e.source().device_type)
                FrameWorkValue["Device_mobility"] = QListWidgetItem(e.source().device_mobility)
                FrameWorkValue["Connectivity"] = QListWidgetItem(e.source().connectivity)
                #Profiling random
                FrameWorkValue["Object_id"] = QListWidgetItem(str(random.randint(0,25)))
                FrameWorkValue["Owner_id"] = QListWidgetItem(str(random.randint(0,25)))
                res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
                FrameWorkValue["Owner_name"] = QListWidgetItem(str(res))
                FrameWorkValue["Manufacturing_id"] = QListWidgetItem(str(random.randint(0,25)))
                # FrameWorkValue["Service_id"] = QListWidgetItem(str(random.randint(1,16)))

                sensor_dataframe = pd.read_csv(creating_filename_sensor)
                application_ids = list(sensor_dataframe["Application_id"])
                if(len(application_ids)==0):
                    #If no application is there in the simulation area a defualt application will be assigned
                    app_id = str(random.randint(1,26))
                    FrameWorkValue["Application_id"] = QListWidgetItem(app_id)
                    service_dic = {"1":"5,8,10","2":"4,8,9","3":"7","4":"1,5,8,10","5":"1,2,10,11","6":"1,5",
                                   "7":"16","8":"3","9":"1,13","10":"1,5,6","11":"5,6,8,9,10",
                                   "12":"4,5","13":"5,6","14":"3,8,13","15":"1,5","16":"14",
                                   "17":"7,15","18":"4","19":"5,6,7","20":"1,2,3,4","21":"4,5",
                                   "22":"4,5","23":"12,16","24":"1,4","25":"1,2","26":"1,2,5,6",}
                    FrameWorkValue["Service_id"] = QListWidgetItem(str(service_dic[app_id]))
                else:
                    application_id = str(application_ids[random.randint(0,len(application_ids)-1)])
                    FrameWorkValue["Application_id_sensor"] = QListWidgetItem(application_id)
                    application_name = sensor_dataframe.loc[sensor_dataframe["Application_id"]==application_id,"Application_name"]
                    application_name = application_name.values[0]
                    temp = application_dataframe.loc[application_dataframe["Applications"]==application_name,"Services id"]
                    temp1 = application_dataframe.loc[application_dataframe["Applications"]==application_name,"Application id"]
                    FrameWorkValue["Service_id"] = QListWidgetItem(str(temp.values[0]))
                    FrameWorkValue["Application_id"] = QListWidgetItem(str(temp1.values[0]))

                l1  = QListWidgetItem(str(x)+","+str(y))
                FrameWorkValue["GPS_Start"]=l1

                #Creating Button for Object on Design Area
                object_button = AddButtonDevice()
                object_button.move(QPoint(x,y))
                url = "object_images/"+(FrameWorkValue["Device"].text())+".jpg"
                object_button.setStyleSheet("border-image:url("+url+");width: 15px; height: 15px; font-size: 15px;color:black")
                # object_button.setStyleSheet("background-image:url("+url+");")
                self.objectsPresent.append(object_button)
                object_button.show()

                #Circle Drawing
                centre = QPoint(x+25,y+25)
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
                data_tobeAdded = ["Device_id","Device","Device_type","Device_mobility","Device Distribution","Object_id","Owner_id",
                                  "Manufacturing_id","Service_id","Application_id","Connectivity","GPS_Start","Application_id_sensor"]
                temp ={}
                for i in FrameWorkValue:
                    if(i in data_tobeAdded):
                        temp[i]= FrameWorkValue[i].text()

                #To add to database
                added_dataframe = added_dataframe.append(temp,ignore_index=True)
                added_dataframe.to_csv(creating_filename,header=True,index=False)
                e.setDropAction(Qt.MoveAction)

                #Setting count back to 1
                countOfObjects.setText("1")

                # #To add Values to the Combo-box
                linkArea.device1.addItem(FrameWorkValue["Device_id"].text())
                # linkArea.device2.addItem(FrameWorkValue["Device_id"].text())
                # realtaionArea.device1.addItem(FrameWorkValue["Device_id"].text())
                # realtaionArea.device2.addItem(FrameWorkValue["Device_id"].text())
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

class ServiceDropdown(QFrame):
    def __init__(self):
        super().__init__()
        # global DeviceDistribution_list
        self.setFrameStyle(2)
        self.setFixedSize(350,60)
        vLayout = QVBoxLayout()
        head = QLabel("Service Management and Composition")
        #Services Dropdown
        self.services = QComboBox()
        services_list = ["Select a Service"]
        services_dataframe = pd.read_csv("services.csv")
        services_list = services_list+list(services_dataframe["Service_name"])
        self.services.addItems(services_list)
        self.services.currentIndexChanged.connect(self.service_function)
        self.service_function(0)
        # vLayout.addWidget(head)
        vLayout.addWidget(self.services)
        self.setLayout(vLayout)

    def service_function(self,index):
        services_selected = self.services.currentText()
        if(services_selected != "Select a Service"):
            url = "services_images/"+services_selected
            l1 = QListWidgetItem(services_selected)
            FrameWorkValue["Service"] = l1
            l1 = QListWidgetItem("")
            FrameWorkValue["Application"] = l1
            adding_button.setStyleSheet("border-image:url("+url+");")

class ApplicationDropdown(QFrame):
    def __init__(self):
        super().__init__()
        # global DeviceDistribution_list
        self.setFrameStyle(2)
        self.setFixedSize(350,60)
        vLayout = QVBoxLayout()
        #Application Dropdown
        self.application = QComboBox()
        application_list = ["Select a Application"]
        application_dataframe = pd.read_csv("applications.csv")
        application_list = application_list+list(application_dataframe["Applications"])
        self.application.addItems(application_list)
        self.application.currentIndexChanged.connect(self.application_function)
        self.application_function(0)
        vLayout.addWidget(self.application)
        self.setLayout(vLayout)
    def application_function(self,index):
        application_select = self.application.currentText()
        if(application_select != "Select a Application"):
            url = "application_images/"+application_select
            l1 = QListWidgetItem(application_select)
            FrameWorkValue["Application"] = l1
            l1 = QListWidgetItem("")
            FrameWorkValue["Service"] = l1
            adding_button.setStyleSheet("border-image:url("+url+");")

class LinkArea(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(2)
        self.setFixedSize(350,150)
        #To read Data From database
        # self.added_dataframe = pd.read_csv(creating_filename)
        self.resize(400,200)
        self.lay = QVBoxLayout()
        head = QLabel("Choose Device and ApplicationID to load Application",self)
        self.device1 = QComboBox(self)
        # self.device1.addItems(list(self.added_dataframe["Device_id"]))
        self.device1.setFixedWidth(100)
        self.device2 = QComboBox(self)
        # self.device2.addItems(list(self.added_dataframe["Device_id"]))
        self.device2.setFixedWidth(100)
        but = QPushButton("Edit Application Preferences",self)
        but1 = QPushButton("Load More Applications",self)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.device1)
        hLayout.addWidget(self.device2)

        but.clicked.connect(self.onClicking)
        but1.clicked.connect(self.onClickingMulitple)

        self.lay.addWidget(head)
        self.lay.addLayout(hLayout)
        self.lay.addWidget(but)
        self.lay.addWidget(but1)

        self.setLayout(self.lay)
        self.setWindowTitle("Link")


    #Function to check if value is nan
    def isNaN(self,string):
        return string != string

    def onClickingMulitple(self):
        entered_device  = self.device1.currentText()
        entered_applicationId  = self.device2.currentText()
        added_dataframe = pd.read_csv(creating_filename)

        sensor_dataframe = pd.read_csv(creating_filename_sensor)
        application_name = sensor_dataframe.loc[sensor_dataframe["Application_id"]==entered_applicationId,"Application_name"]
        application_name = application_name.values[0]
        application_dataframe = pd.read_csv("applications.csv")
        temp1 = application_dataframe.loc[application_dataframe["Applications"]==application_name,"Application id"]
        temp1 = temp1.values[0]
        temp = application_dataframe.loc[application_dataframe["Applications"]==application_name,"Services id"]
        temp = temp.values[0]

        added_dataframe.loc[added_dataframe["Device_id"]==entered_device,"Application_id_sensor"] = \
            added_dataframe.loc[added_dataframe["Device_id"]==entered_device,"Application_id_sensor"]+","+entered_applicationId
        added_dataframe.loc[added_dataframe["Device_id"]==entered_device,"Application_id"] = \
            str(added_dataframe.loc[added_dataframe["Device_id"]==entered_device,"Application_id"].values[0])+","+str(temp1)
        added_dataframe.loc[added_dataframe["Device_id"]==entered_device,"Service_id"] = \
            str(added_dataframe.loc[added_dataframe["Device_id"]==entered_device,"Service_id"].values[0])+","+str(temp)
        added_dataframe.to_csv(creating_filename,header=True,index=False)

    def onClicking(self):
        entered_device  = self.device1.currentText()
        entered_applicationId  = self.device2.currentText()
        added_dataframe = pd.read_csv(creating_filename)

        sensor_dataframe = pd.read_csv(creating_filename_sensor)
        application_name = sensor_dataframe.loc[sensor_dataframe["Application_id"]==entered_applicationId,"Application_name"]
        application_name = application_name.values[0]
        application_dataframe = pd.read_csv("applications.csv")
        temp1 = application_dataframe.loc[application_dataframe["Applications"]==application_name,"Application id"]
        temp1 = temp1.values[0]
        temp = application_dataframe.loc[application_dataframe["Applications"]==application_name,"Services id"]

        added_dataframe.loc[added_dataframe["Device_id"]==entered_device,"Application_id_sensor"] = entered_applicationId
        added_dataframe.loc[added_dataframe["Device_id"]==entered_device,"Application_id"] = temp1
        added_dataframe.loc[added_dataframe["Device_id"]==entered_device,"Service_id"] = str(temp.values[0])
        added_dataframe.to_csv(creating_filename,header=True,index=False)

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

class StatisticArea(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(2)
        self.setFixedSize(350,100)
        lay = QVBoxLayout()
        head = QLabel("Experiment and Result Analysis",self)
        global results_but
        results_but = QPushButton("Results",self)
        results_but.setEnabled(False)
        results_but.clicked.connect(self.onClicking)
        lay.addWidget(head)
        lay.addWidget(results_but)
        self.setLayout(lay)

    def onClicking(self):
        StatsModel.start(session_path)
        # main_page.close()

class ProfilingArea(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(2)
        self.setFixedSize(350,350)
        heading = QLabel("Object Profiling")
        head1 = QLabel("Device ID")
        head2 = QLabel("Device")
        head3 = QLabel("Device Type")
        head4 = QLabel("Device mobility")
        head5 = QLabel("Owner id")
        head6 = QLabel("Manufacturing id")
        head7 = QLabel("Service id")
        head8 = QLabel("Application id")
        head9 = QLabel("Application Loaded")
        head10 = QLabel("Connectivity")
        self.device_id = QLineEdit("")
        self.device_id.setFixedSize(150,30)
        self.device = QLineEdit("")
        self.device.setFixedSize(150,30)
        self.device_type = QLineEdit("")
        self.device_type.setFixedSize(150,30)
        self.device_mobility = QLineEdit("")
        self.device_mobility.setFixedSize(150,30)
        self.owner_id = QLineEdit("")
        self.owner_id.setFixedSize(150,30)
        self.manufacuting_id = QLineEdit("")
        self.manufacuting_id.setFixedSize(150,30)
        self.service_id = QLineEdit("")
        self.service_id.setFixedSize(150,30)
        self.application_id = QLineEdit("")
        self.application_id.setFixedSize(150,30)
        self.application_id_loaded = QLineEdit("")
        self.application_id_loaded.setFixedSize(150,30)
        self.connectivity = QLineEdit("")
        self.connectivity.setFixedSize(150,30)

        lay = QFormLayout()
        lay.addWidget(heading)
        lay.addRow(head1,self.device_id)
        lay.addRow(head2,self.device)
        lay.addRow(head3,self.device_type)
        lay.addRow(head4,self.device_mobility)
        lay.addRow(head5,self.owner_id)
        lay.addRow(head6,self.manufacuting_id)
        lay.addRow(head7,self.service_id)
        lay.addRow(head8,self.application_id)
        lay.addRow(head9,self.application_id_loaded)
        lay.addRow(head10,self.connectivity)

        self.setLayout(lay)

#TODO: Delete this classs
class RelationshipArea(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(2)
        self.setFixedSize(350,250)
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

        self.radio5 = QRadioButton("GOR")
        self.radio6 = QRadioButton("STGOR")
        self.radio7 = QRadioButton("SVOR")
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

class Range(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(2)
        self.setFixedSize(500,45)
        l1 = QLabel("Range")

        disablebut = QPushButton("Disable",self)
        disablebut.setFixedSize(150,30)
        disablebut.clicked.connect(self.onClicking_disable)

        enablebut = QPushButton("Enable",self)
        enablebut.setFixedSize(150,30)
        enablebut.clicked.connect(self.onClicking_enable)

        hLayoutofCircle = QHBoxLayout()
        hLayoutofCircle.addWidget(disablebut)
        hLayoutofCircle.addWidget(enablebut)

        hLayout = QHBoxLayout()
        hLayout.addWidget(l1)
        hLayout.addLayout(hLayoutofCircle)

        self.setLayout(hLayout)

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

class InputArea(QFrame):
    def __init__(self):
        super().__init__()
        self.resize(350,200)
        #If button is clicked or no

        self.lay = QGridLayout()
        self.setFrameStyle(2)
        self.setFixedSize(720,410)

        gridLayout = QGridLayout()
        object_list  = os.listdir("object_images")
        count = 0
        vLayout_out = QVBoxLayout()
        for  i in range(0,len(object_list)//4):
            hLayout = QHBoxLayout()
            for j in range(0,len(object_list)//4):
                k = object_list[count]
                count = count+1
                adding_button = Device_Buttons("",k.split(".")[0],self)
                url = "object_images/"+k
                adding_button.setStyleSheet("border-image:url("+url+");")

                vLayout=QVBoxLayout()
                name= adding_button.device
                d_type= adding_button.device_type
                vLayout.addWidget(adding_button,alignment=Qt.AlignCenter)
                label = QLineEdit(name+"\n("+d_type+")")
                label.setFixedSize(175,30)
                label.setEnabled(False)
                label.setStyleSheet("border :2px solid ;"
                                    "border-color : black;color:black;")
                label.setAlignment(Qt.AlignCenter)
                vLayout.addWidget(label)
                hLayout.addLayout(vLayout)
            vLayout_out.addLayout(hLayout)

        gridLayout.addLayout(vLayout_out,0,0)

        global  countOfObjects
        countOfObjects = QLineEdit()
        countOfObjects.setPlaceholderText("Count")
        countOfObjects.setText("1")
        countOfObjects.setFixedSize(150,30)
        l1 = QLabel("Count of Objects")
        hLayout = QHBoxLayout()
        hLayout.addStretch()
        hLayout.addWidget(l1)
        hLayout.addWidget(countOfObjects)
        hLayout.addStretch()

        vLayout = QVBoxLayout()
        heading = QLabel("Add Devices")
        heading.setAlignment(Qt.AlignCenter)
        # vLayout.addWidget(heading)
        vLayout.addLayout(gridLayout)
        vLayout.addLayout(hLayout)
        # vLayout.addLayout(hLayoutofCircle)
        rangeArea = Range()
        vLayout.addWidget(rangeArea)
        self.setLayout(vLayout)

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
            results_but.setEnabled(True)
            simLayout.relation_line = [[],[],[],[],[],[],[],[],[],[],[]]
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
        self.setFixedSize(350,150)
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
            simLayout.circle_zigbee = []
            simLayout.circle_wifi = []
            simLayout.circle_gsm = []
            simLayout.circle_bluetooth = []
            simLayout.lines =[]
            # simLayout.realtion_lines = []
            simLayout.relation_line = [[],[],[],[],[],[],[],[],[],[],[]]
            simLayout.relation_line1 = []
            simLayout.relation_line2 = []
            simLayout.relation_line3 = []
            simLayout.relation_line4 = []
            simLayout.relation_line5 = []
            simLayout.relation_line6 = []
            simLayout.relation_line7 = []
            simLayout.relation_line8 = []
            simLayout.relation_line9 = []
            simLayout.relation_line10 = []
            simLayout.update()
            lis_gps =[]
            lis_device_id = []
            lis_intersection = []
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
                    while(new_x<0 or new_x>625):
                        new_x = i.x()+random.randrange(-100,100)
                    while(new_y<0 or new_y>675):
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

class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 800)
        global session_path
        date = datetime.datetime.now()
        cwd = os.getcwd()
        print(cwd)
        os.mkdir(cwd+"/simulation_data/EnvironmentModel/"+str(date))
        session_path = cwd+"/simulation_data/EnvironmentModel/"+str(date)
        global creating_filename,creating_filename_sensor
        creating_filename = cwd+"/simulation_data/EnvironmentModel/"+str(date)+"/added.csv"
        creating_filename_sensor = cwd+"/simulation_data/EnvironmentModel/"+str(date)+"/sensor.csv"
        shutil.copyfile(cwd+"/added.csv",creating_filename)
        shutil.copyfile(cwd+"/sensor.csv",creating_filename_sensor)
        print(date)
        #Main Grid layout
        mainLayout = QGridLayout(self)

        #List of Framework
        global simLayout1
        simLayout1  = DeviceFrameWork()
        simLayout1.setFixedSize(550,100)

        #Service and Application Area
        vLayoutofServiceApplication = QVBoxLayout()
        global serviceDropDown,applicationDropDown
        serviceDropDown = ServiceDropdown()
        applicationDropDown = ApplicationDropdown()
        head = QLabel("Service Management and Composition")
        vLayoutofServiceApplication.addWidget(head)
        vLayoutofServiceApplication.addWidget(serviceDropDown)
        vLayoutofServiceApplication.addWidget(applicationDropDown)


        #Object Button
        global adding_button
        adding_button = Button_Device("",self)
        adding_button.setFixedSize(100,75)

        head = QLabel("Selected Service/Application")
        vLayoutofObjectButton = QVBoxLayout()
        vLayoutofObjectButton.addWidget(head)
        vLayoutofObjectButton.addWidget(adding_button)

        hLayoutofFrameWork = QHBoxLayout()
        hLayoutofFrameWork.addLayout(vLayoutofObjectButton)
        hLayoutofFrameWork.addLayout(vLayoutofServiceApplication)

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
        head = QLabel("Add Devices")
        inputArea = InputArea()
        # vLayoutofLastColoumn.addWidget(head)
        vLayoutofLastColoumn.addWidget(inputArea)


        # vLayoutofLastColoumn.addLayout(vLayoutofDistribution)
        # vLayoutofLastColoumn.addWidget(serviceDropDown)

        global linkArea
        global profilingArea

        hLayoutofLinkandRelation = QHBoxLayout()
        linkArea = LinkArea()
        statisticArea = StatisticArea()
        profilingArea = ProfilingArea()

        vLayoutProfile = QVBoxLayout()
        # vLayoutProfile.addWidget(applicationDropDown)
        vLayoutProfile.addWidget(profilingArea)

        #Movement and Time area
        movementRelationfinder = MovementRelationFinder()

        # moveButton = MoveButton("Move",self)
        # movementRelationfinder = MovementRelationFinder()
        vLayoutofLinkArea = QVBoxLayout()
        # vLayoutofLinkArea.addWidget(serviceDropDown)
        # vLayoutofLinkArea.addWidget(applicationDropDown)
        vLayoutofLinkArea.addWidget(linkArea)
        vLayoutofLinkArea.addWidget(movementRelationfinder)
        vLayoutofLinkArea.addWidget(statisticArea)

        hLayoutofLinkandRelation.addLayout(vLayoutofLinkArea)
        hLayoutofLinkandRelation.addLayout(vLayoutProfile)
        # hLayoutofLinkandRelation.addWidget(statisticArea)

        vLayoutofLastColoumn.addLayout(hLayoutofLinkandRelation)


        mainLayout.addLayout(vLayoutofFirstColoumn,0,0)
        mainLayout.addLayout(vLayoutofLastColoumn,0,1)

        #Menu Layout
        file_menu = self.menuBar().addMenu("&Navigate")
        open_static_action = QAction("Static Model", self)
        open_static_action.setStatusTip("Static Model")
        open_static_action.triggered.connect(self.static_button)
        file_menu.addAction(open_static_action)

        open_envi_action = QAction("Dynamic Model", self)
        open_envi_action.setStatusTip("Environment Model")
        open_envi_action.triggered.connect(self.dynamic_button)
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

        self.setWindowTitle('Create Environment')
        scrollArea = QScrollArea()
        widget = QWidget()
        widget.setLayout(mainLayout)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(widget)

        self.setCentralWidget(scrollArea)
        # self.setLayout(mainLayout)
        self.showMaximized()
        self.response = False

    def help_open(self):
        QMessageBox.information(self,"HELP","1.  Select an application from drop-down,drag and drop into simula-tion are.\n"
                                            "2.  Select services from drop-down,drag and drop services either in-side a specific application area or outside application area in thesimulation area.\n"
                                            "3.  Specify the number for a specific object in the text field provided.\n"
                                            "4.  Drag and Drop objects into the simulation area.\n"
                                            "5.  The user can Edit or Load multiple applications onto the objects.\n"
                                            "6.  The user can click on any object present in simulation area to viewits object profiling in Profiling section provided.\n"
                                            "7.  Specify  time  and  objects  that  are  mobile  will  move  around  thesimulator.\n"
                                            "8.  The user then clicks on the ’Find Relationship’ button to obtainsimulated relationships.\n"
                                            "9.  The user then moves to analyse the simulation by clicking on the’Results and Analysis’ button.")

    def rel_open(self):
        relLayout = RelationChange()
        # if executed
        if relLayout.exec_():
            pass

    def static_button(self):
        main_page.close()
        if(self.response):
            StaticModel.start()

    def dynamic_button(self):
        main_page.close()
        if(self.response):
            DynamicModel.start()

    #To exit notification
    def closeEvent(self,event):
        message = QMessageBox.question(self,"Message","Do you want to continue ?",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)

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
    global main_page
    main_page = AppDemo()
    main_page.show()
    sys.exit(app.exec_())

