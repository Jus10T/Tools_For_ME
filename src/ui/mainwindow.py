import sys
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QFrame, QSplitter,
                             QStackedWidget, QLabel, QPushButton)

from src.ui.pages.thermopage import ThermoPage
from src.ui.pages.unitspage import UnitSolverPage
from src.ui.pages.beampage import BeamPage
from src.ui.pages.ohmspage import OhmPage
from src.ui.style.pagestyling import update_sidebar_styles


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setup_Window()
        update_sidebar_styles(self, 0, self.sidebuttons)

    def setup_Window(self):
         self.setGeometry(150,150,1100,700)
         self.setWindowTitle("Tools For ME")


    def setupUI(self):
         central_widget = QWidget()
         self.setCentralWidget(central_widget)
         central_widget.setObjectName("centralwidget")

         #main layout
         main_layout = QHBoxLayout(central_widget)
         main_layout.setContentsMargins(25, 25, 25, 25)
         main_layout.setSpacing(15)
         splitter = QSplitter(Qt.Orientation.Horizontal)
         
        


         #create sidebar and add to layout
         self.sidebar_widget = self.create_sidebar()
         splitter.addWidget(self.sidebar_widget)
         

         #add content area to layout
         self.main_content_widget = self.create_content_area()
         splitter.addWidget(self.main_content_widget)
         main_layout.addWidget(splitter)



    

    def create_sidebar(self):
        #frame
        sidebar = QFrame()
        sidebar.setFrameStyle(QFrame.Shape.StyledPanel)
        sidebar.setMaximumWidth(275)
        #sidebar V layout
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(5,5,5,5)
        sidebar_layout.setSpacing(10)

        #sidebar heading H layout
        sidebar_heading_layout = QHBoxLayout()
        sidebar_heading_layout.setContentsMargins(5, 10, 20, 0)
        sidebar_heading_layout.setSpacing(10)

        #side heading text
        sidebar_heading_text = QLabel("Tools")
        sidebar_heading_text.setObjectName("sidebarHeadingtext")
        sidebar_heading_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sidebar_heading_text.setMaximumHeight(40)


        #heading pixmap
        sidebar_icon = QLabel()
        sidebar_icon.setPixmap(QPixmap("Equations-for-ME/assets/icons/gearcalc.ico"))

        #add icon and text to horizontal
        sidebar_heading_layout.addWidget(sidebar_icon)
        #sidebar_heading_layout.addWidget(sidebar_heading_text)
        #sidebar_heading_layout.addStretch()
        sidebar_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)


        #add H to V
        sidebar_layout.addLayout(sidebar_heading_layout)



        #create sidebar buttons
        self.unitbutton = QPushButton("- Units")
        self.thermobutton  = QPushButton("- Thermodynamics")
        self.beamsbutton = QPushButton("- Beams")
        self.ohmbutton = QPushButton("- Ohm's Law")

        #for button style    
        self.sidebuttons = [self.unitbutton, self.thermobutton, self.beamsbutton, self.ohmbutton]

        

        #add buttons to layout
        sidebar_layout.addWidget(self.unitbutton)
        sidebar_layout.addWidget(self.thermobutton)
        sidebar_layout.addWidget(self.beamsbutton)
        sidebar_layout.addWidget(self.ohmbutton)

        #connect buttons to page switching
        self.unitbutton.clicked.connect(lambda: self.switchPage(0))
        self.thermobutton.clicked.connect(lambda: self.switchPage(1))
        self.beamsbutton.clicked.connect(lambda: self.switchPage(2))
        self.ohmbutton.clicked.connect(lambda: self.switchPage(3))

        #add stretch after buttons
        sidebar_layout.addStretch()



    
        return sidebar


    def create_content_area(self):
        #create frame and stack
        content_frame = QFrame()
        self.main_content_stack = QStackedWidget()

        content_frame.setFrameStyle(QFrame.Shape.StyledPanel)


        #make main layout and add stack to it
        center_layout = QVBoxLayout(content_frame)
        center_layout.addWidget(self.main_content_stack)

        #create pages
        self.unitpage = UnitSolverPage()
        self.thermopage = ThermoPage()
        self.beampage = BeamPage()
        self.ohmpage = OhmPage()

        #add pages to stack
        self.main_content_stack.addWidget(self.unitpage)
        self.main_content_stack.addWidget(self.thermopage)
        self.main_content_stack.addWidget(self.beampage)
        self.main_content_stack.addWidget(self.ohmpage)

        return content_frame
    
    



    def switchPage(self, index):
        self.main_content_stack.setCurrentIndex(index)
        update_sidebar_styles(self, index, self.sidebuttons)
