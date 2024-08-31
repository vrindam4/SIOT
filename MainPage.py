
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QImage, QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import *
import sys
import os
import pandas as pd

import DynamicModel
import EnvironmentModel
import StaticModel
import StatsModel


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

class Window(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.resize(1000, 800)
        headingLayout =QVBoxLayout()
        im = QImage("./back.jpg")
        sImage = im.scaled(QSize(1500, 1000))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        label1=QLabel("AI BASED ASSISTIVE INTERFACE FOR SOCIAL INTERNET OF THINGS")
        label1.setAlignment(Qt.AlignCenter)
        label1.setFont(QFont("Arial",25))

        label2 = QLabel("To get information about neighbourhood objects and the service it is providing in real time.\nTo allow objects to have their own social networks and classify similar objects depending on their \n characteristics(relations) using AI.")
        label2.setFont(QFont("Arial", 18))
        label2.setAlignment(Qt.AlignCenter)
        headingLayout.addWidget(label1)
        headingLayout.addWidget(label2)


        buttonLayout= QGridLayout()
        self.static = QPushButton("Existing")
        self.static.setFont(QFont("Arial",20))
        self.static.setStyleSheet("border: 2px solid black;background-color: rgba(81,102,109,20%);border-radius:10px;")
        buttonLayout.addWidget(self.static,0,0)
        textArea1 = QTextEdit()
        textArea1.setStyleSheet("background-color : rgba(255,0,0,10%);")
        textArea1.setText("This is similar to the existing simulators.Object profiling is taken as input.Mobility has been given only to mobile objects which can move around the fixed simulation area for a certain time specified by the user which can be visualized.Based on previously regulated relationship conditions,relations between the objects.")
        textArea1.setFont(QFont("Arial", 20))
        textArea1.setReadOnly(True)
        textArea1.setFixedSize(350, 250)
        buttonLayout.addWidget(textArea1,1,0)
        self.dynamic = QPushButton("Dynamic")
        self.dynamic.setStyleSheet("border: 2px solid black;background-color: rgba(81,102,109,20%);border-radius:10px;")
        self.dynamic.setFont(QFont("Arial", 20))
        buttonLayout.addWidget(self.dynamic,0,1)
        textArea2 = QTextEdit()
        textArea2.setText("There is movement involved and the relationships are obtained based on the conditions.\nObject profiling is dynamically done and it has results and experiments section where visualization of statistics can be done.")
        textArea2.setStyleSheet("background-color : rgba(255,0,0,10%);")
        textArea2.setFont(QFont("Arial",20))
        textArea2.setReadOnly(True)
        textArea2.setFixedSize(350, 250)
        buttonLayout.addWidget(textArea2, 1, 1)
        self.envi = QPushButton("Environment")
        self.envi.setStyleSheet("border: 2px solid black;background-color: rgba(81,102,109,20%);border-radius:10px;")
        self.envi.setFont(QFont("Arial", 20))
        buttonLayout.addWidget(self.envi,0,2)
        textArea3 = QTextEdit()
        textArea3.setText("User can load applications to devices and add services to it.\nObject profiling is done dynamically and it has results and experiments section where visualization of statistics can be done.")
        textArea3.setStyleSheet("background-color : rgba(255,0,0,10%);")
        textArea3.setFont(QFont("Arial", 20))
        textArea3.setReadOnly(True)
        textArea3.setFixedSize(350, 250)
        buttonLayout.addWidget(textArea3, 1, 2)

        label_image1= QLabel(self)
        self.pixmap = QPixmap('mainpage_images/pic1.jpg')
        label_image1.setPixmap(self.pixmap)
        label_image1.setScaledContents(True)
        label_image1.setFixedSize(350,250)
        buttonLayout.addWidget(label_image1,2, 0)

        label_image2 = QLabel(self)
        self.pixmap = QPixmap('mainpage_images/pic2.png')
        label_image2.setPixmap(self.pixmap)
        label_image2.setScaledContents(True)
        label_image2.setFixedSize(350,250)
        buttonLayout.addWidget(label_image2, 2, 1)

        label_image3 = QLabel(self)
        self.pixmap = QPixmap('mainpage_images/pic3.png')
        label_image3.setPixmap(self.pixmap)
        label_image3.setScaledContents(True)
        label_image3.setFixedSize(350,250)
        buttonLayout.addWidget(label_image3, 2, 2)

        footerLayout= QVBoxLayout()
        #footerLayout.resize(self.width(), self.height())
        label3= QLabel("Developers:\nG SaiCharan\nK Shreya Rao\nPrithvi Kumar B.V\nVrinda S Mirji")
        label3.setFont(QFont("Arial",15))
        label3.setAlignment(Qt.AlignRight)
        label4 = QLabel("Guided by:\nDr. S.P. Shiva Prakash")
        label4.setFont(QFont("Arial", 15))
        footerLayout.addWidget(label4)
        footerLayout.addWidget(label3)

        self.static.clicked.connect(self.static_button)
        self.dynamic.clicked.connect(self.dynamic_button)
        self.envi.clicked.connect(self.envi_button)

        vLayout= QVBoxLayout()

        vLayout.addLayout(headingLayout)
        vLayout.addLayout(buttonLayout)
        vLayout.addLayout(footerLayout)

        layout.addLayout(vLayout,0,0)

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

        # creating a edit menu bar
        edit_menu = self.menuBar().addMenu("&Edit Relationship Preferences")
        #relationship
        self.rel_action = QAction("Change relationship parameters")
        # adding status tip
        self.rel_action.setStatusTip("Change relationship parameters")
        # when triggered undo the editor
        self.rel_action.triggered.connect(self.rel_open)
        edit_menu.addAction(self.rel_action)

        # creating a file menu bar
        file_menu = self.menuBar().addMenu("&Select Folder to Upload")
        open_file_action = QAction("Open Folder", self)
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)

        # creating a help menu bar
        help_menu = self.menuBar().addMenu("&Help")
        open_help_action = QAction("Help", self)
        open_help_action.triggered.connect(self.help_open)
        help_menu.addAction(open_help_action)


        scrollArea = QScrollArea()
        widget = QWidget()
        widget.setLayout(layout)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(widget)
        self.setCentralWidget(scrollArea)
        # self.setLayout(layout)
        self.showMaximized()
        self.response = False
    #To exit notification
    def closeEvent(self,event):
        message = QMessageBox.question(self,"Message","Do you want to continue ?",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)

        if message == QMessageBox.Yes:
            self.response = True
            event.accept()
        else:
            self.response = False
            event.ignore()


    # action called by help open action
    def help_open(self):
        QMessageBox.information(self,"HELP","1.    Existing model button is used to access the simulator layout of the existing model.\n"
                                            "2.    Dynamic model button is used to access the simulator layout of the Dynamic model.\n"
                                            "3.    Environment model button is used to access the simulator layout of the environment model.")


    # action called by file open action
    def file_open(self):
        # getting path and bool value
        path = QFileDialog.getExistingDirectory(
            self, 'Select a directory', os.getcwd()+"/simulation_data")
        try:
            StatsModel.start(path)
        except:
            pass

    def rel_open(self):
        relLayout = RelationChange()
        # if executed
        if relLayout.exec_():
            print("Work")

    def static_button(self):
        main_page.close()
        if(self.response):
            StaticModel.start()
    def dynamic_button(self):
        main_page.close()
        if(self.response):
            DynamicModel.start()
    def envi_button(self):
        main_page.close()
        if(self.response):
            EnvironmentModel.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    global main_page
    main_page = Window()
    main_page.show()
    sys.exit(app.exec_())
