#!/usr/bin/python
# The GUI interface for connecting to the muse
# Using PyQt and pyqtgraph
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import sys, time

# refer to file: MuseApp/server.py
from server import *

# Default settings
# PORT = 1234
# LENGTH = 1100

class Window(QtGui.QWidget):

    # Main Window ***********************************************************
    def __init__(self):
        # Initializing QtGui.QWidget
        super(Window, self).__init__()
        self.setWindowTitle("MuseApp")
        self.setGeometry(50,200, 800, 500)

        # Widgets **************************************************************
            # Textboxes and Labels
        self.portLabel = QtGui.QLabel("Port:")
        self.portEdit = QtGui.QLineEdit()
        self.portEdit.setText("1234")
        self.windowLabel = QtGui.QLabel("Window:")
        self.windowEdit = QtGui.QLineEdit()
        self.windowEdit.setText("1100")
            # Default textbox values
        self.PORT = 1234
        self.LENGTH = 1100
            # Buttons
        self.btnStartServer = QtGui.QPushButton("Start Server", self)
        self.btnUpdateWindow = QtGui.QPushButton("Update Window", self)
        self.btnPlayPause = QtGui.QPushButton("Pause", self)
        self.btnQuit = QtGui.QPushButton("Quit", self)

        # Graphing *************************************************************
            # Plot Widget (pw)
        self.pw = pg.PlotWidget(self)
        self.pw.showGrid(x=True, y=True)
        self.pw.setDownsampling(mode='peak')
        self.pw.setClipToView(True)
        # self.pw.setRange(yRange=[200,1400])
            # Plot details
        self.curve_le = self.pw.plot(pen='r')
        self.curve_lf = self.pw.plot(pen='g')
        self.curve_rf = self.pw.plot(pen='b')
        self.curve_re = self.pw.plot(pen='w')
            # Timer for updating Graph
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.graphUpdate)

        # Widget Layouts *******************************************************
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.portLabel, 0, 0)
        self.layout.addWidget(self.portEdit, 0, 1)
        self.layout.addWidget(self.btnStartServer, 0, 2)
        self.layout.addWidget(self.windowLabel, 1, 0)
        self.layout.addWidget(self.windowEdit, 1, 1)
        self.layout.addWidget(self.btnUpdateWindow, 1, 2)
        self.layout.addWidget(self.btnPlayPause, 2, 1)
        self.layout.addWidget(self.btnQuit, 2, 2)
        self.layout.addWidget(self.pw, 3, 0, 1,3)

        # Widget Interactions **************************************************
        self.btnStartServer.clicked.connect(self.startServer)
        self.btnUpdateWindow.clicked.connect(self.updateWindow)
        self.btnQuit.clicked.connect(self.closeApp)
        self.btnPlayPause.clicked.connect(self.playPause)

        # Display **************************************************************
        self.show()

    # member functions *********************************************************
    # Creates connection to muse_server
    def startServer(self):
        try:
            # Captures input from textbox
            self.PORT = int(self.portEdit.text())
        except TypeError:
            return
        try:
            # Trys to connect to server
            self.muse_server = PylibloServer(self.PORT)
        except ServerError, err:
            # print >> sys.stderr, str(err)
            # sys.exit()
            return
        # start server and block server entry
        self.portEdit.setDisabled(True)
        self.btnStartServer.setDisabled(True)
        self.muse_server.start()
        # Start timer Update Graph
        self.timer.start()

    # called by timer to update each electrode graph
    def graphUpdate(self):
        self.curve_le.setData(self.muse_server.EEG.l_ear)
        self.curve_lf.setData(self.muse_server.EEG.l_forehead)
        self.curve_rf.setData(self.muse_server.EEG.r_forehead)
        self.curve_re.setData(self.muse_server.EEG.r_ear)
        # 20 times a second
        time.sleep(0.05)

    # Rejust plot area, useful later for FFT window
    def updateWindow(self):
        try:
            self.tempLength = int(self.windowEdit.text())
        except TypeError:
            return
        self.LENGTH = self.tempLength
        self.muse_server.set_window(self.LENGTH)

    # Used to pause or restart stream
    def playPause(self):
        # If timer is active and button pressed
        # stop timer
        # Change Pause button to Start
        # else the other way around
        if self.timer.isActive():
            self.timer.stop()
            self.btnPlayPause.setStyleSheet(
            'QPushButton {background-color: #ffffff; color: black;}')
            self.btnPlayPause.setText('Start')
        else:
            self.timer.start()
            self.btnPlayPause.setStyleSheet(
            'QPushButton {background-color: #dddddd; color: black;}')
            self.btnPlayPause.setText('Pause')

    # Crashes when running muse_server.stop()
    # Therefore will have to quit program and connect to server again
    def closeApp(self):
        pg.exit()

# Main function ****************************************************************
if __name__ == "__main__":

    # Run the app
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
