import sys  
from PyQt5 import QtCore 
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog , QApplication , QMessageBox  ,QHeaderView , QTableWidget , QTableWidgetItem , QVBoxLayout
from About import About
import pandas as pd

"""
Author : Yahia Mostafa
14/12/2022
"""

class Travel_Agency (QDialog):
    def __init__(self):
        super().__init__()
        
        # load the UI 
        loadUi('interface.ui' , self)

        # Set title to the window
        self.setWindowTitle("GUC Travel Agency")

        # init the UI Elements
        self.initGUI()


    def initGUI(self):

        # set a backgroung image
        self.setStyleSheet("background-image : url(wallpaper.jpg);")
        
        # insert the logo
        self.logo.setStyleSheet("background-image : url(logo.png);")
        self.logo.setScaledContents(True)


        # Set on ClickListener to Buttons
        self.exitBtn.clicked.connect(self.exit)
        self.aboutMeBtn.clicked.connect(self.aboutMe)
        self.aboutUsBtn.clicked.connect(self.aboutUs)
        self.flightsBtn.clicked.connect(self.flightsFn)
        self.airLinesBtn.clicked.connect(self.getAirLines)
        self.airPortsBtn.clicked.connect(self.getAirPorts)

    def getAirPorts(self):
        df = pd.read_csv('AirPorts.csv' , index_col= 0 )
        self.create_table(df)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

    def getAirLines(self):
        df = pd.read_csv('AirLines.csv' , index_col= 0 )
        self.create_table(df)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

    def flightsFn(self):
        # replce the old screen with the new one
        df = pd.read_csv('/home/yahia/sem9/Data Engineering/Milestone1/lookup_table.csv')
        self.create_table(df[:20])

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

    def aboutUs(self):
        # replace the old screen with the new One
        self.screen = About("Agency")
        self.screen.show()
        self.hide()

    def aboutMe(self):
        # replace the old screen with the new One
        self.screen = About("Yahia")
        self.screen.show()
        self.hide()



    # exit the app when the user click on the exit Button
    def exit(self):
        # init a QmessageBox
        dlg = QMessageBox(self)

        # set a title 
        dlg.setWindowTitle("Exit!")

        # set text
        dlg.setText("Do you want to exit?")

        # set Yes or no Buttons
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # set an icon
        dlg.setIcon(QMessageBox.Question)

        # set a color 
        dlg.setStyleSheet("color : white")


        button = dlg.exec()

        if button == QMessageBox.Yes:
            sys.exit(app.exec_())




    def create_table(self , df):

        # get the number of col and the number of rows
        rows = df.shape[0]
        cols = df.shape[1]

        # create the table object
        self.tableWidget = QTableWidget()

        #set the number of rows
        self.tableWidget.setRowCount(rows) 

        # add a background-image
        self.tableWidget.setStyleSheet("background-image : url(table2.jpg);")
    
  
        #set the number ofColumns
        self.tableWidget.setColumnCount(cols)  

        # Identify the table Headers
        headers = df.columns.tolist()
  


        # iterate over the table 
        for col in range(cols):
            #iterate over each value in the row table
            for row in range(rows):
                self.tableWidget.setItem(row , col , QTableWidgetItem(str(df.iloc[row][col])))
        

        #Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        # set Headers
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

            








    

app = QApplication(sys.argv)
screen = Travel_Agency()
screen.show()
sys.exit(app.exec_())
