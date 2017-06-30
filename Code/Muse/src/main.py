#!/usr/bin/env python2.7
import logging
import sys
import threading

from PyQt4 import QtGui
from biosignals.EOG import EOG
from controller import Controller
from keyboard.MindType import MindType
from muse_server import PylibloServer

logging.basicConfig(level=logging.ERROR)


# Type sudo python main.py -p /dev/ttyUSB0

# Load the plugins from the plugin directory.

def process(biosignal, controller):
    while not controller.exited:
        # print("processing")
        if not biosignal.is_paused():
            biosignal.process()
            # print("processing")
        if biosignal.is_exit():
            controller.exited = True


def execute_board(muse_server, controller):
    timer = 0

    print("Execute-board")
    print("Starting board...")

    while not controller.exited:
        timer += 1
        if controller.instruction_request:
            if not controller.paused and not controller.made:
                muse_server.start()
                controller.make()


    controller.quit()
    muse_server.stop()


def make_gui(controller):
    app = QtGui.QApplication(sys.argv)
    mindType = MindType(controller)
    mindType.resize(550, 550)
    mindType.show()
    sys.exit(app.exec_())


def print_board_transmission_info(board):
    if board.daisy:
        print("Force daisy mode:")
    else:
        print("No daisy:")
        print(board.getNbEEGChannels(), "EEG channels and",
              board.getNbAUXChannels(), "AUX channels at",
              board.getSampleRate(), "Hz.")


if __name__ == '__main__':
    controller = Controller()
    eog = EOG(256, controller)
    muse_server = PylibloServer(eog)

    gui_thread = threading.Thread(target=make_gui, args=[controller])
    gui_thread.daemon = True
    gui_thread.start()

    process_thread = threading.Thread(target=process, args=[eog, controller])
    process_thread.start()

    execute_board(muse_server, controller)
