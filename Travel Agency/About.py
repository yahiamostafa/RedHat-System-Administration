from PyQt5.QtWidgets import QDialog , QApplication , QMessageBox
from PyQt5 import QtCore 

from PyQt5.uic import loadUi

class About (QDialog):
    def __init__(self , who):
        super().__init__()
        
        # load the UI 
        loadUi('about.ui' , self)

        # this variable identifies if we are taking about the developer or the Agency
        self.who = who

        # Set title to the window
        self.setWindowTitle(f"About {self.who}")

        # init the UI Elements
        self.initGUI()

    
    def initGUI(self):
        
        # set a backgroung image
        self.setStyleSheet("background-image : url(wallpaper.jpg);")

        # to add href
        self.label.setOpenExternalLinks(True)

        # to center the text
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        # Check if this page  is about the developer or the Agency
        if (self.who == 'Yahia'):
            self.label.setText(' <h3 style="color: white"> Hi This is Yahia Mostafa <br> The Developer of this Application \
               You can find more projects in my Github Repos</h3> <a href="http://github.com/yahiamostafa/" style="color: white ; font = 32px">Github</a>')
        else:
            self.label.setText(' <h3 style="color: white"> Hi This is GUC Travel Agency <br> For Any inquires \
               You can send us an email on  YahiaMostafa1000@gmail.com</h3>')