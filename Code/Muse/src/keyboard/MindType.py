from PyQt4 import QtGui

# Sayan sucks; don't complain - yours truly Abdel and Scholar
# ^ Sayan is
from Keyboard import Keyboard


class MindType(QtGui.QWidget):
    def __init__(self, controller):
        super(MindType, self).__init__()

        # variables used for pausing
        self.controller = controller
        self.interval = 100

        # Creating main panel which contains everything
        self.main_panel = QtGui.QVBoxLayout()
        self.main_panel.setContentsMargins(0, 0, 0, 0)

        # creating header panel which has start, pause/resume and text display
        self.header_panel = QtGui.QHBoxLayout()
        self.main_panel.addLayout(self.header_panel)

        # creating header panel buttons
        self.character_display_panel = QtGui.QLabel("Enter Text!")
        self.start_button = QtGui.QPushButton("Start")
        self.end_button = QtGui.QPushButton("Pause")

        # setting button click listeners
        self.start_button.clicked.connect(self.start())
        self.end_button.clicked.connect(self.pause_resume())

        # adding buttons to header panel
        self.header_panel.addWidget(self.character_display_panel)
        self.header_panel.addWidget(self.start_button)
        self.header_panel.addWidget(self.end_button)

        # adding keyboard gui to main panel
        # creating a button grid
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(0)
        self.keyboard = Keyboard(self.main_panel, self.character_display_panel, self.interval)

        # setting layout to main_panel
        self.setLayout(self.main_panel)

    # signal functions (on click listeners)
    # -------------------------------------
    def start(self):
        def start_function():
            # setting / resetting variables
            self.start_button.setDisabled(True)
            self.controller.resume()
            print(self.controller)
            self.keyboard.start()

        return start_function

    def pause_resume(self):
        # print("Pause resume")

        def pause_resume_function():

            button_pause_resume = self.end_button
            print("Before pause-resume")
            print(self.controller)
            if button_pause_resume.text() == "Pause":
                button_pause_resume.setText("Resume")
                self.controller.pause()
                self.keyboard.pause()
            else:
                button_pause_resume.setText("Pause")
                self.controller.resume()
                self.keyboard.resume()
            print("After pause-resume")
            print(self.controller)

        return pause_resume_function

    def closeEvent(self, event):
        self.controller.quit()
        print("Exiting...")
        event.accept()