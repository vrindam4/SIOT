import sys

from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QPlainTextEdit, QVBoxLayout, QPushButton, QMessageBox
import StatsModel

class AppDemo(QWidget):
    def __init__(self,path,date):
        super().__init__()
        self.resize(1000, 800)
        self.path = path
        self.date = date
        mainLayout = QGridLayout()

        vLayout = QVBoxLayout()
        self.but = QPushButton("Save and Train")
        self.but.clicked.connect(self.onClicking)
        self.textArea = QPlainTextEdit()
        vLayout.addWidget(self.textArea)
        vLayout.addWidget(self.but)

        file = "TrainingEditCode.py"
        out_text =""
        with open(file,'r') as file:
            for line in file:
                out_text = out_text+line
        self.textArea.setPlainText(out_text)

        mainLayout.addLayout(vLayout,0,0)


        self.setWindowTitle('Training Editor')
        self.setLayout(mainLayout)
        self.showMaximized()

    def onClicking(self):
        file = "TrainingEditCode.py"
        with open(file,'w') as myfile:
            myfile.write(self.textArea.toPlainText())
        try:
            import TrainingEditCode
            TrainingEditCode.training(self.path)
            temp = StatsModel.start(self.date)
            main_page.close()
        except Exception as e:
            QMessageBox.critical(self,"ERROR","Error in traing code : "+str(e))
            temp = StatsModel.start(self.date)
            main_page.close()

class AppDemoNavigation(QWidget):
    def __init__(self,path,date):
        super().__init__()
        self.resize(1000, 800)
        self.path = path
        self.date = date
        mainLayout = QGridLayout()

        vLayout = QVBoxLayout()
        self.but = QPushButton("Save and Plot")
        self.but.clicked.connect(self.onClicking)
        self.textArea = QPlainTextEdit()

        # self.canvas = Canvas(self, width=10, height=13)
        # self.toolbar = NavigationToolbar(self.canvas, self)

        vLayout.addWidget(self.textArea)
        vLayout.addWidget(self.but)
        # vLayout.addWidget(self.canvas)
        # vLayout.addWidget(self.toolbar)

        file = "NavigationEditCode.py"
        out_text =""
        with open(file,'r') as file:
            for line in file:
                out_text = out_text+line
        self.textArea.setPlainText(out_text)

        mainLayout.addLayout(vLayout,0,0)


        self.setWindowTitle('Training Editor')
        self.setLayout(mainLayout)
        self.showMaximized()

    def onClicking(self):
        file = "NavigationEditCode.py"
        with open(file,'w') as myfile:
            myfile.write(self.textArea.toPlainText())
        try:
            import NavigationEditCode
            statsLayout  = StatsModel.start(self.date)
            NavigationEditCode.navigation_plot(self.path,statsLayout)
            main_page.close()
        except Exception as e:
            QMessageBox.critical(self,"ERROR","Error in traing code : "+str(e))
            statsLayout  = StatsModel.start(self.date)
            main_page.close()

def start_navigation(path,date):
    global main_page
    main_page = AppDemoNavigation(path,date)
    main_page.show()

def start(path,date):
    global main_page
    main_page = AppDemo(path,date)
    main_page.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    global main_page
    main_page = AppDemo()
    main_page.show()
    sys.exit(app.exec_())
